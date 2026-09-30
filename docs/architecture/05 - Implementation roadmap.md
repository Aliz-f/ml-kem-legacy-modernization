# 1. Overall implementation strategy

Do **not** start by having three people independently implement all three components immediately.

The safest development order is:

```text
Architecture frozen
      ↓
Protocol contracts frozen
      ↓
Shared project infrastructure
      ↓
Legacy baseline
      ↓
Gateway baseline
      ↓
Cloud baseline
      ↓
Baseline E2E works
      ↓
ML-KEM primitives
      ↓
Secure session protocol
      ↓
Secure E2E works
      ↓
Failure injection
      ↓
Observability
      ↓
Deployment
      ↓
CI/CD
      ↓
Evaluation
      ↓
Documentation
```

The most important rule is:

> **First make the system work without PQC. Then modernize the Gateway–Cloud path.**

That gives you an actual baseline to compare against rather than trying to build everything simultaneously.

---

# 2. Proposed team split

Since your group has five members, I recommend assigning **primary ownership**, but not exclusive ownership.

| Member   | Primary area                     | Secondary area                | People  |
| -------- | -------------------------------- | ----------------------------- | ------- |
| Member 1 | Legacy Device                    | Legacy↔Gateway integration    | Roope   |
| Member 2 | Edge Gateway legacy/API side     | Validation, sequence tracking | Dorsa   |
| Member 3 | Gateway security side            | ML-KEM, sessions, encryption  | Armin   |
| Member 4 | Cloud Service                    | Storage, Cloud crypto         | Masoud  |
| Member 5 | DevOps / Testing / Observability | CI/CD, Docker, E2E, metrics   | Alireza |

This avoids a common problem:

```text
Person A owns Legacy
Person B owns Gateway
Person C owns Cloud

→ nobody owns integration
```

Member 5 becomes the main integration/operations owner, while all PRs still receive peer review.

---

# 3. Dependency graph

The real project dependencies look like this:

```text
                         ┌──────────────────────┐
                         │ Architecture +       │
                         │ Protocol Spec        │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
       Legacy Device         Gateway Skeleton      Cloud Skeleton
               │                    │                    │
               └───────────┐        │        ┌───────────┘
                           ▼        ▼        ▼
                       Baseline Integration
                               │
                               ▼
                        Baseline E2E
                               │
                      ┌────────┴────────┐
                      │                 │
                      ▼                 ▼
                ML-KEM Wrapper     Cloud ML-KEM
                      │                 │
                      └────────┬────────┘
                               ▼
                        Session Protocol
                               │
                               ▼
                      Symmetric Protection
                               │
                               ▼
                       Secure E2E System
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
      Failure Injection    Observability      Security Tests
             │                 │                  │
             └─────────────────┼──────────────────┘
                               ▼
                        Docker Deployment
                               │
                               ▼
                             CI/CD
                               │
                               ▼
                          Evaluation
```

---

# 4. Phase 0 — Freeze architecture

Before coding application logic, commit the design documents.

Target files:

```text
docs/
└── architecture/
    ├── system-overview.md
    ├── legacy-device.md
    ├── edge-gateway.md
    ├── cloud-service.md
    └── protocol-specification.md
```

The documents should contain the designs we created.

The most important one is:

```text
protocol-specification.md
```

because it defines the contract between independently developed components.

### Acceptance gate

Phase 0 is complete when the team agrees on:

```text
Legacy payload
Gateway endpoint
Canonical model

Baseline Cloud endpoint

ML-KEM flow
Session flow
SecureEnvelope

Error semantics
Retry semantics

Failure-injection approach
```

No implementation should silently change these afterward.

---

# 5. Phase 1 — Repository infrastructure

This work can happen immediately.

The repository should already roughly have:

```text
ml-kem-legacy-modernization/
│
├── legacy_system/
├── edge_gateway/
├── cloud_service/
│
├── tests/
│   └── integration/
│
├── docs/
│   ├── architecture/
│   └── ai/
│
├── .github/
│   └── workflows/
│
├── AGENTS.md
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
└── docker-compose.yml
```

Member 5 can own this phase.

Important items:

```text
uv workspace
Python version
ruff
pytest
AI-history CLI
.gitignore
.env.example
basic CI
```

Do not add application dependencies globally unless needed.

### Verification

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ai-history check
```

All should work before application development becomes large.

---

# 6. Phase 2 — Legacy Device implementation


Owner:

```text
Member 1
```

This component has almost no dependency on the others because Protocol A is already frozen.

Development tasks should be separate AI-history tasks.

### Task L1 — Configuration

Implement:

```text
DEVICE_ID
GATEWAY_URL
SEND_INTERVAL_SECONDS
REQUEST_TIMEOUT_SECONDS
MAX_RETRIES

FAILURE_MODE
FAILURE_RATE
FAILURE_SEED

LOG_LEVEL
```

Add startup validation.

### Task L2 — Measurement domain model

Implement the valid internal model:

```text
device_id
temperature_c
humidity_pct
timestamp
sequence_number
```

This model should represent a valid measurement only.

### Task L3 — Sensor generator

Implement valid generation.

Tests:

```text
temperature generation
humidity generation
timestamp
sequence increments
deterministic random source
```

### Task L4 — Serialization / outgoing payload boundary

Convert the valid domain model into a wire payload before fault injection:

```text
Measurement
    ↓
serialize
    ↓
