"""Exercise 03: functions.

Read lessons/03_functions.py first, then implement every function below.
Run the tests with:  python runner.py test 03
"""

from collections.abc import Callable


def build_url(host: str, *, secure: bool = False, port: int | None = None, **params: object) -> str:
    """Build a URL from a host, optional port and query parameters.

    - scheme is "https" if ``secure`` else "http"
    - the port is appended as ``:port`` only when given AND different from the scheme's
      default (80 for http, 443 for https)
    - ``params`` become the query string, in the order given: ``?a=1&b=2``
    - no params -> no "?"

    Examples:
        build_url("example.com")                            -> "http://example.com"
        build_url("example.com", secure=True, q="py")       -> "https://example.com?q=py"
        build_url("localhost", port=8080, a=1, b=2)         -> "http://localhost:8080?a=1&b=2"
        build_url("example.com", secure=True, port=443)     -> "https://example.com"
    """
    raise NotImplementedError


def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Return a function that yields ``start``, ``start + step``, ... on successive calls.

    Each counter keeps its own independent state (closure + ``nonlocal``).

    Example:
        c = make_counter(10, 5)
        c(), c(), c()  -> 10, 15, 20
    """
    raise NotImplementedError


def add_item(item: object, items: list[object] | None = None) -> list[object]:
    """Append ``item`` to ``items`` and return the list.

    If ``items`` is None a brand-new list must be created on every call
    (beware of the mutable-default trap). A list passed in IS modified and returned.

    Examples:
        add_item(1) -> [1];  add_item(2) -> [2]     (not [1, 2]!)
        existing = [1]; add_item(2, existing) -> [1, 2]  (and ``existing`` is now [1, 2])
    """
    raise NotImplementedError


def min_max(values: list[int]) -> tuple[int, int]:
    """Return ``(smallest, largest)``. Raise ``ValueError`` for an empty list.

    Example:
        min_max([4, 8, 1]) -> (1, 8)
    """
    raise NotImplementedError


def compose(*functions: Callable[[object], object]) -> Callable[[object], object]:
    """Compose functions left to right: ``compose(f, g)(x) == g(f(x))``.

    ``compose()`` with no functions returns the identity function.

    Example:
        compose(str.strip, str.upper)("  hi ") -> "HI"
    """
    raise NotImplementedError
