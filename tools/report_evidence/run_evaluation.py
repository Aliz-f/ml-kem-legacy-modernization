"""Create sanitized, reproducible report evidence from isolated local runs.

Run with ``uv run python tools/report_evidence/run_evaluation.py``.  The
script starts only disposable loopback ASGI services and temporary SQLite
databases through the existing measurement harnesses.  It never uses Compose
services, persistent databases, or secret-bearing configuration.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime
import importlib.util
import json
from importlib.metadata import version
from pathlib import Path
import platform
import statistics
import subprocess
import os
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "report-evidence"


def load_script(name: str) -> Any:
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def distribution(values: list[float] | list[int], unit: str = "ms") -> dict[str, Any]:
    """Return raw observations plus descriptive statistics; no inference."""
    ordered = sorted(values)
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else None,
        "min": ordered[0],
        "p95": ordered[(len(ordered) * 95 + 99) // 100 - 1],
        "max": ordered[-1],
        "values": values,
        "unit": unit,
    }


def invoke(name: str, samples: int) -> dict[str, Any]:
    module = load_script(name)
    module.distribution = distribution
    return module.run(samples)


def flatten(runs: list[dict[str, Any]], path: tuple[str, ...]) -> list[float]:
    values: list[float] = []
    for run in runs:
        value: Any = run
        for key in path:
            value = value[key]
        values.extend(value["values"])
    return values


def git(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def write_markdown(summary: dict[str, Any]) -> None:
    modern = summary["modernized"]
    baseline = summary["classical"]
    p = OUTPUT / "methodology.md"
    p.write_text(
        "# Reproducible report-evidence methodology\n\n"
        f"Run identity: `{summary['run_identity']['commit']}` at "
        f"`{summary['run_identity']['timestamp_utc']}`.\n\n"
        "The collector makes three independent runs per explicit mode, each with 30 "
        "sequential valid Legacy measurements. It calls the existing production-client "
        "harnesses: Legacy client → disposable loopback Gateway → disposable loopback "
        "Cloud → temporary file-backed SQLite. No Compose service, persistent database, "
        "or sensor five-second interval is used. Timing begins immediately before the "
        "Legacy client sends and ends after its response; `perf_counter()` is used.\n\n"
        "A cold secure first message includes public-key retrieval, encapsulation, session "
        "request/decapsulation/HKDF/session creation, and secure delivery. Steady-state "
        "secure delivery excludes it. The harness has no warm-up, no concurrent load, no "
        "injected failures, and zero Legacy/Gateway Cloud retries. Values are local-host "
        "observations, not production capacity or network measurements.\n\n"
        f"Classical successful messages: {baseline['successful_messages']}; ML-KEM successful "
        f"messages: {modern['successful_messages']}. Raw observations and descriptive "
        "statistics are in `measurements.csv` and `benchmark_summary.json`.\n",
        encoding="utf-8",
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    samples, runs_count = 30, 3
    classical_runs = [invoke("measure_baseline_e2e.py", samples) for _ in range(runs_count)]
    modern_runs = [invoke("measure_modernized_e2e.py", samples) for _ in range(runs_count)]
    classical_values = flatten(classical_runs, ("legacy_gateway_end_to_end_ms",))
    secure_steady_values = flatten(modern_runs, ("steady_state", "legacy_gateway_end_to_end_ms"))
    secure_first_values = flatten(modern_runs, ("first_message", "legacy_gateway_end_to_end_ms"))
    handshake_values = [run["session_establishment"]["gateway_handshake_ms"]["values"][0] for run in modern_runs]
    public_key_values = [run["session_establishment"]["gateway_public_key_ms"]["values"][0] for run in modern_runs]
    encapsulation_values = [run["session_establishment"]["gateway_encapsulation_ms"]["values"][0] for run in modern_runs]
    decapsulation_values = [run["session_establishment"]["cloud_decapsulation_ms"]["values"][0] for run in modern_runs]
    payload_classical = flatten(classical_runs, ("canonical_payload_bytes",))
    payload_secure = flatten(modern_runs, ("secure_envelope_bytes",))
    summary = {
        "run_identity": {
            "commit": git(["git", "rev-parse", "HEAD"]),
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "working_tree_status_before_artifacts": git(["git", "status", "--short"]),
        },
        "configuration": {"runs_per_mode": runs_count, "logical_messages_per_run": samples,
                          "security_modes": ["classical", "mlkem"], "pqc_failure_policy": "fail_closed"},
        "classical": {"successful_messages": runs_count * samples, "latency_ms": distribution(classical_values),
                      "payload_bytes": distribution(payload_classical, "bytes")},
        "modernized": {"successful_messages": runs_count * samples,
                         "steady_state_latency_ms": distribution(secure_steady_values),
                         "first_message_latency_ms": distribution(secure_first_values),
                         "handshake_ms": distribution(handshake_values),
                         "public_key_retrieval_ms": distribution(public_key_values),
                         "encapsulation_ms": distribution(encapsulation_values),
                         "decapsulation_ms": distribution(decapsulation_values),
                         "payload_bytes": distribution(payload_secure, "bytes"),
                         "session_creations": sum(r["session_establishment"]["cloud_sessions_created"] for r in modern_runs),
                         "authenticated_messages": runs_count * samples},
        "limitations": [
            "Cold-session observations are n=3, below the requested target of 20.",
            "CPU and memory usage were not measured; do not estimate them.",
            "Serialized public-key response and session-request sizes were not captured by this harness.",
            "Loopback HTTP and temporary SQLite are not Docker, WAN, load, or production measurements.",
        ],
    }
    steady_mean = summary["modernized"]["steady_state_latency_ms"]["mean"]
    classical_mean = summary["classical"]["latency_ms"]["mean"]
    summary["comparison"] = {"absolute_steady_state_overhead_ms": steady_mean - classical_mean,
                             "relative_steady_state_overhead_percent": (steady_mean - classical_mean) / classical_mean * 100}
    with (OUTPUT / "benchmark_summary.json").open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, sort_keys=True)
        file.write("\n")
    with (OUTPUT / "measurements.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["mode", "metric", "observation", "unit"])
        for mode, metric, values in (("classical", "end_to_end_latency", classical_values),
                                     ("mlkem", "steady_state_end_to_end_latency", secure_steady_values),
                                     ("mlkem", "first_message_end_to_end_latency", secure_first_values),
                                     ("mlkem", "handshake", handshake_values)):
            writer.writerows((mode, metric, value, "ms") for value in values)
    memory_kib = next((line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines()
                       if line.startswith("MemTotal:")), "unknown")
    docker = subprocess.run(["docker", "--version"], text=True, capture_output=True, check=False)
    environment = {"python": platform.python_version(), "os": platform.platform(),
                   "machine": platform.machine(), "processor": platform.processor(),
                   "logical_cpu_count": os.cpu_count(), "memory_total_kib": memory_kib,
                   "docker": docker.stdout.strip() if docker.returncode == 0 else "unavailable",
                   "cryptography": version("cryptography"), "fastapi": version("fastapi"),
                   "uvicorn": version("uvicorn"), "mlkem_implementation": "cryptography ML-KEM API"}
    (OUTPUT / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