LegacyPayload / dict
```

This is important because failure injection must be able to create payloads that are intentionally invalid, such as:

```text
missing timestamp
malformed timestamp
invalid humidity
```

without corrupting the validated domain object.

### Task L5 — Failure injector

Apply faults to the **serialized outgoing payload**, not to the validated `Measurement` object.

Implement:

```text
none
invalid_temperature
invalid_humidity
missing_field
invalid_timestamp
duplicate_sequence
out_of_order_sequence
random
```

Pipeline:

```text
Sensor
  ↓
Valid Measurement
  ↓
Serialize
  ↓
Failure Injector
  ↓
Outgoing payload
  ↓
Gateway Client
```

### Task L6 — Gateway client

Implement:

```text
POST /api/v1/measurements
```

with:

```text
timeout
bounded retry
500/502/503/504 retry
network/timeout retry
400/409/422 no retry
```

### Task L7 — Main device loop

Implement:

```text
generate valid measurement
→ serialize
→ inject optional payload fault
→ send
→ wait
→ repeat
```

plus graceful shutdown.

### Task L8 — Docker image

Legacy Device should require no inbound port.

---

# 7. Legacy component gate

Do not call Legacy Device finished merely because:

```text
python runs
```

It should pass:

```text
unit tests
configuration tests
failure injection tests
client retry tests
shutdown test
ruff
AI-history review
```

At this stage the Gateway can still be mocked.

---

# 8. Phase 3 — Edge Gateway baseline


Owners:

```text
Member 2
with Member 3 reviewing
```

Do **not** start ML-KEM yet.

First create a functional Baseline Mode Gateway.

### Task G1 — Gateway configuration

Implement:

```text
GATEWAY_ID
CLOUD_URL

CLOUD_TIMEOUT_SECONDS
CLOUD_MAX_RETRIES

SECURITY_MODE

SESSION_TTL_SECONDS
PQC_FAILURE_POLICY

FAILURE_MODE
FAILURE_RATE
FAILURE_SEED

LOG_LEVEL
```

Initially:

```text
SECURITY_MODE=classical
PQC_FAILURE_POLICY=fail_closed
```

For protocol version `1`, `fail_closed` is the only supported PQC failure policy.

### Task G2 — Gateway application/API

Implement:

```text
POST /api/v1/measurements
GET /health
GET /ready
GET /metrics
```

### Task G3 — Legacy measurement validation

Require exactly the five documented Legacy fields; reject additional fields.
The request model supplies schema rejection; the later HTTP validation layer
maps parsed-object schema errors to `422`.

Validate:

```text
device_id
temperature
humidity
timestamp
sequence
```

Freeze the HTTP validation boundary:

```text
malformed or unparseable JSON/body syntax
→ 400 Bad Request

JSON parses, but a required field is missing, has the wrong type,
or violates a domain rule
→ 422 Unprocessable Entity
```

Therefore the Legacy `missing_field` failure scenario expects `422`.

### Task G4 — Canonical normalization

Convert:

```text
timestamp
```

to:

```text
measured_at
```

and add:

```text
received_at
gateway_id
```

The canonical model does **not** contain `request_id`.

Create `request_id` separately as request/transport context after the measurement is accepted.

### Task G5 — Sequence tracker

Track per device:

```text
duplicate
out-of-order
gap
```

Frozen policy:

```text
duplicate      → 409
out-of-order   → 409
gap            → accept + log/metric
```

The sequence tracker records the **last valid sequence observed by the Gateway**, even if later Cloud delivery fails.

### Task G6 — Request/correlation ID

Create a unique:

```text
request_id
```

for every accepted Legacy request.

Baseline propagation:

```text
X-Request-ID
```

Secure propagation later:

```text
SecureEnvelope.request_id
+
AAD
```

### Task G7 — Baseline Cloud client

Implement:

```http
POST /api/v1/baseline/measurements
X-Request-ID: req-...
```

with bounded retry policy.

No ML-KEM yet.

---

# 9. Phase 4 — Cloud baseline


Owner:

```text
Member 4
```

Again, do not start with ML-KEM.

### Task C1 — Cloud configuration

Implement:

```text
CLOUD_ID
DATABASE_URL
SECURITY_MODE=classical
SESSION_TTL_SECONDS

FAILURE_MODE
FAILURE_RATE
FAILURE_SEED

LOG_LEVEL
```

### Task C2 — Cloud application

Implement:

```text
GET /health
GET /ready
GET /metrics

POST /api/v1/baseline/measurements
```

### Task C3 — Canonical validation

Cloud validates the Gateway canonical model again.

### Task C4 — SQLite storage

Implement:

```text
measurements table
```

with:

```text
record_id
device_id
gateway_id
temperature_c
humidity_pct
measured_at
gateway_received_at
cloud_received_at
sequence_number
```

The canonical field:

```text
received_at
```

maps to stored:

```text
gateway_received_at
```

### Task C5 — Repository abstraction

Something simple like:

```text
save()
get()
list()
```

### Task C6 — Idempotency

Protect:

```text
(device_id, sequence_number)
```

from duplicate insertion.

### Task C7 — Query API

Implement:

```text
GET /api/v1/measurements
GET /api/v1/measurements/{record_id}
```

### Task C8 — Baseline correlation

Read:

```http
X-Request-ID
```

from baseline Gateway requests and use it in logs/tracing.

It is not stored as part of the canonical measurement model.

---

# 10. Phase 5 — First integration milestone

Now combine:

```text
Legacy Device
    ↓
