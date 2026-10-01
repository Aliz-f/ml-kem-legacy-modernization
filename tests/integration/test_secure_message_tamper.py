"""Tamper, wrong-session, ownership, and unsupported-version rejection.

The receiver in this module is test-only. It calls the Cloud session lookup,
four-field AAD builder, and AES-GCM decrypt in protocol order, then appends to
the store only after authentication and measurement validation both succeed.
It does not add a Cloud secure-ingest route.

Protocol version 1 has no cryptographic replay counter or window. These tests
do not treat a repeated authenticated envelope as replay rejection.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone

import pytest

from cloud_service.crypto.aad import AadError as CloudAadError
from cloud_service.crypto.aad import build_aad as cloud_build_aad
from cloud_service.crypto.kdf import derive_session_key as cloud_derive_session_key
from cloud_service.crypto.mlkem import decapsulate, generate_keypair
from cloud_service.crypto.session import SessionAccessError, SessionManager
from cloud_service.crypto.symmetric import AeadError
from cloud_service.crypto.symmetric import decrypt as cloud_decrypt
from cloud_service.validation import MeasurementValidationError, validate_measurement
from edge_gateway.crypto.aad import AadError, build_aad
from edge_gateway.crypto.encoding import EncodingError, decode_binary, encode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.kdf import derive_session_key as gateway_derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.public_key import PublicKeyRejected, parse_public_key_response
from edge_gateway.crypto.session import SessionEstablishmentError
from edge_gateway.crypto.session import SessionManager as GatewaySessions
from edge_gateway.crypto.session_client import SessionRejected, parse_session_response
from edge_gateway.crypto.symmetric import generate_nonce

_ENVELOPE_FIELDS = (
    "protocol_version",
    "gateway_id",
    "session_id",
    "request_id",
    "nonce",
    "ciphertext",
)


class SecureRejection(Exception):
    """One frozen secure-message rejection, without payload or key material."""

    def __init__(self, status_code: int, code: str) -> None:
        super().__init__(code)
        self.status_code = status_code
        self.code = code


class DecryptSpy:
    """Count calls, then use Cloud's real AES-GCM decrypt."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes) -> bytes:
        self.calls += 1
        return cloud_decrypt(key, nonce, ciphertext, associated_data)


def _establish(sessions: SessionManager, gateway_id: str) -> tuple[str, bytes]:
    """Agree one real ML-KEM session key and register it with Cloud."""
    public_key, private_key = generate_keypair()
    try:
        ciphertext, gateway_secret = encapsulate(public_key)
        cloud_secret = decapsulate(ciphertext, private_key)
        secrets_match = gateway_secret == cloud_secret
        if not secrets_match:
            raise AssertionError("ML-KEM shared secrets differ")
        gateway_key = gateway_derive_session_key(gateway_secret)
        cloud_key = cloud_derive_session_key(cloud_secret)
        keys_match = gateway_key == cloud_key
        if not keys_match:
            raise AssertionError("HKDF session keys differ")
        session = sessions.create(gateway_id, "cloud-key-1", cloud_key)
        return session.session_id, gateway_key
    finally:
        private_key.close()


def _envelope(key: bytes, session_id: str, request_id: str = "req-1"):
    return build_secure_envelope(
        key=key,
        session_id=session_id,
        request_id=request_id,
        device_id="sensor-001",
        temperature_c=21.7,
        humidity_pct=42.5,
        measured_at="2026-09-21T13:45:31Z",
        sequence_number=184,
        received_at="2026-09-21T13:45:31.218Z",
        gateway_id="gateway-001",
    )


def _different_nonce(current: str) -> str:
    original = decode_binary(current)
    replacement = generate_nonce()
    if replacement == original:
        flipped = bytearray(original)
        flipped[0] ^= 1
        replacement = bytes(flipped)
    return encode_binary(replacement)


