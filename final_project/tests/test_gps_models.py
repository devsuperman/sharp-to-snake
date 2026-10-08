import dataclasses
from datetime import datetime, timedelta

import pytest
from gps.errors import GpsError, InvalidPositionError
from gps.models import Position, Segment, Stop, Summary

T0 = datetime(2024, 5, 1, 8, 0, 0)


def test_error_hierarchy():
    from gps.errors import MalformedRecordError, NotEnoughDataError, OutOfOrderError

    assert issubclass(GpsError, Exception)
    for error in (InvalidPositionError, MalformedRecordError, OutOfOrderError, NotEnoughDataError):
        assert issubclass(error, GpsError)


def test_malformed_record_error_keeps_line_number():
    from gps.errors import MalformedRecordError

    error = MalformedRecordError(7, "bad lat")
    assert error.line_number == 7
    assert "7" in str(error)
    assert "bad lat" in str(error)


def test_position_is_frozen_dataclass():
    position = Position(10.0, 20.0, T0)
    assert dataclasses.is_dataclass(position)
    with pytest.raises(dataclasses.FrozenInstanceError):
        position.lat = 1.0  # type: ignore[misc]
    assert position == Position(10.0, 20.0, T0)


@pytest.mark.parametrize(("lat", "lon"), [(0, 0), (90, 180), (-90, -180), (-23.55, -46.63)])
def test_position_accepts_valid_coordinates(lat, lon):
    assert Position(lat, lon, T0).lat == lat


@pytest.mark.parametrize(("lat", "lon"), [(90.01, 0), (-91, 0), (0, 180.5), (0, -181)])
def test_position_rejects_invalid_coordinates(lat, lon):
    with pytest.raises(InvalidPositionError):
        Position(lat, lon, T0)


def test_segment_duration():
    start = Position(0, 0, T0)
    end = Position(0, 1, T0 + timedelta(minutes=30))
    assert Segment(start, end, 111.0, 222.0).duration == timedelta(minutes=30)


def test_stop_duration():
    stop = Stop(T0, T0 + timedelta(minutes=8), -23.5, -46.6)
    assert stop.duration == timedelta(minutes=8)


def test_summary_to_dict():
    stop = Stop(T0, T0 + timedelta(minutes=8), -23.5, -46.6)
    summary = Summary(12.23456, timedelta(minutes=30), 24.4626, [stop])
    assert summary.to_dict() == {
        "total_distance_km": 12.235,
        "duration_seconds": 1800,
        "avg_speed_kmh": 24.46,
        "stops": [
            {
                "start": "2024-05-01T08:00:00",
                "end": "2024-05-01T08:08:00",
                "duration_seconds": 480,
                "lat": -23.5,
                "lon": -46.6,
            }
        ],
    }
