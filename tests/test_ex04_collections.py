import pytest

from exercises.ex04_collections import (
    common_and_exclusive,
    group_by_key,
    rotate,
    unique_preserve_order,
    word_frequencies,
)


def test_group_by_key_groups_in_order_of_appearance():
    records = [{"t": "a", "n": 1}, {"t": "b", "n": 2}, {"t": "a", "n": 3}]
    result = group_by_key(records, "t")
    assert result == {"a": [records[0], records[2]], "b": [records[1]]}
    assert list(result) == ["a", "b"]


def test_group_by_key_skips_records_without_the_key():
    assert group_by_key([{"x": 1}, {"t": 1}], "t") == {1: [{"t": 1}]}


def test_group_by_key_empty():
    assert group_by_key([], "t") == {}


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        ([], []),
        (["b", "a", "b"], ["b", "a"]),
        ([1, 1, 1], [1]),
    ],
)
def test_unique_preserve_order(items, expected):
    assert unique_preserve_order(items) == expected


def test_word_frequencies_counts_and_orders():
    result = word_frequencies("The cat. The dog! A cat?")
    assert result == {"cat": 2, "the": 2, "a": 1, "dog": 1}
    assert list(result.items()) == [("cat", 2), ("the", 2), ("a", 1), ("dog", 1)]


def test_word_frequencies_empty():
    assert word_frequencies("") == {}
    assert word_frequencies("  ...  ") == {}


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 2, 3, 3], [3, 4], ([3], [1, 2], [4])),
        ([], [1], ([], [], [1])),
        ([5, 5], [5], ([5], [], [])),
    ],
)
def test_common_and_exclusive(a, b, expected):
    assert common_and_exclusive(a, b) == expected


@pytest.mark.parametrize(
    ("items", "steps", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3], -1, [2, 3, 1]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 4, [3, 1, 2]),
        ([], 3, []),
    ],
)
def test_rotate(items, steps, expected):
    assert rotate(items, steps) == expected


def test_rotate_returns_new_list():
    original = [1, 2, 3]
    assert rotate(original, 1) is not original
    assert original == [1, 2, 3]
