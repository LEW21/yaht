from yaht.formats import json_data

from yaml import safe_load, safe_dump


def unserialize(type: type, serialized_value: bytes):
    data = safe_load(serialized_value.decode('utf-8'))
    return json_data.unserialize(type, data)


def serialize(value) -> bytes:
	data = json_data.serialize(value)
	return safe_dump(data).encode('utf-8')
