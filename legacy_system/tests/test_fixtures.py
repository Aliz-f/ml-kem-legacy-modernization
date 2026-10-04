"""Tests verifying that integration test fixtures adhere to Legacy Device domain rules."""

from datetime import datetime
import json
from pathlib import Path

import pytest

from legacy_system.sensor import Measurement


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures"


def _load_fixture(filename: str) -> dict[str, object]:
    path = FIXTURES_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model() -> None:
    data = _load_fixture("valid_legacy_measurement.json")
    measurement = Measurement(
        device_id=str(data["device_id"]),
        temperature_c=float(data["temperature_c"]),
        humidity_pct=float(data["humidity_pct"]),
        timestamp=datetime.fromisoformat(str(data["timestamp"])),
        sequence_number=int(data["sequence_number"]),
    )
    assert measurement.to_payload() == data


def test_invalid_temperature_fixture_fails_domain_validation() -> None:
    data = _load_fixture("invalid_temperature_measurement.json")
    with pytest.raises(ValueError, match="temperature_c must be between -40.0 and 85.0"):
        Measurement(
            device_id=str(data["device_id"]),
            temperature_c=float(data["temperature_c"]),
            humidity_pct=float(data["humidity_pct"]),
            timestamp=datetime.fromisoformat(str(data["timestamp"])),
            sequence_number=int(data["sequence_number"]),
        )


def test_invalid_humidity_fixture_fails_domain_validation() -> None:
    data = _load_fixture("invalid_humidity_measurement.json")
    with pytest.raises(ValueError, match="humidity_pct must be between 0.0 and 100.0"):
        Measurement(
            device_id=str(data["device_id"]),
            temperature_c=float(data["temperature_c"]),
            humidity_pct=float(data["humidity_pct"]),
            timestamp=datetime.fromisoformat(str(data["timestamp"])),
            sequence_number=int(data["sequence_number"]),
        )


def test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp() -> None:
    data = _load_fixture("invalid_timestamp_measurement.json")
    with pytest.raises(ValueError):
        datetime.fromisoformat(str(data["timestamp"]))


def test_missing_field_fixture_omits_timestamp() -> None:
    data = _load_fixture("missing_field_measurement.json")
    assert "timestamp" not in data
    assert set(data) == {"device_id", "temperature_c", "humidity_pct", "sequence_number"}

