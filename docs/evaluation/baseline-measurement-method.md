# Classical baseline measurement method

This M5-32 record makes the M5-31 classical baseline harness reproducible. It
defines one workload and its measurement boundaries; it is not a comparison
with Modernized Mode and does not claim capacity or deployment performance.

## Run

From the repository root with the locked development environment installed:

```bash
uv sync --frozen
uv run python scripts/measure_baseline_e2e.py --samples 10
```

The command prints one JSON report. Retain that complete output with any
evaluation result because it contains the detected Python, OS, machine,
SQLite, FastAPI, HTTPX, and Uvicorn versions. The temporary database is deleted
when the command finishes; the report is the measurement artifact.

## Fixed workload and configuration

| Item | Value |
| --- | --- |
| Number of messages | 10 sequential messages by default (`--samples 10`) |
| Permitted run size | 1–100 sequential messages; record the chosen value from `samples` |
| Legacy measurement | `sensor-baseline-harness`, 22.5 °C, 44.0 %, UTC `2026-10-02T12:00:00Z`, sequences 0 through `samples - 1` |
| Security mode | `SECURITY_MODE=classical` at Gateway and Cloud |
| Failure mode | `FAILURE_MODE=none` at Gateway and Cloud |
| Legacy client | 5 s timeout; zero retries |
| Gateway-to-Cloud client | 5 s timeout; zero retries |
| Deployment boundary | disposable Uvicorn services on one host using loopback HTTP and a temporary file-backed SQLite database |
| Load generation | sequential only; no warm-up, concurrency, or injected fault |

Do not compare runs with different message counts, retry settings, failure
modes, or deployment boundaries as equivalent measurements. A later ML-KEM
comparison must use a separately documented equivalent workload and report its
first-message/session-establishment cost independently.

## Measurement method and boundaries

The harness creates a production `Measurement`, sends it through the production
`GatewayClient`, a live Gateway route, the production baseline Cloud client, a
live Cloud route, and SQLite. It confirms all rows are persisted exactly once
through the Cloud query API before producing the report.

| Report field | Boundary |
| --- | --- |
| `legacy_gateway_end_to_end_ms` | Legacy client call through its received Gateway response |
| `gateway_request_ms` | Gateway middleware entry through route response, including downstream delivery |
| `gateway_cloud_request_ms` | Cloud baseline route middleware entry through response |
| `cloud_storage_ms` | Cloud repository `save_idempotent` call, including SQLite work |
| `canonical_payload_bytes` | Actual canonical JSON body bytes observed at Cloud; excludes HTTP headers |
| `successful_messages` / `persisted_rows` | Accepted Legacy sends and rows queried from Cloud |
| `gateway_cloud_retry_count` | Observed Cloud requests minus logical messages |

All durations use `perf_counter()` and are observations, not acceptance
thresholds. Harness middleware and timing wrappers add local measurement
overhead. The run does not measure a Docker deployment, network latency beyond
the local host, throughput under load, or ML-KEM session establishment.
