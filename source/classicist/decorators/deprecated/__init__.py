from classicist.logging import logger
from classicist.decorators.annotation import annotate

from functools import wraps, partial
from datetime import datetime

logger = logger.getChild(__name__)


def deprecated(
    thing: object = None,
    /,
    reason: str = None,
    since: str = None,
    removal: str = None,
    replacement: str = None,
    advice: str = None,
    ticket: str = None,
    **annotations: dict[str, object],
) -> object:
    """The @deprecated decorator provides support for marking code objects as having
    been deprecated. The decorator also provides support for adding additional arbitrary
    annotations to the object beyond the directly supported annotations."""

    if reason is None:
        pass
    elif isinstance(reason, str):
        annotations["reason"] = reason
    else:
        raise TypeError(
            "The 'reason' argument, if specified, must have a string value!"
        )

    if replacement is None:
        pass
    elif isinstance(replacement, str):
        annotations["replacement"] = replacement
    else:
        raise TypeError(
            "The 'replacement' argument, if specified, must have a string value!"
        )

    if since is None:
        pass
    elif isinstance(since, (str, datetime)):
        annotations["since"] = since
    else:
        raise TypeError(
            "The 'since' argument, if specified, must have a string or datetime value!"
        )

    if removal is None:
        pass
    elif isinstance(removal, (str, datetime)):
        annotations["removal"] = removal
    else:
        raise TypeError(
            "The 'removal' argument, if specified, must have a string or datetime value!"
        )

    if advice is None:
        pass
    elif isinstance(advice, str):
        annotations["advice"] = advice
    else:
        raise TypeError(
            "The 'advice' argument, if specified, must have a string value!"
        )

    if ticket is None:
        pass
    elif isinstance(ticket, str):
        annotations["ticket"] = ticket
    else:
        raise TypeError(
            "The 'ticket' argument, if specified, must have a string value!"
        )

    if thing is None:
        return partial(deprecated, **annotations)

    @wraps(thing)
    def decorator() -> object:
        if not hasattr(thing, "_classicist_deprecated"):
            setattr(thing, "_classicist_deprecated", True)
        return annotate(thing, **annotations)

    return decorator()


def is_deprecated(thing: object) -> bool:
    """The is_deprecated() helper method can be used to determine if an object or class
    has been marked as deprecated."""

    return getattr(thing, "_classicist_deprecated", False) is True


__all__ = [
    "deprecated",
    "is_deprecated",
]
