import subprocess
import sys
from pathlib import Path

import pytest

from exercises.ex11_type_hints import (
    SupportsArea,
    UserRecord,
    count_by_length,
    first_or_none,
    parse_user,
    total_area,
)

ROOT = Path(__file__).resolve().parent.parent
EXERCISE_FILE = ROOT / "exercises" / "ex11_type_hints.py"


class Square:  # satisfies SupportsArea structurally: no inheritance
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


def test_user_record_is_a_typed_dict_with_optional_email():
    assert UserRecord.__required_keys__ == frozenset({"name", "age"})
    assert UserRecord.__optional_keys__ == frozenset({"email"})
    assert UserRecord.__annotations__["age"] is int


def test_supports_area_is_a_protocol():
    assert getattr(SupportsArea, "_is_protocol", False) is True
    assert "area" in dir(SupportsArea)


def test_total_area_accepts_any_iterable_of_shapes():
    assert total_area([Square(2), Square(3)]) == 13.0
    assert total_area(Square(s) for s in (1, 2)) == 5.0
    assert total_area([]) == 0.0


@pytest.mark.parametrize(
    ("items", "expected"),
    [([1, 2], 1), (["a"], "a"), ((), None), ([], None), ("xyz", "x")],
)
def test_first_or_none(items, expected):
    assert first_or_none(items) == expected


def test_first_or_none_uses_pep695_type_parameters():
    assert len(first_or_none.__type_params__) == 1


def test_count_by_length():
    assert count_by_length(["a", "bb", "cc", "d"]) == {1: 2, 2: 2}
    assert count_by_length(w for w in ["abc"]) == {3: 1}
    assert count_by_length([]) == {}


def test_parse_user_valid():
    assert parse_user({"name": "Ana", "age": 31}) == {"name": "Ana", "age": 31}
    full = {"name": "Ana", "age": 31, "email": "a@x.io", "extra": 1}
    assert parse_user(full) == {"name": "Ana", "age": 31, "email": "a@x.io"}


@pytest.mark.parametrize(
    "raw",
    [
        {},
        {"name": "Ana"},
        {"age": 3},
        {"name": 1, "age": 3},
        {"name": "A", "age": "3"},
        {"name": "A", "age": True},
    ],
)
def test_parse_user_invalid_returns_none(raw):
    assert parse_user(raw) is None


def test_parse_user_ignores_non_string_email():
    assert parse_user({"name": "Ana", "age": 31, "email": 5}) == {"name": "Ana", "age": 31}


def test_mypy_strict_passes_on_the_exercise_file():
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(EXERCISE_FILE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, (
        f"mypy --strict reported problems:\n{result.stdout}{result.stderr}"
    )
