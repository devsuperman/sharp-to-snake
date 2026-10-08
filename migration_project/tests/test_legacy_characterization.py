"""Characterization tests: they pin what the LEGACY script does today, bugs included.

These tests pass from the start and must keep passing: they are the record of the old
behaviour that your new implementation is compared against (see test_pos_parity.py).
Tests whose name starts with ``test_BUG_`` document behaviour that is almost certainly a
defect; the migration should FIX them, and ``MIGRATION.md`` is where you decide how.
"""

import csv
from pathlib import Path

import pytest
from legacy_fakes import FakeHttp

from legacy import sync_positions as legacy

DATA = Path(__file__).resolve().parent.parent / "data" / "raw_pings.csv"
FIELDS = ["device_id", "timestamp", "lat", "lon", "speed_kmh"]


def write_csv(path: Path, rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def row(**overrides: str) -> dict[str, str]:
    base = {
        "device_id": "AB-12",
        "timestamp": "01/05/2024 08:00:00",
        "lat": "-23.55",
        "lon": "-46.63",
        "speed_kmh": "40",
    }
    return {**base, **overrides}


@pytest.fixture
def http(monkeypatch):
    return FakeHttp(monkeypatch)


# --- load(): the implicit business rules -------------------------------------------------------


def test_load_converts_local_time_to_utc_by_adding_three_hours(tmp_path):
    rows = legacy.load(write_csv(tmp_path / "p.csv", [row()]))
    assert rows == [
        {
            "device": "AB-12",
            "ts": "2024-05-01T11:00:00Z",
            "lat": -23.55,
            "lon": -46.63,
            "speed": 40.0,
        }
    ]


def test_load_crosses_midnight_when_converting(tmp_path):
    rows = legacy.load(write_csv(tmp_path / "p.csv", [row(timestamp="01/05/2024 22:30:00")]))
    assert rows[0]["ts"] == "2024-05-02T01:30:00Z"


def test_load_normalises_device_id(tmp_path):
    rows = legacy.load(write_csv(tmp_path / "p.csv", [row(device_id="  ab-12 ")]))
    assert rows[0]["device"] == "AB-12"


def test_load_drops_null_island(tmp_path):
    assert legacy.load(write_csv(tmp_path / "p.csv", [row(lat="0", lon="0.0")])) == []


def test_load_keeps_zero_on_only_one_axis(tmp_path):
    assert len(legacy.load(write_csv(tmp_path / "p.csv", [row(lat="0", lon="-46.6")]))) == 1


@pytest.mark.parametrize(("speed", "kept"), [("200", True), ("200.1", False), ("-5", True)])
def test_load_speed_filter_is_strictly_above_200(tmp_path, speed, kept):
    rows = legacy.load(write_csv(tmp_path / "p.csv", [row(speed_kmh=speed)]))
    assert bool(rows) is kept


@pytest.mark.parametrize(
    "bad",
    [
        row(lat="abc"),
        row(lon=""),
        row(speed_kmh=""),
        row(timestamp="2024-05-01 08:00"),
        row(timestamp="31/02/2024 08:00:00"),
    ],
)
def test_load_silently_skips_unparseable_rows(tmp_path, bad):
    assert legacy.load(write_csv(tmp_path / "p.csv", [bad])) == []  # no error, no log


def test_load_duplicate_key_first_wins_after_normalising_device(tmp_path):
    rows = legacy.load(
        write_csv(
            tmp_path / "p.csv",
            [row(speed_kmh="10"), row(device_id=" ab-12 ", speed_kmh="99"), row(device_id="XY-1")],
        )
    )
    assert [(r["device"], r["speed"]) for r in rows] == [("AB-12", 10.0), ("XY-1", 40.0)]


def test_load_duplicate_detection_is_on_the_raw_timestamp_text(tmp_path):
    # "1/5/2024" and "01/05/2024" parse to the same instant, but the dedupe key is the raw text,
    # so the same ping is uploaded twice.
    rows = legacy.load(
        write_csv(
            tmp_path / "p.csv",
            [row(timestamp="1/5/2024 08:00:00"), row(timestamp="01/05/2024 08:00:00")],
        )
    )
    assert len(rows) == 2 and rows[0]["ts"] == rows[1]["ts"]


def test_load_filtered_rows_do_not_consume_their_key(tmp_path):
    # A too-fast row is dropped BEFORE its key is registered, so a later valid row survives.
    rows = legacy.load(write_csv(tmp_path / "p.csv", [row(speed_kmh="250"), row(speed_kmh="40")]))
    assert [r["speed"] for r in rows] == [40.0]


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        legacy.load(tmp_path / "missing.csv")


def test_load_sample_file_keeps_115_of_123_rows():
    rows = legacy.load(DATA)
    assert len(rows) == 115
    assert len({(r["device"], r["ts"]) for r in rows}) == 115


# --- post(): HTTP behaviour ----------------------------------------------------------------------


def test_post_success_sends_json_with_token_header(http):
    assert legacy.post([{"device": "A"}]) is True
    request = http.requests[0]
    assert request.full_url == "http://localhost:8080/api/positions"
    assert request.get_header("Authorization") == "Token secret"  # "Token", not "Bearer"
    assert request.get_header("Content-type") == "application/json"
    assert http.bodies() == [[{"device": "A"}]]
    assert legacy.sent == 1


def test_post_retries_exceptions_three_times_with_fixed_one_second_sleep(monkeypatch):
    http = FakeHttp(monkeypatch, [OSError("down")] * 3)
    assert legacy.post([{"device": "A"}]) is False
    assert len(http.requests) == 3
    assert http.sleeps == [1, 1, 1]  # fixed wait, no backoff, also sleeps after the last try
    assert (legacy.sent, legacy.errors) == (0, 3)


def test_post_recovers_after_a_transient_failure(monkeypatch):
    http = FakeHttp(monkeypatch, [OSError("down"), 200])
    assert legacy.post([{"device": "A"}, {"device": "B"}]) is True
    assert len(http.requests) == 2
    assert (legacy.sent, legacy.errors) == (2, 1)


def test_BUG_post_treats_201_as_failure_and_resends_the_same_batch_three_times(monkeypatch):
    http = FakeHttp(monkeypatch, [201, 201, 201])
    assert legacy.post([{"device": "A"}]) is False
    assert len(http.requests) == 3  # three identical POSTs: duplicates if the server accepted them
    assert http.sleeps == []  # and no wait between them
    assert legacy.sent == 0


def test_BUG_missing_token_fails_silently_before_any_request(http, monkeypatch):
    monkeypatch.setattr(legacy, "TOKEN", None)  # "Token " + None -> TypeError, swallowed
    assert legacy.post([{"device": "A"}]) is False
    assert http.requests == []  # nothing was ever sent
    assert legacy.errors == 3 and http.sleeps == [1, 1, 1]


# --- run(): the orchestration --------------------------------------------------------------------


def test_run_sends_full_batches_of_50(http, capsys):
    assert legacy.run(DATA) == 0
    assert [len(body) for body in http.bodies()] == [50, 50]  # 115 valid rows, 15 never sent
    assert capsys.readouterr().out.strip() == "sent 100 errors 0"


def test_BUG_run_never_sends_the_last_partial_batch(http, tmp_path):
    rows = [row(timestamp=f"01/05/2024 08:{minute:02d}:00") for minute in range(51)]
    legacy.run(write_csv(tmp_path / "p.csv", rows))
    assert [len(body) for body in http.bodies()] == [50]  # the 51st ping is lost
    assert legacy.sent == 50


def test_BUG_run_with_fewer_than_50_rows_sends_nothing_and_reports_success(http, tmp_path, capsys):
    exit_code = legacy.run(write_csv(tmp_path / "p.csv", [row()]))
    assert exit_code == 0 and http.requests == []
    assert capsys.readouterr().out.strip() == "sent 0 errors 0"


def test_BUG_run_exit_code_is_zero_even_when_every_batch_fails(monkeypatch, capsys):
    http = FakeHttp(monkeypatch, [OSError("down")] * 6)
    assert legacy.run(DATA) == 0
    output = capsys.readouterr().out
    assert output.count("FAILED batch") == 2 and "sent 0 errors 6" in output
    assert len(http.requests) == 6  # 2 batches x 3 attempts


def test_run_continues_with_the_next_batch_after_a_failure(monkeypatch):
    http = FakeHttp(monkeypatch, [OSError("down")] * 3 + [200])
    legacy.run(DATA)
    bodies = http.bodies()
    assert len(bodies) == 4  # 3 failed attempts for batch one, then batch two
    assert bodies[0] == bodies[1] == bodies[2]
    assert bodies[3] != bodies[0]
    assert legacy.sent == 50  # first batch lost for good, second one delivered
