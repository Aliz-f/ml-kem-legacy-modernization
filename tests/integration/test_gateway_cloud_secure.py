"""Gateway-to-Cloud secure integration for protocol version 1.

The measurement receiver in this module is mounted only on the test
application. It is not a Cloud production route. Cloud's public-key and
session routes are the real ones.

A valid-length ML-KEM ciphertext change is not required to raise, because
ML-KEM may use implicit rejection. Protocol version 1 has no cryptographic
replay counter or window. Duplicate persistence is business idempotency on
(device_id, sequence_number).
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import re
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.crypto.aad import AadError as CloudAadError
from cloud_service.crypto.aad import build_aad as cloud_build_aad
from cloud_service.crypto.kdf import SESSION_KEY_INFO as CLOUD_SESSION_KEY_INFO
from cloud_service.crypto.kdf import SESSION_KEY_LENGTH as CLOUD_SESSION_KEY_LENGTH
from cloud_service.crypto.kdf import derive_session_key as cloud_derive_session_key
from cloud_service.crypto.session import SessionAccessError
from cloud_service.crypto.symmetric import AeadError
from cloud_service.crypto.symmetric import decrypt as cloud_decrypt
from cloud_service.storage.models import StoredMeasurement
from cloud_service.validation import MeasurementValidationError, validate_measurement
from edge_gateway.config import load_config as load_gateway_config
from edge_gateway.crypto.aad import build_aad as gateway_build_aad
from edge_gateway.crypto.encoding import EncodingError, decode_binary, encode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.kdf import SESSION_KEY_INFO as GATEWAY_SESSION_KEY_INFO
from edge_gateway.crypto.kdf import SESSION_KEY_LENGTH as GATEWAY_SESSION_KEY_LENGTH
from edge_gateway.crypto.kdf import derive_session_key as gateway_derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.public_key_client import fetch_public_key
from edge_gateway.crypto.secure_transport import SecureAcceptance, SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SessionManager as GatewaySessions
from edge_gateway.crypto.session import SessionState
from edge_gateway.dispatch import CloudDispatch

_HKDF_INFO = b"ml-kem-project:v1:gateway-cloud-session"
_ENVELOPE_FIELDS = (
    "protocol_version",
    "gateway_id",
    "session_id",
    "request_id",
    "nonce",
    "ciphertext",
)
_BASE64URL = re.compile(r"[A-Za-z0-9_-]+\Z")
_MEASUREMENT = {
    "device_id": "sensor-001",
    "temperature_c": 22.5,
    "humidity_pct": 44,
    "measured_at": "2026-09-21T13:45:31Z",
    "sequence_number": 1,
    "received_at": "2026-09-21T13:45:31.218Z",
}


class SecureRejection(Exception):
    """One test-receiver rejection. The message is the error code only."""

    def __init__(self, status_code: int, code: str) -> None:
        super().__init__(code)
        self.status_code = status_code
        self.code = code


class Policy:
    """Per-test controls for the test-only measurement receiver."""

    def __init__(self) -> None:
        self.bodies: list[bytes] = []
        self.results: list[tuple[int, str]] = []
        self.handshakes = 0
        self.baseline_posts = 0
        self.decrypt_calls = 0
        self.last_aad: bytes | None = None
        self.force_status: int | None = None
        self.force_code = "SECURE_MESSAGE_REJECTED"
        self.ambiguous_remaining = 0


class Clock:
    """Injectable Gateway clock. Cloud continues to use its own UTC clock."""

    def __init__(self) -> None:
        self.now = datetime.now(timezone.utc)

    def __call__(self) -> datetime:
        return self.now


class BaselineSpy:
    """Records classical deliveries. Fail-closed mode must leave this at zero."""

    def __init__(self) -> None:
        self.calls = 0

    async def send(self, **_fields: object) -> dict[str, str]:
        self.calls += 1
        return {"status": "accepted"}


class CloudHarness:
    """One live Cloud process and the Gateway clients pointed at it."""

    def __init__(self, app: FastAPI, base_url: str, policy: Policy) -> None:
        self.app = app
        self.base_url = base_url
        self.policy = policy

    def gateway_sessions(
        self,
        gateway_id: str = "gateway-001",
        clock: Clock | None = None,
    ) -> GatewaySessions:
        return GatewaySessions(gateway_id, self.base_url, 5.0, clock=clock)

    def transport(
        self,
        sessions: GatewaySessions,
        *,
        max_retries: int = 0,
        sleep: object | None = None,
    ) -> SecureTransport:
        paused = sleep if sleep is not None else (lambda _delay: None)
        return SecureTransport(
            sessions,
            cloud_url=self.base_url,
            timeout_seconds=5.0,
            max_retries=max_retries,
            sleep=paused,  # type: ignore[arg-type]
        )

    def rows(self) -> list[StoredMeasurement]:
        return self.app.state.repository.list()

    def post_json(self, path: str, payload: dict[str, object]) -> tuple[int, dict[str, object]]:
        request = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                status = response.status
                raw = response.read()
        except urllib.error.HTTPError as exc:
            status = exc.code
            raw = exc.read()
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise AssertionError("Cloud response must be a JSON object")
        return status, parsed


def _install(app: FastAPI, policy: Policy) -> None:
    """Mount the test-only receiver. Production routers stay unchanged."""

    @app.middleware("http")
    async def count_posts(request: Request, call_next):
        response = await call_next(request)
        if request.method == "POST" and request.url.path == "/api/v1/crypto/sessions":
            if response.status_code == 200:
                policy.handshakes += 1
        if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
            policy.baseline_posts += 1
        return response

    @app.post("/api/v1/secure/measurements")
    async def secure_measurements(request: Request) -> JSONResponse:
        policy.bodies.append(await request.body())
        try:
            payload = json.loads(policy.bodies[-1])
            checked = _require_envelope(payload)
        except (json.JSONDecodeError, UnicodeError):
            return _reject(policy, 400, "SECURE_MESSAGE_REJECTED")
        except SecureRejection as reject:
            return _reject(policy, reject.status_code, reject.code)
        if policy.force_status is not None:
            return _reject(policy, policy.force_status, policy.force_code)
        try:
            saved = _accept(app, checked, policy)
        except SecureRejection as reject:
            return _reject(policy, reject.status_code, reject.code)
        if policy.ambiguous_remaining > 0:
            policy.ambiguous_remaining -= 1
            return _reject(policy, 503, "SERVICE_UNAVAILABLE")
        marker = "accepted" if saved.created else "already_accepted"
        policy.results.append((202, marker))
        return JSONResponse(
            status_code=202,
            content={"status": marker, "record_id": saved.measurement.record_id},
        )


def _reject(policy: Policy, status_code: int, code: str) -> JSONResponse:
    policy.results.append((status_code, code))
    messages = {
        "SESSION_INVALID": "secure session is invalid",
        "SESSION_EXPIRED": "secure session has expired",
        "SERVICE_UNAVAILABLE": "service is not ready",
        "UNSUPPORTED_PROTOCOL_VERSION": "unsupported protocol version",
        "INVALID_MEASUREMENT": "measurement is invalid",
    }
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": messages.get(code, "secure message rejected")}},
    )


def _require_envelope(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict) or set(payload) != set(_ENVELOPE_FIELDS):
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED")
    if any(not isinstance(payload[name], str) or payload[name] == "" for name in _ENVELOPE_FIELDS):
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED")
    return payload


def _accept(app: FastAPI, checked: dict[str, str], policy: Policy):
    if checked["protocol_version"] != "1":
        try:
            cloud_build_aad(
                protocol_version=checked["protocol_version"],
                gateway_id=checked["gateway_id"],
                session_id=checked["session_id"],
                request_id=checked["request_id"],
            )
        except CloudAadError:
            raise SecureRejection(400, "UNSUPPORTED_PROTOCOL_VERSION") from None
        raise SecureRejection(400, "UNSUPPORTED_PROTOCOL_VERSION")
    try:
        session = app.state.sessions.get(checked["session_id"], checked["gateway_id"])
    except SessionAccessError as exc:
        raise SecureRejection(exc.status_code, exc.code) from None
    try:
        associated = cloud_build_aad(
            protocol_version=checked["protocol_version"],
            gateway_id=checked["gateway_id"],
            session_id=checked["session_id"],
            request_id=checked["request_id"],
        )
    except CloudAadError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    policy.last_aad = associated
    try:
        nonce = decode_binary(checked["nonce"])
        ciphertext = decode_binary(checked["ciphertext"])
    except EncodingError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    policy.decrypt_calls += 1
    try:
        plaintext = cloud_decrypt(session.session_key, nonce, ciphertext, associated)
    except AeadError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    try:
        measurement = validate_measurement(
            json.loads(plaintext),
            expected_gateway_id=checked["gateway_id"],
        )
    except (json.JSONDecodeError, MeasurementValidationError):
        raise SecureRejection(422, "INVALID_MEASUREMENT") from None
    return app.state.repository.save_idempotent(measurement)


def _measurement(**overrides: object) -> dict[str, object]:
    fields = dict(_MEASUREMENT)
    fields.update(overrides)
    return fields


def _deliver(
    transport: SecureTransport,
    request_id: str = "req-1",
    **overrides: object,
) -> SecureAcceptance:
    fields = _measurement(**overrides)
    return asyncio.run(
        transport.send(
            request_id=request_id,
            device_id=str(fields["device_id"]),
            temperature_c=fields["temperature_c"],  # type: ignore[arg-type]
            humidity_pct=fields["humidity_pct"],  # type: ignore[arg-type]
            measured_at=str(fields["measured_at"]),
            sequence_number=fields["sequence_number"],  # type: ignore[arg-type]
            received_at=str(fields["received_at"]),
        )
    )


def _seal(session, request_id: str = "req-1", **overrides: object):
    fields = _measurement(**overrides)
    return build_secure_envelope(
        key=bytes(session.session_key),
        session_id=session.session_id,
        request_id=request_id,
        gateway_id=session.gateway_id,
        device_id=str(fields["device_id"]),
        temperature_c=fields["temperature_c"],  # type: ignore[arg-type]
        humidity_pct=fields["humidity_pct"],  # type: ignore[arg-type]
        measured_at=str(fields["measured_at"]),
        sequence_number=fields["sequence_number"],  # type: ignore[arg-type]
        received_at=str(fields["received_at"]),
    )


def _flip(encoded: str, index: int) -> str:
    raw = bytearray(decode_binary(encoded))
    raw[index] ^= 0x01
    return encode_binary(bytes(raw))


@pytest.fixture
def cloud(tmp_path: Path):
    database = tmp_path / "measurements.db"
    app = create_app(
        load_config(
            {
                "DATABASE_URL": f"sqlite:///{database}",
                "SECURITY_MODE": "mlkem",
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    policy = Policy()
    _install(app, policy)
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="cloud-test-server", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive():
            raise RuntimeError("Cloud test server exited before it accepted connections")
        if time.monotonic() > deadline:
            server.should_exit = True
            raise RuntimeError("Cloud test server did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        raise RuntimeError("Cloud test server has no socket")
    port = sockets[0].getsockname()[1]
    try:
        yield CloudHarness(app, f"http://127.0.0.1:{port}", policy)
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_production_cloud_app_has_no_secure_measurement_route(tmp_path: Path) -> None:
    app = create_app(
        load_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / 'unused.db'}",
                "SECURITY_MODE": "mlkem",
            }
        )
    )
    paths = {route.path for route in app.routes if hasattr(route, "path")}
    assert "/api/v1/secure/measurements" not in paths


def test_versioned_public_key_retrieval(cloud: CloudHarness) -> None:
    with urllib.request.urlopen(cloud.base_url + "/api/v1/crypto/public-key", timeout=5) as response:
        payload = json.loads(response.read())
        status = response.status
    assert status == 200
    assert set(payload) == {"protocol_version", "algorithm", "key_id", "public_key"}
    assert payload["protocol_version"] == "1"
    assert payload["algorithm"] == "ML-KEM-768"
    fetched = fetch_public_key(cloud.base_url, 5.0)
    assert fetched.protocol_version == "1"
    assert fetched.algorithm == "ML-KEM-768"
    assert fetched.key_id == payload["key_id"]
    assert len(fetched.public_key) == 1184


def test_valid_encapsulation_matches_shared_secret_and_hkdf(
    cloud: CloudHarness,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Compare secrets through booleans so a failure does not print key material."""
    caplog.set_level(logging.DEBUG)
    captured: dict[str, bytes] = {}
    real_encapsulate = encapsulate

    def remember(public_key: bytes):
        ciphertext, shared_secret = real_encapsulate(public_key)
        captured["ciphertext"] = ciphertext
        captured["secret"] = shared_secret
        return ciphertext, shared_secret

    monkeypatch.setattr("edge_gateway.crypto.session.encapsulate", remember)
    sessions = cloud.gateway_sessions()
    session = asyncio.run(sessions.get_or_establish())
    cloud_secret = cloud.app.state.keys.decapsulate(captured["ciphertext"])
    same_secret = captured["secret"] == cloud_secret
    assert same_secret
    gateway_key = gateway_derive_session_key(captured["secret"])
    cloud_key = cloud_derive_session_key(cloud_secret)
    same_derived = gateway_key == cloud_key
    assert same_derived
    stored = next(iter(cloud.app.state.sessions._sessions.values()))
    same_gateway = bytes(session.session_key) == gateway_key
    same_cloud = bytes(stored.session_key) == cloud_key
    assert same_gateway and same_cloud
    assert GATEWAY_SESSION_KEY_INFO == _HKDF_INFO
    assert CLOUD_SESSION_KEY_INFO == _HKDF_INFO
    assert GATEWAY_SESSION_KEY_LENGTH == 32
    assert CLOUD_SESSION_KEY_LENGTH == 32
    assert "salt=None" in inspect.getsource(gateway_derive_session_key)
    assert "salt=None" in inspect.getsource(cloud_derive_session_key)
    assert session.state is SessionState.ACTIVE
    assert session.expires_at > datetime.now(timezone.utc)
    assert cloud.policy.handshakes == 1
    leaked = captured["secret"].hex() in caplog.text or gateway_key.hex() in caplog.text
    assert not leaked


