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
        "# Graph Report - project  (2026-10-01)\n\n## Graph Freshness\nBuilt from commit.\n\n## Nodes\nNone.\n",
        encoding="utf-8",
    )

    refresh_graphify.normalize_artifacts(tmp_path)

    assert json.loads(graph_path.read_text(encoding="utf-8")) == {"nodes": []}
    assert report_path.read_text(encoding="utf-8") == "# Graph Report - project\n\n## Nodes\nNone.\n"


def test_clear_incremental_state_removes_all_prior_graphify_output(
    tmp_path: Path,
) -> None:
    graph_path = tmp_path / "graph.json"
    report_path = tmp_path / "GRAPH_REPORT.md"
    graph_path.write_text("shared graph", encoding="utf-8")
    report_path.write_text("shared report", encoding="utf-8")
    (tmp_path / "manifest.json").write_text("incremental state", encoding="utf-8")
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "stamp").write_text("incremental state", encoding="utf-8")
    backup = tmp_path / "2026-09-30"
    backup.mkdir()
    (backup / "graph.json").write_text("generated backup", encoding="utf-8")

    refresh_graphify.clear_incremental_state(tmp_path)

    assert not graph_path.exists()
    assert not report_path.exists()
    assert list(tmp_path.iterdir()) == []


def test_report_is_identical_across_local_and_ci_dates(tmp_path: Path) -> None:
    outputs = []
    # Same instant straddling midnight locally/UTC, plus a later build day.
    for day in ("2026-10-01", "2026-09-30", "2027-01-01"):
        graph_path = tmp_path / "graph.json"
        report_path = tmp_path / "GRAPH_REPORT.md"
        graph_path.write_text('{"nodes": [], "built_at_commit": "abc"}', encoding="utf-8")
        report_path.write_text(
            f"# Graph Report - project  ({day})\n\n"
            "## Graph Freshness\nVolatile metadata.\n\n"
            "## Nodes\nSource date: 2026-09-30\n",
            encoding="utf-8",
        )
        refresh_graphify.normalize_artifacts(tmp_path)
        first = (graph_path.read_bytes(), report_path.read_bytes())
        refresh_graphify.normalize_artifacts(tmp_path)
        assert (graph_path.read_bytes(), report_path.read_bytes()) == first
        outputs.append(first)

    assert outputs[0] == outputs[1] == outputs[2]
    assert report_path.read_text(encoding="utf-8") == (
        "# Graph Report - project\n\n## Nodes\nSource date: 2026-09-30\n"
    )


def test_refresh_uses_a_stable_hash_seed(tmp_path: Path, monkeypatch) -> None:
    calls: list[dict[str, object]] = []
    monkeypatch.delenv("PYTHONHASHSEED", raising=False)
    monkeypatch.setattr(refresh_graphify, "clear_incremental_state", lambda _: None)
    monkeypatch.setattr(refresh_graphify, "normalize_artifacts", lambda _: None)
    monkeypatch.setattr(
        refresh_graphify.subprocess,
        "run",
        lambda *_, **kwargs: calls.append(kwargs),
    )

    refresh_graphify.refresh_graph(tmp_path)

    assert len(calls) == 2
    assert all(call["env"]["PYTHONHASHSEED"] == "0" for call in calls)
