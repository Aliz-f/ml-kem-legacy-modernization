"""Cloud handshake validation, HTTP error mapping and Gateway compatibility."""

import asyncio
from datetime import datetime, timedelta, timezone
import logging
import socket
from threading import Thread
from time import monotonic, sleep

from fastapi.testclient import TestClient
import pytest
import uvicorn

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.crypto.session import SecureSession, SessionManager, SessionState
from cloud_service.gateway import sessions as routes
from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.aad import build_aad
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.session import SessionManager as GatewaySessions
from edge_gateway.crypto.session_client import parse_session_response
from edge_gateway.crypto.symmetric import encrypt
from cloud_service.crypto.encoding import encode_binary as cloud_encode_binary
from cloud_service.crypto.symmetric import AeadError
from cloud_service.gateway import secure as secure_routes

PATH = "/api/v1/crypto/sessions"


@pytest.fixture
def client():
    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": "sqlite:///:memory:"}))
    with TestClient(app) as client:
        yield client


def handshake(client):
    ciphertext, secret = encapsulate(client.app.state.keys.public_key)
    return {
        "protocol_version": "1", "gateway_id": "gateway-1",
        "key_id": client.app.state.keys.key_id,
        "encapsulation_ciphertext": encode_binary(ciphertext),
    }, derive_session_key(secret)


