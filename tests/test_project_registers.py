"""Regression checks for M5-81/82 project-wide coordination registers."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
DEBT = ROOT / "docs/technical-debt.md"
RISK = ROOT / "docs/risk-register.md"


def test_technical_debt_register_covers_the_frozen_cross_component_limits() -> None:
    document = DEBT.read_text(encoding="utf-8")

    for entry in (
        "No authentication on the Legacy Device → Gateway HTTP/JSON boundary",
        "No persistent Gateway queue or store-and-forward buffer",
        "Gateway sequence state is in memory",
        "Secure sessions are in memory",
        "Cloud ML-KEM key pair is ephemeral",
        "Simplified Cloud public-key trust",
        "SQLite and single-instance services",
        "No dedicated cryptographic anti-replay counter/window",
        "Python cannot guarantee secure memory zeroization",
    ):
        assert entry in document
    assert "not cryptographic replay protection" in document
    assert "TD-10 and TD-11 are deliberately separate entries" in document


def test_risk_register_is_separate_from_debt_and_records_required_events() -> None:
    document = RISK.read_text(encoding="utf-8")

    assert "distinct from the accepted implementation limitations" in document
    for event in (
        "substitutes the Cloud ML-KEM public key",
        "spoofs or modifies Legacy → Gateway traffic",
        "authenticated secure envelope is replayed",
        "outage causes a measurement delivery failure or loss",
        "Retry layers increase downstream work",
        "restart loses sequence/session/key state",
        "Future diagnostics expose private keys",
    ):
        assert event in document


def test_registers_do_not_overstate_current_controls() -> None:
    debt = DEBT.read_text(encoding="utf-8")
    risk = RISK.read_text(encoding="utf-8")

    assert "It is **not cryptographic replay protection**" in debt
    assert "does not claim that the current controls remove the listed\nrisks" in risk
    assert "no dedicated cryptographic anti-replay counter or\nwindow" in debt
