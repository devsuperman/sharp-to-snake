from datetime import UTC, datetime, timedelta

import pytest

from course_support.http_fakes import FakeClient
from course_support.rest_types import Response, TransportError
from positions_sync.config import Config
from positions_sync.models import Ping
from positions_sync.sender import SendReport, send_pings

CONFIG = Config(api_url="http://api.test/positions", token="secret", batch_size=3, retries=2)


def pings(count: int) -> list[Ping]:
    start = datetime(2024, 5, 1, 11, 0, tzinfo=UTC)
    return [Ping("AB-12", start + timedelta(minutes=i), -23.5, -46.6, 30.0) for i in range(count)]


class Sleeper:
    def __init__(self):
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


def test_report_defaults():
    assert SendReport() == SendReport(0, 0, 0)


def test_sends_every_batch_including_the_last_partial_one():
    client = FakeClient()
    report = send_pings(client, CONFIG, pings(7), sleep=Sleeper())
    assert [len(call.json) for call in client.calls] == [3, 3, 1]
    assert report == SendReport(sent=7, batches_ok=3, batches_failed=0)


def test_request_shape_matches_the_legacy_contract():
    client = FakeClient()
    batch = pings(2)
    send_pings(client, CONFIG, batch, sleep=Sleeper())
    call = client.calls[0]
    assert call.method == "POST" and call.url == "http://api.test/positions"
    assert call.json == [p.to_payload() for p in batch]
    assert call.headers["Authorization"] == "Token secret"
    assert call.headers["Content-Type"] == "application/json"


def test_nothing_to_send_makes_no_request():
    client = FakeClient()
    assert send_pings(client, CONFIG, [], sleep=Sleeper()) == SendReport()
    assert client.calls == []


@pytest.mark.parametrize("status", [200, 201, 202, 204])
def test_any_2xx_is_a_success_and_is_not_resent(status):
    client = FakeClient(default=Response(status))
    report = send_pings(client, CONFIG, pings(3), sleep=Sleeper())
    assert len(client.calls) == 1 and report.batches_ok == 1


def test_retry_resends_the_batch_with_the_same_idempotency_key():
    client = FakeClient([TransportError("reset"), Response(503), Response(201)])
    sleeper = Sleeper()
    report = send_pings(client, CONFIG, pings(3), sleep=sleeper)
    assert report == SendReport(sent=3, batches_ok=1, batches_failed=0)
    assert len(client.calls) == 3
    keys = {call.headers["Idempotency-Key"] for call in client.calls}
    assert len(keys) == 1 and keys != {""}
    assert sleeper.delays == [0.5, 1.0]  # exponential backoff


def test_different_batches_get_different_idempotency_keys():
    client = FakeClient()
    send_pings(client, CONFIG, pings(6), sleep=Sleeper())
    first, second = (call.headers["Idempotency-Key"] for call in client.calls)
    assert first != second


def test_same_batch_content_gets_the_same_key_across_runs():
    keys = []
    for _ in range(2):
        client = FakeClient()
        send_pings(client, CONFIG, pings(3), sleep=Sleeper())
        keys.append(client.calls[0].headers["Idempotency-Key"])
    assert keys[0] == keys[1]


def test_a_failed_batch_is_counted_and_the_run_continues():
    # batch 1: 3 attempts (retries=2) all fail; batch 2: succeeds first time
    client = FakeClient([Response(503)] * 3 + [Response(200)])
    report = send_pings(client, CONFIG, pings(6), sleep=Sleeper())
    assert report == SendReport(sent=3, batches_ok=1, batches_failed=1)
    assert len(client.calls) == 4


def test_client_errors_are_not_retried_but_do_not_stop_the_run():
    client = FakeClient([Response(422, {"error": "bad"}), Response(200)])
    report = send_pings(client, CONFIG, pings(6), sleep=Sleeper())
    assert report == SendReport(sent=3, batches_ok=1, batches_failed=1)
    assert len(client.calls) == 2


def test_accepts_a_generator_of_pings():
    client = FakeClient()
    report = send_pings(client, CONFIG, (p for p in pings(4)), sleep=Sleeper())
    assert report.sent == 4 and len(client.calls) == 2
