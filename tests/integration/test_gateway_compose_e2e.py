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


def _wait_for_device_measurement(url: str, device_id: str) -> dict[str, object]:
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        payload = _wait_json(f"{url}/api/v1/measurements?device_id={device_id}")
        if isinstance(payload, dict) and payload.get("items"):
            return payload["items"][0]
        time.sleep(0.2)
    raise AssertionError("Legacy Compose service did not persist a measurement")


def _wait_unavailable(url: str) -> None:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=2):
                pass
        except Exception:
            return
        time.sleep(0.2)
    raise AssertionError("service did not become unavailable")


def _metrics(url: str) -> str:
    with urlopen(url, timeout=5) as response:
        return response.read().decode()


def _measurement(device_id: str, sequence_number: int) -> dict[str, object]:
    return {
        "device_id": device_id,
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": f"2026-09-21T12:{sequence_number:02d}:00Z",
        "sequence_number": sequence_number,
    }


def _send(gateway_url: str, device_id: str, sequence_number: int):
    return GatewayClient(
        gateway_url, request_timeout_seconds=15, max_retries=0,
    ).send(_measurement(device_id, sequence_number))


def test_compose_starts_legacy_device_and_persists_a_measurement() -> None:
    """The frozen three-service topology starts the Legacy runtime after Gateway readiness."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    gateway_port, cloud_port = _port(), _port()
    project = f"mlkem-full-compose-{os.getpid()}"
    device_id = f"sensor-compose-device-{os.getpid()}"
    environment = {
        **os.environ,
        "SECURITY_MODE": "classical",
        "GATEWAY_HOST_PORT": str(gateway_port),
        "CLOUD_HOST_PORT": str(cloud_port),
        "DATABASE_URL": "sqlite:////data/cloud.db",
        "DEVICE_ID": device_id,
        "SEND_INTERVAL_SECONDS": "60",
        "REQUEST_TIMEOUT_SECONDS": "15",
        "MAX_RETRIES": "0",
        "LEGACY_FAILURE_MODE": "none",
        "LEGACY_FAILURE_RATE": "0",
        "GATEWAY_FAILURE_MODE": "none",
        "GATEWAY_FAILURE_RATE": "0",
        "CLOUD_FAILURE_MODE": "none",
        "CLOUD_FAILURE_RATE": "0",
        "LOG_LEVEL": "INFO",
    }
    cloud_url = f"http://127.0.0.1:{cloud_port}"
    try:
        started = _compose(project, environment, "up", "--detach", "--build", "--wait", check=False)
        assert started.returncode == 0, started.stdout + started.stderr
        stored = _wait_for_device_measurement(cloud_url, device_id)
        assert stored["device_id"] == device_id
        assert stored["sequence_number"] == 0
        logs = _compose(project, environment, "logs", "--no-color", "legacy-device").stdout
        assert "event=device_ready component=legacy_system" in logs
        assert "event=measurement_delivered component=legacy_system" in logs
    finally:
        _compose(
            project, environment, "down", "--volumes", "--remove-orphans",
            "--timeout", "10", check=False,
        )


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
        assert _wait_json(f"http://127.0.0.1:{cloud_port}/health") == {"status": "ok"}
        expected_cloud_ready = {"status": "ready", "storage": "ok"}
        if security_mode == "mlkem":
            expected_cloud_ready["mlkem"] = "available"
        # Neither mode requires an active Gateway session: sessions are lazy.
        assert _wait_json(f"http://127.0.0.1:{cloud_port}/ready") == expected_cloud_ready
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


def test_compose_cloud_restart_recovers_readiness_and_delivery() -> None:
    """A Cloud outage is visible to delivery and recovery restores a fresh request."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    gateway_port, cloud_port = _port(), _port()
    project = f"mlkem-compose-recovery-{os.getpid()}"
    environment = {
        **os.environ,
        "SECURITY_MODE": "classical",
        "GATEWAY_HOST_PORT": str(gateway_port),
        "CLOUD_HOST_PORT": str(cloud_port),
        "DATABASE_URL": "sqlite:////data/cloud.db",
        "CLOUD_MAX_RETRIES": "0",
        "GATEWAY_FAILURE_MODE": "none",
        "GATEWAY_FAILURE_RATE": "0",
        "CLOUD_FAILURE_MODE": "none",
        "CLOUD_FAILURE_RATE": "0",
        "LOG_LEVEL": "INFO",
    }
    gateway_url = f"http://127.0.0.1:{gateway_port}"
    cloud_url = f"http://127.0.0.1:{cloud_port}"
    try:
        started = _compose(
            project, environment, "up", "--detach", "--build", "--wait",
            "cloud-service", "edge-gateway", check=False,
        )
        assert started.returncode == 0, started.stdout + started.stderr
        assert _wait_json(f"{cloud_url}/ready") == {"status": "ready", "storage": "ok"}
        assert _wait_json(f"{gateway_url}/ready") == {
            "status": "ready", "security_mode": "classical",
        }

        stopped = _compose(project, environment, "stop", "--timeout", "10", "cloud-service")
        assert stopped.returncode == 0
        _wait_unavailable(f"{cloud_url}/health")
        # Gateway readiness reports its initialized local transport, not Cloud reachability.
        assert _wait_json(f"{gateway_url}/ready") == {
            "status": "ready", "security_mode": "classical",
        }

        failed = GatewayClient(gateway_url, request_timeout_seconds=15, max_retries=0).send({
            "device_id": "sensor-compose-recovery",
            "temperature_c": 22.5,
            "humidity_pct": 44.0,
            "timestamp": "2026-09-21T12:00:00Z",
            "sequence_number": 1,
        })
        assert not failed.success and failed.status_code == 503 and failed.attempt_count == 1

        restarted = _compose(
            project, environment, "up", "--detach", "--wait", "cloud-service", check=False,
        )
        assert restarted.returncode == 0, restarted.stdout + restarted.stderr
        assert _wait_json(f"{cloud_url}/health") == {"status": "ok"}
        assert _wait_json(f"{cloud_url}/ready") == {"status": "ready", "storage": "ok"}

        recovered = GatewayClient(gateway_url, request_timeout_seconds=15, max_retries=0).send({
            "device_id": "sensor-compose-recovery",
            "temperature_c": 22.5,
            "humidity_pct": 44.0,
            "timestamp": "2026-09-21T12:01:00Z",
            "sequence_number": 2,
        })
        assert recovered.success and recovered.status_code == 202 and recovered.attempt_count == 1
        listing = _wait_json(f"{cloud_url}/api/v1/measurements")
        assert [item["sequence_number"] for item in listing["items"]] == [2]
    finally:
        _compose(
            project, environment, "down", "--volumes", "--remove-orphans",
            "--timeout", "10", check=False,
        )


