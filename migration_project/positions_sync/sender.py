"""Uploading pings in batches, with the reliability the legacy script lacked (lesson 14)."""

import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from course_support.rest_types import HttpClient
from positions_sync.config import Config
from positions_sync.models import Ping


@dataclass
class SendReport:
    """Fields (all ``int``, default 0): ``sent`` (pings delivered), ``batches_ok``,
    ``batches_failed``."""

    sent: int = 0
    batches_ok: int = 0
    batches_failed: int = 0


def send_pings(
    client: HttpClient,
    config: Config,
    pings: Iterable[Ping],
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> SendReport:
    """POST the pings to ``config.api_url`` in batches of ``config.batch_size``.

    Differences from the legacy script (all deliberate fixes, see MIGRATION.md):
    - the LAST partial batch is sent too (legacy silently dropped it);
    - any 2xx status is a success (legacy accepted only 200 and resent the batch on 201);
    - transient failures are retried with exponential backoff, ``config.retries`` times;
    - each batch carries an ``Idempotency-Key`` (identical on every retry of that batch), so a
      retried POST cannot create duplicates.

    Kept from the legacy script:
    - the body is the JSON list of ``ping.to_payload()``;
    - the header is ``Authorization: Token <token>`` (NOT "Bearer");
    - a batch that still fails after the retries does not stop the run: count it in
      ``batches_failed`` and continue with the next one.

    Hint: ``build_headers``, ``post_idempotent`` and ``chunked`` from your exercises 13 and 14
    do almost all the work.
    """
    raise NotImplementedError
