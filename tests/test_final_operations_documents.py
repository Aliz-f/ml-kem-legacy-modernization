"""Regression checks for Member 5 final-evaluation and runbook documents."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
EVALUATION = ROOT / "docs" / "evaluation" / "final-evaluation-evidence.md"
DEMOS = ROOT / "docs" / "presentation" / "demo-scenarios.md"
RUNBOOK = ROOT / "docs" / "RUNBOOK.md"


def test_final_evaluation_uses_named_evidence_and_preserves_limitations() -> None:
    document = EVALUATION.read_text(encoding="utf-8")

    for evidence in (
        "test_legacy_mode_success_compatibility.py",
        "test_modernized_end_to_end.py",
        "test_secure_message_tamper.py",
        "test_mlkem_handshake_failure_demo.py",
        "measure_mode_comparison.py",
    ):
        assert evidence in document
    assert "not cryptographic replay protection" in document
    assert "no dedicated cryptographic anti-replay counter" in document


def test_demo_scenarios_cover_baseline_modernized_and_failure_flows() -> None:
    document = DEMOS.read_text(encoding="utf-8")

    for scenario in (
        "SECURITY_MODE=classical",
        "SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed",
        "GATEWAY_FAILURE_MODE=corrupt_ciphertext",
        "CLOUD_FAILURE_MODE=storage_failure",
    ):
        assert scenario in document
    assert "docker compose down --volumes --remove-orphans" in document
    assert "Never show private keys" in document


def test_system_runbook_links_operations_and_states_frozen_recovery_rules() -> None:
    document = RUNBOOK.read_text(encoding="utf-8")

    assert "deployment/compose-test-environment.md" in document
    assert "presentation/demo-scenarios.md" in document
    assert "never performs runtime automatic plaintext fallback" in document
    assert "409 SESSION_INVALID" in document
    assert "same already-built" in document
    assert "not cryptographic replay protection" in document
