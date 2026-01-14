from classicist import annotation, annotations, annotate


def test_annotation_of_function():
    """Test the annotation decorator on a demonstration function."""

    # Add several annotations to a function object
    @annotation(one=1, two=2, three=3)
    def test_function():
        return "<test_function>"

    assert callable(test_function)
    assert test_function.__name__ == "test_function"

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(test_function) == dict(one=1, two=2, three=3)


def test_annotation_of_class_and_method():
    """Test the annotation decorator on a demonstration class."""

    # Add several annotations to a function object
    @annotation(one=1, two=2, three=3)
    def test_function():
        return "<test_function>"

    assert callable(test_function)
    assert test_function.__name__ == "test_function"

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(test_function) == dict(one=1, two=2, three=3)

    # Add several annotations to the class object
    @annotation(one=1, two=2, three=3, four=4)
    class Test(object):
        # Add several annotations to the class method object
        @annotation(one=1, two=2, three=3, four=4, five=5)
        def test_method():
            return "<test_method>"

    assert isinstance(Test, type)
    assert issubclass(Test, object)

    assert Test.__name__ == "Test"
    assert callable(Test.test_method)
    assert Test.test_method.__name__ == "test_method"

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(Test) == dict(one=1, two=2, three=3, four=4)

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(Test.test_method) == dict(one=1, two=2, three=3, four=4, five=5)


def test_annotation_of_class_type_object():
    """Test the annotation decorator on a demonstration thing."""

    @annotation(zero=0)
    class Thing(object):
        pass

    # Add several more annotations to the class object (adding annotations is additive)
    thing = annotate(Thing, one=1, two=2, three=3)

    assert thing is Thing

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(thing) == dict(zero=0, one=1, two=2, three=3)


def test_annotation_of_class_instance_object():
    """Test the annotation decorator on a demonstration thing."""

    class Thing(object):
        pass

    thing = Thing()

    # Add several annotations to a class object
    thing = annotate(thing, one=1, two=2, three=3)

    assert isinstance(thing, object)

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(thing) == dict(one=1, two=2, three=3)


def test_annotation_of_function_object():
    """Test the annotation decorator on a demonstration thing."""

    def thing() -> int:
        return 123

    # Add several annotations to a function object
    thing = annotate(thing, one=1, two=2, three=3)

    assert isinstance(thing, object)

    # Ensure that the annotations were set and can be retrieved as expected
    assert annotations(thing) == dict(one=1, two=2, three=3)
