"""M2-09 request IDs and separate baseline/secure transport context."""

from datetime import datetime, timezone
import json
import logging
from uuid import UUID

import httpx
import pytest

from edge_gateway.correlation import baseline_headers, create_request_id
from edge_gateway.crypto.aad import build_aad
from edge_gateway.crypto.encoding import decode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.symmetric import AeadError, decrypt
from edge_gateway.models import LegacyMeasurement
from edge_gateway.normalization import normalize
from edge_gateway.validation import validate_legacy_measurement


@pytest.fixture
def canonical():
    measured_at = datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc)
    received_at = datetime(2026, 9, 21, 13, 45, 32, tzinfo=timezone.utc)
    legacy = validate_legacy_measurement(
        LegacyMeasurement("sensor-private-marker", 21.7, 42.5, measured_at, 184)
    )
    return normalize(legacy, gateway_id="gateway-001", received_at=received_at)


def test_independent_requests_get_distinct_uuid4_ids():
    ids = [create_request_id() for _ in range(100)]
    assert len(set(ids)) == len(ids)
    for request_id in ids:
        assert request_id.startswith("req-")
        identifier = UUID(request_id.removeprefix("req-"))
        assert identifier.version == 4
        assert request_id == f"req-{identifier}"


def test_gateway_logs_generated_id_without_measurement_data(canonical, caplog):
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        request_id = create_request_id()
    record, = caplog.records
    assert record.request_id == request_id
    assert record.getMessage() == f"gateway_request_created request_id={request_id}"
    assert canonical.device_id not in caplog.text
    assert "temperature_c" not in caplog.text


def test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(canonical):
    request_id = create_request_id()
    body = canonical.to_dict()
    for _ in range(2):
        request = httpx.Request(
            "POST", "http://cloud.test/api/v1/baseline/measurements",
            headers=baseline_headers(request_id), json=body,
        )
        assert request.headers["X-Request-ID"] == request_id
        assert json.loads(request.content) == body
        assert "request_id" not in json.loads(request.content)
        assert request_id.encode() not in request.content
    headers = baseline_headers(request_id)
    headers["X-Request-ID"] = "changed"
    assert baseline_headers(request_id) == {"X-Request-ID": request_id}


def test_existing_secure_envelope_authenticates_same_request_context(canonical):
    request_id = create_request_id()
    key = bytes(range(32))  # Fixed test key only.
    envelope = build_secure_envelope(
        key=key, session_id="sess-test", request_id=request_id, **canonical.to_dict()
    )
    assert envelope.as_dict()["request_id"] == request_id
    nonce = decode_binary(envelope.nonce)
    ciphertext = decode_binary(envelope.ciphertext)
    aad = build_aad(
        protocol_version="1", gateway_id=canonical.gateway_id,
        session_id="sess-test", request_id=request_id,
    )
    assert json.loads(decrypt(key, nonce, ciphertext, aad)) == canonical.to_dict()
    wrong_aad = build_aad(
        protocol_version="1", gateway_id=canonical.gateway_id,
        session_id="sess-test", request_id=create_request_id(),
    )
    with pytest.raises(AeadError):
        decrypt(key, nonce, ciphertext, wrong_aad)
