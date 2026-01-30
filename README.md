# Classicist: Classy Class Decorators & Extensions

The Classicist library provides several useful decorators and helper methods including:

 * `@hybridmethod` – a decorator that allows methods to be used both as class methods and as instance methods;
 * `@classproperty` – a decorator that allow class methods to be accessed as class properties;
 * `@annotation` – a decorator that can be used to apply arbitrary annotations to code objects;
 * `@deprecated` – a decorator that can be used to mark functions, classes and methods as being deprecated;
 * `@alias` – a decorator that can be used to add aliases to classes, methods defined within classes, module-level functions, and nested functions when overriding the aliasing scope;
 * `@nocache` – a decorator that can be used to mark functions and methods as not being suitable for caching;
 * `shadowproof` – a metaclass that can be used to protect subclasses from class-level attributes
  being overwritten (or shadowed) which can otherwise negatively affect class behaviour in some cases.

The `classicist` library was previously named `hybridmethod` so if a prior version had
been installed, please update references to the new library name. Installation of the
library via its old name, `hybridmethod`, will install the new `classicist` library with
a mapping for backwards compatibility so that code continues to function as before.

### Requirements

The Classicist library has been tested with Python 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14.
The library is not compatible with Python 3.8 or earlier.

### Installation

The Classicist library is available from PyPI, so may be added to a project's dependencies
via its `requirements.txt` file or similar by referencing the Classicist library's name,
`classicist`, or the library may be installed directly into your local runtime environment
using `pip` via the `pip install` command by entering the following into your shell:

	$ pip install classicist

#### Hybrid Methods

The Classicist library provides a `@hybridmethod` method decorator that allows methods
defined in a class to be used as both class methods and as instance methods.

The `@hybridmethod` decorator provided by the library wraps methods defined in classes
using the usual `@` decorator syntax. Methods defined in classes that are decorated with
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

If using the `isinstance(<variable>, <class>)` check as described above, substitute in
the name of the first argument variable of a hybrid method for the `<variable>` place
holder and the name of the class for the `<class>` place holder.

##### Hybrid Methods: Usage

To use the `@hybridmethod` decorator import the decorator from the `classicist` library
and use it to decorate the class methods you wish to use as both class methods and
instance methods:

```python
from classicist import hybridmethod

class hybridcollection(object):
    """An example class to demonstrate one possible use of a hybridmethod; here we have
    a list maintained at the class-level, accessible by all class instances as well as
    available directly on the class itself, as well as instance-level lists maintained
    individually by each instance of the class. The hybridmethod decorator allows the
    same methods to operate on the lists, affecting the relevant list, either the class
    or instance level list, based on whether the call was made directly on the class or
    if the call was made on an instance of the class."""

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

The Classicist library provides a `@classproperty` method decorator that allows class
methods to be accessed as class properties.

The `@classproperty` decorator provided by the library wraps methods defined in classes
using the usual `@` decorator syntax. Methods defined in classes that are decorated with
the `@classproperty` decorator can then be accessed as though they are real properties
on the class.

The `@classproperty` decorator addresses the removal in Python 3.13 of the prior support
for combining the `@classmethod` and `@property` decorators to create class properties;
a change which was made due to complexity in the underlying interpreter implementation.

##### Class Properties: Usage

To use the `@classproperty` decorator import the decorator from the `classicist` library
and use it to decorate any class methods you wish to access as class properties.

```python
from classicist import classproperty

class exampleclass(object):
    @classproperty
    def greeting(cls) -> str:
        """The 'greeting' class method has been decorated with classproperty so acts as
        a property; we can do some potentially complex work to compute return value."""
        return "hello"

assert isinstance(exampleclass, type)
assert issubclass(exampleclass, exampleclass)
assert issubclass(exampleclass, object)

