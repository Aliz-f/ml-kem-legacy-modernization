"""M5-33 orchestration of the valid Gateway-to-Cloud ML-KEM session path.

This is deliberately limited to public-key retrieval and session establishment.
Secure-message delivery is the separate M5-34 acceptance scope.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
from pathlib import Path

import pytest
import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from cloud_service.crypto.encoding import decode_binary
from cloud_service.crypto.kdf import derive_session_key as cloud_derive_session_key
from edge_gateway.crypto.kdf import (
    SESSION_KEY_INFO,
    SESSION_KEY_LENGTH,
    derive_session_key as gateway_derive_session_key,
)
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.session import SessionManager, SessionState


class LiveCloud:
    """Production Cloud app running on a disposable loopback port."""

    def __init__(self, app, url: str, server: uvicorn.Server, thread: threading.Thread) -> None:
        self.app = app
        self.url = url
        self._server = server
        self._thread = thread

    def close(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)
        if self._thread.is_alive():
            raise RuntimeError("Cloud did not stop")


@pytest.fixture
def cloud(tmp_path: Path) -> LiveCloud:
    app = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / 'sessions.db').as_posix()}",
                "SECURITY_MODE": "mlkem",
                "FAILURE_MODE": "none",
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    app.state.handshake_requests = []

    @app.middleware("http")
    async def observe_handshake(request: Request, call_next):
        body = await request.body()
        response = await call_next(request)
        if request.url.path in {"/api/v1/crypto/public-key", "/api/v1/crypto/sessions"}:
            app.state.handshake_requests.append((request.url.path, body))
        return response

    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="m5-33-cloud", daemon=True)
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
    instance = LiveCloud(app, f"http://127.0.0.1:{sockets[0].getsockname()[1]}", server, thread)
    try:
        yield instance
    finally:
        instance.close()


def test_valid_mlkem_handshake_uses_the_frozen_session_contract(
    cloud: LiveCloud, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Compare key material only in memory and assert it never reaches HTTP/logs."""
    captured: dict[str, bytes] = {}
    real_encapsulate = encapsulate

    def remember_encapsulation(public_key: bytes) -> tuple[bytes, bytes]:
        ciphertext, shared_secret = real_encapsulate(public_key)
        captured["ciphertext"] = ciphertext
        captured["shared_secret"] = shared_secret
        return ciphertext, shared_secret

    caplog.set_level(logging.DEBUG)
    monkeypatch.setattr("edge_gateway.crypto.session.encapsulate", remember_encapsulation)
    gateway = SessionManager("gateway-m5-33", cloud.url, timeout_seconds=5)

    session = asyncio.run(gateway.get_or_establish())

    requests: list[tuple[str, bytes]] = cloud.app.state.handshake_requests
    assert [path for path, _body in requests] == [
        "/api/v1/crypto/public-key",
        "/api/v1/crypto/sessions",
    ]
    session_request = json.loads(requests[1][1])
    assert set(session_request) == {
        "protocol_version",
        "gateway_id",
        "key_id",
        "encapsulation_ciphertext",
    }
    assert session_request["protocol_version"] == "1"
    assert session_request["gateway_id"] == "gateway-m5-33"
    assert session_request["key_id"] == cloud.app.state.keys.key_id
    assert decode_binary(session_request["encapsulation_ciphertext"]) == captured["ciphertext"]
    assert "shared_secret" not in session_request
    assert "session_key" not in session_request

    cloud_secret = cloud.app.state.keys.decapsulate(captured["ciphertext"])
    assert captured["shared_secret"] == cloud_secret
    gateway_key = gateway_derive_session_key(captured["shared_secret"])
    cloud_key = cloud_derive_session_key(cloud_secret)
    assert gateway_key == cloud_key
    assert SESSION_KEY_INFO == b"ml-kem-project:v1:gateway-cloud-session"
    assert SESSION_KEY_LENGTH == 32

    [cloud_session] = cloud.app.state.sessions._sessions.values()
    assert session.state is SessionState.ACTIVE
    assert session.gateway_id == cloud_session.gateway_id == "gateway-m5-33"
    assert session.cloud_key_id == cloud_session.cloud_key_id == cloud.app.state.keys.key_id
    assert session.session_id == cloud_session.session_id
    assert session.expires_at == cloud_session.expires_at
    assert bytes(session.session_key) == bytes(cloud_session.session_key) == gateway_key
    assert captured["shared_secret"].hex() not in caplog.text
    assert gateway_key.hex() not in caplog.text
