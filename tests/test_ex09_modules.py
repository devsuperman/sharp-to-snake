import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run_python(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("  Python --- rocks ", "python-rocks"),
        ("!!!", ""),
        ("Already-slugged-123", "already-slugged-123"),
    ],
)
def test_slugify_via_package(text, expected):
    from exercises.ex09_textkit import slugify

    assert slugify(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"), [("Hello, World!  Again", 3), ("   ", 0), ("one", 1), ("", 0)]
)
def test_word_count_via_package(text, expected):
    from exercises.ex09_textkit import word_count

    assert word_count(text) == expected


def test_public_api_is_declared_and_comes_from_submodules():
    from exercises import ex09_textkit as package

    assert sorted(package.__all__) == ["slugify", "word_count"]
    assert package.slugify is package.slug.slugify
    assert package.word_count is package.counts.word_count


def test_import_has_no_side_effects():
    result = run_python("-c", "import exercises.ex09_textkit as p; p.slugify, p.word_count")
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""


def test_module_entry_point():
    result = run_python("-m", "exercises.ex09_textkit", "Hello, World!  Again")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["hello-world-again", "3"]
