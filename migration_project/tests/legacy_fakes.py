"""Test double for the legacy script's network and clock (shared by two test modules)."""

import json

import pytest

from legacy import sync_positions as legacy


class FakeHttp:
    """Replaces urllib.request.urlopen and time.sleep inside the legacy module."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, outcomes=None):
        self.outcomes = list(outcomes or [])  # ints (status) or Exceptions
        self.requests: list = []
        self.sleeps: list[float] = []
        monkeypatch.setattr(legacy.urllib.request, "urlopen", self._urlopen)
        monkeypatch.setattr(legacy.time, "sleep", self.sleeps.append)
        monkeypatch.setattr(legacy, "sent", 0)
        monkeypatch.setattr(legacy, "errors", 0)
        monkeypatch.setattr(legacy, "TOKEN", "secret")

    def _urlopen(self, req):
        self.requests.append(req)
        outcome = self.outcomes.pop(0) if self.outcomes else 200
        if isinstance(outcome, Exception):
            raise outcome
        return type("FakeResponse", (), {"status": outcome})()

    def bodies(self) -> list[list[dict]]:
        return [json.loads(r.data) for r in self.requests]
