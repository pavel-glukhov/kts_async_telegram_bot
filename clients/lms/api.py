from json import JSONDecodeError
from typing import Tuple

from aiohttp import ClientResponse

from clients.base import ClientError, Client


class LmsClientError(ClientError):
    def __str__(self):
        return f"status: [{self.response.status}]: error:{self.content}"


class LmsClient(Client):
    BASE_PATH = 'https://lms.metaclass.kts.studio/'

    def __init__(self, token: str):
        self.token: str = token
        super().__init__()

    async def _handle_response(self, resp):
        if resp.status != 200:
            raise LmsClientError(response=resp)

        try:
            return resp, await resp.json()
        except JSONDecodeError as er:
            raise LmsClientError(resp, er)

    def get_path(self, url: str) -> str:
        return f'{self.get_base_path()}{url}'

    async def get_user_current(self) -> dict:
        url = '/api/v2.user.current'
        cookies = {
            'sessionid': self.token
        }

        data = await self._perform_request('get',
                                           url=self.get_path(url),
                                           cookies=cookies)
        return data[1]

    async def login(self, email: str, password: str) -> str:
        url = '/api/v2.user.login'

        payload = {
            'email': email,
            'password': password
        }

        data = await self._perform_request('post', url=self.get_path(url),
                                           json=payload)
        str_ = data[0].headers.get('Set-Cookie')
        if not str_:
            raise LmsClientError(data)

        token = str_.split(';')[0][10:]
        return token
