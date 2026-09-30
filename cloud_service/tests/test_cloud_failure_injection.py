"""M4-41 through M4-51 controlled Cloud failures and unchanged safe defaults."""

import logging

from fastapi.testclient import TestClient
import pytest

from cloud_service.app import create_app
from cloud_service.config import FailureMode, load_config
from cloud_service.failure import FailureInjector
from cloud_service.gateway import routes, secure
from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import encapsulate

SECURE_PATH = "/api/v1/secure/measurements"
BASELINE_PATH = "/api/v1/baseline/measurements"


def canonical():
    return {
        "device_id": "sensor-failure", "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-10-01T12:00:00Z", "sequence_number": 41,
        "received_at": "2026-10-01T12:00:01Z", "gateway_id": "gateway-failure",
    }


def config(tmp_path, mode=FailureMode.NONE, *, rate=1.0, delay=0):
    return load_config({
        "SECURITY_MODE": "mlkem", "DATABASE_URL": f"sqlite:///{(tmp_path / f'{mode.value}-{rate}.db').as_posix()}",
        "FAILURE_MODE": mode.value, "FAILURE_RATE": str(rate), "FAILURE_SEED": "87",
        "FAILURE_DELAY_SECONDS": str(delay),
    })


def handshake(client):
    ciphertext, secret = encapsulate(client.app.state.keys.public_key)
    response = client.post("/api/v1/crypto/sessions", json={
        "protocol_version": "1", "gateway_id": "gateway-failure", "key_id": client.app.state.keys.key_id,
        "encapsulation_ciphertext": encode_binary(ciphertext),
    })
    assert response.status_code == 200
    return response.json()["session_id"], derive_session_key(secret)


def envelope(client):
    session_id, key = handshake(client)
    return build_secure_envelope(key=key, session_id=session_id, request_id="req-failure", **canonical()).as_dict()


def secure_client(tmp_path, mode, *, rate=1.0, delay=0):
    return TestClient(create_app(config(tmp_path, mode, rate=rate, delay=delay)))


def test_none_and_zero_rate_leave_secure_flow_unchanged(tmp_path):
    for mode, rate in ((FailureMode.NONE, 1.0), (FailureMode.DECRYPTION_FAILURE, 0.0)):
        with secure_client(tmp_path, mode, rate=rate) as client:
            response = client.post(SECURE_PATH, json=envelope(client))
            assert response.status_code == 202
            assert response.json()["status"] == "accepted"
            assert len(client.app.state.repository.list()) == 1


_RANDOM_SECURE_MODES = (
    FailureMode.SESSION_NOT_FOUND, FailureMode.SESSION_EXPIRED,
    FailureMode.DECRYPTION_FAILURE, FailureMode.STORAGE_FAILURE,
    FailureMode.DROP_RESPONSE,
)


def test_random_rate_zero_never_injects():
    injector = FailureInjector(FailureMode.RANDOM, 0.0, 17, 0)
    assert [injector.select(_RANDOM_SECURE_MODES).mode for _ in range(20)] == [None] * 20


def test_random_rate_one_selects_one_applicable_fault_for_request():
    injector = FailureInjector(FailureMode.RANDOM, 1.0, 17, 0)
    selection = injector.select((FailureMode.DECRYPTION_FAILURE,))
    assert selection.mode is FailureMode.DECRYPTION_FAILURE
    assert selection.inject(FailureMode.DECRYPTION_FAILURE)
    assert not selection.inject(FailureMode.STORAGE_FAILURE)


def test_random_seed_is_reproducible_and_selects_only_allowed_modes():
    left = FailureInjector(FailureMode.RANDOM, 1.0, 17, 0)
    right = FailureInjector(FailureMode.RANDOM, 1.0, 17, 0)
    left_modes = [left.select(_RANDOM_SECURE_MODES).mode for _ in range(30)]
    right_modes = [right.select(_RANDOM_SECURE_MODES).mode for _ in range(30)]
    assert left_modes == right_modes
    assert set(left_modes) <= set(_RANDOM_SECURE_MODES)


def test_enabled_injection_logs_safe_warning(caplog):
    with caplog.at_level(logging.WARNING, logger="cloud_service"):
        FailureInjector(FailureMode.DECRYPTION_FAILURE, 1.0, 3, 0)
    assert "event=failure_injection_enabled mode=decryption_failure rate=1.0" in caplog.text


def test_public_key_unavailable(tmp_path):
    with secure_client(tmp_path, FailureMode.PUBLIC_KEY_UNAVAILABLE) as client:
        response = client.get("/api/v1/crypto/public-key")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"


def test_simulated_decapsulation_failure_creates_no_session(tmp_path):
    with secure_client(tmp_path, FailureMode.MLKEM_DECAPSULATION_FAILURE) as client:
        ciphertext, _ = encapsulate(client.app.state.keys.public_key)
        response = client.post("/api/v1/crypto/sessions", json={
            "protocol_version": "1", "gateway_id": "gateway-failure", "key_id": client.app.state.keys.key_id,
            "encapsulation_ciphertext": encode_binary(ciphertext),
        })
        assert len(client.app.state.sessions) == 0
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"


