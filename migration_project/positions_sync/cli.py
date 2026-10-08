"""Command-line entry point: wires reading, cleaning and sending together."""

import time
from collections.abc import Callable, Mapping, Sequence

from course_support.rest_types import HttpClient


def main(
    argv: Sequence[str],
    env: Mapping[str, str],
    client: HttpClient,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Run the sync and return the process exit code. Never calls ``sys.exit`` or reads
    ``os.environ`` itself (``argv``, ``env`` and ``client`` are injected so it can be tested).

    ``argv`` holds exactly one positional argument: the path of the CSV file (use ``argparse``;
    for a wrong command line argparse exits with code 2, which is fine).

    1. Load the config from ``env``. A ``ConfigError`` prints ``error: <message>`` to STDERR and
       returns 2.
    2. A missing input file prints ``error: file not found: <path>`` to STDERR and returns 2.
       Nothing must be sent in that case.
    3. Otherwise read, clean and send, then print ONE line to STDOUT:
           ``read=<total> kept=<kept> skipped=<total-kept> sent=<sent> failed_batches=<n>``
       and return 0 if no batch failed, else 1 (the legacy script always exited 0).
    """
    raise NotImplementedError
