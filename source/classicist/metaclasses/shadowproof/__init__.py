from classicist.logging import logger
from classicist.exceptions.metaclasses.shadowproof import AttributeShadowingError

logger = logger.getChild(__name__)


class shadowproof(type):
    """The shadowproof type provides support for detecting overwritten attributes – that
    is attributes from a superclass that get shadowed by a subclass' attributes, helping
    to protect against bugs which can sometimes be difficult to detect when a subclass
    unintentionally shadows a superclass' attribute with its own."""

    def __new__(
        cls,
        name: str,
        bases: tuple[object],
        attributes: dict[str, object],
        raises: bool = True,
    ):
        # Iterate through attributes defined in the current class
        for attribute, value in attributes.items():
            # Skip special Python attributes and methods
            if attribute.startswith("__") and attribute.endswith("__"):
                continue

            # Check for attribute shadowing in any of the base classes
            for base in bases:
                if hasattr(base, attribute):
                    message = f"The '{attribute}' attribute in the '{name}' class shadows the attribute of the same name in the '{base.__name__}' base class!"

                    if raises is True:
                        raise AttributeShadowingError(message)
                    else:
                        logger.warning(message)

        return super().__new__(cls, name, bases, attributes)
