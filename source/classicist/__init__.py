import logging


logger = logging.getLogger(__name__)


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


class classproperty(property):
    """The classproperty decorator transforms a method into a class-level property. This
    provides access to the method as if it were a class attribute; this addresses the
    removal of support for combining the @classmethod and @property decorators to create
    class properties in Python 3.13, a change which was made due to some complexity in
    the underlying interpreter implementation."""

    def __init__(self, fget: callable, fset: callable = None, fdel: callable = None):
        super().__init__(fget, fset, fdel)

    def __get__(self, instance: object, klass: type = None):
        if klass is None:
            return self
        return self.fget(klass)

    def __set__(self, instance: object, value: object):
        # Note that the __set__ descriptor cannot be used on class methods unless
        # the class is created with a metaclass that implements this behaviour
        raise NotImplemented

    def __delete__(self, instance: object):
        # Note that the __delete__ descriptor cannot be used on class methods unless
        # the class is created with a metaclass that implements this behaviour
        raise NotImplemented

    def __getattr__(self, name: str):
        if name in ATTRIBUTES:
            return getattr(self.fget, name)
        else:
            raise AttributeError(
                "The classproperty method '%s' does not have an '%s' attribute!"
                % (
                    self.fget.__name__,
                    name,
                )
            )

    # # For inspectability, provide access to the underlying function's metadata
    # # including __module__, __name__, __qualname__, __doc__, and __annotations__
    # @property
    # def __module__(self):
    #     return self.fget.__module__
    #
    # @property
    # def __name__(self):
    #     return self.fget.__name__
    #
    # @property
    # def __qualname__(self):
    #     return self.fget.__qualname__
    #
    # @property
    # def __doc__(self):
    #     return self.fget.__doc__
    #
    # @property
    # def __annotations__(self):
    #     return self.fget.__annotations__
