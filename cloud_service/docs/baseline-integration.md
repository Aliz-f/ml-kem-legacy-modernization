# M4-14 / M4-15 baseline integration evidence

The Cloud-local harness imports the existing
`edge_gateway.crypto.plaintext.serialize_canonical_measurement` serializer and
sends its bytes with `Content-Type: application/json` and `X-Request-ID` through
HTTPX to a real Uvicorn Cloud server on an ephemeral loopback port. Cloud runs
in explicit `classical` mode with a fresh file-backed SQLite database.

This verifies serializer-to-Cloud integration. It is **not a full Gateway HTTP
client integration**: Gateway routing, normalization, sequence policy, retries,
Legacy delivery, Docker networking and secure transport are not exercised. The
full baseline E2E milestone still requires Member 2's Gateway application/client
and Member 5's system integration. No Gateway source or production Cloud code
was changed for these tasks. M4-16 is not started.

## Reproduce

From the workspace root, using the existing frozen workspace dependencies:

```powershell
uv sync --frozen --all-packages --all-extras
$env:UV_NO_SYNC='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
uv run python cloud_service/tools/measure_baseline.py --samples 100
uv run pytest cloud_service/tests/test_baseline_integration.py -q
```

The harness prints JSON only after all checks succeed and deletes its temporary
database after closing it. It uses isolated configuration, bypasses environment
HTTP proxies, and does not read production data. Sample counts are limited to
1–1000, matching the query endpoint limit. Tests use three inserts and make no
timing threshold assertions.

Checks cover all seven canonical fields (timestamps compared as UTC instants),
`received_at` → `gateway_received_at`, generated `record_id` and
`cloud_received_at`, the absence of `request_id` from the body and stored model,
request/record correlation in Cloud logs, list/detail responses, duplicate
identity, and persistence after server shutdown and database reopening.
`/health` returns 200. `/ready` remains the existing 503 placeholder; this work
does not claim full readiness or deployment verification.

## Measurement method

One HTTPX client performs 100 sequential unique inserts without concurrency or
retries. A health/readiness probe precedes ingestion; there are no discarded
insert warmups. The first insert is included. Each payload uses fixed synthetic
IDs, temperature 21.7, humidity 42.5, fixed UTC timestamps, and sequence 0–99.

- Request latency: `perf_counter` around `client.post`, including HTTP transport,
  Cloud validation, worker scheduling, storage and response receipt; excludes
  canonical serialization, query verification and JSON response decoding.
- Storage latency: a harness-only repository subclass times the entire existing
  `save_idempotent` method, including mapping, lock acquisition, SQL and commit.
  It is a subset of request latency, not a pure SQLite engine measurement.
- Payload size: actual serialized UTF-8 request body bytes, excluding HTTP
  headers, responses and transport overhead.
- Median and nearest-rank p95 are computed across successful unique inserts.
  One duplicate and one failed write are measured separately.
- Failure injection: `PRAGMA query_only = ON` on the disposable Cloud connection
  causes a real SQLite write error; it is reset in `finally`. This is harness
  instrumentation, not the later runtime failure-injection framework.

## Observed run

Run at **2026-09-29T13:38:03.239697+00:00** on Windows, Python 3.12.14,
SQLite 3.53.1, FastAPI 0.141.1, Uvicorn 0.54.0 and HTTPX 0.28.1.
Values below are measured, rounded to three decimal places.

| Metric (100 inserts) | Minimum | Median | p95 | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Request latency (ms) | 5.875 | 8.082 | 10.429 | 40.614 |
| Storage latency (ms) | 3.535 | 5.148 | 7.249 | 27.720 |
| Payload size (bytes) | 202 | 203 | 203 | 203 |

All **100** unique requests returned `202 accepted` with distinct record IDs;
all 100 rows survived reopening. The duplicate returned `202 already_accepted`
with the original record ID (request 2.968 ms, storage 0.475 ms), without an
additional row. The forced failed write returned `503 STORAGE_UNAVAILABLE`
with a generic error message (request 2.558 ms, storage 0.221 ms); its sequence
was absent after reopening. Correlation logs and both query endpoints passed
the harness checks.

These are a single local functional baseline, not a throughput, production
network, durability-under-power-loss or comparative PQC benchmark. Machine
load, filesystem caching and instrumentation affect timings; reruns will vary.
Use the same workload and environment for any later comparison.
