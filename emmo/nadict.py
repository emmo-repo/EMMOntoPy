# -*- coding: utf-8 -*-
"""
A nested dict with both attribute and item access.

NA stands for Nested and Attribute.
"""
import collections
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
        object.__setattr__(self, '_dict', {})
        self.update(*args, **kw)

    def __getitem__(self, key):
        if '.' in key:
            k1, k2 = key.split('.', 1)
            return self._dict[k1][k2]
        else:
            return self._dict[key]

    def __setitem__(self, key, value):
        if key in ('clear', 'copy', 'fromkeys', 'get', 'items', 'keys',
                   'pop', 'popitem', 'setdefault', 'update', 'values'):
            raise ValueError('invalid key "%s": must not override supported '
                             'dict method names' % key)
        elif '.' in key:
            k1, k2 = key.split('.', 1)
            if k1 not in self._dict:
                self._dict[k1] = NADict()
            self._dict[k1][k2] = value
        elif key in self._dict:
            if isinstance(self._dict[key], NADict):
                self._dict[key].update(value)
            else:
                self._dict[key] = value
        else:
            if isinstance(value, collections.abc.Mapping):
                self._dict[key] = NADict(value)
            else:
                self._dict[key] = value

    def __delitem__(self, key):
        if '.' in key:
            k1, k2 = key.split('.', 1)
            del self._dict[k1][k2]
        else:
            del self._dict[key]

    def __getattr__(self, key):
        if key not in self._dict:
            raise AttributeError('No such key: %s' % (key, ))
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
        if '.' in key:
            k1, k2 = key.split('.', 1)
            return k2 in self._dict[k1]
        else:
            return key in self._dict

    def __iter__(self, prefix=''):
        for k, v in self._dict.items():
            key = '%s.%s' % (prefix, k) if prefix else k
            if isinstance(v, NADict):
                yield from v.__iter__(key)
            else:
                yield key

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%s' % (k, repr(v)) for k, v in self._dict.items()))

    def clear(self):
        """Clear all keys."""
        self._dict.clear()

    def copy(self):
        """Returns a deep copy of self."""
        return copy.deepcopy(self)

    @staticmethod
    def fromkeys(self, iterable, value=None):
        """Returns a new NADict with keys from `iterable` and values
        set to `value`."""
        n = NADict()
        for key in iterable:
            n[key] = value
        return n

    def get(self, key, default=None):
        """Returns the value for `key` if `key` is in self, else return
        `default`."""
        if '.' in key:
            k1, k2 = key.split('.', 1)
            return self._dict[k1].get(k2, default)
        else:
            return self._dict.get(key, default)

    def items(self, prefix=''):
        """Returns an iterator over all items as (key, value) pairs."""
        for k, v in self._dict.items():
            key = '%s.%s' % (prefix, k) if prefix else k
            if isinstance(v, NADict):
                yield from v.items(key)
            else:
                yield (key, v)

    def keys(self, prefix=''):
        """Returns an iterator over all keys."""
        for k, v in self._dict.items():
            key = '%s.%s' % (prefix, k) if prefix else k
            if isinstance(v, NADict):
                yield from v.keys(key)
            else:
                yield key

    def pop(self, key, default=None):
        """Removed `key` and returns corresponding value.  If `key` is not
        found, `default` is returned if given, otherwise KeyError is
        raised."""
        if '.' in key:
            k1, k2 = key.split('.', 1)
            return self._dict[k1].pop(k2, default)
        else:
            return self._dict.pop(key, default)

    def popitem(self, prefix=''):
        """Removes and returns some (key, value). Raises KeyError if empty."""
        item = self._dict.popitem()
        if isinstance(item, NADict):
            k, v = item
            item2 = item.popitem(k)
            self._dict[k] = v
            return item2
        else:
            k, v = self._dict.popitem()
            key = '%s.%s' % (prefix, k) if prefix else k
            return (key, v)

    def setdefault(self, key, value=None):
        """Inserts `key` and `value` pair if key is not found.

        Returns the new value for `key`."""
        if '.' in key:
            k1, k2 = key.split('.', 1)
            return self._dict[k1].setdefault(k2, value)
        else:
            return self._dict.setdefault(key, value)

    def update(self, *args, **kw):
        """Updates self with dict/iterable from `args` and keyword arguments
        from `kw`."""
        for arg in args:
            if hasattr(arg, 'keys'):
                for k in arg:
                    self[k] = arg[k]
            else:
                for k, v in arg:
                    self[k] = v
        for k, v in kw.items():
            self[k] = v

    def values(self):
        """Returns a set-like providing a view of all style values."""
        return self._dict.values()
