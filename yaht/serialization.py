from typing import Any, Type, TypeVar

from yaht.core import TypedBytes
from yaht.formats import byte_formats

T = TypeVar('T')


def unserialize(type: Type[T], tb: TypedBytes) -> T:
    mime_type = tb.type
    encoding = mime_type.rpartition('/')[2].rpartition('+')[2]
    return byte_formats[encoding]().unserialize(type, tb.value)


def serialize(value: Any, mime_type: str) -> bytes:
    encoding = mime_type.rpartition('/')[2].rpartition('+')[2]
    return byte_formats[encoding]().serialize(value)
