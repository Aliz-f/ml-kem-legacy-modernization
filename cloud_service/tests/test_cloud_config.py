"""M4-01 environment boundaries and safe validation failures."""

import traceback

import pytest

from cloud_service.config import Config, ConfigurationError, FailureMode, SecurityMode, load_config


def test_defaults_do_not_create_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_config({}) == Config(
        cloud_id="cloud-001", host="0.0.0.0", port=9000,
        database_url="sqlite:///cloud.db", security_mode=SecurityMode.CLASSICAL,
        session_ttl_seconds=300, failure_mode=FailureMode.NONE,
        failure_rate=0.0, failure_seed=None, failure_delay_seconds=2.0,
        log_level="INFO",
    )
    assert list(tmp_path.iterdir()) == []


def test_custom_environment():
    config = Config.from_env({
        "CLOUD_ID": "cloud-test", "HOST": "127.0.0.1", "PORT": "9100",
        "DATABASE_URL": "sqlite:///:memory:", "SECURITY_MODE": "mlkem",
        "SESSION_TTL_SECONDS": "300", "FAILURE_MODE": "processing_delay",
        "FAILURE_RATE": "0.25", "FAILURE_SEED": "-42",
        "FAILURE_DELAY_SECONDS": "0.5", "LOG_LEVEL": "debug",
    })
    assert config == Config(
        cloud_id="cloud-test", host="127.0.0.1", port=9100,
        database_url="sqlite:///:memory:", security_mode=SecurityMode.MLKEM,
        session_ttl_seconds=300, failure_mode=FailureMode.PROCESSING_DELAY,
        failure_rate=0.25, failure_seed=-42, failure_delay_seconds=0.5,
        log_level="DEBUG",
    )


def test_process_environment_and_explicit_mapping(monkeypatch):
    monkeypatch.setenv("CLOUD_ID", "process-cloud")
    assert load_config().cloud_id == "process-cloud"
    assert load_config({}).cloud_id == "cloud-001"


@pytest.mark.parametrize(("name", "values"), [
    ("CLOUD_ID", ["", "  "]),
    ("HOST", ["", "  "]),
    ("PORT", ["0", "-1", "65536", "1.5", "invalid", ""]),
    ("SESSION_TTL_SECONDS", ["0", "-1", "301", "60", "invalid", ""]),
    ("SECURITY_MODE", ["unknown", "", "MLKEM"]),
    ("FAILURE_MODE", ["unknown", "invalid_temperature", ""]),
    ("FAILURE_RATE", ["-0.01", "1.01", "nan", "inf", "-inf", "invalid", ""]),
    ("FAILURE_DELAY_SECONDS", ["-0.01", "nan", "inf", "invalid", ""]),
    ("FAILURE_SEED", ["1.5", "invalid"]),
    ("LOG_LEVEL", ["TRACE", ""]),
])
def test_invalid_configuration(name, values):
    for value in values:
        with pytest.raises(ConfigurationError, match=name):
            load_config({name: value})


@pytest.mark.parametrize("url", [
    "", "sqlite://", "sqlite:///", "sqlite:////", "postgresql://host/db",
    "sqlite://host/db", "sqlite:///folder/", "sqlite:///.", "sqlite:///..",
    "sqlite:///db?mode=ro", "sqlite:///db#fragment", "sqlite:///db\x00file",
])
def test_invalid_database_url(url):
    with pytest.raises(ConfigurationError, match="DATABASE_URL"):
        load_config({"DATABASE_URL": url})


@pytest.mark.parametrize("url", [
    "sqlite:///measurements.db", "sqlite:///data/cloud.db",
    "sqlite:////tmp/cloud.db", "sqlite:///C:/data/cloud.db", "sqlite:///:memory:",
])
def test_sqlite_paths(url):
    assert load_config({"DATABASE_URL": url}).database_url == url


@pytest.mark.parametrize("mode", list(FailureMode))
def test_supported_cloud_failure_modes(mode):
    assert load_config({"FAILURE_MODE": mode.value}).failure_mode is mode


@pytest.mark.parametrize("port", [1, 65535])
@pytest.mark.parametrize("rate", [0.0, 1.0])
def test_inclusive_boundaries(port, rate):
    config = load_config({"PORT": str(port), "FAILURE_RATE": str(rate),
                          "FAILURE_DELAY_SECONDS": "0", "FAILURE_SEED": " "})
    assert config.port == port
    assert config.failure_rate == rate
    assert config.failure_delay_seconds == 0
    assert config.failure_seed is None


@pytest.mark.parametrize("name", ["DATABASE_URL", "PORT", "FAILURE_MODE", "SECURITY_MODE"])
def test_errors_do_not_echo_invalid_values(name, caplog):
    marker = "invalid-config-marker"
    with pytest.raises(ConfigurationError) as error:
        load_config({name: marker})
    assert marker not in "".join(traceback.format_exception(error.value))
    assert caplog.text == ""
