"""M5-47 through M5-51 live trace, log-safety, and metrics integration checks."""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pytest
import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


@contextmanager
def _serve(app, name: str):
    """Serve one production ASGI app on an isolated loopback port."""
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name=name, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            thread.join(timeout=5)
            raise RuntimeError(f"{name} did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError(f"{name} has no listening socket")
    try:
        yield f"http://127.0.0.1:{sockets[0].getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        if thread.is_alive():
            raise RuntimeError(f"{name} did not stop")


def _get_json(url: str) -> dict[str, object]:
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.status == 200
        payload = json.loads(response.read())
    assert isinstance(payload, dict)
    return payload


def _get_metrics(url: str) -> str:
    with urllib.request.urlopen(f"{url}/metrics", timeout=5) as response:
        assert response.status == 200
        assert response.headers["Content-Type"].startswith("text/plain")
        return response.read().decode("utf-8")


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
def test_live_end_to_end_trace_is_correlated_safe_and_observable(
    tmp_path: Path,
    security_mode: str,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Trace one sequence-42 measurement across both frozen transport modes."""
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / f'{security_mode}.db'}",
                "SECURITY_MODE": security_mode,
                "LOG_LEVEL": "INFO",
            }
        )
    )
    forwarded: list[dict[str, object]] = []

    @cloud.middleware("http")
    async def capture_gateway_boundary(request: Request, call_next):
        if request.url.path == "/api/v1/baseline/measurements":
            forwarded.append(
                {
                    "mode": "classical",
                    "request_id": request.headers.get("X-Request-ID"),
                }
            )
        elif request.url.path == "/api/v1/secure/measurements":
            envelope = json.loads(await request.body())
            assert isinstance(envelope, dict)
            forwarded.append(
                {
                    "mode": "mlkem",
                    "request_id": envelope["request_id"],
                    "fields": set(envelope),
                }
            )
        return await call_next(request)

    captured_secret: dict[str, bytes] = {}
    if security_mode == "mlkem":
        real_encapsulate = encapsulate

        def remember_secret(public_key: bytes) -> tuple[bytes, bytes]:
            ciphertext, shared_secret = real_encapsulate(public_key)
            captured_secret["shared_secret"] = shared_secret
            return ciphertext, shared_secret

        monkeypatch.setattr("edge_gateway.crypto.session.encapsulate", remember_secret)

    measurement = Measurement(
        device_id="sensor-observability",
        # A marker that is present in encrypted/plaintext data, never in a safe log event.
        temperature_c=73.987654,
        humidity_pct=44.0,
        timestamp=datetime.fromisoformat("2026-09-21T12:00:00+00:00"),
        sequence_number=42,
    )
    caplog.set_level(logging.INFO)
    with _serve(cloud, f"m5-observability-cloud-{security_mode}") as cloud_url:
        gateway = create_gateway_app(
            load_gateway_config(
                {
                    "GATEWAY_ID": "gateway-observability",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": security_mode,
                    "PQC_FAILURE_POLICY": "fail_closed",
                    "CLOUD_TIMEOUT_SECONDS": "5",
                    "CLOUD_MAX_RETRIES": "0",
                    "LOG_LEVEL": "INFO",
                }
            )
        )
        with _serve(gateway, f"m5-observability-gateway-{security_mode}") as gateway_url:
            result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(
                measurement.to_payload()
            )
            gateway_metrics = _get_metrics(gateway_url)
            cloud_metrics = _get_metrics(cloud_url)
            listing = _get_json(f"{cloud_url}/api/v1/measurements")

    assert result.success and result.status_code == 202
    items = listing["items"]
    assert isinstance(items, list) and len(items) == 1
    stored = items[0]
    assert isinstance(stored, dict)
    assert stored["sequence_number"] == 42
    assert stored["gateway_id"] == "gateway-observability"
    record_id = stored["record_id"]
    assert isinstance(record_id, str) and record_id

    assert len(forwarded) == 1
    trace = forwarded[0]
    request_id = trace["request_id"]
    assert isinstance(request_id, str) and request_id.startswith("req-")
    if security_mode == "classical":
        assert trace == {"mode": "classical", "request_id": request_id}
        assert "cloud_baseline_requests_total 1" in cloud_metrics
        assert "cloud_secure_requests_total 0" in cloud_metrics
    else:
        assert trace == {
            "mode": "mlkem",
            "request_id": request_id,
            "fields": {
                "protocol_version", "gateway_id", "session_id", "request_id", "nonce", "ciphertext",
            },
        }
        assert "cloud_baseline_requests_total 0" in cloud_metrics
        assert "cloud_secure_requests_total 1" in cloud_metrics
        assert "cloud_authenticated_messages_total 1" in cloud_metrics

    assert "gateway_measurements_received_total 1" in gateway_metrics
    assert "gateway_measurements_accepted_total 1" in gateway_metrics
    assert "gateway_cloud_requests_total 1" in gateway_metrics
    assert 'gateway_service_info{security_mode="' + security_mode + '"} 1' in gateway_metrics
    assert 'cloud_service_info{security_mode="' + security_mode + '"} 1' in cloud_metrics
    for metrics in (gateway_metrics, cloud_metrics):
        for forbidden in ("request_id", "session_id", "record_id", "device_id", "gateway_id"):
            assert forbidden not in metrics

    messages = [record.getMessage() for record in caplog.records]
    assert any(
        record.name == "edge_gateway"
        and record.getMessage() == (
            "event=gateway_request_created component=edge_gateway " f"request_id={request_id}"
        )
        for record in caplog.records
    )
    assert any(
        record.name == "cloud_service"
        and "event=measurement_stored component=cloud_service" in record.getMessage()
        and f"request_id={request_id!r}" in record.getMessage()
        and f"record_id={record_id}" in record.getMessage()
        for record in caplog.records
    )

    log_text = "\n".join(messages)
    assert "73.987654" not in log_text
    assert "sensor-observability" in log_text  # Safe correlation/device field, not payload dumping.
    if security_mode == "mlkem":
        shared_secret = captured_secret["shared_secret"]
        session_key = derive_session_key(shared_secret)
        assert shared_secret.hex() not in log_text
        assert session_key.hex() not in log_text
