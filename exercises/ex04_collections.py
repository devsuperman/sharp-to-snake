"""Exercise 04: collections.

Read lessons/04_collections.py first, then implement every function below.
Run the tests with:  python runner.py test 04
"""

from collections.abc import Hashable


def group_by_key(
    records: list[dict[str, object]], key: str
) -> dict[Hashable, list[dict[str, object]]]:
    """Group dictionaries by the value stored under ``key``.

    Records without ``key`` are skipped. Group order and the order inside each group follow
    the order of first appearance in ``records``.

    Example:
        group_by_key([{"t": "a", "n": 1}, {"t": "b", "n": 2}, {"t": "a", "n": 3}], "t")
        -> {"a": [{"t": "a", "n": 1}, {"t": "a", "n": 3}], "b": [{"t": "b", "n": 2}]}
    """
    raise NotImplementedError


def unique_preserve_order(items: list[Hashable]) -> list[Hashable]:
    """Remove duplicates while keeping the FIRST occurrence of each item.

    Example:
        unique_preserve_order([3, 1, 3, 2, 1]) -> [3, 1, 2]
    """
    raise NotImplementedError


def word_frequencies(text: str) -> dict[str, int]:
    """Count words, case-insensitively, ignoring the punctuation ``.,!?;:``.

    The returned dict is ordered by count descending, ties broken alphabetically.

    Example:
        word_frequencies("The cat. The dog! A cat?")
        -> {"cat": 2, "the": 2, "a": 1, "dog": 1}
    """
    raise NotImplementedError


def common_and_exclusive(a: list[int], b: list[int]) -> tuple[list[int], list[int], list[int]]:
    """Return ``(in_both, only_in_a, only_in_b)``, each as a sorted list without duplicates.

    Example:
        common_and_exclusive([1, 2, 3, 3], [3, 4]) -> ([3], [1, 2], [4])
    """
    raise NotImplementedError


def rotate(items: list[int], steps: int) -> list[int]:
    """Return a NEW list rotated ``steps`` positions to the right (negative = left).

    Use slicing. Rotating by more than the length wraps around; an empty list stays empty.

    Examples:
        rotate([1, 2, 3, 4, 5], 2)  -> [4, 5, 1, 2, 3]
        rotate([1, 2, 3], -1)       -> [2, 3, 1]
    """
    raise NotImplementedError
