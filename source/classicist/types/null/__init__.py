from __future__ import annotations


class NullType(object):
    """The NullType class supports the creation of a Null singleton instance that offers
    support for safely chaining nested attribute accesses without raising exceptions for
    attributes that have no inherent value.

    As Python currently lacks a null-aware navigation operator, such as `?.`, like many
    other dynamic languages, for safely navigating nested object hierarchies which may
    contain null attributes, the library offers the `NullType` and `Null` singleton as a
    potential option to support this need in the interim. Consistent use of the `Null`
    singleton in place of the standard `None` singleton, in relevant scenarios, such as
    within a data model library for example, can allow for more expressive and clearer
    code that does not require endless checks for intermediary attribute existence.

    However, there are some caveats to the use of the `NullType` and `Null` singleton as
    these are not built-in features of the language, and Python does not offer support
    for the creation of custom operators nor overriding the `is` operator for identity
    checking which limits some of the cases in which the `Null` singleton could be used.

    With knowledge of the caveats and in the right scenarios, the `Null` singleton can
    offer a good way to achieve clearer and more expressive code while navigating nested
    object hierarchies without the clutter of nested attribute existence checks."""

    _instance: NullType = None

    def __new__(cls) -> NullType:
        """Ensure NullType can only create a singleton instance; further calls to create
        instances of the NullType will return the existing singleton instance."""

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __getattr__(self, name: str) -> NullType:
        """Support nested attribute access by returning the singleton instance."""

        return self.__class__._instance

    def __bool__(self) -> bool:
        """Support falsey equality checks for boolean comparisons against NullType."""

        return False  # Always returns False

    def __eq__(self, value: object) -> bool:
        """Support value equality checks against NullType via the `==` operator as the
        fallback option to being able to support identity equality checks via the `is`
        operator which are not currently possible due to language constraints."""

        if value is None or value is False:
            return True
        else:
            return self is value

    def __str__(self) -> str:
        return "Null"

    def __repr__(self) -> str:
        return "Null"


# Create the singleton instance of Null
Null = NullType()

__all__ = [
    "NullType",
    "Null",
]
