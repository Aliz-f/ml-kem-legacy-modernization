"""M5-34 production Gateway-to-Cloud secure-session integration coverage."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import Request
from fastapi.testclient import TestClient

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from edge_gateway.crypto.encoding import decode_binary


@contextmanager
def serve(app, name: str):
    """Serve one production ASGI application on an isolated local port."""
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


def _query_one(cloud_url: str) -> dict[str, object]:
    with urllib.request.urlopen(f"{cloud_url}/api/v1/measurements", timeout=5) as response:
        assert response.status == 200
        payload = json.loads(response.read())
    assert isinstance(payload, dict)
    items = payload["items"]
    assert isinstance(items, list) and len(items) == 1
    row = items[0]
    assert isinstance(row, dict)
    return row


def test_gateway_secure_session_encrypts_and_delivers_to_live_cloud(tmp_path: Path) -> None:
    """Use real HTTP for every Gateway-to-Cloud protocol exchange."""
    payload = {
        "device_id": "sensor-secure-e2e",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": 1,
    }
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / 'secure.db').as_posix()}",
                "SECURITY_MODE": "mlkem",
                "FAILURE_MODE": "none",
            }
        )
    )
    requests: list[tuple[str, str, bytes]] = []

    @cloud.middleware("http")
    async def capture_gateway_protocol(request: Request, call_next):
        body = await request.body()
        response = await call_next(request)
        if request.url.path in {
            "/api/v1/crypto/public-key",
            "/api/v1/crypto/sessions",
            "/api/v1/secure/measurements",
        }:
            requests.append((request.method, request.url.path, body))
        return response

    with serve(cloud, "m5-34-cloud") as cloud_url:
        gateway = create_gateway_app(
            load_gateway_config(
                {
                    "GATEWAY_ID": "gateway-secure-e2e",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": "mlkem",
                    "PQC_FAILURE_POLICY": "fail_closed",
                    "CLOUD_TIMEOUT_SECONDS": "5",
                    "CLOUD_MAX_RETRIES": "0",
                    "FAILURE_MODE": "none",
                }
            )
        )
        with TestClient(gateway) as client:
            response = client.post("/api/v1/measurements", json=payload)
        stored = _query_one(cloud_url)

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert [(method, path) for method, path, _body in requests] == [
        ("GET", "/api/v1/crypto/public-key"),
        ("POST", "/api/v1/crypto/sessions"),
        ("POST", "/api/v1/secure/measurements"),
    ]
    session_request = json.loads(requests[1][2])
    assert set(session_request) == {
        "protocol_version",
        "gateway_id",
        "key_id",
        "encapsulation_ciphertext",
    }
    assert session_request["protocol_version"] == "1"
    assert session_request["gateway_id"] == "gateway-secure-e2e"
    assert isinstance(session_request["key_id"], str) and session_request["key_id"]
    assert len(decode_binary(session_request["encapsulation_ciphertext"])) == 1088

    envelope = json.loads(requests[2][2])
    assert set(envelope) == {
        "protocol_version", "gateway_id", "session_id", "request_id", "nonce", "ciphertext"
    }
    assert envelope["protocol_version"] == "1"
    assert envelope["gateway_id"] == "gateway-secure-e2e"
    assert isinstance(envelope["session_id"], str) and envelope["session_id"].startswith("sess-")
    assert isinstance(envelope["request_id"], str) and envelope["request_id"].startswith("req-")
    assert len(decode_binary(envelope["nonce"])) == 12
    assert decode_binary(envelope["ciphertext"])
    assert json.dumps(payload, separators=(",", ":")).encode() not in requests[2][2]
    assert "device_id" not in envelope
    assert "message_counter" not in envelope

    assert stored["device_id"] == payload["device_id"]
    assert stored["temperature_c"] == payload["temperature_c"]
    assert stored["humidity_pct"] == payload["humidity_pct"]
    assert stored["sequence_number"] == payload["sequence_number"]
    assert stored["gateway_id"] == "gateway-secure-e2e"
    assert datetime.fromisoformat(str(stored["measured_at"])) == datetime.fromisoformat(
        payload["timestamp"]
    )
    assert datetime.fromisoformat(str(stored["gateway_received_at"])).utcoffset() is not None
    assert datetime.fromisoformat(str(stored["cloud_received_at"])).utcoffset() is not None
