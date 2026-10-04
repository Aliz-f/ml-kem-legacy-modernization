"""Regression checks for Member 5's shared integration-test assets."""

import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
INTEGRATION = ROOT / "tests" / "integration"


def _fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_shared_fixtures_match_the_frozen_legacy_and_canonical_shapes() -> None:
    legacy = _fixture("valid_legacy_measurement.json")
    invalid_temperature = _fixture("invalid_temperature_measurement.json")
    invalid_humidity = _fixture("invalid_humidity_measurement.json")
    invalid_timestamp = _fixture("invalid_timestamp_measurement.json")
    missing_field = _fixture("missing_field_measurement.json")
    canonical = _fixture("canonical_measurement.json")

    assert set(legacy) == {
        "device_id", "temperature_c", "humidity_pct", "timestamp", "sequence_number",
    }
    assert invalid_temperature == {**legacy, "temperature_c": 85.1}
    assert invalid_humidity == {**legacy, "humidity_pct": 100.1}
    assert invalid_timestamp == {**legacy, "timestamp": "not-a-timestamp"}
    assert missing_field == {k: v for k, v in legacy.items() if k != "timestamp"}
    assert set(missing_field) == {
        "device_id", "temperature_c", "humidity_pct", "sequence_number",
    }
    assert set(canonical) == {
        "device_id", "temperature_c", "humidity_pct", "measured_at",
        "sequence_number", "received_at", "gateway_id",
    }
    assert "request_id" not in canonical


def test_shared_fixtures_do_not_embed_crypto_material() -> None:
    forbidden_terms = ("private_key", "public_key", "shared_secret", "session_key")

    for fixture in FIXTURES.glob("*.json"):
        fixture_text = fixture.read_text(encoding="utf-8").lower()
        assert not any(term in fixture_text for term in forbidden_terms)


def test_integration_test_scaffold_reserves_the_planned_boundaries() -> None:
    assert {
        "test_legacy_gateway.py",
        "test_gateway_cloud_baseline.py",
        "test_gateway_cloud_secure.py",
        "test_failure_paths.py",
        "test_end_to_end.py",
    } <= {path.name for path in INTEGRATION.glob("test_*.py")}
