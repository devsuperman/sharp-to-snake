"""Course runner: list lessons, run their tests, and track progress.

Usage:
    python runner.py list
    python runner.py test 01        # one lesson ("final" for the GPS project)
    python runner.py test all
    python runner.py progress
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
PROGRESS_FILE = ROOT / "progress.json"


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    tests_glob: str  # relative to ROOT


LESSONS: tuple[Lesson, ...] = (
    Lesson("01", "Types and variables", "tests/test_ex01_*.py"),
    Lesson("02", "Control flow", "tests/test_ex02_*.py"),
    Lesson("03", "Functions", "tests/test_ex03_*.py"),
    Lesson("04", "Collections", "tests/test_ex04_*.py"),
    Lesson("05", "Comprehensions and iteration", "tests/test_ex05_*.py"),
    Lesson("06", "Classes and dataclasses", "tests/test_ex06_*.py"),
    Lesson("07", "Exceptions", "tests/test_ex07_*.py"),
    Lesson("08", "Files and JSON", "tests/test_ex08_*.py"),
    Lesson("09", "Modules and packages", "tests/test_ex09_*.py"),
    Lesson("10", "Async basics", "tests/test_ex10_*.py"),
    Lesson("11", "Type hints", "tests/test_ex11_*.py"),
    Lesson("final", "Final project: GPS fleet tracker", "final_project/tests/test_gps_*.py"),
)
LESSONS_BY_ID = {lesson.id: lesson for lesson in LESSONS}
NUMBERED = [lesson for lesson in LESSONS if lesson.id != "final"]


def load_progress() -> dict[str, dict]:
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def save_progress(progress: dict[str, dict]) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")


def run_lesson_tests(lesson: Lesson) -> dict:
    """Run pytest for one lesson and return a result record."""
    files = sorted(ROOT.glob(lesson.tests_glob))
    if not files:
        print(f"No test files found for '{lesson.id}' ({lesson.tests_glob}).")
        return {"completed": False, "passed": 0, "total": 0}

    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.xml"
        command = [sys.executable, "-m", "pytest", "-q", f"--junitxml={report}"]
        completed_process = subprocess.run([*command, *map(str, files)], cwd=ROOT)
        passed, total = read_counts(report)

    all_green = completed_process.returncode == 0 and total > 0 and passed == total
    return {
        "completed": all_green,
        "passed": passed,
        "total": total,
        "last_run": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def read_counts(report: Path) -> tuple[int, int]:
    """Return (passed, total) from a JUnit XML report; (0, 0) if unreadable."""
    try:
        root = ET.parse(report).getroot()
    except (FileNotFoundError, ET.ParseError):
        return 0, 0
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        return 0, 0
    total = int(suite.get("tests", 0))
    bad = sum(int(suite.get(key, 0)) for key in ("failures", "errors", "skipped"))
    return total - bad, total


def status_label(record: dict | None) -> str:
    if record is None:
        return "pending"
    return "completed" if record["completed"] else "in progress"


def cmd_list(_: argparse.Namespace) -> int:
    progress = load_progress()
    print(f"{'ID':<6}{'Status':<13}{'Tests':<9}Title")
    for lesson in LESSONS:
        record = progress.get(lesson.id)
        tests = f"{record['passed']}/{record['total']}" if record else "-"
        print(f"{lesson.id:<6}{status_label(record):<13}{tests:<9}{lesson.title}")
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    if args.lesson == "all":
        targets = list(LESSONS)
    elif args.lesson in LESSONS_BY_ID:
        targets = [LESSONS_BY_ID[args.lesson]]
    elif args.lesson.zfill(2) in LESSONS_BY_ID:  # accept "1" as "01"
        targets = [LESSONS_BY_ID[args.lesson.zfill(2)]]
    else:
        valid = ", ".join([*LESSONS_BY_ID, "all"])
        print(f"Unknown lesson '{args.lesson}'. Valid values: {valid}")
        return 2

    progress = load_progress()
    exit_code = 0
    for lesson in targets:
        print(f"\n=== Lesson {lesson.id}: {lesson.title} ===")
        record = run_lesson_tests(lesson)
        progress[lesson.id] = record
        save_progress(progress)
        if record["completed"]:
            print(f"\nLesson {lesson.id} completed ({record['passed']}/{record['total']} tests).")
        else:
            exit_code = 1
            print(
                f"\nLesson {lesson.id} not done yet ({record['passed']}/{record['total']} tests)."
            )
    return exit_code


def cmd_progress(_: argparse.Namespace) -> int:
    progress = load_progress()
    done = sum(1 for lesson in NUMBERED if progress.get(lesson.id, {}).get("completed"))
    bar = "#" * done + "." * (len(NUMBERED) - done)
    print(f"Lessons: {done}/{len(NUMBERED)}  [{bar}]")
    final_done = progress.get("final", {}).get("completed", False)
    print(f"Final project: {'completed' if final_done else 'pending'}")
    next_up = next((x for x in LESSONS if not progress.get(x.id, {}).get("completed")), None)
    if next_up is None:
        print("Everything is green. Tag it v1.0!")
    else:
        print(f"Next up: {next_up.id} - {next_up.title}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python Fundamentals course runner.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list lessons and their status").set_defaults(func=cmd_list)

    test = sub.add_parser("test", help="run the tests of a lesson")
    test.add_argument("lesson", help="lesson id (01..11), 'final', or 'all'")
    test.set_defaults(func=cmd_test)

    sub.add_parser("progress", help="show overall progress").set_defaults(func=cmd_progress)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
