"""Refresh and normalize the shared Graphify code graph."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GRAPH_OUTPUT = REPOSITORY_ROOT / "graphify-out"


def refresh_graph(root: Path) -> None:
    """Build the local code-only graph and its report."""
    subprocess.run(
        ["uv", "run", "graphify", "extract", ".", "--code-only", "--no-viz"],
        cwd=root,
        check=True,
    )
    subprocess.run(
        ["uv", "run", "graphify", "cluster-only", ".", "--no-viz"],
        cwd=root,
        check=True,
    )
    normalize_artifacts(root / "graphify-out")


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
