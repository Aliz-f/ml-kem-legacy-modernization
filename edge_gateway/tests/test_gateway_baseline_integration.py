"""M2-16: production Gateway client -> live Cloud HTTP -> file SQLite."""

import asyncio
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import logging
import socket
import sqlite3
from threading import Thread
from time import monotonic, sleep

import httpx
import pytest
import uvicorn
from fastapi import Request

from cloud_service.app import create_app
from cloud_service.config import load_config
from edge_gateway.cloud.baseline import BaselineCloudClient, BaselineCloudError


CANONICAL = {
    "device_id": "sensor-test",
    "temperature_c": 22.5,
    "humidity_pct": 44.0,
    "measured_at": "2026-09-21T12:00:00Z",
    "sequence_number": 1,
    "received_at": "2026-09-21T12:00:00.100Z",
    "gateway_id": "gateway-test",
}


@contextmanager
def live_cloud(database_path):
    """Run production routes/lifespan; observe requests without replacing delivery."""
    app = create_app(load_config({
        "DATABASE_URL": f"sqlite:///{database_path}", "SECURITY_MODE": "classical",
    }))
    requests = []

    @app.middleware("http")
    async def capture(request: Request, call_next):
        if request.method == "POST":
            requests.append((
                request.url.path, request.headers.get("X-Request-ID"),
                await request.body(),
            ))
        return await call_next(request)

    logger = logging.getLogger("cloud_service")
    previous_level = logger.level
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
            assert server.started, "Cloud failed to start"
            url = f"http://127.0.0.1:{listener.getsockname()[1]}"
            with httpx.Client(base_url=url, timeout=5, trust_env=False) as query:
                assert query.get("/health").status_code == 200
                # Readiness remains a placeholder in the current application.
                assert query.get("/ready").status_code == 503
                yield app, url, query, requests
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            logger.setLevel(previous_level)
            assert not thread.is_alive(), "Cloud failed to stop"


def test_baseline_client_preserves_fields_correlation_and_persistence(tmp_path, caplog):
    database_path = tmp_path / "baseline.db"
    with caplog.at_level(logging.INFO, logger="cloud_service"):
        with live_cloud(database_path) as (_, url, query, requests):
            client = BaselineCloudClient(cloud_url=url, timeout_seconds=5, max_retries=0)
            started = datetime.now(timezone.utc)
            accepted = asyncio.run(client.send(request_id="req-test-001", **CANONICAL))
            assert accepted.status == "accepted"
            assert accepted.record_id
            detail = query.get(f"/api/v1/measurements/{accepted.record_id}")
            assert detail.status_code == 200
            row = detail.json()
            expected = dict(CANONICAL)
            expected["gateway_received_at"] = expected.pop("received_at")
            assert set(row) == set(expected) | {"record_id", "cloud_received_at"}
            for field, value in expected.items():
                if field in {"measured_at", "gateway_received_at"}:
                    assert datetime.fromisoformat(row[field]) == datetime.fromisoformat(value)
                else:
                    assert row[field] == value
            assert row["record_id"] == accepted.record_id
            assert started <= datetime.fromisoformat(row["cloud_received_at"]) <= datetime.now(timezone.utc)

            duplicate = asyncio.run(client.send(request_id="req-test-001", **CANONICAL))
            assert duplicate.status == "already_accepted"
            assert duplicate.record_id == accepted.record_id
            listing = query.get("/api/v1/measurements")
            assert listing.status_code == 200
            assert listing.json() == {"items": [row]}
            assert len(requests) == 2
            assert requests[0] == requests[1]
            path, request_id, body = requests[0]
            assert path == "/api/v1/baseline/measurements"
            assert request_id == "req-test-001"
            assert json.loads(body) == CANONICAL  # Exactly seven fields, no request_id.
            for status in ("accepted", "already_accepted"):
                assert any(
                    record.name == "cloud_service" and record.getMessage() == (
                        f"measurement_{status} request_id='req-test-001' "
                        f"record_id={accepted.record_id}"
                    ) for record in caplog.records
                )

    # A fresh connection after Cloud shutdown proves committed disk persistence.
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        persisted = [dict(record) for record in connection.execute("SELECT * FROM measurements")]
    assert persisted == [row]


@pytest.mark.parametrize("failure", ["validation", "storage"])
def test_baseline_client_classifies_real_cloud_failures_without_persisting(tmp_path, failure):
    with live_cloud(tmp_path / "failure.db") as (app, url, query, requests):
        delays = []
        client = BaselineCloudClient(
            cloud_url=url, timeout_seconds=5, max_retries=2, sleep=delays.append,
        )
        measurement = dict(CANONICAL)
        if failure == "validation":
            measurement["temperature_c"] = 100
        else:
            # Fail actual SQLite writes on this disposable Cloud connection.
            with app.state.database.transaction() as connection:
                connection.execute("PRAGMA query_only = ON")
        with pytest.raises(BaselineCloudError) as caught:
            asyncio.run(client.send(request_id="req-test-failure", **measurement))
        assert caught.value.code == (
            "INVALID_MEASUREMENT" if failure == "validation" else "STORAGE_UNAVAILABLE"
        )
        assert caught.value.retryable is (failure == "storage")
        assert delays == ([] if failure == "validation" else [1.0, 2.0])
        assert len(requests) == (1 if failure == "validation" else 3)
        assert all(request == requests[0] for request in requests)
        response = query.get("/api/v1/measurements")
        assert response.status_code == 200
        assert response.json() == {"items": []}
