"""
Lesson 08: Files and JSON

Goal: read and write text files, CSV and JSON safely with pathlib and context managers.
"""

# 1. CONCEPT
# `pathlib.Path` is the modern way to handle paths (objects, `/` operator, cross-platform).
# `open()` returns a file object; always use it in a `with` block so the file is closed even
# if an error occurs. ALWAYS pass `encoding="utf-8"` for text: the default depends on the OS.
#
#   Path.read_text() / write_text()   whole-file shortcuts
#   open(path) + iteration            streams line by line (constant memory)
#   json.loads/dumps                  str <-> Python objects
#   json.load/dump                    file <-> Python objects
#   csv.DictReader / DictWriter       rows as dicts keyed by the header line

import csv
import json
import tempfile
from pathlib import Path

# 2. EXAMPLES


def demo_paths(base: Path) -> None:
    path = base / "reports" / "2024" / "summary.txt"  # `/` joins path parts
    print(path.name, path.stem, path.suffix, path.parent.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("line one\nline two\n", encoding="utf-8")
    print("exists:", path.exists(), "| is_file:", path.is_file())
    print("found:", [p.relative_to(base).as_posix() for p in base.rglob("*.txt")])


def demo_reading(base: Path) -> None:
    path = base / "lines.txt"
    path.write_text("alpha\n\nbeta\ngamma\n", encoding="utf-8")

    with path.open(encoding="utf-8") as handle:  # streams; never loads the whole file
        for number, line in enumerate(handle, start=1):
            print(f"  {number}: {line.rstrip()!r}")

    print("all text:", path.read_text(encoding="utf-8").splitlines())


def demo_json(base: Path) -> None:
    payload = {"name": "Zoë", "tags": ["a", "b"], "active": True, "score": None}
    text = json.dumps(payload, indent=2, ensure_ascii=False)  # ensure_ascii=False keeps "ë"
    print(text)
    print(json.loads(text) == payload)  # round trip

    path = base / "data.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    print("loaded:", json.loads(path.read_text(encoding="utf-8"))["name"])
    # JSON has no tuple/set/datetime: they need conversion (tuple -> list, datetime -> str)


def demo_csv(base: Path) -> None:
    path = base / "fleet.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:  # newline="" is required for csv
        writer = csv.DictWriter(handle, fieldnames=["plate", "km"])
        writer.writeheader()
        writer.writerows([{"plate": "A1", "km": 120}, {"plate": "B2", "km": 80}])

    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    print(rows)  # NOTE: every value is a str; convert explicitly (int(row["km"]))


def demo_missing_file(base: Path) -> None:
    try:
        (base / "nope.txt").read_text(encoding="utf-8")
    except FileNotFoundError as err:  # EAFP, see lesson 07
        print("missing file ->", type(err).__name__)


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:  # a throwaway directory, removed afterwards
        base = Path(tmp)
        demo_paths(base)
        demo_reading(base)
        demo_json(base)
        demo_csv(base)
        demo_missing_file(base)


# 3. C# EQUIVALENT
#
#   Python                               C#
#   -----------------------------------  ---------------------------------------------
#   Path("a") / "b" / "c.txt"            Path.Combine("a", "b", "c.txt")
#   path.read_text(encoding="utf-8")     File.ReadAllText(path, Encoding.UTF8)
#   with open(...) as f: for line in f   using var r = new StreamReader(...); ReadLine()
#   path.mkdir(parents=True)             Directory.CreateDirectory(path)
#   path.rglob("*.txt")                  Directory.EnumerateFiles(p, "*.txt", AllDirectories)
#   json.dumps / json.loads              JsonSerializer.Serialize / Deserialize
#   csv.DictReader                       CsvHelper (3rd party) -- the BCL has no CSV reader
#   with (context manager)               using (IDisposable)
#   tempfile.TemporaryDirectory()        Directory.CreateTempSubdirectory()

# 4. COMMON PITFALLS
#
#   a) Forgetting encoding="utf-8" works on your machine and breaks on another OS.
#   b) csv files need newline="" on open(), or you get blank lines on Windows.
#   c) CSV values are always strings; json numbers/bools/null keep their types.
#   d) json.dump cannot serialize datetime/set/Decimal directly; convert first (or `default=`).
#   e) read_text() loads everything into memory; iterate over the file for large inputs.

# 5. EXERCISE
# Open exercises/ex08_files_json.py, implement the functions, then run:
#     python runner.py test 08

if __name__ == "__main__":
    demo()
