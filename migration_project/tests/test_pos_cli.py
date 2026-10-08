from pathlib import Path

import pytest

from course_support.http_fakes import FakeClient
from course_support.rest_types import Response
from positions_sync.cli import main

DATA = Path(__file__).resolve().parent.parent / "data" / "raw_pings.csv"
ENV = {"TRACKING_TOKEN": "secret", "TRACKING_API": "http://api.test/positions"}


def no_sleep(_: float) -> None:
    return None


def test_successful_run_prints_summary_and_returns_zero(capsys):
    client = FakeClient()
    code = main([str(DATA)], ENV, client, sleep=no_sleep)
    assert code == 0
    assert capsys.readouterr().out.strip() == (
        "read=123 kept=115 skipped=8 sent=115 failed_batches=0"
    )
    assert [len(call.json) for call in client.calls] == [50, 50, 15]
    assert client.calls[0].url == "http://api.test/positions"


def test_failed_batches_make_the_exit_code_nonzero(capsys):
    client = FakeClient(default=Response(503))
    code = main([str(DATA)], ENV, client, sleep=no_sleep)
    assert code == 1
    assert "sent=0 failed_batches=3" in capsys.readouterr().out


def test_missing_token_is_reported_not_swallowed(capsys):
    client = FakeClient()
    code = main([str(DATA)], {}, client, sleep=no_sleep)
    captured = capsys.readouterr()
    assert code == 2 and client.calls == []
    assert captured.err.startswith("error:") and "TRACKING_TOKEN" in captured.err
    assert captured.out == ""


def test_missing_input_file(tmp_path, capsys):
    client = FakeClient()
    code = main([str(tmp_path / "nope.csv")], ENV, client, sleep=no_sleep)
    captured = capsys.readouterr()
    assert code == 2 and client.calls == []
    assert "file not found" in captured.err and "nope.csv" in captured.err


def test_wrong_command_line_exits_with_two():
    with pytest.raises(SystemExit) as info:
        main([], ENV, FakeClient(), sleep=no_sleep)
    assert info.value.code == 2
