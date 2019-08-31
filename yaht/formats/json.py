from yaht.formats import json_data

from json import loads, dumps


def unserialize(type, serialized_value):
	data = loads(serialized_value.decode('utf-8'))
	return json_data.unserialize(type, data)


def serialize(value):
	data = json_data.serialize(value)
	return dumps(data).encode('utf-8')
