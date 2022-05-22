import asyncio
from typing import Optional


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        # обязательный параметр, в _task нужно положить запущенную корутину поллера
        self._task: Optional[asyncio.Task] = None
        raise NotImplementedError

    async def _worker(self):
        """
        нужно получать данные из tg, стоит использовать метод get_updates_in_objects
        полученные сообщения нужно положить в очередь queue
        в очередь queue нужно класть UpdateObj
        """
        raise NotImplementedError

    def start(self):
        """
        нужно запустить корутину _worker
        """
        raise NotImplementedError

    async def stop(self):
        """
        нужно отменить корутину _worker и дождаться ее отмены
        """
        raise NotImplementedError
