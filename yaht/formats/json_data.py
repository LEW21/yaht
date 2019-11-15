from typing import Any, Union, Sequence
from typing_extensions import Literal
from datetime import datetime, timezone
from warnings import warn

from yaht.auto import Auto


def to_auto(data, always_dicts = set(), key = None):
    if isinstance(data, dict):
        processed_data = {k: to_auto(v, always_dicts, k) for k, v in data.items()}
        return Auto(**processed_data) if key not in always_dicts else processed_data
    elif isinstance(data, list):
        return [to_auto(v, always_dicts) for v in data]
    else:
        return data


def unserialize(Object, data):
    if Object is Auto:
        return to_auto(data)

    from yaht.schema import Schema
    if Object is Schema:
        # TODO delete after this becomes strong enough to interpret JSON Schema schema correctly
        return to_auto(data, {'definitions', 'properties'})

    if Object is type(None):
        if data is not None:
            raise ValueError(Object)
        return data

    if getattr(Object, '__origin__', None) == Literal:
        const = Object.__args__[0]
        if data != const:
            raise ValueError(Object)
        return data

    if Object == bool:
        if not isinstance(data, bool):
            raise ValueError(Object)
        return data

    if Object == int:
        if not isinstance(data, int):
            raise ValueError(Object)
        return data

    if Object == float:
        if not isinstance(data, float):
            raise ValueError(Object)
        return data

    if Object == str:
        if not isinstance(data, str):
            raise ValueError(Object)
        return data

    if Object == datetime:
        if not isinstance(data, str):
            raise ValueError(Object)
        if not data.endswith('Z'):
            raise NotImplementedError('Parsing dates with non-Z timezones is not supported.')
        return datetime.fromisoformat(data[:-1]).replace(tzinfo = timezone.utc)

    if getattr(Object, '__resttest_plain__', False):
        if not isinstance(data, dict):
            raise ValueError(Object)

        unknown_data = set(data.keys()) - set(Object.__annotations__.keys())
        if unknown_data != set():
            warn(f'{Object.__name__} has unknown properties: {", ".join(unknown_data)}', UserWarning, 2)

        missing_data = set(Object.__annotations__.keys()) - set(data.keys()) - set(Object.__dict__.keys())
        if missing_data != set():
            raise TypeError(f'{Object.__name__} is missing required properties: {", ".join(missing_data)}')

        kwargs = dict()
        for prop_name, prop_type in Object.__annotations__.items():
            if prop_name in data:
                kwargs[prop_name] = unserialize(prop_type, data[prop_name])

        return Object(**kwargs)

    if getattr(Object, '__origin__', None) == Union:
        results = []

        for arg in Object.__args__:
            try:
                results.append(unserialize(arg, data))
            except ValueError as e:
                pass

        if len(results) > 1:
            raise NotImplementedError('Matching multiple options from anyOf is not implemented.')

        if len(results) == 1:
            return results[0]

        raise ValueError(Object)

    if Object == dict:
        if not isinstance(data, dict):
            raise ValueError(Object)
        return data

    if issubclass(getattr(Object, '__origin__', type(None)), Sequence):
        if not isinstance(data, list):
            raise ValueError(Object)
        item_type = Object.__args__[0]
        return [unserialize(item_type, item) for item in data]

    if Object == list:
        if not isinstance(data, list):
            raise ValueError(Object)
        return data

    if Object == Any:
        return data

    raise ValueError(Object)


def serialize(obj):
    if obj is None or isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str):
        return obj

    if isinstance(obj, datetime):
        return obj.isoformat().replace('+00:00', 'Z')

    if getattr(type(obj), '__resttest_plain__', False):
        return serialize(obj.__dict__)

    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [serialize(v) for v in obj]

    raise ValueError()
