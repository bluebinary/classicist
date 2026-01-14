import pytest

from classicist import classproperty


@pytest.fixture(scope="module", name="exampleclass")
def test_classproperty_fixture() -> type:
    class exampleclass(object):
        @classproperty
        def name(cls) -> str:
            return cls.__name__

    return exampleclass


def test_classproperty(exampleclass: type):
    """Test the classproperty decorator on a demonstration class."""

    assert isinstance(exampleclass, type)
    assert issubclass(exampleclass, exampleclass)

    assert isinstance(exampleclass.name, str)
    assert exampleclass.name == "exampleclass"


def test_classproperty_overwrite(exampleclass: type):
    # Unfortunately without a metaclass to intervene, classproperties can be overwritten
    # as although Python by default calls the __get__ descriptor method it will not
    # automatically call the __set__ or __delete__ descriptor methods on classes, so we
    # have no way to prevent the property being reassigned unless a metaclass is used to
    # intervene and provide behaviour we had previously with @classmethod and @property
    exampleclass.name = "hello"
    assert exampleclass.name == "hello"
