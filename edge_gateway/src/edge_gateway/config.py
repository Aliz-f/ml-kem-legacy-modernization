"""Centralized runtime configuration for the Edge Gateway.

Only this module reads Gateway environment variables. Application and
transport code receive a :class:`GatewayConfig` instance instead of reading
``os.environ`` themselves.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math
import os
from urllib.parse import urlparse


DEFAULTS: dict[str, str] = {
    "GATEWAY_ID": "gateway-001",
    "HOST": "0.0.0.0",
    "PORT": "8000",
    "CLOUD_URL": "http://cloud-service:9000",
    "CLOUD_TIMEOUT_SECONDS": "3",
    "CLOUD_MAX_RETRIES": "2",
    "SECURITY_MODE": "classical",
    "SESSION_TTL_SECONDS": "300",
    "PQC_FAILURE_POLICY": "fail_closed",
    "FAILURE_MODE": "none",
    "FAILURE_RATE": "0.0",
    "FAILURE_SEED": "",
    "LOG_LEVEL": "INFO",
}

SECURITY_MODES = frozenset({"classical", "mlkem"})
PQC_FAILURE_POLICIES = frozenset({"fail_closed"})
KNOWN_FAILURE_MODES = frozenset(
    {
        "none",
        "processing_error",
        "processing_delay",
        "cloud_timeout",
        "cloud_unavailable",
        "drop_message",
        "random",
        "mlkem_handshake_failure",
        "corrupt_ciphertext",
        "session_missing",
        "session_expired",
    }
)


class ConfigurationError(ValueError):
    """Raised when Gateway configuration cannot safely be used."""


@dataclass(frozen=True, slots=True)
class GatewayConfig:
    """Validated configuration shared by Gateway application components."""

    gateway_id: str
    host: str
    port: int
    cloud_url: str
    cloud_timeout_seconds: float
    cloud_max_retries: int
    security_mode: str
    session_ttl_seconds: int
    pqc_failure_policy: str
    failure_mode: str
    failure_rate: float
    failure_seed: str | None
    log_level: str


def load_config(environ: Mapping[str, str] | None = None) -> GatewayConfig:
    """Load and validate all Gateway configuration values once.

    ``environ`` makes configuration deterministic in tests. Production code
    should call this function without arguments during application startup.
    """

    source = os.environ if environ is None else environ

    gateway_id = _required_text(source, "GATEWAY_ID")
    host = _required_text(source, "HOST")
    cloud_url = _valid_cloud_url(_required_text(source, "CLOUD_URL"))
    security_mode = _allowed_value(source, "SECURITY_MODE", SECURITY_MODES)
    pqc_failure_policy = _allowed_value(
        source, "PQC_FAILURE_POLICY", PQC_FAILURE_POLICIES
    )
    failure_mode = _allowed_value(source, "FAILURE_MODE", KNOWN_FAILURE_MODES)
    failure_seed = _value(source, "FAILURE_SEED").strip() or None

    return GatewayConfig(
        gateway_id=gateway_id,
        host=host,
        port=_positive_int(source, "PORT", minimum=1, maximum=65_535),
        cloud_url=cloud_url,
        cloud_timeout_seconds=_positive_float(source, "CLOUD_TIMEOUT_SECONDS"),
        cloud_max_retries=_non_negative_int(source, "CLOUD_MAX_RETRIES"),
        security_mode=security_mode,
        session_ttl_seconds=_positive_int(source, "SESSION_TTL_SECONDS", minimum=1),
        pqc_failure_policy=pqc_failure_policy,
        failure_mode=failure_mode,
        failure_rate=_failure_rate(source),
        failure_seed=failure_seed,
        log_level=_required_text(source, "LOG_LEVEL"),
    )


def _value(environ: Mapping[str, str], name: str) -> str:
    return environ.get(name, DEFAULTS[name])


def _required_text(environ: Mapping[str, str], name: str) -> str:
    value = _value(environ, name).strip()
    if not value:
        raise ConfigurationError(f"{name} must be non-empty")
    return value


def _positive_int(
    environ: Mapping[str, str], name: str, *, minimum: int, maximum: int | None = None
) -> int:
    value = _integer(environ, name)
    if value < minimum or (maximum is not None and value > maximum):
        range_description = f"between {minimum} and {maximum}" if maximum else f">= {minimum}"
        raise ConfigurationError(f"{name} must be {range_description}")
    return value


def _non_negative_int(environ: Mapping[str, str], name: str) -> int:
    value = _integer(environ, name)
    if value < 0:
        raise ConfigurationError(f"{name} must be >= 0")
    return value


def _integer(environ: Mapping[str, str], name: str) -> int:
    try:
        return int(_value(environ, name))
    except ValueError as error:
        raise ConfigurationError(f"{name} must be an integer") from error


def _positive_float(environ: Mapping[str, str], name: str) -> float:
    try:
        value = float(_value(environ, name))
    except ValueError as error:
        raise ConfigurationError(f"{name} must be a number") from error
    if not math.isfinite(value) or value <= 0:
        raise ConfigurationError(f"{name} must be > 0")
    return value


def _allowed_value(
    environ: Mapping[str, str], name: str, allowed_values: frozenset[str]
) -> str:
    value = _required_text(environ, name)
    if value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        raise ConfigurationError(f"{name} must be one of: {allowed}")
    return value


def _valid_cloud_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ConfigurationError("CLOUD_URL must be an absolute HTTP(S) URL")
    try:
        parsed.port
    except ValueError as error:
        raise ConfigurationError("CLOUD_URL must include a valid port when specified") from error
    return value


def _failure_rate(environ: Mapping[str, str]) -> float:
    try:
        value = float(_value(environ, "FAILURE_RATE"))
    except ValueError as error:
        raise ConfigurationError("FAILURE_RATE must be a number") from error
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ConfigurationError("FAILURE_RATE must be between 0.0 and 1.0")
    return value