# We can now access `.greeting` as though it was defined as a property.
# The return value of `.greeting` is indiscernible from the value being returned
assert isinstance(exampleclass.greeting, str)
assert exampleclass.greeting == "hello"
```

⚠️ An important caveat regarding class properties which applies equally to the method of
supporting class properties provided by this library, and to class properties which are
supported natively in Python 3.9 – 3.12 by combining the `@classmethod` and `@property`
decorators, is that unfortunately unless a custom metaclass is used to intervene, class
properties can be overwritten by value assignment, just like regular attributes can be.

This is a result of differences in Python's handling for descriptors between classes and
instances of classes. For both classes and instances, the `__get__` descriptor is called
while the `__set__` and `__delete__` descriptor methods will only be called on instances
such that we have no way to be involved in the property reassignment or deletion process
as would be the case for properties on instances where we can create our own setter and
deleter methods in addition to the getter.

This caveat can be remedied through a custom metaclass however, which overrides default
behaviour, and is able to intercept the `__setattr__` and `__delattr__` calls as needed.

The two code samples below illustrate the creation of a class property, `greeting`, via
this library's `@classproperty` decorator, and compares this to a class property created
natively in supported versions of Python by combining the `@classmethod` and `@property`
decorators. The code samples then highlight the possibility in both cases of overwriting
a class property by assigning a new value. The class property will be overwritten due to
standard attribute assignment behaviour. As such, whether using natively supported class
properties created by combining the `@classmethod` and `@property` decorators in Python
versions that support such class properties, or if using the `@classproperty` decorator
offered by this library, one must be mindful that a class property can be overwritten by
value assignment, unless one uses a custom metaclass to prevent such behaviour:

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

As can be seen with the method of natively supporting class properties, class properties
can also have their values reassigned without warning in just the same way:

```python
import sys
import pytest

# As Python only natively supported combining @classmethod and @property between version
# 3.9 and 3.12, the example below is not usable on other versions, such as 3.13+
if (sys.version_info.major == 3) and not (9 <= sys.version_info.minor <= 12):
    pytest.skip("This test can only run on Python version 3.9 – 3.12")

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

#### Alias Decorator & Metaclass: Add Aliases to Classes, Methods & Functions

The `@alias` decorator can be used to add aliases to classes, methods defined within
classes, module-level functions, and nested functions when overriding the aliasing scope,
such that both the original name and any defined aliases can be used to access the same
code object at runtime.

To alias a class or a module-level function, that is a function defined at the top-level
of a module file (rather than nested within a function or class), simply decorate the 
class or module-level function with the `@alias(...)` decorator and specify the one or
more name aliases for the class or function as one or more string arguments passed into
the decorator method.

To use the `@alias` decorator on methods defined within a class, it is also necessary to
set the containing class' metaclass to the `aliased` metaclass provided by the `classicist`
library; the metaclass iterates through the class' namespace during parse time and sets up
the aliases as additional attributes on the class so that the aliased methods are available
at runtime via both their original name and any aliases.

The examples below demonstrate adding an alias to a module-level function, a class and a
method defined within a class, and using the `aliased` metaclass when defining a class
that contains aliased methods to ensure that any aliases are parsed and translated to
additional class attributes so that the method is accessible via its original name and
any alias at runtime.

If control over the scope is required, usually for nested functions, the optional `scope`
keyword-only argument can be used to specify the scope into which to apply the alias; this
must be a reference to `globals()` or `locals()` at the point in code where the `@alias(...)`
decorator is applied to the nested function.

