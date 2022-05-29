import asyncio
from dataclasses import dataclass
from typing import List
from clients.fapi.s3 import S3Client
from clients.fapi.tg import TgClientWithFile
from clients.tg.api import TgClient
from clients.tg.dcs import UpdateObj, File


@dataclass
class WorkerConfig:
    endpoint_url: str
    aws_secret_access_key: str
    aws_access_key_id: str
    bucket: str
    concurrent_workers: int = 1


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, config: WorkerConfig):
        self.config = config
        self.queue = queue
        self.tg = TgClient(token)
        # обязательный параметр, в него нужно сохранить запущенные корутины воркера
        self._tasks: List[asyncio.Task] = []
        # обязательный параметр, выполнять работу с s3 нужно через объект класса self.s3
        # для загрузки файла нужно использовать функцию fetch_and_upload или stream_upload
        self.s3 = S3Client(
            endpoint_url=config.endpoint_url,
            aws_secret_access_key=config.aws_secret_access_key,
            aws_access_key_id=config.aws_access_key_id
        )
        self.is_running = False
        self.is_first_msg = True
        self.ftg = TgClientWithFile(token)

    async def handle_update(self, upd: UpdateObj):
        if self.is_first_msg:
            self.is_first_msg = False
            await self.tg.send_message(upd.message.chat.id, '[greeting]')

        else:
            if not upd.message.document:
                await self.tg.send_message(upd.message.chat.id, '[document is required]')
            else:
                await self.tg.send_message(upd.message.chat.id, '[document]')
                file = await self.ftg.get_file(upd.message.document.file_id)
                await self.s3.stream_file(self.config.bucket, upd.message.document.file_name, file.file_path)
                await self.tg.send_message(upd.message.chat.id, '[document has been saved]')

    async def _worker(self):
        while self.is_running:
            upd: UpdateObj = await self.queue.get()
            await self.handle_update(upd)
            self.queue.task_done()

    def start(self):
        """
        должен запустить столько воркеров, сколько указано в config.concurrent_workers
        запущенные задачи нужно положить в _tasks
        """
        self.is_running = True
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.config.concurrent_workers)]

    async def stop(self):
        self.is_running = False
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
