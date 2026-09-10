from __future__ import annotations

from pathlib import Path

from ai_history import cli
from ai_history.storage import load_state, validate


def run(tmp_path: Path, monkeypatch, *arguments: str) -> int:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='test'\nversion='0'\n")
    monkeypatch.chdir(tmp_path)
    return cli.main(list(arguments))


def start(tmp_path: Path, monkeypatch) -> None:
    assert (
        run(
            tmp_path,
            monkeypatch,
            "start",
            "--title",
            "Safe title!",
            "--task",
            "Task",
            "--prompt",
            "line one\nline two",
            "--agent",
            "Test",
        )
        == 0
    )


def test_first_id_slug_and_multiline_prompt(tmp_path, monkeypatch):
    start(tmp_path, monkeypatch)
    file = tmp_path / "docs/ai/history/0001-safe-title.md"
    assert file.exists() and "line one\nline two" in file.read_text()


def test_full_acceptance_lifecycle(tmp_path, monkeypatch):
    start(tmp_path, monkeypatch)
    assert run(tmp_path, monkeypatch, "output", "--summary", "Done") == 0
    assert (
        run(
            tmp_path,
            monkeypatch,
            "review",
            "--problems",
            "None",
            "--decision",
            "Accepted",
        )
        == 0
    )
    assert (
        run(
            tmp_path,
            monkeypatch,
            "verify",
            "--human-confirmed",
            "Inspected final result.",
        )
        == 0
    )
    assert load_state(tmp_path)["status"] == "idle"
    assert not validate(tmp_path)


def test_modified_requires_changes_and_revision_preserves_rounds(tmp_path, monkeypatch):
    start(tmp_path, monkeypatch)
    run(tmp_path, monkeypatch, "output", "--summary", "Done")
    assert (
        run(
            tmp_path,
            monkeypatch,
            "review",
            "--problems",
            "Issue",
            "--decision",
            "Modified",
        )
        == 1
    )
    assert (
        run(
            tmp_path,
            monkeypatch,
            "review",
            "--problems",
            "Issue",
            "--decision",
            "Modified",
            "--requested-modifications",
            "Fix it",
        )
        == 0
    )
    assert run(tmp_path, monkeypatch, "revision", "--summary", "Fixed") == 0
    text = next((tmp_path / "docs/ai/history").glob("*.md")).read_text()
    assert "# Human Review — Round 1" in text and "# AI Revision — Round 1" in text


def test_rejection_and_second_task(tmp_path, monkeypatch):
    start(tmp_path, monkeypatch)
    run(tmp_path, monkeypatch, "output", "--summary", "Done")
    run(
        tmp_path,
        monkeypatch,
        "review",
        "--problems",
        "Unsafe",
        "--decision",
        "Rejected",
    )
    assert (
        run(
            tmp_path,
            monkeypatch,
            "start",
            "--title",
            "Next",
            "--task",
            "Task",
            "--prompt",
            "Prompt",
        )
        == 0
    )
    assert (tmp_path / "docs/ai/history/0002-next.md").exists()


def test_cannot_start_while_active_or_corrupt_state(tmp_path, monkeypatch):
    start(tmp_path, monkeypatch)
    assert (
        run(
            tmp_path,
            monkeypatch,
            "start",
            "--title",
            "Other",
            "--task",
            "x",
            "--prompt",
            "x",
        )
        == 1
    )
    (tmp_path / "docs/ai/.state.json").write_text(
        '{"active_task":"9999","status":"in_progress"}'
    )
    assert run(tmp_path, monkeypatch, "check") == 1
