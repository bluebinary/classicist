from __future__ import annotations

from datetime import datetime, timedelta
from functools import wraps
from inspect import unwrap

from classicist.logging import logger

logger = logger.getChild(__name__)


class Runtimer(object):
    """The Runtimer class times and tracks the runtime of function calls."""

    _funcobj: callable = None
    _started: datetime = None
    _stopped: datetime = None

    def __init__(self, function: callable):
        """Supports instantiating an instance of the Runtimer class."""

        if not callable(function):
            raise TypeError("The 'function' argument must reference a callable!")

        self._funcobj = function

    def __str__(self) -> str:
        """Returns a string representation of the current Runtimer instance."""

        return f"<{self.__class__.__name__}(started: {self.started}, stopped: {self.stopped}, duration: {self.duration})>"

    def __repr__(self) -> str:
        """Returns a debug string representation of the current Runtimer instance."""

        return f"<{self.__class__.__name__}(started: {self.started}, stopped: {self.stopped}, duration: {self.duration}) @ {hex(id(self))}>"

    def reset(self) -> Runtimer:
        """Supports resetting the Runtimer timing information."""

        self._started = None
        self._stopped = None

        return self

    def start(self) -> Runtimer:
        """Supports starting the Runtimer timer by recording the current datetime."""

        self._started = datetime.now()
        self._stopped = None

        return self

    def stop(self) -> Runtimer:
        """Supports stopping the Runtimer timer by recording the current datetime."""

        if self._started is None:
            self._started = datetime.now()
        self._stopped = datetime.now()

        return self

    @property
    def function(self) -> callable:
        """Supports returning the Runtimer instance's associated function/method."""

        return self._funcobj

    @property
    def started(self) -> datetime:
        """Supports returning the started datetime or the current time as a fallback."""

        return self._started or datetime.now()

    @property
    def stopped(self) -> datetime:
        """Supports returning the stopped datetime or the current time as a fallback."""

        return self._stopped or datetime.now()

    @property
    def timedelta(self) -> timedelta:
        """Supports returning the timedelta for the decorated function's call time."""

        if isinstance(self._started, datetime) and isinstance(self._stopped, datetime):
            return self._stopped - self._started
        else:
            return timedelta(0)

    @property
    def duration(self) -> float:
        """Supports returning the duration of the decorated function's call time."""

        return self.timedelta.total_seconds()


def runtimer(function: callable) -> callable:
    """The runtimer decorator method creates an instance of the Runtimer class for the
    specified function, allowing calls to the function to be timed."""

    if not callable(function):
        raise TypeError("The 'function' argument must reference a callable!")

    logger.debug("runtimer(function: %s)", function)

    # If the function already has an associated Runtimer instance, reset it
    if isinstance(
        _runtimer := getattr(function, "_classicist_runtimer", None), Runtimer
    ):
        _runtimer.reset()
    else:
        # Otherwise, create a new instance and associate it with the function
        _runtimer = function._classicist_runtimer = Runtimer(function)

    @wraps(function)
    def wrapper(*args, **kwargs):
        logger.debug(
            "runtimer(function: %s).wrapper(args: %s, kwargs: %s)",
            function,
            args,
            kwargs,
        )

        _runtimer.start()
        result = function(*args, **kwargs)
        _runtimer.stop()

        return result

    return wrapper


def runtime(function: callable) -> Runtimer | None:
    """The runtime helper method can be used to obtain the Runtimer instance for the
    specified function, if one is present, allowing access to the most recent function
    call start and stop time stamps and call duration."""

    if not callable(function):
        raise TypeError("The 'function' argument must reference a callable!")

    function = unwrap(function)

    logger.debug("runtime(function: %s)" % (function))

    if isinstance(
        _runtimer := getattr(function, "_classicist_runtimer", None), Runtimer
    ):
        return _runtimer


def has_runtimer(function: callable) -> bool:
    """The has_runtimer helper method can be used to determine if the specified function
    has an associated Runtimer instance or not, returning a boolean to indicate this."""

    if isinstance(getattr(function, "_classicist_runtimer", None), Runtimer):
        return True
    else:
        return False


__all__ = [
    "Runtimer",
    "runtimer",
    "runtime",
    "hasruntimer",
]
