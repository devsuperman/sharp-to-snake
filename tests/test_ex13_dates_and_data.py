from datetime import UTC, date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from exercises.ex13_dates_and_data import (
    chunked,
    dedupe_last,
    group_by_local_day,
    parse_timestamp,
    to_zone,
    total_by,
)

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
NOON_UTC = datetime(2024, 5, 1, 11, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    "text",
    [
        "2024-05-01T11:00:00Z",
        "2024-05-01T08:00:00-03:00",
        "  2024-05-01T11:00:00+00:00  ",
    ],
)
def test_parse_timestamp_with_offset(text):
    assert parse_timestamp(text) == NOON_UTC


def test_parse_timestamp_result_is_utc():
    result = parse_timestamp("2024-05-01T08:00:00-03:00")
    assert result.utcoffset() == timedelta(0)


@pytest.mark.parametrize("text", ["2024-05-01T08:00:00", "01/05/2024 08:00:00"])
def test_parse_timestamp_naive_uses_assumed_zone(text):
    assert parse_timestamp(text, SAO_PAULO) == NOON_UTC
    assert parse_timestamp(text) == datetime(2024, 5, 1, 8, 0, tzinfo=UTC)  # default is UTC


def test_parse_timestamp_accepts_fixed_offset_tz():
    assert parse_timestamp("01/05/2024 08:00:00", timezone(timedelta(hours=-3))) == NOON_UTC


@pytest.mark.parametrize("text", ["", "yesterday", "2024-13-01T00:00:00", "32/01/2024 00:00:00"])
def test_parse_timestamp_invalid(text):
    with pytest.raises(ValueError):
        parse_timestamp(text)


def test_to_zone_converts_instant():
    local = to_zone(NOON_UTC, "America/Sao_Paulo")
    assert local == NOON_UTC
    assert (local.hour, local.utcoffset()) == (8, timedelta(hours=-3))


def test_to_zone_rejects_naive():
    with pytest.raises(ValueError):
        to_zone(datetime(2024, 5, 1, 8, 0), "America/Sao_Paulo")


def test_group_by_local_day_uses_local_calendar():
    records = [
        {"id": "1", "at": "2024-05-02T01:30:00Z"},  # 22:30 on May 1st locally
        {"id": "2", "at": "2024-05-01T15:00:00Z"},
        {"id": "3", "at": "2024-05-02T12:00:00Z"},
    ]
    grouped = group_by_local_day(records, "at", "America/Sao_Paulo")
    assert list(grouped) == [date(2024, 5, 1), date(2024, 5, 2)]  # ordered by day
    assert [r["id"] for r in grouped[date(2024, 5, 1)]] == ["1", "2"]  # input order kept
    assert [r["id"] for r in grouped[date(2024, 5, 2)]] == ["3"]


def test_group_by_local_day_naive_taken_as_utc_and_empty():
    grouped = group_by_local_day([{"at": "2024-05-02T01:30:00"}], "at", "America/Sao_Paulo")
    assert list(grouped) == [date(2024, 5, 1)]
    assert group_by_local_day([], "at", "UTC") == {}


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (1, [[0], [1], [2], [3], [4]]),
        (2, [[0, 1], [2, 3], [4]]),
        (5, [[0, 1, 2, 3, 4]]),
        (9, [[0, 1, 2, 3, 4]]),
    ],
)
def test_chunked(size, expected):
    assert list(chunked(range(5), size)) == expected


def test_chunked_empty_and_generators_and_laziness():
    assert list(chunked([], 3)) == []
    consumed = []

    def source():
        for i in range(100):
            consumed.append(i)
            yield i

    first = next(chunked(source(), 3))
    assert first == [0, 1, 2]
    assert len(consumed) <= 4  # did not read the whole source


def test_chunked_invalid_size():
    with pytest.raises(ValueError):
        list(chunked([1, 2], 0))


def test_dedupe_last_last_wins_first_position():
    records = [
        {"id": "a", "v": "1"},
        {"id": "b", "v": "2"},
        {"id": "a", "v": "3"},
    ]
    assert dedupe_last(records, "id") == [{"id": "a", "v": "3"}, {"id": "b", "v": "2"}]


def test_dedupe_last_no_duplicates_and_empty():
    records = [{"id": "x"}, {"id": "y"}]
    assert dedupe_last(records, "id") == records
    assert dedupe_last([], "id") == []


def test_total_by_orders_by_total_then_key():
    records = [
        {"p": "B", "km": "5"},
        {"p": "A", "km": "2.5"},
        {"p": "A", "km": "2.5"},
        {"p": "C", "km": "10"},
    ]
    result = total_by(records, "p", "km")
    assert list(result.items()) == [("C", 10.0), ("A", 5.0), ("B", 5.0)]


def test_total_by_bad_value_and_empty():
    with pytest.raises(ValueError):
        total_by([{"p": "A", "km": "abc"}], "p", "km")
    assert total_by([], "p", "km") == {}
