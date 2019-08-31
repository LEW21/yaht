from yaht.formats import json_data

from yaml import safe_load, safe_dump


def unserialize(type, value):
    data = safe_load(value.decode('utf-8'))
    return json_data.unserialize(type, data)


def serialize(value):
	data = json_data.serialize(value)
	return safe_dump(data).encode('utf-8')
