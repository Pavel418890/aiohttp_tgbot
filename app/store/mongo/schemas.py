from dataclasses import field
from enum import Enum

import bson
from typing import Optional, Any, Mapping, Callable

from marshmallow_dataclass import dataclass
from marshmallow import fields, EXCLUDE, Schema, ValidationError, missing


class ObjectIdField(fields.Field):
    def deserialize(
            self,
            value: Any,
            attr: str | None = None,
            data: Mapping[str, Any] | None = None,
            **kwargs,
    ):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError("Invalid ObjectId %s" % value)

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        if value is None:
            return missing
        return str(value)


Schema.TYPE_MAPPING[bson.ObjectId] = ObjectIdField


