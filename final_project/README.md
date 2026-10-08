# Final project: GPS fleet tracker

A small command-line tool that reads a GPS track (CSV or JSON), then reports total distance,
duration, average speed and the places where the vehicle stopped.

It uses everything from the course, in a domain you already know:

| Module | Lesson it exercises |
|---|---|
| `gps/errors.py` | 07: custom exception hierarchy |
| `gps/models.py` | 06: dataclasses, properties, validation in `__post_init__` |
| `gps/geo.py` | 03/05: pure functions, generators (`iter_segments`) |
| `gps/readers.py` | 05/08: lazy CSV reading, JSON, `pathlib`, error handling |
| `gps/analysis.py` | 04/05: single-pass stream processing, stop detection |
| `gps/cli.py`, `gps/__main__.py` | 09: `argparse`, `python -m gps` |
| everything | 11: full type hints (`mypy --strict final_project/gps`) |

## What to do

Every module under `gps/` contains documented stubs (`raise NotImplementedError`); the dataclass
fields in `models.py` are already declared, so only their behaviour is left to you. Implement
them one module at a time, in the order of the table above, and run the matching tests:

```bash
pytest final_project/tests/test_gps_models.py -q
pytest final_project/tests/test_gps_geo.py -q
...
python runner.py test final        # everything, recorded in progress.json
```

Then try the real thing (from the `final_project/` directory):

```bash
cd final_project
python -m gps summary data/sample_trip.csv
python -m gps summary data/sample_trip.csv --json
```

## Data format

CSV with a header line and ISO 8601 timestamps:

```
timestamp,lat,lon
2024-05-01T08:00:00,-23.550500,-46.633300
2024-05-01T08:01:00,-23.545500,-46.633300
```

JSON is a list of objects with the same three keys.

`data/sample_trip.csv` is a 30-minute trip: 10 minutes of driving, an 8-minute stop, then
12 more minutes of driving (about 12.2 km in total).

## Ideas for later (optional, small steps)

- Expose the summary through FastAPI.
- Store tracks in SQLite.
- Draw the route on a map with `folium`.
