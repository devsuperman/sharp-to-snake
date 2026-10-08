import pytest

from exercises.ex03_functions import add_item, build_url, compose, make_counter, min_max


@pytest.mark.parametrize(
    ("args", "kwargs", "expected"),
    [
        (("example.com",), {}, "http://example.com"),
        (("example.com",), {"secure": True, "q": "py"}, "https://example.com?q=py"),
        (("localhost",), {"port": 8080, "a": 1, "b": 2}, "http://localhost:8080?a=1&b=2"),
        (("example.com",), {"secure": True, "port": 443}, "https://example.com"),
        (("example.com",), {"port": 80}, "http://example.com"),
        (("example.com",), {"secure": True, "port": 80}, "https://example.com:80"),
    ],
)
def test_build_url(args, kwargs, expected):
    assert build_url(*args, **kwargs) == expected


def test_make_counter_defaults():
    counter = make_counter()
    assert [counter(), counter(), counter()] == [0, 1, 2]


def test_make_counter_custom_start_and_step():
    counter = make_counter(10, 5)
    assert [counter(), counter(), counter()] == [10, 15, 20]


def test_make_counter_instances_are_independent():
    first, second = make_counter(), make_counter()
    first()
    first()
    assert second() == 0


def test_add_item_does_not_share_default_list():
    assert add_item(1) == [1]
    assert add_item(2) == [2]


def test_add_item_uses_the_list_passed_in():
    existing = [1]
    result = add_item(2, existing)
    assert result == [1, 2]
    assert result is existing


@pytest.mark.parametrize(
    ("values", "expected"),
    [([4, 8, 1], (1, 8)), ([5], (5, 5)), ([-3, -1, -2], (-3, -1))],
)
def test_min_max(values, expected):
    assert min_max(values) == expected


def test_min_max_empty_raises():
    with pytest.raises(ValueError):
        min_max([])


def test_compose_applies_left_to_right():
    pipeline = compose(str.strip, str.upper, lambda s: s + "!")
    assert pipeline("  hi ") == "HI!"


def test_compose_empty_is_identity():
    assert compose()(42) == 42
