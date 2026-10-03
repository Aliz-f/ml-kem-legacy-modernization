"""M2-44 real Gateway-to-Cloud baseline HTTP contract tests."""

from __future__ import annotations

from contextlib import contextmanager
import asyncio
from datetime import datetime
import json
from pathlib import Path
import socket
from threading import Thread
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
import uvicorn
from fastapi import Request as FastAPIRequest

from cloud_service.app import create_app
from cloud_service.config import load_config
from edge_gateway.cloud.baseline import BaselineCloudClient


CANONICAL = {
    "gateway_id": "gateway-contract", "device_id": "sensor-contract",
    "temperature_c": 22.5, "humidity_pct": 44.0,
    "measured_at": "2026-09-21T12:00:00Z", "sequence_number": 10,
    "received_at": "2026-09-21T12:00:00.100Z",
}


@contextmanager
def _live_cloud(database: Path):
    app = create_app(load_config({
        "DATABASE_URL": f"sqlite:///{database}", "SECURITY_MODE": "classical",
    }))
    captured: list[tuple[str | None, bytes]] = []

    @app.middleware("http")
    async def capture(request: FastAPIRequest, call_next):
        if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
            captured.append((request.headers.get("X-Request-ID"), await request.body()))
        return await call_next(request)

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(
            app, log_config=None, access_log=False, lifespan="on",
            timeout_graceful_shutdown=5,
        ))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = monotonic() + 10
            while not server.started and thread.is_alive() and monotonic() < deadline:
                sleep(0.01)
            assert server.started
            yield f"http://127.0.0.1:{listener.getsockname()[1]}", captured
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            assert not thread.is_alive()


@pytest.fixture
def cloud(tmp_path: Path):
    with _live_cloud(tmp_path / "baseline-contract.db") as running:
        yield running


def _post(base_url: str, payload: dict[str, object]) -> tuple[int, dict[str, object]]:
    request = Request(
        base_url + "/api/v1/baseline/measurements",
        data=json.dumps(payload).encode(), method="POST",
        headers={"Content-Type": "application/json", "X-Request-ID": "req-invalid"},
    )
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def test_gateway_canonical_json_and_correlation_are_accepted_and_mapped(cloud) -> None:
    base_url, captured = cloud
    client = BaselineCloudClient(
        cloud_url=base_url, timeout_seconds=5, max_retries=0,
    )
    acceptance = asyncio.run(client.send(request_id="req-contract", **CANONICAL))

    assert acceptance.status == "accepted"
    assert len(captured) == 1
    request_id, body = captured[0]
    assert request_id == "req-contract"
    assert json.loads(body) == CANONICAL
    assert set(json.loads(body)) == set(CANONICAL)
    assert "request_id" not in json.loads(body)

    with urlopen(base_url + f"/api/v1/measurements/{acceptance.record_id}", timeout=5) as response:
        stored = json.loads(response.read())
    assert stored["gateway_id"] == CANONICAL["gateway_id"]
    assert stored["device_id"] == CANONICAL["device_id"]
    assert datetime.fromisoformat(stored["measured_at"]) == datetime.fromisoformat(
        CANONICAL["measured_at"]
    )
    assert datetime.fromisoformat(stored["gateway_received_at"]) == datetime.fromisoformat(
        CANONICAL["received_at"]
    )
    assert "received_at" not in stored and "request_id" not in stored


@pytest.mark.parametrize("mutation", [
    lambda payload: payload.pop("received_at"),
    lambda payload: payload.update(unknown_field="not-allowed"),
])
def test_cloud_rejects_missing_or_unknown_canonical_fields(cloud, mutation) -> None:
    base_url, _ = cloud
    payload = dict(CANONICAL)
    mutation(payload)
    status, body = _post(base_url, payload)
    assert status == 422
    assert body["error"]["code"] == "INVALID_MEASUREMENT"


def test_cloud_sources_do_not_import_gateway_application_models() -> None:
    root = Path(__file__).parents[2] / "cloud_service/src/cloud_service"
    source = "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.py"))
    assert "from edge_gateway" not in source
    assert "import edge_gateway" not in source