Edge Gateway
    ↓
Cloud
```

but without ML-KEM.

This milestone is extremely important.

The target:

```text
Legacy generates:
21.7°C
42.5%

↓ Gateway

Gateway validates
normalizes
forwards

↓ Cloud

Cloud validates
stores

↓ Query

21.7°C
42.5%
```

The values must survive end-to-end unchanged.

---

# 11. Baseline E2E acceptance test


Create a deterministic valid Legacy measurement:

```json
{
  "device_id": "sensor-test",
  "temperature_c": 22.5,
  "humidity_pct": 44.0,
  "timestamp": "2026-09-21T12:00:00Z",
  "sequence_number": 1
}
```

Then verify:

```text
Legacy sends
↓
Gateway validates
↓
Gateway records sequence state
↓
Gateway normalizes
↓
Gateway adds request_id separately
↓
Gateway sends CanonicalMeasurement to baseline Cloud endpoint
with X-Request-ID
↓
Cloud validates
↓
Cloud stores
↓
Cloud query returns
```

Expected stored values:

```text
temperature = 22.5
humidity = 44.0
sequence = 1
device_id = sensor-test

measured_at = 2026-09-21T12:00:00Z

gateway_received_at exists
cloud_received_at exists
gateway_id is correct
```

Only after this works should the team implement PQC.

---

# 12. Freeze baseline

Tag or commit the baseline clearly.

For example:

```text
baseline-classical-complete
```

Record:

```text
request latency
payload size
test count
test coverage if used
```

You need this later for comparison.

The assignment explicitly expects understanding and evaluation of the baseline before modernization.

---

# 13. Phase 6 — ML-KEM library investigation

Owners:

```text
Member 3 + Member 4
```

Do this as its own task.

Do not let an AI agent simply pick random crypto packages.

Evaluate the selected library for:

```text
ML-KEM support
parameter sets
Python compatibility
maintenance
installation
API quality
license
testability
```

Chosen target from our design:

```text
ML-KEM-768
```

But verify that the selected library supports it appropriately.

---

# 14. Phase 7 — Crypto wrapper design

Keep library-specific code isolated.

Gateway:

```text
edge_gateway/crypto/mlkem.py
```

Cloud:

```text
cloud_service/crypto/mlkem.py
```

The rest of the application should not depend directly on library APIs.

Conceptually:

```python
ciphertext, shared_secret = encapsulate(public_key)
```

and:

```python
shared_secret = decapsulate(ciphertext, private_key)
```

This makes later library changes much easier.

---

# 15. ML-KEM primitive integration test

Before HTTP sessions exist, prove the normal valid path:

```text
Cloud generates key pair

Gateway receives public key

Gateway encapsulates
→ ciphertext
→ secret A

Cloud decapsulates that valid ciphertext
→ secret B

assert A == B
```

This should be one of the strongest crypto integration tests.

Also test wrapper behavior for malformed/incorrect-length inputs where the selected library exposes such validation, but do **not** assume that every modified, correctly sized ML-KEM ciphertext must raise an explicit decapsulation exception. ML-KEM implementations may use implicit-rejection behavior and return different pseudorandom keying material instead.

Use explicit failure injection to test operational handling of a decapsulation/wrapper failure.

No network is required yet.

---

# 16. Phase 8 — KDF implementation


Owners:

```text
Member 3 + Member 4
```

Implement the same KDF semantics independently on both sides.

Frozen contract:

```text
HKDF-SHA-256

input key material:
ML-KEM shared secret

salt:
None

length:
32 bytes

info:
"ml-kem-project:v1:gateway-cloud-session"
```

Test:

```text
same ML-KEM shared secret
+
salt=None
+
same fixed info
+
same output length

→ identical session key
```

Never log the shared secret or derived key.

---

# 17. Phase 9 — Cloud ML-KEM key service


Owner:

```text
Member 4
```

Implement:

```http
GET /api/v1/crypto/public-key
```

Cloud startup:

```text
generate ML-KEM-768 key pair
→ assign key_id
→ retain private key in memory
```

Response:

```json
{
  "protocol_version": "1",
  "algorithm": "ML-KEM-768",
  "key_id": "cloud-key-001",
  "public_key": "<base64url>"
}
```

No private key leaves Cloud.

Protocol version `1` uses an ephemeral in-memory Cloud key pair; Cloud restart generates a new key pair.

---

# 18. Phase 10 — Session establishment


Owners:

```text
Member 3 — Gateway
Member 4 — Cloud
```

Cloud endpoint:

```http
POST /api/v1/crypto/sessions
```

Gateway flow:

```text
GET /api/v1/crypto/public-key
↓
validate protocol_version / algorithm / key_id
↓
ML-KEM-768 encapsulate
↓
HKDF-SHA-256 derive session key
↓
POST versioned session request
↓
receive versioned session response
```

Session request:

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "key_id": "cloud-key-001",
  "encapsulation_ciphertext": "<base64url>"
}
```

Cloud flow:

```text
validate request
↓
Base64URL-decode ciphertext
↓
ML-KEM-768 decapsulate
↓
HKDF-SHA-256 derive 32-byte session key
↓
store in-memory session
```

For a valid Gateway encapsulation, Gateway and Cloud derive equivalent shared keying material and therefore the same session key.

Do not treat the absence of a decapsulation exception as proof that both sides necessarily derived the same key for an arbitrarily modified valid-length ciphertext.

Response:

