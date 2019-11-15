from importlib import import_module
from typing import cast

class Format:
    @staticmethod
    def serialize(value) -> bytes:
        return b''

    @staticmethod
    def unserialize(type: type, serialized_value: bytes):
        return

byte_formats = dict(
    json = lambda: cast(Format, import_module('yaht.formats.json')),
    yaml = lambda: cast(Format, import_module('yaht.formats.yaml')),
)
