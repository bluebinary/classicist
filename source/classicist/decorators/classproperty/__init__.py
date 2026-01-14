from classicist.logging import logger

logger = logger.getChild(__name__)


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
        # the class is created with a metaclass that implements this behaviour.
        raise NotImplementedError

    def __delete__(self, instance: object):
        # Note that the __delete__ descriptor cannot be used on class methods unless
        # the class is created with a metaclass that implements this behaviour.
        raise NotImplementedError

    def __getattr__(self, name: str):
        if hasattr(self.fget, name):
            return getattr(self.fget, name)
        else:
            raise AttributeError(
                "The classproperty method '%s' does not have an '%s' attribute!"
                % (
                    self.fget.__name__,
                    name,
                )
            )
