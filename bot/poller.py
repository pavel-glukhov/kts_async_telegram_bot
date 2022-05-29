import asyncio
from typing import Optional
from clients.tg.api import TgClient


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        self.tg = TgClient(token)
        self.queue = queue
        self._is_running: bool = False
        self._task: Optional[asyncio.Task] = None
        self.offset: int = 0
        self.timeout: int = 60

    async def _worker(self):

        while self._is_running:
            kw = {'offset': self.offset, 'timeout': self.timeout}
            messages = await self.tg.get_updates_in_objects(**kw)
            for message in messages:
                self.queue.put_nowait(message)
                self.offset = message.update_id + 1

    def start(self):
        self._is_running = True
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        self._is_running = False
        self._task.cancel()
