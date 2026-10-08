# sharp-to-snake: Python Fundamentals, an Executable Course

A hands-on Python course for experienced C#/.NET developers. Each lesson explains one concept
(with a "C# equivalent" section), gives you an exercise file full of stubs, and ships automated
tests that tell you whether your implementation is right.

See [PLAN.md](PLAN.md) for the full plan and curriculum.

## Setup

Requires Python 3.12 or newer.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## How a lesson works

1. **Read** `lessons/NN_topic.py`. Run it (`python lessons/NN_topic.py`) to see the demos.
2. **Implement** the stubs in `exercises/exNN_topic.py` (they raise `NotImplementedError`).
3. **Test** with the runner: `python runner.py test NN`
4. **Check progress**: `python runner.py progress`

## Runner commands

| Command | What it does |
|---|---|
| `python runner.py list` | Lists lessons with their status (pending / completed) |
| `python runner.py test 01` | Runs the tests of lesson 01 and records the result |
| `python runner.py test final` | Runs the tests of the final GPS project |
| `python runner.py test all` | Runs every lesson, one after another |
| `python runner.py progress` | Shows overall progress |

A lesson counts as **completed** only when all of its tests pass. Results are stored in
`progress.json`.

## Lessons

| # | Topic |
|---|---|
| 01 | Types and variables |
| 02 | Control flow |
| 03 | Functions |
| 04 | Collections |
| 05 | Comprehensions and iteration |
| 06 | Classes and dataclasses |
| 07 | Exceptions |
| 08 | Files and JSON |
| 09 | Modules and packages |
| 10 | Async basics |
| 11 | Type hints |
| final | GPS / fleet mini-project (`final_project/`) |

## Ground rules

- Never look at a solution before trying. Stuck for more than 30 minutes? Write the question
  in `NOTES.md`, move on, and come back later.
- Run `ruff check .` and `ruff format .` before each commit.
- Keep a short learning diary in [NOTES.md](NOTES.md).

## Running tests directly

```bash
pytest tests/test_ex03_functions.py -q   # one exercise
pytest -q                                # everything (stubs fail until you implement them)
```
