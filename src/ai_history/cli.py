"""Command-line interface for the AI-history workflow."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from .models import ACTIVE_STATUSES, Status
from .storage import (
    HistoryError,
    Task,
    active_task,
    append,
    atomic_write,
    find_task,
    git_changes,
    markdown_list,
    now,
    paths,
    parse_task,
    replace_metadata,
    root_from,
    save_state,
    slugify,
    task_files,
    validate,
)


def parser() -> argparse.ArgumentParser:
    app = argparse.ArgumentParser(
        prog="ai-history", description="Manage human-reviewed AI development history."
    )
    commands = app.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Show the active workflow state.")
    start = commands.add_parser("start", help="Start a new AI-assisted task.")
    start.add_argument("--title", required=True)
    start.add_argument("--task", required=True)
    start.add_argument("--prompt", required=True)
    start.add_argument("--agent", default="Unknown")
    for name, help_text in (
        ("output", "Record completed initial AI implementation."),
        ("revision", "Record a completed AI revision."),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--summary", required=True)
        command.add_argument("--notes", default="None")
        command.add_argument("--command", dest="checks", action="append", default=[])
        command.add_argument("--result", action="append", default=[])
        command.add_argument("--created", action="append", default=[])
        command.add_argument("--modified", action="append", default=[])
        command.add_argument("--deleted", action="append", default=[])
    review = commands.add_parser("review", help="Record a human review.")
    review.add_argument("--problems", required=True)
    review.add_argument(
        "--decision", required=True, choices=["Accepted", "Modified", "Rejected"]
    )
    review.add_argument("--requested-modifications")
    verify = commands.add_parser(
        "verify", help="Record final verification after acceptance."
    )
    verify.add_argument("--human-confirmed", required=True)
    verify.add_argument("--ai-check", action="append", default=[])
    show = commands.add_parser("show", help="Display a task history file.")
    show.add_argument("task_id")
    commands.add_parser("list", help="List task histories.")
    resolve = commands.add_parser(
        "resolve-merge-conflict",
        help="Split a same-ID Git conflict into preserved, sequential histories.",
    )
    resolve.add_argument("conflict_file", help="Conflicted file under docs/ai/history.")
    commands.add_parser("check", help="Validate histories and machine-readable state.")
    return app


def require_active(root: Path, status: Status) -> Task:
    task = active_task(root)
    if task is None or task.status != status:
        raise HistoryError(f"This command requires an active task in status: {status}.")
    return task


def start(root: Path, args: argparse.Namespace) -> None:
    if active_task(root):
        raise HistoryError(
            "An active task already exists; resolve its workflow before starting another."
        )
    tasks = task_files(root)
    task_id = f"{len(tasks) + 1:04d}"
    timestamp = now()
    history, _, _ = paths(root)
    path = history / f"{task_id}-{slugify(args.title)}.md"
    if path.exists():
        raise HistoryError(f"Refusing to overwrite existing history: {path}")
    content = f"# AI Task {task_id} — {args.title}\n\n**Status:** In Progress\n\n**Created:** {timestamp}\n\n**Updated:** {timestamp}\n\n**Agent:** {args.agent}\n\n---\n\n# Task\n\n{args.task}\n\n---\n\n# Prompt\n\n{args.prompt}\n"
    atomic_write(path, content)
    save_state(root, task_id, Status.IN_PROGRESS)
    print(f"Started AI Task {task_id}: {path.relative_to(root)}")


def recorded_changes(root: Path, args: argparse.Namespace) -> dict[str, list[str]]:
    detected = git_changes(root) or {"created": [], "modified": [], "deleted": []}
    return {kind: (getattr(args, kind) or detected[kind]) for kind in detected}


def record_work(root: Path, args: argparse.Namespace, revision: bool) -> None:
    required = Status.REVISION_REQUESTED if revision else Status.IN_PROGRESS
    task = require_active(root, required)
    changes = recorded_changes(root, args)
    heading = (
        f"# AI Revision — Round {task.path.read_text(encoding='utf-8').count('# AI Revision —') + 1}"
        if revision
        else "# AI Implementation — Initial"
    )
    summary_heading = "## Revision Summary" if revision else "## LLM Output"
    commands = markdown_list(args.checks, "No commands recorded.")
    results = markdown_list(args.result, "No command results recorded.")
    append(
        task,
        f"{heading}\n\n{summary_heading}\n\n{args.summary}\n\n## Files Created\n\n{markdown_list(changes['created'])}\n\n## Files Modified\n\n{markdown_list(changes['modified'])}\n\n## Files Deleted\n\n{markdown_list(changes['deleted'])}\n\n## AI-Executed Verification\n\n### Commands\n\n{commands}\n\n### Results\n\n{results}\n\n## AI Notes\n\n{args.notes}",
    )
    replace_metadata(task, Status.AWAITING_REVIEW)
    save_state(root, task.task_id, Status.AWAITING_REVIEW)
    print(f"AI work recorded. Task {task.task_id} is now Awaiting Human Review.")
    print(
        "Review the implementation and provide Problems Found, Decision, and Requested Modifications if Modified."
    )


def review(root: Path, args: argparse.Namespace) -> None:
    task = require_active(root, Status.AWAITING_REVIEW)
    if args.decision == "Modified" and not args.requested_modifications:
        raise HistoryError(
            "Requested Modifications is required when Decision is Modified."
        )
    number = task.path.read_text(encoding="utf-8").count("# Human Review —") + 1
    section = f"# Human Review — Round {number}\n\n## Problems Found\n\n{args.problems}\n\n## Decision\n\n{args.decision}"
    if args.requested_modifications:
        section += f"\n\n## Requested Modifications\n\n{args.requested_modifications}"
    append(task, section)
    status = {
        "Accepted": Status.AWAITING_VERIFICATION,
        "Modified": Status.REVISION_REQUESTED,
        "Rejected": Status.REJECTED,
    }[args.decision]
    replace_metadata(task, status)
    save_state(
        root,
        None if status == Status.REJECTED else task.task_id,
        None if status == Status.REJECTED else status,
    )
    print(f"Human review recorded. Task {task.task_id} is now {status}.")


def verify(root: Path, args: argparse.Namespace) -> None:
    task = require_active(root, Status.AWAITING_VERIFICATION)
    append(
        task,
        f"# Final Verification\n\n## AI-Executed Verification\n\n{markdown_list(args.ai_check, 'No additional AI checks recorded.')}\n\n## Human-Confirmed Verification\n\n{args.human_confirmed}\n\n---\n\n# Final Outcome\n\n**Status:** Complete",
    )
    replace_metadata(task, Status.COMPLETE)
    save_state(root, None, None)
    print(f"Task {task.task_id} is Complete.")


def status(root: Path) -> None:
    errors = validate(root)
    if errors:
        raise HistoryError("State validation failed:\n- " + "\n- ".join(errors))
    task = active_task(root)
    print("AI History Status\n" + "─" * 32)
    if task:
        print(
            f"Active task: {task.task_id}\nStatus: {task.status}\nHistory file: {task.path.relative_to(root)}"
        )
    else:
        print("No active task.\nReady for a new AI-assisted task.")


def resolve_merge_conflict(root: Path, args: argparse.Namespace) -> None:
    history, _, _ = paths(root)
    path = (root / args.conflict_file).resolve()
    if history.resolve() not in path.parents:
        raise HistoryError("Conflict file must be inside docs/ai/history.")
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(
        r"<<<<<<<[^\n]*\n(.*?)=======\n(.*?)>>>>>>>[^\n]*\n?", text, re.S
    )
    if not match:
        raise HistoryError("File is not a simple two-way Git conflict.")
    first, second = match.group(1), match.group(2)

    def details(value: str) -> tuple[str, str, str, Status]:
        heading = re.search(r"^# AI Task (\d{4}) — (.+)$", value, re.M)
        created = re.search(r"^\*\*Created:\*\* (.+)$", value, re.M)
        status = re.search(r"^\*\*Status:\*\* (.+)$", value, re.M)
        if not heading or not created or not status:
            raise HistoryError("Each conflict side must contain valid task metadata.")
        try:
            parsed_status = Status(status.group(1).strip())
        except ValueError as exc:
            raise HistoryError("Each conflict side must contain valid task metadata.") from exc
        return heading.group(1), heading.group(2), created.group(1), parsed_status

    first_id, _, first_created, first_status = details(first)
    second_id, second_title, second_created, second_status = details(second)
    if first_id != second_id:
        raise HistoryError(
            "This command only resolves conflicts with the same task ID."
        )
    existing = [parse_task(file) for file in history.glob("*.md") if file != path]
    if (
        first_status in ACTIVE_STATUSES
        or second_status in ACTIVE_STATUSES
        or any(task.status in ACTIVE_STATUSES for task in existing)
    ):
        raise HistoryError(
            "Resolve active-task conflicts manually before using this command."
        )
    earlier, later = (
        (first, second) if first_created <= second_created else (second, first)
    )
    next_id = max([int(task.task_id) for task in existing] + [int(first_id)]) + 1
    new_id = f"{next_id:04d}"
    later = re.sub(
        r"^# AI Task \d{4} —", f"# AI Task {new_id} —", later, count=1, flags=re.M
    )
    atomic_write(path, earlier)
    new_path = history / f"{new_id}-{slugify(second_title)}.md"
    atomic_write(new_path, later)
    print(
        f"Resolved conflict: kept {first_id}; preserved later task as {new_id}: {new_path.relative_to(root)}"
    )


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        root = root_from()
        if args.command == "start":
            start(root, args)
        elif args.command == "output":
            record_work(root, args, False)
        elif args.command == "revision":
            record_work(root, args, True)
        elif args.command == "review":
            review(root, args)
        elif args.command == "verify":
            verify(root, args)
        elif args.command == "status":
            status(root)
        elif args.command == "show":
            print(
                find_task(root, args.task_id).path.read_text(encoding="utf-8"), end=""
            )
        elif args.command == "list":
            print("ID    Status                       Title")
            for task in task_files(root):
                print(f"{task.task_id}  {str(task.status):<27} {task.title}")
        elif args.command == "resolve-merge-conflict":
            resolve_merge_conflict(root, args)
        elif args.command == "check":
            errors = validate(root)
            if errors:
                raise HistoryError("\n".join(f"ERROR: {error}" for error in errors))
            print("AI history validation passed.")
    except HistoryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