def test_secure_envelope_round_trip_stores_canonical_measurement(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    acceptance = _deliver(cloud.transport(sessions), request_id="req-round")
    stored = cloud.app.state.repository.find_by_device_sequence("sensor-001", 1)
    assert stored is not None
    assert acceptance.status == "accepted"
    assert acceptance.record_id == stored.record_id
    assert stored.temperature_c == 22.5
    assert stored.humidity_pct == 44
    assert stored.sequence_number == 1
    assert stored.device_id == "sensor-001"
    assert stored.gateway_id == "gateway-001"
    envelope = json.loads(cloud.policy.bodies[-1])
    assert set(envelope) == set(_ENVELOPE_FIELDS)
    assert "message_counter" not in envelope
    assert len(decode_binary(envelope["nonce"])) == 12
    assert _BASE64URL.fullmatch(envelope["nonce"])
    assert _BASE64URL.fullmatch(envelope["ciphertext"])
    gateway_aad = gateway_build_aad(
        protocol_version="1",
        gateway_id="gateway-001",
        session_id=envelope["session_id"],
        request_id="req-round",
    )
    cloud_aad = cloud_build_aad(
        protocol_version="1",
        gateway_id="gateway-001",
        session_id=envelope["session_id"],
        request_id="req-round",
    )
    same_aad = gateway_aad == cloud_aad == cloud.policy.last_aad
    assert same_aad
    assert set(json.loads(gateway_aad)) == {
        "protocol_version",
        "gateway_id",
        "session_id",
        "request_id",
    }
    assert cloud.policy.handshakes == 1
    assert cloud.policy.baseline_posts == 0
    assert len(cloud.rows()) == 1


def test_one_handshake_is_reused_for_three_measurements(cloud: CloudHarness) -> None:
    transport = cloud.transport(cloud.gateway_sessions())

    async def send_three() -> list[SecureAcceptance]:
        return [
            await transport.send(request_id=f"req-{number}", **_measurement(sequence_number=number))
            for number in (1, 2, 3)
        ]

    accepted = asyncio.run(send_three())
    assert [item.status for item in accepted] == ["accepted", "accepted", "accepted"]
    assert cloud.policy.handshakes == 1
    assert len(cloud.rows()) == 3
    assert len({json.loads(body)["session_id"] for body in cloud.policy.bodies}) == 1


def test_local_session_expiry_reestablishes_before_the_next_send(cloud: CloudHarness) -> None:
    clock = Clock()
    sessions = cloud.gateway_sessions(clock=clock)
    transport = cloud.transport(sessions)
    current = asyncio.run(sessions.get_or_establish())
    original = current.session_id
    # Equality expires the held session. The replacement Cloud expiry is later
    # than this instant, so the new handshake is still in the future.
    clock.now = current.expires_at
    acceptance = _deliver(transport, request_id="req-local-expiry")
    delivered = json.loads(cloud.policy.bodies[-1])["session_id"]
    assert acceptance.status == "accepted"
    assert delivered != original
    assert cloud.policy.handshakes == 2
    assert len(cloud.policy.bodies) == 1
    assert len(cloud.rows()) == 1


def test_expired_session_returns_409_and_recovers_once(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    current = asyncio.run(sessions.get_or_establish())
    stored = cloud.app.state.sessions._sessions[current.session_id]
    object.__setattr__(stored, "expires_at", datetime.now(timezone.utc) - timedelta(seconds=5))
    acceptance = _deliver(cloud.transport(sessions), request_id="req-expired")
    assert cloud.policy.results[0] == (409, "SESSION_EXPIRED")
    assert cloud.policy.results[1] == (202, "accepted")
    assert acceptance.status == "accepted"
    assert current.session_id not in cloud.app.state.sessions._sessions
    assert cloud.policy.handshakes == 2
    assert len(cloud.rows()) == 1
    first = json.loads(cloud.policy.bodies[0])
    second = json.loads(cloud.policy.bodies[1])
    assert first["request_id"] == second["request_id"] == "req-expired"
    assert first["session_id"] != second["session_id"]


def test_invalid_session_returns_409_and_recovers_once(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    current = asyncio.run(sessions.get_or_establish())
    cloud.app.state.sessions.invalidate(current.session_id)
    acceptance = _deliver(cloud.transport(sessions), request_id="req-invalid")
    assert cloud.policy.results[0] == (409, "SESSION_INVALID")
    assert cloud.policy.results[1] == (202, "accepted")
    assert acceptance.status == "accepted"
    assert cloud.policy.handshakes == 2
    assert len(cloud.rows()) == 1


def test_a_second_session_rejection_is_not_recovered(cloud: CloudHarness) -> None:
    cloud.policy.force_status = 409
    cloud.policy.force_code = "SESSION_INVALID"
    sessions = cloud.gateway_sessions()
    transport = cloud.transport(sessions, max_retries=2)
    with pytest.raises(SecureTransportError) as caught:
        _deliver(transport, request_id="req-bound")
    assert caught.value.retryable is False
    assert caught.value.code == "SESSION_INVALID"
    assert cloud.policy.handshakes == 2
    assert cloud.policy.results == [(409, "SESSION_INVALID"), (409, "SESSION_INVALID")]
    assert cloud.rows() == []
    first = json.loads(cloud.policy.bodies[0])
    second = json.loads(cloud.policy.bodies[1])
    assert first["request_id"] == second["request_id"] == "req-bound"
    assert first["session_id"] != second["session_id"]


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("ciphertext", "SECURE_MESSAGE_REJECTED"),
        ("nonce", "SECURE_MESSAGE_REJECTED"),
        ("request_id", "SECURE_MESSAGE_REJECTED"),
        ("tag", "SECURE_MESSAGE_REJECTED"),
    ],
    ids=(
        "corrupted-aead-ciphertext",
        "nonce-tampering",
        "aad-tampering",
        "cloud-decryption-failure",
    ),
)
def test_tampered_secure_message_is_rejected(cloud: CloudHarness, field: str, code: str) -> None:
    sessions = cloud.gateway_sessions()
    session = asyncio.run(sessions.get_or_establish())
    changed = _seal(session).as_dict()
    if field == "ciphertext":
        changed["ciphertext"] = _flip(changed["ciphertext"], 0)
    elif field == "tag":
        changed["ciphertext"] = _flip(changed["ciphertext"], -1)
    elif field == "nonce":
        changed["nonce"] = _flip(changed["nonce"], 0)
    elif field == "request_id":
        changed["request_id"] = "req-changed"
    status, body = cloud.post_json("/api/v1/secure/measurements", changed)
    assert status == 400
    assert body["error"]["code"] == code
    assert cloud.policy.decrypt_calls == 1
    assert cloud.rows() == []


def test_wrong_session_is_rejected_without_storage(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    first = asyncio.run(sessions.get_or_establish())
    first_key = bytes(first.session_key)
    sessions.invalidate()
    second = asyncio.run(sessions.get_or_establish())
    foreign = build_secure_envelope(
        key=first_key,
        session_id=second.session_id,
        request_id="req-wrong-session",
        gateway_id=second.gateway_id,
        device_id="sensor-001",
        temperature_c=22.5,
        humidity_pct=44,
        measured_at="2026-09-21T13:45:31Z",
        sequence_number=1,
        received_at="2026-09-21T13:45:31.218Z",
    )
    status, body = cloud.post_json("/api/v1/secure/measurements", foreign.as_dict())
    assert status == 400
    assert body["error"]["code"] == "SECURE_MESSAGE_REJECTED"
    assert cloud.policy.decrypt_calls == 1
    assert len(cloud.app.state.sessions) == 2
    assert cloud.rows() == []


def test_wrong_gateway_ownership_is_rejected_before_decrypt(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    session = asyncio.run(sessions.get_or_establish())
    changed = _seal(session).as_dict()
    changed["gateway_id"] = "gateway-002"
    status, body = cloud.post_json("/api/v1/secure/measurements", changed)
    assert status == 400
    assert body["error"]["code"] == "SECURE_MESSAGE_REJECTED"
    assert cloud.policy.decrypt_calls == 0
    assert len(cloud.app.state.sessions) == 1
    assert cloud.rows() == []


def test_unsupported_protocol_version_is_rejected(cloud: CloudHarness) -> None:
    sessions = cloud.gateway_sessions()
    session = asyncio.run(sessions.get_or_establish())
    changed = _seal(session).as_dict()
    changed["protocol_version"] = "999"
    status, body = cloud.post_json("/api/v1/secure/measurements", changed)
    assert status == 400
    assert body["error"]["code"] == "UNSUPPORTED_PROTOCOL_VERSION"
    assert cloud.policy.decrypt_calls == 0
    assert cloud.rows() == []

    def unreachable(_ciphertext: bytes) -> bytes:
        raise AssertionError("unsupported protocol version reached decapsulation")

    cloud.app.state.keys.decapsulate = unreachable
    before = len(cloud.app.state.sessions)
    status, body = cloud.post_json(
        "/api/v1/crypto/sessions",
        {
            "protocol_version": "999",
            "gateway_id": "gateway-001",
            "key_id": cloud.app.state.keys.key_id,
            "encapsulation_ciphertext": "abcd",
        },
    )
    assert status == 400
    assert body["error"]["code"] == "UNSUPPORTED_PROTOCOL_VERSION"
    assert len(cloud.app.state.sessions) == before


def test_malformed_mlkem_ciphertext_is_rejected(cloud: CloudHarness) -> None:
    def unreachable(_ciphertext: bytes) -> bytes:
        raise AssertionError("malformed ML-KEM ciphertext reached decapsulation")

    cloud.app.state.keys.decapsulate = unreachable
    status, body = cloud.post_json(
        "/api/v1/crypto/sessions",
        {
            "protocol_version": "1",
            "gateway_id": "gateway-001",
            "key_id": cloud.app.state.keys.key_id,
            "encapsulation_ciphertext": "abcd",
        },
    )
    assert status == 400
    assert body["error"]["code"] == "INVALID_SESSION_REQUEST"
    assert len(cloud.app.state.sessions) == 0


def test_simulated_decapsulation_failure_leaves_no_session(cloud: CloudHarness) -> None:
    ciphertext, secret = encapsulate(cloud.app.state.keys.public_key)
    del secret

    def fail(_ciphertext: bytes) -> bytes:
        raise RuntimeError("simulated decapsulation failure")

    cloud.app.state.keys.decapsulate = fail
    status, body = cloud.post_json(
        "/api/v1/crypto/sessions",
        {
            "protocol_version": "1",
            "gateway_id": "gateway-001",
            "key_id": cloud.app.state.keys.key_id,
            "encapsulation_ciphertext": encode_binary(ciphertext),
        },
    )
    assert status == 503
    assert body["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert len(cloud.app.state.sessions) == 0
    assert cloud.policy.handshakes == 0


def test_valid_length_mlkem_mutation_is_not_required_to_raise(cloud: CloudHarness) -> None:
    """A valid-length ML-KEM ciphertext change may use implicit rejection and is not required to raise."""
    ciphertext, secret = encapsulate(cloud.app.state.keys.public_key)
    flipped = bytearray(ciphertext)
    flipped[0] ^= 0x01
    raised = False
    try:
        other = cloud.app.state.keys.decapsulate(bytes(flipped))
    except Exception:
        raised = True
        other = b""
    if not raised:
        differs = other != secret
        assert differs
        assert len(other) == 32
    original = cloud.app.state.keys.decapsulate(ciphertext) == secret
    assert original
    assert len(cloud.app.state.sessions) == 0


def test_secure_failure_does_not_call_baseline(cloud: CloudHarness, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    cloud.policy.force_status = 400
    cloud.policy.force_code = "SECURE_MESSAGE_REJECTED"
    sessions = cloud.gateway_sessions()
    transport = cloud.transport(sessions)
    baseline = BaselineSpy()
    dispatch = CloudDispatch(
        load_gateway_config({"SECURITY_MODE": "mlkem", "CLOUD_URL": cloud.base_url}),
        baseline=baseline,
        secure=transport,
    )
    with pytest.raises(SecureTransportError):
        _deliver(dispatch, request_id="req-closed")
    assert baseline.calls == 0
    assert cloud.policy.baseline_posts == 0
    assert dispatch.metrics.secure_failures_total == 1
    assert dispatch.pqc_metrics.pqc_fallback_total == 0
    assert any("event=pqc_fail_closed" in record.message for record in caplog.records)


def test_ambiguous_transport_retries_the_same_envelope(cloud: CloudHarness) -> None:
    delays: list[float] = []
    cloud.policy.ambiguous_remaining = 1
    sessions = cloud.gateway_sessions()
    transport = cloud.transport(sessions, max_retries=1, sleep=delays.append)
    acceptance = _deliver(transport, request_id="req-retry")
    same_body = cloud.policy.bodies[0] == cloud.policy.bodies[1]
    assert same_body
    assert delays == [1.0]
    assert cloud.policy.results == [(503, "SERVICE_UNAVAILABLE"), (202, "already_accepted")]
    assert acceptance.status == "already_accepted"
    assert cloud.policy.handshakes == 1
    assert len(cloud.rows()) == 1
    first = json.loads(cloud.policy.bodies[0])
    second = json.loads(cloud.policy.bodies[1])
    same_envelope = first == second
    assert same_envelope
    assert first["request_id"] == "req-retry"


def test_duplicate_sequence_is_stored_once(cloud: CloudHarness) -> None:
    """Business idempotency keeps the first row. Protocol version 1 has no cryptographic replay counter or window."""
    transport = cloud.transport(cloud.gateway_sessions())

    async def send_twice() -> tuple[SecureAcceptance, SecureAcceptance]:
        first = await transport.send(request_id="req-original", **_measurement(sequence_number=7))
        second = await transport.send(
            request_id="req-duplicate",
            **_measurement(sequence_number=7, temperature_c=30.0),
        )
        return first, second

    first, second = asyncio.run(send_twice())
    stored = cloud.app.state.repository.find_by_device_sequence("sensor-001", 7)
    assert stored is not None
    assert first.status == "accepted"
    assert second.status == "already_accepted"
    assert first.record_id == second.record_id == stored.record_id
    assert stored.temperature_c == 22.5
    assert len(cloud.rows()) == 1
    assert cloud.policy.handshakes == 1
    assert "REPLAY" not in {code for _status, code in cloud.policy.results}
