from classicist import shadowproof
from classicist.exceptions.metaclasses.shadowproof import AttributeShadowingError

import pytest


def test_subclassing_without_shadowproof():
    """Test subclassing without the use of the shadowproof metaclass."""

    # Create class using the standard object superclass and standard metaclass
    class Thing(object):
        greeting: str = "hello"

    class SomeThing(Thing):
        # For classes with the default metaclass, the attribute is reassigned silently
        # depending on what it is used for in the program, this could affect behaviour
        greeting: str = "goodbye"

    assert issubclass(SomeThing, Thing)

    assert Thing.greeting == "hello"

    assert SomeThing.greeting == "goodbye"


def test_subclassing_with_shadowproof():
    """Test subclassing with the use of the shadowproof metaclass."""

    with pytest.raises(AttributeShadowingError) as exception:
        # Create class using the standard object superclass with shadowproof metaclass
        class Thing(object, metaclass=shadowproof):
            greeting: str = "hello"

        class SomeThing(Thing):
            # For classes using the shadowproof metaclass, class attribute reassignment
            # will result in an AttributeShadowingError exception being raised...
            greeting: str = "goodbye"

        assert Thing.greeting == "hello"
        assert SomeThing.greeting == "hello"
        assert str(exception) == ""
