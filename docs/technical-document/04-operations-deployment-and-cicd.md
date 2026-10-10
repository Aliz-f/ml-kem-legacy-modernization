# Chapter 4 — Operations, Deployment and CI/CD

## 4.1 Operational design goals

The operational work makes the three-service telemetry path reproducible and
inspectable:

```text
Legacy Device  →  Edge Gateway  →  Cloud Service  →  SQLite volume
```

The core goals are deterministic local deployment, explicit security-mode
selection, liveness/readiness visibility, safe correlation, bounded metrics,
controlled fault injection, and automated regression gates.  The system uses
Python 3.12 and the root `uv` workspace with its committed `uv.lock`; it does
not add a separate `requirements.txt` dependency path.

The deployment is intentionally a single-host course test environment.  It is
not a claim of high availability, distributed storage, durable Gateway
buffering, or production transport identity.  These limits are recorded in the
technical-debt and risk registers rather than being hidden by the operational
documentation.

## 4.2 Docker Compose topology and lifecycle

`docker-compose.yml` (Appendix A.1) is the reproducible system
topology.  It builds the three application images from their service
Dockerfiles, connects them through Compose DNS, exposes only the Gateway and
Cloud application ports on loopback, and persists accepted Cloud measurements
in the named `cloud-data` volume.

```text
┌────────────────┐      http://edge-gateway:8000       ┌────────────────┐
│ legacy-device  │ ─────────────────────────────────►  │  edge-gateway  │
│ no inbound port│                                     │  loopback:8000 │
└────────────────┘                                     └───────┬────────┘
                                                               │
                                    http://cloud-service:9000  │
                                                               ▼
                                                         ┌────────────────┐
                                                         │ cloud-service  │
                                                         │ loopback:9000  │
                                                         └───────┬────────┘
                                                                 │
                                                          cloud-data volume

                           ┌──────────────────────────────────────────────┐
                           │ dashboard (local, loopback:8080, optional UI)│
                           └──────────────────────────────────────────────┘
```

The dashboard is a local operational aid, not a data-path component.  It can
display service/metric status and apply restricted temporary overrides for a
selected container.  Because it needs local Docker control, it mounts the
Docker socket and is therefore deliberately bound to `127.0.0.1`, carries no
remote exposure or credentials, and is appropriate only for a trusted local
demonstration environment.

Compose starts the Cloud first, waits for its health check before starting the
Gateway, then waits for Gateway health before starting the Legacy Device.  The
Cloud's SQLite path defaults to `sqlite:////data/cloud.db` in the named volume.
Internal service URLs are `http://edge-gateway:8000` and
`http://cloud-service:9000`; host-port overrides are available for local port
conflicts.

The documented start sequence is:

```bash
docker compose config --quiet
docker compose build

# Baseline comparison run
SECURITY_MODE=classical docker compose up --build --wait

# Modernized run (after stopping the preceding stack)
docker compose down
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait
```

The security-mode change is explicit.  Modernized Mode retains the frozen
`PQC_FAILURE_POLICY=fail_closed` value; it never responds to a handshake or
secure-delivery problem by forwarding the measurement through the baseline
endpoint.  Service-specific root environment variables (`LEGACY_FAILURE_*`,
`GATEWAY_FAILURE_*`, and `CLOUD_FAILURE_*`) map to each process's local failure
configuration, allowing controlled tests without sending failure-control data
over the network.

`docker compose down` stops the stack while retaining the demonstration
database.  `docker compose down --volumes --remove-orphans` is the documented
clean reset and permanently deletes the locally stored measurements in
`cloud-data`; it is used before deterministic demonstrations and automated
assertions.  The volume contains accepted business records only—private keys,
shared secrets, session keys, and session state remain process-local.

## 4.3 Health and readiness contracts

Gateway and Cloud each expose `GET /health` and `GET /ready`; Compose health
checks call the health endpoints from inside the respective containers.  A
normal health result is `{ "status": "ok" }`.  Readiness adds meaningful
dependencies rather than merely reporting process existence:

