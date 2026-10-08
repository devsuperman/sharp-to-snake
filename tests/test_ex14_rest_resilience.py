import base64
import hashlib

import pytest

from course_support.http_fakes import FakeClient
from course_support.rest_types import HttpStatusError, Response, TransportError
from exercises.ex14_rest_resilience import (
    backoff_delays,
    build_headers,
    call_with_retry,
    idempotency_key,
    is_retryable_status,
    iter_pages,
    post_idempotent,
    process_once,
)

URL = "http://api.test/positions"


class Sleeper:
    def __init__(self):
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


# --- build_headers ---------------------------------------------------------------------------


def test_build_headers_defaults():
    assert build_headers() == {"Accept": "application/json", "Content-Type": "application/json"}


def test_build_headers_bearer_and_custom_scheme():
    assert build_headers("abc")["Authorization"] == "Bearer abc"
    assert build_headers("abc", scheme="Token")["Authorization"] == "Token abc"


def test_build_headers_basic():
    headers = build_headers(basic=("user", "secret"))
    assert headers["Authorization"] == "Basic dXNlcjpzZWNyZXQ="
    assert base64.b64decode(headers["Authorization"].split()[1]) == b"user:secret"


def test_build_headers_basic_is_utf8():
    encoded = build_headers(basic=("zoë", "pä"))["Authorization"].split()[1]
    assert base64.b64decode(encoded).decode("utf-8") == "zoë:pä"


def test_build_headers_rejects_both_and_extra_overrides():
    with pytest.raises(ValueError):
        build_headers("t", basic=("u", "p"))
    assert build_headers(extra={"Accept": "text/plain", "X-Id": "1"})["Accept"] == "text/plain"
    assert build_headers(extra={"X-Id": "1"})["X-Id"] == "1"


# --- is_retryable_status / backoff_delays ----------------------------------------------------


@pytest.mark.parametrize("status", [408, 429, 500, 502, 503, 504])
def test_retryable_statuses(status):
    assert is_retryable_status(status)


@pytest.mark.parametrize("status", [200, 201, 400, 401, 403, 404, 409, 422, 501])
def test_non_retryable_statuses(status):
    assert not is_retryable_status(status)


def test_backoff_delays_exponential_and_capped():
    assert backoff_delays(4) == [0.5, 1.0, 2.0, 4.0]
    assert backoff_delays(4, base=10, cap=25) == [10.0, 20.0, 25.0, 25.0]
    assert backoff_delays(0) == []


# --- call_with_retry -------------------------------------------------------------------------


def test_call_with_retry_success_first_try():
    client = FakeClient([Response(201, {"id": 1})])
    sleeper = Sleeper()
    response = call_with_retry(client, "POST", URL, json={"a": 1}, sleep=sleeper)
    assert response.status == 201
    assert len(client.calls) == 1 and sleeper.delays == []
    assert client.calls[0].method == "POST" and client.calls[0].json == {"a": 1}


def test_call_with_retry_recovers_from_transient_failures():
    client = FakeClient([TransportError("reset"), Response(503), Response(200, {"ok": True})])
    sleeper = Sleeper()
    response = call_with_retry(client, "GET", URL, sleep=sleeper)
    assert response.body == {"ok": True}
    assert len(client.calls) == 3
    assert sleeper.delays == [0.5, 1.0]


def test_call_with_retry_uses_base_delay():
    client = FakeClient([Response(500), Response(500), Response(200)])
    sleeper = Sleeper()
    call_with_retry(client, "GET", URL, base_delay=2, sleep=sleeper)
    assert sleeper.delays == [2.0, 4.0]


@pytest.mark.parametrize("status", [400, 401, 404, 422])
def test_call_with_retry_fails_fast_on_client_errors(status):
    client = FakeClient([Response(status, {"error": "nope"}), Response(200)])
    sleeper = Sleeper()
    with pytest.raises(HttpStatusError) as info:
        call_with_retry(client, "POST", URL, sleep=sleeper)
    assert info.value.status == status and info.value.body == {"error": "nope"}
    assert len(client.calls) == 1 and sleeper.delays == []


def test_call_with_retry_gives_up_with_last_status():
    client = FakeClient(default=Response(503, {"why": "down"}))
    sleeper = Sleeper()
    with pytest.raises(HttpStatusError) as info:
        call_with_retry(client, "GET", URL, retries=2, sleep=sleeper)
    assert info.value.status == 503
    assert len(client.calls) == 3  # retries + 1
    assert sleeper.delays == [0.5, 1.0]  # no sleep after the final attempt


def test_call_with_retry_gives_up_with_transport_error():
    boom = TransportError("timeout")
    client = FakeClient([boom, boom, boom])
    with pytest.raises(TransportError) as info:
        call_with_retry(client, "GET", URL, retries=2, sleep=Sleeper())
    assert info.value is boom


def test_call_with_retry_zero_retries_means_single_attempt():
    client = FakeClient([Response(503), Response(200)])
    with pytest.raises(HttpStatusError):
        call_with_retry(client, "GET", URL, retries=0, sleep=Sleeper())
    assert len(client.calls) == 1


