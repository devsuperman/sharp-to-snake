"""Domain models (lesson 06). Implement these as dataclasses."""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Position:
    """One GPS fix.

    Fields (in order): ``lat: float``, ``lon: float``, ``timestamp: datetime``.

    Immutable. ``__post_init__`` must raise ``InvalidPositionError`` unless
    -90 <= lat <= 90 and -180 <= lon <= 180 (import it from ``gps.errors``).
    """

    lat: float
    lon: float
    timestamp: datetime


@dataclass(frozen=True)
class Segment:
    """The movement between two consecutive positions.

    Fields: ``start: Position``, ``end: Position``, ``distance_km: float``, ``speed_kmh: float``.
    Property ``duration`` -> ``timedelta`` between the two timestamps.
    """

    start: Position
    end: Position
    distance_km: float
    speed_kmh: float

    @property
    def duration(self) -> timedelta:
        raise NotImplementedError


@dataclass(frozen=True)
class Stop:
    """A period where the vehicle was (almost) stationary.

    Fields: ``start: datetime``, ``end: datetime``, ``lat: float``, ``lon: float``.
    Property ``duration`` -> ``timedelta`` (``end - start``).
    """

    start: datetime
    end: datetime
    lat: float
    lon: float

    @property
    def duration(self) -> timedelta:
        raise NotImplementedError


@dataclass(frozen=True)
class Summary:
    """The result of analysing a track.

    Fields: ``total_distance_km: float``, ``duration: timedelta``, ``avg_speed_kmh: float``,
    ``stops: list[Stop]``.

    ``to_dict()`` returns a JSON-friendly dict:
        {
          "total_distance_km": <rounded to 3 decimals>,
          "duration_seconds": <int>,
          "avg_speed_kmh": <rounded to 2 decimals>,
          "stops": [
            {"start": <ISO str>, "end": <ISO str>, "duration_seconds": <int>,
             "lat": <float>, "lon": <float>},
            ...
          ],
        }
    """

    total_distance_km: float
    duration: timedelta
    avg_speed_kmh: float
    stops: list[Stop]

    def to_dict(self) -> dict[str, object]:
        raise NotImplementedError
