"""Refresh and normalize the shared Graphify code graph."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GRAPH_OUTPUT = REPOSITORY_ROOT / "graphify-out"
_SHARED_ARTIFACTS = frozenset({"graph.json", "GRAPH_REPORT.md"})


def refresh_graph(root: Path) -> None:
    """Build the local code-only graph and its report."""
    clear_incremental_state(root / "graphify-out")
    environment = {**os.environ, "PYTHONHASHSEED": "0"}
    subprocess.run(
        ["uv", "run", "graphify", "extract", ".", "--code-only", "--no-viz"],
        cwd=root,
        check=True,
        env=environment,
    )
    subprocess.run(
        ["uv", "run", "graphify", "cluster-only", ".", "--no-viz"],
        cwd=root,
        check=True,
        env=environment,
    )
    normalize_artifacts(root / "graphify-out")


def clear_incremental_state(output_directory: Path) -> None:
    """Remove ignored Graphify state so refresh matches a clean CI checkout."""
    if not output_directory.exists():
        return
    for path in output_directory.iterdir():
        if path.name in _SHARED_ARTIFACTS:
            continue
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()


def normalize_artifacts(output_directory: Path) -> None:
    """Remove Graphify metadata that varies only with the local Git checkout."""
    graph_path = output_directory / "graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph.pop("built_at_commit", None)
    graph_path.write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    report_path = output_directory / "GRAPH_REPORT.md"
    report_path.write_text(
        _without_section(
            report_path.read_text(encoding="utf-8"), "## Graph Freshness\n"
        ),
        encoding="utf-8",
    )


def _without_section(content: str, heading: str) -> str:
    start = content.find(heading)
    if start == -1:
        return content
    end = content.find("\n## ", start + len(heading))
    if end == -1:
        return content[:start]
    return content[:start] + content[end + 1 :]


if __name__ == "__main__":
    refresh_graph(REPOSITORY_ROOT)
