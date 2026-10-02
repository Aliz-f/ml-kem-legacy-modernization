"""Show the handshake counter across reuse and local session expiry.

The first Legacy measurement establishes a session. The next two reuse it.
Setting the Gateway clock to that session's expires_at makes the following
measurement establish a new session. GET /metrics is the visible record.
This module does not add a metric.
"""

from __future__ import annotations

import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager


PATH = "/api/v1/measurements"
HANDSHAKE_SUCCESS = 'gateway_mlkem_handshakes_total{result="success"}'
HANDSHAKE_FAILURE = 'gateway_mlkem_handshakes_total{result="failure"}'
REESTABLISH_SUCCESS = 'gateway_session_reestablishments_total{result="success"}'
REESTABLISH_FAILURE = 'gateway_session_reestablishments_total{result="failure"}'
FIRST = 'gateway_secure_message_duration_seconds_count{phase="first"}'
STEADY = 'gateway_secure_message_duration_seconds_count{phase="steady"}'


class _Cloud:
    def __init__(self, server: uvicorn.Server, thread: threading.Thread, url: str) -> None:
        self._server = server
        self._thread = thread
        self.url = url

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)


def _serve(tmp_path: Path) -> _Cloud:
    app = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / 'cloud.db'}",
                "SECURITY_MODE": "mlkem",
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="pqc-observability-cloud", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            raise RuntimeError("Cloud did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        raise RuntimeError("Cloud has no socket")
    return _Cloud(server, thread, f"http://127.0.0.1:{sockets[0].getsockname()[1]}")


def _payload(sequence_number: int) -> dict[str, object]:
    return {
        "device_id": "sensor-001",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T13:45:31Z",
        "sequence_number": sequence_number,
    }


def _count(scrape: str, sample: str) -> int:
    matches = [line for line in scrape.splitlines() if line.startswith(sample + " ")]
    assert len(matches) == 1, sample
    return int(matches[0].rsplit(" ", 1)[1])


def _post(client: TestClient, sequence_number: int) -> None:
    response = client.post(PATH, json=_payload(sequence_number))
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert "session_id" not in response.text
    assert "nonce" not in response.text


def test_handshake_counter_shows_reuse_then_expiry(tmp_path: Path) -> None:
    """The scrape shows one handshake, reuse, then a second handshake after expiry."""
    cloud = _serve(tmp_path)
    now = [datetime(2026, 9, 21, 12, 0, tzinfo=timezone.utc)]
    metrics = PqcMetrics()
    try:
        config = load_config(
            {
                "SECURITY_MODE": "mlkem",
                "CLOUD_URL": cloud.url,
                "GATEWAY_ID": "gateway-001",
                "LOG_LEVEL": "WARNING",
                "CLOUD_MAX_RETRIES": "0",
            }
        )
        sessions = SessionManager(
            config.gateway_id,
            cloud.url,
            config.cloud_timeout_seconds,
            clock=lambda: now[0],
            metrics=metrics,
        )
        secure = SecureTransport(
            sessions,
            cloud_url=cloud.url,
            timeout_seconds=config.cloud_timeout_seconds,
            max_retries=0,
            metrics=metrics,
            sleep=lambda _delay: None,
        )
        with TestClient(
            create_app(config, pqc_metrics=metrics, secure_transport=secure)
        ) as client:
            _post(client, 1)
            opened = client.get("/metrics")
            assert opened.status_code == 200
            first = opened.text
            _post(client, 2)
            _post(client, 3)
            reused = client.get("/metrics").text
            held = sessions._session
            assert held is not None
            now[0] = held.expires_at
            _post(client, 4)
            expired = client.get("/metrics").text
    finally:
        cloud.stop()

    assert _count(first, HANDSHAKE_SUCCESS) == 1
    assert _count(first, HANDSHAKE_FAILURE) == 0
    assert _count(first, "gateway_active_session") == 1
    assert _count(first, "gateway_pqc_fallback_total") == 0
    assert _count(first, REESTABLISH_SUCCESS) == 0
    assert _count(first, FIRST) == 1
    assert _count(first, STEADY) == 0
    assert "session_id" not in first
    assert "request_id" not in first

    assert _count(reused, HANDSHAKE_SUCCESS) == 1
    assert _count(reused, FIRST) == 1
    assert _count(reused, STEADY) == 2
    assert _count(reused, "gateway_active_session") == 1

    assert _count(expired, HANDSHAKE_SUCCESS) == 2
    assert _count(expired, HANDSHAKE_FAILURE) == 0
    assert _count(expired, REESTABLISH_SUCCESS) == 0
    assert _count(expired, REESTABLISH_FAILURE) == 0
    assert _count(expired, "gateway_active_session") == 1
    assert _count(expired, "gateway_pqc_fallback_total") == 0
    assert _count(expired, FIRST) == 1
    assert _count(expired, STEADY) == 3
    assert metrics.handshakes_succeeded == 2


def test_recorded_scrape_matches_the_observability_note() -> None:
    document = (
        Path(__file__).parents[2] / "edge_gateway" / "docs" / "pqc-observability.md"
    ).read_text(encoding="utf-8")
    readme = (Path(__file__).parents[2] / "edge_gateway" / "README.md").read_text(
        encoding="utf-8"
    )

    assert "It does not add a metric." in document
    assert f"{HANDSHAKE_SUCCESS} 1" in document
    assert f"{HANDSHAKE_SUCCESS} 2" in document
    assert f"{STEADY} 2" in document
    assert f"{STEADY} 3" in document
    assert "gateway_pqc_fallback_total 0" in document
    assert "The scrape does not include a session identifier." in readme
