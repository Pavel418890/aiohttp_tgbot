from dataclasses import field
from typing import ClassVar, Type, List, Optional, Any

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class FileInfo:
    file_id: str
    file_size: int
    file_unique_id: str


@dataclass
class File(FileInfo):
    file_path: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Document(FileInfo):
    file_name: str
    mime_type: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class MessageFrom:
    id: int
    first_name: str
    username: str
    last_name: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: Optional[str] = None
    document: Optional[Document] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    update_id: int
    message: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class OkStatusResponse:
    ok: bool
    result: Any

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse(OkStatusResponse):
    result: Optional[List[Update]] = field(default_factory=list)


@dataclass
class GetFileResponse(OkStatusResponse):
    result: File


@dataclass
class MessageResponse(OkStatusResponse):
    result: Message
