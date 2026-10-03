# Gateway metrics and operations — M2-34 through M2-37

PR9 completes the application metrics portion of roadmap Phase 21 and the
request-size/lifecycle refinements in Member 2's task list. Existing baseline,
secure transport, failure injection, and PR8 health/logging behavior are reused.
Member 5's metrics contract remains authoritative for metric meanings.

## M2-34 — Metrics

`GET /metrics` exports Prometheus text from process-local registries. Counters
start at zero and reset on process restart. The application registry is locked
because HTTP attempts run in worker threads while Legacy handling and scrapes
run in the ASGI event loop. Each application instance has its own registry.

| Family | Increment/observation point |
| --- | --- |
| `gateway_measurements_received_total` | Entry to a Legacy POST, before reading/parsing its body. |
| `gateway_measurements_accepted_total` | Schema/domain validation and sequence policy pass, before normalization, injected processing faults, or Cloud delivery. |
| `gateway_measurements_rejected_total` | Body-size, syntax, schema/domain, or sequence rejection. |
| `gateway_duplicate_measurements_total` | Equal sequence rejection. |
| `gateway_out_of_order_measurements_total` | Lower sequence rejection. |
| `gateway_sequence_gaps_total` | One accepted measurement with a gap; does not count each missing sequence. |
| `gateway_cloud_requests_total` | Each baseline or secure measurement HTTP attempt, including an injected timeout/unavailability before network I/O. |
| `gateway_cloud_failures_total` | Each attempt without valid Cloud acceptance, including invalid responses and session-error responses. |
| `gateway_cloud_retries_total` | Each ordinary retry actually entered; excludes the initial attempt and the bounded session-recovery send. |
| `gateway_cloud_request_duration_seconds` | Summary `_sum`/`_count` for completed attempts, successful or failed, in seconds; excludes retry backoff, handshake, and encryption. |
| `gateway_injected_failures_total` | Existing shared PQC registry counts applied application and crypto faults once. |

Local acceptance does **not** prove persistence. A Cloud failure leaves the local
acceptance counter and sequence state committed. Legacy `202` still requires a
valid Cloud acceptance. Handshake/encryption failures before a measurement HTTP
attempt affect existing PQC counters, not Cloud-attempt counters. Recovery
handshakes remain in Member 3's session metrics. The fallback counter stays zero.

Production composition shares one application registry with the processor and
selected transport. Tests or custom composition that supply their own transport
can pass the same `GatewayMetrics` through `application_metrics` to `create_app`
and `SecureTransport`, or through `metrics` to `BaselineCloudClient`.

## M2-35 — Labels

New application counters and duration samples have no labels. Existing families
retain only finite label sets: service `security_mode` (`classical`, `mlkem`),
PQC `result` (`success`, `failure`), `reason` (`injected`, `transport`, `rejected`,
`cryptographic`, `unexpected`), `phase` (`first`, `steady`), and `failure_type`
(`processing_error`, `processing_delay`, `cloud_timeout`, `cloud_unavailable`,
`drop_message`, `mlkem_handshake_failure`, `corrupt_ciphertext`, `session_missing`,
`session_expired`). No identifier, timestamp, payload, or secret becomes a label.
Metric registry methods cannot add arbitrary series.

## M2-36 — Legacy body limit

The frozen limit is **16,384 bytes inclusive**. The Legacy route counts streamed
bytes before JSON parsing; it does not trust `Content-Length`. It stops reading
when the next chunk would exceed the limit and returns:

```json
{"error":{"code":"PAYLOAD_TOO_LARGE","message":"request body exceeds 16 KiB"}}
```

The HTTP status is **413 Content Too Large**, the client-error choice permitted
by M2-36. This request never reaches validation, sequence state, fault injection,
or Cloud transport. Small malformed JSON remains `400`; parsed invalid data
remains `422`. The server may already have buffered the current incoming chunk;
the application does not accumulate the remainder of an oversized stream.

## M2-37 — Shutdown

Uvicorn handles Ctrl+C/SIGINT and SIGTERM (also used by `docker stop`). It stops
accepting network requests and drains existing ASGI requests, with the existing
five-second graceful timeout. Lifespan cleanup marks the app stopped, rejects
late Legacy requests with `503 SERVICE_UNAVAILABLE`, closes the baseline HTTP
client when present, then invokes Member 3's secure cleanup (HTTP client before
session clearing). Health/readiness return 503 after shutdown.

Baseline shutdown rejects new sends, waits for any active HTTP attempt, then
closes its opener once. It does not serialize concurrent delivery attempts.
Individual network timeouts still apply; arbitrary blocked external I/O cannot
be guaranteed to finish within the ASGI drain deadline. Forced termination
cannot guarantee delivery or cleanup. Session-memory limitations remain in
[secure shutdown](secure-shutdown.md). No retry, session, or cryptographic policy
is changed by PR9.

## Verification

```bash
uv run pytest edge_gateway/tests/test_gateway_application_metrics.py \
  edge_gateway/tests/test_gateway_request_size.py \
  edge_gateway/tests/test_gateway_shutdown.py \
  edge_gateway/tests/test_baseline_client.py \
  edge_gateway/tests/test_secure_transport.py \
  edge_gateway/tests/test_secure_shutdown.py
```

These cover local acceptance versus persistence, sequence outcomes, successful
and failed HTTP attempts, retry versus recovery, metric isolation/concurrency,
bounded series, exact-limit and chunked bodies, cleanup ordering, and real
SIGINT/SIGTERM processes in both security modes. Full repository checks and
human review remain required. Service Dockerfile/Compose integration belongs
to M2-49/M2-50 and Member 5; PR9 can verify Docker stop using the existing
Gateway verification image with the updated source mounted.
