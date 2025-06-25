# Classicist: Classy Class Decorators & Extensions

The Classicist library provides several useful class decorators for Python class methods
including a `hybridmethod` decorator that allows methods defined in a class to be used
both a class method and an instance method, and a `classproperty` decorator that allows
class methods to be accessed as class properties.

The `classicist` library was previously named `hybridmethod` so if a prior version had been
installed, please update references to the new library name. Installation of the
library via its old name, `hybridmethod`, will install the new `classicist` library with
a mapping for backwards compatibility so that code continues to function as before.

### Requirements

The Classicist library has been tested with Python 3.9, 3.10, 3.11, 3.12 and 3.13. The library is not compatible with Python 3.8 or earlier.

### Installation

The Classicist library is available from PyPI, so may be added to a project's dependencies via its `requirements.txt` file or similar by referencing the Classicist library's name, `classicist`, or the library may be installed directly into your local runtime environment using `pip` via the `pip install` command by entering the following into your shell:

	$ pip install classicist

#### Hybrid Methods

The Classicist library provides a `hybridmethod` method decorator that allows methods
defined in a class to be used as both a class method and an instance method.

The `@hybridmethod` decorator provided by the library wraps methods defined in classes
using the usual `@decorator` syntax. Methods defined in classes that are decorated with
the `@hybridmethod` decorator can then be accessed as both class methods and as instance
methods, with the first argument passed to the method being a reference to either the
class when the method is called as a class method or to the instance when the method is
called as an instance method.

If a class-level property is defined and then an instance-level property is created with
the same name that shadows the class-level property, the hybrid method can be used to
interact with both the class-level property and the instance-level property simply based
on whether the hybrid method was called directly on the class or on an a class instance.

If desired, a simple check of the value of the first variable passed to a hybrid method
using `isinstance(<variable>, <class>)` allows one to determine if the call was made on
an instance of the class in which case `isinstance()` evaluates to `True` or if the call
was made on the class itself, in which case `isinstance()` evaluates to `False`.

The variable passed as the first argument to the method may have any name, including as
is common in Python, `self`, although the use of `self` as the name of this argument on
an instance method is just customary and the name has no significance.

If using the `isinstance(<variable>, <class>)` check as described above is used simply
substitute in the name of the first variable of a hybrid method for `<variable>` and the
name of the class for `<class>`.

#### Hybrid Methods: Usage

To use the `hybridmethod` decorator import the decorator from the `classicist` library
and use it to decorate the class methods you wish to use as both class methods and
instance methods:

```python
from classicist import hybridmethod

class hybridcollection(object):
    items: list[str] = []

    def __init__(self):
        # Create an 'items' instance variable; note that this shadows the class variable
        # of the same name which can still be accessed directly via self.__class__.items
        self.items: list[object] = []

    @hybridmethod
    def add_item(self, item: object):
        # We can use the following line to differentiate between the call being made on
        # an instance or directly on the class; isinstance(self, <class>) returns True
        # if the method was called on an instance of the class, or False if the method
        # was called on the class directly; the 'self' variable will reference either
        # the instance or the class; although 'self' is traditionally used in Python as
        # reference to the instance
        if isinstance(self, hybridcollection):
            self.items.append(item)
        else:
            self.items.append(item)

    def get_class_items(self) -> list[object]:
        return self.__class__.items

    def get_instance_items(self) -> list[object]:
        return self.items

    def get_combined_items(self) -> list[object]:
        return self.__class__.items + self.items

hybridcollection.add_item("ABC")  # Add an item to the class-level items list

collection = hybridcollection()

collection.add_item("XYZ")  # Add an item to the instance-level items list

assert collection.get_class_items() == ["ABC"]

assert collection.get_instance_items() == ["XYZ"]

assert collection.get_combined_items() == ["ABC", "XYZ"]
```

#### Class Properties

The Classicist library provides a `classproperty` method decorator that allows class
methods to be accessed as class properties.

The `@classproperty` decorator provided by the library wraps methods defined in classes
using the usual `@decorator` syntax. Methods defined in classes that are decorated with
the `@classproperty` decorator can then be accessed as though they were real properties
on the class.

