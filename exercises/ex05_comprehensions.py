"""Exercise 05: comprehensions and generators.

Read lessons/05_comprehensions.py first, then implement every function below.
Run the tests with:  python runner.py test 05
"""

from collections.abc import Hashable, Iterable, Iterator


def squares_of_evens(numbers: list[int]) -> list[int]:
    """Return the squares of the even numbers, using a list comprehension.

    Example:
        squares_of_evens([1, 2, 3, 4]) -> [4, 16]
    """
    raise NotImplementedError


def invert_dict(mapping: dict[Hashable, Hashable]) -> dict[Hashable, Hashable]:
    """Swap keys and values with a dict comprehension. Values are assumed unique.

    Example:
        invert_dict({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    """
    raise NotImplementedError


def batched(items: Iterable[int], size: int) -> Iterator[list[int]]:
    """Lazily yield lists of ``size`` items; the last one may be shorter.

    This MUST be a generator: it has to work on infinite iterables, and must not consume
    more input than needed. ``size < 1`` raises ``ValueError`` (when iteration starts).

    Examples:
        list(batched(range(5), 2)) -> [[0, 1], [2, 3], [4]]
        next(batched(itertools.count(), 3)) -> [0, 1, 2]
    """
    raise NotImplementedError


def running_total(numbers: Iterable[float]) -> Iterator[float]:
    """Lazily yield the cumulative sum of ``numbers`` (a generator).

    Example:
        list(running_total([1, 2, 3, 4])) -> [1, 3, 6, 10]
    """
    raise NotImplementedError


def pair_with_index(names: list[str], start: int = 1) -> list[str]:
    """Return ``"<index>. <name>"`` for each name, numbering from ``start``.

    Use ``enumerate``.

    Example:
        pair_with_index(["Ana", "Bob"]) -> ["1. Ana", "2. Bob"]
    """
    raise NotImplementedError
