import functools
import threading

# instance __dict__ key holding the _Store
_STORE = "_instance_cache_"
_MISSING, _KWARGS = object(), object()
_REPLACE_LOCK = threading.Lock()


class _Store(dict):
    """An instance's {method: {args: result}} dict, tagged with its owner's id.
    copy.copy shares this object between original and copy, so the tag lets the copy
    ignore it. Deep copies and pickles get an empty store instead of the results."""

    __slots__ = ("owner",)

    def __init__(self, owner=None):
        self.owner = owner

    def __deepcopy__(self, memo):
        return _Store()

    def __reduce__(self):
        return _Store, ()


def _store(self):
    """self's own _Store, replacing a missing, copied or unpickled one (first call only)."""

    state = vars(self)

    store = state.get(_STORE)

    if store is None or store.owner != id(self):
        with _REPLACE_LOCK:  # check-then-replace must not race; runs once per instance
            store = state.get(_STORE)

            if store is None or store.owner != id(self):
                store = state[_STORE] = _Store(id(self))

    return store


def cache(func):
    """Leak-free functools.cache replacement for methods and @property. Results live on
    the instance and are freed with it; copies start with an empty cache."""

    if isinstance(func, property):
        return property(cache(func.fget), func.fset, func.fdel, func.__doc__)

    @functools.wraps(func)
    def wrapper(self, /, *args, **kwargs):
        key = args + (_KWARGS, *sorted(kwargs.items())) if kwargs else args

        store = vars(self).get(_STORE)

        if store is None or store.owner != id(self):
            store = _store(self)

        results = store.get(wrapper) or store.setdefault(wrapper, {})

        value = results.get(key, _MISSING)

        if value is _MISSING:
            # setdefault keeps the first result stored, so racing threads
            # all return the same object:
            value = results.setdefault(key, func(self, *args, **kwargs))

        return value

    return wrapper


def cache_clear(obj):
    """Drop all cached results on obj."""

    vars(obj).pop(_STORE, None)
