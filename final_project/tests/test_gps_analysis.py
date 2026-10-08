from datetime import datetime, timedelta
from pathlib import Path

import pytest
from gps.analysis import detect_stops, summarize
from gps.errors import NotEnoughDataError
from gps.geo import iter_segments
from gps.models import Position
from gps.readers import iter_positions_csv

T0 = datetime(2024, 5, 1, 8, 0, 0)
SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_trip.csv"
STEP = 0.005  # degrees of latitude per minute, ~33.4 km/h


def track(pattern: str) -> list[Position]:
    """Build a track from a pattern: one char per minute, 'm' = moving, 's' = standing still."""
    lat, points = 0.0, [Position(0.0, 0.0, T0)]
    for minute, step in enumerate(pattern, start=1):
        lat += STEP if step == "m" else 0.0
        points.append(Position(lat, 0.0, T0 + timedelta(minutes=minute)))
    return points


def test_detect_stops_finds_a_long_enough_stop():
    stops = detect_stops(iter_segments(track("mmmsssssssmm")))  # 7 minutes standing
    assert len(stops) == 1
    stop = stops[0]
    assert stop.start == T0 + timedelta(minutes=3)
    assert stop.end == T0 + timedelta(minutes=10)
    assert stop.duration == timedelta(minutes=7)
    assert stop.lat == pytest.approx(3 * STEP)


def test_detect_stops_ignores_short_stops():
    assert detect_stops(iter_segments(track("mmsssmm"))) == []  # only 3 minutes


@pytest.mark.parametrize(
    ("min_minutes", "expected"),
    [(3, 1), (4, 0)],
)
def test_detect_stops_respects_min_minutes(min_minutes, expected):
    assert len(detect_stops(iter_segments(track("mmsssmm")), min_minutes=min_minutes)) == expected


def test_detect_stops_multiple_stops_and_a_stop_at_the_end():
    stops = detect_stops(iter_segments(track("mssssssmmssssss")))
    assert [s.duration for s in stops] == [timedelta(minutes=6), timedelta(minutes=6)]


def test_detect_stops_never_stopped():
    assert detect_stops(iter_segments(track("mmmmmm"))) == []


def test_detect_stops_speed_threshold():
    slow = [Position(0.0, 0.0, T0), Position(0.0017, 0.0, T0 + timedelta(minutes=10))]  # ~1.1 km/h
    segments = list(iter_segments(slow))
    assert len(detect_stops(segments, max_speed_kmh=2.0)) == 1
    assert detect_stops(segments, max_speed_kmh=1.0) == []


def test_summarize_the_sample_trip():
    summary = summarize(iter_positions_csv(SAMPLE))
    assert summary.total_distance_km == pytest.approx(12.231, abs=0.01)
    assert summary.duration == timedelta(minutes=30)
    assert summary.avg_speed_kmh == pytest.approx(24.46, abs=0.05)
    assert len(summary.stops) == 1
    assert summary.stops[0].start == datetime(2024, 5, 1, 8, 10)
    assert summary.stops[0].end == datetime(2024, 5, 1, 8, 18)


def test_summarize_accepts_a_one_shot_generator():
    positions = (p for p in track("mmmsssssssmm"))
    summary = summarize(positions)
    assert summary.duration == timedelta(minutes=12)
    assert len(summary.stops) == 1


def test_summarize_passes_stop_settings_through():
    summary = summarize(track("mmsssmm"), min_stop_minutes=3)
    assert len(summary.stops) == 1


@pytest.mark.parametrize("count", [0, 1])
def test_summarize_needs_two_positions(count):
    with pytest.raises(NotEnoughDataError):
        summarize(track("m")[:count])
