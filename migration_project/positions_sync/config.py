"""Explicit configuration (lesson 12): no hidden ``os.environ`` reads, no silent failures."""

from collections.abc import Mapping
from dataclasses import dataclass

DEFAULT_API_URL = "http://localhost:8080/api/positions"
BATCH_SIZE = 50
RETRIES = 3


class ConfigError(Exception):
    """Missing or invalid configuration. Must derive from ``Exception``."""


@dataclass(frozen=True)
class Config:
    """Fields (in order): ``api_url: str``, ``token: str``, ``batch_size: int = BATCH_SIZE``,
    ``retries: int = RETRIES``."""

    api_url: str
    token: str
    batch_size: int = BATCH_SIZE
    retries: int = RETRIES


def load_config(env: Mapping[str, str]) -> Config:
    """Build a ``Config`` from environment variables.

    - ``TRACKING_API``: optional, defaults to ``DEFAULT_API_URL``.
    - ``TRACKING_TOKEN``: REQUIRED. The legacy script did not check it and failed silently on
      every request; here a missing or blank token raises ``ConfigError`` mentioning the name.
    - Values are stripped. ``batch_size`` and ``retries`` keep their defaults.
    """
    raise NotImplementedError
