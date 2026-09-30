"""Environment configuration for the Cloud Service; no startup side effects."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
import math
import os


class ConfigurationError(ValueError):
    """Invalid Cloud configuration, with a safe message naming the setting."""


class SecurityMode(StrEnum):
    CLASSICAL = "classical"
    MLKEM = "mlkem"


class FailureMode(StrEnum):
    """Cloud contract values; fault injection is implemented in later tasks."""

    NONE = "none"
    PUBLIC_KEY_UNAVAILABLE = "public_key_unavailable"
    MLKEM_DECAPSULATION_FAILURE = "mlkem_decapsulation_failure"
    SESSION_NOT_FOUND = "session_not_found"
    SESSION_EXPIRED = "session_expired"
    DECRYPTION_FAILURE = "decryption_failure"
    STORAGE_FAILURE = "storage_failure"
    PROCESSING_DELAY = "processing_delay"
    SERVICE_UNAVAILABLE = "service_unavailable"
    DROP_RESPONSE = "drop_response"
    RANDOM = "random"


@dataclass(frozen=True, slots=True)
class Config:
    """Settings returned by load_config; use from_env for validated input."""

    cloud_id: str
    host: str
    port: int
    database_url: str
    security_mode: SecurityMode
    session_ttl_seconds: int
    failure_mode: FailureMode
    failure_rate: float
    failure_seed: int | None
    failure_delay_seconds: float
    log_level: str

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Config":
        return load_config(environ)


_DEFAULTS = {
    "CLOUD_ID": "cloud-001",
    "HOST": "0.0.0.0",
    "PORT": "9000",
    "DATABASE_URL": "sqlite:///cloud.db",
    "SECURITY_MODE": "classical",
    "SESSION_TTL_SECONDS": "300",
    "FAILURE_MODE": "none",
    "FAILURE_RATE": "0.0",
    "FAILURE_SEED": "",
    "FAILURE_DELAY_SECONDS": "2",
    "LOG_LEVEL": "INFO",
}
_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
_MAX_FAILURE_DELAY_SECONDS = 30.0


def load_config(environ: Mapping[str, str] | None = None) -> Config:
    """Read environment settings without opening storage or initializing crypto.

    An explicit mapping, including an empty one, isolates the loader from the
    process environment. Errors never echo supplied configuration values.
    """
    environment = os.environ if environ is None else environ

    def value(name: str) -> str:
        return environment.get(name, _DEFAULTS[name])

    def text(name: str) -> str:
        result = value(name).strip()
        if not result or any(ord(char) < 32 for char in result):
            raise ConfigurationError(f"{name} must be non-empty text without control characters")
        return result

    def integer(name: str) -> int:
        try:
            return int(value(name))
        except ValueError:
            raise ConfigurationError(f"{name} must be an integer") from None

    def number(name: str) -> float:
        try:
            result = float(value(name))
        except ValueError:
            raise ConfigurationError(f"{name} must be a finite number") from None
        if not math.isfinite(result):
            raise ConfigurationError(f"{name} must be a finite number")
        return result

    cloud_id = text("CLOUD_ID")
    host = text("HOST")
    port = integer("PORT")
    if not 1 <= port <= 65535:
        raise ConfigurationError("PORT must be between 1 and 65535")

    database_url = text("DATABASE_URL")
    database_path = database_url.removeprefix("sqlite:///")
    if (
        not database_url.startswith("sqlite:///")
        or not database_path.strip("/")
        or database_path.endswith(("/", "/.", "/.."))
        or database_path in {".", ".."}
        or any(char in database_path for char in "?#\\")
    ):
        raise ConfigurationError("DATABASE_URL must be sqlite:/// followed by a database file path or :memory:")

    try:
        security_mode = SecurityMode(value("SECURITY_MODE"))
    except ValueError:
        raise ConfigurationError("SECURITY_MODE must be classical or mlkem") from None

    session_ttl_seconds = integer("SESSION_TTL_SECONDS")
    if session_ttl_seconds != 300:
        raise ConfigurationError("SESSION_TTL_SECONDS must be 300 for protocol version 1")

    try:
        failure_mode = FailureMode(value("FAILURE_MODE"))
    except ValueError:
        raise ConfigurationError("FAILURE_MODE must be a supported Cloud failure mode") from None

    failure_rate = number("FAILURE_RATE")
    if not 0 <= failure_rate <= 1:
        raise ConfigurationError("FAILURE_RATE must be between 0.0 and 1.0")
    failure_seed = None if not value("FAILURE_SEED").strip() else integer("FAILURE_SEED")
    failure_delay_seconds = number("FAILURE_DELAY_SECONDS")
    if not 0 <= failure_delay_seconds <= _MAX_FAILURE_DELAY_SECONDS:
        raise ConfigurationError("FAILURE_DELAY_SECONDS must be between 0 and 30 seconds")
    log_level = value("LOG_LEVEL").upper()
    if log_level not in _LOG_LEVELS:
        raise ConfigurationError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR or CRITICAL")

    return Config(
        cloud_id=cloud_id,
        host=host,
        port=port,
        database_url=database_url,
        security_mode=security_mode,
        session_ttl_seconds=session_ttl_seconds,
        failure_mode=failure_mode,
        failure_rate=failure_rate,
        failure_seed=failure_seed,
        failure_delay_seconds=failure_delay_seconds,
        log_level=log_level,
    )
