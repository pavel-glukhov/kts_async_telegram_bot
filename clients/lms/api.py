from typing import Tuple

from aiohttp import ClientResponse

from clients.base import ClientError, Client


class LmsClientError(ClientError):
    pass


class LmsClient(Client):
    BASE_PATH = ''

    def __init__(self, token: str):
        raise NotImplementedError

    async def _handle_response(self, resp: ClientResponse) -> Tuple[dict, ClientResponse]:
        raise NotImplementedError

    async def get_user_current(self) -> dict:
        raise NotImplementedError

    async def login(self, email: str, password: str) -> str:
        raise NotImplementedError
