"""M4-33 wire schema only; encoding/domain validation belongs to M4-34."""

from dataclasses import FrozenInstanceError, fields
import json

import pytest

from cloud_service.crypto.envelope import EnvelopeSchemaError, SecureEnvelope
from edge_gateway.crypto.envelope import build_secure_envelope


def payload():
    return dict(protocol_version="1", gateway_id="gateway-001", session_id="sess-1",
                request_id="req-1", nonce="AAECAwQFBgcICQoL", ciphertext="encoded-ciphertext")


def test_exact_fields_immutable_and_independent_dictionary():
    original = payload()
    model = SecureEnvelope.from_dict(original)
    assert [field.name for field in fields(model)] == list(original)
    assert model.to_dict() == original
    original["gateway_id"] = "changed"
    returned = model.to_dict()
    returned["request_id"] = "changed"
    assert model.gateway_id == "gateway-001"
    assert model.request_id == "req-1"
    with pytest.raises(FrozenInstanceError):
        model.nonce = "changed"
    with pytest.raises(AttributeError):
        model.__dict__


def test_existing_gateway_builder_wire_round_trip():
    gateway = build_secure_envelope(
        key=bytes(range(32)), session_id="sess-1", request_id="req-1",
        device_id="sensor-1", temperature_c=21.7, humidity_pct=42.5,
        measured_at="2026-09-29T12:00:00Z", sequence_number=1,
        received_at="2026-09-29T12:00:01Z", gateway_id="gateway-001",
    )
    wire = json.loads(json.dumps(gateway.as_dict()))
    cloud = SecureEnvelope.from_dict(wire)
    assert cloud.to_dict() == gateway.as_dict()
    assert isinstance(cloud.nonce, str) and isinstance(cloud.ciphertext, str)


@pytest.mark.parametrize("field", list(payload()))
def test_missing_field_rejected(field):
    value = payload()
    del value[field]
    with pytest.raises(EnvelopeSchemaError):
        SecureEnvelope.from_dict(value)


@pytest.mark.parametrize("extra", ["message_counter", "cloud_id", "session_key", "plaintext", "extra"])
def test_extra_fields_rejected_without_echo(extra):
    with pytest.raises(EnvelopeSchemaError) as caught:
        SecureEnvelope.from_dict(payload() | {extra: "sensitive-marker"})
    assert "sensitive-marker" not in str(caught.value)


@pytest.mark.parametrize("field", list(payload()))
@pytest.mark.parametrize("value", [None, 1, True, b"bytes", [], {}])
def test_wrong_types_rejected_for_parsing_and_direct_construction(field, value):
    values = payload() | {field: value}
    with pytest.raises(EnvelopeSchemaError):
        SecureEnvelope.from_dict(values)
    with pytest.raises(EnvelopeSchemaError):
        SecureEnvelope(**values)


@pytest.mark.parametrize("value", [None, [], "{}", b"{}", 1])
def test_nonobjects_rejected(value):
    with pytest.raises(EnvelopeSchemaError):
        SecureEnvelope.from_dict(value)


def test_model_preserves_strings_without_claiming_security_validation():
    # Intentional M4-33 boundary: schema construction is not acceptance for use.
    values = payload() | {"protocol_version": "2", "gateway_id": "", "nonce": "%invalid%", "ciphertext": ""}
    assert SecureEnvelope.from_dict(values).to_dict() == values
