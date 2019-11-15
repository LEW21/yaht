from yaht.core import TypedBytes


class PipeableType(type):
    def __ror__(self, other):
        return self(other)


class Auto(metaclass = PipeableType):
    _data: dict

    # TODO make _tb positional-only in 3.8
    def __init__(self, _tb: TypedBytes = None, **data):
        if _tb:
            # Ensure this, because many other types would just work without errors, and we don't want that.
            assert isinstance(_tb, TypedBytes)

        from yaht.serialization import unserialize
        self._data = unserialize(type(self), _tb)._data if _tb else {}
        self._data.update(data)

    def __getattr__(self, attr):
        try:
            return self._data[attr]
        except KeyError as e:
            raise AttributeError(attr) from e

    def __str__(self):
        return 'Auto ' + str(self._data)

    def __repr__(self):
        return 'Auto ' + repr(self._data)
