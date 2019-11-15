from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence, Union, Type, TYPE_CHECKING
from warnings import warn

from importlib import resources
from typing_extensions import Literal

from yaht.auto import Auto
from yaht.core import TypedBytes


class Undefined:
    def __repr__(self):
        return 'undefined'


class SchemaDocument:
    def __init__(self, schema: Schema):
        self.document = schema
        if isinstance(self.document.definitions, Auto):
            self.document.definitions = self.document.definitions._data

    def to_type(self, schema: Schema, override_type = None):
        assert not isinstance(schema, dict)
        undefined = Undefined()

        ref = getattr(schema, '$ref', undefined)
        if ref is not undefined:
            if ref == '#':
                # TODO Recursion
                return Any

            assert ref.startswith('#/definitions/')
            def_name = ref[len('#/definitions/'):]
            return self.to_type(self.document.definitions[def_name])

        if schema == True:
            return Any

        const = getattr(schema, 'const', undefined)
        if const is not undefined:
            if const is None:
                return type(None)
            else:
                return Literal[const]

        anyOf = getattr(schema, 'anyOf', undefined)
        if anyOf is not undefined:
            return Union[tuple(self.to_type(subschema) for subschema in anyOf)]

        schema_type = override_type or getattr(schema, 'type', undefined)

        if isinstance(schema_type, list):
            return Union[tuple(self.to_type(schema, override_type = single_type) for single_type in schema_type)]

        if schema_type == 'null':
            return type(None)
        if schema_type == 'boolean':
            return bool
        if schema_type == 'integer':
            return int
        if schema_type == 'number':
            return float
        if schema_type == 'string':
            format = getattr(schema, 'format', None)
            if format == 'date-time':
                return datetime
            return str

        if schema_type == 'object':
            properties = getattr(schema, 'properties', undefined)
            additionalProperties = getattr(schema, 'additionalProperties', undefined)

            if properties is not undefined and additionalProperties is not undefined:
                raise NotImplementedError('Handling both properties and additionalProperties on a single object is not implemented.')

            if properties is not undefined:
                if isinstance(properties, Auto):
                    properties = properties._data
                property_types = dict()
                default_values = dict()
                for prop_name, prop_schema in properties.items():
                    property_types[prop_name] = self.to_type(prop_schema)
                    default = getattr(prop_schema, 'default', undefined)
                    if default is not undefined:
                        default_values[prop_name] = default

                def __init__(self, **kwargs):
                    unknown_kwargs = set(kwargs.keys()) - set(type(self).__annotations__.keys())
                    if unknown_kwargs != set():
                        raise TypeError(f'{type(self).__name__} got unexpected properties: {", ".join(unknown_kwargs)}')

                    for prop_name, prop_type in type(self).__annotations__.items():
                        if prop_name in kwargs:
                            setattr(self, prop_name, kwargs[prop_name])

                def __str__(self):
                    return f'{type(self).__name__} {self.__dict__}'

                Patch = type((schema.title or '') + 'Patch', (), dict(
                    __annotations__ = property_types,
                    __resttest_plain__ = True,
                    __resttest_schema__ = schema,
                    __init__ = __init__,
                    __str__ = __str__,
                    __repr__ = __str__,
                ))

                Full = type(schema.title or '', (Patch,), dict(
                    Patch = Patch,
                    **default_values,
                ))

                def __init__(self, **kwargs):
                    missing_kwargs = set(type(self).__annotations__.keys()) - set(kwargs.keys()) - set(type(self).__dict__.keys())
                    if missing_kwargs != set():
                        raise TypeError(f'{type(self).__name__} missing required properties: {", ".join(missing_kwargs)}')

                    super(Full, self).__init__(**kwargs)

                Full.__init__ = __init__

                return Full

            if additionalProperties is not undefined:
                return Mapping[str, self.to_type(additionalProperties)]

            warn(f"Untyped object: {schema}", UserWarning, 2)
            return dict

        if schema_type == 'array':
            items = getattr(schema, 'items', undefined)

            if items is not undefined:
                if isinstance(items, list):
                    raise NotImplementedError('Handling pre-set list items is not implemented.')

                return Sequence[self.to_type(items)]

            warn(f"Untyped array: {schema}", UserWarning, 2)
            return list

        warn(f"Untyped value: {schema}", UserWarning, 2)
        return Any


def schema_to_type(top_level_schema: Schema, chosen_schema: Schema = None) -> type:
    return SchemaDocument(top_level_schema).to_type(chosen_schema or top_level_schema)


if TYPE_CHECKING:
    Schema = Any
else:
    Schema = schema_to_type(TypedBytes('application/yaml', resources.read_binary('yaht', 'schema.yaml')) | Auto)
