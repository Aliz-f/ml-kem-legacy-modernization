from __future__ import annotations

import pytest

from edge_gateway.config import ConfigurationError, load_config


def test_load_config_uses_documented_defaults() -> None:
    config = load_config({})

    assert config.gateway_id == "gateway-001"
    assert config.host == "0.0.0.0"
    assert config.port == 8000
    assert config.cloud_url == "http://cloud-service:9000"
    assert config.cloud_timeout_seconds == 3.0
    assert config.cloud_max_retries == 2
    assert config.security_mode == "classical"
    assert config.session_ttl_seconds == 300
    assert config.pqc_failure_policy == "fail_closed"
    assert config.failure_mode == "none"
    assert config.failure_rate == 0.0
    assert config.failure_seed is None
    assert config.log_level == "INFO"


def test_load_config_uses_custom_environment_values() -> None:
    config = load_config(
        {
            "GATEWAY_ID": "gateway-test",
            "HOST": "127.0.0.1",
            "PORT": "8080",
            "CLOUD_URL": "https://cloud.example.test:9443",
            "CLOUD_TIMEOUT_SECONDS": "1.5",
            "CLOUD_MAX_RETRIES": "0",
            "SECURITY_MODE": "mlkem",
            "SESSION_TTL_SECONDS": "120",
            "PQC_FAILURE_POLICY": "fail_closed",
            "FAILURE_MODE": "session_expired",
            "FAILURE_RATE": "0.25",
            "FAILURE_SEED": "gateway-demo",
            "LOG_LEVEL": "DEBUG",
        }
    )

    assert config.gateway_id == "gateway-test"
    assert config.host == "127.0.0.1"
    assert config.port == 8080
    assert config.cloud_url == "https://cloud.example.test:9443"
    assert config.cloud_timeout_seconds == 1.5
    assert config.cloud_max_retries == 0
    assert config.security_mode == "mlkem"
    assert config.session_ttl_seconds == 120
    assert config.pqc_failure_policy == "fail_closed"
    assert config.failure_mode == "session_expired"
    assert config.failure_rate == 0.25
    assert config.failure_seed == "gateway-demo"
    assert config.log_level == "DEBUG"


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("GATEWAY_ID", ""),
        ("PORT", "0"),
        ("PORT", "65536"),
        ("PORT", "not-a-port"),
        ("CLOUD_URL", "not-a-url"),
        ("CLOUD_TIMEOUT_SECONDS", "-1"),
        ("CLOUD_MAX_RETRIES", "-1"),
        ("SECURITY_MODE", "plaintext"),
        ("SESSION_TTL_SECONDS", "0"),
        ("PQC_FAILURE_POLICY", "fallback"),
        ("FAILURE_RATE", "1.01"),
        ("FAILURE_RATE", "not-a-rate"),
        ("FAILURE_MODE", "unknown_failure"),
    ],
)
def test_load_config_rejects_invalid_values(name: str, value: str) -> None:
    with pytest.raises(ConfigurationError, match=name):
        load_config({name: value})
