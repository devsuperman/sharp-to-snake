"""Exercise 14: consuming REST APIs reliably.

Read lessons/14_rest_resilience.py first. The HTTP vocabulary (``Response``, ``TransportError``,
``HttpStatusError``, ``HttpClient``) is given in ``course_support/rest_types.py``; the tests use
a scripted fake client, so no network or real sleeping is involved.
Run the tests with:  python runner.py test 14
"""

import time
from collections.abc import Callable, Iterator

from course_support.rest_types import (  # noqa: F401  (HttpStatusError/TransportError are used by your code)
    HttpClient,
    HttpStatusError,
    Response,
    TransportError,
)

RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})


def build_headers(
    token: str | None = None,
    *,
    scheme: str = "Bearer",
    basic: tuple[str, str] | None = None,
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build the request headers.

    Always present: ``Accept`` and ``Content-Type``, both ``application/json``.
    - ``token``  -> ``Authorization: "<scheme> <token>"`` (default scheme "Bearer")
    - ``basic``  -> ``Authorization: "Basic <base64 of 'user:password'>"`` (UTF-8, standard base64)
    - giving both ``token`` and ``basic`` raises ``ValueError``
    - ``extra`` is merged last and may override anything.

    Example:
        build_headers("abc") ["Authorization"] == "Bearer abc"
        build_headers(basic=("user", "secret"))["Authorization"] == "Basic dXNlcjpzZWNyZXQ="
    """
    raise NotImplementedError


def is_retryable_status(status: int) -> bool:
    """True when the status is in ``RETRYABLE_STATUSES`` (a transient failure)."""
    raise NotImplementedError


def backoff_delays(
    retries: int, base: float = 0.5, factor: float = 2.0, cap: float = 30.0
) -> list[float]:
    """Return the wait before each retry: ``min(cap, base * factor**n)`` for n = 0..retries-1.

    Examples:
        backoff_delays(4)                  -> [0.5, 1.0, 2.0, 4.0]
        backoff_delays(4, base=10, cap=25) -> [10.0, 20.0, 25.0, 25.0]
        backoff_delays(0)                  -> []
    """
    raise NotImplementedError


def call_with_retry(
    client: HttpClient,
    method: str,
    url: str,
    *,
    json: object | None = None,
    headers: dict[str, str] | None = None,
    retries: int = 3,
    base_delay: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
) -> Response:
    """Send a request, retrying transient failures. Total attempts = ``retries + 1``.

    - 2xx response            -> return it immediately.
    - ``TransportError``      -> retryable.
    - retryable status        -> retryable (see ``is_retryable_status``).
    - any other status (400, 401, 404, ...) -> raise ``HttpStatusError(status, body)`` at once,
      without sleeping or retrying.
    - Before retry number n (0-based) call ``sleep(delay)`` where ``delay`` is
      ``backoff_delays(retries, base_delay)[n]``; BUT if the failed response carries a numeric
      ``Retry-After`` header (case-insensitive name, value in seconds), sleep that value instead.
    - When the attempts are exhausted: re-raise the last ``TransportError``, or raise
      ``HttpStatusError`` for the last retryable status. Never sleep after the final attempt.
    - Every attempt sends the same ``method``, ``url``, ``json`` and ``headers``.
    """
    raise NotImplementedError


def idempotency_key(payload: object) -> str:
    """A stable key for a payload: the SHA-256 hex digest of its canonical JSON.

    Canonical JSON = ``json.dumps(payload, sort_keys=True, separators=(",", ":"),
    ensure_ascii=False)`` encoded as UTF-8. Equal payloads (whatever their dict key order)
    give equal keys; different payloads give different keys.
    """
    raise NotImplementedError


def post_idempotent(
    client: HttpClient,
    url: str,
    payload: object,
    *,
    headers: dict[str, str] | None = None,
    key: str | None = None,
    retries: int = 3,
    base_delay: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
) -> Response:
    """POST ``payload`` safely: add an ``Idempotency-Key`` header and retry like
    ``call_with_retry``.

    The key is ``key`` if given, else ``idempotency_key(payload)``. The SAME key must be sent on
    every attempt. Other ``headers`` are preserved (the caller's dict must not be mutated).
    """
    raise NotImplementedError


def process_once(message_id: str, handler: Callable[[], None], seen: set[str]) -> bool:
    """Consumer-side de-duplication: run ``handler`` unless ``message_id`` is already in ``seen``.

    - already seen -> do not call ``handler``; return ``False``.
    - otherwise call ``handler()``; only AFTER it returns normally add the id to ``seen`` and
      return ``True``. If the handler raises, the exception propagates and the id is NOT
      recorded (so the message can be retried).
    """
    raise NotImplementedError


def iter_pages(
    client: HttpClient,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> Iterator[dict]:
    """Lazily yield every item of a paginated collection.

    Each page is a JSON object ``{"items": [...], "next": "<url>" | None}``. GET ``url`` (using
    ``call_with_retry``), yield the items one by one, then follow ``next`` until it is ``None``
    or missing. Pages must be requested lazily: taking only the first item must not fetch the
    second page.
    """
    raise NotImplementedError