| Service and mode | Readiness condition | Example successful response |
| --- | --- | --- |
| Gateway | Process is running and its configured dispatch is available. | `{ "status": "ready", "security_mode": "mlkem" }` |
| Cloud, classical | Process is running and SQLite is initialized/writable. | `{ "status": "ready", "storage": "ok" }` |
| Cloud, ML-KEM | Cloud storage is writable and key/session/crypto dependencies are initialized. | `{ "status": "ready", "storage": "ok", "mlkem": "available" }` |

An active secure session is intentionally **not** a readiness dependency on
either service.  Sessions are created lazily on the first secure delivery, so
a zero active-session count is healthy before traffic.  Conversely, the
absence of a usable cryptographic subsystem in Modernized Mode makes the Cloud
unready.  The Legacy Device has no inbound health/readiness API; its operational
state is represented through its process/container status and logs rather than
by inventing an endpoint.

The standard post-start operational check queries both services:

```bash
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/health
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/ready
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/health
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/ready
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/api/v1/measurements
```

## 4.4 Structured logging, correlation, and secret safety

The project adopts compact structured-text events: stable, lowercase
`event=...` names followed by bounded `key=value` fields.  The common
correlation vocabulary is `event`, `component`, `request_id`, `gateway_id`,
`device_id`, and `sequence_number`; `session_id`, `key_id`, and `record_id`
may be included when relevant.  A typical trace follows the same request ID
from Gateway receipt through Cloud persistence:

```text
Gateway: event=legacy_measurement_received request_id=req-123 device_id=sensor-001
Gateway: event=cloud_delivery_started request_id=req-123 session_id=sess-55
Cloud:   event=secure_measurement_received request_id=req-123 gateway_id=gateway-001
Cloud:   event=measurement_stored request_id=req-123 record_id=rec-900
```

The logging standard prohibits raw request/response bodies, arbitrary headers,
unbounded exception text, configuration values, and sensitive cryptographic
buffers.  Specifically, ML-KEM private/public key material, encapsulation
ciphertext, shared secrets, AES-GCM keys/nonces/ciphertexts/tags/plaintext,
passwords, tokens, credentials, and `.env` contents must not be logged.

The secret-logging review combines source inspection with automated tests.  It
includes Gateway tests for the absence of generated shared secrets and session
keys, Cloud tests covering key/AEAD/error paths, and a live secure
end-to-end observability regression that checks captured Gateway/Cloud logs
for absence of the actual session secret and derived key.  This is evidence of
the current reviewed paths, not a claim that future changes will be safe
without review; logging and error changes remain security-review work.

## 4.5 Metrics and local monitoring

Gateway and Cloud expose Prometheus-style plaintext metrics at `GET /metrics`.
Their metric families are intentionally bounded: correlation identifiers such
as `request_id` and `session_id` never become labels.  The metric contract
covers normal flow, failures, session state, and controlled test conditions.
Counters end in `_total`, duration families end in `_duration_seconds`, and
active-session values are gauges.  They are defined to answer an operational
question, rather than merely to count implementation details.

### 4.5.1 Gateway metric inventory

