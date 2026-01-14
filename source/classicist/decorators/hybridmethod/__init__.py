from classicist.logging import logger

logger = logger.getChild(__name__)


class hybridmethod(object):
    """The 'hybridmethod' decorator allows a method to be used as both a class method
    and an instance method. The hybridmethod class decorator can wrap methods defined
    in classes using the usual @decorator syntax. Methods defined in classes that are
    decorated with the @hybridmethod decorator can be accessed as both class methods
    and as instance methods, with the first argument passed to the method being the
    reference to either the class when the method is called as a class method or to
    the instance when the method is called as an instance method.

    A check of the value of the first variable using isinstance(<variable>, <class>) can
    be used within a hybrid method to determine if the call was made on an instance of
    the class in which case the isinstance() call would evalute to True or if the call
    was made on the class itself, in which case isinstance() would evaluate to False.
    The variable passed as the first argument to the method may have any name, including
    'self', as in Python, the use of 'self' as the name of the first argument on an
    instance method is just customary and the name has no significance like it does in
    other languages where the reference to the instance is provided automatically and
    may go by 'self', 'this' or something else."""

    def __init__(self, function: callable):
        logger.debug(
            "%s.__init__(function: %s)",
            self.__class__.__name__,
            function,
        )

        if not callable(function):
            raise TypeError(
                "The '%s' decorator can only be used to wrap callables!"
                % (self.__class__.__name__)
            )
        elif not type(function).__name__ == "function":
            raise TypeError(
                "The '%s' decorator can only be used to wrap functions!"
                % (self.__class__.__name__)
            )

        self.function: callable = function

    def __get__(self, instance, owner) -> callable:
        logger.debug(
            "%s.__get__(self: %s, instance: %s, owner: %s)",
            self.__class__.__name__,
            self,
            instance,
            owner,
        )

        if instance is None:
            return lambda *args, **kwargs: self.function(owner, *args, **kwargs)
        else:
            return lambda *args, **kwargs: self.function(instance, *args, **kwargs)
