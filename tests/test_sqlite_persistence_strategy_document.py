"""Regression checks for the Member 5 SQLite persistence guidance."""

from pathlib import Path


STRATEGY = Path(__file__).parents[1] / "docs/deployment/sqlite-persistence.md"


def test_strategy_describes_demo_and_clean_test_modes() -> None:
    document = STRATEGY.read_text(encoding="utf-8")

    assert "Development and demonstration mode" in document
    assert "Clean automated-test mode" in document
    assert "sqlite:////data/cloud.db" in document
    assert "sqlite:///:memory:" in document
    assert "fresh temporary volume" in document


def test_strategy_preserves_storage_and_secret_boundaries() -> None:
    document = STRATEGY.read_text(encoding="utf-8")

    assert "UNIQUE(device_id, sequence_number)" in document
    for prohibited in (
        "ML-KEM private keys",
        "ML-KEM shared secrets",
        "derived session\nkeys",
        "secure-session state",
    ):
        assert prohibited in document
    assert "Docker Compose services" in document
    assert "does not add" in document
