from classicist import Runtimer, runtimer, runtime, has_runtimer

import time


def test_runtimer_for_function():
    """Test the runtimer for a function."""

    @runtimer
    def complex(value: int, sleep: float = 0.01) -> int:
        time.sleep(sleep)
        return value * 2

    assert callable(complex)
    assert complex.__name__ == "complex"
    assert has_runtimer(complex)

    assert complex(value=2) == 4
    assert isinstance(timer := runtime(complex), Runtimer)
    assert 0.01 <= timer.duration < 0.02

    assert complex(value=2, sleep=0.02) == 4
    assert isinstance(timer := runtime(complex), Runtimer)
    assert 0.02 <= timer.duration < 0.03


def test_runtimer_for_class_method():
    """Test the runtimer for a class method."""

    class Test(object):
        @classmethod
        @runtimer  # Note that the @runtimer decorator *must* go before @classmethod
        def complex(cls, value: int, sleep: float = 0.01) -> int:
            time.sleep(sleep)
            return value * 2

    assert callable(Test.complex)
    assert Test.complex.__name__ == "complex"
    assert has_runtimer(Test.complex)

    assert Test.complex(value=2) == 4
    assert isinstance(timer := runtime(Test.complex), Runtimer)
    assert 0.01 <= timer.duration < 0.02

    assert Test.complex(value=2, sleep=0.02) == 4
    assert isinstance(timer := runtime(Test.complex), Runtimer)
    assert 0.02 <= timer.duration < 0.03


def test_runtimer_for_class_instance_method():
    """Test the runtimer for a class instance method."""

    class Test(object):
        @runtimer
        def complex(self, value: int, sleep: float = 0.01) -> int:
            time.sleep(sleep)
            return value * 2

    test = Test()

    assert isinstance(test, Test)

    assert callable(test.complex)
    assert test.complex.__name__ == "complex"
    assert has_runtimer(test.complex)

    assert test.complex(value=2) == 4
    assert isinstance(timer := runtime(test.complex), Runtimer)
    assert 0.01 <= timer.duration < 0.02

    assert test.complex(value=2, sleep=0.02) == 4
    assert isinstance(timer := runtime(test.complex), Runtimer)
    assert 0.02 <= timer.duration < 0.03


def test_has_runtimer_helper_method():
    """Test the has_runtimer() helper method."""

    @runtimer
    def function_with_runtimer():
        pass

    assert has_runtimer(function_with_runtimer) is True

    def function_without_runtimer():
        pass

    assert has_runtimer(function_without_runtimer) is False
