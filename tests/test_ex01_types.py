from exercises.ex01_types import describe_type, format_greeting, normalize_tags, safe_to_int


def test_format_greeting_plural():
    assert format_greeting("ana", 30) == "Hello, Ana! You are 30 years old."


def test_format_greeting_singular_and_whitespace():
    assert format_greeting("  bob ", 1) == "Hello, Bob! You are 1 year old."


def test_format_greeting_zero_is_plural():
    assert format_greeting("Eve", 0) == "Hello, Eve! You are 0 years old."


def test_safe_to_int_valid_values():
    assert safe_to_int("42") == 42
    assert safe_to_int(" 7 ") == 7
    assert safe_to_int("-3") == -3


def test_safe_to_int_invalid_values():
    assert safe_to_int("3.5") is None
    assert safe_to_int("abc") is None
    assert safe_to_int("") is None
    assert safe_to_int(None) is None


def test_describe_type_bool_is_not_int():
    assert describe_type(True) == "bool"
    assert describe_type(False) == "bool"
    assert describe_type(1) == "int"


def test_describe_type_other_kinds():
    assert describe_type(1.5) == "float"
    assert describe_type("x") == "str"
    assert describe_type(None) == "none"
    assert describe_type([1]) == "other"


def test_normalize_tags_does_not_mutate_input():
    original = [" Python ", "", "C#"]
    result = normalize_tags(original)
    assert result == ["python", "c#"]
    assert original == [" Python ", "", "C#"]
    assert result is not original
