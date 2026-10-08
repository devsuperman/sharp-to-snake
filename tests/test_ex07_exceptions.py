import pytest

from exercises.ex07_exceptions import (
    InvalidValueError,
    MissingFieldError,
    ValidationError,
    first_valid_int,
    parse_age,
    run_with_cleanup,
    validate_user,
)


def test_exception_hierarchy():
    assert issubclass(ValidationError, Exception)
    assert issubclass(MissingFieldError, ValidationError)
    assert issubclass(InvalidValueError, ValidationError)
    assert not issubclass(MissingFieldError, InvalidValueError)


def test_exceptions_carry_field_information():
    missing = MissingFieldError("name")
    assert missing.field == "name"
    assert "name" in str(missing)
    invalid = InvalidValueError("age", "must be 0-150")
    assert invalid.field == "age"
    assert "age" in str(invalid)
    assert InvalidValueError("age").field == "age"


@pytest.mark.parametrize(("text", "expected"), [("42", 42), (" 7 ", 7), ("0", 0), ("150", 150)])
def test_parse_age_valid(text, expected):
    assert parse_age(text) == expected


@pytest.mark.parametrize("text", ["-1", "151", "200"])
def test_parse_age_out_of_range(text):
    with pytest.raises(InvalidValueError):
        parse_age(text)


def test_parse_age_chains_the_original_error():
    with pytest.raises(InvalidValueError) as info:
        parse_age("abc")
    assert isinstance(info.value.__cause__, ValueError)


def test_validate_user_cleans_and_drops_extras():
    result = validate_user({"name": " Ana ", "age": "31", "x": 1})
    assert result == {"name": "Ana", "age": 31}
    assert validate_user({"name": "Bo", "age": 5}) == {"name": "Bo", "age": 5}


@pytest.mark.parametrize(
    ("data", "field"),
    [({"age": 3}, "name"), ({"name": "Ana"}, "age"), ({}, "name")],
)
def test_validate_user_missing_fields(data, field):
    with pytest.raises(MissingFieldError) as info:
        validate_user(data)
    assert info.value.field == field


@pytest.mark.parametrize(
    "data",
    [
        {"name": "  ", "age": 3},
        {"name": 123, "age": 3},
        {"name": "Ana", "age": "old"},
        {"name": "Ana", "age": 200},
        {"name": "Ana", "age": True},
        {"name": "Ana", "age": None},
    ],
)
def test_validate_user_invalid_values(data):
    with pytest.raises(InvalidValueError):
        validate_user(data)


def test_validate_errors_are_catchable_as_validation_error():
    with pytest.raises(ValidationError):
        validate_user({})


def test_first_valid_int():
    assert first_valid_int(["x", "7", "9"]) == 7
    with pytest.raises(InvalidValueError):
        first_valid_int(["x", "y"])
    with pytest.raises(InvalidValueError):
        first_valid_int([])


def test_run_with_cleanup_success():
    calls = []
    result = run_with_cleanup(lambda: calls.append("action") or 42, lambda: calls.append("cleanup"))
    assert result == 42
    assert calls == ["action", "cleanup"]


def test_run_with_cleanup_still_cleans_up_on_error():
    calls = []

    def failing():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        run_with_cleanup(failing, lambda: calls.append("cleanup"))
    assert calls == ["cleanup"]
