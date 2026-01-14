from classicist.logging import logger

logger = logger.getChild(__name__)


def nocache(function: callable):
    """A no-cache decorator to specifically call out functions and properties that must
    not be cached using the functools.cache decorator or similar."""

    return function