def test_call_with_retry_honours_retry_after_header():
    client = FakeClient([Response(429, headers={"retry-after": "7"}), Response(200)])
    sleeper = Sleeper()
    call_with_retry(client, "GET", URL, sleep=sleeper)
    assert sleeper.delays == [7.0]


def test_call_with_retry_ignores_non_numeric_retry_after():
    client = FakeClient([Response(503, headers={"Retry-After": "Wed, 21 Oct 2026"}), Response(200)])
    sleeper = Sleeper()
    call_with_retry(client, "GET", URL, sleep=sleeper)
    assert sleeper.delays == [0.5]


def test_call_with_retry_sends_identical_requests():
    client = FakeClient([Response(502), Response(200)])
    call_with_retry(client, "PUT", URL, json={"x": 1}, headers={"X-A": "1"}, sleep=Sleeper())
    first, second = client.calls
    assert first == second
    assert first.headers == {"X-A": "1"}


# --- idempotency -----------------------------------------------------------------------------


def test_idempotency_key_is_stable_and_order_independent():
    assert idempotency_key({"a": 1, "b": [1, 2]}) == idempotency_key({"b": [1, 2], "a": 1})
    assert idempotency_key({"a": 1}) != idempotency_key({"a": 2})


def test_idempotency_key_is_canonical_sha256():
    expected = hashlib.sha256(b'{"a":1,"n":"z\xc3\xab"}').hexdigest()
    assert idempotency_key({"n": "zë", "a": 1}) == expected


def test_post_idempotent_sends_same_key_on_every_attempt():
    client = FakeClient([TransportError("x"), Response(503), Response(201, {"id": 9})])
    response = post_idempotent(client, URL, {"device": "A1"}, sleep=Sleeper())
    assert response.status == 201
    keys = {call.headers["Idempotency-Key"] for call in client.calls}
    assert keys == {idempotency_key({"device": "A1"})}
    assert all(call.method == "POST" and call.json == {"device": "A1"} for call in client.calls)


def test_post_idempotent_explicit_key_and_headers_not_mutated():
    client = FakeClient()
    caller_headers = {"Authorization": "Bearer t"}
    post_idempotent(client, URL, {"a": 1}, headers=caller_headers, key="my-key", sleep=Sleeper())
    sent = client.calls[0].headers
    assert sent["Idempotency-Key"] == "my-key" and sent["Authorization"] == "Bearer t"
    assert caller_headers == {"Authorization": "Bearer t"}


def test_post_idempotent_does_not_retry_validation_errors():
    client = FakeClient([Response(422), Response(200)])
    with pytest.raises(HttpStatusError):
        post_idempotent(client, URL, {"a": 1}, sleep=Sleeper())
    assert len(client.calls) == 1


# --- process_once ----------------------------------------------------------------------------


def test_process_once_runs_handler_once_per_id():
    seen: set[str] = set()
    calls = []
    assert process_once("m1", lambda: calls.append("m1"), seen) is True
    assert process_once("m1", lambda: calls.append("again"), seen) is False
    assert process_once("m2", lambda: calls.append("m2"), seen) is True
    assert calls == ["m1", "m2"] and seen == {"m1", "m2"}


def test_process_once_failed_handler_is_not_recorded():
    seen: set[str] = set()

    def failing():
        raise RuntimeError("db down")

    with pytest.raises(RuntimeError):
        process_once("m1", failing, seen)
    assert "m1" not in seen
    assert process_once("m1", lambda: None, seen) is True  # can be retried


# --- iter_pages ------------------------------------------------------------------------------


def paged_client():
    return FakeClient(
        [
            Response(200, {"items": [{"id": 1}, {"id": 2}], "next": "http://api.test/p2"}),
            Response(200, {"items": [{"id": 3}], "next": "http://api.test/p3"}),
            Response(200, {"items": [{"id": 4}], "next": None}),
        ]
    )


def test_iter_pages_follows_next_links():
    client = paged_client()
    items = list(iter_pages(client, "http://api.test/p1", headers={"X": "1"}, sleep=Sleeper()))
    assert [item["id"] for item in items] == [1, 2, 3, 4]
    assert [c.url for c in client.calls] == [
        "http://api.test/p1",
        "http://api.test/p2",
        "http://api.test/p3",
    ]
    assert all(c.method == "GET" and c.headers == {"X": "1"} for c in client.calls)


def test_iter_pages_is_lazy():
    client = paged_client()
    iterator = iter_pages(client, "http://api.test/p1", sleep=Sleeper())
    assert client.calls == []  # nothing requested before iterating
    assert next(iterator) == {"id": 1}
    assert len(client.calls) == 1


def test_iter_pages_missing_next_and_empty_page():
    client = FakeClient([Response(200, {"items": []})])
    assert list(iter_pages(client, "http://api.test/p1", sleep=Sleeper())) == []


def test_iter_pages_retries_transient_failures():
    client = FakeClient([Response(503), Response(200, {"items": [{"id": 1}], "next": None})])
    sleeper = Sleeper()
    assert list(iter_pages(client, "http://api.test/p1", sleep=sleeper)) == [{"id": 1}]
    assert sleeper.delays == [0.5]
