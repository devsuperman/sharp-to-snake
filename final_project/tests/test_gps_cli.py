import json
import subprocess
import sys
from pathlib import Path

import pytest
from gps.cli import main

PROJECT = Path(__file__).resolve().parent.parent
SAMPLE = PROJECT / "data" / "sample_trip.csv"


def test_summary_text_output(capsys):
    assert main(["summary", str(SAMPLE)]) == 0
    out = capsys.readouterr().out
    assert f"File: {SAMPLE}" in out
    assert "Distance: 12.23 km" in out
    assert "Duration: 0:30:00" in out
    assert "Average speed: 24.46 km/h" in out
    assert "Stops: 1" in out
    assert "08:10:00 -> 08:18:00 (0:08:00)" in out


def test_summary_json_output(capsys):
    assert main(["summary", str(SAMPLE), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["duration_seconds"] == 1800
    assert data["total_distance_km"] == pytest.approx(12.231, abs=0.01)
    assert len(data["stops"]) == 1
    assert data["stops"][0]["duration_seconds"] == 480


def test_stop_minutes_option_changes_detection(capsys):
    assert main(["summary", str(SAMPLE), "--stop-minutes", "10"]) == 0
    assert "Stops: 0" in capsys.readouterr().out


def test_missing_file_is_reported_not_raised(capsys):
    assert main(["summary", "does-not-exist.csv"]) == 1
    captured = capsys.readouterr()
    assert captured.err.startswith("error:")
    assert "does-not-exist.csv" in captured.err


def test_malformed_file_is_reported(tmp_path, capsys):
    bad = tmp_path / "bad.csv"
    bad.write_text("timestamp,lat,lon\n2024-05-01T08:00:00,oops,1\n", encoding="utf-8")
    assert main(["summary", str(bad)]) == 1
    assert "line 2" in capsys.readouterr().err


def test_unsupported_suffix_is_reported(tmp_path, capsys):
    other = tmp_path / "track.gpx"
    other.write_text("<gpx/>", encoding="utf-8")
    assert main(["summary", str(other)]) == 1
    assert capsys.readouterr().err.startswith("error:")


def test_python_dash_m_gps_works_end_to_end():
    result = subprocess.run(
        [sys.executable, "-m", "gps", "summary", "data/sample_trip.csv"],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Distance: 12.23 km" in result.stdout
