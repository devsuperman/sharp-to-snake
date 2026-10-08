"""Geometry and per-segment kinematics (lessons 03 and 05)."""

from collections.abc import Iterable, Iterator

from gps.models import Position, Segment

EARTH_RADIUS_KM = 6371.0088  # mean Earth radius


def haversine_km(a: Position, b: Position) -> float:
    """Great-circle distance between two positions, in kilometres.

    Formula (angles in radians):
        h = sin²(Δlat/2) + cos(lat_a) · cos(lat_b) · sin²(Δlon/2)
        distance = 2 · R · asin(sqrt(h))

    Examples:
        one degree of longitude at the equator is about 111.195 km
        the distance from a point to itself is 0.0
    """
    raise NotImplementedError


def make_segment(start: Position, end: Position) -> Segment:
    """Build the ``Segment`` between two positions.

    ``speed_kmh = distance_km / elapsed hours``.
    Raise ``OutOfOrderError`` if ``end.timestamp <= start.timestamp``.
    """
    raise NotImplementedError


def iter_segments(positions: Iterable[Position]) -> Iterator[Segment]:
    """Lazily yield a ``Segment`` for every pair of consecutive positions.

    Must work on a one-shot generator and must not load all positions into memory
    (``itertools.pairwise`` helps). Fewer than two positions yields nothing.
    """
    raise NotImplementedError