def _tamper(envelope: dict[str, str], field: str) -> dict[str, str]:
    changed = dict(envelope)
    if field == "ciphertext":
        raw = bytearray(decode_binary(changed["ciphertext"]))
        raw[0] ^= 1
        changed["ciphertext"] = encode_binary(bytes(raw))
    elif field == "nonce":
        changed["nonce"] = _different_nonce(changed["nonce"])
    elif field == "gateway_id":
        changed["gateway_id"] = "gateway-002"
    elif field == "session_id":
        changed["session_id"] = "sess-changed"
    elif field == "request_id":
        changed["request_id"] = "req-changed"
    elif field == "protocol_version":
        changed["protocol_version"] = "999"
    else:
        raise AssertionError(f"unknown tamper field {field}")
    return changed


def _require_envelope(envelope: object) -> dict[str, str]:
    if not isinstance(envelope, dict) or set(envelope) != set(_ENVELOPE_FIELDS):
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED")
    if any(not isinstance(envelope[name], str) or envelope[name] == "" for name in _ENVELOPE_FIELDS):
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED")
    return envelope


def _receive(envelope: object, sessions: SessionManager, store: list[object], decrypt: DecryptSpy) -> None:
    """Accept one envelope only after Cloud authentication succeeds."""
    checked = _require_envelope(envelope)
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
        session = sessions.get(checked["session_id"], checked["gateway_id"])
    except SessionAccessError as exc:
        raise SecureRejection(exc.status_code, exc.code) from None
    try:
        associated_data = cloud_build_aad(
            protocol_version=checked["protocol_version"],
            gateway_id=checked["gateway_id"],
            session_id=checked["session_id"],
            request_id=checked["request_id"],
        )
    except CloudAadError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    try:
        nonce = decode_binary(checked["nonce"])
        ciphertext = decode_binary(checked["ciphertext"])
    except EncodingError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    try:
        plaintext = decrypt(session.session_key, nonce, ciphertext, associated_data)
    except AeadError:
        raise SecureRejection(400, "SECURE_MESSAGE_REJECTED") from None
    try:
        measurement = validate_measurement(
            json.loads(plaintext),
            expected_gateway_id=checked["gateway_id"],
        )
    except (json.JSONDecodeError, MeasurementValidationError):
        raise SecureRejection(422, "INVALID_MEASUREMENT") from None
    store.append(measurement)


def _reject(envelope: dict[str, str], sessions: SessionManager) -> tuple[SecureRejection, DecryptSpy, list[object]]:
    store: list[object] = []
    decrypt = DecryptSpy()
    with pytest.raises(SecureRejection) as caught:
        _receive(envelope, sessions, store, decrypt)
    return caught.value, decrypt, store


def test_authentic_envelope_is_stored_once(caplog: pytest.LogCaptureFixture) -> None:
    sessions = SessionManager()
    session_id, key = _establish(sessions, "gateway-001")
    body = _envelope(key, session_id).as_dict()
    assert list(body) == list(_ENVELOPE_FIELDS)
    assert "message_counter" not in body
    store: list[object] = []
    decrypt = DecryptSpy()
    with caplog.at_level(logging.DEBUG):
        _receive(body, sessions, store, decrypt)
    assert decrypt.calls == 1
    assert len(store) == 1
    saved = store[0]
    assert saved.device_id == "sensor-001"
    assert saved.sequence_number == 184
    assert saved.gateway_id == "gateway-001"
    assert caplog.text == ""


@pytest.mark.parametrize(
    ("field", "status", "code", "decrypts"),
    [
        ("ciphertext", 400, "SECURE_MESSAGE_REJECTED", True),
        ("nonce", 400, "SECURE_MESSAGE_REJECTED", True),
        ("gateway_id", 400, "SECURE_MESSAGE_REJECTED", False),
        ("session_id", 409, "SESSION_INVALID", False),
        ("request_id", 400, "SECURE_MESSAGE_REJECTED", True),
        ("protocol_version", 400, "UNSUPPORTED_PROTOCOL_VERSION", False),
    ],
)
def test_tampered_field_is_rejected_and_stores_nothing(
    field: str,
    status: int,
    code: str,
    decrypts: bool,
) -> None:
    sessions = SessionManager()
    session_id, key = _establish(sessions, "gateway-001")
    original = _envelope(key, session_id).as_dict()
    tampered = _tamper(original, field)
    assert tampered[field] != original[field]
    assert "message_counter" not in tampered
    rejection, decrypt, store = _reject(tampered, sessions)
    assert (rejection.status_code, rejection.code) == (status, code)
    assert decrypt.calls == int(decrypts)
    assert store == []


