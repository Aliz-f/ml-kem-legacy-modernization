# Cloud PR14–PR16 integration and operations review

This is a Cloud-local implementation and review companion to the frozen
[shared protocol](../../docs/architecture/04%20-%20Shared%20Cross-Component%20Protocol%20Specification.md)
and [Cloud design](../../docs/architecture/03%20-%20Cloud%20Service.md). The
frozen documents remain authoritative.

## Protocol and service boundary

In classical mode, the Gateway sends the seven-field CanonicalMeasurement to
`POST /api/v1/baseline/measurements`; `request_id` travels only as
`X-Request-ID`. In `mlkem` mode, Cloud publishes the versioned ML-KEM-768 public
key, decapsulates a session request, derives one 32-byte key with
HKDF-SHA-256 (`salt=None`,
`info=b"ml-kem-project:v1:gateway-cloud-session"`), and authenticates a
six-field SecureEnvelope with AES-256-GCM. The 12-byte nonce and ciphertext
are Base64URL. AAD is compact, sorted-key UTF-8 JSON with exactly
`protocol_version`, `gateway_id`, `session_id`, and `request_id`. Cloud validates
session lookup, ownership, then expiry. Unknown and expired sessions return
`409 SESSION_INVALID` and `409 SESSION_EXPIRED`; a Gateway recovery makes one
replacement session and rebuilds the envelope under its key, retaining the
logical request ID. Ordinary ambiguous HTTP retry resends the exact already
built envelope. No plaintext downgrade is allowed.

The canonical `received_at` becomes `gateway_received_at` in SQLite; Cloud adds
`cloud_received_at` and `record_id`. The unique `(device_id, sequence_number)`
constraint returns `already_accepted` for duplicate logical measurements.
This business idempotency is **not** cryptographic replay protection: protocol
v1 has no dedicated anti-replay counter/window. `GET /api/v1/measurements` and
`GET /api/v1/measurements/{record_id}` expose bounded queries.

ML-KEM public keys are unauthenticated by protocol v1, so their origin is a
deployment trust assumption. Cloud keeps its private key, shared secrets, and
session keys in memory; a Cloud restart changes the key identity and invalidates
sessions. Valid-length modified ML-KEM ciphertext need not raise at
decapsulation because the maintained implementation may use implicit rejection;
subsequent authenticated communication detects key mismatch. Logs, metrics,
responses, and SQLite contain no key material. Cloud's `/health` reports
process liveness; `/ready` checks initialized storage and, in `mlkem` mode,
key/session state and KDF/AEAD usability without requiring an active session.
`/metrics` uses bounded labels. Failure injection remains off by default and
reports applied, rather than merely selected, faults.

## Deployment and verification

Build from the repository root with
`docker build -f cloud_service/Dockerfile -t course-cloud .`. The image uses
Python 3.12, the frozen `uv.lock`, port 9000, SIGTERM, a non-root process, and
`/ready` as its health check. Its default
`DATABASE_URL=sqlite:////data/cloud.db` points to `/data/cloud.db`. For a
development/demo restart, attach a **named volume at `/data`**. For isolated
tests, use a fresh temporary volume or `DATABASE_URL=sqlite:///:memory:`.
The database schema holds measurements only, so a volume does not persist
ML-KEM private keys or sessions. Member 5 owns Compose wiring; the current
`docker-compose.yml` declares `cloud-service` and `edge-gateway` and their
named Cloud data volume. CI builds the Cloud image from the clean
repository context, starts it with `SECURITY_MODE=mlkem`, and verifies both
`/ready` and `/health`; this proves that SQLite initialization, the ML-KEM key
pair, and the KDF/AEAD dependencies are usable in the image. Local
Cloud startup, readiness, SQLite reopen, and empty-session-after-restart are
tested by `cloud_service/tests/test_full_path_integration.py` and existing
Cloud app/storage tests. CI also runs the full suite and an explicit Cloud plus
Gateway↔Cloud integration selection.

The secure live E2E test uses the normal `create_app` composition in
`SECURITY_MODE=mlkem`: the Gateway creates its existing session manager and
fail-closed secure transport at startup. Thus the Legacy client, Gateway HTTP
route, and Cloud secure endpoint are exercised without test-only transport
injection. M4-77 observes two retry attempts and Cloud 503 responses; the
Gateway application metrics export `gateway_cloud_retries_total`, and the
baseline and secure transport tests assert its increment. The Compose recovery
test additionally stops and restarts Cloud, then verifies Cloud readiness and
fresh Gateway delivery recovery.

## Measured local sample

These are one Windows/Python 3.12 loopback runs on 2026-10-01, not benchmarks
or mode rankings. The [mode harness](../../tests/integration/test_mode_evaluation.py)
uses the real Cloud HTTP service and Gateway dispatch (not the Legacy/Gateway
HTTP route). Four equivalent measurements per mode were sent; first secure
delivery includes key retrieval and session establishment, while the next
three reuse one session. One 409 recovery was then exercised. The separate
[Cloud baseline harness](../tools/measure_baseline.py) sends 10 canonical
measurements over loopback HTTP and times SQLite repository operations.

