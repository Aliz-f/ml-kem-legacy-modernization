"""Secure ingestion acceptance gates, error ordering and no plaintext fallback."""

from datetime import datetime, timedelta, timezone
import asyncio
import json
import logging

from fastapi.testclient import TestClient
import pytest
from starlette.requests import Request

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.crypto.envelope_validation import MAX_ENVELOPE_BYTES, EnvelopeValidationError, validate_envelope
from cloud_service.crypto.session import SessionManager
from cloud_service.crypto.session import SessionAccessError
from cloud_service.crypto.encoding import decode_binary
from cloud_service.crypto.symmetric import AeadError
from cloud_service.gateway import secure
from edge_gateway.crypto.aad import build_aad
from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.symmetric import encrypt, generate_nonce

PATH = "/api/v1/secure/measurements"


def canonical():
    return dict(device_id="sensor-1", temperature_c=21.7, humidity_pct=42.5,
                measured_at="2026-09-30T12:00:00Z", sequence_number=1,
                received_at="2026-09-30T12:00:01Z", gateway_id="gateway-1")


@pytest.fixture
def client(tmp_path):
    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": f"sqlite:///{(tmp_path / 'secure.db').as_posix()}"}))
    with TestClient(app) as client:
        yield client


def establish(client):
    ciphertext, secret = encapsulate(client.app.state.keys.public_key)
    response = client.post("/api/v1/crypto/sessions", json={
        "protocol_version": "1", "gateway_id": "gateway-1", "key_id": client.app.state.keys.key_id,
        "encapsulation_ciphertext": encode_binary(ciphertext),
    })
    assert response.status_code == 200
    return response.json()["session_id"], derive_session_key(secret)


def envelope(client):
    session_id, key = establish(client)
    return build_secure_envelope(key=key, session_id=session_id, request_id="req-1", **canonical()).as_dict()


def forbid(*args, **kwargs):
    pytest.fail("Rejected input reached a forbidden processing stage")


def test_gateway_envelope_persistence_query_and_identical_retry(client, caplog):
    wire = envelope(client)
    with caplog.at_level(logging.DEBUG):
        first = client.post(PATH, json=wire)
        repeat = client.post(PATH, json=wire)
    assert first.status_code == repeat.status_code == 202
    assert first.json()["status"] == "accepted"
    assert repeat.json() == {"status": "already_accepted", "record_id": first.json()["record_id"]}
    row = client.get(f"/api/v1/measurements/{first.json()['record_id']}").json()
    expected = canonical()
    expected["gateway_received_at"] = expected.pop("received_at")
    for field, value in expected.items():
        if field.endswith("_at"):
            assert datetime.fromisoformat(row[field]) == datetime.fromisoformat(value)
        else:
            assert row[field] == value
    assert "request_id" not in row
    assert "cloud_received_at" in row
    assert len(client.get("/api/v1/measurements").json()["items"]) == 1
    assert "request_id='req-1'" in caplog.text
    assert wire["ciphertext"] not in caplog.text and wire["nonce"] not in caplog.text


@pytest.mark.parametrize(("field", "value", "code"), [
    ("protocol_version", "2", "UNSUPPORTED_PROTOCOL_VERSION"),
    ("gateway_id", "", "SECURE_MESSAGE_REJECTED"),
    ("gateway_id", " gw ", "SECURE_MESSAGE_REJECTED"),
    ("session_id", "", "SECURE_MESSAGE_REJECTED"),
    ("request_id", "", "SECURE_MESSAGE_REJECTED"),
    ("nonce", "%%%", "SECURE_MESSAGE_REJECTED"),
    ("nonce", encode_binary(b"x" * 11), "SECURE_MESSAGE_REJECTED"),
    ("nonce", encode_binary(b"x" * 13), "SECURE_MESSAGE_REJECTED"),
    ("nonce", "+" * 16, "SECURE_MESSAGE_REJECTED"),
    ("ciphertext", "", "SECURE_MESSAGE_REJECTED"),
    ("ciphertext", "AB==", "SECURE_MESSAGE_REJECTED"),
    ("ciphertext", "YQ=", "SECURE_MESSAGE_REJECTED"),
    ("ciphertext", "Y Q==", "SECURE_MESSAGE_REJECTED"),
    ("ciphertext", None, "SECURE_MESSAGE_REJECTED"),
])
def test_invalid_envelope_rejected_before_lookup(client, monkeypatch, field, value, code):
    wire = envelope(client) | {field: value}
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    monkeypatch.setattr(secure, "decrypt", forbid)
    response = client.post(PATH, json=wire)
    assert (response.status_code, response.json()["error"]["code"]) == (400, code)
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize("body", [b"{", b"[]", b"null", b"\xff", b'{"x":1,"x":2}', b'{"x":NaN}', b"[" * 2000])
def test_malformed_json_stops_before_lookup(client, monkeypatch, body):
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    response = client.post(PATH, content=body, headers={"Content-Type": "application/json"})
    assert response.status_code == 400


