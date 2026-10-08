import inspect
import itertools
from datetime import datetime, timedelta

import pytest
from gps.errors import OutOfOrderError
from gps.geo import haversine_km, iter_segments, make_segment
from gps.models import Position

T0 = datetime(2024, 5, 1, 8, 0, 0)


def at(minutes: float, lat: float = 0.0, lon: float = 0.0) -> Position:
    return Position(lat, lon, T0 + timedelta(minutes=minutes))


def test_haversine_same_point_is_zero():
    assert haversine_km(at(0, 10, 10), at(1, 10, 10)) == pytest.approx(0.0, abs=1e-9)


def test_haversine_one_degree_of_longitude_at_the_equator():
    assert haversine_km(at(0, 0, 0), at(1, 0, 1)) == pytest.approx(111.195, rel=1e-4)


def test_haversine_london_to_paris():
    london, paris = at(0, 51.5074, -0.1278), at(1, 48.8566, 2.3522)
    assert haversine_km(london, paris) == pytest.approx(343.6, abs=1.0)


def test_haversine_is_symmetric():
    a, b = at(0, -23.55, -46.63), at(1, -22.90, -43.17)
    assert haversine_km(a, b) == pytest.approx(haversine_km(b, a))


def test_make_segment_computes_distance_and_speed():
    segment = make_segment(at(0, 0, 0), at(30, 0, 1))  # ~111.195 km in half an hour
    assert segment.distance_km == pytest.approx(111.195, rel=1e-4)
    assert segment.speed_kmh == pytest.approx(222.39, rel=1e-4)


def test_make_segment_stationary_has_zero_speed():
    assert make_segment(at(0, 5, 5), at(1, 5, 5)).speed_kmh == pytest.approx(0.0, abs=1e-6)


@pytest.mark.parametrize("minutes", [0, -1])
def test_make_segment_rejects_non_increasing_time(minutes):
    with pytest.raises(OutOfOrderError):
        make_segment(at(0), at(minutes))


def test_iter_segments_pairs_consecutive_positions():
    positions = [at(0, 0, 0), at(1, 0, 0.01), at(2, 0, 0.02)]
    segments = list(iter_segments(positions))
    assert len(segments) == 2
    assert segments[0].start is positions[0] and segments[0].end is positions[1]
    assert segments[1].start is positions[1] and segments[1].end is positions[2]


@pytest.mark.parametrize("count", [0, 1])
def test_iter_segments_needs_two_positions(count):
    assert list(iter_segments([at(i) for i in range(count)])) == []


def test_iter_segments_is_lazy_and_accepts_one_shot_generators():
    def endless():
        for minute in itertools.count():
            yield at(minute, 0, minute * 0.001)

    segments = iter_segments(endless())
    assert inspect.isgenerator(segments)
    assert len(list(itertools.islice(segments, 5))) == 5
