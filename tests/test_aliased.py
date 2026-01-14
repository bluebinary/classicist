from classicist import aliased, alias, aliases, is_aliased
from classicist.exceptions.decorators.aliased import AliasError

import pytest


def test_alias_class_method():
    """Test using the @alias decorator on a method."""

    class Welcome(metaclass=aliased):
        @alias("sweet", "greet")
        def hello(self, name: str) -> str:
            return f"hello: {name}"

    assert Welcome.hello is Welcome.sweet
    assert Welcome.hello is Welcome.greet

    assert is_aliased(Welcome.hello) is True
    assert is_aliased(Welcome.sweet) is True
    assert is_aliased(Welcome.greet) is True

    assert aliases(Welcome.hello) == ["sweet", "greet"]
    assert aliases(Welcome.hello) == ["sweet", "greet"]


def test_alias_class_method_property():
    """Test using the @alias decorator with a @property decorator."""

    class Welcome(metaclass=aliased):
        @property
        @alias("sweet", "greet")
        @classmethod
        def hello(self, name: str) -> str:
            return f"hello: {name}"

    assert Welcome.hello is Welcome.sweet
    assert Welcome.hello is Welcome.greet

    assert is_aliased(Welcome.hello) is True
    assert is_aliased(Welcome.sweet) is True
    assert is_aliased(Welcome.greet) is True

    assert aliases(Welcome.hello) == ["sweet", "greet"]
    assert aliases(Welcome.hello) == ["sweet", "greet"]


def test_alias_class_method_alias_with_valid_identifier():
    """Test using the @alias decorator with a valid identifier."""

    class Welcome(metaclass=aliased):
        @alias("greet")
        def hello(self, name: str) -> str:
            return f"hello: {name}"

    # Ensure that the alias has been registered on the class as a new attribute
    assert hasattr(Welcome, "hello") is True
    assert hasattr(Welcome, "greet") is True

    # Ensure that the alias points to the original method
    assert Welcome.greet is Welcome.hello

    # Create an instance of the test class
    welcome = Welcome()
    assert isinstance(welcome, Welcome)

    # Ensure that the alias that has been registered is also available on the instance
    assert hasattr(welcome, "greet") is True

    # Ensure that the aliased method functionality operates as expected
    assert welcome.hello("me") == "hello: me"
    assert welcome.greet("me") == "hello: me"

    class SubWelcome(Welcome):
        pass

    assert hasattr(SubWelcome, "hello") is True
    assert hasattr(SubWelcome, "greet") is True

    subwelcome = SubWelcome()

    assert hasattr(subwelcome, "hello") is True
    assert hasattr(subwelcome, "greet") is True

    # Ensure that the aliased method functionality operates as expected
    assert subwelcome.hello("me") == "hello: me"

    # Ensure when the alias hasn't been registered that access raises an AttributeError
    assert subwelcome.greet("me") == "hello: me"


def test_alias_class_method_with_invalid_identifier():
    """Test using the @alias decorator with an invalid identifier."""

    with pytest.raises(AliasError) as exception:

        class Welcome(metaclass=aliased):
            @alias("greet!")  # Invalid identifiers or reserved keywords cannot be used
            def hello(self, name: str) -> str:
                return f"hello: {name}"

        assert (
            str(exception)
            == "All @alias decorator name arguments must be valid Python identifier values; strings such as 'greet!' are not considered valid identifiers by Python!"
        )


def test_alias_class_method_without_metaclass():
    """Test using the @alias decorator without the aliased metaclass."""

    with pytest.raises(AttributeError) as exception:

        class Welcome(object):  # Without the metaclass, the aliases won't be registered
            @alias("greet")
            def hello(self, name: str) -> str:
                return f"hello: {name}"

        # When the @alias decorator is used without the metaclass the aliases won't work
        assert hasattr(Welcome, "hello") is True
        assert hasattr(Welcome, "greet") is False

        # Create an instance of the test class for use below
        welcome = Welcome()
        assert isinstance(welcome, Welcome)

        # Ensure that the aliased method functionality operates as expected
        assert welcome.hello("me") == "hello: me"

        # Ensure when the alias hasn't been registered that access raises an AttributeError
        assert welcome.greet("me") == "hello: me"

        assert str(exception) == "'Welcome' object has no attribute 'greet'"