```python
from classicist import aliased, alias, is_aliased, aliases

# Define an alias on a module-level method; as this demonstration occurs
# within the README file which is parsed by and run within an external
# scope by pytest and pytest-codeblocks, we override the scope within
# which to apply the alias otherwise the alias would be assigned within
# an external scope which would prevent the alias from working; however
# it is rare to need to override the inferred scope, and aliasing of
# module-level functions defined within actual modules will work normally;
# for rare cases where overriding scope is necessary the optional `scope`
# keyword-only argument can be used as shown below.
@alias("sums", scope=globals())
def adds(a: int, b: int) -> int:
    return a + b

assert globals().get("adds") is adds
assert globals().get("sums") is sums
assert adds is sums
assert adds(1, 2) == 3
assert sums(1, 2) == 3

# Define an alias on a class
@alias("Color")
class Colour(object):
    pass

assert Colour is Color

# Define an alias on a method defined within a class;
# this also requires the use of the aliased metaclass
# which is responsible for adding the aliases within
# the scope of the class once the class has been parsed
class Welcome(metaclass=aliased):
    @alias("greet")
    def hello(self, name: str) -> str:
        return f"Hello {name}!"

assert is_aliased(Welcome.hello) is True

assert aliases(Welcome.hello) == ["greet"]

assert Welcome.hello is Welcome.greet

welcome = Welcome()

assert isinstance(welcome, Welcome)

assert welcome.hello("you") == "Hello you!"
assert welcome.greet("you") == "Hello you!"
```

⚠️ Note: Aliases must be valid Python identifiers, following the same rules as for all
other function and method names and aliases cannot be reserved keywords. If an invalid
alias is specified an `AliasError` exception will be raised at runtime. Furthermore, if
a name has already been used in the current scope, an `AliasError` exception will be
raised at runtime.

#### Annotation Decorator: Add Arbitrary Annotations to Code Objects

The `@annotation` decorator can be used to assign arbitrary annotations to mutable code
objects including classes, methods, functions and most objects, with the exception of
immutable objects that do not allow their attributes to be modified. The annotations
can be used for any purpose, such as to assist with generating documentation for the
annotated code objects, or for storing addition metadata on the code objects themselves
which can be accessed later.

Annotations applied to a code object using the `@annotation` decorator can be accessed via
the `annotations()` helper method which provides easy access to the assigned annotations:

```python
from classicist import annotation, annotations

class Test(object):
    @annotation(added="01/12/2026")
    def new(self):
        pass

assert annotations(Test.new) == dict(added="01/12/2026")
```

#### Deprecation Decorator: Mark Functions and Methods as Deprecated

The `@deprecated` decorator can be used to mark code objects such as methods and functions
as deprecated and for checking deprecated status of such objects via the `is_deprecated`
helper method.

The `@deprecated` decorator and `is_deprecated` helper method can be used as follows:

```python
from classicist import deprecated, is_deprecated

class Test(object):
    @deprecated
    def old(self):
        pass

    def new(self):
        pass

assert is_deprecated(Test.old) is True
assert is_deprecated(Test.new) is False
```

One can also add arbitrary annotations via the `@deprecated` decorator, specifying each
annotation as a keyword argument. The `@deprecated` decorator supports several optional
annotations by default, and these can be used to note common attributes of a deprecation
including when the deprecation began, the reason for the deprecation, when the deprecated
code will be removed, a reference to its replacement functionality (if applicable), and
advice on the replacement functionality's use, and a reference to ticket (if applicable)
tracking the deprecation. These default annotations may be specified by using the following
keyword arguments on the `@deprecated` decorator:

 * `reason` (`str`) – The optional `reason` keyword argument can be used to specify a
  reason note for the deprecation which can be useful for users to understand the change
  and can also be obtained from the deprecation annotation for use in documentation.

 * `since` (`str` | `datetime.datetime`) – The optional `since` keyword argument can be
  used to specify when the date for when the deprecation began; the argument can accept
  a string formatted date or a `datetime.datetime` instance. The `since` value serves to
  note when the deprecation began which can be useful in cases where there is a standard
  deprecation window of say six-twelve months before deprecated code is removed. The date
  is visible in the deprecation annotation and can also be obtained for use in documentation.

 * `removal` (`str` | `datetime.datetime`) – The optional `removal` keyword argument can be
  used to specify when the date for when the deprecated code will be removed; the argument
  can accept a string formatted date or a `datetime.datetime` instance. The `removal` value
  serves to note when the deprecation began which can be useful in cases where there is a
  standard deprecation window of say six-twelve months before deprecated code is removed.
  The date is visible at the site of the deprecation and can also be obtained for use in
  documentation.

 * `replacement` (`str`) – The optional `replacement` keyword argument can be used to
  specify a note about the replacement functionality (if applicable) that can be used
  instead of the deprecated functionality. The replacement note is visible at the site
  of the deprecation and can also be obtained for use in documentation.

 * `advice` (`str`) – The optional `advice` keyword argument can be used to specify any
  relevant advice about the replacement functionality (if applicable) that can be used
  instead of the deprecated functionality. The advice note is visible at the site of the
  deprecation and can also be obtained for use in documentation.

 * `ticket` (`str`) – The optional `ticket` keyword argument can be used to specify a
  reference to a ticket number or a ticket URL that is being used to track the deprecation.
  The ticket value is visible at the site of the deprecation and can also be obtained for
  use in documentation.

