"""M5-09/10/13 static Gateway and Cloud container contract checks."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCKERFILE = ROOT / "edge_gateway" / "Dockerfile"
CLOUD_DOCKERFILE = ROOT / "cloud_service" / "Dockerfile"
LEGACY_DOCKERFILE = ROOT / "legacy_system" / "Dockerfile"
COMPOSE = ROOT / "docker-compose.yml"


def test_gateway_service_image_is_frozen_non_root_and_signal_aware() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim-bookworm" in text
    assert "ghcr.io/astral-sh/uv:0.12.19" in text
    assert "uv sync --frozen --package edge-gateway --no-dev --no-editable" in text
    assert "USER 10001:10001" in text
    assert "EXPOSE 8000" in text
    assert "STOPSIGNAL SIGTERM" in text
    assert 'CMD ["edge-gateway"]' in text
    assert "/health" in text
    assert "--reload" not in text


def test_cloud_service_image_is_frozen_non_root_and_readiness_aware() -> None:
    text = CLOUD_DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim-bookworm" in text
    assert "ghcr.io/astral-sh/uv:0.12.19" in text
    assert "uv sync --frozen --package cloud-service --no-dev --no-editable" in text
    assert "USER 10001:10001" in text
    assert "EXPOSE 9000" in text
    assert "STOPSIGNAL SIGTERM" in text
    assert 'CMD ["cloud-service"]' in text
    assert "/ready" in text


def test_legacy_device_image_uses_the_locked_workspace_runtime() -> None:
    text = LEGACY_DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim-bookworm" in text
    assert "ghcr.io/astral-sh/uv:0.12.19" in text
    assert "uv sync --frozen --package legacy-system --no-dev --no-editable" in text
    assert "USER 10001:10001" in text
    assert "STOPSIGNAL SIGTERM" in text
    assert 'CMD ["python", "-m", "legacy_system.main"]' in text


def test_compose_uses_internal_dns_and_service_scoped_failure_sources() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "dockerfile: edge_gateway/Dockerfile" in text
    assert "dockerfile: cloud_service/Dockerfile" in text
    assert "CLOUD_URL: ${CLOUD_URL:-http://cloud-service:9000}" in text
    assert "FAILURE_MODE: ${GATEWAY_FAILURE_MODE:-none}" in text
    assert "FAILURE_RATE: ${GATEWAY_FAILURE_RATE:-0.0}" in text
    assert "FAILURE_SEED: ${GATEWAY_FAILURE_SEED:-2}" in text
    assert "FAILURE_MODE: ${CLOUD_FAILURE_MODE:-none}" in text
    assert "SECURITY_MODE: ${SECURITY_MODE:-classical}" in text
    assert "condition: service_healthy" in text
    assert "localhost" not in text
    assert "http://127.0.0.1:9000/health" in text
    assert "http://127.0.0.1:8000/health" in text
    assert text.count("healthcheck:") == 2
