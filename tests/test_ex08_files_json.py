import json

import pytest

from exercises.ex08_files_json import (
    count_non_empty_lines,
    list_files,
    load_json_or_default,
    read_csv_rows,
    write_json,
)


def test_read_csv_rows(tmp_path):
    file = tmp_path / "fleet.csv"
    file.write_text("plate,km\nA1,120\nB2,80\n", encoding="utf-8")
    assert read_csv_rows(file) == [{"plate": "A1", "km": "120"}, {"plate": "B2", "km": "80"}]


def test_read_csv_rows_handles_utf8_and_quotes(tmp_path):
    file = tmp_path / "people.csv"
    file.write_text('name,note\n"Zoë","a, b"\n', encoding="utf-8")
    assert read_csv_rows(file) == [{"name": "Zoë", "note": "a, b"}]


def test_read_csv_rows_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_csv_rows(tmp_path / "missing.csv")


def test_write_json_round_trip_and_format(tmp_path):
    file = tmp_path / "out.json"
    write_json(file, {"name": "Zoë", "tags": [1, 2]})
    text = file.read_text(encoding="utf-8")
    assert json.loads(text) == {"name": "Zoë", "tags": [1, 2]}
    assert "Zoë" in text  # not escaped as ë
    assert '\n  "name"' in text  # indent=2
    assert text.endswith("\n")


def test_write_json_creates_parent_directories(tmp_path):
    file = tmp_path / "a" / "b" / "out.json"
    write_json(file, [1])
    assert json.loads(file.read_text(encoding="utf-8")) == [1]


def test_load_json_or_default_missing_file(tmp_path):
    assert load_json_or_default(tmp_path / "nope.json", {"empty": True}) == {"empty": True}


def test_load_json_or_default_existing_file(tmp_path):
    file = tmp_path / "x.json"
    file.write_text('{"a": 1}', encoding="utf-8")
    assert load_json_or_default(file, None) == {"a": 1}


def test_load_json_or_default_does_not_hide_invalid_json(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json_or_default(file, None)


def test_count_non_empty_lines(tmp_path):
    file = tmp_path / "t.txt"
    file.write_text("a\n\n  \nb\nc", encoding="utf-8")
    assert count_non_empty_lines(file) == 3


def test_count_non_empty_lines_empty_file(tmp_path):
    file = tmp_path / "t.txt"
    file.write_text("", encoding="utf-8")
    assert count_non_empty_lines(file) == 0


def test_list_files_recursive_sorted_relative(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "deeper").mkdir()
    for name in ("b.txt", "a.txt", "sub/c.txt", "sub/d.md", "sub/deeper/e.txt"):
        (tmp_path / name).write_text("x", encoding="utf-8")
    assert list_files(tmp_path, ".txt") == ["a.txt", "b.txt", "sub/c.txt", "sub/deeper/e.txt"]
    assert list_files(tmp_path, ".md") == ["sub/d.md"]
    assert list_files(tmp_path, ".zip") == []
