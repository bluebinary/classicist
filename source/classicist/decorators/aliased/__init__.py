from classicist.logging import logger
from classicist.exceptions.decorators.aliased import AliasError
from classicist.inspector import unwrap

from typing import Callable
from functools import wraps

import keyword
import inspect
import sys

logger = logger.getChild(__name__)


def alias(*names: tuple[str], scope: object = None) -> Callable:
    """Decorator that applies one or more alias names to a class, function or method.
    The decorator records the assigned aliases on the class, method or function object,
    and where possible creates aliases in the same scope as the original class or module
    level function directly as the decorator call runs. Methods within classes cannot be
    aliased directly by the `@alias` decorator, but instead require the assistance of the
    corresponding `aliased` metaclass that must be specified on the class definition. If
    control over the scope is required, the optional `scope` keyword argument can be used
    to specify the scope into which to apply the alias, this should be a reference to the
    globals() or locals() at the site in code where the `@alias()` decorator is used."""

    for name in names:
        if not isinstance(name, str):
            raise AliasError(
                "All @alias decorator name arguments must have a string value; non-string values cannot be used!"
            )
        elif len(name := name.strip()) == 0:
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

    def decorator(thing: object, *args, **kwargs) -> object:
        nonlocal scope

        thing = unwrap(thing)

        logger.debug(f"@alias({names}) called on {thing}")

        if isinstance(aliases := getattr(thing, "_classicist_aliases", None), tuple):
            setattr(thing, "_classicist_aliases", tuple([*aliases, *names]))
        else:
            setattr(thing, "_classicist_aliases", names)

        @wraps(thing)
        def wrapper_class(*args, **kwargs):
            return thing

        @wraps(thing)
        def wrapper_method(*args, **kwargs):
            return thing(*args, **kwargs)

        @wraps(thing)
        def wrapper_function(*args, **kwargs):
            return thing

        if inspect.isclass(thing):
            if not scope:
                scope = sys.modules.get(thing.__module__ or "__main__")

            if isinstance(scope, object):
                for name in names:
                    if hasattr(scope, name):
                        raise AliasError(
                            "Cannot create alias '%s' for %s class in the %s module as an object with that name already exists!"
                            % (
                                name,
                                thing,
                                scope,
                            )
                        )

                    # Create a module-level alias for the class
                    if isinstance(scope, dict):
                        scope[name] = thing
                    else:
                        setattr(scope, name, thing)

            return wrapper_class(*args, **kwargs)
        elif inspect.ismethod(thing) or isinstance(thing, classmethod):
            return wrapper_method
        elif inspect.isfunction(thing):
            if not scope:
                scope = sys.modules.get(thing.__module__ or "__main__")

                # The qualified name for module-level functions only contain the name of the
                # function, whereas functions nested within other functions or classes have
                # names comprised of multiple parts separated by the "." character; because
                # it is only currently possible to alias module-level functions, any nested
                # or class methods are ignored during this stage of the aliasing process.
                if len(thing.__qualname__.split(".")) > 1:
                    logger.debug(
                        "Unable to apply alias to functions defined beyond the top-level of a module: %s!"
                        % (thing.__qualname__)
                    )

                    return wrapper_function(*args, **kwargs)

            # if signature := inspect.signature(thing):
            #     if len(parameters := signature.parameters) > 0 and "self" in parameters:
            #         return wrapper_function(*args, **kwargs)

            if isinstance(scope, object):
                # At this point we should only be left with module-level functions to alias
                for name in names:
                    # Ensure the scope doesn't already contain an object of the same name
                    if hasattr(scope, name):
                        raise AliasError(
                            "Cannot create alias '%s' for %s function in the %s module as an object with that name already exists!"
                            % (
                                name,
                                thing,
                                scope,
                            )
                        )

                    logger.debug(f"Added alias '{name}' to {scope}.{thing}")

                    if isinstance(scope, dict):
                        scope[name] = thing
                    elif isinstance(scope, object):
                        setattr(scope, name, thing)
            else:
                logger.warning(
                    f"No scope was found or specified for {thing} into which to assign aliases!"
                )

            return wrapper_function(*args, **kwargs)
        else:
            raise AliasError(
                "The @alias decorator can only be applied to classes, methods and functions, not %s!"
                % (type(thing))
            )

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
