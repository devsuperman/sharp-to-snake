# Part 2 project: migrate a legacy sync script

The scenario of the job you are preparing for: *a Python script nobody understands is critical
to the business, and it must be re-implemented properly* (in the job, in C#/.NET; here, as a
clean Python package, because the **method** is the skill being trained).

The script is [`legacy/sync_positions.py`](legacy/sync_positions.py): it reads a CSV of raw
GPS tracker pings and uploads them to a tracking API. It "works", but it hides business rules,
swallows errors and loses data. Your job is **not** to translate it line by line.

## The method (follow it in order)

| Step | What you do | Where |
|---|---|---|
| 1. Read | Use the checklist from lesson 12: entry point, inputs, outputs, hidden state, error policy, implicit rules. | `legacy/sync_positions.py` |
| 2. Pin | Read the characterization tests: they record what the script really does today, bugs included (`test_BUG_*`). They already pass; never edit them to make something pass. | `tests/test_legacy_characterization.py` |
| 3. Document | Fill in `MIGRATION.md`: every implicit rule, every bug, and for each bug whether you **keep** or **fix** it, and why. | `MIGRATION.md` |
| 4. Re-implement | Fill the stubs in `positions_sync/`, one module at a time (order below). | `positions_sync/` |
| 5. Compare | The parity tests run old and new code on the same input and assert what is identical and what changed on purpose. | `tests/test_pos_parity.py` |
| 6. Cut over | Plan how you would put it in production (parallel run, comparison, monitoring, rollback). | `MIGRATION.md`, last section |

## Implementation order

```bash
pytest migration_project/tests/test_pos_models_config.py -q   # models.py, config.py
pytest migration_project/tests/test_pos_cleaning.py -q        # cleaning.py
pytest migration_project/tests/test_pos_sender.py -q          # sender.py (reuse ex13/ex14)
pytest migration_project/tests/test_pos_cli.py -q             # cli.py
pytest migration_project/tests/test_pos_parity.py -q          # old vs new
python runner.py test migration                               # everything, recorded
```

| Module | Skills from |
|---|---|
| `positions_sync/models.py` | 06: frozen dataclass |
| `positions_sync/config.py` | 12: explicit configuration instead of hidden `os.environ` reads |
| `positions_sync/cleaning.py` | 05/08/13: streaming CSV, time zones, business rules, a report of what was dropped |
| `positions_sync/sender.py` | 13/14: batching, auth header, retry with backoff, idempotency keys |
| `positions_sync/cli.py` | 09/12: `argparse`, injected dependencies, meaningful exit codes |

`sender.py` is meant to **reuse your own solutions** from exercises 13 and 14, so finish those
lessons first.

## Running the real thing

The cleaning step works offline. Sending needs an API; to try it without one, start a tiny
local server (any server that answers `201` to `POST` will do) and point the script at it:

```bash
export TRACKING_TOKEN=secret
export TRACKING_API=http://127.0.0.1:8080/api/positions
PYTHONPATH=migration_project python -m positions_sync migration_project/data/raw_pings.csv
# read=123 kept=115 skipped=8 sent=115 failed_batches=0
```

The old script, for comparison (it sends 100 of the 115 pings and always exits with 0):

```bash
cd migration_project && python legacy/sync_positions.py data/raw_pings.csv
```

## Data

`data/raw_pings.csv` has 123 rows from 3 trackers: 115 are valid. The rest are traps on
purpose: a ping at 0,0, speeds of 250 and 200.1 km/h, an unparseable latitude, a bad timestamp,
a blank speed, and duplicates (one with a different device-id spelling).

## Ground rules

- Do not edit anything under `legacy/` or the characterization tests.
- Python only needs to *read* the legacy file: treat `positions_sync/` as the "C# side" and
  keep its design clean (small functions, explicit dependencies, no global state).