@pytest.mark.parametrize("padded", [False, True])
def test_handshake_wire_contract_and_no_secret_leak(client, caplog, padded):
    payload, expected_key = handshake(client)
    if padded:
        payload["encapsulation_ciphertext"] += "="
    with caplog.at_level(logging.DEBUG):
        response = client.post(PATH, json=payload)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    body = response.json()
    assert set(body) == {"protocol_version", "session_id", "status", "expires_at"}
    parsed = parse_session_response(body, now=datetime.now(timezone.utc))
    session = client.app.state.sessions.get(parsed.session_id, "gateway-1")
    keys_match = bytes(session.session_key) == expected_key
    assert keys_match
    assert session.cloud_key_id == payload["key_id"]
    assert session.expires_at - session.created_at == timedelta(seconds=300)
    assert session.state == SessionState.ACTIVE
    output = caplog.text + response.text + repr(session)
    assert all(value not in output for value in (repr(expected_key), expected_key.hex(), encode_binary(expected_key)))
    with client.app.state.database.transaction() as connection:
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    assert [row[0] for row in tables] == ["measurements"]
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize(("field", "value", "code"), [
    ("protocol_version", "2", "UNSUPPORTED_PROTOCOL_VERSION"),
    ("protocol_version", 1, "UNSUPPORTED_PROTOCOL_VERSION"),
    ("gateway_id", "", "INVALID_SESSION_REQUEST"),
    ("gateway_id", " g ", "INVALID_SESSION_REQUEST"),
    ("gateway_id", None, "INVALID_SESSION_REQUEST"),
    ("key_id", "old-key", "INVALID_SESSION_REQUEST"),
    ("key_id", None, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "%%%", "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "A" * 1450, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "A" * 1453, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "A" * 1452, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "A" * 1450 + "B", "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "A" * 1450 + "==", "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", "+" * 1451, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", " " * 1451, "INVALID_SESSION_REQUEST"),
    ("encapsulation_ciphertext", None, "INVALID_SESSION_REQUEST"),
])
def test_validation_precedes_crypto(client, monkeypatch, field, value, code):
    payload, _ = handshake(client)
    payload[field] = value
    def unexpected(_):
        pytest.fail("Invalid request reached decapsulation")
    monkeypatch.setattr(client.app.state.keys, "decapsulate", unexpected)
    response = client.post(PATH, json=payload)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == code
    assert len(client.app.state.sessions) == 0


@pytest.mark.parametrize("payload", [{}, [], None, {"protocol_version": "1"}])
def test_missing_fields_or_nonobject(client, payload):
    response = client.post(PATH, json=payload)
    assert response.status_code == 400
    assert len(client.app.state.sessions) == 0


def test_extra_field_and_malformed_json(client):
    payload, _ = handshake(client)
    payload["cloud_id"] = "forbidden"
    assert client.post(PATH, json=payload).status_code == 400
    assert client.post(PATH, content=b"{").status_code == 400
    assert len(client.app.state.sessions) == 0


@pytest.mark.parametrize("stage", ["decapsulate", "kdf", "create", "response"])
def test_operational_failure_never_leaves_usable_session(client, monkeypatch, caplog, stage):
    payload, _ = handshake(client)
    def fail(*args, **kwargs):
        raise RuntimeError("sensitive-failure-marker")
    if stage == "decapsulate":
        monkeypatch.setattr(client.app.state.keys, "decapsulate", fail)
    elif stage == "kdf":
        monkeypatch.setattr(routes, "derive_session_key", fail)
    elif stage == "create":
        monkeypatch.setattr(client.app.state.sessions, "create", fail)
    else:
        monkeypatch.setattr(SecureSession, "response", fail)
    response = client.post(PATH, json=payload)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert len(client.app.state.sessions) == 0
    assert "sensitive-failure-marker" not in response.text + caplog.text


def test_expiry_http_mapping_and_replacement(client):
    now = [datetime.now(timezone.utc)]
    client.app.state.sessions.close()
    client.app.state.sessions = SessionManager(clock=lambda: now[0])
    # Test-only route exercises the production error handler; no secure API added.
    @client.app.get("/test-session/{session_id}/{gateway_id}")
    def probe(session_id: str, gateway_id: str):
        client.app.state.sessions.get(session_id, gateway_id)
        return {"active": True}
    payload, _ = handshake(client)
    first = client.post(PATH, json=payload).json()
    path = f"/test-session/{first['session_id']}"
    assert client.get(path + "/gateway-1").status_code == 200
    now[0] += timedelta(seconds=300)
    wrong = client.get(path + "/other")
    assert (wrong.status_code, wrong.json()["error"]["code"]) == (400, "SECURE_MESSAGE_REJECTED")
    expired = client.get(path + "/gateway-1")
    assert (expired.status_code, expired.json()["error"]["code"]) == (409, "SESSION_EXPIRED")
    missing = client.get(path + "/gateway-1")
    assert (missing.status_code, missing.json()["error"]["code"]) == (409, "SESSION_INVALID")
    payload, _ = handshake(client)
    second = client.post(PATH, json=payload).json()
    assert first["session_id"] != second["session_id"]
    assert client.get(f"/test-session/{second['session_id']}/gateway-1").status_code == 200


def test_shutdown_and_classical_mode():
    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": "sqlite:///:memory:"}))
    with pytest.raises(RuntimeError, match="exit"):
        with TestClient(app) as client:
            payload, _ = handshake(client)
            body = client.post(PATH, json=payload).json()
            manager = app.state.sessions
            database = app.state.database
            session = manager.get(body["session_id"], "gateway-1")
            raise RuntimeError("exit")
    assert app.state.sessions is None
    assert database.closed
    assert len(manager) == 0
    assert session.state == SessionState.CLOSED
    assert session.session_key == bytearray(32)
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        assert client.post(PATH, json={}).status_code == 503
        assert client.app.state.sessions is None


def test_synthetic_secret_markers_never_appear_in_cloud_logs(client, monkeypatch, caplog):
    """Exercise key generation, decapsulation/KDF/session creation and AEAD failure safely."""
    from cloud_service.crypto import keys as keys_module

    private_marker = "synthetic-private-key-marker"
    shared_marker = b"synthetic-shared-secret-marker".ljust(32, b"-")

    class MarkerPrivateKey:
        marker = private_marker

        def close(self):
            return None

    with caplog.at_level(logging.DEBUG, logger="cloud_service"):
        monkeypatch.setattr(keys_module.mlkem, "generate_keypair", lambda: (b"public", MarkerPrivateKey()))
        keys_module.KeyService().close()  # Key generation must not write the marker to Cloud logs.
        payload, _ = handshake(client)
        monkeypatch.setattr(client.app.state.keys, "decapsulate", lambda _ciphertext: shared_marker)
        established = client.post(PATH, json=payload)
        session_id = established.json()["session_id"]
        session = client.app.state.sessions.get(session_id, "gateway-1")
        session_key = bytes(session.session_key)
        canonical = b'{"device_id":"sensor-secret","gateway_id":"gateway-1","temperature_c":22.5,"humidity_pct":44.0,"sequence_number":1,"measured_at":"2026-09-21T12:00:00Z","received_at":"2026-09-21T12:00:01Z"}'
        metadata = {"protocol_version": "1", "gateway_id": "gateway-1", "session_id": session_id, "request_id": "req-secret"}
        nonce = b"\x01" * 12
        wire = metadata | {
            "nonce": cloud_encode_binary(nonce),
            "ciphertext": cloud_encode_binary(encrypt(session_key, nonce, canonical, build_aad(**metadata))),
        }
        assert client.post("/api/v1/secure/measurements", json=wire).status_code == 202
        monkeypatch.setattr(secure_routes, "decrypt", lambda *_: (_ for _ in ()).throw(AeadError("synthetic-session-key-marker")))
        assert client.post("/api/v1/secure/measurements", json=wire | {"request_id": "req-secret-failure"}).status_code == 400

    output = caplog.text
    for marker in (private_marker, shared_marker.decode(), session_key.hex(), encode_binary(session_key), "synthetic-session-key-marker"):
        assert marker not in output


def test_session_initialization_failure_releases_keys(monkeypatch, caplog):
    from cloud_service import app as module
    from cloud_service.app import StartupError
    keys = []
    original = module.KeyService
    def key_service():
        result = original()
        keys.append(result)
        return result
    def fail(*args):
        raise RuntimeError("sensitive-startup-marker")
    monkeypatch.setattr(module, "KeyService", key_service)
    monkeypatch.setattr(module, "SessionManager", fail)
    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": "sqlite:///:memory:"}))
    with pytest.raises(StartupError):
        with TestClient(app):
            pytest.fail("Session manager initialization failure must abort startup")
    assert keys[0].closed
    assert app.state.keys is app.state.sessions is app.state.database is None
    assert not app.state.running
    assert "sensitive-startup-marker" not in caplog.text


def test_existing_gateway_session_client_over_real_http():
    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": "sqlite:///:memory:"}))
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(app, log_config=None, access_log=False))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        gateway = None
        try:
            deadline = monotonic() + 10
            while not server.started and thread.is_alive() and monotonic() < deadline:
                sleep(0.01)
            assert server.started
            gateway = GatewaySessions("gateway-live", f"http://127.0.0.1:{listener.getsockname()[1]}", 5)
            local = asyncio.run(gateway.get_or_establish())
            remote = app.state.sessions.get(local.session_id, "gateway-live")
            keys_match = local.session_key == remote.session_key
            assert keys_match
            assert local.expires_at == remote.expires_at
            assert local.cloud_key_id == remote.cloud_key_id
        finally:
            if gateway is not None:
                gateway.close()
            server.should_exit = True
            thread.join(10)
            assert not thread.is_alive()