```json
{
  "protocol_version": "1",
  "session_id": "sess-...",
  "status": "established",
  "expires_at": "..."
}
```

No shared secret/session key crosses the network.

---

# 19. Session integration test

Verify:

```text
Gateway local session
Cloud stored session

same derived key
same session ID association
same expiry assumptions
same gateway ownership
```

Again, do not print the keys merely to verify them.

Use assertions.

---

# 20. Phase 11 — Authenticated encryption


Implement AEAD wrappers using the frozen suite:

```text
AES-256-GCM
```

Gateway:

```text
encrypt
```

Cloud:

```text
authenticate/decrypt
```

Use:

```text
32-byte session key
12-byte / 96-bit nonce
```

with cryptographically secure nonce generation.

AAD contains exactly:

```text
protocol_version
gateway_id
session_id
request_id
```

AAD encoding is deterministic JSON:

```text
UTF-8
sorted keys
compact separators "," and ":"
```

Both sides must independently produce byte-identical AAD.

For a new logical secure message:

```text
new request_id
new nonce
new encryption
```

For a pure transport retry of the same logical request:

```text
resend the already-built SecureEnvelope
```

rather than creating a second logical message.

---

# 21. Crypto unit tests

Test:

```text
round trip

wrong key fails

modified ciphertext fails

modified AAD fails

modified nonce fails

same ciphertext cannot be silently accepted after modification
```

This is a key security-review area.

---

# 22. Phase 12 — Secure envelope


Implement exactly:

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "session_id": "sess-...",
  "request_id": "req-...",
  "nonce": "<base64url>",
  "ciphertext": "<base64url>"
}
```

Rules:

```text
nonce decodes to exactly 12 bytes
all binary JSON fields use Base64URL
request_id is authenticated as AAD
no algorithm negotiation field
no plaintext canonical measurement
no shared/session secret
```

Gateway serializes.

Cloud validates and parses.

The crypto suite is selected by protocol version, not by per-message negotiation.

---

# 23. Phase 13 — Secure cloud endpoint


Cloud implements:

```http
POST /api/v1/secure/measurements
```

Processing:

```text
envelope validation
      ↓
protocol-version validation
      ↓
Base64URL / nonce-size validation
      ↓
session lookup
      ↓
session ownership
      ↓
expiry check
      ↓
reconstruct deterministic AAD
      ↓
AES-256-GCM authenticate/decrypt
      ↓
JSON parse
      ↓
canonical validation
      ↓
gateway identity consistency check
      ↓
idempotency
      ↓
storage
```

No storage before all validation succeeds.

Frozen session errors:

```text
unknown session
→ 409 SESSION_INVALID

expired session
→ 409 SESSION_EXPIRED
```

The secure endpoint never attempts to interpret failed secure input as plaintext.

---

# 24. Phase 14 — Gateway secure transport


Gateway selects one transport explicitly.

```text
if SECURITY_MODE=classical
→ POST /api/v1/baseline/measurements
→ X-Request-ID header
```

```text
if SECURITY_MODE=mlkem
→ ML-KEM session
→ SecureEnvelope
→ POST /api/v1/secure/measurements
```

Protocol version `1` supports:

```text
PQC_FAILURE_POLICY=fail_closed
```

only.

Therefore:

```text
ML-KEM/session/security failure
→ visible failure
→ no automatic baseline POST
```

Session recovery is separate:

```text
409 SESSION_INVALID / SESSION_EXPIRED
→ invalidate local session
→ establish one new session
→ retry same logical request once
```

Do not merge baseline and secure parsing/transport into an ambiguous path.

---

# 25. First PQC end-to-end milestone

Now test:

```text
Legacy Device
      ↓
Gateway
      ↓
ML-KEM handshake
      ↓
session
      ↓
AEAD protected measurement
      ↓
Cloud
      ↓
decrypt
      ↓
store
```

Success means:

```text
original measurement == stored measurement
```

This is your biggest technical milestone.

---

# 26. Phase 15 — Session reuse

Verify that you are **not performing ML-KEM for every measurement**.

Expected:

```text
Measurement 1
→ handshake
→ send

Measurement 2
→ reuse session

Measurement 3
→ reuse session
```

Test by counting handshakes.

---

# 27. Phase 16 — Session expiration/rekey


Default:

```text
SESSION_TTL_SECONDS=300
```

For tests, use a controlled clock or a very small TTL such as:

```text
1 second
```

Verify:

```text
session established
↓
expires
↓
Gateway attempts next secure message
↓
Cloud returns 409 SESSION_EXPIRED if Gateway did not already detect local expiry
↓
Gateway invalidates local session
↓
new ML-KEM handshake
↓
new session
↓
same logical request retried once
```

Also verify Gateway can proactively re-establish when its own local expiry check detects expiration before sending.

---

# 28. Phase 17 — Failure injection: Legacy

Member 1 finalizes fault simulation.

Test end-to-end:

```text
FAILURE_MODE=invalid_humidity
FAILURE_RATE=1.0

Legacy sends humidity=145
↓
Gateway rejects
↓
Cloud receives nothing
```

Repeat for selected scenarios.

---

# 29. Phase 18 — Failure injection: Gateway


Owners:

```text
Member 2 + Member 3
```

Initial modes:

```text
none
processing_error
processing_delay
mlkem_handshake_failure
corrupt_ciphertext
cloud_timeout
cloud_unavailable
drop_message
session_missing
session_expired
random
```

Representative expected behavior:

```text
processing_error
→ Gateway request fails visibly

