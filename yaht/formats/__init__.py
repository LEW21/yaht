from importlib import import_module

byte_formats = dict(
    json = lambda: import_module('yaht.formats.json'),
    yaml = lambda: import_module('yaht.formats.yaml'),
)
