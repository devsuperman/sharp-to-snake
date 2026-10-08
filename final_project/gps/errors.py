"""Custom exceptions (lesson 07).

Replace each placeholder class with a real exception following this hierarchy:

    GpsError(Exception)                 base class for every error raised by this package
    ├── InvalidPositionError            latitude/longitude out of range
    ├── MalformedRecordError            a CSV/JSON record cannot be parsed; keeps ``line_number``
    │                                    and ``str(exc)`` mentions the line, e.g. "line 7: bad lat"
    ├── OutOfOrderError                 timestamps do not strictly increase
    └── NotEnoughDataError              fewer than 2 positions to analyse

``MalformedRecordError(line_number: int, message: str)`` must expose ``.line_number``.
"""


class GpsError:
    """Base class of all package errors."""


class InvalidPositionError:
    """Latitude or longitude outside the valid range."""


class MalformedRecordError:
    """A record in the input file could not be parsed."""


class OutOfOrderError:
    """Consecutive positions whose timestamps do not strictly increase."""


class NotEnoughDataError:
    """Fewer than two positions were provided."""