cloud_timeout / cloud_unavailable
→ bounded retry

mlkem_handshake_failure
→ fail closed; no baseline fallback

corrupt_ciphertext
→ Cloud authentication failure; no storage

session_missing / session_expired
→ session re-establishment path

drop_message
→ no false success
```

Test representative modes against actual downstream behavior.

---

# 30. Phase 19 — Failure injection: Cloud


Owner:

```text
Member 4
```

Initial modes:

```text
none
public_key_unavailable
mlkem_decapsulation_failure
# explicit simulated wrapper/application failure
session_not_found
session_expired
decryption_failure
storage_failure
service_unavailable
processing_delay
drop_response
random
```

Important scenario:

```text
drop_response
```

means:

```text
Cloud may successfully store
↓
response is lost/dropped
↓
Gateway retries by resending the SAME already-built SecureEnvelope
(same request_id, nonce, ciphertext, and AAD)
↓
Cloud idempotency prevents duplicate row
```

This is required for the idempotent retransmission test.

---

# 31. Cross-component failure suite


Member 5 coordinates these scenarios.

| Scenario | Expected |
|---|---|
| Malformed/unparseable Legacy JSON | Gateway rejects with `400` |
| Missing required Legacy field | Gateway rejects with `422` |
| Invalid Legacy humidity | Gateway rejects with `422` |
| Invalid timestamp | Gateway rejects with `422` |
| Duplicate sequence | Gateway rejects with `409` |
| Out-of-order sequence | Gateway rejects with `409` |
| Sequence gap | Gateway accepts + log/metric |
| Gateway processing error | Legacy receives visible failure |
| Gateway ML-KEM failure | no secure session; fail closed |
| Gateway corrupt ciphertext | Cloud rejects; no storage |
| Gateway Cloud timeout | bounded retry |
| Gateway Cloud unavailable | bounded retry |
| Gateway drop message | no Cloud record; no false success |
| Cloud public key unavailable | Gateway cannot establish session |
| Cloud simulated ML-KEM wrapper/decapsulation failure | no session |
| Cloud unknown session | `409 SESSION_INVALID`; Gateway re-establishes |
| Cloud session expired | `409 SESSION_EXPIRED`; Gateway re-establishes |
| Cloud decryption failure | no storage |
| Cloud storage failure | `503 Service Unavailable`; Gateway applies bounded retry |
| Cloud service unavailable | bounded Gateway retry |
| Cloud drop response | retry remains idempotent; only one DB row |

---

# 32. Phase 20 — Logging

Member 5 can define format, but each component implements its own events.

Common fields:

```text
event
request_id
device_id
gateway_id
sequence_number
```

Conditional:

```text
session_id
key_id
record_id
```

Absolutely prohibited:

```text
private_key
shared_secret
session_key
password
token
```

---

# 33. Secret-leakage tests

Create automated tests that use known fake secret values.

For example:

```text
fake session secret = known marker
```

Run relevant code while capturing logs.

Then:

```text
assert marker not in logs
```

This is particularly valuable for the assignment's requirement to critically evaluate generated code.

---

# 34. Phase 21 — Metrics


Owner:

```text
Member 5
```

Member 5 coordinates the metric contract; Members 2–4 implement component-owned metrics.

Gateway minimum set:

```text
gateway_measurements_received_total
gateway_measurements_accepted_total
gateway_measurements_rejected_total
gateway_duplicate_measurements_total
gateway_out_of_order_measurements_total
gateway_sequence_gaps_total

gateway_cloud_requests_total
gateway_cloud_failures_total
gateway_cloud_retries_total
gateway_cloud_request_duration_seconds

gateway_mlkem_handshakes_total
gateway_mlkem_handshake_failures_total
gateway_mlkem_handshake_duration_seconds
gateway_session_reestablishments_total
gateway_encryption_failures_total
gateway_active_session
gateway_pqc_fallback_total

gateway_injected_failures_total
```

For protocol v1, `gateway_pqc_fallback_total` should remain zero because runtime fallback is not implemented.

Cloud minimum set:

```text
cloud_baseline_requests_total
cloud_secure_requests_total
cloud_secure_requests_rejected_total
cloud_request_duration_seconds

cloud_mlkem_sessions_created_total
cloud_mlkem_session_failures_total
cloud_mlkem_decapsulation_duration_seconds
cloud_active_sessions
cloud_expired_sessions_total

cloud_decryption_failures_total
cloud_authenticated_messages_total

cloud_measurements_stored_total
cloud_storage_failures_total
cloud_duplicate_measurements_total

cloud_injected_failures_total
```

Do not create excessive or high-cardinality metrics.

Never use:

```text
request_id
session_id
record_id
```

as unbounded metric labels.

---

# 35. Phase 22 — Health/readiness

Gateway:

```text
GET /health
GET /ready
```

Cloud:

```text
GET /health
GET /ready
```

Expected semantics:

```text
health
→ process alive

ready
→ capable of useful work in the configured mode
```

Frozen readiness rules:

```text
Gateway readiness
→ does not require an already active ML-KEM session

Cloud readiness
→ does not require an active Gateway session

Modernized Mode
→ crypto subsystem must be initialized and usable

Baseline Mode
→ active secure-session state is not required
```

Sessions are established lazily.

Do not expose sensitive crypto information.

---

# 36. Phase 23 — Docker Compose

Owner:

```text
Member 5
```

Target:

```text
docker compose up
```

starts:

```text
legacy-device
edge-gateway
cloud-service
```

and possibly no separate DB if SQLite is used.

Network:

```text
legacy-device
     ↓
