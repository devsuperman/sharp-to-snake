"""Exercise 08: files and JSON.

Read lessons/08_files_and_json.py first, then implement every function below.
Always use ``encoding="utf-8"``. Run the tests with:  python runner.py test 08
"""

from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV file with a header line into a list of dicts (values stay strings).

    A missing file must raise ``FileNotFoundError`` (do not swallow it).

    Example:
        file "plate,km\\nA1,120\\n" -> [{"plate": "A1", "km": "120"}]
    """
    raise NotImplementedError


def write_json(path: Path, data: object) -> None:
    """Write ``data`` as pretty JSON (indent=2), UTF-8, keeping non-ASCII characters readable.

    Missing parent directories must be created. The file ends with a newline.

    Example:
        write_json(Path("out/a.json"), {"name": "Zoë"})  -> out/a.json contains "Zoë" literally
    """
    raise NotImplementedError


def load_json_or_default(path: Path, default: object) -> object:
    """Load JSON from ``path``; return ``default`` if the file does not exist.

    ONLY a missing file is tolerated: invalid JSON must still raise ``json.JSONDecodeError``.
    """
    raise NotImplementedError


def count_non_empty_lines(path: Path) -> int:
    """Count lines that contain something other than whitespace.

    Process the file line by line (do not read it whole).

    Example:
        "a\\n\\n  \\nb\\n" -> 2
    """
    raise NotImplementedError


def list_files(directory: Path, suffix: str) -> list[str]:
    """Recursively list files under ``directory`` whose name ends with ``suffix``.

    Return paths relative to ``directory``, as POSIX strings ("sub/a.txt"), sorted.
    Directories are not included.

    Example:
        tree: a.txt, sub/b.txt, sub/c.md  with suffix ".txt" -> ["a.txt", "sub/b.txt"]
    """
    raise NotImplementedError
