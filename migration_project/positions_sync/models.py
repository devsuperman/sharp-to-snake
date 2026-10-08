"""The domain model: one cleaned GPS ping."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Ping:
    """One cleaned tracker ping.

    Fields (in order): ``device_id: str`` (already upper-cased and stripped),
    ``timestamp: datetime`` (AWARE, in UTC), ``lat: float``, ``lon: float``, ``speed_kmh: float``.
    """

    device_id: str
    timestamp: datetime
    lat: float
    lon: float
    speed_kmh: float

    def to_payload(self) -> dict[str, object]:
        """The JSON object the tracking API expects (same shape the legacy script sent).

        Keys: ``device``, ``ts`` (UTC, ``"%Y-%m-%dT%H:%M:%SZ"``), ``lat``, ``lon``, ``speed``.

        Example:
            {"device": "AB-12", "ts": "2024-05-01T11:00:00Z", "lat": -23.55, "lon": -46.63,
             "speed": 40.0}
        """
        raise NotImplementedError