| Observation | Local sample |
|---|---:|
| Classical first dispatch | 53.194 ms |
| Classical steady dispatch mean (requests 2–4) | 7.761 ms |
| Secure first dispatch | 53.707 ms |
| Secure steady dispatch mean (requests 2–4) | 11.669 ms |
| First Gateway handshake | 40.446 ms |
| Gateway encapsulation | 0.322 ms |
| First Cloud decapsulation | 0.149 ms |
| Active Cloud sessions before recovery | 1 |
| Classical body / secure envelope | 192 / 455 bytes |
| Session reuse / 409 re-establishment | 3 / 1 |
| Secure-to-baseline fallback calls | 0 |
| Baseline HTTP insert median / p95 (10 samples) | 8.645 / 11.109 ms |
| Baseline SQLite save median / p95 (10 samples) | 4.880 / 8.090 ms |
| Baseline duplicate | 202 `already_accepted`, same record ID |
| Baseline storage failure | 503 `STORAGE_UNAVAILABLE`, no row |

Scheduling and startup noise make these single-run values unsuitable for a
performance ranking. Cloud's `cloud_mlkem_decapsulation_duration_seconds`
summary supplied the direct decapsulation observation. The secure integration
suite separately checks authentication failure, storage failure, and retry
behavior. Re-run the harnesses in the deployment environment before drawing
comparative conclusions.

## Threats and remaining risk

| Threat | Current control | Remaining risk |
|---|---|---|
| Malformed envelope, nonce, AAD or ciphertext | Strict fields/encoding and AES-GCM rejection before storage | No protocol-level request authentication beyond session key |
| Wrong/expired/unknown session or Gateway mismatch | Lookup → ownership → expiry, generic errors, 409 recovery | In-memory sessions vanish on restart |
| Modified ML-KEM ciphertext | Length validation, maintained ML-KEM, AEAD authentication | Valid-length implicit rejection can defer detection |
| Replayed authenticated envelope or duplicate logical request | Unique device/sequence idempotency | No cryptographic replay counter/window |
| Storage outage | Fail-closed 503, bounded Gateway transport retry | Single SQLite instance limits availability/concurrency |
| Secret leakage | Structured bounded logs, no secret persistence, synthetic-marker tests | Process memory is not guaranteed to be zeroized by Python |
| Public-key substitution / spoofed Gateway | Deployment trust of configured HTTP endpoint | No TLS/mTLS, authenticated key directory, or pinning in v1 |

Further Cloud technical debt: ephemeral key identity and simple rotation,
single instance/no HA, SQLite scaling, no HSM/KMS, and a basic query API rather
than an analytics service. Future persistent key management, distributed
sessions, PostgreSQL, authenticated transport/key pinning, and cryptographic
replay controls require a new design and protocol review, not silent v1 changes.

## Review and demo evidence

- **M4-93 PQC observability:** run the secure integration suite's
  `test_secure_envelope_round_trip_stores_canonical_measurement`, session-reuse,
  and expiry/recovery tests. Inspect `/metrics` for session creation, active
  sessions, expiry, and Gateway re-establishment. Sessions are in-memory; no
  active session is needed for `/ready`.
- **M4-94 corrupted ciphertext:**
  `test_tampered_secure_message_is_rejected` and
  `test_injected_crypto_failure_does_not_call_baseline` exercise Cloud
  authentication rejection, a decryption-failure metric, no row, and no
  baseline fallback.
- **M4-95 storage failure:**
  `test_cloud_failure_retries_the_same_secure_request_without_storage`
  selects `storage_failure`, checks Cloud authentication, two 503 responses,
  byte-identical retry bodies, and no row.
- **M4-96 Member 3 crypto interface review:** the live secure suite checks
  ML-KEM-768 metadata/decapsulation, identical Gateway/Cloud HKDF output,
  four-field AAD, 12-byte nonce, exact envelope fields, bounded 409 recovery,
  byte-identical ordinary retry, fail-closed behavior, and implicit-rejection
assumptions. No protocol mismatch was observed in these checks. The Gateway
executable composes its fail-closed secure transport, and ordinary retry metrics
are exported by `gateway_cloud_retries_total`.
- **M4-97 Member 2 baseline contract review:**
  `test_shared_canonical_fixture_is_accepted_and_preserves_the_baseline_contract`
  checks shared field names, timestamp forms, header-only request ID,
  Gateway ID, `received_at` mapping, and idempotency without importing Gateway
  application models. The new live three-component test additionally exercises
  the actual Legacy and Gateway HTTP boundary.
- **M4-98 Member 5 deployment review:** Cloud's port, DB URL, named-volume
  target, environment, and readiness are specified above. CI and the Compose
  regressions verify the current Docker runtime behavior; Member 5 retains
  deployment ownership.
- **M4-99 dependency review:** Cloud directly uses FastAPI, Uvicorn,
  `cryptography` (HKDF/AES-GCM), and the maintained ML-KEM library through
  `cloud_service.crypto.mlkem`; SQLite and metrics use the standard library.
  No broker, distributed store, or heavy ORM is introduced.

The human reviewer must complete the M4-86 checklist in the task document;
AI checks are evidence, not human acceptance. Existing actual history shows
**Modified → Accepted** for task 0072 (random failure selection and session
ordering/logging revisions) and task 0104 (scope and security-test revision).
No **Rejected** human decision was found in those reviewed records; the
architecture's rejected *proposals* (plaintext fallback, persisted session
keys, a v1 replay counter) must not be misrepresented as human review events.