In addition to the default annotations, any other desired annotation can be added to via
the `@deprecated` decorator by specifying it as an additional keyword argument value. All
keyword argument values must be valid keyword argument identifiers and not be reserved words.

```python
from classicist import deprecated, is_deprecated, annotations

class Test(object):
    @deprecated(since="01/01/2026")
    def old(self):
        pass

    def new(self):
        pass

assert is_deprecated(Test.old) is True
assert is_deprecated(Test.new) is False

# The annotations can be obtained and accessed by using the `annotations` helper method:
assert annotations(Test.old) == dict(since="01/01/2026")
```

#### No Cache Decorator: Mark Functions and Methods as "Not Cacheable"

The `@nocache` decorator can be used to mark functions and methods as not being suitable
for caching via say `functools.cache`.

⚠️ Note: The `@nocache` decorator does not prevent caching via mechanisms such as the
`functools.cache` decorator, but rather acts as a clear note directly in code that the
function or method should not be cached via such means.

The `@nocache` decorator can be used as follows:

```python
from classicist import nocache

class Test(object):
    @nocache
    def computation(self) -> int:
        pass
```

#### ShadowProof: Attribute Shadowing Protection Metaclass

The `shadowproof` metaclass can be used to protect classes and subclasses from attribute
-shadowing. The issue is usually caused by a subclass unintentionally redefining or
overwriting an attribute value that has been inherited from a superclass and can
otherwise be quite difficult to debug, as it may lead to unexpected behaviour in either
the superclass or subclass without an immediately obvious cause. Python does not issue
any warnings or raise any errors when most attributes are overwritten, aside from special
cases mostly in the standard library on immutable objects. The `shadowproof` metaclass
helps solve this issue by raising an `AttributeShadowingError` when this happens.

To use the `shadowproof` metaclass to protect a class and its subclasses, implement code
similar to the following, by importing the `shadowproof` metaclass and assigning it as
the metaclass for the class and subclasses you want to protect:

```python
from classicist import shadowproof, AttributeShadowingError

class Test(object, metaclass=shadowproof):
    example: int = 123

try:
    class SubTest(Test):
        example: str = "hello"
except AttributeShadowingError as exception:
    # The AttributeShadowingError is expected as the `example` attribute was modified!
    pass
```

### Unit Tests

The Classicist library includes a suite of comprehensive unit tests which ensure that
the library functionality operates as expected. The unit tests were developed with and
are run via `pytest`.

To ensure that the unit tests are run within a predictable runtime environment where all
of the necessary dependencies are available, a [Docker](https://www.docker.com) image is
created within which the tests are run. To run the unit tests, ensure Docker and Docker
Compose is [installed](https://docs.docker.com/engine/install/), and perform the following
commands, which will build the Docker image via `docker compose build` and then run the
tests via `docker compose run` – the output of running the tests will be displayed:

```shell
$ docker compose build
$ docker compose run tests
```

To run the unit tests with optional command line arguments being passed to `pytest`, append
the relevant arguments to the `docker compose run tests` command, as follows, for example
passing `-vv` to enable verbose output:

```shell
$ docker compose run tests -vv
```

See the documentation for [PyTest](https://docs.pytest.org/en/latest/) regarding available
optional command line arguments.

### Copyright & License Information

Copyright © 2025-2026 Daniel Sissman; licensed under the MIT License.