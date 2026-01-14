# Test the @deprecated object decorator and the is_deprecated() helper method

from classicist import deprecated, is_deprecated, annotations


def test_deprecated_decorator_on_standalone_function_without_annotations():
    """Test deprecating a standalone function without specifying any annotations."""

    @deprecated
    def sample_function_one():
        """Sample function one documentation."""

        return 123

    assert callable(sample_function_one)

    assert sample_function_one.__name__ == "sample_function_one"
    assert sample_function_one.__doc__ == "Sample function one documentation."

    assert is_deprecated(sample_function_one) is True
    assert annotations(sample_function_one) == {}


def test_deprecated_decorator_on_standalone_function_with_annotation():
    """Test deprecating a standalone function with an arbitrary annotation."""

    @deprecated(since="2025-12-04")
    def sample_function_two():
        """Sample function two documentation."""

        return 123

    assert callable(sample_function_two)

    assert sample_function_two.__name__ == "sample_function_two"
    assert sample_function_two.__doc__ == "Sample function two documentation."

    assert is_deprecated(sample_function_two) is True
    assert annotations(sample_function_two) == {"since": "2025-12-04"}


def test_deprecated_decorator_on_class():
    """Test the @deprecated decorator on a class, class method and instance method."""

    # Test deprecating a class with an arbitrary annotation
    @deprecated(since="2025-12-01")
    class Sample(object):
        """Sample class documentation."""

        # Test deprecating a class method with an arbitrary annotation
        @classmethod
        @deprecated(since="2025-12-02")
        def old_class_method(cls) -> int:
            """Test deprecating a class method."""
            return 123

        # Test deprecating an instance method with an arbitrary annotation
        @deprecated(since="2025-12-03")
        def old_method(self) -> int:
            """Test deprecating an instance method."""
            return 123

        def new_method(self) -> int:
            return 123

    # Ensure that the @deprecated decorator did not affect access to class properties
    assert isinstance(Sample, type)
    assert Sample.__name__ == "Sample"
    assert Sample.__doc__ == "Sample class documentation."

    # Ensure that the Sample class annotations are present and as expected
    assert annotations(Sample) == {"since": "2025-12-01"}

    # Ensure that the @deprecated decorator did not affect access to method properties
    assert callable(Sample.old_class_method)
    assert Sample.old_class_method.__self__ is Sample
    assert Sample.old_class_method.__name__ == "old_class_method"

    # Ensure that the Sample.old_class_method has been marked as deprecated
    assert is_deprecated(Sample.old_class_method) is True

    # Ensure that the Sample.old_class_method annotations are present and as expected
    assert annotations(Sample.old_class_method) == {"since": "2025-12-02"}

    # Create an instance of the class
    sample = Sample()

    # Ensure that the instance reports the expected type
    assert isinstance(sample, Sample)

    # Ensure that the instance and its underlying class have been marked as deprecated
    assert is_deprecated(sample) is True
    assert is_deprecated(sample.__class__) is True

    # Ensure that the Sample class and instance annotations are present and as expected
    assert annotations(sample.__class__) == {"since": "2025-12-01"}
    assert annotations(sample) == {"since": "2025-12-01"}

    # Ensure that the @deprecated decorator did not affect access to method properties
    assert hasattr(sample, "old_method")
    assert sample.old_method.__self__ is sample

    # Ensure that the Sample.old_method has been marked as deprecated
    assert is_deprecated(sample.old_method) is True

    # Ensure that the Sample.old_method annotations are present and as expected
    assert annotations(sample.old_method) == {"since": "2025-12-03"}

    # Ensure that the @deprecated decorator did not affect access to method properties
    assert hasattr(sample, "new_method")
    assert sample.new_method.__self__ is sample

    # Ensure that the Sample.new_method has not been marked as deprecated
    assert is_deprecated(sample.new_method) is False

    # Ensure that the Sample.new_method has no annotations
    assert annotations(sample.new_method) is None
