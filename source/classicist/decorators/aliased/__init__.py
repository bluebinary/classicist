from classicist.logging import logger
from classicist.exceptions.decorators.aliased import AliasError
from classicist.inspector import unwrap

from typing import Callable
from functools import wraps

import keyword

logger = logger.getChild(__name__)


def alias(*names: tuple[str]) -> Callable:
    """Decorator that marks a method with one or more alias names. The decorator does
    not modify the function – it simply records the aliases on the function object."""

    for name in names:
        if not isinstance(name, str):
            raise AliasError(
                "All @alias decorator name arguments must have a string value; non-string values cannot be used!"
            )
        elif len(name) == 0:
            raise AliasError(
                "All @alias decorator name arguments must be valid Python identifier values; empty strings cannot be used!"
            )
        elif not name.isidentifier():
            raise AliasError(
                f"All @alias decorator name arguments must be valid Python identifier values; strings such as '{name}' are not considered valid identifiers by Python!"
            )
        elif keyword.iskeyword(name):
            raise AliasError(
                f"All @alias decorator name arguments must be valid Python identifier values; reserved keywords, such as '{name}' cannot be used!"
            )

    def decorator(function: Callable) -> Callable:
        function = unwrap(function)

        if isinstance(aliases := getattr(function, "_classicist_aliases", None), tuple):
            setattr(function, "_classicist_aliases", tuple([*aliases, *names]))
        else:
            setattr(function, "_classicist_aliases", names)

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return decorator


def is_aliased(function: callable) -> bool:
    """The is_aliased() helper method can be used to determine if a class method has
    been aliased."""

    function = unwrap(function)

    return isinstance(getattr(function, "_classicist_aliases", None), tuple)


def aliases(function: callable) -> list[str]:
    """The aliases() helper method can be used to obtain any class method aliases."""

    function = unwrap(function)

    if isinstance(aliases := getattr(function, "_classicist_aliases", None), tuple):
        return list(aliases)


__all__ = [
    "alias",
    "is_aliased",
    "aliases",
]
