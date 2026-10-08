"""A real HTTP client built on the standard library (``urllib``). Given code."""

from __future__ import annotations

import json as jsonlib
import urllib.error
import urllib.request

from course_support.rest_types import Response, TransportError


def _decode(raw: bytes) -> object:
    if not raw:
        return None
    try:
        return jsonlib.loads(raw)
    except ValueError:
        return raw.decode("utf-8", errors="replace")


class UrllibClient:
    """Implements the ``HttpClient`` protocol. HTTP error statuses are returned, not raised;
    only failures without a response become ``TransportError``."""

    def request(
        self,
        method: str,
        url: str,
        *,
        json: object | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 10.0,
    ) -> Response:
        data = None if json is None else jsonlib.dumps(json).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=dict(headers or {}), method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return Response(resp.status, _decode(resp.read()), dict(resp.headers))
        except urllib.error.HTTPError as err:
            return Response(err.code, _decode(err.read()), dict(err.headers))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
            raise TransportError(str(err)) from err
