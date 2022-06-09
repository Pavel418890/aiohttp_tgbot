from dataclasses import field
import datetime

import dateutil.tz
from dateutil.tz import tzutc, tzlocal
from typing import ClassVar, Type, Any, Mapping, Optional

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE, fields, ValidationError, missing


class DatetimeLocal(fields.Field):
    def _deserialize(
            self,
            value: Any,
            attr: str | None,
            data: Mapping[str, Any] | None,
            **kwargs,
    ):
        try:
            return datetime.datetime.astimezone(value, tz=tzlocal())
        except Exception:
            raise ValidationError("Invalid datetime object %s" % value)

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        if value is None:
            return missing
        return value.strftime("%y-%m-%d %H:%M:%S %Z")


Schema.TYPE_MAPPING[datetime.datetime] = DatetimeLocal


@dataclass
class Owner:
    ID: str
    DisplayName: Optional[str]


@dataclass
class Content:
    Key: str
    ETag: str
    Size: int
    StorageClass: str
    Owner: Owner
    LastModified: datetime.datetime = field(default=None)


@dataclass
class ResponseMetadata:
    HTTPHeaders: dict
    HTTPStatusCode: int
    HostId: str
    RequestId: str
    RetryAttempts: int


@dataclass
class MultipartUploadToBucketResponse:
    Bucket: str
    ETag: str
    Key: str
    Location: str
    ResponseMetadata: ResponseMetadata

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class ListFilesResponse:
    IsTruncated: bool
    Marker: str
    Name: str
    Prefix: str
    MaxKeys: int
    EncodingType: str
    ResponseMetadata: ResponseMetadata
    Contents: Optional[list[Content]] = field(default_factory=list)

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
