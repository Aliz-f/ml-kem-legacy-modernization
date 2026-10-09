import importlib.util
from pathlib import Path


_PATH = Path(__file__).resolve().parents[1] / "tools" / "report_evidence" / "run_round_2.py"
_SPEC = importlib.util.spec_from_file_location("round_2_evidence", _PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
distribution = _MODULE.distribution


def test_distribution_keeps_payload_units() -> None:
    assert distribution([221, 222], "bytes")["unit"] == "bytes"


def test_distribution_uses_nearest_rank_p95_and_sample_stdev() -> None:
    result = distribution([1.0, 2.0, 3.0, 4.0, 5.0])
    assert result["p95"] == 5.0
    assert result["stdev"] > 1.5