def test_compose_gateway_restart_establishes_a_fresh_mlkem_session() -> None:
    """M5-77/M5-78: Gateway restart loses its local session and handshakes again."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    gateway_port, cloud_port = _port(), _port()
    project = f"mlkem-compose-gateway-restart-{os.getpid()}"
    environment = {
        **os.environ,
        "SECURITY_MODE": "mlkem",
        "GATEWAY_HOST_PORT": str(gateway_port),
        "CLOUD_HOST_PORT": str(cloud_port),
        "DATABASE_URL": "sqlite:////data/cloud.db",
        "GATEWAY_FAILURE_MODE": "none",
        "GATEWAY_FAILURE_RATE": "0",
        "CLOUD_FAILURE_MODE": "none",
        "CLOUD_FAILURE_RATE": "0",
        "LOG_LEVEL": "INFO",
    }
    gateway_url = f"http://127.0.0.1:{gateway_port}"
    cloud_url = f"http://127.0.0.1:{cloud_port}"
    device_id = "sensor-compose-gateway-restart"
    try:
        started = _compose(
            project, environment, "up", "--detach", "--build", "--wait",
            "cloud-service", "edge-gateway", check=False,
        )
        assert started.returncode == 0, started.stdout + started.stderr
        assert _send(gateway_url, device_id, 1).success
        assert "cloud_mlkem_sessions_created_total 1" in _metrics(f"{cloud_url}/metrics")

        stopped = _compose(project, environment, "stop", "--timeout", "10", "edge-gateway")
        assert stopped.returncode == 0
        _wait_unavailable(f"{gateway_url}/health")
        restarted = _compose(
            project, environment, "up", "--detach", "--force-recreate", "--no-deps", "--wait",
            "edge-gateway", check=False,
        )
        assert restarted.returncode == 0, restarted.stdout + restarted.stderr
        assert _wait_json(f"{gateway_url}/ready") == {
            "status": "ready", "security_mode": "mlkem",
        }

        assert _send(gateway_url, device_id, 2).success
        cloud_metrics = _metrics(f"{cloud_url}/metrics")
        gateway_metrics = _metrics(f"{gateway_url}/metrics")
        assert "cloud_mlkem_sessions_created_total 2" in cloud_metrics
        assert 'gateway_mlkem_handshakes_total{result="success"} 1' in gateway_metrics
        assert "gateway_pqc_fallback_total 0" in gateway_metrics
        listing = _wait_json(f"{cloud_url}/api/v1/measurements")
        assert [item["sequence_number"] for item in listing["items"]] == [1, 2]
    finally:
        _compose(
            project, environment, "down", "--volumes", "--remove-orphans",
            "--timeout", "10", check=False,
        )


def test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback() -> None:
    """M5-77/M5-79: a Cloud restart rejects the stale session and recovers once."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    gateway_port, cloud_port = _port(), _port()
    project = f"mlkem-compose-cloud-restart-{os.getpid()}"
    environment = {
        **os.environ,
        "SECURITY_MODE": "mlkem",
        "GATEWAY_HOST_PORT": str(gateway_port),
        "CLOUD_HOST_PORT": str(cloud_port),
        "DATABASE_URL": "sqlite:////data/cloud.db",
        "GATEWAY_FAILURE_MODE": "none",
        "GATEWAY_FAILURE_RATE": "0",
        "CLOUD_FAILURE_MODE": "none",
        "CLOUD_FAILURE_RATE": "0",
        "LOG_LEVEL": "INFO",
    }
    gateway_url = f"http://127.0.0.1:{gateway_port}"
    cloud_url = f"http://127.0.0.1:{cloud_port}"
    device_id = "sensor-compose-cloud-restart"
    try:
        started = _compose(
            project, environment, "up", "--detach", "--build", "--wait",
            "cloud-service", "edge-gateway", check=False,
        )
        assert started.returncode == 0, started.stdout + started.stderr
        initial_key = _wait_json(f"{cloud_url}/api/v1/crypto/public-key")["key_id"]
        assert _send(gateway_url, device_id, 1).success

        stopped = _compose(project, environment, "stop", "--timeout", "10", "cloud-service")
        assert stopped.returncode == 0
        _wait_unavailable(f"{cloud_url}/health")
        restarted = _compose(
            project, environment, "up", "--detach", "--wait", "cloud-service", check=False,
        )
        assert restarted.returncode == 0, restarted.stdout + restarted.stderr
        assert _wait_json(f"{cloud_url}/ready") == {
            "status": "ready", "storage": "ok", "mlkem": "available",
        }
        assert _wait_json(f"{cloud_url}/api/v1/crypto/public-key")["key_id"] != initial_key

        # The Gateway first submits through its stale session. Cloud responds
        # SESSION_INVALID; the frozen recovery rebuilds this logical request
        # under one replacement session rather than using the baseline route.
        recovered = _send(gateway_url, device_id, 2)
        assert recovered.success and recovered.status_code == 202
        gateway_metrics = _metrics(f"{gateway_url}/metrics")
        cloud_metrics = _metrics(f"{cloud_url}/metrics")
        assert 'gateway_mlkem_handshakes_total{result="success"} 2' in gateway_metrics
        assert 'gateway_session_reestablishments_total{result="success"} 1' in gateway_metrics
        assert "gateway_pqc_fallback_total 0" in gateway_metrics
        assert "cloud_baseline_requests_total 0" in cloud_metrics
        assert "cloud_mlkem_sessions_created_total 1" in cloud_metrics
        listing = _wait_json(f"{cloud_url}/api/v1/measurements")
        assert [item["sequence_number"] for item in listing["items"]] == [1, 2]
    finally:
        _compose(
            project, environment, "down", "--volumes", "--remove-orphans",
            "--timeout", "10", check=False,
        )
