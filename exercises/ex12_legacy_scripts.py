"""Exercise 12: reading legacy scripts.

Read lessons/12_reading_legacy_scripts.py first. The first four functions inspect Python
*source code given as a string* using the ``ast`` module (never ``exec`` or ``import`` it:
the script under inspection must not run). The last part turns hidden ``os.environ`` reads
into an explicit, testable configuration object.
Run the tests with:  python runner.py test 12
"""

from collections.abc import Mapping
from dataclasses import dataclass


def list_imports(source: str) -> list[str]:
    """Return the sorted, de-duplicated TOP-LEVEL module names the script imports.

    - ``import os.path``             -> "os"
    - ``from urllib.request import urlopen`` -> "urllib"
    - ``import numpy as np``         -> "numpy"
    - relative imports (``from . import x``, ``from .pkg import y``) are ignored.

    Imports nested inside functions or ``try`` blocks count too.
    A script with a syntax error raises ``SyntaxError`` (do not catch it).

    Example:
        "import os, sys\\nfrom os.path import join" -> ["os", "sys"]
    """
    raise NotImplementedError


def find_env_vars(source: str) -> list[str]:
    """Return the sorted, de-duplicated names of environment variables the script reads.

    Recognise these three forms, only when the name is a string literal:
        os.getenv("NAME")  /  os.getenv("NAME", default)
        os.environ.get("NAME")  /  os.environ.get("NAME", default)
        os.environ["NAME"]

    Dynamic names (``os.getenv(prefix + "X")``) are ignored.

    Example:
        'import os\\nA = os.getenv("API_URL")\\nB = os.environ["TOKEN"]' -> ["API_URL", "TOKEN"]
    """
    raise NotImplementedError


def find_risky_excepts(source: str) -> list[int]:
    """Return the sorted line numbers of ``except`` clauses that hide errors.

    A clause is risky when it is a bare ``except:`` OR when its body consists only of ``pass``.
    The line number is the line of the ``except`` keyword.

    ``except ValueError: raise`` and ``except OSError as e: log(e)`` are NOT risky.
    """
    raise NotImplementedError


def find_global_writes(source: str) -> list[str]:
    """Return the sorted, de-duplicated names declared with ``global`` inside any function.

    These are the module-level variables the script mutates: hidden shared state.

    Example:
        "def f():\\n    global count, last\\n    count += 1" -> ["count", "last"]
    """
    raise NotImplementedError


class ConfigError(Exception):
    """Invalid or missing configuration. Must derive from ``Exception``."""


@dataclass(frozen=True)
class Config:
    """Configuration of a job, built from environment variables.

    Fields (in order): ``api_url: str``, ``token: str``, ``timeout: float = 10.0``.
    """

    api_url: str
    token: str
    timeout: float = 10.0


def load_config(env: Mapping[str, str]) -> Config:
    """Build a ``Config`` from a mapping of environment variables (e.g. ``os.environ``).

    - ``API_URL`` and ``API_TOKEN`` are required; blank values (``""`` or only spaces) count as
      missing. If any are missing, raise ONE ``ConfigError`` whose message lists every missing
      name (so the operator fixes them all at once).
    - ``TIMEOUT_SECONDS`` is optional (default 10.0). It must parse as a float > 0, otherwise
      ``ConfigError`` mentioning ``TIMEOUT_SECONDS``.
    - Values are stripped of surrounding whitespace.

    The function must NOT read ``os.environ`` itself: that is what makes it testable.

    Example:
        load_config({"API_URL": "http://x", "API_TOKEN": "t"}) -> Config("http://x", "t", 10.0)
    """
    raise NotImplementedError
