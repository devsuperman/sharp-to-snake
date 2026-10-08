"""Command-line interface (lesson 09): ``python -m gps summary FILE``."""


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return the process exit code.

    Command: ``summary FILE [--json] [--stop-minutes N] [--stop-speed KMH]``
      --json            print ``Summary.to_dict()`` as indented JSON instead of text
      --stop-minutes N  minimum stop duration (default 5)
      --stop-speed KMH  maximum speed that still counts as stopped (default 1.0)

    Text output (exact labels matter):
        File: <path as given>
        Distance: 12.23 km
        Duration: 0:30:00
        Average speed: 24.46 km/h
        Stops: 1
          1. 08:10:00 -> 08:18:00 (0:08:00) at -23.50050, -46.63330

    Errors (``GpsError`` subclasses, a missing file, or an unsupported suffix) are reported on
    stderr as ``error: <message>`` and the exit code is 1. Success returns 0.
    Use ``argparse`` with a sub-command; ``argv=None`` means ``sys.argv[1:]``.
    """
    raise NotImplementedError
