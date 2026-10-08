"""Small HTTP vocabulary used by lesson 14 and the migration project.

Nothing here touches the network: it only defines the *shapes* your code talks to, so the
same code can run against a real client (``urllib_client.UrllibClient``) or a scripted fake
(``http_fakes.FakeClient``) in the tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Response:
    """An HTTP response: status code, decoded JSON body (or None) and response headers."""

    status: int
    body: object = None
    headers: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300


class TransportError(Exception):
    """The request never produced a response (DNS failure, connection reset, timeout)."""


class HttpStatusError(Exception):
    """The server answered, but with a status the caller cannot accept."""

    def __init__(self, status: int, body: object = None) -> None:
        super().__init__(f"HTTP {status}")
        self.status = status
        self.body = body


class HttpClient(Protocol):
    """Anything with this ``request`` method is an HTTP client (structural typing)."""

    def request(
        self,
        method: str,
        url: str,
        *,
        json: object | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> Response: ...
