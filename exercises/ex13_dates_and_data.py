"""Exercise 13: dates, time zones and data idioms.

Read lessons/13_dates_and_data_idioms.py first. Standard library only.
Run the tests with:  python runner.py test 13
"""

from collections.abc import Hashable, Iterable, Iterator
from datetime import UTC, date, datetime, tzinfo


def parse_timestamp(text: str, assume_tz: tzinfo = UTC) -> datetime:
    """Parse a timestamp string into an AWARE datetime expressed in UTC.

    Accepted formats (after stripping whitespace):
      - ISO 8601 with offset or "Z":   "2024-05-01T08:00:00-03:00", "2024-05-01T11:00:00Z"
      - ISO 8601 without offset:       "2024-05-01T08:00:00"
      - Legacy "dd/mm/YYYY HH:MM:SS":  "01/05/2024 08:00:00"
    A string without an offset is naive: interpret it in ``assume_tz``.

    The result is always converted to UTC. Anything else raises ``ValueError``.

    Example:
        parse_timestamp("01/05/2024 08:00:00", ZoneInfo("America/Sao_Paulo"))
            -> datetime(2024, 5, 1, 11, 0, tzinfo=UTC)
    """
    raise NotImplementedError


def to_zone(moment: datetime, zone_name: str) -> datetime:
    """Convert an aware datetime to the named IANA zone (e.g. "America/Sao_Paulo").

    A naive ``moment`` raises ``ValueError`` (we refuse to guess).
    """
    raise NotImplementedError


def group_by_local_day(
    records: Iterable[dict[str, str]], field: str, zone_name: str
) -> dict[date, list[dict[str, str]]]:
    """Group records by the LOCAL calendar day of their timestamp field.

    ``record[field]`` is any string ``parse_timestamp`` accepts (naive ones are taken as UTC).
    Days are computed in ``zone_name``. The returned dict is ordered by day ascending, and the
    records inside a day keep their input order.

    Example (zone America/Sao_Paulo, UTC-3):
        "2024-05-02T01:30:00Z" belongs to day 2024-05-01.
    """
    raise NotImplementedError


def chunked[T](items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Lazily yield successive lists of at most ``size`` items.

    Works with any iterable, including generators (do not call ``len`` or index it).
    ``size < 1`` raises ``ValueError`` (when iteration starts is fine).

    Example:
        list(chunked(range(5), 2)) -> [[0, 1], [2, 3], [4]]
    """
    raise NotImplementedError


def dedupe_last(records: Iterable[dict[str, str]], key: str) -> list[dict[str, str]]:
    """Keep one record per ``record[key]``: the LAST one seen, placed at the position where
    that key FIRST appeared.

    Example:
        [{"id": "a", "v": "1"}, {"id": "b", "v": "2"}, {"id": "a", "v": "3"}]
          -> [{"id": "a", "v": "3"}, {"id": "b", "v": "2"}]
    """
    raise NotImplementedError


def total_by(
    records: Iterable[dict[str, str]], key_field: str, value_field: str
) -> dict[Hashable, float]:
    """Sum ``float(record[value_field])`` per ``record[key_field]``.

    The result is ordered by total descending, ties broken by key ascending. Values come from
    CSV so they are strings; a non-numeric value raises ``ValueError``.

    Example:
        [{"p": "B", "km": "5"}, {"p": "A", "km": "2.5"}, {"p": "A", "km": "2.5"}]
          -> {"A": 5.0, "B": 5.0}
    """
    raise NotImplementedError
