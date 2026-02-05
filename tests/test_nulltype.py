from __future__ import annotations

from classicist import NullType, Null


def test_nulltype():
    """Test the `NullType` class."""

    assert isinstance(NullType, type)
    assert issubclass(NullType, object)


def test_nulltype_instantiation():
    """Test the instantiation of the `NullType` class."""

    # Create an instance of the NullType class (this should return the singleton)
    null1 = NullType()

    # Ensure it has the expected type
    assert isinstance(null1, NullType)

    # Create an instance of the NullType class (this should return the singleton)
    null2 = NullType()

    # Ensure it has the expected type
    assert isinstance(null2, NullType)

    # Ensure that the NullType can only create and return a singleton instance; as all
    # instances should pass identity checks with each other via the `is` operator:
    assert null1 is null2

    # Ensure any NullType instances are all the same, and are the same as the singleton
    assert null1 is null2 is Null


def test_nulltype_singleton():
    """Test the `Null` singleton instance's type."""

    assert isinstance(Null, NullType)


def test_nulltype_string_representation():
    """Test the `Null` singleton instance's string representation."""

    assert str(Null) == "Null"


def test_nulltype_debug_string_representation():
    """Test the `Null` singleton instance's debug string representation."""

    assert repr(Null) == "Null"


def test_nulltype_arbitrary_attribute_access():
    """Test arbitrary attribute access on the `Null` singleton instance."""

    thing = Null

    assert thing.a is Null
    assert thing.a.b is Null
    assert thing.a.c is Null
    assert thing.a.c.d is Null
    assert thing.a.c.d.e is Null
    assert thing.a.c.d.e.f is Null


def test_nulltype_boolean_comparison():
    """Test arbitrary attribute boolean comparison on the `Null` singleton instance."""

    thing: object = Null

    # We expect that these non-existent nested attributes will boolean compare as falsey
    # hence the use of `assert not` in the tests below:
    assert not thing.a
    assert not thing.a.b
    assert not thing.a.c
    assert not thing.a.c.d
    assert not thing.a.c.d.e
    assert not thing.a.c.d.e.f


def test_nulltype_boolean_comparison_with_if_else_statement():
    """Test arbitrary attribute boolean comparison on the `Null` singleton instance."""

    thing: object = Null

    exists: bool = None

    # Test the boolean comparison through an `if-else` statement
    if thing.a.b.c.d.e.f:
        exists = True
    else:
        exists = False  # We expect to reach this assignment as `if` should not pass

    # Ensure that the result of the if-else statement is as expected
    assert exists is False


def test_nulltype_boolean_comparison_with_if_not_else_statement():
    """Test arbitrary attribute boolean comparison on the `Null` singleton instance."""

    thing: object = Null

    exists: bool = None

    # Test the boolean comparison through an `if-else` statement
    if not thing.a.b.c.d.e.f:
        exists = False  # We expect to reach this assignment as `if not` should pass
    else:
        exists = True

    # Ensure that the result of the if-not-else statement is as expected
    assert exists is False


def test_nulltype_identity_comparison():
    """Test arbitrary attribute boolean comparison on the `Null` singleton instance."""

    thing: object = Null

    # We expect that the identity comparisons to True should *not* pass
    assert not thing.a is True
    assert not thing.a.b is True

    # We expect that the identity comparisons to False should *not* pass
    assert not thing.a is False
    assert not thing.a.b is False

    # We expect that the identity comparisons to None should *not* pass
    assert not thing.a is None
    assert not thing.a.b is None

    # We expect identity comparisons to anything other than `Null` should *not* pass
    assert not thing.a == 123
    assert not thing.a.b == 123

    # We expect that the identity comparison to the `Null` singleton *will* pass
    assert thing.a is Null
    assert thing.a.b is Null


def test_nulltype_with_a_custom_data_model():
    """Test the `Null` singleton instance in a custom data model to demonstrate the
    ability to use the `Null` singleton instead of `None` for a null-safe experience."""

    data: dict = {
        "id": 1,
        "name": "A",
        "related": {
            "id": 2,
            "name": "B",
            "related": {
                "id": 3,
                "name": "C",
            },
        },
    }

    class Model(object):
        """Sample Model with some properties that reference nested Model instances."""

        def __init__(self, data: dict):
            if not isinstance(data, dict):
                raise TypeError(
                    "The 'data' argument must reference a valid data dictionary!"
                )

            if not ("id" in data and isinstance(data["id"], int)):
                raise ValueError(
                    "The 'data' must contain an 'id' key with an integer value!"
                )

            if not ("name" in data and isinstance(data["name"], str)):
                raise ValueError(
                    "The 'data' must contain an 'name' key with an string value!"
                )

            self.data = data

        @property
        def id(self) -> int:
            return self.data["id"]

        @property
        def name(self) -> str:
            return self.data["name"]

        @property
        def related(self) -> Model | Null:
            if data := self.data.get("related"):
                return Model(data=data)
            else:
                return Null

        @property
        def relates(self) -> Model | Null:
            if data := self.data.get("relates"):
                return Model(data=data)
            else:
                return Null

    # Create an instance of the sample Model data class
    model = Model(data=data)

    # Check that the expected data attributes are available
    assert model.id == 1
    assert model.name == "A"

    # The model.related property references A/1 in the data above, so these properties exist
    assert model.related
    assert model.related.id
    assert model.related.name

    # Ensure the nested property values are as expected
    assert model.related.id == 2
    assert model.related.name == "B"

    # Note that model.relates had no corresponding data, so the Model returns `Null` which
    # still allows for nested attribute access, such as to `.id` and `.name` without raising
    # any exceptions; the `Null` singleton also allows for `bool` comparison as shown below:
    assert not model.relates
    assert not model.relates.id
    assert not model.relates.name

    # There is no limit to the levels of nesting that `NullType` and the `Null` singleton
    # can support, so long as a custom data model or library consistently returns `Null`
    # for cases where the "null-safe" navigation is desired:

    # model.related.related references 3/C in the data above, so these properties exist
    assert model.related.related.id
    assert model.related.related.name

    # model.related.relates was not specified in the data above so the Model returns `Null`
    assert not model.related.relates.id
    assert not model.related.relates.name

    # Ensure the nested property values are as expected
    assert model.related.related.id == 3
    assert model.related.related.name == "C"

    # These features make it easy to write clearer more expressive code without
    # boilerplate code to check for the availability of nested attributes or entities:
    if isinstance(name := model.related.name, str):
        print("model.related.name => %s" % (name))

    # No exception is raised here even though model.relates is effectively "null":
    if isinstance(name := model.relates.name, str):
        print("model.relates.name => %s" % (name))

    # However, there are some caveats as noted with `NullType` and the `Null` singleton
    # as these are a third-party solution so we can only go so far in supplementing
    # null-safe operator behaviour in the language; for example, we cannot perform
    # identity checks to the boolean values, True or False, or None singleton value:

    # Notice the `assert not` as `assert` would fail here
    assert not model.relates is True

    # Notice the `assert not` as `assert` would fail here
    assert not model.relates is False

    # Notice the `assert not` as `assert` would fail here
    assert not model.relates is None

    # We can however perform an identity check against the `Null` singleton if needed:
    assert model.relates is Null
