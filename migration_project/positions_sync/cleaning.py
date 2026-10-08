"""Reading and cleaning raw tracker pings: this is where the legacy business rules live."""

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from positions_sync.models import Ping

SOURCE_TIMEZONE = "America/Sao_Paulo"  # trackers report local time (legacy: "+3 hours")
MAX_SPEED_KMH = 200.0


@dataclass
class CleaningReport:
    """What happened to the input rows. Every row ends in exactly one bucket, so
    ``total == kept + invalid + null_island + too_fast + duplicates``.

    Fields (all ``int``, default 0): ``total``, ``kept``, ``invalid``, ``null_island``,
    ``too_fast``, ``duplicates``.
    """

    total: int = 0
    kept: int = 0
    invalid: int = 0
    null_island: int = 0
    too_fast: int = 0
    duplicates: int = 0


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    """Lazily yield the rows of a CSV file with a header line (UTF-8, ``newline=""``).

    The file is opened when iteration starts; a missing file then raises ``FileNotFoundError``.
    Must stream: never load the whole file into memory.
    """
    raise NotImplementedError


def parse_local_timestamp(text: str) -> datetime:
    """Parse a tracker timestamp ``"dd/mm/YYYY HH:MM:SS"`` (local time in ``SOURCE_TIMEZONE``)
    into an AWARE datetime in UTC. Invalid text raises ``ValueError``.

    Use ``zoneinfo`` instead of the legacy hard-coded ``+3 hours`` so the code survives a change
    of the offset. (Your ``parse_timestamp`` from exercise 13 is a good starting point.)

    Example:
        "01/05/2024 08:00:00" -> datetime(2024, 5, 1, 11, 0, tzinfo=UTC)
    """
    raise NotImplementedError


def clean_rows(rows: Iterable[Mapping[str, str]]) -> tuple[list[Ping], CleaningReport]:
    """Apply the legacy rules to raw CSV rows and report what was dropped.

    Columns: ``device_id``, ``timestamp``, ``lat``, ``lon``, ``speed_kmh``. Rules, checked IN
    THIS ORDER (the first one that applies decides the bucket of the row):

    1. ``invalid``      any of lat/lon/speed is not a number, or the timestamp does not parse
                        (a missing column also counts as invalid).
    2. ``null_island``  lat == 0 AND lon == 0 (a tracker without a GPS fix).
    3. ``too_fast``     speed > 200 km/h (exactly 200 is kept; negative speeds are kept).
    4. ``duplicates``   same (device, instant) as a row already KEPT: the first one wins.
                        Device ids are compared after ``strip().upper()``.

    Order of the returned pings = order of the input. Rows dropped by rules 1-3 never "reserve"
    their key, so a later valid row with the same key is kept.

    Improvement over the legacy script (decision to record in MIGRATION.md): duplicates are
    detected on the parsed INSTANT, not on the raw text, so "1/5/2024 08:00:00" and
    "01/05/2024 08:00:00" are the same ping.
    """
    raise NotImplementedError
