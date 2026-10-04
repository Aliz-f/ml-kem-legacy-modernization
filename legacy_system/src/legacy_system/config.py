"""Validated runtime configuration for the Legacy Device."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
import math
import os
from urllib.parse import urlparse


class ConfigurationError(ValueError):
    """Raised when the Legacy Device configuration is invalid."""


class FailureMode(StrEnum):
    """Failure modes supported by the Legacy Device contract."""

    NONE = "none"
    INVALID_TEMPERATURE = "invalid_temperature"
    INVALID_HUMIDITY = "invalid_humidity"
    MISSING_FIELD = "missing_field"
    INVALID_TIMESTAMP = "invalid_timestamp"
    DUPLICATE_SEQUENCE = "duplicate_sequence"
    OUT_OF_ORDER_SEQUENCE = "out_of_order_sequence"
    RANDOM = "random"


@dataclass(frozen=True, slots=True)
class Config:
    """Validated settings used by the Legacy Device."""

    device_id: str
    gateway_url: str
    send_interval_seconds: float
    request_timeout_seconds: float
    max_retries: int
    failure_mode: FailureMode
    failure_rate: float
    failure_seed: int | None
    log_level: str

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Config":
        """Build configuration from an injectable environment mapping."""
        return load_config(environ)


_DEFAULTS = {
    "DEVICE_ID": "sensor-001",
    "GATEWAY_URL": "http://edge-gateway:8000",
    "SEND_INTERVAL_SECONDS": "5",
    "REQUEST_TIMEOUT_SECONDS": "3",
    "MAX_RETRIES": "2",
    "FAILURE_MODE": FailureMode.NONE.value,
    "FAILURE_RATE": "0.0",
    "FAILURE_SEED": "",
    "LOG_LEVEL": "INFO",
}
_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


def load_config(environ: Mapping[str, str] | None = None) -> Config:
    """Read, parse, and validate Legacy Device settings."""
    environment = os.environ if environ is None else environ

    device_id = _required_text(environment, "DEVICE_ID")
    gateway_url = _required_text(environment, "GATEWAY_URL")
    try:
        parsed_url = urlparse(gateway_url)
    except ValueError as error:
        raise ConfigurationError(
            "GATEWAY_URL must be a valid HTTP or HTTPS URL"
        ) from error
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ConfigurationError("GATEWAY_URL must be a valid HTTP or HTTPS URL")
    try:
        parsed_url.port
    except ValueError as error:
        raise ConfigurationError(
            "GATEWAY_URL must include a valid port when specified"
        ) from error

    send_interval_seconds = _number(environment, "SEND_INTERVAL_SECONDS")
    if not math.isfinite(send_interval_seconds) or send_interval_seconds <= 0:
        raise ConfigurationError("SEND_INTERVAL_SECONDS must be a finite number greater than zero")

    request_timeout_seconds = _number(environment, "REQUEST_TIMEOUT_SECONDS")
    if not math.isfinite(request_timeout_seconds) or request_timeout_seconds <= 0:
        raise ConfigurationError("REQUEST_TIMEOUT_SECONDS must be a finite number greater than zero")

    max_retries = _integer(environment, "MAX_RETRIES")
    if max_retries < 0:
        raise ConfigurationError("MAX_RETRIES must be zero or greater")

    failure_rate = _number(environment, "FAILURE_RATE")
    if not math.isfinite(failure_rate) or not 0.0 <= failure_rate <= 1.0:
        raise ConfigurationError("FAILURE_RATE must be between 0.0 and 1.0")

    failure_mode_value = _value(environment, "FAILURE_MODE")
    try:
        failure_mode = FailureMode(failure_mode_value)
    except ValueError as error:
        supported = ", ".join(mode.value for mode in FailureMode)
        raise ConfigurationError(
            f"FAILURE_MODE must be one of: {supported}"
        ) from error

    failure_seed_value = _value(environment, "FAILURE_SEED")
    failure_seed = (
        None if failure_seed_value == "" else _integer(environment, "FAILURE_SEED")
    )

    log_level = _value(environment, "LOG_LEVEL").upper()
    if log_level not in _LOG_LEVELS:
        supported = ", ".join(sorted(_LOG_LEVELS))
        raise ConfigurationError(f"LOG_LEVEL must be one of: {supported}")

    return Config(
        device_id=device_id,
        gateway_url=gateway_url,
        send_interval_seconds=send_interval_seconds,
        request_timeout_seconds=request_timeout_seconds,
        max_retries=max_retries,
        failure_mode=failure_mode,
        failure_rate=failure_rate,
        failure_seed=failure_seed,
        log_level=log_level,
    )


def _value(environ: Mapping[str, str], name: str) -> str:
    return environ.get(name, _DEFAULTS[name])


def _required_text(environ: Mapping[str, str], name: str) -> str:
    value = _value(environ, name).strip()
    if not value:
        raise ConfigurationError(f"{name} must be non-empty")
    return value


def _integer(environ: Mapping[str, str], name: str) -> int:
    value = _value(environ, name)
    try:
        return int(value)
    except (TypeError, ValueError) as error:
        raise ConfigurationError(f"{name} must be an integer") from error


def _number(environ: Mapping[str, str], name: str) -> float:
    value = _value(environ, name)
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ConfigurationError(f"{name} must be a number") from error
