# Modernized measurement method

This M5-65 through M5-69 harness measures the same local workload as the
classical method, through the production Legacy client, Gateway route, Cloud
routes, and temporary file-backed SQLite database. It reports observations; it
does not establish a performance target or capacity claim.

Run it from the repository root:

```bash
uv sync --frozen
uv run python scripts/measure_modernized_e2e.py --samples 10
```

Use 2–100 sequential messages. The fixed workload is `sensor-baseline-harness`,
22.5 °C, 44.0 %, UTC `2026-10-02T12:00:00Z`, and sequence numbers starting at
zero. It uses `SECURITY_MODE=mlkem`, `PQC_FAILURE_POLICY=fail_closed`, no
injected faults, five-second timeouts, and zero Legacy/Gateway retries. These
values deliberately match the baseline method; do not compare differing
workloads as a PQC effect.

The output separates the first secure message from steady-state messages. The
first message includes public-key retrieval, ML-KEM-768 encapsulation and Cloud
decapsulation, the fixed HKDF-SHA-256 derivation, session establishment, and
secure delivery. Steady-state messages reuse that session and measure secure
delivery without averaging the setup cost into every message.

The report also records actual SecureEnvelope JSON bytes observed at the Cloud
boundary, storage timings, successful/persisted rows, request retries, and the
bounded Gateway/Cloud session metrics: handshake duration, public-key and
encapsulation duration, Cloud decapsulation duration, created/failed/active
sessions, re-establishments, encryption failures, decryption failures, and the
always-zero protocol-v1 fallback counter. Identifiers never become metric
labels, and no secret value is printed or persisted.

The disposable services and database are local loopback evidence only. Record
the complete JSON output, including environment versions, alongside any report
or presentation claim.
