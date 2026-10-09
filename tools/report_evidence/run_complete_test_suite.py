"""Run every collected pytest node in resumable, bounded batches.

This is evidence infrastructure, not a test-semantic timeout wrapper: it never
sets pytest timeouts.  Each completed batch is recorded from JUnit XML, while
an interrupted process leaves its nodes unexecuted for a later invocation.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "docs" / "report-evidence" / "verification-final"


def command(*parts: str) -> list[str]:
    return [sys.executable, "-m", "pytest", *parts]


def collect_nodes() -> list[str]:
    result = subprocess.run(command("--collect-only", "-q", "--disable-warnings"), cwd=ROOT, text=True, capture_output=True, check=True)
    return [line for line in result.stdout.splitlines() if "::" in line]


def load_manifest(path: Path, nodes: list[str]) -> dict[str, object]:
    if path.exists():
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("collected_nodes") != nodes:
            raise RuntimeError("collected node set changed; use a new output directory")
        return manifest
    return {"started_at_utc": datetime.now(UTC).isoformat(), "collected_nodes": nodes, "results": {}, "batches": []}


def write_manifest(path: Path, manifest: dict[str, object]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def junit_results(path: Path, selected: list[str]) -> dict[str, str]:
    root = ET.parse(path).getroot()
    results: dict[str, str] = {}
    for case in root.iter("testcase"):
        name = case.attrib.get("name", "")
        matching = [node for node in selected if node.rsplit("::", 1)[-1] == name]
        if len(matching) != 1:
            continue
        node = matching[0]
        # Default JUnit classname can omit workspace package segments, so match
        # the unique selected node by its pytest-preserved test name.
        status = "passed"
        if case.find("failure") is not None:
            status = "failed"
        elif case.find("error") is not None:
            status = "error"
        elif case.find("skipped") is not None:
            status = "skipped"
        results[node] = status
    return results


def batch_size(nodes: list[str], ordinary_size: int) -> int:
    # Compose and image tests can build/restart containers and must be isolated.
    if "test_gateway_compose_e2e.py" in nodes[0] or "test_gateway_crypto_image.py" in nodes[0]:
        return 1
    return ordinary_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--max-seconds", type=float, default=20.0)
    parser.add_argument("--defer-compose", action="store_true", help="leave Docker Compose/image nodes unexecuted for isolated handling")
    parser.add_argument("--rerun-failed", action="store_true", help="remove failed node records before executing them again")
    args = parser.parse_args()
    if args.batch_size < 1 or args.max_seconds <= 0:
        raise SystemExit("batch size and max seconds must be positive")
    output = args.output.resolve()
    logs = output / "test-logs"
    logs.mkdir(parents=True, exist_ok=True)
    nodes = collect_nodes()
    manifest_path = output / "test_coverage_manifest.json"
    manifest = load_manifest(manifest_path, nodes)
    results = manifest["results"]
    assert isinstance(results, dict)
    if args.rerun_failed:
        for node, status in list(results.items()):
            if status in {"failed", "error"}:
                del results[node]
    started = monotonic()
    while monotonic() - started < args.max_seconds:
        remaining = [node for node in nodes if node not in results]
        if args.defer_compose:
            remaining = [node for node in remaining if "test_gateway_compose_e2e.py" not in node and "test_gateway_crypto_image.py" not in node]
        if not remaining:
            break
        size = batch_size(remaining, args.batch_size)
        selected = remaining[:size]
        index = len(manifest["batches"]) + 1  # type: ignore[index]
        junit = logs / f"batch-{index:04d}.xml"
        log = logs / f"batch-{index:04d}.txt"
        launched = datetime.now(UTC).isoformat()
        began = monotonic()
        completed = subprocess.run(command("-q", f"--junitxml={junit}", *selected), cwd=ROOT, text=True, capture_output=True, check=False)
        duration = monotonic() - began
        log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
        parsed = junit_results(junit, selected) if junit.exists() else {}
        # JUnit uses forward-slash relative paths; only record IDs actually returned.
        for node in selected:
            found = parsed.get(node)
            if found is not None:
                results[node] = found
        manifest["batches"].append({"id": index, "nodes": selected, "started_at_utc": launched, "duration_seconds": duration, "exit_code": completed.returncode, "log": log.relative_to(output).as_posix(), "junit": junit.relative_to(output).as_posix(), "recorded_nodes": sum(node in results for node in selected)})  # type: ignore[index]
        write_manifest(manifest_path, manifest)
        # A no-JUnit batch may have been externally interrupted; do not spin or mark it passed.
        if not parsed:
            break
    manifest["finished_at_utc"] = datetime.now(UTC).isoformat()
    manifest["accounting"] = {"collected": len(nodes), "recorded": len(results), "unexecuted": len(nodes) - len(results)}
    write_manifest(manifest_path, manifest)
    print(json.dumps(manifest["accounting"], sort_keys=True))


if __name__ == "__main__":
    main()