| Metric | Type | Why it is defined |
| --- | --- | --- |
| `gateway_measurements_received_total` | Counter | Establishes incoming Legacy-device workload and is the denominator for Gateway acceptance/rejection analysis. |
| `gateway_measurements_accepted_total` | Counter | Shows how many validated measurements entered the accepted delivery path. |
| `gateway_measurements_rejected_total` | Counter | Detects malformed, invalid, or sequence-policy-rejected Legacy traffic. |
| `gateway_duplicate_measurements_total` | Counter | Separates equal-sequence rejections from general validation failure, aiding device/retry diagnosis. |
| `gateway_out_of_order_measurements_total` | Counter | Identifies lower sequence values, which can indicate device restart, delayed delivery, or ordering problems. |
| `gateway_sequence_gaps_total` | Counter | Reveals accepted jumps in a device sequence without treating a gap as a false rejection. |
| `gateway_cloud_requests_total` | Counter | Counts each Gateway-to-Cloud attempt and supports comparison with accepted input and Cloud outcomes. |
| `gateway_cloud_failures_total` | Counter | Makes downstream availability/delivery problems visible. |
| `gateway_cloud_retries_total` | Counter | Shows whether bounded ordinary retries are occurring and helps detect retry amplification. |
| `gateway_cloud_request_duration_seconds` | Duration | Measures Cloud-delivery latency, including its contribution to end-to-end processing time. |
| `gateway_mlkem_handshakes_total` | Counter | Counts ML-KEM session-establishment attempts/outcomes, providing the volume for secure-mode reliability analysis. |
| `gateway_mlkem_handshake_failures_total` | Counter | Detects failed key/session establishment independently from message-encryption failures. |
| `gateway_mlkem_handshake_duration_seconds` | Duration | Isolates first-message session-establishment cost from steady-state message delivery cost. |
| `gateway_session_reestablishments_total` | Counter | Shows bounded recovery attempts after `SESSION_INVALID` or `SESSION_EXPIRED`; unexpected growth indicates session churn. |
| `gateway_encryption_failures_total` | Counter | Detects inability to build a secure envelope before transmission. |
| `gateway_active_session` | Gauge | Indicates whether the Gateway currently has one usable in-memory secure session; it is not a readiness requirement. |
| `gateway_pqc_fallback_total` | Counter/invariant | Must remain `0`: any non-zero value would expose an impermissible runtime plaintext downgrade in protocol v1. |
| `gateway_injected_failures_total` | Counter | Distinguishes intentionally simulated test failures from an unexplained operational fault. |

### 4.5.2 Cloud metric inventory

| Metric | Type | Why it is defined |
| --- | --- | --- |
| `cloud_baseline_requests_total` | Counter | Provides the baseline-mode request volume for controlled comparison with secure mode. |
| `cloud_secure_requests_total` | Counter | Counts secure-envelope traffic reaching the Cloud boundary. |
| `cloud_secure_requests_rejected_total` | Counter | Makes secure messages rejected before acceptance/storage visible without exposing their content. |
| `cloud_request_duration_seconds` | Duration | Measures Cloud-side request-processing time and helps separate Cloud cost from Gateway delivery timing. |
| `cloud_mlkem_sessions_created_total` | Counter | Shows successful creation of Cloud-side secure sessions. |
| `cloud_mlkem_session_failures_total` | Counter | Detects failed session establishment on the receiving/decapsulation side. |
| `cloud_mlkem_decapsulation_duration_seconds` | Duration | Measures the Cloud's ML-KEM decapsulation contribution to handshake overhead. |
| `cloud_active_sessions` | Gauge | Shows the number of live process-local sessions, helping explain recovery or restart behavior. |
| `cloud_expired_sessions_total` | Counter | Identifies expiry/cleanup activity and provides context for session-recovery events. |
| `cloud_authenticated_messages_total` | Counter | Counts envelopes that passed AES-GCM authentication and decryption. |
| `cloud_decryption_failures_total` | Counter | Detects authentication/decryption rejection, including tampering or mismatched session/key material. |
| `cloud_measurements_stored_total` | Counter | Counts newly persisted logical measurements. |
| `cloud_storage_failures_total` | Counter | Makes SQLite/storage availability failures visible to operators and tests. |
| `cloud_duplicate_measurements_total` | Counter | Shows idempotent retransmissions that returned an existing logical record instead of producing a second row. |
| `cloud_injected_failures_total` | Counter | Marks deliberate Cloud fault scenarios so their effects are interpretable during tests. |

Metrics can have only finite, low-cardinality labels such as `result`,
`failure_type`, `security_mode`, or `phase`.  Labels must not contain device,
request, session, key, or record IDs; timestamps; payload values; nonces;
ciphertexts; or secrets.  Correlation belongs in logs, not in a time-series
label set.  Together, these metrics answer whether traffic is accepted,
rejected, retried, encrypted, authenticated, stored, or intentionally failed;
they support, but do not replace, the test and empirical evidence in Chapter 5.

The local dashboard consumes this bounded operational information and makes the
service status visible during a demonstration.  It explicitly reports the
Legacy Device's lack of HTTP health/readiness rather than presenting a false
probe result.  Browser actions that apply a permitted temporary override show a
confirmation and recreate only the selected service; a normal Compose recreate
restores the committed Compose/`.env` configuration.

## 4.6 Continuous integration and delivery gates

