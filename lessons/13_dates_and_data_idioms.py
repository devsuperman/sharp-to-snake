"""
Lesson 13: Dates, time zones and everyday data idioms

Goal: handle timestamps correctly (aware vs naive) and reshape records with the standard
library: chunking, de-duplicating, grouping and summing.
"""

# 1. CONCEPT
# A `datetime` is either:
#   naive  no tzinfo: "08:00" on some unknown clock. Arithmetic works, meaning is ambiguous.
#   aware  has tzinfo: an exact instant. Comparable across zones.
# Rules of thumb for automation: parse everything into aware UTC datetimes at the edge, do all
# the logic in UTC, and convert to a local zone only to display or to group by local day.
# Never compare naive with aware (Python raises TypeError, which is a feature).
#
# Everyday data idioms (all stdlib, no pandas):
#   itertools.islice / batched   take a slice of any iterable, lazily
#   collections.defaultdict      dict that creates missing values for you
#   collections.Counter          counting (and summing) by key
#   dict preserves insertion order; assigning an existing key keeps its ORIGINAL position
#   sorted(items, key=..., reverse=...)   multi-criteria sorting with tuples as keys

import itertools
from collections import Counter, defaultdict
from datetime import UTC, datetime, timezone
from zoneinfo import ZoneInfo  # IANA database: "America/Sao_Paulo"

# 2. EXAMPLES


def demo_naive_vs_aware() -> None:
    naive = datetime(2024, 5, 1, 8, 0)
    aware = datetime(2024, 5, 1, 8, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))
    print(naive.tzinfo, "|", aware.tzinfo)
    print("as UTC:", aware.astimezone(UTC).isoformat())  # 11:00 UTC
    try:
        naive < aware  # noqa: B015
    except TypeError as err:
        print("comparison refused ->", err)


def demo_parsing() -> None:
    print(datetime.fromisoformat("2024-05-01T08:00:00Z"))  # "Z" is understood since 3.11
    print(datetime.fromisoformat("2024-05-01T08:00:00-03:00").astimezone(UTC))
    parsed = datetime.strptime("01/05/2024 08:00:00", "%d/%m/%Y %H:%M:%S")  # naive!
    print(parsed, "->", parsed.replace(tzinfo=ZoneInfo("America/Sao_Paulo")).astimezone(UTC))
    print(datetime(2024, 5, 1, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))


def demo_local_day() -> None:
    instant = datetime(2024, 5, 2, 1, 30, tzinfo=UTC)  # 22:30 the day BEFORE in Sao Paulo
    print(
        "UTC date:",
        instant.date(),
        "| local date:",
        instant.astimezone(ZoneInfo("America/Sao_Paulo")).date(),
    )


def demo_batching() -> None:
    def chunks(items, size):
        iterator = iter(items)
        while batch := list(itertools.islice(iterator, size)):  # walrus: assign and test
            yield batch

    print(list(chunks(range(7), 3)))  # [[0, 1, 2], [3, 4, 5], [6]]
    print(list(itertools.batched(range(7), 3)))  # 3.12+: same, but yields tuples


def demo_grouping_and_counting() -> None:
    rows = [("A1", 10.0), ("B2", 5.0), ("A1", 2.5)]
    groups: defaultdict[str, list[float]] = defaultdict(list)
    for plate, km in rows:
        groups[plate].append(km)
    print(dict(groups))

    totals: Counter[str] = Counter()
    for plate, km in rows:
        totals[plate] += km
    print(totals.most_common())  # sorted by value, descending

    latest: dict[str, int] = {}
    for key, value in [("x", 1), ("y", 2), ("x", 3)]:
        latest[key] = value  # "last wins", but "x" keeps its first position
    print(latest)


def demo() -> None:
    demo_naive_vs_aware()
    demo_parsing()
    demo_local_day()
    demo_batching()
    demo_grouping_and_counting()


# 3. C# EQUIVALENT
#
#   Python                                     C#
#   -----------------------------------------  ---------------------------------------------
#   naive datetime / aware datetime            DateTime (Kind: Unspecified) / DateTimeOffset
#   datetime.now(UTC)                          DateTimeOffset.UtcNow
#   datetime.fromisoformat(s)                  DateTimeOffset.Parse / ParseExact
#   strptime(s, "%d/%m/%Y")                    DateTime.ParseExact(s, "dd/MM/yyyy", ...)
#   ZoneInfo("America/Sao_Paulo")              TimeZoneInfo.FindSystemTimeZoneById
#   dt.astimezone(zone)                        TimeZoneInfo.ConvertTime(dto, zone)
#   islice / batched                           Enumerable.Chunk(size)  (.NET 6+)
#   defaultdict(list)                          GroupBy / ToLookup  (LINQ)
#   Counter                                    GroupBy(...).ToDictionary(g => g.Key, g => g.Sum())
#   dict "last wins" assignment                dictionary[key] = value (indexer upsert)

# 4. COMMON PITFALLS
#
#   a) `datetime.now()` and `datetime.utcnow()` return NAIVE values (utcnow is deprecated).
#      Use `datetime.now(UTC)`.
#   b) `.replace(tzinfo=...)` only LABELS the clock; `.astimezone(...)` CONVERTS. Mixing them
#      up silently shifts every timestamp by hours.
#   c) Grouping "by day" in UTC splits a local business day in two. Convert first.
#   d) Fixed offsets (UTC-3) break on daylight saving; use named zones from `zoneinfo`.
#   e) On Windows the IANA database is missing: `pip install tzdata` (in requirements-dev).
#   f) A `defaultdict` creates keys on READ, so `d["typo"]` quietly adds an entry.

# 5. EXERCISE
# Open exercises/ex13_dates_and_data.py, implement the functions, then run:
#     python runner.py test 13

if __name__ == "__main__":
    demo()