edge-gateway:8000
     ↓
cloud-service:9000
```

---

# 37. Docker configuration


Example conceptual service configuration:

```text
Legacy container:
DEVICE_ID=sensor-001
GATEWAY_URL=http://edge-gateway:8000
FAILURE_MODE=<mapped Legacy value>
FAILURE_RATE=<mapped Legacy value>
```

```text
Gateway container:
GATEWAY_ID=gateway-001
CLOUD_URL=http://cloud-service:9000
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
FAILURE_MODE=<mapped Gateway value>
FAILURE_RATE=<mapped Gateway value>
```

```text
Cloud container:
CLOUD_ID=cloud-001
SECURITY_MODE=mlkem
FAILURE_MODE=<mapped Cloud value>
FAILURE_RATE=<mapped Cloud value>
```

At the root `.env.example` / Compose level, use service-scoped source variables:

```text
LEGACY_FAILURE_MODE=none
LEGACY_FAILURE_RATE=0.0

GATEWAY_FAILURE_MODE=none
GATEWAY_FAILURE_RATE=0.0

CLOUD_FAILURE_MODE=none
CLOUD_FAILURE_RATE=0.0
```

Compose maps those into each process's generic internal variables:

```text
FAILURE_MODE
FAILURE_RATE
```

This prevents one global root variable from accidentally controlling all three components.

No secret material should be committed.

---

# 38. Phase 24 — CI pipeline

The CI should eventually run:

```text
uv sync --frozen

ruff

unit tests

contract tests

integration tests

ai-history check
```

Potentially:

```text
docker build
```

too.

Keep pipeline runtime manageable.

---

# 39. CI ordering

Recommended:

```text
Checkout
   ↓
Python setup
   ↓
uv setup
   ↓
uv sync --frozen
   ↓
ruff
   ↓
unit tests
   ↓
contract tests
   ↓
integration tests
   ↓
ai-history check
   ↓
Docker build
```

A failure should stop the pipeline.

---

# 40. Phase 25 — Baseline vs Modernized evaluation

Now run equivalent workloads.

Example:

```text
100 measurements
```

Baseline:

```text
SECURITY_MODE=classical
```

Modern:

```text
SECURITY_MODE=mlkem
```

Record:

|Metric|Baseline Mode (`classical`)|Modernized Mode (`mlkem`)|
|---|--:|--:|
|Gateway→Cloud latency|||
|First-message latency|||
|Subsequent-message latency|||
|Payload size|||
|Session establishment time|N/A||
|Successful messages|||
|Failure handling|||

Don't invent conclusions.

Collect actual numbers.

---

# 41. Why first-message and later-message latency should be separate

The first secure message includes:

```text
public key retrieval
ML-KEM encapsulation
session setup
```

Later messages reuse the session.

Therefore:

```text
first message
≠
normal steady-state message
```

Measure both.

That's a much better technical evaluation than averaging everything together.

---

# 42. Phase 26 — Security evaluation


Evaluate:

```text
Legacy side remains non-PQC and comparatively weak

Gateway→Cloud confidentiality

Gateway→Cloud integrity/authentication

ML-KEM-768 post-quantum key establishment

HKDF-SHA-256 session-key derivation

AES-256-GCM nonce/AAD handling

session management and expiry

fail-closed behavior

tampered ciphertext rejection

AAD tampering rejection

secret logging

replay/idempotency

Cloud public-key trust assumptions

restart behavior for ephemeral Cloud key/session state

ML-KEM implicit-rejection behavior and its testing implications
```

Be explicit about limitations.

Do not claim:

```text
"system is fully quantum secure"
```

because the Legacy→Gateway path is not post-quantum protected and the Cloud public-key trust model is simplified.

---

# 43. Phase 27 — Technical debt evaluation

Create a technical-debt table.

Likely items:

|Debt|Component|Impact|Possible future improvement|
|---|---|---|---|
|No legacy authentication|Legacy/Gateway|spoofing risk|device credentials|
|No offline queue|Legacy/Gateway|data loss|persistent queue|
|Simplified Cloud key trust|Gateway|MITM trust limitation|PKI|
|Ephemeral ML-KEM key|Cloud|identity changes on restart|persistent secure key|
|In-memory sessions|Gateway/Cloud|restart loses sessions|persistent session store|
|SQLite|Cloud|limited scale|PostgreSQL|
|No dedicated cryptographic anti-replay counter/window|Gateway/Cloud|authenticated envelopes can be replayed at crypto layer; business idempotency only prevents duplicate rows|per-session authenticated counter or replay window|
|Single instances|Gateway/Cloud|no HA|replication|

This aligns directly with the course expectation to identify weaknesses, remaining risks, and technical debt.

---

# 44. Recommended branch strategy

Use small branches such as:

```text
feature/legacy-sensor
feature/legacy-http-client
feature/gateway-validation
feature/cloud-storage
feature/mlkem-wrapper
feature/session-protocol
feature/secure-envelope
feature/failure-injection-gateway
feature/metrics
test/e2e-secure-flow
```

Avoid:

```text
feature/whole-project
```

---

# 45. PR dependency rule

A PR should be independently reviewable.

For example:

```text
PR #1 Protocol docs
      ↓
PR #2 Legacy models
      ↓