def test_extra_missing_and_duplicate_fields(client, monkeypatch):
    wire = envelope(client)
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    assert client.post(PATH, json=wire | {"message_counter": 1}).status_code == 400
    assert client.post(PATH, json={key: value for key, value in wire.items() if key != "nonce"}).status_code == 400
    duplicate = json.dumps(wire)[:-1] + ',"request_id":"again"}'
    assert client.post(PATH, content=duplicate, headers={"Content-Type": "application/json"}).status_code == 400


def test_size_exact_boundary_and_streamed_overflow(client, monkeypatch):
    wire = envelope(client)
    raw = json.dumps(wire).encode()
    exact = raw + b" " * (MAX_ENVELOPE_BYTES - len(raw))
    assert client.post(PATH, content=exact, headers={"Content-Type": "application/json"}).status_code == 202
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    assert client.post(PATH, content=exact + b" ", headers={"Content-Type": "application/json"}).status_code == 400
    def chunks():
        yield exact
        yield b" "
    assert client.post(PATH, content=chunks(), headers={"Content-Type": "application/json"}).status_code == 400
    with pytest.raises(EnvelopeValidationError):
        validate_envelope(exact + b" ")


@pytest.mark.parametrize("which", ["nonce", "ciphertext", "request_id"])
def test_authentication_failure_never_parses_or_stores(client, monkeypatch, which):
    wire = envelope(client)
    if which == "request_id":
        wire[which] = "changed"
    else:
        wire[which] = ("A" if wire[which][0] != "A" else "B") + wire[which][1:]
    monkeypatch.setattr(secure, "validate_measurement", forbid)
    monkeypatch.setattr(client.app.state.repository, "save_idempotent", forbid)
    response = client.post(PATH, json=wire)
    assert (response.status_code, response.json()["error"]["code"]) == (400, "SECURE_MESSAGE_REJECTED")


def test_stream_reader_stops_at_limit_without_consuming_remainder(client, monkeypatch):
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    chunks = iter([b" " * MAX_ENVELOPE_BYTES, b"x"])
    reads = []
    async def receive():
        chunk = next(chunks)
        reads.append(len(chunk))
        return {"type": "http.request", "body": chunk, "more_body": True}
    request = Request({"type": "http", "method": "POST", "path": PATH,
                       "headers": [(b"content-type", b"application/json")], "app": client.app}, receive)
    response = asyncio.run(secure.secure_measurement(request))
    assert response.status_code == 400
    assert reads == [MAX_ENVELOPE_BYTES, 1]


def test_correctly_padded_base64url_is_accepted(client):
    wire = envelope(client)
    for field in ("nonce", "ciphertext"):
        wire[field] += "=" * (-len(wire[field]) % 4)
    assert client.post(PATH, json=wire).status_code == 202


def test_session_lookup_ownership_expiry_order(client, monkeypatch):
    now = [datetime.now(timezone.utc)]
    client.app.state.sessions.close()
    client.app.state.sessions = SessionManager(clock=lambda: now[0])
    wire = envelope(client)
    monkeypatch.setattr(secure, "decrypt", forbid)
    missing = client.post(PATH, json=wire | {"session_id": "missing"})
    assert (missing.status_code, missing.json()["error"]["code"]) == (409, "SESSION_INVALID")
    assert missing.json() == {"error": {"code": "SESSION_INVALID", "message": "secure session is invalid"}}
    now[0] += timedelta(seconds=300)
    wrong = client.post(PATH, json=wire | {"gateway_id": "other"})
    assert (wrong.status_code, wrong.json()["error"]["code"]) == (400, "SECURE_MESSAGE_REJECTED")
    expired = client.post(PATH, json=wire)
    assert (expired.status_code, expired.json()["error"]["code"]) == (409, "SESSION_EXPIRED")
    assert expired.json() == {"error": {"code": "SESSION_EXPIRED", "message": "secure session has expired"}}
    assert len(client.app.state.sessions) == 0
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize("plaintext", [b"not JSON", b"\xff", b"[]", b"{}", b'{"x":1,"x":2}',
    json.dumps(canonical() | {"humidity_pct": 101}).encode(),
    json.dumps(canonical() | {"gateway_id": "other"}).encode()])
def test_authenticated_invalid_measurement_is_not_stored(client, monkeypatch, plaintext):
    session_id, key = establish(client)
    metadata = dict(protocol_version="1", gateway_id="gateway-1", session_id=session_id, request_id="req-invalid")
    nonce = generate_nonce()
    wire = metadata | {"nonce": encode_binary(nonce), "ciphertext": encode_binary(encrypt(key, nonce, plaintext, build_aad(**metadata)))}
    monkeypatch.setattr(client.app.state.repository, "save_idempotent", forbid)
    response = client.post(PATH, json=wire)
    assert (response.status_code, response.json()["error"]["code"]) == (422, "INVALID_MEASUREMENT")
    assert response.json() == {"error": {"code": "INVALID_MEASUREMENT", "message": "measurement validation failed"}}


