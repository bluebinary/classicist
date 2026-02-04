# Classicist Library Change Log

## [1.0.4] - 2026-02-03
### Added
- Added support for the new `@runtimer` decorator which can be used to gather run times
for functions, class methods and instance methods.

### Updated
- Improved top-level import availability for the `AliasError` and `AnnotationError` classes.

## [1.0.3] - 2026-01-30
### Updated
- Improved logging for aliasing functionality.

## [1.0.2] - 2026-01-29
### Added
- Added support for aliasing classes and module-level functions, in addition to the
earlier support provided by the library for aliasing methods defined within classes.

## [1.0.1] - 2026-01-12
### Added
- Added support for creating method aliases on classes via the new `@alias()` decorator
 and its associated `aliased` metaclass.

- Added support for creating arbitrary annotations on mutable code objects via the new
 `@annotation()` decorator, including on classes, methods, functions and most objects.

- Added support for marking code objects such as methods and functions as deprecated via
 the new `@deprecated` decorator and for checking deprecated status via `is_deprecated`.

- Added support for protecting classes and subclasses from attribute-shadowing, via the
 new `shadowproof` metaclass. The issue is usually caused by a subclass unintentionally
 redefining or overwriting an attribute value that has been inherited from a superclass
 and can otherwise be quite difficult to debug, as it may lead to unexpected behaviour
 in either the superclass or subclass without an immediately obvious cause. Python does
 not issue any warnings or raise any errors when most attributes are overwritten, aside
 from special cases mostly in the standard library on immutable objects. The `shadowproof`
 metaclass helps solve this issue by raising an `AttributeShadowingError` when this happens.

 - Added support for marking functions and class methods as not being suitable for caching
 via the `@nocache` decorator; the decorator acts as clear code-documentation rather than
 a mechanism to prevent caching from taking place.

## [1.0.0] - 2025-06-24
### Added
- First release of the Classicist class decorator library.
