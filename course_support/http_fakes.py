"""A scripted fake HTTP client for tests and lesson demos (no network involved)."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass

from course_support.rest_types import Response


@dataclass(frozen=True)
class Call:
    """One recorded request."""

    method: str
    url: str
    json: object | None
    headers: dict[str, str]
    timeout: float


class FakeClient:
    """Plays back a script, one item per request, then falls back to ``default``.

    Each script item is either a ``Response`` (returned) or an exception instance (raised).
    Every request is recorded in ``calls``.

        client = FakeClient([TransportError("boom"), Response(200, {"ok": True})])
    """

    def __init__(
        self,
        script: Iterable[Response | Exception] = (),
        default: Response | None = None,
    ) -> None:
        self._script: deque[Response | Exception] = deque(script)
        self._default = default if default is not None else Response(200, {})
        self.calls: list[Call] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        json: object | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> Response:
        self.calls.append(Call(method, url, json, dict(headers or {}), timeout))
        item = self._script.popleft() if self._script else self._default
        if isinstance(item, Exception):
            raise item
        return item
