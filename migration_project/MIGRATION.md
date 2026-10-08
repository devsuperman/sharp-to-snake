# Migration notes: `sync_positions.py` -> `positions_sync`

Fill this in as you go (step 3 of the README). It is the most valuable artifact of the
exercise: in a real migration this document is what the next person reads.

## 1. What the script does (in your own words)

<!-- 3-5 lines. Who runs it, when, with which input, what it produces. -->

## 2. Inventory (lesson 12 checklist)

| Aspect | Findings |
|---|---|
| Entry point | |
| Inputs (argv, env, files, network, clock) | |
| Outputs (API calls, prints, exit code) | |
| Hidden state (globals) | |
| Error policy (excepts, retries, sleeps) | |

## 3. Implicit business rules

Rules that no comment documents but the code enforces. Each one needs a test in the new code.

| # | Rule | Evidence (legacy test) | Kept in new code? |
|---|---|---|---|
| 1 | Timestamps are local time, converted to UTC by adding 3 hours | `test_load_converts_local_time...` | |
| 2 | | | |
| 3 | | | |

## 4. Bugs and risks found

For each: what happens, what the impact is, and the decision (**fix** / **keep** / **ask the
business**). A `test_BUG_*` test marks the likely candidates, but look for more.

| # | Problem | Impact | Decision | Why |
|---|---|---|---|---|
| 1 | The last partial batch is never sent | Up to 49 pings lost per run, silently | | |
| 2 | | | | |
| 3 | | | | |

## 5. Mapping to C# / .NET

How each piece would be built in the real job. Fill the right-hand column.

| Python (legacy) | Python (new) | C# / .NET equivalent |
|---|---|---|
| `os.environ.get` at import | `load_config(env)` | `IConfiguration` + `IOptions<T>` |
| `csv.DictReader` + dict rows | `read_rows` + `Ping` dataclass | |
| `datetime.strptime` + 3 hours | `zoneinfo` conversion | |
| `urllib` + `time.sleep(1)` loop | retry with backoff + idempotency key | |
| `print` + `sys.exit(0)` | summary line + exit code | |
| scheduled by cron (assumed) | | |

## 6. Decisions that changed behaviour on purpose

List every place where the new code is intentionally *different* (the parity tests assert them).

## 7. Cut-over plan

1. **Parallel run:** how would you run old and new on the same input? What do you compare?
2. **Monitoring:** which metrics and alerts tell you the new job is healthy (CloudWatch)?
3. **Rollback:** how do you go back if the new job misbehaves?
4. **Idempotency:** what stops a re-run from creating duplicates?
5. **Retirement:** when is it safe to delete the old script?