The committed GitHub Actions workflow `.github/workflows/ai-history.yml` (Appendix B.1)
runs on pushes and pull requests.  It uses Python 3.12, installs the root workspace with
`uv sync --frozen`, and separates fast quality feedback from integration,
secure end-to-end, container-build, and clean-environment evidence.  Each job
uses a fresh Ubuntu runner; therefore no test depends on a prior job's local
virtual environment, containers, database, or cached service process.

```text
quality ────────────────┐
unit-tests ─────────────┼──► secure-e2e ──┐
integration-tests ──────┘                 ├──► clean-environment
quality ───────────────────► docker-build ─┘
```

| CI job | Commands and coverage | Why the gate exists |
| --- | --- | --- |
| `quality` | `uv sync --frozen`, `uv run ruff check .`, then `ai-history --help`, `status`, `list`, and `check`. | Rejects style/static defects and ensures the locked dependency graph and AI-governance CLI work in a clean runner. |
| `unit-tests` | Component/repository tests, targeted protocol-model and session/envelope/AAD/KDF contract tests, Gateway crypto/transport/trust/logging checks, and tamper regression. | Proves local behavior and frozen protocol encodings before exercising service composition. |
| `integration-tests` | Entire `tests/integration` suite, targeted observability/metric sanity tests, Cloud checks, and Legacy–Gateway, baseline, ML-KEM-session, and secure-path tests. | Detects mismatches between independently owned components, including failure classification and cross-service metric behavior. |
| `secure-e2e` | Runs only after `quality`, `unit-tests`, and `integration-tests`; executes classical E2E, ML-KEM E2E, and legacy-compatibility regression tests. | Demonstrates that both explicit modes still work across the complete Legacy-to-Cloud path after earlier gates pass. |
| `docker-build` | Runs after `quality` and builds the Legacy Device, Gateway, and Cloud images from their committed Dockerfiles. | Catches container-build/dependency issues that Python-only tests cannot reveal. |
| `clean-environment` | Runs after both `secure-e2e` and `docker-build`; reinstalls with `uv sync --frozen`, validates resolved Compose configuration, and runs the Compose recovery regression. | Rechecks reproducibility from the committed lockfile and validates the deployed three-service recovery path without relying on a developer workstation. |

The workflow's dependency graph is intentional.  `secure-e2e` cannot start
until static quality, component/protocol behavior, and cross-service behavior
have passed.  `clean-environment` cannot start until both end-to-end evidence
and image builds pass, so the Compose recovery check is the final automated
gate.  Failing jobs stop dependent stages, giving fast diagnosis at the lowest
useful layer rather than obscuring a unit defect behind an E2E failure.

This is a CI validation pipeline, not continuous deployment (CD) to a public
or production environment.  It does not push images, alter remote
infrastructure, create a release, or deploy secrets.  The delivery-related
evidence is instead reproducible image construction and the locally documented
Compose test deployment.  The locked install and clean-environment stage
protect against a cached developer environment hiding an unavailable or
unlocked dependency.  AI-history validation is a separate governance gate: it
checks that recorded history is structurally valid, but never substitutes for
the required human review and final verification.

## 4.7 Operational boundaries and handover procedure

The root runbook defines the normal operator sequence: validate Compose,
choose mode explicitly, start with `--wait`, check health/readiness/metrics and
the Cloud query API, inspect secret-safe operational logs, then stop or reset
the environment.  The recommended repository validation set before review is:

```bash
uv sync --frozen
uv run ruff check .
uv run pytest
uv run ai-history check
```

During Modernized Mode, a `409 SESSION_INVALID` or `409 SESSION_EXPIRED`
causes at most one secure recovery: a replacement session is established and
the logical request ID is preserved.  An ordinary ambiguous-response retry,
by contrast, resends the identical already-built `SecureEnvelope`.  Operators
must not mistake the idempotent database row guarantee for cryptographic replay
protection: protocol version 1 has no replay counter/window.

The remaining operational limitations are explicit: HTTP-only controlled
transport, ephemeral Cloud key/session state, in-memory Gateway sequence state,
single-instance SQLite, simple bounded retry behavior, and no persistent
Gateway queue.  These constraints are adequate for reproducible course
demonstration and testing; Chapter 7 evaluates their associated debt and risks.
