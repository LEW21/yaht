from typing import Any

from yaht.core import TypedBytes
from yaht.formats import byte_formats


def unserialize(type: type, tb: TypedBytes):
    mime_type = tb.type
    encoding = mime_type.rpartition('/')[2].rpartition('+')[2]
    return byte_formats[encoding]().unserialize(type, tb.value)


def serialize(value: Any, mime_type: str):
    encoding = mime_type.rpartition('/')[2].rpartition('+')[2]
    return byte_formats[encoding]().serialize(value)
