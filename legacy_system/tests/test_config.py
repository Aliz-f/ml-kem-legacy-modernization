import pytest

from legacy_system.config import Config, ConfigurationError, FailureMode, load_config


def test_default_configuration() -> None:
    config = load_config({})

    assert config == Config(
        device_id="sensor-001",
        gateway_url="http://edge-gateway:8000",
        send_interval_seconds=5,
        request_timeout_seconds=3,
        max_retries=2,
        failure_mode=FailureMode.NONE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )


def test_valid_environment_configuration() -> None:
    config = load_config(
        {
            "DEVICE_ID": "sensor-007",
            "GATEWAY_URL": "https://gateway.example.test/api",
            "SEND_INTERVAL_SECONDS": "10",
            "REQUEST_TIMEOUT_SECONDS": "4",
            "MAX_RETRIES": "0",
            "FAILURE_MODE": "random",
            "FAILURE_RATE": "0.25",
            "FAILURE_SEED": "42",
            "LOG_LEVEL": "debug",
        }
    )

    assert config.device_id == "sensor-007"
    assert config.gateway_url == "https://gateway.example.test/api"
    assert config.send_interval_seconds == 10
    assert config.request_timeout_seconds == 4
    assert config.max_retries == 0
    assert config.failure_mode is FailureMode.RANDOM
    assert config.failure_rate == 0.25
    assert config.failure_seed == 42
    assert config.log_level == "DEBUG"


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("SEND_INTERVAL_SECONDS", "not-a-number"),
        ("REQUEST_TIMEOUT_SECONDS", "not-a-number"),
        ("MAX_RETRIES", "not-a-number"),
        ("FAILURE_RATE", "not-a-number"),
    ],
)
def test_invalid_numeric_values(name: str, value: str) -> None:
    with pytest.raises(ConfigurationError, match=name):
        load_config({name: value})


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("SEND_INTERVAL_SECONDS", "0"),
        ("SEND_INTERVAL_SECONDS", "-1"),
        ("REQUEST_TIMEOUT_SECONDS", "0"),
        ("REQUEST_TIMEOUT_SECONDS", "-1"),
        ("MAX_RETRIES", "-1"),
        ("FAILURE_RATE", "-0.001"),
        ("FAILURE_RATE", "1.001"),
    ],
)
def test_invalid_boundary_values(name: str, value: str) -> None:
    with pytest.raises(ConfigurationError, match=name):
        load_config({name: value})


def test_valid_boundary_values() -> None:
    config = load_config(
        {
            "SEND_INTERVAL_SECONDS": "1",
            "REQUEST_TIMEOUT_SECONDS": "1",
            "MAX_RETRIES": "0",
            "FAILURE_RATE": "1.0",
        }
    )

    assert config.failure_rate == 1.0


def test_empty_device_id() -> None:
    with pytest.raises(ConfigurationError, match="DEVICE_ID"):
        load_config({"DEVICE_ID": "  "})


def test_invalid_gateway_url() -> None:
    with pytest.raises(ConfigurationError, match="GATEWAY_URL"):
        load_config({"GATEWAY_URL": "gateway:8000"})


def test_unknown_failure_mode() -> None:
    with pytest.raises(ConfigurationError, match="FAILURE_MODE"):
        load_config({"FAILURE_MODE": "unrecognized"})


def test_invalid_log_level() -> None:
    with pytest.raises(ConfigurationError, match="LOG_LEVEL"):
        load_config({"LOG_LEVEL": "TRACE"})


def test_empty_failure_seed_is_none() -> None:
    assert load_config({"FAILURE_SEED": ""}).failure_seed is None


def test_failure_seed_is_integer() -> None:
    assert load_config({"FAILURE_SEED": "-17"}).failure_seed == -17


def test_invalid_failure_seed() -> None:
    with pytest.raises(ConfigurationError, match="FAILURE_SEED"):
        load_config({"FAILURE_SEED": "seed"})