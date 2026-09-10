"""Filesystem, Markdown, and Git-status helpers for ai-history."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .models import ACTIVE_STATUSES, Status, state_name


class HistoryError(Exception):
    """A user-correctable history workflow error."""


@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    status: Status
    path: Path
    created: str
    updated: str


def root_from(path: Path | None = None) -> Path:
    current = (path or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise HistoryError("Cannot find repository root (pyproject.toml).")


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def paths(root: Path) -> tuple[Path, Path, Path]:
    ai = root / "docs" / "ai"
    return ai / "history", ai / ".state.json", ai / "templates" / "task.md"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def load_state(root: Path) -> dict[str, object]:
    _, path, _ = paths(root)
    if not path.exists():
        return {"active_task": None, "status": "idle"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HistoryError(f"Invalid state file: {exc}") from exc
    if not isinstance(data, dict):
        raise HistoryError("State file must contain a JSON object.")
    return data


def save_state(root: Path, task_id: str | None, status: Status | None) -> None:
    data = {"active_task": task_id, "status": state_name(status) if status else "idle"}
    atomic_write(paths(root)[1], json.dumps(data, indent=2) + "\n")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "untitled-task"


def parse_task(path: Path) -> Task:
    text = path.read_text(encoding="utf-8")
    heading = re.search(r"^# AI Task (\d{4}) — (.+)$", text, re.MULTILINE)
    status = re.search(r"^\*\*Status:\*\* (.+)$", text, re.MULTILINE)
    created = re.search(r"^\*\*Created:\*\* (.+)$", text, re.MULTILINE)
    updated = re.search(r"^\*\*Updated:\*\* (.+)$", text, re.MULTILINE)
    if not all((heading, status, created, updated)):
        raise HistoryError(f"{path}: missing required metadata.")
    try:
        parsed_status = Status(status.group(1).strip())
    except ValueError as exc:
        raise HistoryError(f"{path}: invalid status {status.group(1)!r}.") from exc
    return Task(
        heading.group(1),
        heading.group(2),
        parsed_status,
        path,
        created.group(1),
        updated.group(1),
    )


def task_files(root: Path) -> list[Task]:
    history, _, _ = paths(root)
    if not history.exists():
        return []
    tasks: list[Task] = []
    for file in history.glob("*.md"):
        tasks.append(parse_task(file))
    return sorted(tasks, key=lambda task: (task.created, task.task_id))


def find_task(root: Path, task_id: str) -> Task:
    normalized = f"{int(task_id):04d}" if task_id.isdigit() else task_id
    matches = [task for task in task_files(root) if task.task_id == normalized]
    if len(matches) != 1:
        raise HistoryError(f"Task {task_id} does not exist.")
    return matches[0]


def active_task(root: Path) -> Task | None:
    state = load_state(root)
    active = state.get("active_task")
    if active is None:
        return None
    if not isinstance(active, str):
        raise HistoryError("State file active_task must be a string or null.")
    return find_task(root, active)


def replace_metadata(task: Task, status: Status) -> None:
    text = task.path.read_text(encoding="utf-8")
    text = re.sub(
        r"^\*\*Status:\*\* .+$",
        f"**Status:** {status}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^\*\*Updated:\*\* .+$",
        f"**Updated:** {now()}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    atomic_write(task.path, text)


def append(task: Task, content: str) -> None:
    text = (
        task.path.read_text(encoding="utf-8").rstrip()
        + "\n\n---\n\n"
        + content.strip()
        + "\n"
    )
    atomic_write(task.path, text)


def git_changes(root: Path) -> dict[str, list[str]] | None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    changes = {"created": [], "modified": [], "deleted": []}
    for line in result.stdout.splitlines():
        code, file = line[:2], line[3:]
        if "?" in code or "A" in code:
            changes["created"].append(file)
        elif "D" in code:
            changes["deleted"].append(file)
        else:
            changes["modified"].append(file)
    return changes


def markdown_list(items: list[str], fallback: str = "None") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {fallback}"


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        tasks = task_files(root)
        state = load_state(root)
    except HistoryError as exc:
        return [str(exc)]
    ids = [task.task_id for task in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task IDs detected.")
    expected = [f"{number:04d}" for number in range(1, len(ids) + 1)]
    if sorted(ids) != expected:
        errors.append("Task IDs must be sequential from 0001.")
    active = [task for task in tasks if task.status in ACTIVE_STATUSES]
    if len(active) > 1:
        errors.append("Only one active task is allowed.")
    expected_id = active[0].task_id if active else None
    expected_status = state_name(active[0].status) if active else "idle"
    if (
        state.get("active_task") != expected_id
        or state.get("status") != expected_status
    ):
        errors.append("State file does not match the active Markdown task.")
    for task in tasks:
        text = task.path.read_text(encoding="utf-8")
        if not re.fullmatch(r"\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md", task.path.name):
            errors.append(f"Task {task.task_id}: invalid filename.")
        for value, label in ((task.created, "Created"), (task.updated, "Updated")):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                errors.append(f"Task {task.task_id}: {label} timestamp is invalid.")
        if (
            task.status == Status.AWAITING_REVIEW
            and "# AI Implementation — Initial" not in text
            and "# AI Revision —" not in text
        ):
            errors.append(
                f"Task {task.task_id}: awaiting review without recorded AI output."
            )
        if (
            "## Decision\n\nModified" in text
            and "## Requested Modifications\n\n" not in text
        ):
            errors.append(
                f"Task {task.task_id}: Modified review lacks requested modifications."
            )
        if task.status == Status.COMPLETE and (
            "## Decision\n\nAccepted" not in text
            or "## Human-Confirmed Verification\n\n" not in text
        ):
            errors.append(
                f"Task {task.task_id}: Complete requires acceptance and human-confirmed verification."
            )
        if task.status == Status.REJECTED and (
            "## Decision\n\nRejected" not in text or "## Problems Found\n\n" not in text
        ):
            errors.append(
                f"Task {task.task_id}: Rejected requires a human decision and problems."
            )
    return errors
