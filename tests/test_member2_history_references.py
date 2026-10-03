"""Regression checks for corrected Member 2 AI-history traceability."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
FINAL_EVALUATION = ROOT / "edge_gateway/docs/pr13-final-evaluation.md"
HISTORY = ROOT / "docs/ai/history/0148-m2-53-through-m2-69-gateway-final-evaluation-and-documentation.md"


def test_member2_final_evaluation_points_to_the_actual_completed_task_records() -> None:
    document = FINAL_EVALUATION.read_text(encoding="utf-8")

    for task_id in range(141, 149):
        assert f"`0{task_id}`" in document
    for stale_id in ("`0123`", "`0130`", "`0131`", "`0132`", "`0133`", "`0134`", "`0135`", "`0136`"):
        assert stale_id not in document
    assert "completed human review and verification" in document


def test_m2_final_history_record_names_its_actual_file_and_completed_review_state() -> None:
    document = HISTORY.read_text(encoding="utf-8")

    assert "docs/ai/history/0148-m2-53-through-m2-69-gateway-final-evaluation-and-documentation.md" in document
    assert "completed human review and final verification for task 0148" in document
    assert "task 0136" not in document
