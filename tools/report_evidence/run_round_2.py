"""Collect second-round, matched local evidence without changing service behavior.

The command starts disposable loopback ASGI applications and temporary SQLite
databases via the existing production-path measurement harnesses.  It retains
every successful observation, including the separately reported first request
of each run; no latency observations are filtered as outliers.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime
import importlib.util
import json
import os
from importlib.metadata import version
from pathlib import Path
import platform
import statistics
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "report-evidence" / "verification-round-2"


def load_script(name: str) -> Any:
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def distribution(values: list[float] | list[int], unit: str = "ms") -> dict[str, Any]:
    if not values:
        raise ValueError("cannot summarize no observations")
    ordered = sorted(values)
    return {
        "count": len(values), "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else None,
        "min": ordered[0], "p95": ordered[(len(ordered) * 95 + 99) // 100 - 1],
        "max": ordered[-1], "values": values, "unit": unit,
    }


def invoke(name: str, samples: int) -> dict[str, Any]:
    module = load_script(name)
    module.distribution = lambda observations: distribution(observations)
    return module.run(samples)


def values(run: dict[str, Any], *path: str) -> list[float]:
    node: Any = run
    for key in path:
        node = node[key]
    return list(node["values"])


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).isoformat()
    runs_per_mode, messages_per_run, cold_sessions = 3, 30, 30
    baseline_runs = [invoke("measure_baseline_e2e.py", messages_per_run) for _ in range(runs_per_mode)]
    secure_runs = [invoke("measure_modernized_e2e.py", messages_per_run) for _ in range(runs_per_mode)]
    # Each two-message run is an independent service/session lifecycle.  Its first
    # message is the cold-session observation; the second only validates delivery.
    cold_runs = [invoke("measure_modernized_e2e.py", 2) for _ in range(cold_sessions)]

    classical_steady = [v for run in baseline_runs for v in values(run, "steady_state", "legacy_gateway_end_to_end_ms")]
    secure_steady = [v for run in secure_runs for v in values(run, "steady_state", "legacy_gateway_end_to_end_ms")]
    classical_first = [values(run, "first_message", "legacy_gateway_end_to_end_ms")[0] for run in baseline_runs]
    secure_first = [values(run, "first_message", "legacy_gateway_end_to_end_ms")[0] for run in cold_runs]
    metric_paths = {
        "handshake_ms": ("gateway_handshake_ms",),
        "public_key_retrieval_ms": ("gateway_public_key_ms",),
        "encapsulation_ms": ("gateway_encapsulation_ms",),
        "decapsulation_ms": ("cloud_decapsulation_ms",),
    }
    cold_metrics = {
        name: [values(run, "session_establishment", *path)[0] for run in cold_runs]
        for name, path in metric_paths.items()
    }
    classical_payloads = [v for run in baseline_runs for v in values(run, "canonical_payload_bytes")]
    secure_payloads = [v for run in secure_runs for v in values(run, "secure_envelope_bytes")]
    classical_summary, secure_summary = distribution(classical_steady), distribution(secure_steady)
    overhead = secure_summary["mean"] - classical_summary["mean"]
    summary: dict[str, Any] = {
        "run_identity": {
            "commit": git("rev-parse", "HEAD"), "timestamp_utc": timestamp,
            "working_tree_status_before_artifacts": git("status", "--short"),
        },
        "method": {
            "timing_boundary": "Legacy client send immediately before HTTP request through Gateway and Cloud to returned Legacy response",
            "workload": "sequential valid logical messages; disposable loopback ASGI services and temporary SQLite; no warm-up, concurrency, or injected failure",
            "runs_per_mode": runs_per_mode, "logical_messages_per_run": messages_per_run,
            "cold_session_runs": cold_sessions,
            "startup_policy": "first measurement of every independent baseline and secure steady-state run excluded only from primary steady-state populations and retained separately",
        },
        "classical": {"first_message_latency_ms": distribution(classical_first), "steady_state_latency_ms": classical_summary,
                      "per_run_steady_state_ms": [distribution(values(run, "steady_state", "legacy_gateway_end_to_end_ms")) for run in baseline_runs],
                      "payload_bytes": distribution(classical_payloads)},
        "modernized": {"first_message_latency_ms": distribution(secure_first), "steady_state_latency_ms": secure_summary,
                        "per_run_steady_state_ms": [distribution(values(run, "steady_state", "legacy_gateway_end_to_end_ms")) for run in secure_runs],
                        "payload_bytes": distribution(secure_payloads),
                        "session_reuse": {"authenticated_messages": 90, "initial_sessions": sum(run["session_establishment"]["cloud_sessions_created"] for run in secure_runs), "messages_per_session": 30, "unexpected_reestablishments": sum(run["session_establishment"]["gateway_session_reestablishments"] for run in secure_runs)}},
        "cold_session": {name: distribution(observations) for name, observations in cold_metrics.items()} | {"first_secure_message_latency_ms": distribution(secure_first)},
        "payload_comparison": {"absolute_overhead_bytes": statistics.fmean(secure_payloads) - statistics.fmean(classical_payloads), "relative_overhead_percent": (statistics.fmean(secure_payloads) - statistics.fmean(classical_payloads)) / statistics.fmean(classical_payloads) * 100},
        "comparison": {"absolute_steady_state_overhead_ms": overhead, "relative_steady_state_overhead_percent": overhead / classical_summary["mean"] * 100},
        "limitations": ["Loopback ASGI and temporary SQLite results are not Docker, WAN, throughput, load, or production measurements.", "CPU and memory use were not measured.", "The existing harness does not capture serialized public-key or session-request body sizes.", "Cold observations are independent session/service lifecycles, not independent hosts."]
    }
    (OUTPUT / "benchmark_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (OUTPUT / "measurements.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["mode", "run", "phase", "metric", "observation", "unit"])
        for mode, runs in (("classical", baseline_runs), ("mlkem", secure_runs)):
            for number, run in enumerate(runs, 1):
                writer.writerow([mode, number, "first", "legacy_gateway_end_to_end_latency", values(run, "first_message", "legacy_gateway_end_to_end_ms")[0], "ms"])
                for observation in values(run, "steady_state", "legacy_gateway_end_to_end_ms"):
                    writer.writerow([mode, number, "steady", "legacy_gateway_end_to_end_latency", observation, "ms"])
        for number, run in enumerate(cold_runs, 1):
            writer.writerow(["mlkem", number, "cold", "first_secure_message_latency", values(run, "first_message", "legacy_gateway_end_to_end_ms")[0], "ms"])
            for name, path in metric_paths.items():
                writer.writerow(["mlkem", number, "cold", name, values(run, "session_establishment", *path)[0], "ms"])
    memory = next((line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines() if line.startswith("MemTotal:")), "unknown")
    docker = subprocess.run(["docker", "--version"], text=True, capture_output=True, check=False)
    environment = {"timestamp_utc": timestamp, "git_commit": summary["run_identity"]["commit"], "python": platform.python_version(), "os": platform.platform(), "machine": platform.machine(), "logical_cpu_count": os.cpu_count(), "memory_total_kib": memory, "docker": docker.stdout.strip() if docker.returncode == 0 else "unavailable", "cryptography": version("cryptography"), "fastapi": version("fastapi"), "uvicorn": version("uvicorn")}
    (OUTPUT / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUTPUT / "methodology.md").write_text("# Verification round 2 methodology\n\n" + "Command: `UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python tools/report_evidence/run_round_2.py`.\n\n" + "The primary comparison excludes exactly one first observation from every independent 30-message run in both modes (3 × 29 = 87 each); raw first-message observations remain in `measurements.csv`. Cold-session metrics use 30 independent two-message service/session lifecycles. No observations were deleted as outliers.\n\n" + "Timing, payload, lifecycle, and scope limitations are machine-readable in `benchmark_summary.json`.\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
