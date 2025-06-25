import pytest

from classicist import hybridmethod


@pytest.fixture(scope="module", name="hybridcollection")
def test_hybridmethod_fixture() -> type:
    """Test the hybridmethod decorator on the 'hybridcollection' demonstration class."""

    class hybridcollection(object):
        """This sample class provides hybrid methods that allow items to be added to and
        removed from the class-level list and item-level list without needing to define
        separate methods to manage the lists. The class also provides helper methods for
        accessing the class-level list, instance-level list, and a combined list."""

        items: list[object] = []

        def __init__(self):
            # Create an 'items' instance variable; note this shadows the class variable
            # of the same name which can still be accessed via self.__class__.items
            self.items: list[str] = []

        @hybridmethod
        def add_item(self, item: object):
            # We can use the following line to differentiate between the call being made
            # on an instance or directly on the class; isinstance(self, <class>) returns
            # True if the method was called on an instance of the class, or False if the
            # method was called on the class directly; the variable 'self' references
            # either the instance or the class; although 'self' is traditionally used in
            # Python as reference to the instance; the variable can be named anything:
            if isinstance(self, hybridcollection):
                self.items.append(item)
            else:
                self.items.append(item)

        @hybridmethod
        def remove_item(self, item: object):
            if (index := self.items.index(item)) >= 0:
                del self.items[index]

        def get_class_items(self) -> list[object]:
            return self.__class__.items

        def get_instance_items(self) -> list[object]:
            return self.items

        def get_combined_items(self) -> list[object]:
            return self.__class__.items + self.items

    return hybridcollection


def test_hybridmethod(hybridcollection: type):
    """Test the hybridmethod decorator through an example use case of a class providing
    access to a class-level list and instance-level list that are separately held in
    memory and can be added to and removed from without affecting the other, while also
    offering a method that returns a combined list of the items held in both lists."""

    # Ensure that the hybridcollection type is of the expected type
    assert isinstance(hybridcollection, type)

    # Ensure that the hybridcollection type has an items list
    assert isinstance(hybridcollection.items, list)

    # Ensure that the class' items list is empty to begin with
    assert len(hybridcollection.items) == 0

    # Add an item to the class' items list
    hybridcollection.add_item("ABC")

    # Ensure that the class' items list length now reflects the newly added item
    assert len(hybridcollection.items) == 1

    # Ensure that the class' items list has the expected contents
    assert hybridcollection.items == ["ABC"]

    # Create an instance of the class
    collection = hybridcollection()

    # Ensure that the instance is of the expected type
    assert isinstance(collection, hybridcollection)

    # Ensure that the instance has an items list
    assert isinstance(collection.items, list)

    # Ensure that the instance's items list is empty
    assert len(collection.items) == 0

    # Add an item to the instance's item list
    collection.add_item("XYZ")

    # Ensure that the instance's items list length now reflects the newly added item
    assert len(collection.items) == 1

    # Ensure that the instance's items list has the expected contents
    assert collection.items == ["XYZ"]

    # Ensure that the instance's items list has the expected contents, in this case
    # as accessed via the class' get_instance_items helper method:
    assert collection.get_instance_items() == ["XYZ"]

    # Ensure that the class' items list still has the expected contents and was not
    # affected by the addition of an item to the instance's items list, in this case
    # as accessed via the class reference on the instance:
    assert collection.__class__.items == ["ABC"]

    # Ensure that the class' items list still has the expected contents and was not
    # affected by the addition of an item to the instance's items list, in this case
    # as accessed via the class' get_class_items helper method:
    assert collection.get_class_items() == ["ABC"]

    # Ensure that the combined items held in the class' and the instance's items list
    # are as expected, in this case as accessed via the items lists directly:
    assert collection.__class__.items + collection.items == ["ABC", "XYZ"]

    # Ensure that the combined items held in the class' and the instance's items list
    # are as expected, in this case accessed via the get_combined_items helper method:
    assert collection.get_combined_items() == ["ABC", "XYZ"]

    # Add another item to the instance's item list
    collection.add_item(123)

    # Ensure that the class' items list still contains the expected number of items
    assert len(hybridcollection.items) == 1

    # Ensure that the class' items list still contains the expected items
    assert hybridcollection.items == ["ABC"]

    # Ensure that the instance's items list contains the expected number of items
    assert len(collection.items) == 2

    # Ensure that the instance's items list contains the expected items
    assert collection.items == ["XYZ", 123]

    # Remove an item from the list
    collection.remove_item("XYZ")

    # Ensure that the instance's items list contains the expected number of items
    assert len(collection.items) == 1

    # Ensure that the instance's items list contains the expected items
    assert collection.items == [123]

    # Ensure that the class' items list still contains the expected number of items
    assert len(hybridcollection.items) == 1

    # Ensure that the class' items list still contains the expected items
    assert hybridcollection.items == ["ABC"]
