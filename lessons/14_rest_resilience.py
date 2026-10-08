"""
Lesson 14: Consuming REST APIs reliably

Goal: call HTTP APIs the way production automation must: authenticated, with timeouts,
retries only where they are safe, and idempotent writes.
"""

# 1. CONCEPT
# The network fails in two different ways, and they are handled differently:
#   transport failure   no response at all (timeout, reset). The request MAY have been
#                       processed. Usually retryable.
#   bad status          the server answered. 4xx = your request is wrong (retrying cannot
#                       help, except 408 Timeout and 429 Too Many Requests). 5xx = the server
#                       is struggling (502/503/504 and sometimes 500 are worth retrying).
#
# A retry policy has four parts: WHICH failures, HOW MANY times, HOW LONG to wait (exponential
# backoff: 0.5s, 1s, 2s, ... with a cap, honouring `Retry-After`), and WHAT to do when giving up.
#
# Retrying a write is only safe if the write is IDEMPOTENT: doing it twice has the effect of
# doing it once. GET/PUT/DELETE are idempotent by definition; POST is not. Make POST safe with
# an idempotency key: the client sends the SAME unique key on every attempt and the server
# stores it, so a repeated key returns the first result instead of creating a duplicate.
# The mirror image applies to consumers of queues/webhooks: remember processed message ids.
#
# Other basics: always set a timeout (urllib/requests have none by default!), send credentials
# in the `Authorization` header (never in the URL), and follow pagination links lazily.

import base64
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # make `course_support` importable

from course_support.http_fakes import FakeClient  # noqa: E402
from course_support.rest_types import Response, TransportError  # noqa: E402

# 2. EXAMPLES


def demo_naive_retry_is_wrong() -> None:
    """The retry loop most legacy scripts have -- and why it is dangerous."""
    client = FakeClient([Response(400, {"error": "bad payload"})] * 3 + [Response(200, {})])
    attempts = 0
    for _ in range(3):  # retries EVERYTHING, even a 400 that can never succeed
        attempts += 1
        try:
            response = client.request("POST", "http://api/positions", json={"id": 1})
            if response.status == 200:
                break
        except Exception:  # noqa: BLE001 - also hides bugs in our own code
            pass
        time.sleep(0)  # fixed (here: zero) wait, no backoff
    print(f"sent {attempts} identical POSTs; the server may have created {attempts} records")


def demo_basic_auth_header() -> None:
    token = base64.b64encode(b"user:secret").decode("ascii")
    print({"Authorization": f"Basic {token}"})


def demo_scripted_failures() -> None:
    client = FakeClient([TransportError("timeout"), Response(503), Response(200, {"ok": True})])
    for _ in range(3):
        try:
            print("->", client.request("GET", "http://api/health"))
        except TransportError as err:
            print("-> transport error:", err)
    print("requests made:", len(client.calls))


def demo() -> None:
    demo_naive_retry_is_wrong()
    demo_basic_auth_header()
    demo_scripted_failures()


# 3. C# EQUIVALENT
#
#   Python (this lesson)                       C#
#   -----------------------------------------  ---------------------------------------------
#   client.request(method, url, ...)           HttpClient.SendAsync(HttpRequestMessage)
#   TransportError / HttpStatusError           HttpRequestException / EnsureSuccessStatusCode()
#   timeout=10.0                               HttpClient.Timeout / CancellationToken
#   call_with_retry(...)                       Polly: Policy.Handle<...>().WaitAndRetryAsync
#   backoff_delays(...)                        Polly: Backoff.ExponentialBackoff / DecorrelatedJitter
#   Idempotency-Key header                     same header (Stripe-style), generated per operation
#   sleep injected as a parameter              TimeProvider / fake delay in tests
#   iter_pages (generator)                     IAsyncEnumerable<T> with yield return
#   FakeClient                                 HttpMessageHandler stub / MockHttp

# 4. COMMON PITFALLS
#
#   a) No timeout means a hung connection hangs your job forever.
#   b) Retrying 4xx errors, or retrying non-idempotent POSTs without a key, creates duplicates.
#   c) Retrying instantly hammers a server that is already struggling: back off, add a cap.
#   d) Catching `Exception` around the whole call hides programming errors; catch the specific
#      transport/status errors you can recover from.
#   e) A 200 is not the only success: 201 Created and 204 No Content are successes too.
#   f) Tests that call `time.sleep` for real are slow; inject `sleep` and pass a fake.

# 5. EXERCISE
# Open exercises/ex14_rest_resilience.py, implement the functions, then run:
#     python runner.py test 14

if __name__ == "__main__":
    demo()