The `@classproperty` decorator addresses the removal in Python 3.13 of the prior support
for combining the `@classmethod` and `@property` decorators to create class properties,
a change which was made due to complexity in the underlying interpreter implementation.

#### Class Properties: Usage

To use the `classproperty` decorator import the decorator from the `classicist` library
and use it to decorate any class methods you wish to access as class properties.

```python
from classicist import classproperty

class exampleclass(object):
    @classproperty
    def greeting(cls) -> str:
        """The 'greeting' class method has been decorated with classproperty so acts as
        a property; here we could do some work to generate a return value."""
        return "hello"

assert isinstance(exampleclass, type)
assert issubclass(exampleclass, exampleclass)
assert issubclass(exampleclass, object)

# We can access `.greeting` as though it was defined as a property:
# The return value of `.greeting` is indiscernible from the value being returned
assert isinstance(exampleclass.greeting, str)
assert exampleclass.greeting == "hello"
```

⚠️ An important caveat regarding class properties which applies equally to the method of
supporting class properties provided by this library, and to class properties which are
supported natively in Python 3.9 – 3.12 by combining the `@classmethod` and `@property`
decorators, is that unfortunately unless a custom metaclass is used to intervene, class
properties can be overwritten by value assignment.

This is a result of differences in Python's handling for descriptors between classes and
instances of classes. For both classes and instances, the `__get__` descriptor is called
while the `__set__` and `__delete__` descriptor methods will only be called on instances
such that we have no way to be involved in the property reassignment or deletion process
as would be the case for properties on instances where we can create our own setter and
deleter methods in addition to the getter.

This caveat can be remedied through a custom metaclass however, which overrides default
behaviour, and is able to intercept the `__setattr_` and `__delattr__` calls as needed.

```python
from classicist import classproperty

class exampleclass(object):
    @classproperty
    def greeting(cls) -> str:
        # Generate a return value here
        return "hello"

# We can access `.greeting` as though it was defined as a property:
assert exampleclass.greeting == "hello"

# Note: The `.greeting` property will be reassigned to the new value, "goodbye":
exampleclass.greeting = "goodbye"
assert exampleclass.greeting == "goodbye"
```

As can be seen with the method of natively supporting class properties, they could also
have their values reassigned without warning:

```python
import sys
import pytest

# As Python only natively supported combining @classmethod and @property between version
# 3.9 and 3.12, the example below is not usable on other versions, such as 3.13+
if sys.version_info.major == 3 and not (9 <= sys.version_info.minor <= 12):
    pytest.skip("This test can run on Python versions 3.9 – 3.12")

class exampleclass(object):
    @classmethod
    @property
    def greeting(cls) -> str:
        # Generate a return value here
        return "hello"

# We can access `.greeting` as though it was defined as a property:
assert exampleclass.greeting == "hello"

# Note: The `.greeting` property will be reassigned to the new value, "goodbye":
exampleclass.greeting = "goodbye"
assert exampleclass.greeting == "goodbye"
```

### Unit Tests

The Classicist library includes a suite of comprehensive unit tests which ensure that
the library functionality operates as expected. The unit tests were developed with and
are run via `pytest`.

To ensure that the unit tests are run within a predictable runtime environment where all of the necessary dependencies are available, a [Docker](https://www.docker.com) image is created within which the tests are run. To run the unit tests, ensure Docker and Docker Compose is [installed](https://docs.docker.com/engine/install/), and perform the following commands, which will build the Docker image via `docker compose build` and then run the tests via `docker compose run` – the output of running the tests will be displayed:

```shell
$ docker compose build
$ docker compose run tests
```

To run the unit tests with optional command line arguments being passed to `pytest`, append the relevant arguments to the `docker compose run tests` command, as follows, for example passing `-vv` to enable verbose output:

```shell
$ docker compose run tests -vv
```

See the documentation for [PyTest](https://docs.pytest.org/en/latest/) regarding available optional command line arguments.

### Copyright & License Information

Copyright © 2025 Daniel Sissman; licensed under the MIT License.