"""Tests for stable shared Graphify artifact normalization."""

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "refresh_graphify.py"
SPEC = importlib.util.spec_from_file_location("refresh_graphify", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
refresh_graphify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refresh_graphify)


def test_normalize_artifacts_removes_checkout_specific_metadata(tmp_path: Path) -> None:
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(
        json.dumps({"nodes": [], "built_at_commit": "abc123"}), encoding="utf-8"
    )
    report_path = tmp_path / "GRAPH_REPORT.md"
    report_path.write_text(
        "# Report\n\n## Graph Freshness\nBuilt from commit.\n\n## Nodes\nNone.\n",
        encoding="utf-8",
    )

    refresh_graphify.normalize_artifacts(tmp_path)

    assert json.loads(graph_path.read_text(encoding="utf-8")) == {"nodes": []}
    assert report_path.read_text(encoding="utf-8") == "# Report\n\n## Nodes\nNone.\n"
