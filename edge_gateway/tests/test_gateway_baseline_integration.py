"""M2-16/17: baseline HTTP boundaries and Legacy-to-SQLite field preservation."""

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
from edge_gateway.app import create_app as create_gateway
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


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

    with live_service(app, "cloud_service") as (url, query):
        yield app, url, query, requests


@contextmanager
def live_service(app, logger_name):
    """Serve a production app on an isolated port with bounded startup/shutdown."""
    logger = logging.getLogger(logger_name)
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
            assert server.started, f"{logger_name} failed to start"
            url = f"http://127.0.0.1:{listener.getsockname()[1]}"
            with httpx.Client(base_url=url, timeout=5, trust_env=False) as query:
                assert query.get("/health").status_code == 200
                # Readiness remains a placeholder in the current application.
                assert query.get("/ready").status_code == 503
                yield url, query
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            logger.setLevel(previous_level)
            assert not thread.is_alive(), f"{logger_name} failed to stop"


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


@contextmanager
def live_baseline_gateway(cloud_url):
    """Use the app's production composition, including its real baseline client."""
    app = create_gateway(load_gateway_config({
        "GATEWAY_ID": "gateway-e2e",
        "CLOUD_URL": cloud_url,
        "SECURITY_MODE": "classical",
        "CLOUD_TIMEOUT_SECONDS": "5",
        "CLOUD_MAX_RETRIES": "0",
    }))
    with live_service(app, "edge_gateway") as (url, _):
        yield GatewayClient(url, request_timeout_seconds=5, max_retries=0)


@pytest.mark.parametrize(("temperature", "humidity", "timestamp"), [
    (22.5, 44.0, "2026-09-21T12:00:00Z"),  # Roadmap Phase 5 fixture.
    (-40.0, 0.0, "2026-09-21T12:00:00.123456Z"),
    (85.0, 100.0, "2026-09-21T12:00:00Z"),
])
def test_legacy_to_sqlite_preserves_gateway_transformations(
    tmp_path, caplog, temperature, humidity, timestamp,
):
    measurement = Measurement(
        device_id="sensor-test", temperature_c=temperature, humidity_pct=humidity,
        timestamp=datetime.fromisoformat(timestamp), sequence_number=1,
    )
    payload = measurement.to_payload()
    assert payload == {
        "device_id": "sensor-test", "temperature_c": temperature,
        "humidity_pct": humidity, "timestamp": timestamp, "sequence_number": 1,
    }
    database_path = tmp_path / "e2e.db"
    with caplog.at_level(logging.INFO, logger="cloud_service"):
        with live_cloud(database_path) as (_, cloud_url, query, requests):
            with live_baseline_gateway(cloud_url) as legacy:
                started = datetime.now(timezone.utc)
                result = legacy.send(payload)
                finished = datetime.now(timezone.utc)
                assert result.success and result.status_code == 202
                assert result.attempt_count == 1

                # Query immediately after Legacy acceptance: persistence is synchronous.
                listing = query.get("/api/v1/measurements")
                assert listing.status_code == 200
                [row] = listing.json()["items"]
                assert len(requests) == 1
                path, request_id, body = requests[0]
                assert path == "/api/v1/baseline/measurements"
                assert isinstance(request_id, str) and request_id.strip()
                canonical = json.loads(body)
                assert canonical == {
                    "device_id": payload["device_id"],
                    "temperature_c": payload["temperature_c"],
                    "humidity_pct": payload["humidity_pct"],
                    "measured_at": payload["timestamp"],
                    "sequence_number": payload["sequence_number"],
                    "received_at": canonical["received_at"],
                    "gateway_id": "gateway-e2e",
                }
                received_at = datetime.fromisoformat(canonical["received_at"])
                assert started <= received_at <= finished
                expected = dict(canonical)
                expected["gateway_received_at"] = expected.pop("received_at")
                assert set(row) == set(expected) | {"record_id", "cloud_received_at"}
                for field, value in expected.items():
                    if field in {"measured_at", "gateway_received_at"}:
                        assert datetime.fromisoformat(row[field]) == datetime.fromisoformat(value)
                    else:
                        assert row[field] == value
                assert received_at <= datetime.fromisoformat(row["cloud_received_at"]) <= finished
                assert row["record_id"]
                detail = query.get(f"/api/v1/measurements/{row['record_id']}")
                assert detail.status_code == 200
                assert detail.json() == row
                assert any(
                    record.name == "cloud_service" and record.getMessage() == (
                        f"measurement_accepted request_id={request_id!r} "
                        f"record_id={row['record_id']}"
                    ) for record in caplog.records
                )

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        persisted = [dict(record) for record in connection.execute("SELECT * FROM measurements")]
    assert persisted == [row]


def test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(tmp_path):
    payload = Measurement(
        device_id="sensor-test", temperature_c=22.5, humidity_pct=44.0,
        timestamp=datetime.fromisoformat("2026-09-21T12:00:00Z"), sequence_number=1,
    ).to_payload()
    with live_cloud(tmp_path / "e2e-failures.db") as (app, cloud_url, query, requests):
        with live_baseline_gateway(cloud_url) as legacy:
            invalid = legacy.send({**payload, "humidity_pct": 101.0})
            assert not invalid.success and invalid.status_code == 422
            assert invalid.attempt_count == 1 and not invalid.retryable
            assert requests == []

            # Fail real persistence; Gateway must not return 202 or undo sequence 1.
            with app.state.database.transaction() as connection:
                connection.execute("PRAGMA query_only = ON")
            failed = legacy.send(payload)
            assert not failed.success and failed.status_code == 503
            assert failed.attempt_count == 1 and failed.retryable
            assert len(requests) == 1
            assert query.get("/api/v1/measurements").json() == {"items": []}
            with app.state.database.transaction() as connection:
                connection.execute("PRAGMA query_only = OFF")

            for sequence in (1, 0):
                rejected = legacy.send({**payload, "sequence_number": sequence})
                assert not rejected.success and rejected.status_code == 409
                assert rejected.attempt_count == 1 and not rejected.retryable
            assert len(requests) == 1

            # A higher sequence still succeeds; invalid input did not consume it.
            invalid = legacy.send({**payload, "sequence_number": 3, "humidity_pct": 101.0})
            assert invalid.status_code == 422
            accepted = legacy.send({**payload, "sequence_number": 3})
            assert accepted.success and accepted.status_code == 202
            assert len(requests) == 2
            assert requests[0][1] != requests[1][1]
            [row] = query.get("/api/v1/measurements").json()["items"]
            assert row["sequence_number"] == 3
            assert row["temperature_c"] == payload["temperature_c"]
            assert row["humidity_pct"] == payload["humidity_pct"]
