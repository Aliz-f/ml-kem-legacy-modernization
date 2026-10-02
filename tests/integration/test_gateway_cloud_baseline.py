"""M5-27 real Gateway-to-Cloud baseline HTTP integration coverage."""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import Request

from cloud_service.app import create_app
from cloud_service.config import load_config
from edge_gateway.cloud.baseline import BaselineCloudClient


FIXTURE = Path(__file__).parents[1] / "fixtures" / "canonical_measurement.json"


@contextmanager
def live_cloud(database_path: Path):
    """Serve production Cloud routes and record the Gateway HTTP boundary."""
    app = create_app(
        load_config(
            {
                "DATABASE_URL": f"sqlite:///{database_path.as_posix()}",
                "SECURITY_MODE": "classical",
            }
        )
    )
    requests: list[tuple[str, str | None, bytes]] = []

    @app.middleware("http")
    async def record_gateway_request(request: Request, call_next):
        if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
            requests.append(
                (request.url.path, request.headers.get("X-Request-ID"), await request.body())
            )
        return await call_next(request)

    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="gateway-cloud-baseline-test", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            thread.join(timeout=5)
            raise RuntimeError("Cloud did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("Cloud has no listening socket")
    try:
        yield app, f"http://127.0.0.1:{sockets[0].getsockname()[1]}", requests
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def get_json(url: str) -> dict[str, object]:
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.status == 200
        payload = json.loads(response.read())
    assert isinstance(payload, dict)
    return payload


def test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping(
    tmp_path: Path, caplog
) -> None:
    canonical = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(canonical, dict)
    request_id = "req-m5-27"

    with caplog.at_level(logging.INFO, logger="cloud_service"):
        with live_cloud(tmp_path / "measurements.db") as (_, cloud_url, requests):
            client = BaselineCloudClient(cloud_url=cloud_url, timeout_seconds=5, max_retries=0)
            accepted = asyncio.run(client.send(request_id=request_id, **canonical))
            duplicate = asyncio.run(client.send(request_id=request_id, **canonical))
            row = get_json(f"{cloud_url}/api/v1/measurements/{accepted.record_id}")

    assert accepted.status == "accepted"
    assert accepted.record_id
    assert duplicate.status == "already_accepted"
    assert duplicate.record_id == accepted.record_id
    assert len(requests) == 2
    assert requests[0] == requests[1]
    path, propagated_request_id, body = requests[0]
    assert path == "/api/v1/baseline/measurements"
    assert propagated_request_id == request_id
    assert json.loads(body) == canonical
    assert set(json.loads(body)) == {
        "device_id",
        "temperature_c",
        "humidity_pct",
        "measured_at",
        "sequence_number",
        "received_at",
        "gateway_id",
    }
    assert "request_id" not in json.loads(body)

    expected = dict(canonical)
    expected["gateway_received_at"] = expected.pop("received_at")
    assert set(row) == set(expected) | {"record_id", "cloud_received_at"}
    for field, value in expected.items():
        if field in {"measured_at", "gateway_received_at"}:
            assert datetime.fromisoformat(str(row[field])) == datetime.fromisoformat(str(value))
        else:
            assert row[field] == value
    assert row["record_id"] == accepted.record_id
    assert datetime.fromisoformat(str(row["cloud_received_at"]))
    assert request_id in caplog.text
