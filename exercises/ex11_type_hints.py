"""Exercise 11: type hints.

Read lessons/11_type_hints.py first. Implement AND fully annotate everything below.
One test runs ``mypy --strict`` on this file: unannotated or wrongly annotated code fails.
Run the tests with:  python runner.py test 11
"""


class UserRecord:
    """Make this a ``TypedDict`` with ``name: str``, ``age: int`` and an optional ``email: str``
    (use ``NotRequired``)."""


class SupportsArea:
    """Make this a ``Protocol`` with a single method ``area(self) -> float``."""


def total_area(shapes):
    """Sum ``shape.area()`` for any iterable of objects that satisfy ``SupportsArea``.

    Example:
        total_area([Square(2), Square(3)]) -> 13.0
    """
    raise NotImplementedError


def first_or_none(items):
    """Return the first item of a sequence, or None if it is empty.

    Must be a generic function written with the Python 3.12 syntax ``def first_or_none[T](...)``
    so that ``first_or_none([1, 2])`` is typed ``int | None`` and ``first_or_none(["a"])`` is
    typed ``str | None``.
    """
    raise NotImplementedError


def count_by_length(words):
    """Map each word length to how many words have that length.

    Accepts any iterable of ``str``; returns ``dict[int, int]``.

    Example:
        count_by_length(["a", "bb", "cc", "d"]) -> {1: 2, 2: 2}
    """
    raise NotImplementedError


def parse_user(raw):
    """Turn an untyped mapping (``Mapping[str, object]``) into a ``UserRecord``, or None.

    - ``name`` must be a ``str`` and ``age`` an ``int`` (not a ``bool``), otherwise return None
    - ``email`` is copied only when present and a ``str``
    - extra keys are ignored

    Example:
        parse_user({"name": "Ana", "age": 31, "email": "a@x.io", "x": 1})
        -> {"name": "Ana", "age": 31, "email": "a@x.io"}
    """
    raise NotImplementedError
