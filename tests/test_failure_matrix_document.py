"""Regression checks for the frozen project-wide failure-test matrix."""

from pathlib import Path
import re


MATRIX = Path(__file__).parents[1] / "docs/testing/FAILURE_TEST_MATRIX.md"


def test_failure_matrix_covers_the_complete_planned_scenario_set() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    assert re.findall(r"\| F(\d+) \|", document) == [str(number) for number in range(1, 19)]
    for task in ("M5-40", "M5-41", "M5-42", "M5-43", "M5-44"):
        assert task in document


def test_failure_matrix_preserves_secure_recovery_and_retransmission_rules() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    assert "409 SESSION_INVALID" in document
    assert "409 SESSION_EXPIRED" in document
    assert "one bounded re-establishment attempt" in document
    assert "same request ID, session ID,\nnonce, ciphertext, and AAD" in document
    assert "no baseline call or plaintext fallback" in document


def test_failure_matrix_records_mlkem_and_replay_scope_limits() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    assert "implicit rejection" in document
    assert "no dedicated cryptographic replay counter or window" in document
    assert "UNIQUE(device_id, sequence_number)" in document
