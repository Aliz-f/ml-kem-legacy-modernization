"""Live Legacy HTTP client, Gateway application, and Cloud persistence paths."""

from __future__ import annotations

import ast
from contextlib import contextmanager
from datetime import datetime
import json
from pathlib import Path
import threading
import time
from typing import Iterator
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest
import uvicorn
from fastapi import FastAPI

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager
from legacy_system.client import GatewayClient


@contextmanager
def _serve(app: FastAPI) -> Iterator[str]:
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started:
            if not thread.is_alive() or time.monotonic() >= deadline:
                raise RuntimeError("integration server did not start")
            time.sleep(0.02)
        sockets = server.servers[0].sockets
        assert sockets
        yield f"http://127.0.0.1:{sockets[0].getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        assert not thread.is_alive()


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
def test_legacy_gateway_cloud_http_path_persists_canonical_measurement(
    tmp_path: Path, mode: str,
) -> None:
    """M4-78/79: all three production HTTP boundaries and SQLite are real."""
    fixture_path = Path(__file__).parents[2] / "tests/fixtures/valid_legacy_measurement.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    cloud_app = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'cloud.db').as_posix()}",
        "SECURITY_MODE": mode,
    }))
    with _serve(cloud_app) as cloud_url:
        gateway_config = load_gateway_config({
            "SECURITY_MODE": mode, "CLOUD_URL": cloud_url, "CLOUD_MAX_RETRIES": "0",
        })
        secure = None
        if mode == "mlkem":
            # Gateway composition is supplied here until its owner wires main().
            sessions = SessionManager(gateway_config.gateway_id, cloud_url, 5.0)
            secure = SecureTransport(sessions, cloud_url=cloud_url, timeout_seconds=5.0, max_retries=0)
        gateway_app = create_gateway_app(gateway_config, secure_transport=secure)
        with _serve(gateway_app) as gateway_url:
            result = GatewayClient(gateway_url, 5.0, max_retries=0).send(payload)
            assert result.success is True
            assert result.status_code == 202
            assert result.attempt_count == 1

        rows = cloud_app.state.repository.list()
        assert len(rows) == 1
        stored = rows[0]
        assert stored.device_id == payload["device_id"]
        assert stored.gateway_id == gateway_config.gateway_id
        assert stored.temperature_c == payload["temperature_c"]
        assert stored.humidity_pct == payload["humidity_pct"]
        assert stored.sequence_number == payload["sequence_number"]
        assert stored.measured_at == datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
        assert stored.gateway_received_at <= stored.cloud_received_at
        with urlopen(cloud_url + f"/api/v1/measurements/{stored.record_id}", timeout=5) as response:
            queried = json.load(response)
        assert queried["record_id"] == stored.record_id
        assert queried["gateway_received_at"] == stored.to_dict()["gateway_received_at"]
        assert queried["cloud_received_at"] == stored.to_dict()["cloud_received_at"]
        if mode == "mlkem":
            assert len(cloud_app.state.sessions) == 1
        else:
            assert cloud_app.state.sessions is None

    # A new Cloud process reopens only persisted measurements, never session keys.
    restarted = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'cloud.db').as_posix()}",
        "SECURITY_MODE": mode,
    }))
    with _serve(restarted):
        assert len(restarted.state.repository.list()) == 1
        if mode == "mlkem":
            assert len(restarted.state.sessions) == 0


def test_cloud_runtime_only_accepts_gateway_canonical_fields(tmp_path: Path) -> None:
    """M4-80: Cloud has no Legacy/Gateway implementation imports or field aliases."""
    source_root = Path(__file__).parents[1] / "src/cloud_service"
    for path in source_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            else:
                continue
            assert all(not name.startswith(("legacy_system", "edge_gateway")) for name in modules)

    cloud_app = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'cloud.db').as_posix()}",
        "SECURITY_MODE": "classical",
    }))
    fixture_path = Path(__file__).parents[2] / "tests/fixtures/valid_legacy_measurement.json"
    legacy_payload = fixture_path.read_bytes()
    from urllib.request import Request

    with _serve(cloud_app) as cloud_url:
        request = Request(
            cloud_url + "/api/v1/baseline/measurements", data=legacy_payload,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with pytest.raises(HTTPError) as caught:
            urlopen(request, timeout=5)
        assert caught.value.code == 422
        assert cloud_app.state.repository.list() == []
