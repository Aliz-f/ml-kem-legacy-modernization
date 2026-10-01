"""Session secrets stay in process memory, and replacement clears the old key."""

from pathlib import Path

DOCUMENT = Path(__file__).parents[1] / "docs" / "session-memory.md"
README = Path(__file__).parents[1] / "README.md"
SESSION_SOURCE = (
    Path(__file__).parents[1] / "src" / "edge_gateway" / "crypto" / "session.py"
)


def test_session_memory_records_process_only_storage() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "process memory only" in document
    assert "debug dump" in document
    assert "cache file" in document
    assert "SQLite" in document
    assert "JSON state" in document
    assert "AI history" in document
    assert "Tests do not save snapshots that contain real key bytes." in document


def test_session_memory_states_the_zeroization_limitation() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "cleared and dereferenced" in document
    assert "Python does not guarantee secure memory zeroization." in document
    assert "does not remove every copy" in document


def test_readme_points_at_the_session_memory_limitation() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/session-memory.md" in readme
    assert "process memory" in readme
    assert "Python does not guarantee secure memory zeroization" in readme


def test_session_module_does_not_persist_session_state() -> None:
    source = SESSION_SOURCE.read_text(encoding="utf-8")

    assert "sqlite" not in source.lower()
    assert "json" not in source.lower()
    assert "pickle" not in source.lower()
