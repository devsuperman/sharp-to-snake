import inspect
import json
from datetime import datetime
from pathlib import Path

import pytest
from gps.errors import InvalidPositionError, MalformedRecordError
from gps.models import Position
from gps.readers import iter_positions, iter_positions_csv, load_positions_json, parse_timestamp

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_trip.csv"


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_parse_timestamp():
    assert parse_timestamp("2024-05-01T08:30:15") == datetime(2024, 5, 1, 8, 30, 15)


def test_csv_reader_is_a_lazy_generator():
    assert inspect.isgenerator(iter_positions_csv(SAMPLE))


def test_csv_reader_reads_the_sample_file():
    positions = list(iter_positions_csv(SAMPLE))
    assert len(positions) == 31
    assert positions[0] == Position(-23.5505, -46.6333, datetime(2024, 5, 1, 8, 0, 0))
    assert positions[-1].timestamp == datetime(2024, 5, 1, 8, 30, 0)


def test_csv_reader_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(iter_positions_csv(tmp_path / "nope.csv"))


def test_csv_reader_header_must_have_all_columns(tmp_path):
    path = write(tmp_path, "t.csv", "timestamp,lat\n2024-05-01T08:00:00,1.0\n")
    with pytest.raises(MalformedRecordError) as info:
        list(iter_positions_csv(path))
    assert info.value.line_number == 1


@pytest.mark.parametrize(
    "bad_row",
    [
        "2024-05-01T08:01:00,abc,2.0",  # non numeric lat
        "not-a-date,1.0,2.0",  # bad timestamp
        "2024-05-01T08:01:00,1.0",  # missing value
    ],
)
def test_csv_reader_reports_the_line_number_of_a_bad_row(tmp_path, bad_row):
    path = write(tmp_path, "t.csv", f"timestamp,lat,lon\n2024-05-01T08:00:00,1.0,2.0\n{bad_row}\n")
    with pytest.raises(MalformedRecordError) as info:
        list(iter_positions_csv(path))
    assert info.value.line_number == 3  # header = line 1, first row = 2, bad row = 3


def test_csv_reader_chains_the_original_error(tmp_path):
    path = write(tmp_path, "t.csv", "timestamp,lat,lon\n2024-05-01T08:00:00,abc,2.0\n")
    with pytest.raises(MalformedRecordError) as info:
        list(iter_positions_csv(path))
    assert info.value.__cause__ is not None


def test_csv_reader_out_of_range_coordinates(tmp_path):
    path = write(tmp_path, "t.csv", "timestamp,lat,lon\n2024-05-01T08:00:00,95.0,2.0\n")
    with pytest.raises(InvalidPositionError):
        list(iter_positions_csv(path))


def test_json_loader(tmp_path):
    data = [
        {"timestamp": "2024-05-01T08:00:00", "lat": 1.5, "lon": 2.5},
        {"timestamp": "2024-05-01T08:01:00", "lat": 1.6, "lon": 2.6},
    ]
    path = write(tmp_path, "t.json", json.dumps(data))
    positions = load_positions_json(path)
    assert [p.lat for p in positions] == [1.5, 1.6]
    assert positions[1].timestamp == datetime(2024, 5, 1, 8, 1, 0)


def test_json_loader_reports_bad_item_index(tmp_path):
    data = [{"timestamp": "2024-05-01T08:00:00", "lat": 1.5, "lon": 2.5}, {"lat": 1.0}]
    path = write(tmp_path, "t.json", json.dumps(data))
    with pytest.raises(MalformedRecordError) as info:
        load_positions_json(path)
    assert info.value.line_number == 2


def test_json_loader_requires_a_list(tmp_path):
    path = write(tmp_path, "t.json", json.dumps({"lat": 1}))
    with pytest.raises(MalformedRecordError):
        load_positions_json(path)


def test_iter_positions_dispatches_on_suffix(tmp_path):
    assert len(list(iter_positions(SAMPLE))) == 31
    path = write(
        tmp_path, "t.json", json.dumps([{"timestamp": "2024-05-01T08:00:00", "lat": 1, "lon": 2}])
    )
    assert len(list(iter_positions(path))) == 1


def test_iter_positions_rejects_unknown_suffix(tmp_path):
    with pytest.raises(ValueError):
        list(iter_positions(tmp_path / "track.gpx"))
