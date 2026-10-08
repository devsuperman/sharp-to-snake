"""Parity tests: the new implementation against the legacy script, on the same input.

They are the safety net of the migration. Where the new code is DELIBERATELY different
(fixed bugs), the difference is asserted explicitly rather than hidden.
"""

import json
from pathlib import Path

import pytest
from legacy_fakes import FakeHttp

from course_support.http_fakes import FakeClient
from course_support.rest_types import Response
from legacy import sync_positions as legacy
from positions_sync.cleaning import clean_rows, read_rows
from positions_sync.config import Config
from positions_sync.sender import send_pings

DATA = Path(__file__).resolve().parent.parent / "data" / "raw_pings.csv"
CONFIG = Config(api_url="http://localhost:8080/api/positions", token="secret")


def test_cleaning_produces_exactly_the_rows_the_legacy_script_kept():
    pings, _ = clean_rows(read_rows(DATA))
    assert [ping.to_payload() for ping in pings] == legacy.load(DATA)


def test_full_batches_are_identical_to_what_legacy_posted(monkeypatch):
    http = FakeHttp(monkeypatch)
    legacy.run(DATA)
    legacy_bodies = http.bodies()

    client = FakeClient()
    pings, _ = clean_rows(read_rows(DATA))
    send_pings(client, CONFIG, pings, sleep=lambda _: None)
    new_bodies = [call.json for call in client.calls]

    assert new_bodies[: len(legacy_bodies)] == legacy_bodies  # same data, same batching
    assert len(new_bodies) == len(legacy_bodies) + 1  # ... plus the batch legacy lost
    assert len(new_bodies[-1]) == 15


def test_authorization_header_is_unchanged(monkeypatch):
    http = FakeHttp(monkeypatch)
    legacy.post([{"device": "A"}])
    legacy_header = http.requests[0].get_header("Authorization")

    client = FakeClient()
    pings, _ = clean_rows(read_rows(DATA))
    send_pings(client, CONFIG, pings[:1], sleep=lambda _: None)
    assert client.calls[0].headers["Authorization"] == legacy_header


def test_every_ping_legacy_lost_is_now_delivered(monkeypatch):
    http = FakeHttp(monkeypatch)
    legacy.run(DATA)
    delivered_by_legacy = {(p["device"], p["ts"]) for body in http.bodies() for p in body}

    client = FakeClient()
    pings, report = clean_rows(read_rows(DATA))
    send_pings(client, CONFIG, pings, sleep=lambda _: None)
    delivered_now = {(p["device"], p["ts"]) for call in client.calls for p in call.json}

    assert delivered_by_legacy < delivered_now  # strict subset
    assert len(delivered_now) == report.kept == 115
    assert len(delivered_now - delivered_by_legacy) == 15


def test_payload_is_valid_json_serialisable():
    pings, _ = clean_rows(read_rows(DATA))
    json.dumps([ping.to_payload() for ping in pings])  # must not raise (no datetime objects)


@pytest.mark.parametrize("status", [201, 202])
def test_legacy_resends_on_201_new_code_does_not(monkeypatch, status):
    http = FakeHttp(monkeypatch, [status] * 3)
    legacy.post([{"device": "A"}])
    assert len(http.requests) == 3

    client = FakeClient(default=Response(status))
    pings, _ = clean_rows(read_rows(DATA))
    send_pings(client, CONFIG, pings[:3], sleep=lambda _: None)
    assert len(client.calls) == 1
