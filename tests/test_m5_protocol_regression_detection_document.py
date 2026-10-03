"""Regression checks for the M5-98 protocol-regression coordination index."""

from pathlib import Path


DOCUMENT = Path(__file__).parents[1] / "docs/testing/M5_PROTOCOL_REGRESSION_DETECTION.md"


def test_protocol_regression_index_covers_every_required_contract_category() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    for category in (
        "Legacy/Gateway endpoint, JSON fields, status boundary",
        "Canonical JSON fields and Cloud storage mapping",
        "Gateway/Cloud endpoint and protocol version",
        "Public-key fields and `key_id` semantics",
        "Session request/response fields and errors",
        "ML-KEM suite and HKDF salt/info/length",
        "AES-GCM nonce size and four-field AAD serialization",
        "Exact SecureEnvelope shape",
        "Ordinary retry and session recovery semantics",
        "Health/readiness behavior, ports, and environment mapping",
    ):
        assert category in document


def test_protocol_regression_index_preserves_explicit_prohibited_addition_guards() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    for prohibited in (
        "`cloud_id` or another Cloud identity field",
        "`session_key` in a wire message",
        "Extra session-response field",
        "`message_counter` or dedicated replay counter/window",
        "Fresh encryption on ordinary transport retry",
    ):
        assert prohibited in document
    assert "not\ncryptographic replay protection" in document


def test_protocol_regression_index_records_ci_and_primary_test_evidence() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "complete suite on every push and pull\nrequest" in document
    for path in (
        "edge_gateway/tests/test_gateway_models.py",
        "cloud_service/tests/test_cloud_session_api.py",
        "edge_gateway/tests/test_kdf.py",
        "cloud_service/tests/test_cloud_envelope.py",
        "tests/integration/test_gateway_cloud_secure.py",
        "tests/integration/test_gateway_compose_e2e.py",
    ):
        assert path in document