def test_alias_class_method_alias_with_subclass():
    """Test using the @alias decorator on a superclass and inheritance by subclasses."""

    class Welcome(metaclass=aliased):
        @alias("greet")
        def hello(self, name: str) -> str:
            return f"hello: {name}"

        def __getattr__(self, name: str) -> object:
            if name.startswith("_"):
                return super().__getattr__(name)
            else:
                raise AttributeError(
                    f"The '{self.__class__.__name__}' class lacks the '{name}' attribute!"
                )

    # Ensure that the alias has been registered on the class as a new attribute
    assert hasattr(Welcome, "hello") is True
    assert hasattr(Welcome, "greet") is True

    assert ("hello" in Welcome.__dict__) is True
    assert ("greet" in Welcome.__dict__) is True

    # Ensure that the alias points to the original method
    assert Welcome.greet is Welcome.hello

    # Create an instance of the test class
    welcome = Welcome()
    assert isinstance(welcome, Welcome)

    # Ensure that the alias that has been registered is also available on the instance
    assert hasattr(welcome, "greet") is True

    # Ensure that the aliased method functionality operates as expected
    assert welcome.hello("me") == "hello: me"
    assert welcome.greet("me") == "hello: me"

    # Create a subclass from the aliased superclass
    class SubWelcome(Welcome):
        def sweet(self, name: str) -> str:
            return f"sweet, {name}!"

    # Ensure that the subclass inherits the aliases declared on the superclass
    assert hasattr(SubWelcome, "hello") is True
    assert hasattr(SubWelcome, "greet") is True
    assert hasattr(SubWelcome, "sweet") is True

    assert ("hello" in SubWelcome.__dict__) is False
    assert ("greet" in SubWelcome.__dict__) is False
    assert ("sweet" in SubWelcome.__dict__) is True

    # Create an instance of the subclass
    subwelcome = SubWelcome()

    # Ensure that the subclass inherits the aliases declared on the superclass
    assert hasattr(subwelcome, "hello") is True
    assert hasattr(subwelcome, "greet") is True
    assert hasattr(subwelcome, "sweet") is True

    # Ensure that the source method functionality operates as expected
    assert subwelcome.hello("me") == "hello: me"

    # Ensure that the aliased method functionality operates as expected
    assert subwelcome.greet("me") == "hello: me"

    # Ensure that the aliased method functionality operates as expected
    assert subwelcome.sweet("me") == "sweet, me!"

    # Create a sub-subclass from the aliased superclass
    class SubSubWelcome(SubWelcome):
        pass

    # Ensure that the subclass inherits the aliases declared on the superclass
    assert hasattr(SubSubWelcome, "hello") is True
    assert hasattr(SubSubWelcome, "greet") is True
    assert hasattr(SubSubWelcome, "sweet") is True

    # Create an instance of the subclass
    subsubwelcome = SubSubWelcome()

    # Ensure that the subclass inherits the aliases declared on the superclass
    assert hasattr(subsubwelcome, "hello") is True
    assert hasattr(subsubwelcome, "greet") is True
    assert hasattr(subsubwelcome, "sweet") is True

    # Ensure that the source method functionality operates as expected
    assert subsubwelcome.hello("me") == "hello: me"

    # Ensure that the aliased method functionality operates as expected
    assert subsubwelcome.greet("me") == "hello: me"

    # Ensure that the aliased method functionality operates as expected
    assert subsubwelcome.sweet("me") == "sweet, me!"
