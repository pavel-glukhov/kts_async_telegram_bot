from json import JSONDecodeError
from typing import Optional, List, Any, ClassVar, Type

from marshmallow import ValidationError
from clients.base import ClientError, Client
from clients.tg.dcs import UpdateObj, Message, GetUpdatesResponse, \
    SendMessageResponse


class TgClientError(ClientError):
    def __str__(self):
        return f"status: [{self.response.status}]: error:{self.content}"


class TgClient(Client):
    BASE_PATH = 'https://api.telegram.org'

    def __init__(self, token: str = ''):
        self.token = token
        super().__init__()

    def get_path(self, url: str) -> str:
        return f'{self.get_base_path()}/bot{self.token}/{url}'

    def get_file_path(self, url: str) -> str:
        return f'{self.get_base_path()}/file/bot{self.token}/{url}'

    async def _handle_response(self, resp):
        if resp.status != 200:
            raise TgClientError(response=resp)

        if resp.content_type != 'application/json':
            return resp, None

        try:
            data = await resp.json()
            return resp, data

        except JSONDecodeError as er:
            raise TgClientError(resp, er)

    async def get_me(self) -> dict:
        resp, data = await self._perform_request('get', self.get_path('getMe'))
        return data

    async def get_updates(self, offset: Optional[int] = None,
                          timeout: int = 0) -> dict:
        request: list = []
        if offset:
            request.append(f'offset={offset}')
        if timeout:
            request.append(f'timeout={timeout}')

        request_url = 'getUpdates?' + '&'.join(request)
        resp, data = await self._perform_request(
            'get',
            self.get_path(request_url),
            timeout=timeout
        )
        return data

    async def get_updates_in_objects(self, *args, **kwargs) -> List[UpdateObj]:
        data = await self.get_updates(*args, **kwargs)

        try:
            obj = GetUpdatesResponse.Schema().load(data)
        except ValidationError as er:
            raise TgClientError(data, content=er)

        return obj.result

    async def send_message(self, chat_id: int, text: str) -> Message:

        payload = {
            'chat_id': chat_id,
            'text': text
        }

        resp, data = await self._perform_request('post',
                                                 self.get_path('sendMessage'),
                                                 json=payload)

        obj = SendMessageResponse.Schema().load(data=data)

        return obj.result
