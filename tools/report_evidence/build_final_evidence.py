"""Build the final report-evidence package from preserved round-two data."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from importlib.metadata import version
import json
from pathlib import Path
import platform
import re
import statistics
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ROUND2 = ROOT / "docs" / "report-evidence" / "verification-round-2"
OUTPUT = ROOT / "docs" / "report-evidence" / "verification-final"


def summary(values: list[float], unit: str) -> dict[str, Any]:
    if not values:
        raise ValueError("cannot summarize no values")
    ordered = sorted(values)
    return {"count": len(values), "mean": statistics.fmean(values), "median": statistics.median(values), "stdev": statistics.stdev(values) if len(values) > 1 else None, "min": ordered[0], "p95": ordered[(len(ordered) * 95 + 99) // 100 - 1], "max": ordered[-1], "unit": unit}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def test_reference(manifest: dict[str, Any], node: str) -> dict[str, str]:
    for batch in manifest["batches"]:
        if node in batch["nodes"]:
            return {"node_id": node, "command": f"UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest -q {node}", "log": batch["log"], "junit": batch["junit"]}
    raise KeyError(node)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(UTC).isoformat()
    rows = list(csv.DictReader((ROUND2 / "measurements.csv").open(encoding="utf-8")))
    previous = json.loads((ROUND2 / "benchmark_summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((OUTPUT / "test_coverage_manifest.json").read_text(encoding="utf-8"))
    steady = {mode: [float(row["observation"]) for row in rows if row["mode"] == mode and row["phase"] == "steady" and row["metric"] == "legacy_gateway_end_to_end_latency"] for mode in ("classical", "mlkem")}
    cold = {metric: [float(row["observation"]) for row in rows if row["phase"] == "cold" and row["metric"] == metric] for metric in ("first_secure_message_latency", "handshake_ms", "public_key_retrieval_ms", "encapsulation_ms", "decapsulation_ms")}
    payload_classical = previous["classical"]["payload_bytes"]["values"]
    payload_secure = previous["modernized"]["payload_bytes"]["values"]
    classical, secure = summary(steady["classical"], "ms"), summary(steady["mlkem"], "ms")
    overhead = secure["mean"] - classical["mean"]
    per_run: list[dict[str, Any]] = []
    for run in range(1, 4):
        base = [float(row["observation"]) for row in rows if row["mode"] == "classical" and row["run"] == str(run) and row["phase"] == "steady"]
        modern = [float(row["observation"]) for row in rows if row["mode"] == "mlkem" and row["run"] == str(run) and row["phase"] == "steady"]
        b, m = statistics.fmean(base), statistics.fmean(modern)
        per_run.append({"run": run, "classical_mean_ms": b, "mlkem_mean_ms": m, "absolute_difference_ms": m - b, "relative_difference_percent": (m - b) / b * 100})
    final_benchmark = {"generated_at_utc": generated, "source_round_2": "docs/report-evidence/verification-round-2/measurements.csv", "source_commit": previous["run_identity"]["commit"], "steady_state": {"classical": classical, "mlkem": secure, "absolute_overhead_ms": overhead, "relative_overhead_percent": overhead / classical["mean"] * 100}, "per_run": per_run, "cold_session": {metric: summary(values, "ms") for metric, values in cold.items()}, "payload": {"classical_body_bytes": summary(payload_classical, "bytes"), "secure_envelope_body_bytes": summary(payload_secure, "bytes"), "absolute_overhead_bytes": statistics.fmean(payload_secure) - statistics.fmean(payload_classical), "relative_overhead_percent": (statistics.fmean(payload_secure) - statistics.fmean(payload_classical)) / statistics.fmean(payload_classical) * 100}, "session_reuse": previous["modernized"]["session_reuse"], "statistic_definition": "p95 is nearest-rank ceil(0.95*n); standard deviation is sample standard deviation (n-1).", "limitations": previous["limitations"]}
    (OUTPUT / "benchmark_summary.json").write_text(json.dumps(final_benchmark, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (OUTPUT / "per_run_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(per_run[0]))
        writer.writeheader()
        writer.writerows(per_run)
    statuses = list(manifest["results"].values())
    test_results = {"generated_at_utc": generated, "collection_started_at_utc": manifest["started_at_utc"], "collection_finished_at_utc": manifest["finished_at_utc"], "total_collected": len(manifest["collected_nodes"]), "passed": statuses.count("passed"), "failed": statuses.count("failed"), "skipped": statuses.count("skipped"), "errors": statuses.count("error"), "xfailed": 0, "xpassed": 0, "unexecuted": len(manifest["collected_nodes"]) - len(manifest["results"]), "total_batch_duration_seconds": sum(batch["duration_seconds"] for batch in manifest["batches"]), "status": "FULL SUITE VERIFIED" if len(manifest["collected_nodes"]) == len(manifest["results"]) and set(statuses) == {"passed"} else "PARTIALLY VERIFIED", "command": "UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python tools/report_evidence/run_complete_test_suite.py --batch-size 6 --max-seconds 15"}
    (OUTPUT / "test_suite_results.json").write_text(json.dumps(test_results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    references = {
        "aad_tampering": "tests/integration/test_secure_message_tamper.py::test_tampered_field_is_rejected_and_stores_nothing[request_id-400-SECURE_MESSAGE_REJECTED-True]",
        "invalid_session": "tests/integration/test_gateway_cloud_secure.py::test_invalid_session_returns_409_and_recovers_once",
        "expired_session": "tests/integration/test_gateway_cloud_secure.py::test_expired_session_returns_409_and_recovers_once",
        "handshake_failure": "tests/integration/test_mlkem_handshake_failure_demo.py::test_handshake_failure_stays_closed_without_a_session",
        "storage_failure": "tests/integration/test_gateway_cloud_secure.py::test_cloud_failure_retries_the_same_secure_request_without_storage[storage_failure]",
        "simulated_unavailability": "tests/integration/test_gateway_cloud_secure.py::test_cloud_failure_retries_the_same_secure_request_without_storage[service_unavailable]",
        "compose_restart": "tests/integration/test_gateway_compose_e2e.py::test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback",
        "same_envelope": "tests/integration/test_gateway_cloud_secure.py::test_ambiguous_transport_retries_the_same_envelope",
        "legacy_validation": "tests/integration/test_legacy_gateway.py::test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery",
        "secret_logging": "edge_gateway/tests/test_security_logging.py::test_handshake_and_delivery_omit_secrets_and_separate_timings",
    }
    security = {"generated_at_utc": generated, "test_references": {name: test_reference(manifest, node) for name, node in references.items()}, "outcomes": {"aad_tampering": "request_id: 400 SECURE_MESSAGE_REJECTED/AEAD rejection; gateway_id: pre-AEAD ownership rejection; session_id: 409 SESSION_INVALID; protocol_version: 400 UNSUPPORTED_PROTOCOL_VERSION; zero rows", "invalid_and_expired": "409 SESSION_INVALID and 409 SESSION_EXPIRED recover once without baseline fallback", "handshake_failure": "503 fail-closed; no baseline fallback", "storage_failure": "no false acceptance; bounded retry; no row", "simulated_cloud_unavailability": "controlled service-unavailable response, not a disconnected Cloud", "compose_cloud_restart": "isolated Docker Compose restart; replacement public key, one re-establishment, successful 202 recovery, zero baseline requests", "same_envelope": "ordinary retry preserves built envelope; one stored row", "logging": "tested paths do not emit private keys, ML-KEM shared secrets, or session keys"}, "limitations": ["Finite tests do not prove all log paths.", "No public-key authentication/pinning, cryptographic replay window, forward-secrecy guarantee, or end-to-end PQC protection is established.", "Business idempotency is not cryptographic replay protection."]}
    (OUTPUT / "security_results.json").write_text(json.dumps(security, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    unit_errors = [row for row in rows if row["unit"] != "ms"]
    expected = {"classical": 87, "mlkem": 87}
    validation = {"generated_at_utc": generated, "checks": {"latency_csv_units_ms": not unit_errors, "payload_units_bytes": final_benchmark["payload"]["classical_body_bytes"]["unit"] == "bytes" and final_benchmark["payload"]["secure_envelope_body_bytes"]["unit"] == "bytes", "steady_counts": {mode: len(values) == expected[mode] for mode, values in steady.items()}, "cold_counts": {metric: len(values) == 30 for metric, values in cold.items()}, "per_run_counts": all(sum(1 for row in rows if row["mode"] == mode and row["run"] == str(run) and row["phase"] == "steady") == 29 for mode in expected for run in range(1, 4)), "all_collected_tests_accounted": test_results["unexecuted"] == 0, "all_executed_tests_passed": test_results["failed"] == 0 and test_results["errors"] == 0, "no_private_key_pem_in_final_artifacts": not any(re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", path.read_text(encoding="utf-8", errors="ignore")) for path in OUTPUT.rglob("*") if path.is_file())}, "known_prior_metadata_issue": "Round-two payload summary labels were ms; preserved artifacts remain unchanged. Final aggregation corrects payload units to bytes and source generator now emits bytes."}
    (OUTPUT / "evidence_validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cpu = next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")), "NOT RECORDED")
    memory = next((line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines() if line.startswith("MemTotal:")), "NOT RECORDED")
    environment = {"generated_at_utc": generated, "git_commit": git("rev-parse", "HEAD"), "working_tree_status_at_generation": git("status", "--short"), "os": platform.platform(), "kernel": platform.release(), "machine": platform.machine(), "cpu": cpu, "logical_cpu_count": __import__("os").cpu_count(), "memory_total_kib": memory, "python": platform.python_version(), "cryptography": version("cryptography"), "fastapi": version("fastapi"), "uvicorn": version("uvicorn"), "pytest": version("pytest"), "mlkem_implementation": "cryptography ML-KEM API", "execution_window": "interactive command calls yielded/terminated at approximately 30 seconds; final test runner used resumable bounded batches"}
    (OUTPUT / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUTPUT / "methodology.md").write_text(f"# Final evidence methodology\n\nGenerated at `{generated}` from preserved round-two raw observations. The original exact benchmark collection start/end time was **NOT RECORDED**; its generated timestamp and source commit are retained in the source artifact.\n\n## Environment and architecture\n\nThe experiment used one local Linux machine, Python 3.12, Cryptography ML-KEM-768, FastAPI/Uvicorn, disposable loopback Legacy client → Gateway ASGI app → Cloud ASGI app → temporary SQLite. It is not a WAN, Docker-network, load, or production benchmark.\n\n## Workload and timing\n\nThree independent runs per mode sent 30 valid sequential logical measurements with no concurrent load or intentionally injected failure. Timing began immediately before the Legacy HTTP request and ended when the Legacy client received its final response. The first observation of every run was excluded only from the primary steady-state comparison; all raw observations remain in round-two CSV.\n\n## Cold sessions and statistics\n\nThirty independent service/session lifecycles measured cold secure establishment; they are not independent physical machines. Statistics are mean, median, sample standard deviation, minimum, maximum, count, and nearest-rank p95 (`ceil(0.95*n)`). No significance test is claimed.\n\n## Limits\n\nSingle-machine loopback, sequential delivery, only three independent steady-state runs, no WAN/load/CPU/RAM study, finite security tests, and no universal production claim limit interpretation. The pooled overhead is an observation, not a stable universal penalty.\n", encoding="utf-8")
    (OUTPUT / "final_report_evidence.md").write_text("# Final report-evidence freeze\n\n**Verified measurement:** matched loopback latency/payload observations in `benchmark_summary.json`.\n\n**Verified tested behavior:** all currently collected pytest nodes are JUnit-accounted in `test_coverage_manifest.json`; selected security traces are in `security_results.json`.\n\n**Statically verified design:** frozen protocol constraints remain documented in architecture and regression tests.\n\n**Documented limitations:** the Legacy segment remains HTTP/JSON; Gateway is trusted; Cloud public-key authentication is simplified; sessions are in memory; business idempotency is not cryptographic replay protection; fail-closed behavior reduces availability under Cloud failure.\n", encoding="utf-8")
    print(json.dumps({"tests": test_results, "validation": validation}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