def test_storage_failure_real_sqlite_and_safe_internal_failure(client, monkeypatch, caplog):
    wire = envelope(client)
    with client.app.state.database.transaction() as connection:
        connection.execute("PRAGMA query_only = ON")
    try:
        response = client.post(PATH, json=wire)
        assert (response.status_code, response.json()["error"]["code"]) == (503, "STORAGE_UNAVAILABLE")
        assert response.json() == {"error": {"code": "STORAGE_UNAVAILABLE", "message": "storage is unavailable"}}
        assert client.app.state.repository.list() == []
    finally:
        with client.app.state.database.transaction() as connection:
            connection.execute("PRAGMA query_only = OFF")
    def fail(*args):
        raise RuntimeError("sensitive-marker")
    monkeypatch.setattr(client.app.state.repository, "save_idempotent", fail)
    response = client.post(PATH, json=wire)
    assert (response.status_code, response.json()["error"]["code"]) == (500, "INTERNAL_ERROR")
    assert response.json() == {"error": {"code": "INTERNAL_ERROR", "message": "internal error"}}
    assert "sensitive-marker" not in caplog.text + response.text


def test_plaintext_never_falls_back(client, monkeypatch):
    monkeypatch.setattr(client.app.state.sessions, "get", forbid)
    monkeypatch.setattr(client.app.state.repository, "save_idempotent", forbid)
    assert client.post(PATH, json=canonical()).status_code == 400
    assert client.post("/api/v1/baseline/measurements", json=canonical()).status_code == 503
    assert client.post(PATH, content=json.dumps(canonical()), headers={"Content-Type": "text/plain"}).status_code == 400


def test_classical_accepts_only_baseline_and_secure_unavailable():
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        assert client.post(PATH, json=canonical()).status_code == 503
        assert client.post("/api/v1/baseline/measurements", json=canonical()).status_code == 202
        assert len(client.app.state.repository.list()) == 1


def test_success_contract_survives_new_session_and_request_id(client):
    first = client.post(PATH, json=envelope(client))
    assert first.status_code == 202
    record_id = first.json()["record_id"]
    assert first.json() == {"status": "accepted", "record_id": record_id}
    assert isinstance(record_id, str) and record_id.startswith("rec-")
    session_id, key = establish(client)
    retry = build_secure_envelope(key=key, session_id=session_id, request_id="new-request", **canonical()).as_dict()
    duplicate = client.post(PATH, json=retry)
    assert duplicate.status_code == 202
    assert duplicate.json() == {"status": "already_accepted", "record_id": record_id}
    assert len(client.app.state.repository.list()) == 1


@pytest.mark.parametrize("failure", ["syntax", "encoding", "ownership", "authentication"])
def test_rejection_has_one_public_message(client, monkeypatch, caplog, failure):
    wire = envelope(client)
    if failure == "syntax":
        wire.pop("nonce")
    elif failure == "encoding":
        wire["nonce"] = "unsafe-binary-marker!"
    elif failure == "ownership":
        wire["gateway_id"] = "another-owner"
    else:
        def fail(*args):
            raise AeadError("sensitive-vendor-diagnostic")
        monkeypatch.setattr(secure, "decrypt", fail)
    response = client.post(PATH, json=wire)
    assert response.status_code == 400
    assert response.json() == {"error": {"code": "SECURE_MESSAGE_REJECTED",
        "message": "secure message could not be processed"}}
    assert "sensitive-vendor-diagnostic" not in response.text + caplog.text
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize(("code", "message"), [
    ("SESSION_INVALID", "secure session is invalid"),
    ("SESSION_EXPIRED", "secure session has expired"),
])
def test_session_http_handler_never_echoes_exception_text(client, monkeypatch, caplog, code, message):
    wire = envelope(client)
    def fail(*args):
        raise SessionAccessError(409, code, "sensitive-session-diagnostic")
    monkeypatch.setattr(client.app.state.sessions, "get", fail)
    response = client.post(PATH, json=wire)
    assert response.status_code == 409
    assert response.json() == {"error": {"code": code, "message": message}}
    assert "sensitive-session-diagnostic" not in response.text + caplog.text


def test_published_public_key_round_trip_and_handshake(client):
    public = client.get("/api/v1/crypto/public-key").json()
    decoded = decode_binary(public["public_key"])
    assert decoded == client.app.state.keys.public_key
    assert len(decoded) == 1184
    assert "=" not in public["public_key"]
    # Existing helper uses the unchanged Gateway encoder for the ML-KEM ciphertext.
    assert client.post(PATH, json=envelope(client)).status_code == 202
