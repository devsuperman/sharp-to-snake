"""Reading GPS tracks from disk (lessons 05 and 08)."""

from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from gps.models import Position


def parse_timestamp(text: str) -> datetime:
    """Parse an ISO 8601 timestamp such as ``2024-05-01T08:00:00`` (``datetime.fromisoformat``)."""
    raise NotImplementedError


def iter_positions_csv(path: Path) -> Iterator[Position]:
    """Lazily yield positions from a CSV file with the header ``timestamp,lat,lon``.

    - Must be a generator that reads the file line by line (works on huge files).
    - A missing file raises ``FileNotFoundError`` (when iteration starts).
    - A header without all three columns raises ``MalformedRecordError(1, ...)``.
    - A data row with a missing value, a non-numeric lat/lon or an unparsable timestamp raises
      ``MalformedRecordError(<file line number>, ...)``; the header is line 1, so the first data
      row is line 2. Chain the original error with ``raise ... from err``.
      (Tip: ``reader.line_num``.)
    - Out-of-range coordinates raise ``InvalidPositionError`` (it comes from ``Position``).
    """
    raise NotImplementedError


def load_positions_json(path: Path) -> list[Position]:
    """Load positions from a JSON file: a list of ``{"timestamp", "lat", "lon"}`` objects.

    Unlike CSV this loads the whole file (JSON cannot be streamed with the stdlib).
    A bad item raises ``MalformedRecordError(<1-based item index>, ...)``; a document that
    is not a list also raises ``MalformedRecordError(0, ...)``.
    """
    raise NotImplementedError


def iter_positions(path: Path) -> Iterator[Position]:
    """Dispatch on the file suffix: ``.csv`` -> lazy CSV reader, ``.json`` -> JSON loader.

    Any other suffix raises ``ValueError`` (when iteration starts).
    """
    raise NotImplementedError
