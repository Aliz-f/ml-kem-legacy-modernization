# Baseline Gateway measurements (M2-18)

This is a local sample for later comparison, collected through the production
Legacy serializer/client, live Gateway HTTP route, production baseline client,
live Cloud HTTP route, and temporary file-backed SQLite. It complements M2-16/17
correctness evidence and the Cloud-local measurement harness. No service runtime
instrumentation or protocol changes are introduced.

## Reproduce

From the workspace root with the locked development environment installed:

```bash
uv run pytest edge_gateway/tests/test_gateway_baseline_integration.py -k baseline_gateway_measurements -q -s
```

The test prints two `M2-18` JSON reports and checks counts, statuses, real HTTP
attempts, exact retry body/header equality, and persisted row counts after
shutdown. It checks healthy stored sequence numbers and sensor values. Timing
values are observations, never pass/fail thresholds. Loopback socket access is
required. Databases are disposable pytest artifacts, not repository evidence.

The healthy workload sends 100 sequential measurements from `sensor-test`,
sequence 1–100, temperature 22.5 °C, humidity 44.0 %, and timestamp
`2026-09-21T12:00:00Z`. Gateway ID is `gateway-baseline`; Gateway receipt times
and correlation IDs are generated normally. Four subsequent controls send
malformed JSON (`400`), invalid humidity (`422`), duplicate sequence (`409`),
and out-of-order sequence (`409`). None reaches Cloud.

The separate failure scenario uses fresh service instances and SQLite storage,
sets SQLite `PRAGMA query_only = ON`, and sends one valid measurement. The real
baseline client makes three attempts with its normal one- and two-second
backoffs, then Gateway returns `503`. No row persists. This scenario does not
contribute to healthy latency statistics.

Both scenarios explicitly select `SECURITY_MODE=classical`. Configured failure
injection remains disabled (`FAILURE_MODE=none`); SQLite write rejection is a
test-only control. Gateway Cloud timeout is 5 seconds, maximum retries 2. Legacy
request timeout is 10 seconds with zero retries. Requests are sequential, with
no warmup or concurrent load. Services run in threads on one machine using
loopback HTTP; health and readiness probes are excluded from samples.

## Measurement boundaries

| JSON field | Meaning |
| --- | --- |
| `legacy_requests` | POSTs observed at the Gateway measurement route |
| `accepted` | Gateway `202`, after Cloud acceptance |
| `rejected` | Gateway `4xx` validation/sequence rejections |
| `failed` | Gateway `5xx` delivery/application failures, separate from rejections |
| `gateway_request_ms` | Middleware entry until route response is available, including downstream delivery, across all measured POSTs |
| `gateway_accepted_request_ms` | Same boundary for the 100 successful requests only; null in failure scenario |
| `cloud_delivery_ms` | Production `BaselineCloudClient.send`, including serialization, thread scheduling, HTTP attempts, response parsing, and retry backoff |
| `cloud_attempt_ms` | Each production `_post` call, including HTTP and response parsing; excludes backoff |
| `cloud_retries` | Actual `_post` calls minus logical `send` calls |
| `canonical_payload_bytes_per_attempt` | Actual serialized body length passed to `_post`, checked against bytes received by Cloud; excludes HTTP headers |
| `persisted_rows` | Row count verified via query API and fresh SQLite connection after shutdown |

Durations use `perf_counter`. Distributions contain count, minimum, mean, and
maximum. Gateway timing includes parsing, validation, sequencing, normalization,
and Cloud delivery, but excludes the Legacy client's network round trip and
final response transmission. It is not isolated Gateway CPU time. Test-only
middleware and a delegating baseline-client subclass add measurement overhead;
Cloud capture middleware also adds overhead. Retries are measured at the actual
attempt boundary, not inferred from response status alone.

## Recorded local sample

Collected on 2026-10-02 after synchronizing develop at merge `fc87e2e`, using the
M2-18 working-tree collector. Environment: macOS (`Darwin`), ARM64, Python
3.12.14, SQLite 3.53.1, repository locked dependencies, local disk. The full
baseline integration module passed all 9 tests in 6.67 seconds during this run.

| Measurement | Healthy + rejection controls | Storage failure |
| --- | ---: | ---: |
| Legacy requests | 104 | 1 |
| Accepted / rejected / failed | 100 / 4 / 0 | 0 / 0 / 1 |
| Persisted rows | 100 | 0 |
| Cloud attempts / retries | 100 / 0 | 3 / 2 |
| Gateway request mean | 2.136 ms (104 requests) | 3026.317 ms |
| Gateway accepted request mean | 2.212 ms (100 requests) | N/A |
| Cloud delivery mean | 1.905 ms | 3025.431 ms |
| Cloud attempt mean | 1.813 ms | 4.952 ms |
| Canonical payload min / mean / max | 201 / 201.92 / 203 bytes | 201 / 201 / 201 bytes |

Payload sizes vary with sequence-number width. These are small local samples,
not a capacity estimate or deployment benchmark. First-use overhead is included.
Repeat equivalent workloads and timing boundaries before comparing modes, and
report the modernized first-message handshake separately. The earlier
`mode-evaluation.md` sample measures dispatch directly and is not numerically
comparable to this Gateway-route measurement. Member 5 still owns shared
benchmark orchestration, baseline freezing, and container deployment evidence.
