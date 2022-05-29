from typing import ClassVar, Type, List, Optional
from dataclasses import field
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass
class From:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str
    language_code: Optional[str]


@dataclass
class File:
    file_name: Optional[str]
    mime_type: Optional[str]
    thumb: Optional[dict]
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: Optional[str]
    duration: Optional[int]


@dataclass
class Message:
    message_id: int
    from_: From = field(metadata={'data_key': 'from'})
    chat: Chat
    date: int
    text: Optional[str]
    document: Optional[File]
    animation: Optional[File]
    entities: Optional[list]


@dataclass
class UpdateObj:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetFileResponse:
    ok: bool
    result: File

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
