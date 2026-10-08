import inspect
import itertools

import pytest

from exercises.ex05_comprehensions import (
    batched,
    invert_dict,
    pair_with_index,
    running_total,
    squares_of_evens,
)


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([1, 2, 3, 4], [4, 16]), ([], []), ([1, 3], []), ([-2, 0], [4, 0])],
)
def test_squares_of_evens(numbers, expected):
    assert squares_of_evens(numbers) == expected


def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert_dict({}) == {}


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (2, [[0, 1], [2, 3], [4]]),
        (5, [[0, 1, 2, 3, 4]]),
        (10, [[0, 1, 2, 3, 4]]),
        (1, [[0], [1], [2], [3], [4]]),
    ],
)
def test_batched_sizes(size, expected):
    assert list(batched(range(5), size)) == expected


def test_batched_empty_input():
    assert list(batched([], 3)) == []


def test_batched_is_lazy_generator():
    result = batched(itertools.count(), 3)
    assert inspect.isgenerator(result)
    assert next(result) == [0, 1, 2]
    assert next(result) == [3, 4, 5]


def test_batched_rejects_bad_size():
    with pytest.raises(ValueError):
        list(batched([1, 2, 3], 0))


def test_running_total_is_lazy_and_correct():
    result = running_total(iter([1, 2, 3, 4]))
    assert inspect.isgenerator(result)
    assert list(result) == [1, 3, 6, 10]
    assert list(running_total([])) == []


def test_running_total_on_infinite_input():
    assert list(itertools.islice(running_total(itertools.repeat(2)), 4)) == [2, 4, 6, 8]


def test_pair_with_index():
    assert pair_with_index(["Ana", "Bob"]) == ["1. Ana", "2. Bob"]
    assert pair_with_index(["x"], start=0) == ["0. x"]
    assert pair_with_index([]) == []
