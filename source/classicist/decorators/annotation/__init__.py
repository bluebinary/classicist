from __future__ import annotations

from classicist.logging import logger
from classicist.exceptions.decorators.annotation import AnnotationError

import builtins

logger = logger.getChild(__name__)


def annotate(thing: object, **annotations: dict[str, object]) -> callable:
    """Supports associating arbitrary annotations with the provided code object."""

    if isinstance(thing, object) and not thing in [None, True, False]:
        if hasattr(thing, "_classicist_annotations") and isinstance(
            thing._classicist_annotations, dict
        ):
            thing._classicist_annotations.update(annotations)
        else:
            try:
                thing._classicist_annotations = annotations
            except AttributeError as exception:
                raise AnnotationError(
                    "Cannot assign annotations to an object of type %s: %s!"
                    % (builtins.type(thing), str(exception))
                )

    return thing


def annotation(**annotations: dict[str, object]) -> callable:
    """Supports associating arbitrary annotations with a code object via a decorator."""

    def decorator(thing: object) -> object:
        return annotate(thing, **annotations)

    return decorator


def annotations(thing: object, metadata: bool = False) -> dict[str, object] | None:
    """Supports obtaining arbitrary annotations for a code object."""

    if isinstance(thing, object) and hasattr(thing, "_classicist_annotations"):
        if isinstance(annotations := thing._classicist_annotations, dict):
            if metadata is True:
                annotations["__name__"] = thing.__name__
                annotations["__type__"] = type(thing)
            return annotations


__all__ = [
    "annotate",
    "annotation",
    "annotations",
]
