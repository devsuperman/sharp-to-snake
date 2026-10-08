import textwrap

import pytest

from exercises.ex12_legacy_scripts import (
    Config,
    ConfigError,
    find_env_vars,
    find_global_writes,
    find_risky_excepts,
    list_imports,
    load_config,
)

SCRIPT = textwrap.dedent(
    """\
    import os, sys
    import urllib.request
    import numpy as np
    from datetime import datetime as dt
    from os.path import join
    from . import helpers
    from .pkg import thing

    URL = os.environ.get("API_URL", "http://localhost")
    TOKEN = os.getenv("API_TOKEN")
    RAW = os.environ["RAW_DIR"]
    DYNAMIC = os.getenv("PREFIX_" + "X")
    count = 0

    def run():
        global count, last
        import json
        try:
            count += 1
        except:
            print("swallowed")
        try:
            1 / 0
        except ZeroDivisionError:
            pass
        try:
            int("x")
        except ValueError:
            raise
        try:
            int("y")
        except OSError as err:
            print(err)

    def other():
        global count
    """
)


def line_of(text: str, occurrence: int = 1) -> int:
    seen = 0
    for number, line in enumerate(SCRIPT.splitlines(), start=1):
        if text in line:
            seen += 1
            if seen == occurrence:
                return number
    raise AssertionError(text)


def test_list_imports_top_level_sorted_unique():
    assert list_imports(SCRIPT) == ["datetime", "json", "numpy", "os", "sys", "urllib"]


def test_list_imports_ignores_relative_and_handles_empty():
    assert list_imports("from . import x\nfrom .a import b") == []
    assert list_imports("") == []


def test_list_imports_syntax_error_propagates():
    with pytest.raises(SyntaxError):
        list_imports("def (:")


def test_find_env_vars_three_forms_and_ignores_dynamic():
    assert find_env_vars(SCRIPT) == ["API_TOKEN", "API_URL", "RAW_DIR"]


def test_find_env_vars_none():
    assert find_env_vars("print('hello')") == []


def test_find_env_vars_deduplicates():
    source = 'import os\na = os.getenv("X")\nb = os.environ.get("X")\nc = os.environ["X"]'
    assert find_env_vars(source) == ["X"]


def test_find_risky_excepts_bare_and_pass_only():
    assert find_risky_excepts(SCRIPT) == [line_of("except:"), line_of("except ZeroDivisionError")]


def test_find_risky_excepts_clean_code_has_none():
    assert find_risky_excepts("try:\n    x = 1\nexcept ValueError as e:\n    print(e)\n") == []


def test_find_global_writes():
    assert find_global_writes(SCRIPT) == ["count", "last"]
    assert find_global_writes("x = 1") == []


def test_load_config_minimal_defaults():
    config = load_config({"API_URL": "http://x", "API_TOKEN": "t"})
    assert config == Config("http://x", "t", 10.0)


def test_load_config_strips_and_parses_timeout():
    config = load_config({"API_URL": " http://x ", "API_TOKEN": " t ", "TIMEOUT_SECONDS": " 2.5 "})
    assert config == Config("http://x", "t", 2.5)


def test_load_config_lists_all_missing_names_at_once():
    with pytest.raises(ConfigError) as info:
        load_config({"API_URL": "   "})
    message = str(info.value)
    assert "API_URL" in message and "API_TOKEN" in message


@pytest.mark.parametrize("bad", ["abc", "0", "-3", ""])
def test_load_config_rejects_bad_timeout(bad):
    with pytest.raises(ConfigError, match="TIMEOUT_SECONDS"):
        load_config({"API_URL": "u", "API_TOKEN": "t", "TIMEOUT_SECONDS": bad})


def test_config_error_is_an_exception():
    assert issubclass(ConfigError, Exception)
