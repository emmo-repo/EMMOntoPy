# -*- coding: utf-8 -*-
"""
A nested dict with both attribute and item access.

NA stands for Nested and Attribute.
"""
from collections.abc import Mapping
import copy


class NADict:
    """A nested dict with both attribute and item access.

    It is intended to be used with keys that are valid Python
    identifiers.  However, except for string keys containing a dot,
    there are actually no hard limitations.  If a key equals an existing
    attribute name, attribute access is of cause not possible.

    Nested items can be accessed via a dot notation, as shown in the
    example below.

    Examples
    --------
    >>> n = NADict(a=1, b=NADict(c=3, d=4))
    >>> n['a']
    1
    >>> n.a
    1
    >>> n['b.c']
    3
    >>> n.b.c
    3
    >>> n['b.e'] = 5
    >>> n.b.e
    5

    Attributes
    ----------
    _dict : dict
        Dictionary holding the actial items.
    """

    def __init__(self, *args, **kw):
        object.__setattr__(self, "_dict", {})
        self.update(*args, **kw)

    def __getitem__(self, key):
        if "." in key:
            key1, key2 = key.split(".", 1)
            return self._dict[key1][key2]
        return self._dict[key]

    def __setitem__(self, key, value):
        if key in (
            "clear",
            "copy",
            "fromkeys",
            "get",
            "items",
            "keys",
            "pop",
            "popitem",
            "setdefault",
            "update",
            "values",
        ):
            raise ValueError(
                f"invalid key {key!r}: must not override supported dict method"
                " names"
            )

        if "." in key:
            key1, key2 = key.split(".", 1)
            if key1 not in self._dict:
                self._dict[key1] = NADict()
            self._dict[key1][key2] = value
        elif key in self._dict:
            if isinstance(self._dict[key], NADict):
                self._dict[key].update(value)
            else:
                self._dict[key] = value
        else:
            if isinstance(value, Mapping):
                self._dict[key] = NADict(value)
            else:
                self._dict[key] = value

    def __delitem__(self, key):
        if "." in key:
            key1, key2 = key.split(".", 1)
            del self._dict[key1][key2]
        else:
            del self._dict[key]

    def __getattr__(self, key):
        if key not in self._dict:
            raise AttributeError(f"No such key: {key}")
        return self._dict[key]

    def __setattr__(self, key, value):
        if key in self._dict:
            self._dict[key] = value
        else:
            object.__setattr__(self, key, value)

    def __delattr__(self, key):
        if key in self._dict:
            del self._dict[key]
        else:
            object.__delattr__(self, key)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        if "." in key:
            key1, key2 = key.split(".", 1)
            return key2 in self._dict[key1]
        return key in self._dict

    def __iter__(self, prefix=""):
        for key, value in self._dict.items():
            key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, NADict):
                yield from value.__iter__(key)
            else:
                yield key

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{', '.join(f'{key}={value!r}' for key, value in self._dict.items())})"  # pylint: disable=line-too-long
        )

    def clear(self):
        """Clear all keys."""
        self._dict.clear()

    def copy(self):
        """Returns a deep copy of self."""
        return copy.deepcopy(self)

    @staticmethod
    def fromkeys(iterable, value=None):
        """Returns a new NADict with keys from `iterable` and values
        set to `value`."""
        res = NADict()
        for key in iterable:
            res[key] = value
        return res

    def get(self, key, default=None):
        """Returns the value for `key` if `key` is in self, else return
        `default`."""
        if "." in key:
            key1, key2 = key.split(".", 1)
            return self._dict[key1].get(key2, default)
        return self._dict.get(key, default)

    def items(self, prefix=""):
        """Returns an iterator over all items as (key, value) pairs."""
        for key, value in self._dict.items():
            key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, NADict):
                yield from value.items(key)
            else:
                yield (key, value)

    def keys(self, prefix=""):
        """Returns an iterator over all keys."""
        for key, value in self._dict.items():
            key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, NADict):
                yield from value.keys(key)
            else:
                yield key

    def pop(self, key, default=None):
        """Removed `key` and returns corresponding value.  If `key` is not
        found, `default` is returned if given, otherwise KeyError is
        raised."""
        if "." in key:
            key1, key2 = key.split(".", 1)
            return self._dict[key1].pop(key2, default)
        return self._dict.pop(key, default)

    def popitem(self, prefix=""):
        """Removes and returns some (key, value). Raises KeyError if empty."""
        item = self._dict.popitem()
        if isinstance(item, NADict):
            key, value = item
            item2 = item.popitem(key)
            self._dict[key] = value
            return item2
        key, value = self._dict.popitem()
        key = f"{prefix}.{key}" if prefix else key
        return (key, value)

    def setdefault(self, key, value=None):
        """Inserts `key` and `value` pair if key is not found.

        Returns the new value for `key`."""
        if "." in key:
            key1, key2 = key.split(".", 1)
            return self._dict[key1].setdefault(key2, value)
        return self._dict.setdefault(key, value)

    def update(self, *args, **kwargs):
        """Updates self with dict/iterable from `args` and keyword arguments
        from `kw`."""
        for arg in args:
            if hasattr(arg, "keys"):
                for _ in arg:
                    self[_] = arg[_]
            else:
                for key, value in arg:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def values(self):
        """Returns a set-like providing a view of all style values."""
        return self._dict.values()
