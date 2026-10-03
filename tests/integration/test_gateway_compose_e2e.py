"""M2-51/52 real Legacy client through Compose Gateway and Cloud containers."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time
from urllib.request import urlopen

import pytest

from legacy_system.client import GatewayClient


ROOT = Path(__file__).parents[2]
COMPOSE = ROOT / "docker-compose.yml"


def _port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def _compose(project: str, environment: dict[str, str], *args: str, check: bool = True):
    return subprocess.run(
        ["docker", "compose", "--project-name", project, "--file", str(COMPOSE), *args],
        cwd=ROOT, env=environment, text=True, capture_output=True, check=check,
    )


def _wait_json(url: str) -> object:
    deadline = time.monotonic() + 45
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=2) as response:
                return json.loads(response.read())
        except Exception as error:
            last_error = error
            time.sleep(0.2)
    raise AssertionError(f"service did not become available: {type(last_error).__name__}")


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
def test_legacy_contract_persists_through_compose_in_both_modes(security_mode: str) -> None:
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    gateway_port, cloud_port = _port(), _port()
    project = f"mlkem-m2-pr12-{security_mode}-{os.getpid()}"
    environment = {
        **os.environ,
        "SECURITY_MODE": security_mode,
        "GATEWAY_HOST_PORT": str(gateway_port),
        "CLOUD_HOST_PORT": str(cloud_port),
        "DATABASE_URL": "sqlite:////data/cloud.db",
        "GATEWAY_FAILURE_MODE": "none",
        "GATEWAY_FAILURE_RATE": "0",
        "CLOUD_FAILURE_MODE": "none",
        "CLOUD_FAILURE_RATE": "0",
        "LOG_LEVEL": "INFO",
    }
    try:
        started = _compose(
            project, environment, "up", "--detach", "--build", "--wait",
            "cloud-service", "edge-gateway", check=False,
        )
        assert started.returncode == 0, started.stdout + started.stderr
        assert _wait_json(f"http://127.0.0.1:{gateway_port}/health") == {"status": "ok"}
        ready = _wait_json(f"http://127.0.0.1:{gateway_port}/ready")
        assert ready == {"status": "ready", "security_mode": security_mode}

        payload = {
            "device_id": f"sensor-compose-{security_mode}",
            "temperature_c": 22.5,
            "humidity_pct": 44.0,
            "timestamp": "2026-09-21T12:00:00Z",
            "sequence_number": 1,
        }
        result = GatewayClient(
            f"http://127.0.0.1:{gateway_port}", request_timeout_seconds=15,
            max_retries=0,
        ).send(payload)
        assert result.success and result.status_code == 202 and result.attempt_count == 1

        listing = _wait_json(f"http://127.0.0.1:{cloud_port}/api/v1/measurements")
        [stored] = listing["items"]
        assert stored["device_id"] == payload["device_id"]
        assert stored["temperature_c"] == payload["temperature_c"]
        assert stored["humidity_pct"] == payload["humidity_pct"]
        assert stored["sequence_number"] == payload["sequence_number"]
        assert stored["gateway_id"] == "gateway-001"

        with urlopen(f"http://127.0.0.1:{gateway_port}/metrics", timeout=5) as response:
            gateway_metrics = response.read().decode()
        with urlopen(f"http://127.0.0.1:{cloud_port}/metrics", timeout=5) as response:
            metrics = response.read().decode()
        assert f'gateway_service_info{{security_mode="{security_mode}"}} 1' in gateway_metrics
        assert "gateway_measurements_received_total 1" in gateway_metrics
        assert "gateway_measurements_accepted_total 1" in gateway_metrics
        assert "gateway_cloud_requests_total 1" in gateway_metrics
        assert f'cloud_service_info{{security_mode="{security_mode}"}} 1' in metrics
        if security_mode == "classical":
            assert "cloud_baseline_requests_total 1" in metrics
            assert "cloud_secure_requests_total 0" in metrics
        else:
            assert "cloud_baseline_requests_total 0" in metrics
            assert "cloud_secure_requests_total 1" in metrics

        stopped = _compose(project, environment, "stop", "--timeout", "10", "edge-gateway")
        assert stopped.returncode == 0
        logs = _compose(project, environment, "logs", "--no-color", "edge-gateway").stdout
        assert "gateway_shutting_down" in logs
        assert "Application shutdown complete" in logs
        assert "Traceback" not in logs and "ERROR" not in logs
    finally:
        _compose(
            project, environment, "down", "--volumes", "--remove-orphans",
            "--timeout", "10", check=False,
        )
