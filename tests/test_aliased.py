from classicist import aliased, alias, aliases, is_aliased
from classicist.exceptions.decorators.aliased import AliasError

import pytest
import sys
import types
import conftest

# Obtain a reference to the current module
module = sys.modules[__name__]
assert isinstance(module, types.ModuleType)
assert module.__name__ == __name__


# Define and alias a module-level function for testing below
@alias("doubled")
def doubler(value: int) -> int:
    """Sample method that doubles and returns the provided number."""

    return value * 2


def test_alias_function():
    """Test using the @alias decorator on a  module-level function."""

    # Ensure that both the original function "doubler" and its alias exist in the module
    assert hasattr(module, "doubler")
    assert hasattr(module, "doubled")

    # Ensure that the module attributes directly reference the function objects
    # and ensure that the function names both exist in scope; by ensuring that
    # the aliased name also exists equally in scope and has the same visibility
    # we ensure that the module-level alias is working correctly
    assert getattr(module, "doubler") is doubler
    assert getattr(module, "doubled") is doubled

    assert doubler is doubled

    assert doubler(1) == 2
    assert doubled(2) == 4


def test_alias_function_defined_in_an_imported_module():
    """Test using the @alias decorator on an imported module-level function."""

    # Ensure that both the original function "halves" and its alias exist in the module
    assert hasattr(conftest, "halves")
    assert hasattr(conftest, "divide")

    # Ensure that the module attributes directly reference the function object and
    # that the original and aliased function names both exist in scope; by ensuring
    # that the aliased name exists equally in scope and has the same visibility as
    # the original function object, we confirm that the alias is working correctly
    assert getattr(conftest, "halves") is conftest.halves
    assert getattr(conftest, "divide") is conftest.divide

    # Ensure that the original and the alias refer to the same object in memory
    assert conftest.halves is conftest.divide

    # Test the original and aliased function names
    assert conftest.halves(2) == 1
    assert conftest.divide(4) == 2

    # Ensure that both the original and aliased function can be imported
    from conftest import halves, divide

    # Ensure that the imported names refer to the same object in memory
    assert conftest.halves is halves
    assert conftest.divide is divide

    # Test the original and aliased function names
    assert halves(2) == 1
    assert divide(4) == 2


def test_alias_class():
    """Test using the @alias decorator on a class."""

    @alias("Greeter")
    class Welcome(object):
        pass

    # Ensure that both the original and the aliased names exists
    assert isinstance(Welcome, type)
    assert isinstance(Greeter, type)

    # Ensure both the original and the aliased names refer to the same object in memory
    assert Welcome is Greeter
    assert Greeter is Welcome


def test_alias_class_method():
    """Test using the @alias decorator on a method."""

    # Create a sample class that aliases a method; due to the way that Python classes
    # are parsed by the interpreter, it is necessary to use a metaclass or custom base
    # class to apply the method aliases to the class scope, thus the use of the aliased
    # metaclass in the class definition below; this special metaclass scans the class'
    # methods, looking for any with assigned aliases, and then adds the aliases to the
    # class' scope so that the methods can be accessed both via their original name and
    # any aliases that have been defined; without the metaclass the aliases won't exist.
    class Welcome(metaclass=aliased):
        @alias("sweet", "greet")
        def hello(self, name: str) -> str:
            return f"hello: {name}"

    # Ensure both the original and the aliased names refer to the same object in memory
    assert Welcome.hello is Welcome.sweet
    assert Welcome.hello is Welcome.greet

    # Ensure both the original and the aliased names report as having been aliased
    assert is_aliased(Welcome.hello) is True
    assert is_aliased(Welcome.sweet) is True
    assert is_aliased(Welcome.greet) is True

    # Check that the class method object reports its aliases correctly
    assert aliases(Welcome.hello) == ["sweet", "greet"]


def test_alias_class_method_property():
    """Test using the @alias decorator with @property and @classmethod decorators."""

    class Welcome(metaclass=aliased):
        @property
        @alias("sweet", "greet")
        @classmethod
        def hello(self, name: str) -> str:
            return f"hello: {name}"

    # Ensure both the original and the aliased names refer to the same object in memory
    assert Welcome.hello is Welcome.sweet
    assert Welcome.hello is Welcome.greet

    # Ensure both the original and the aliased names report as having been aliased
    assert is_aliased(Welcome.hello) is True
    assert is_aliased(Welcome.sweet) is True
    assert is_aliased(Welcome.greet) is True

    # Check that the class method object reports its aliases correctly
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

    # Ensure that aliases are inherited by subclasses
    class SubWelcome(Welcome):
        pass

    # Ensure that aliases are inherited by subclasses
    assert hasattr(SubWelcome, "hello") is True
    assert hasattr(SubWelcome, "greet") is True

    # Ensure that aliases are inherited by subclass instances
    subwelcome = SubWelcome()

    # Ensure that aliases are inherited by subclass instances
    assert hasattr(subwelcome, "hello") is True
    assert hasattr(subwelcome, "greet") is True

    # Ensure that the aliased method functionality operates as expected
    assert subwelcome.hello("me") == "hello: me"
    assert subwelcome.greet("me") == "hello: me"

    # Ensure when an alias hasn't been registered that access raises an AttributeError
    with pytest.raises(AttributeError) as exception:
        assert subwelcome.sweet("me") == "hello: me"

        assert (
            str(exception)
            == "AttributeError: 'SubWelcome' object has no attribute 'sweet'. Did you mean: 'greet'?"
        )


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
