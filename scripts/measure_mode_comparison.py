"""Run the equivalent classical and ML-KEM M5 evaluation workloads.

Example: ``uv run python scripts/measure_mode_comparison.py --samples 10``.
The output contains actual observations from that invocation; it intentionally
does not ship fixed timing values.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def _load(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(samples: int = 10) -> dict[str, object]:
    """Run one matched workload in each explicit security mode."""
    if type(samples) is not int or not 2 <= samples <= 100:
        raise ValueError("samples must be an integer from 2 to 100")
    baseline = _load("measure_baseline_e2e.py").run(samples)
    modernized = _load("measure_modernized_e2e.py").run(samples)
    baseline_first = baseline["first_message"]
    baseline_steady = baseline["steady_state"]
    modern_first = modernized["first_message"]
    modern_steady = modernized["steady_state"]
    if not all(isinstance(value, dict) for value in (baseline_first, baseline_steady, modern_first, modern_steady)):
        raise RuntimeError("matched workload did not produce first and steady-state observations")
    session = modernized["session_establishment"]
    if not isinstance(session, dict):
        raise RuntimeError("modernized report did not contain session metrics")
    baseline_successful = baseline["successful_messages"]
    modernized_successful = modernized["successful_messages"]
    if not isinstance(baseline_successful, int) or not isinstance(modernized_successful, int):
        raise RuntimeError("workload reports did not contain successful-message counts")
    return {
        "scope": "Matched local Legacy -> Gateway -> Cloud -> SQLite workloads",
        "samples": samples,
        "comparison": {
            "first_message_latency_ms": {
                "classical": baseline_first["legacy_gateway_end_to_end_ms"],
                "mlkem": modern_first["legacy_gateway_end_to_end_ms"],
            },
            "steady_state_latency_ms": {
                "classical": baseline_steady["legacy_gateway_end_to_end_ms"],
                "mlkem": modern_steady["legacy_gateway_end_to_end_ms"],
            },
            "gateway_to_cloud_payload_bytes": {
                "classical": baseline["canonical_payload_bytes"],
                "mlkem": modernized["secure_envelope_bytes"],
            },
            "session_setup": {"classical": "not_applicable", "mlkem": session},
            "successful_messages": {
                "classical": baseline_successful,
                "mlkem": modernized_successful,
            },
            "failed_messages": {
                "classical": samples - baseline_successful,
                "mlkem": samples - modernized_successful,
            },
            "storage_success": {
                "classical": baseline["persisted_rows"],
                "mlkem": modernized["persisted_rows"],
            },
        },
        "baseline_report": baseline,
        "modernized_report": modernized,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=10)
    print(json.dumps(run(parser.parse_args().samples), indent=2, sort_keys=True))
