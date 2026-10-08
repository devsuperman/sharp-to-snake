import csv
from datetime import UTC, datetime
from pathlib import Path

import pytest

from positions_sync.cleaning import (
    CleaningReport,
    clean_rows,
    parse_local_timestamp,
    read_rows,
)

DATA = Path(__file__).resolve().parent.parent / "data" / "raw_pings.csv"


def row(**overrides: str) -> dict[str, str]:
    base = {
        "device_id": "AB-12",
        "timestamp": "01/05/2024 08:00:00",
        "lat": "-23.55",
        "lon": "-46.63",
        "speed_kmh": "40",
    }
    return {**base, **overrides}


def test_parse_local_timestamp_converts_to_utc():
    assert parse_local_timestamp("01/05/2024 08:00:00") == datetime(2024, 5, 1, 11, 0, tzinfo=UTC)
    assert parse_local_timestamp("01/05/2024 08:00:00").utcoffset().total_seconds() == 0


def test_parse_local_timestamp_crosses_midnight():
    assert parse_local_timestamp("01/05/2024 22:30:00") == datetime(2024, 5, 2, 1, 30, tzinfo=UTC)


@pytest.mark.parametrize("text", ["", "2024-05-01 08:00", "31/02/2024 08:00:00", "01/05/2024"])
def test_parse_local_timestamp_invalid(text):
    with pytest.raises(ValueError):
        parse_local_timestamp(text)


def test_report_defaults_to_zero():
    assert CleaningReport() == CleaningReport(0, 0, 0, 0, 0, 0)


def test_clean_rows_happy_path():
    pings, report = clean_rows([row()])
    assert len(pings) == 1
    assert pings[0].device_id == "AB-12"
    assert pings[0].timestamp == datetime(2024, 5, 1, 11, 0, tzinfo=UTC)
    assert (pings[0].lat, pings[0].lon, pings[0].speed_kmh) == (-23.55, -46.63, 40.0)
    assert report == CleaningReport(total=1, kept=1)


def test_clean_rows_normalises_device_id():
    pings, _ = clean_rows([row(device_id="  ab-12 ")])
    assert pings[0].device_id == "AB-12"


def test_clean_rows_null_island_needs_both_zero():
    pings, report = clean_rows(
        [row(lat="0", lon="0.0"), row(lat="0", lon="-46.6", timestamp="02/05/2024 08:00:00")]
    )
    assert len(pings) == 1 and report.null_island == 1


@pytest.mark.parametrize(
    ("speed", "kept"), [("200", True), ("200.1", False), ("-5", True), ("0", True)]
)
def test_clean_rows_speed_limit(speed, kept):
    pings, report = clean_rows([row(speed_kmh=speed)])
    assert bool(pings) is kept
    assert report.too_fast == (0 if kept else 1)


@pytest.mark.parametrize(
    "bad",
    [
        row(lat="abc"),
        row(lon=""),
        row(speed_kmh=""),
        row(timestamp="2024-05-01 08:00"),
        {"device_id": "AB-12", "timestamp": "01/05/2024 08:00:00"},  # missing columns
    ],
)
def test_clean_rows_counts_invalid_rows(bad):
    pings, report = clean_rows([bad])
    assert pings == [] and report == CleaningReport(total=1, invalid=1)


def test_clean_rows_duplicates_first_wins_and_ignores_device_case_and_spaces():
    pings, report = clean_rows(
        [row(speed_kmh="10"), row(device_id=" ab-12 ", speed_kmh="99"), row(device_id="XY-1")]
    )
    assert [(p.device_id, p.speed_kmh) for p in pings] == [("AB-12", 10.0), ("XY-1", 40.0)]
    assert report.duplicates == 1


def test_clean_rows_duplicates_are_detected_on_the_instant_not_the_text():
    pings, report = clean_rows(
        [row(timestamp="1/5/2024 08:00:00"), row(timestamp="01/05/2024 08:00:00")]
    )
    assert len(pings) == 1 and report.duplicates == 1  # deliberate improvement over legacy


def test_clean_rows_dropped_rows_do_not_reserve_their_key():
    pings, report = clean_rows([row(speed_kmh="250"), row(speed_kmh="40")])
    assert [p.speed_kmh for p in pings] == [40.0]
    assert (report.too_fast, report.duplicates, report.kept) == (1, 0, 1)


def test_clean_rows_rule_order_decides_the_bucket():
    # null island AND too fast -> counted as null_island (rule 2 comes before rule 3)
    _, report = clean_rows([row(lat="0", lon="0", speed_kmh="300")])
    assert report == CleaningReport(total=1, null_island=1)


def test_clean_rows_preserves_input_order_and_accepts_any_iterable():
    rows = (row(timestamp=f"01/05/2024 08:{m:02d}:00") for m in (5, 1, 3))
    pings, _ = clean_rows(rows)
    assert [p.timestamp.minute for p in pings] == [5, 1, 3]


def test_report_buckets_add_up():
    _, report = clean_rows(read_rows(DATA))
    parts = report.kept + report.invalid + report.null_island + report.too_fast + report.duplicates
    assert report.total == parts


def test_sample_file_numbers():
    pings, report = clean_rows(read_rows(DATA))
    assert len(pings) == 115
    assert report == CleaningReport(
        total=123, kept=115, invalid=3, null_island=1, too_fast=2, duplicates=2
    )


def test_read_rows_streams_and_decodes_utf8(tmp_path):
    path = tmp_path / "p.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["device_id", "note"])
        writer.writeheader()
        writer.writerow({"device_id": "Zoë", "note": "a, b"})
    iterator = read_rows(path)
    assert next(iterator) == {"device_id": "Zoë", "note": "a, b"}


def test_read_rows_missing_file_raises_on_iteration(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(read_rows(tmp_path / "missing.csv"))