PR #3 Legacy client
```

Crypto work:

```text
PR A ML-KEM wrapper
      ↓
PR B KDF
      ↓
PR C Session management
      ↓
PR D AEAD wrapper
      ↓
PR E Secure endpoint
```

This makes human review much easier.

---

# 46. AI-history task strategy

Each meaningful implementation task should have one AI-history record.

For example:

```text
Task 0008
Implement Gateway legacy validation

Task 0009
Implement Gateway sequence tracker

Task 0010
Implement Cloud storage repository

Task 0011
Implement ML-KEM wrapper

Task 0012
Implement Gateway session manager
```

Within one task there may be several significant AI interactions.

Do not create one task for every trivial prompt.

---

# 47. AI workflow per development task

Your standard workflow should be:

```text
uv run ai-history start
        ↓
Agent implements full requested task
        ↓
Record significant interactions
        ↓
Agent runs tests/ruff
        ↓
Agent fixes its own issues
        ↓
uv run ai-history output
        ↓
Human reviews diff
        ↓
uv run ai-history review
        ↓
Accepted?
   ┌────┴─────┐
   │          │
  yes       modified
   │          │
   │        revision
   │          │
   └────┬─────┘
        ↓
human verifies
        ↓
uv run ai-history verify
```

The course expects AI outputs to be critically evaluated rather than trusted automatically.

---

# 48. Human review gate for normal code

Review:

```text
Does implementation match task?

Does it follow protocol specification?

Are errors handled?

Are tests meaningful?

Was unnecessary complexity added?

Did AI modify unrelated files?
```

---

# 49. Human review gate for crypto code

Crypto code requires stricter review:

```text
Are we using maintained library APIs correctly?

Any custom cryptographic logic?

Any secrets logged?

Any key written to disk unexpectedly?

Correct KDF context?

Correct key size?

Nonce safe?

AAD consistent?

Silent downgrade?

Exception swallowed?

AEAD ciphertext/authentication failure correctly rejected?

Does ML-KEM testing avoid assuming every modified valid-length KEM ciphertext must raise an explicit decapsulation exception?
```

---

# 50. Five-person parallel work schedule

A useful parallel sequence would look like this:

|Stage|Member 1|Member 2|Member 3|Member 4|Member 5|
|---|---|---|---|---|---|
|A|Legacy config/model|Gateway config/API|Crypto research|Cloud config/API|Repo/CI|
|B|Sensor/client|Validation/normalization|ML-KEM wrapper|Storage|Integration framework|
|C|Legacy failure injection|Sequence tracking|KDF/AEAD|Baseline endpoint|Docker baseline|
|D|Legacy tests|Gateway baseline client|Session manager|Cloud ML-KEM|Baseline E2E|
|E|Fix integration|Gateway failure modes|Secure Gateway flow|Secure Cloud flow|Secure E2E|
|F|Docs/review|Logs/metrics|Crypto review|Cloud failure modes|CI/metrics/evaluation|

This gives everyone meaningful independent work while respecting dependencies.

---

# 51. Critical merge milestones

I would use six project-wide milestones.

### Milestone A — Architecture Complete

```text
All four design docs committed.
```

### Milestone B — Baseline Components Complete

```text
Legacy
Gateway
Cloud

run separately.
```

### Milestone C — Baseline E2E Complete

```text
Legacy → Gateway → Cloud → SQLite
```

works.

### Milestone D — PQC Protocol Complete

```text
ML-KEM
KDF
session
AEAD
secure envelope
```

all work.

### Milestone E — Secure E2E Complete

```text
Legacy → Gateway → ML-KEM secured Cloud → DB
```

works.

### Milestone F — Production-like Course Demo

```text
Docker
CI
failure injection
health
metrics
logs
evaluation
documentation
```

all work.

---

# 52. Definition of Done for a development task

A task is not done merely because an agent produced code.

It is done when:

```text
implementation exists
tests exist
tests pass
ruff passes
protocol remains consistent
no unrelated changes
AI history complete
human review performed
requested revisions applied
final verification completed
PR reviewed
CI passes
```

---

# 53. Definition of Done for Legacy Device

Legacy is complete when:

```text
normal sensor generation works
failure generation works
sequence works
timestamps work
HTTP client works
timeouts work
retries work
400/409/422 vs retryable 5xx distinction works
400 = malformed/unparseable body
422 = parsed but missing/wrongly typed/domain-invalid fields
graceful shutdown works
Docker works
tests pass
```

---

# 54. Definition of Done for Gateway


Gateway is complete when:

```text
legacy API works
validation works
normalization works
request_id handling works
sequence tracking works
duplicate/out-of-order return 409
sequence state timing matches protocol

baseline Cloud communication works
X-Request-ID baseline propagation works

ML-KEM-768 sessions work
HKDF-SHA-256 works
AES-256-GCM works
secure envelopes work
request_id is authenticated as AAD

409 session recovery works
fail-closed behavior works
no automatic baseline downgrade

failure injection works
bounded retry works
health/readiness work
readiness does not require an active Gateway session
metrics work
logs are safe
Docker works
tests pass
```

---

# 55. Definition of Done for Cloud


Cloud is complete when:

```text
baseline endpoint works
X-Request-ID baseline correlation works

ML-KEM-768 public-key endpoint works
versioned session establishment works
ML-KEM wrapper tests handle implicit-rejection semantics correctly
HKDF-SHA-256 works
AES-256-GCM authentication/decryption works

409 SESSION_INVALID works
409 SESSION_EXPIRED works