def test_session_a_ciphertext_is_rejected_when_the_envelope_claims_session_b(
    caplog: pytest.LogCaptureFixture,
) -> None:
    sessions = SessionManager()
    session_a, key_a = _establish(sessions, "gateway-001")
    session_b, key_b = _establish(sessions, "gateway-001")
    keys_differ = key_a != key_b
    assert keys_differ
    body = _envelope(key_a, session_b, request_id="req-b").as_dict()
    assert body["session_id"] == session_b
    associated_data = cloud_build_aad(
        protocol_version="1",
        gateway_id="gateway-001",
        session_id=session_b,
        request_id="req-b",
    )
    opened = cloud_decrypt(
        key_a,
        decode_binary(body["nonce"]),
        decode_binary(body["ciphertext"]),
        associated_data,
    )
    assert json.loads(opened)["device_id"] == "sensor-001"
    with caplog.at_level(logging.DEBUG):
        rejection, decrypt, store = _reject(body, sessions)
    assert (rejection.status_code, rejection.code) == (400, "SECURE_MESSAGE_REJECTED")
    assert decrypt.calls == 1
    assert store == []
    assert sessions.get(session_a, "gateway-001").session_id == session_a
    assert sessions.get(session_b, "gateway-001").session_id == session_b
    assert caplog.text == ""


def test_gateway_002_cannot_use_the_session_owned_by_gateway_001() -> None:
    sessions = SessionManager()
    session_id, key = _establish(sessions, "gateway-001")
    body = _envelope(key, session_id).as_dict()
    body["gateway_id"] = "gateway-002"
    rejection, decrypt, store = _reject(body, sessions)
    assert (rejection.status_code, rejection.code) == (400, "SECURE_MESSAGE_REJECTED")
    assert decrypt.calls == 0
    assert store == []
    owned = sessions.get(session_id, "gateway-001")
    assert owned.gateway_id == "gateway-001"
    assert owned.session_id == session_id


def test_protocol_version_999_is_rejected_before_secure_processing(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    rejected_key = {
        "protocol_version": "999",
        "algorithm": "ML-KEM-768",
        "key_id": "cloud-key-001",
        "public_key": "AAAA",
    }
    with pytest.raises(PublicKeyRejected, match="Unsupported protocol_version"):
        parse_public_key_response(rejected_key)
    with pytest.raises(SessionRejected, match="Unsupported protocol_version"):
        parse_session_response(
            {
                "protocol_version": "999",
                "session_id": "sess-1",
                "status": "established",
                "expires_at": "2026-09-21T00:05:00Z",
            },
            now=datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
    with pytest.raises(AadError):
        build_aad(
            protocol_version="999",
            gateway_id="gateway-001",
            session_id="sess-1",
            request_id="req-1",
        )
    with pytest.raises(CloudAadError):
        cloud_build_aad(
            protocol_version="999",
            gateway_id="gateway-001",
            session_id="sess-1",
            request_id="req-1",
        )
    sealed = _envelope(bytes(range(32)), "sess-1")
    assert sealed.protocol_version == "1"

    def reject_public_key(cloud_url: str, timeout_seconds: float) -> None:
        parse_public_key_response(rejected_key)

    def handshake_continued(*args: object, **kwargs: object) -> None:
        raise AssertionError("handshake continued after protocol 999")

    monkeypatch.setattr("edge_gateway.crypto.session.fetch_public_key", reject_public_key)
    monkeypatch.setattr("edge_gateway.crypto.session.post_session", handshake_continued)
    manager = GatewaySessions("gateway-001", "http://cloud.test", 3.0)
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(SessionEstablishmentError) as caught:
            asyncio.run(manager.get_or_establish())
    assert caught.value.retryable is False
    assert str(caught.value) == "session establishment rejected"
    assert manager.metrics.active_session == 0
    assert manager.metrics.pqc_fallback_total == 0
    assert manager.metrics.handshake_failures["rejected"] == 1
    assert "reason=rejected" in caplog.text
    assert "AAAA" not in caplog.text
    assert "event=session_created" not in caplog.text
