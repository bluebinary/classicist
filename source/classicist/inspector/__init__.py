from classicist.logging import logger

import sys

logger = logger.getChild(__name__)


def unwrap(function: callable) -> callable:
    """Support unwrapping methods decorated with @property and other descriptor protocol
    decorators such as @classmethod and @staticmethod as well as function decorators
    that follow best-practice and have a __wrapped__ attribute referencing the original
    function, so that the original function can be found by unwrapping via the chain of
    the __wrapped__ and fget attributes.

    This implementation is based on the standard library's inspect.unwrap() method."""

    original: callable = function

    functionids: dict[id, callable] = {id(function): function}

    recursion_limit: int = sys.getrecursionlimit()

    while (w := hasattr(function, "__wrapped__")) or (d := hasattr(function, "fget")):
        if w is True:
            function = getattr(function, "__wrapped__")
        elif d is True:
            function = getattr(function, "fget")

        functionid: int = id(function)

        if (functionid in functionids) or (len(functionids) >= recursion_limit):
            raise ValueError(
                "Found wrapper loop while unwrapping {!r}!".format(original)
            )

        functionids[functionid] = function

    return function
