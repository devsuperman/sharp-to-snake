"""Exercise 01: types and variables.

Read lessons/01_types_and_variables.py first, then implement every function below.
Run the tests with:  python runner.py test 01
"""


def format_greeting(name: str, age: int) -> str:
    """Build a greeting with an f-string.

    The name is stripped of surrounding whitespace and capitalized (use ``str.capitalize``).
    "year" is singular only when ``age == 1``.

    Examples:
        format_greeting("ana", 30)    -> "Hello, Ana! You are 30 years old."
        format_greeting("  bob ", 1)  -> "Hello, Bob! You are 1 year old."
    """
    raise NotImplementedError


def safe_to_int(value: object) -> int | None:
    """Convert ``value`` to an int, returning None instead of raising.

    Strings are parsed after stripping whitespace. Anything that cannot be converted,
    including ``None`` and non-numeric text such as "3.5" or "abc", gives None.

    Examples:
        safe_to_int("42")    -> 42
        safe_to_int(" 7 ")   -> 7
        safe_to_int("3.5")   -> None
        safe_to_int(None)    -> None
    """
    raise NotImplementedError


def describe_type(value: object) -> str:
    """Name the kind of ``value``: "bool", "int", "float", "str", "none" or "other".

    Careful: ``bool`` is a subclass of ``int``.

    Examples:
        describe_type(True)   -> "bool"
        describe_type(1)      -> "int"
        describe_type(None)   -> "none"
        describe_type([1])    -> "other"
    """
    raise NotImplementedError


def normalize_tags(tags: list[str]) -> list[str]:
    """Return a NEW list with each tag stripped and lower-cased, dropping empty ones.

    The input list must not be modified (mutability!).

    Example:
        normalize_tags([" Python ", "", "C#"])  -> ["python", "c#"]
    """
    raise NotImplementedError
