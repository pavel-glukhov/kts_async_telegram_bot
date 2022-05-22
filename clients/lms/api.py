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
            data = await resp.json()
        except JSONDecodeError as er:
            raise LmsClientError(resp, er)

        return resp, data

    def get_path(self, url: str) -> str:
        return f'{self.get_base_path()}{url}'

    async def get_user_current(self) -> dict:
        url = '/api/v2.user.current'
        cookies = {
            'sessionid': self.token
        }

        resp, data = await self._perform_request('get',
                                                 url=self.get_path(url),
                                                 cookies=cookies)
        return data

    async def login(self, email: str, password: str) -> str:
        url = '/api/v2.user.login'

        payload = {
            'email': email,
            'password': password
        }

        resp, data = await self._perform_request('post', url=self.get_path(url),
                                                 json=payload)

        sessionid = resp.cookies.get('sessionid')
        if not sessionid:
            raise LmsClientError(resp, await resp.text())

        return sessionid.value