@pytest.mark.parametrize(("mode", "code"), [
    (FailureMode.SESSION_NOT_FOUND, "SESSION_INVALID"),
    (FailureMode.SESSION_EXPIRED, "SESSION_EXPIRED"),
])
def test_injected_session_failures_are_frozen_409s(tmp_path, mode, code):
    with secure_client(tmp_path, mode) as client:
        wire = envelope(client)
        response = client.post(SECURE_PATH, json=wire)
        assert len(client.app.state.sessions) == 0
    assert response.status_code == 409
    assert response.json()["error"]["code"] == code


def test_session_not_found_preserves_ownership_before_invalidation(tmp_path):
    with secure_client(tmp_path, FailureMode.SESSION_NOT_FOUND) as client:
        wire = envelope(client)
        wrong_owner = wire | {"gateway_id": "another-gateway"}
        response = client.post(SECURE_PATH, json=wrong_owner)
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "SECURE_MESSAGE_REJECTED"
        assert len(client.app.state.sessions) == 1
        assert client.app.state.repository.list() == []


def test_selected_fault_logs_only_when_its_boundary_is_reached(tmp_path, caplog):
    with secure_client(tmp_path, FailureMode.DECRYPTION_FAILURE) as client:
        with caplog.at_level(logging.WARNING, logger="cloud_service"):
            malformed = client.post(SECURE_PATH, json={})
            assert malformed.status_code == 400
            assert "event=failure_injected" not in caplog.text
            response = client.post(SECURE_PATH, json=envelope(client))
    assert response.status_code == 400
    assert caplog.text.count("event=failure_injected failure_type=decryption_failure") == 1


def test_decryption_failure_prevents_plaintext_and_storage(tmp_path, monkeypatch):
    with secure_client(tmp_path, FailureMode.DECRYPTION_FAILURE) as client:
        wire = envelope(client)
        monkeypatch.setattr(secure, "validate_measurement", lambda value, **kwargs: pytest.fail("plaintext parsed"))
        response = client.post(SECURE_PATH, json=wire)
        assert client.app.state.repository.list() == []
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "SECURE_MESSAGE_REJECTED"


def test_storage_failure_is_503_for_secure_and_baseline(tmp_path):
    with secure_client(tmp_path, FailureMode.STORAGE_FAILURE) as client:
        response = client.post(SECURE_PATH, json=envelope(client))
        assert client.app.state.repository.list() == []
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "STORAGE_UNAVAILABLE"
    baseline = load_config({
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'baseline.db').as_posix()}",
        "FAILURE_MODE": "storage_failure", "FAILURE_RATE": "1", "FAILURE_DELAY_SECONDS": "0",
    })
    with TestClient(create_app(baseline)) as client:
        response = client.post(BASELINE_PATH, json=canonical())
        assert client.app.state.repository.list() == []
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "STORAGE_UNAVAILABLE"


@pytest.mark.parametrize(("path", "payload"), [(SECURE_PATH, "secure"), (BASELINE_PATH, "baseline")])
def test_processing_delay_is_bounded_and_selected(tmp_path, monkeypatch, path, payload):
    calls = []
    async def pause(seconds):
        calls.append(seconds)
    target = secure if payload == "secure" else routes
    monkeypatch.setattr(target.asyncio, "sleep", pause)
    if payload == "secure":
        with secure_client(tmp_path, FailureMode.PROCESSING_DELAY, delay=0.25) as client:
            response = client.post(path, json=envelope(client))
    else:
        settings = load_config({
            "DATABASE_URL": f"sqlite:///{(tmp_path / 'delay.db').as_posix()}",
            "FAILURE_MODE": "processing_delay", "FAILURE_RATE": "1", "FAILURE_DELAY_SECONDS": "0.25",
        })
        with TestClient(create_app(settings)) as client:
            response = client.post(path, json=canonical())
    assert response.status_code == 202
    assert calls == [0.25]


def test_service_unavailable_stops_secure_boundary(tmp_path):
    with secure_client(tmp_path, FailureMode.SERVICE_UNAVAILABLE) as client:
        response = client.post(SECURE_PATH, json={})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"


def test_drop_response_commits_then_same_envelope_retries_idempotently(tmp_path):
    with secure_client(tmp_path, FailureMode.DROP_RESPONSE) as client:
        wire = envelope(client)
        first = client.post(SECURE_PATH, json=wire)
        assert first.status_code == 503
        records = client.app.state.repository.list()
        assert len(records) == 1
        client.app.state.failure_injector = FailureInjector(FailureMode.NONE, 0.0, None, 0)
        retry = client.post(SECURE_PATH, json=wire)
        assert retry.status_code == 202
        assert retry.json() == {"status": "already_accepted", "record_id": records[0].record_id}
        assert len(client.app.state.repository.list()) == 1
