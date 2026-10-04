"""M1-13/14 static Legacy Device Dockerfile and Compose packaging contract checks."""

import importlib
from pathlib import Path
import tomllib

from legacy_system.config import FailureMode, load_config

LEGACY_ROOT = Path(__file__).parents[1]
DOCKERFILE = LEGACY_ROOT / "Dockerfile"
PYPROJECT = LEGACY_ROOT / "pyproject.toml"
COMPOSE = LEGACY_ROOT.parent / "docker-compose.yml"


def test_legacy_dockerfile_exists_and_uses_frozen_python_base() -> None:
    assert DOCKERFILE.is_file(), f"Expected Dockerfile to exist at {DOCKERFILE}"
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim-bookworm" in content
    assert "COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv" in content


def test_legacy_dockerfile_uses_frozen_uv_sync() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "UV_LINK_MODE=copy" in content
    assert "UV_PROJECT_ENVIRONMENT=/app/.venv" in content
    assert 'PATH="/app/.venv/bin:${PATH}"' in content
    assert "RUN uv sync --frozen --package legacy-system --no-dev --no-editable" in content


def test_legacy_dockerfile_non_root_and_stopsignal() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "USER 10001:10001" in content
    assert "STOPSIGNAL SIGTERM" in content


def test_legacy_dockerfile_does_not_expose_ports() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    expose_lines = [line for line in lines if line.startswith("EXPOSE")]
    assert not expose_lines, (
        f"Legacy Device is strictly an outbound client and must not expose ports: {expose_lines}"
    )


def test_legacy_dockerfile_command_invokes_entrypoint() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert 'CMD ["python", "-m", "legacy_system.main"]' in content


def test_legacy_pyproject_registers_console_script() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert "legacy-device" in scripts
    entry_point = scripts["legacy-device"]
    assert entry_point == "legacy_system.main:main"

    module_name, func_name = entry_point.split(":")
    mod = importlib.import_module(module_name)
    func = getattr(mod, func_name)
    assert callable(func)


def test_compose_defines_legacy_device_service_and_build_target() -> None:
    assert COMPOSE.is_file(), f"Expected docker-compose.yml at {COMPOSE}"
    text = COMPOSE.read_text(encoding="utf-8")
    assert "legacy-device:" in text
    assert "dockerfile: legacy_system/Dockerfile" in text


def test_compose_legacy_device_depends_on_healthy_gateway() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "legacy-device:" in text
    legacy_section = text.split("legacy-device:")[1]
    assert "edge-gateway:" in legacy_section
    assert "condition: service_healthy" in legacy_section


def test_compose_legacy_device_uses_internal_dns_endpoint() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "legacy-device:" in text
    legacy_section = text.split("legacy-device:")[1]
    assert "GATEWAY_URL: ${GATEWAY_URL:-http://edge-gateway:8000}" in legacy_section
    assert "localhost" not in legacy_section


def test_compose_legacy_device_maps_service_scoped_failure_variables() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "legacy-device:" in text
    legacy_section = text.split("legacy-device:")[1]
    assert "FAILURE_MODE: ${LEGACY_FAILURE_MODE:-none}" in legacy_section
    assert "FAILURE_RATE: ${LEGACY_FAILURE_RATE:-0.0}" in legacy_section
    assert "FAILURE_SEED: ${LEGACY_FAILURE_SEED-}" in legacy_section


def test_compose_legacy_device_does_not_publish_ports() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "legacy-device:" in text
    legacy_section = text.split("legacy-device:")[1]
    if "volumes:" in legacy_section:
        legacy_section = legacy_section.split("volumes:")[0]
    lines = [line.strip() for line in legacy_section.splitlines()]
    port_lines = [line for line in lines if line.startswith("ports:")]
    assert not port_lines, f"Legacy device in Compose must not publish ports: {port_lines}"


def test_compose_environment_loads_valid_legacy_config() -> None:
    compose_env = {
        "DEVICE_ID": "sensor-001",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "5",
        "REQUEST_TIMEOUT_SECONDS": "3",
        "MAX_RETRIES": "2",
        "FAILURE_MODE": "none",
        "FAILURE_RATE": "0.0",
        "FAILURE_SEED": "1",
        "LOG_LEVEL": "INFO",
    }
    config = load_config(environ=compose_env)
    assert config.device_id == "sensor-001"
    assert config.gateway_url == "http://edge-gateway:8000"
    assert config.send_interval_seconds == 5
    assert config.request_timeout_seconds == 3
    assert config.max_retries == 2
    assert config.failure_mode == FailureMode.NONE
    assert config.failure_rate == 0.0
    assert config.failure_seed == 1
    assert config.log_level == "INFO"


def test_compose_empty_failure_seed_keeps_legacy_selection_nondeterministic() -> None:
    config = load_config({"FAILURE_SEED": ""})

    assert config.failure_seed is None


def test_compose_environment_with_custom_failure_settings_loads_valid_legacy_config() -> None:
    # Emulate Compose mapping LEGACY_FAILURE_* into container's generic FAILURE_*
    compose_env = {
        "DEVICE_ID": "sensor-custom",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "10",
        "REQUEST_TIMEOUT_SECONDS": "4",
        "MAX_RETRIES": "3",
        "FAILURE_MODE": "invalid_temperature",
        "FAILURE_RATE": "0.5",
        "FAILURE_SEED": "42",
        "LOG_LEVEL": "DEBUG",
    }
    config = load_config(environ=compose_env)
    assert config.device_id == "sensor-custom"
    assert config.failure_mode == FailureMode.INVALID_TEMPERATURE
    assert config.failure_rate == 0.5
    assert config.failure_seed == 42
    assert config.log_level == "DEBUG"