canonical validation works
storage works
received_at maps to gateway_received_at
idempotency works
query API uses {record_id}

secure endpoint never accepts plaintext
authentication failure prevents storage
runtime plaintext fallback is absent

failure injection works
drop_response/idempotent retry works
health/readiness work
metrics work
logs safe
Docker works
tests pass
```

---

# 56. Definition of Done for the whole project


The project should satisfy all of these:

```text
Baseline Mode works
Modernized Mode works

Baseline Mode = SECURITY_MODE=classical
Modernized Mode = SECURITY_MODE=mlkem

Legacy compatibility preserved

ML-KEM-768 used on Gateway→Cloud path
HKDF-SHA-256 parameters match
AES-256-GCM protocol matches

No homemade crypto

PQC failure policy is fail_closed
No automatic plaintext downgrade

Unknown/expired sessions use 409 recovery contract

Legacy validation boundary is consistent:
400 = malformed/unparseable JSON
422 = parsed JSON with missing/wrongly typed/domain-invalid fields

ML-KEM tests do not assume every modified valid-length ciphertext raises an explicit exception

Failure injection works at all 3 layers

Dropped-response retry remains idempotent

Tests cover happy, negative, failure, and security paths

CI passes

Docker Compose starts test environment

Health/readiness checks work
Active secure sessions are not required merely for readiness

Logs are useful and secret-safe

Metrics are meaningful and avoid high-cardinality IDs

Baseline vs ML-KEM measurements recorded

Technical debt documented

AI outputs reviewed

AI history valid

Documentation complete
```

---

# 57. Recommended first implementation sequence


If you're starting coding now, follow this order:

```text
1. Commit/freeze architecture and corrected protocol documents

2. Implement Legacy configuration + valid Measurement model

3. Implement Legacy serializer / outgoing payload boundary

4. Implement Gateway legacy endpoint/model/validation

5. Implement Cloud baseline endpoint/storage

6. Implement Legacy HTTP client + payload failure injection

7. Make Baseline Mode Legacy → Gateway → Cloud work

8. Freeze and measure baseline

9. Select/test ML-KEM library
   - verify ML-KEM-768 support
   - document implicit-rejection behavior
   - avoid tests that require every modified valid-length ciphertext to throw

10. Implement Cloud ML-KEM-768 key pair/public-key endpoint

11. Implement Gateway ML-KEM-768 encapsulation

12. Implement Cloud decapsulation

13. Implement identical HKDF-SHA-256
    salt=None
    fixed info
    length=32

14. Implement versioned sessions

15. Implement AES-256-GCM wrappers + deterministic AAD

16. Implement SecureEnvelope

17. Implement secure Cloud endpoint

18. Implement Gateway Modernized Mode

19. Get secure E2E passing

20. Add bounded 409 session recovery

21. Add/finalize Legacy failure injection

22. Add/finalize Gateway failure injection

23. Add/finalize Cloud failure injection including drop_response

24. Add metrics

25. Finish health/readiness

26. Finish Docker Compose

27. Harden CI

28. Run baseline vs secure measurements

29. Run failure/security experiments

30. Document technical debt and final human review/report
```

Every difficult step should have a previously working state to fall back to.

Modernized Mode must never fall back automatically to Baseline Mode.

---

# 58. What should be implemented first this week

The first actual coding milestone should **not** contain ML-KEM.

Aim first for:

```text
Legacy Device
    │
    │ JSON
    ▼
Gateway
    │
    │ canonical JSON
    ▼
Cloud
    │
    ▼
SQLite
```

with:

```text
docker compose up
```

and one measurement reaching the database.

Once that is stable and tested, you have a proper baseline and can modernize only the Gateway–Cloud boundary.

That approach matches the course's modernization framing much better than building the PQC version first and inventing a baseline afterward.

---

# 59. Final project development flow


The whole project is:

```text
DESIGN
  │
  ├── Legacy design
  ├── Gateway design
  ├── Cloud design
  └── Shared protocol specification
  │
  ▼
BASELINE IMPLEMENTATION
  │
  ├── Legacy valid Measurement + serializer
  ├── Gateway validation/sequence/canonicalization
  └── Cloud baseline/storage
  │
  ▼
BASELINE E2E
  │
  ├── SECURITY_MODE=classical
  └── X-Request-ID correlation
  │
  ▼
PQC MODERNIZATION
  │
  ├── ML-KEM-768
  ├── HKDF-SHA-256
  │   ├── salt=None
  │   ├── fixed info
  │   └── 32-byte output
  ├── Sessions
  ├── AES-256-GCM
  │   ├── 12-byte nonce
  │   └── deterministic AAD
  └── SecureEnvelope
  │
  ▼
SECURE E2E
  │
  ├── SECURITY_MODE=mlkem
  ├── fail_closed
  └── bounded 409 session recovery
  │
  ▼
FAILURE TESTING
  │
  ├── Legacy payload failures
  ├── Gateway processing/crypto/transport failures
  └── Cloud crypto/storage/drop-response failures
  │
  ▼
OPERATIONS
  │
  ├── Logging
  ├── Metrics
  ├── Health/readiness
  ├── Docker
  └── CI/CD
  │
  ▼
EVALUATION
  │
  ├── Baseline vs ML-KEM
  ├── Security
  ├── Performance
  ├── Maintainability
  ├── Operations
  └── Technical debt
  │
  ▼
FINAL DOCUMENTATION
```

---
