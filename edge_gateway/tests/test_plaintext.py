"""Canonical measurement plaintext."""

from __future__ import annotations

import json

import pytest

from edge_gateway.crypto.plaintext import PlaintextError, serialize_canonical_measurement


def _measurement(**overrides: object) -> bytes:
    fields: dict[str, object] = {
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
        "gateway_id": "gateway-001",
    }
    fields.update(overrides)
    return serialize_canonical_measurement(**fields)  # type: ignore[arg-type]


def test_protocol_example_is_deterministic_utf8_json():
    expected = (
        b'{"device_id":"sensor-001","temperature_c":21.7,"humidity_pct":42.5,'
        b'"measured_at":"2026-09-21T13:45:31Z","sequence_number":184,'
        b'"received_at":"2026-09-21T13:45:31.218Z","gateway_id":"gateway-001"}'
    )
    assert _measurement() == expected
    assert _measurement() == _measurement()


def test_explicit_utc_offsets_are_preserved():
    encoded = _measurement(
        measured_at="2026-09-21T13:45:31+00:00",
        received_at="2026-09-21T13:45:31.218+00:00",
    )
    assert b"2026-09-21T13:45:31+00:00" in encoded
    assert b"2026-09-21T13:45:31.218+00:00" in encoded


def test_non_finite_numbers_booleans_and_local_timestamps_are_rejected():
    for overrides in (
        {"temperature_c": float("nan")},
        {"humidity_pct": float("inf")},
        {"temperature_c": float("-inf")},
        {"temperature_c": True},
        {"sequence_number": False},
        {"sequence_number": 1.5},
        {"device_id": ""},
        {"device_id": " \t\n"},
        {"gateway_id": "gateway-001 "},
        {"measured_at": "2026-09-21T13:45:31"},
        {"received_at": "2026-09-21T13:45:31+03:00"},
        {"measured_at": "yesterday"},
        {"humidity_pct": "42.5"},
    ):
        with pytest.raises(PlaintextError):
            _measurement(**overrides)


def test_device_id_whitespace_is_preserved_like_baseline_delivery():
    assert json.loads(_measurement(device_id=" sensor-001 "))["device_id"] == " sensor-001 "
