from classicist.logging import logger
from classicist.exceptions.decorators.aliased import AliasError

logger = logger.getChild(__name__)


class aliased(type):
    """Metaclass that looks for methods that have been decorated with @alias(...) and
    automatically creates the corresponding aliases for those methods on the class."""

    def __new__(cls: object, name: str, bases: tuple[object], namespace: dict):
        # Create the class first
        cls = super().__new__(cls, name, bases, namespace)

        # Walk through the class body (namespace) and install the aliases
        for name, value in namespace.items():
            original: object = value

            # If a function has been wrapped by a well behaved decorator, unwrap it, to
            # get to the original function, and thus to the alias annotation we need to
            # create the function aliases in the class; without access to the annotation
            # the aliases cannot be created, so any decorators used should follow best
            # practice and apply the __wrapped__ attribute to point back to the wrapped
            # function using functools.wraps or similar or use property getter practice:
            while (w := hasattr(value, "__wrapped__")) or (p := hasattr(value, "fget")):
                if w is True:  # Get the original wrapped function
                    value = getattr(value, "__wrapped__")
                elif p is True:  # Get the original property function
                    value = getattr(value, "fget")

            if aliases := getattr(value, "_classicist_aliases", None):
                for alias in aliases:
                    if hasattr(cls, alias):
                        raise AliasError(
                            f"Cannot create alias '{alias}' for method '{name}' as '{cls.__name__}.{alias}' already exists!"
                        )

                    # The alias points to the original function or property accessor
                    setattr(cls, alias, original)

        return cls
