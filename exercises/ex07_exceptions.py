"""Exercise 07: exceptions.

Read lessons/07_exceptions.py first. The three exception classes are placeholders:
make them real exceptions with the hierarchy described below.
Run the tests with:  python runner.py test 07
"""

from collections.abc import Callable


class ValidationError:
    """Base class of all validation errors. Must derive from ``Exception``."""


class MissingFieldError:
    """A required field is absent. Must derive from ``ValidationError``.

    ``MissingFieldError("name")`` stores ``.field == "name"``; ``str(exc)`` mentions the field.
    """


class InvalidValueError:
    """A field is present but its value is bad. Must derive from ``ValidationError``.

    ``InvalidValueError("age", "must be 0-150")`` stores ``.field == "age"``; the reason is
    optional (default "invalid value"); ``str(exc)`` mentions the field.
    """


def parse_age(text: str) -> int:
    """Parse an age from text. Accepts 0..150 inclusive (after stripping whitespace).

    - non-numeric text -> ``InvalidValueError("age", ...)`` raised *from* the original
      ``ValueError`` (so ``exc.__cause__`` is that ``ValueError``)
    - numeric but outside 0..150 -> ``InvalidValueError("age", ...)``

    Examples:
        parse_age(" 42 ") -> 42
        parse_age("abc")  -> InvalidValueError
        parse_age("200")  -> InvalidValueError
    """
    raise NotImplementedError


def validate_user(data: dict[str, object]) -> dict[str, object]:
    """Validate and clean a user record.

    - ``name``: required; must be a non-blank ``str`` -> returned stripped
    - ``age``: required; an ``int`` (not ``bool``) or a ``str`` parsed with ``parse_age``;
      must be in 0..150
    - missing key -> ``MissingFieldError(<field>)``; present but bad -> ``InvalidValueError``
    - extra keys are dropped; the result is exactly ``{"name": ..., "age": ...}``

    Example:
        validate_user({"name": " Ana ", "age": "31", "x": 1}) -> {"name": "Ana", "age": 31}
    """
    raise NotImplementedError


def first_valid_int(values: list[str]) -> int:
    """Return the first value that parses as an int (EAFP: just try ``int(...)``).

    If none does, raise ``InvalidValueError("values", "no valid integer")``.

    Examples:
        first_valid_int(["x", "7", "9"]) -> 7
    """
    raise NotImplementedError


def run_with_cleanup(action: Callable[[], object], cleanup: Callable[[], None]) -> object:
    """Call ``action()`` and return its result; ``cleanup()`` ALWAYS runs afterwards.

    Exceptions raised by ``action`` must still propagate (after the cleanup ran).
    Use ``try`` / ``finally``.
    """
    raise NotImplementedError
