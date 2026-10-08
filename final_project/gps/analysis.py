"""Stop detection and track summaries (lessons 04 and 05)."""

from collections.abc import Iterable

from gps.models import Position, Segment, Stop, Summary


def detect_stops(
    segments: Iterable[Segment],
    max_speed_kmh: float = 1.0,
    min_minutes: float = 5.0,
) -> list[Stop]:
    """Find the periods where the vehicle stayed (almost) still.

    A *run* is a maximal sequence of consecutive segments whose ``speed_kmh <= max_speed_kmh``.
    A run becomes a ``Stop`` when ``last.end.timestamp - first.start.timestamp`` lasts at least
    ``min_minutes`` minutes. The stop starts at the run's first start timestamp, ends at its last
    end timestamp, and sits at the first segment's start position (``lat``/``lon``).

    Process the segments in a single pass (they may come from a generator).
    """
    raise NotImplementedError


def summarize(
    positions: Iterable[Position],
    max_speed_kmh: float = 1.0,
    min_stop_minutes: float = 5.0,
) -> Summary:
    """Summarize a track.

    - ``total_distance_km``: sum of all segment distances
    - ``duration``: last timestamp - first timestamp
    - ``avg_speed_kmh``: total distance / duration in hours (stops included)
    - ``stops``: from ``detect_stops``

    ``positions`` may be a ONE-SHOT generator and a track can be huge, so make a single lazy
    pass: for example, wrap ``iter_segments(positions)`` in a small generator that updates running
    totals (distance, first/last timestamp) while ``detect_stops`` consumes it.
    Fewer than two positions raises ``NotEnoughDataError``.
    """
    raise NotImplementedError
