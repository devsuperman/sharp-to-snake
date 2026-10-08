from datetime import UTC, datetime

import pytest

from positions_sync.config import (
    BATCH_SIZE,
    DEFAULT_API_URL,
    RETRIES,
    Config,
    ConfigError,
    load_config,
)
from positions_sync.models import Ping


def test_ping_is_frozen_dataclass_with_ordered_fields():
    ping = Ping("AB-12", datetime(2024, 5, 1, 11, 0, tzinfo=UTC), -23.55, -46.63, 40.0)
    assert ping.device_id == "AB-12" and ping.speed_kmh == 40.0
    with pytest.raises(AttributeError):
        ping.lat = 0.0  # type: ignore[misc]


def test_ping_to_payload_matches_legacy_shape():
    ping = Ping("AB-12", datetime(2024, 5, 1, 11, 0, tzinfo=UTC), -23.55, -46.63, 40.0)
    assert ping.to_payload() == {
        "device": "AB-12",
        "ts": "2024-05-01T11:00:00Z",
        "lat": -23.55,
        "lon": -46.63,
        "speed": 40.0,
    }


def test_load_config_defaults():
    config = load_config({"TRACKING_TOKEN": "secret"})
    assert config == Config(DEFAULT_API_URL, "secret", BATCH_SIZE, RETRIES)
    assert (config.batch_size, config.retries) == (50, 3)


def test_load_config_overrides_and_strips():
    config = load_config({"TRACKING_API": " http://prod/api ", "TRACKING_TOKEN": " t "})
    assert (config.api_url, config.token) == ("http://prod/api", "t")


@pytest.mark.parametrize("env", [{}, {"TRACKING_TOKEN": ""}, {"TRACKING_TOKEN": "   "}])
def test_load_config_requires_a_token(env):
    with pytest.raises(ConfigError, match="TRACKING_TOKEN"):
        load_config(env)


def test_config_error_is_an_exception():
    assert issubclass(ConfigError, Exception)
