# Member 2 — Edge Gateway Application & Legacy Interface Owner

## Overall mission

Member 2 owns the part of the gateway that turns unreliable or limited legacy-device traffic into **clean, validated, canonical data ready for modern cloud transport**.

Their main responsibility is this side of the architecture:

```text
Legacy Device
     │
     │ HTTP + JSON
     ▼
┌──────────────────────────────┐
│         Edge Gateway         │
│                              │
│  Legacy HTTP API             │  ← Member 2
│  Request validation          │  ← Member 2
│  Data normalization          │  ← Member 2
│  Sequence tracking           │  ← Member 2
│  Request correlation         │  ← Member 2
│  Baseline Cloud client       │  ← Member 2
│  Failure injection           │  ← Member 2 + Member 3
│  Health / readiness          │  ← Member 2 + Member 5
│                              │
│  Session management          │  ← Member 3
│  ML-KEM                      │  ← Member 3
│  KDF                         │  ← Member 3
│  AEAD encryption             │  ← Member 3
└──────────────┬───────────────┘
               │
               ▼
         Cloud Service
```

Member 2 therefore owns the **legacy adaptation layer and most of the gateway application behavior**, while Member 3 owns the cryptographic modernization internals.

---

# Member 2 final deliverables

Member 2 should ultimately contribute:

|Deliverable|Expected result|
|---|---|
|Gateway configuration|validated runtime configuration|
|Gateway application skeleton|runnable HTTP service|
|Legacy measurement endpoint|`/api/v1/measurements`|
|Request validation|schema + domain validation|
|Canonical normalization|legacy → canonical model|
|Sequence tracking|duplicates, out-of-order, gaps|
|Request/correlation IDs|cross-service traceability|
|Baseline Cloud client|Gateway→Cloud classical path|
|Baseline retry handling|bounded Cloud communication|
|Gateway failure injection|non-crypto and integration-oriented scenarios|
|Gateway logging|request/validation/sequence behavior|
|Gateway health/readiness|usable operational endpoints|
|Unit tests|API, validation, sequence, client, failures|
|Integration tests|Legacy↔Gateway and baseline Gateway↔Cloud|
|Contract tests|legacy and cloud protocol consistency|
|Documentation|gateway application behavior|
|AI-history records|prompts, outputs, human decisions|
|Peer review|especially Member 1 and Member 3 boundaries|

---

# Task M2-00 — Review and freeze Gateway boundaries

**Priority:** Critical  
**Coding:** No application implementation yet.

Before writing code, Member 2 must understand exactly where their ownership begins and ends.

The gateway has two interfaces:

```text
Interface A
Legacy Device → Gateway

Interface B
Gateway → Cloud
```

Member 2 owns Interface A completely and owns the **baseline/non-crypto application part** of Interface B.

Member 3 owns the secure ML-KEM/session/AEAD implementation behind Interface B.

### Legacy contract to confirm

```http
POST /api/v1/measurements
Content-Type: application/json
```

Request:

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "timestamp": "2026-09-21T13:45:31Z",
  "sequence_number": 184
}
```

### Canonical output Member 2 must produce

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "measured_at": "2026-09-21T13:45:31Z",
  "sequence_number": 184,
  "received_at": "2026-09-21T13:45:31.218Z",
  "gateway_id": "gateway-001"
}
```

### Acceptance criteria

```text
[ ] Legacy request schema understood
[ ] Gateway status-code semantics understood
[ ] Canonical model frozen
[ ] Baseline Cloud endpoint agreed
[ ] Member 2 / Member 3 boundary agreed
[ ] No independent protocol changes
```

---

# Task M2-01 — Implement Gateway configuration

**Primary file:**

```text
edge_gateway/
└── src/
    └── edge_gateway/
        └── config.py
```

Recommended configuration:

```text
GATEWAY_ID=gateway-001
HOST=0.0.0.0
PORT=8000
CLOUD_URL=http://cloud-service:9000
CLOUD_TIMEOUT_SECONDS=3
CLOUD_MAX_RETRIES=2
SECURITY_MODE=classical
SESSION_TTL_SECONDS=300
PQC_FAILURE_POLICY=fail_closed
FAILURE_MODE=none
FAILURE_RATE=0.0
FAILURE_SEED=
LOG_LEVEL=INFO
```

Member 2 should implement the complete configuration object even if some values are later consumed by Member 3.

### Validation

```text
GATEWAY_ID → non-empty
PORT → valid TCP port
CLOUD_URL → non-empty / valid enough for client
CLOUD_TIMEOUT_SECONDS → > 0
CLOUD_MAX_RETRIES → >= 0
SECURITY_MODE → classical | mlkem
SESSION_TTL_SECONDS → > 0
PQC_FAILURE_POLICY → fail_closed only
FAILURE_RATE → 0.0–1.0
FAILURE_MODE → known gateway failure mode
```

For protocol version `1`, any `PQC_FAILURE_POLICY` value other than `fail_closed` must fail startup.

Configuration should be loaded once into one structured object rather than scattering `os.getenv(...)` calls throughout the application.

### Tests

```text
valid defaults
custom environment values
empty gateway ID
invalid port
negative timeout
negative retries
unknown security mode
zero session TTL
PQC_FAILURE_POLICY != fail_closed
invalid failure rate
unknown failure mode
```

### Definition of Done

```text
[ ] Configuration centralized
[ ] Defaults documented
[ ] Invalid startup config rejected
[ ] Protocol v1 accepts fail_closed only
[ ] Tests pass
[ ] Member 3 can consume crypto-related config
```

---

# Task M2-02 — Implement Gateway application skeleton

**Primary file:**

```text
app.py
```

The application framework should support:

```text
POST /api/v1/measurements
GET  /health
GET  /ready
GET  /metrics
```

The exact framework can be FastAPI if that is the team's choice.

### Application responsibilities

The top-level app should:

```text
load configuration
initialize logging
initialize dependencies
register routes
manage lifecycle
start service
handle graceful shutdown
```

It should **not** contain:

```text
validation business rules
sequence algorithms
Cloud retry loops
ML-KEM implementation
encryption code
SQL
```

### Acceptance

```text
[ ] Service starts
[ ] Routes register
[ ] Invalid config prevents startup
[ ] Lifecycle hooks available
[ ] Dependencies can be tested/mocked
```

---

# Task M2-03 — Implement Legacy measurement request model

Member 2 needs a gateway-side representation of incoming Legacy data.

Suggested:

```text
LegacyMeasurement
├── device_id
├── temperature_c
├── humidity_pct
├── timestamp
└── sequence_number
```

This model must match Member 1's protocol exactly.

### Important rule

Do not directly import:

```python
from legacy_system...
```

into the gateway.

Both components implement the same **documented contract** independently.

That avoids tight source-code coupling.

### Tests

Verify:

```text
valid payload parses
missing field rejected
wrong type rejected
extra fields rejected (exactly the five documented Legacy fields)
field names exactly match protocol
```

---

# Task M2-04 — Implement schema validation

Member 2 should separate:

```text
syntactic/schema validation
```

from:

```text
domain validation
```

### Schema validation examples

Reject:

```json
{
  "temperature_c": "hot"
}
```

Reject:

```json
{
  "humidity_pct": null
}
```

Reject missing required fields.

### Expected response

The project-wide mapping is frozen:

```text
malformed or unparseable JSON/body syntax
→ 400 Bad Request

JSON parses, but a required field is missing, has the wrong type,
or violates a domain rule
→ 422 Unprocessable Entity
```

### Acceptance

```text
[ ] Bad JSON safely rejected
[ ] Missing required fields rejected
[ ] Wrong field types rejected
[ ] No Cloud call occurs on invalid schema
```

---

# Task M2-05 — Implement domain validation

Once JSON/schema is structurally valid, validate values.

Agreed ranges:

```text
temperature_c:
-40 <= x <= 85

humidity_pct:
0 <= x <= 100

sequence_number:
>= 0

device_id:
non-empty

timestamp:
valid ISO-8601 UTC/timezone-aware
```

### Important distinction

The Legacy Device normally generates:

```text
temperature 15–30
humidity 30–70
```

but the Gateway must accept the **wider valid protocol range**.

Example:

```text
temperature = -25
```

should be valid even though the simulator does not normally generate it.

### Tests

```text
minimum valid temperature
maximum valid temperature
below minimum
above maximum

humidity 0
humidity 100
humidity -1
humidity 101

empty device ID

valid timestamp
invalid timestamp
timezone-less timestamp if policy rejects it

sequence 0
negative sequence
```

---

# Task M2-06 — Define Gateway validation errors

Member 2 should create predictable application-level error semantics.

Use the common project structure:

```json
{
  "error": {
    "code": "INVALID_MEASUREMENT",
    "message": "measurement validation failed"
  }
}
```

Frozen Legacy-facing status mapping:

```text
invalid JSON/body → 400
schema/domain validation failure → 422
duplicate sequence → 409 OUT_OF_ORDER_SEQUENCE/DUPLICATE_SEQUENCE
out-of-order sequence → 409
Cloud or secure path unavailable after bounded retries → 503
Gateway internal failure → 500
```

Stable codes include:

```text
INVALID_JSON
INVALID_MEASUREMENT
DUPLICATE_SEQUENCE
OUT_OF_ORDER_SEQUENCE
CLOUD_UNAVAILABLE
INTERNAL_ERROR
```

Do not expose Python exceptions, stack traces, filesystem paths, library internals, or cryptographic details to Legacy Devices.

Tests must verify both HTTP status and stable `error.code`.

---

# Task M2-07 — Implement canonical measurement model

Member 2 owns translation from Legacy representation into Gateway canonical form.

Model:

```text
CanonicalMeasurement
├── device_id
├── temperature_c
├── humidity_pct
├── measured_at
├── sequence_number
├── received_at
└── gateway_id
```

### Transformation

```text
Legacy timestamp
→ measured_at

Gateway current UTC time
→ received_at

GATEWAY_ID
→ gateway_id
```

### Do not add

```text
session_id
nonce
ciphertext
ML-KEM data
Cloud record ID
```

Those belong later in transport/security/storage.

---

# Task M2-08 — Implement normalization layer

**Suggested file:**

```text
validation.py
```

or a dedicated:

```text
normalization.py
```

if this makes the code clearer.

Conceptually:

```python
canonical = normalize(
    legacy_measurement,
    gateway_id=...,
    received_at=...
)
```

### Requirements

Normalization should:

```text
preserve device ID
preserve temperature exactly
preserve humidity exactly
preserve sequence number
rename timestamp → measured_at
add received_at
add gateway_id
```

### Tests

Use deterministic timestamps.

Assert:

```text
legacy.temperature == canonical.temperature

legacy.humidity == canonical.humidity

legacy.timestamp == canonical.measured_at

canonical.gateway_id == configured ID
```

---

# Task M2-09 — Implement request/correlation ID creation

For every accepted incoming Legacy request, Gateway creates a unique `request_id`.

Example:

```text
req-550e8400-e29b-...
```

`request_id` is request/transport context. It is **not** part of `CanonicalMeasurement`.

### Baseline Mode

For:

```http
POST /api/v1/baseline/measurements
```

send:

```http
X-Request-ID: req-...
```

The canonical JSON body remains unchanged.

### Modernized Mode

Member 3 includes `request_id` in `SecureEnvelope` and authenticates it as AAD. The Gateway may also send `X-Request-ID` for HTTP diagnostics, but the authenticated envelope value is authoritative.

### Requirements

```text
unique enough for tracing
not secret
not key material
not based on sensitive contents
not used as an unbounded metrics label
```

### Tests

```text
different accepted requests get different IDs
request_id is absent from CanonicalMeasurement serialization
baseline Cloud request carries X-Request-ID
request_id appears in Gateway logs
secure transport receives the same request_id context
```

---

# Task M2-10 — Implement sequence tracker

This is one of Member 2's main functional tasks.

Maintain `last_sequence_number` per `device_id`.

Frozen behavior:

```text
first valid sequence → accept
new == last + 1 → accept
new > last + 1 → accept + gap log/metric
new == last → reject with 409 DUPLICATE_SEQUENCE
new < last → reject with 409 OUT_OF_ORDER_SEQUENCE
```

The meaning of `last_sequence_number` is frozen:

> the last valid sequence observed and accepted by the Gateway's Legacy-side sequence policy.

It does **not** mean the last sequence successfully stored by Cloud.

The state update occurs after schema/domain validation and sequence-policy acceptance, before downstream Cloud delivery. This is no longer an open design question.

---

# Task M2-11 — Sequence-state design

Initial sequence tracking is in-memory. Gateway restart therefore loses history; this is accepted technical debt.

### Frozen timing

```text
receive seq=10
↓
schema/domain validation succeeds
↓
sequence policy accepts
↓
last_sequence[device_id] = 10
↓
Cloud forwarding later fails
```

The state remains `10`. Cloud delivery state is separate.

### Concurrency

Checking and updating `last_sequence[device_id]` must be atomic enough that concurrent same-device requests do not both pass against stale state. A simple lock or serialized update is enough for this course.

### Tests

```text
first message
normal increment
duplicate → 409
out-of-order → 409
gap accepted
two device IDs independent
Cloud failure after valid seq=10 → state remains 10
concurrent same-device requests → deterministic safe state
```

---

# Task M2-12 — Implement `/api/v1/measurements`

This is Member 2's main endpoint.

Processing order:

```text
Receive HTTP request
↓
Parse request
↓
Validate schema
↓
Validate domain
↓
Check + commit sequence state
↓
Normalize to CanonicalMeasurement
↓
Create request_id separately
↓
Apply relevant Gateway processing failure hook
↓
Forward through selected Cloud transport
↓
Interpret result
↓
Respond to Legacy Device
```

Before Cloud communication:

```text
invalid JSON → 400
invalid schema/domain → 422
duplicate → 409
out-of-order → 409
```

Only return `202 Accepted` after downstream Cloud acceptance in this initial synchronous design.

Because sequence state means “last valid sequence observed by Gateway,” it is committed before Cloud forwarding. If Cloud later fails, a Legacy retry of the same sequence can legitimately receive `409` as duplicate. Cloud-side idempotency separately protects Gateway→Cloud retransmissions.

Document this tradeoff clearly.

---

# Task M2-13 — Implement baseline Cloud client

Before any ML-KEM work, Member 2 must get **Baseline Mode** forwarding working.

```http
POST /api/v1/baseline/measurements
Content-Type: application/json
X-Request-ID: req-...
```

Body:

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "measured_at": "...",
  "sequence_number": 184,
  "received_at": "...",
  "gateway_id": "gateway-001"
}
```

`request_id` is **not** part of this body; it travels in `X-Request-ID`.

Responsibilities:

```text
serialize CanonicalMeasurement
attach X-Request-ID
send request
timeout
retry classification
return normalized result
```

Do not skip the baseline and jump directly to ML-KEM.

---

# Task M2-14 — Implement Cloud retry policy

Gateway→Cloud behavior has three categories.

### Normal transport/service retry

```text
network failure
timeout
500
502
503
504
```

### Permanent/non-retryable

```text
400
422
unsupported protocol version
malformed/tampered secure-message rejection
```

### Secure session recovery

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

These are not ordinary repeated HTTP retries. Member 3's secure transport should:

```text
invalidate local session
↓
fetch current Cloud public key
↓
establish one new ML-KEM session
↓
retry the same logical request once
```

Default normal transport retry:

```text
CLOUD_MAX_RETRIES=2
```

meaning at most 3 transport attempts. Tests must mock backoff/sleep.

---

# Task M2-15 — Define Gateway response mapping

Member 2 should map outcomes to Legacy responses consistently.

| Gateway/downstream condition | Legacy response |
|---|---:|
| successful Cloud delivery | `202` |
| invalid JSON | `400` |
| invalid Legacy schema/domain | `422` |
| duplicate sequence | `409` |
| out-of-order sequence | `409` |
| Cloud unavailable after retries | `503` |
| secure session/PQC unavailable after bounded recovery | `503` |
| Gateway internal failure | `500` |

Use stable structured error codes such as `INVALID_JSON`, `INVALID_MEASUREMENT`, `DUPLICATE_SEQUENCE`, `OUT_OF_ORDER_SEQUENCE`, `CLOUD_UNAVAILABLE`, and `INTERNAL_ERROR`.

Any change requires coordination with Member 1 and an update to the shared protocol first.

---

# Task M2-16 — Baseline Gateway↔Cloud integration

**Shared with:** Member 4.

Before ML-KEM work, prove:

```text
Gateway
↓
POST /api/v1/baseline/measurements
+ X-Request-ID
↓
Cloud
↓
SQLite
```

Canonical test input:

```json
{
  "device_id": "sensor-test",
  "temperature_c": 22.5,
  "humidity_pct": 44.0,
  "measured_at": "2026-09-21T12:00:00Z",
  "sequence_number": 1,
  "received_at": "2026-09-21T12:00:00.100Z",
  "gateway_id": "gateway-test"
}
```

Create `request_id=req-test-001` separately and verify Cloud receives it through `X-Request-ID`.

Also verify canonical `received_at` maps to stored `gateway_received_at`; Cloud adds `cloud_received_at` and `record_id`.

---

# Task M2-17 — Support first full baseline E2E

**Shared with:** Members 1, 4, and 5.

Target:

```text
Legacy
 ↓
Gateway
 ↓
Cloud
 ↓
SQLite
```

Member 2 verifies Gateway transformations are correct.

### Acceptance

```text
Legacy temperature
=
Cloud stored temperature

Legacy humidity
=
Cloud stored humidity

Legacy timestamp
=
Cloud measured_at

Gateway received_at added

Gateway ID added
```

This milestone must exist before PQC modernization.

---

# Task M2-18 — Baseline Gateway measurements

Member 2 should help collect baseline evidence.

Useful Gateway-side measurements:

```text
number of Legacy requests

accepted requests

rejected requests

Legacy→Gateway processing duration

Gateway→Cloud baseline latency

Cloud retry count

canonical payload size
```

Do not create an excessive benchmarking framework.

The goal is evidence for later comparison.

---

# Task M2-19 — Implement Gateway failure-injection framework

Member 2 and Member 3 jointly own Gateway failure injection.

Member 2 should build the generic application-level infrastructure.

Suggested package:

```text
failure/
└── injector.py
```

Configuration:

```text
FAILURE_MODE=none
FAILURE_RATE=0.0
FAILURE_SEED=
```

### Member 2-owned failure modes

```text
none
processing_error
processing_delay
cloud_timeout
cloud_unavailable
drop_message
random
```

### Member 3-owned or jointly implemented

```text
mlkem_handshake_failure
corrupt_ciphertext
session_missing
session_expired
```

Do not let the generic injector become tangled with crypto internals.

---

# Task M2-20 — Implement `processing_error`

Purpose:

Simulate a Gateway application failure after valid Legacy input.

Example:

```text
Legacy valid
 ↓
Gateway validates
 ↓
failure injection
 ↓
processing_error
 ↓
500
```

This tests Legacy behavior when Gateway itself fails.

### Requirements

```text
controlled
logged
measured
does not crash process
does not permanently damage state
```

---

# Task M2-21 — Implement `processing_delay`

Optional but useful.

Configuration may include:

```text
FAILURE_DELAY_SECONDS=2
```

Flow:

```text
valid request
 ↓
injected delay
 ↓
continue
```

This allows timeout behavior to be tested.

### Safeguard

Do not allow absurd unbounded values without validation.

---

# Task M2-22 — Implement `cloud_timeout`

This should simulate the Cloud client observing a timeout without needing to physically break the network every time.

Expected:

```text
Cloud attempt
 ↓
simulated timeout
 ↓
retry policy
```

This belongs at the Cloud-client boundary, not inside validation.

### Tests

```text
failure rate 1.0
→ timeout every eligible call

retry count honored

final 503 after exhaustion
```

---

# Task M2-23 — Implement `cloud_unavailable`

Simulate:

```text
503-like downstream condition
```

Expected:

```text
Gateway retries
```

and after exhaustion:

```text
Legacy receives 503
```

---

# Task M2-24 — Implement `drop_message`

This scenario deliberately avoids Cloud forwarding.

Be explicit about semantics.

Recommended behavior for testing:

```text
measurement accepted internally
 ↓
injection decides to drop
 ↓
log failure
 ↓
do not pretend Cloud accepted it
 ↓
Legacy receives failure
```

Do **not** silently return `202`.

Otherwise data loss becomes invisible.

---

# Task M2-25 — Failure-injection safety review

Member 2 must ensure:

```text
FAILURE_MODE default = none
FAILURE_RATE default = 0.0
```

When enabled:

```text
WARNING event=failure_injection_enabled
```

at startup.

### Critical rule

When `none`:

```text
normal code path must be unchanged
```

### Tests

```text
none never injects
rate 0.0 never injects
rate 1.0 always injects
seed deterministic
normal requests unaffected when disabled
```

---

# Task M2-26 — Coordinate secure-transport interface with Member 3

This task is about **interface design**, not crypto implementation.

Member 2 should call a transport abstraction such as conceptually:

```python
result = cloud_transport.send(
    canonical_measurement,
    request_id=...
)
```

Member 2 should not need to know whether it uses:

```text
baseline JSON
or
ML-KEM session + AEAD
```

### Desired abstraction

```text
Gateway processing
       ↓
CloudTransport
       ├── BaselineTransport
       └── SecureTransport
```

Member 2 can own the application interface.

Member 3 implements secure transport internals.

This keeps cryptographic logic isolated.

---

# Task M2-27 — Implement security-mode dispatch

Gateway supports two explicit modes.

### Baseline Mode

```text
SECURITY_MODE=classical
→ BaselineCloudTransport
→ POST /api/v1/baseline/measurements
→ X-Request-ID
```

### Modernized Mode

```text
SECURITY_MODE=mlkem
→ SecureCloudTransport
→ ML-KEM-768
→ HKDF-SHA-256
→ AES-256-GCM
→ POST /api/v1/secure/measurements
```

Member 2 wires the selected transport but does not implement Member 3's crypto internals.

Protocol version `1` is fail-closed only:

```text
SECURITY_MODE=mlkem
+ secure transport failure
→ classified failure upstream
→ NO automatic baseline POST
```

Switching to Baseline Mode requires explicit configuration/operator action.

---

# Task M2-28 — Preserve Legacy interface after PQC modernization

This is one of Member 2's most important project-level responsibilities.

After Member 3 integrates ML-KEM, confirm the Legacy contract remains:

```http
POST /api/v1/measurements
```

with exactly the same payload.

Legacy Device must not know:

```text
SECURITY_MODE
session_id
ML-KEM
nonce
Cloud public key
```

### Compatibility test

Run same Legacy Device against:

```text
Gateway SECURITY_MODE=classical
```

then:

```text
Gateway SECURITY_MODE=mlkem
```

without changing Legacy code.

Both should work.

This directly supports the project's legacy migration requirement.

---

# Task M2-29 — Implement Gateway `/health`

`/health` should answer:

```text
Is this Gateway process alive?
```

Keep it simple.

Example:

```json
{
  "status": "ok"
}
```

It should not depend on Cloud being available.

Otherwise a Cloud outage would make the Gateway appear dead rather than unready.

---

# Task M2-30 — Implement Gateway `/ready`

`/ready` should answer:

```text
Can Gateway perform useful work?
```

Potential response:

```json
{
  "status": "ready",
  "security_mode": "mlkem",
  "cloud": "reachable"
}
```

Member 2 should coordinate the secure-specific readiness check with Member 3.

### Important

Do not expose:

```text
session keys
public/private key contents
shared secret
detailed crypto state
```

---

# Task M2-31 — Define readiness behavior

`/ready` answers: “Can the Gateway perform useful work in the configured mode?”

Check valid configuration and required initialized dependencies; when `SECURITY_MODE=mlkem`, the secure transport subsystem must be initialized.

### Important

Readiness must **not** require an already active ML-KEM session. Sessions are established lazily.

```text
Gateway alive
SECURITY_MODE=mlkem
secure transport initialized
no active session yet
→ may still be ready
```

If Cloud is unavailable, readiness may be false according to the team's chosen connectivity policy, but liveness remains separate.

Do not expose key material or detailed crypto state. Document and test the exact semantics with Members 3 and 5.

---

# Task M2-32 — Gateway request logging

Member 2 owns application-layer log events.

Recommended:

```text
gateway_starting
gateway_ready

legacy_measurement_received
legacy_validation_failed

sequence_duplicate_detected
sequence_out_of_order_detected
sequence_gap_detected

canonical_measurement_created

cloud_delivery_started
cloud_delivery_retry
cloud_delivery_succeeded
cloud_delivery_failed

failure_injected

gateway_shutting_down
```

### Common fields

```text
request_id
device_id
sequence_number
gateway_id
status_code
attempt
```

### Crypto-specific events

Member 3 owns:

```text
mlkem_handshake_started
session_created
encryption_failed
```

but both members should follow the same logging conventions.

---

# Task M2-33 — Logging privacy/security review

Do not log:

```text
entire environment
credentials
future Cloud token
ML-KEM shared secret
session key
private key
```

Also consider whether full sensor payload logging is necessary.

Usually IDs and sequence values are enough for tracing.

---

# Task M2-34 — Gateway application metrics

Member 2 owns or contributes these metrics:

```text
gateway_measurements_received_total

gateway_measurements_accepted_total

gateway_measurements_rejected_total

gateway_duplicate_measurements_total

gateway_out_of_order_measurements_total

gateway_sequence_gaps_total

gateway_cloud_requests_total

gateway_cloud_retries_total

gateway_cloud_failures_total

gateway_cloud_request_duration_seconds

gateway_injected_failures_total
```

Member 3 adds crypto-related metrics.

Member 5 helps standardize/export them.

---

# Task M2-35 — Metric-label safety

Member 2 must avoid:

```text
request_id as metric label
device_id if unbounded fleet scale matters
session_id
timestamps
```

because those create high-cardinality metrics.

Prefer labels such as:

```text
result
failure_type
security_mode
status_class
```

---

# Task M2-36 — Implement request-size protections

The shared protocol freezes the Legacy request-body limit at:

```text
<= 16 KiB
```

Enforce it before unnecessary parsing/processing where practical.

Tests:

```text
normal payload accepted
payload within limit accepted
payload above 16 KiB rejected
oversized payload never reaches Cloud transport
```

Use the framework's appropriate client-error response and document it consistently if the precise oversized-body status is framework-specific.

---

# Task M2-37 — Graceful Gateway shutdown

Gateway must support:

```text
Ctrl+C
SIGTERM
Docker stop
```

Member 2 owns application lifecycle while Member 3 clears secure sessions and Member 5 verifies Docker behavior.

Expected:

```text
SIGTERM
 ↓
stop accepting new requests
 ↓
close Cloud HTTP client
 ↓
Member 3 clears sessions
 ↓
flush/finish safe work
 ↓
exit
```

No ugly stack trace during normal Docker shutdown.

---

# Task M2-38 — Gateway unit-test suite

Recommended structure:

```text
edge_gateway/
└── tests/
    ├── test_config.py
    ├── test_models.py
    ├── test_validation.py
    ├── test_normalization.py
    ├── test_sequence.py
    ├── test_routes.py
    ├── test_cloud_client.py
    ├── test_failure_injector.py
    ├── test_health.py
    └── test_lifecycle.py
```

Crypto tests belong mainly to Member 3.

---

# Task M2-39 — Route tests

Test:

```text
valid request
invalid JSON
missing field
invalid temperature
invalid humidity
invalid timestamp
negative sequence
duplicate sequence
out-of-order sequence
Cloud success
Cloud failure
```

Mock transport as appropriate.

---

# Task M2-40 — Validation tests

Ensure boundaries are covered exactly:

```text
temperature -40 valid
temperature 85 valid
temperature -40.01 invalid
temperature 85.01 invalid

humidity 0 valid
humidity 100 valid
humidity -0.1 invalid
humidity 100.1 invalid
```

Boundary testing is important because AI-generated validation code often makes off-by-one/range mistakes.

---

# Task M2-41 — Sequence tests

Required:

```text
first message
increment by one
gap
duplicate
older/out-of-order
two independent devices
state after rejected schema/domain input
state after duplicate rejection
state after out-of-order rejection
state after Cloud failure
concurrent same-device requests
```

Frozen expectations:

```text
valid seq=10 accepted
→ last_sequence becomes 10

Cloud forwarding then fails
→ last_sequence remains 10
```

Malformed/domain-invalid input does not change sequence state. Duplicate/out-of-order requests return `409` and do not move state backward. A gap is accepted and advances state.

---

# Task M2-42 — Decide sequence-state timing explicitly

This is no longer a design decision. It is an implementation/verification task.

Frozen policy:

> Track the last valid sequence observed by the Gateway after schema/domain validation and sequence-policy acceptance, regardless of later Cloud delivery success.

```text
message seq=10
↓
validation succeeds
↓
sequence policy accepts
↓
commit last_sequence=10
↓
Cloud forwarding
```

If Cloud forwarding fails, `last_sequence` remains `10`.

Known consequence:

```text
Legacy retries same seq=10
→ Gateway may return 409 duplicate
```

Member 2 must implement, document, and test this exact ordering.

---

# Task M2-43 — Legacy↔Gateway contract tests

**Shared with Member 1.**

Required:

```text
valid fixture → accepted when downstream succeeds
invalid JSON → 400
invalid_temperature → 422
invalid_humidity → 422
invalid_timestamp → 422
missing required field → 422 Unprocessable Entity
duplicate sequence → 409 DUPLICATE_SEQUENCE
out-of-order sequence → 409 OUT_OF_ORDER_SEQUENCE
sequence gap → accepted + log/metric
```

Also verify `400/409/422` are non-retryable for Member 1's Legacy client.

No direct package imports across components.

---

# Task M2-44 — Gateway↔Cloud baseline contract tests

**Shared with Member 4.**

Required:

```text
Gateway CanonicalMeasurement JSON → Cloud accepts
field names identical
timestamp formats compatible
gateway_id present
request_id absent from canonical JSON
X-Request-ID present and propagated
Cloud maps received_at → gateway_received_at
unknown/missing field behavior understood
```

No Gateway application-model import should be required inside Cloud.

---

# Task M2-45 — Support secure Gateway↔Cloud contract tests

After Member 3 implements secure transport, Member 2 verifies application behavior around it.

```text
secure transport success → Legacy 202
409 SESSION_INVALID → one bounded re-establishment/retry inside SecureTransport
409 SESSION_EXPIRED → same
permanent secure rejection → no blind retry
Cloud 500/502/503/504 or timeout → bounded transport retry
ordinary ambiguous secure retry → resend same already-built SecureEnvelope
ML-KEM/session establishment failure → fail closed → normally Legacy 503 → no baseline call
```

Also verify SecureTransport receives `CanonicalMeasurement` and `request_id` as separate inputs and does not modify canonical business data.

---

# Task M2-46 — Implement failure propagation correctly

Member 2 must ensure internal errors are translated properly.

Example:

```text
Legacy valid
 ↓
Cloud storage unavailable
 ↓
Cloud 503
 ↓
Gateway retries
 ↓
all retries fail
 ↓
Gateway 503
 ↓
Legacy retries according to its own policy
```

This is a multi-level retry chain, so bounded retries are important.

---

# Task M2-47 — Avoid retry amplification problems

If:

```text
Legacy performs 3 attempts
```

and each Gateway attempt performs:

```text
3 Cloud attempts
```

then one Legacy measurement could trigger:

```text
9 Cloud requests
```

This is acceptable in a small simulation but should be recognized.

Member 2 should document this operational consequence.

Do not introduce a complex queue solely to fix it.

---

# Task M2-48 — Verify failure paths do not bypass validation

Failure injection must not accidentally let invalid payloads reach secure transport.

Correct:

```text
Legacy invalid payload
 ↓
Gateway validation fails
 ↓
stop
```

Not:

```text
Legacy invalid
 ↓
failure hook
 ↓
somehow bypass validation
 ↓
Cloud
```

Test this explicitly.

---

# Task M2-49 — Dockerize Gateway

Member 2 can own:

```text
edge_gateway/Dockerfile
```

while Member 5 owns overall Compose.

Requirements:

```text
correct Python version
uv-compatible installation
service listens on configured host/port
SIGTERM works
no development-only hot reload in final deployment
```

Gateway does expose:

```text
8000
```

inside the Compose network and potentially to host for testing.

---

# Task M2-50 — Docker Compose integration

**Shared with Member 5.**

Gateway should resolve `cloud-service` through Docker internal DNS:

```text
CLOUD_URL=http://cloud-service:9000
```

Legacy reaches:

```text
http://edge-gateway:8000
```

At repository-root Compose level, use service-scoped source variables such as:

```text
GATEWAY_FAILURE_MODE
GATEWAY_FAILURE_RATE
GATEWAY_FAILURE_SEED
```

and map them into the Gateway process's internal `FAILURE_MODE`, `FAILURE_RATE`, and `FAILURE_SEED` values. This keeps Gateway fault settings independent from Legacy and Cloud.

Verify both `SECURITY_MODE=classical` and `SECURITY_MODE=mlkem`.

---

# Task M2-51 — Baseline container test

Before ML-KEM:

```text
docker compose up
```

then:

```text
Legacy
→ Gateway
→ Cloud
→ database
```

must work in:

```text
SECURITY_MODE=classical
```

This is a project milestone.

---

# Task M2-52 — Modernized container regression test

After Member 3's work:

```text
SECURITY_MODE=mlkem
```

same Gateway route:

```text
POST /api/v1/measurements
```

must work unchanged from Member 1's perspective.

---

# Task M2-53 — AI-history workflow

Like Member 1, Member 2 must document meaningful AI-assisted development.

The slides explicitly state that AI must be used to create the code, generated code must be manually evaluated continuously, prompts must be included in technical documentation, and AI use must be reported.

Example tasks:

```text
Implement Gateway measurement validation

Implement canonical normalization

Implement sequence tracker

Implement baseline Cloud client

Implement Gateway failure injection
```

Each should follow:

```text
start
 ↓
AI interactions
 ↓
implementation complete
 ↓
tests/checks
 ↓
output
 ↓
human review
 ↓
accepted / modified / rejected
 ↓
revision if needed
 ↓
verify
```

Use the actual `ai-history` CLI available in the repository.

---

# Task M2-54 — Manual review of AI-generated Gateway code

Gateway code is particularly important because it is a trust boundary.

Member 2 should review:

### Correctness

```text
schema matches protocol
validation ranges correct
canonical mapping correct
sequence semantics correct
HTTP status mapping correct
```

### Reliability

```text
timeout exists
retry bounded
no retry on permanent errors
no crash on Cloud outage
graceful shutdown
```

### Maintainability

```text
routes remain thin
validation separate
Cloud client separate
no giant god-class Gateway
```

### Security

```text
malformed Legacy data rejected
no stack traces externally
no silent bypass
no secret logging
no insecure fallback introduced
```

### Testability

```text
Cloud client mockable
time injectable if needed
sequence state testable
failure injection deterministic
```

---

# Gateway secure-protocol limitation to preserve

Protocol version `1` intentionally has **no dedicated cryptographic anti-replay counter/window**.

Cloud business idempotency on `(device_id, sequence_number)` prevents duplicate logical database rows but is not cryptographic replay protection.

Member 2 must not introduce a `message_counter`, replay window, `confirmation_tag`, `cloud_id` protocol field, or transcript-bound KDF through application-layer integration work.

---

# Task M2-55 — Record accepted/modified/rejected AI decisions

Good examples for Member 2 documentation:

```text
AI proposed putting Cloud forwarding directly inside route handler.
→ Modified
Reason:
transport should be isolated for maintainability/testability.
```

```text
AI proposed retrying every HTTP status.
→ Rejected
Reason:
retrying 422 repeatedly is useless.
```

```text
AI proposed silently dropping duplicate messages and returning 202.
→ Modified/Rejected
Reason:
our protocol specifies explicit duplicate handling.
```

```text
AI proposed adding ML-KEM logic directly to the request route.
→ Rejected
Reason:
crypto belongs in Member 3's isolated secure transport/session layer.
```

These examples directly satisfy the course's expectation that the group explain what was accepted, modified, or rejected and why.

---

# Task M2-56 — Gateway documentation contribution

Member 2 should maintain the application portions of:

```text
docs/architecture/edge-gateway.md
```

and relevant parts of:

```text
docs/architecture/protocol-specification.md
```

Documentation should include:

```text
Legacy API
validation rules
canonical model
sequence behavior
request IDs
baseline Cloud transport
retry rules
failure injection
health/readiness
logging
metrics
known limitations
```

Protocol changes must be team-approved before documentation/code changes.

---

# Task M2-57 — Document Gateway application technical debt

Expected items:

|Technical debt|Impact|Future improvement|
|---|---|---|
|In-memory sequence state|lost on restart|persistent lightweight state|
|No message buffer|Cloud outage propagates to Legacy|store-and-forward queue|
|Synchronous forwarding|Legacy latency depends on Cloud|asynchronous queue|
|Simple retry policy|may amplify failures|jitter/backoff/circuit breaker|
|No strong Legacy authentication|spoofed devices possible|provisioned device credentials|
|Single Gateway process|no high availability|clustered gateways|
|Limited request protection|not production-grade ingress|rate limiting/authentication|

Member 2 should document these rather than hide them.

---

# Task M2-58 — Peer review Member 1's Legacy client changes

Member 2 should review Member 1 PRs affecting:

```text
Gateway URL
HTTP endpoint
request fields
serialized payload boundary
failure injection
retry semantics
status-code assumptions
```

Questions:

```text
Does Legacy send the exact schema?
Does valid Measurement remain valid internally?
Are malformed simulations introduced only after serialization?
Does Legacy avoid retrying 400/409/422?
Does it use the correct content type?
Does it add any undocumented field?
Do duplicate/out-of-order simulations affect only the outgoing payload, not internal sequence progression?
```

---

# Task M2-59 — Peer review Member 3's secure transport integration

Member 2 reviews secure-transport integration from the application perspective.

Questions:

```text
Does SecureTransport expose a clean abstraction?
Did crypto logic leak into route handlers?
Does Modernized Mode preserve the Legacy API?
Does transport accept CanonicalMeasurement + request_id separately?
Does request_id remain outside CanonicalMeasurement?
Are 409 SESSION_INVALID / SESSION_EXPIRED handled as bounded session recovery?
Are permanent secure failures prevented from blind retry?
Does SECURITY_MODE=mlkem fail closed?
Can any crypto failure accidentally call the baseline endpoint?
Does re-establishment preserve the same logical-request semantics?
Does Member 3 accidentally change canonical data?
```

---

# Task M2-60 — Peer review Member 4's Cloud contract changes

Member 2 should watch for:

```text
canonical field renames
baseline endpoint changes
status-code changes
error-contract changes
```

No Cloud PR should silently break Gateway serialization.

---

# Task M2-61 — CI regression responsibility

Any PR touching:

```text
Gateway routes
models
validation
sequence behavior
Cloud client
```

should trigger:

```text
Gateway unit tests
Legacy↔Gateway contract tests
Gateway↔Cloud baseline contract tests
relevant E2E tests
```

Member 2 should help Member 5 ensure CI includes these.

---

# Task M2-62 — Static/code-quality verification

Before each Gateway PR:

```bash
uv run pytest edge_gateway/tests
uv run ruff check edge_gateway
uv run ai-history check
```

plus repository-specific integration checks.

Member 2 should inspect:

```bash
git status
git diff
```

for:

```text
unrelated changes
debug prints
temporary files
.env
secret material
unnecessary dependencies
```

---

# Task M2-63 — Dependency review

Gateway will likely need:

```text
API framework
HTTP client
validation library
metrics library
crypto libraries via Member 3
```

Member 2 should avoid adding:

```text
Redis
Kafka
Celery
database ORM
message broker
```

without an actual requirement.

The course explicitly advises keeping the project simple.

---

# Task M2-64 — Final baseline review

Before secure modernization begins, Member 2 should confirm:

```text
[ ] Legacy endpoint stable
[ ] Validation stable
[ ] Normalization stable
[ ] Sequence behavior stable
[ ] Baseline Cloud forwarding works
[ ] Retry works
[ ] Docker works
[ ] Baseline E2E passes
[ ] Baseline measurements recorded
```

Then establish a clear baseline commit/tag.

---

# Task M2-65 — Final modernized Gateway regression

After Member 3 finishes secure transport integration, rerun the full application suite.

Check:

```text
Legacy interface unchanged
Validation unchanged
Sequence behavior unchanged
Sequence state timing unchanged
Canonical model unchanged
request_id remains separate from CanonicalMeasurement
Baseline Mode works when SECURITY_MODE=classical
Modernized Mode works when SECURITY_MODE=mlkem
Modernized Mode fails closed
no automatic baseline fallback exists
409 session recovery works
Cloud failure mapping remains correct
health/readiness still work
readiness does not require an active session
failure injection still works
```

---

# Task M2-66 — End-to-end failure scenarios

Member 2 should actively participate in these full-system tests.

### Invalid Legacy humidity

```text
Legacy payload fault → Gateway 422 → Cloud never contacted
```

### Duplicate sequence

```text
Gateway detects duplicate → 409 DUPLICATE_SEQUENCE → Cloud never contacted
```

### Out-of-order sequence

```text
Gateway detects older sequence → 409 OUT_OF_ORDER_SEQUENCE → Cloud never contacted
```

### Sequence gap

```text
10, 11, 13 → Gateway accepts 13 → gap log/metric
```

### Cloud unavailable

```text
valid Legacy request
→ Gateway commits valid observed sequence
→ bounded Cloud retries
→ exhaustion
→ 503 to Legacy
```

### Gateway processing failure

```text
valid Legacy request → injected Gateway error → 500
```

### Gateway crypto failure

```text
SECURITY_MODE=mlkem
→ ML-KEM/session failure
→ fail closed
→ no baseline POST
→ classified Legacy failure, normally 503
```

### Secure session invalid/expired

```text
Cloud 409 session error
→ one bounded session recovery
→ success or classified failure
```

### Cloud storage failure

```text
Cloud 503 → bounded Gateway retry → proper Legacy result
```

---

# Task M2-67 — Baseline vs modernized evaluation contribution

Member 2 contributes Gateway application measurements using the canonical terminology:

```text
Baseline Mode = SECURITY_MODE=classical
Modernized Mode = SECURITY_MODE=mlkem
```

| Measurement | Baseline Mode | Modernized Mode |
|---|---:|---:|
| Gateway total request latency | | |
| Gateway→Cloud latency | | |
| First secure request latency | N/A | |
| Subsequent secure request latency | N/A | |
| Gateway→Cloud payload size | | |
| Retry behavior | | |
| Validation behavior | same | same |
| Legacy API | same | same |

Use equivalent workloads. Report first secure-message latency separately because it includes session establishment.

---

# Task M2-68 — Document modernization invariants

Member 2 should help prove modernization did **not** change:

```text
Legacy endpoint
Legacy request schema
Legacy field meanings
Gateway validation rules
sequence semantics
CanonicalMeasurement schema
```

`request_id` remains separate request/transport context.

Baseline:

```text
CanonicalMeasurement + X-Request-ID
→ /api/v1/baseline/measurements
```

Modernized:

```text
CanonicalMeasurement + request_id
→ SecureTransport
→ ML-KEM-768 / HKDF-SHA-256 / AES-256-GCM
→ /api/v1/secure/measurements
```

Only the Gateway→Cloud transport/security boundary changes.

---

# Task M2-69 — Final Gateway application quality pass

Before freeze, verify:

```text
Configuration
✓ classical | mlkem
✓ PQC_FAILURE_POLICY=fail_closed only

Legacy API
✓

Validation
✓ 400 vs 422 behavior documented

Normalization
✓ CanonicalMeasurement unchanged
✓ request_id not embedded in canonical data

Sequence handling
✓ duplicate/out-of-order = 409
✓ gap accepted
✓ last valid observed sequence committed before Cloud delivery

Request tracing
✓ Baseline X-Request-ID
✓ Secure request_id context

Baseline Cloud transport
✓

Secure transport integration
✓ bounded 409 recovery
✓ fail closed
✓ no automatic baseline fallback

Failure injection
✓

Retry handling
✓ transport retry separated from session recovery

Health/readiness
✓ no active session required merely to be ready

Logging
✓

Metrics
✓

Request-size limit
✓ <= 16 KiB Legacy body

Docker
✓

Tests
✓

Documentation
✓

AI history
✓
```

Remove debug prints, dead code, stale alternative sequence policies, stale fallback branches, unused configuration/dependencies, and unfinished TODOs.

---

# Recommended Member 2 task order

I would assign work in this exact sequence:

```text
M2-00  Review/freeze Gateway boundaries

M2-01  Gateway configuration

M2-02  Application skeleton

M2-03  Legacy request model

M2-04  Schema validation

M2-05  Domain validation

M2-06  Error model

M2-07  Canonical model

M2-08  Normalization

M2-09  Request/correlation ID

M2-10  Sequence tracker

M2-11  Sequence-state behavior

M2-12  Legacy measurement route

M2-13  Baseline Cloud client

M2-14  Cloud retry policy

M2-15  Response mapping

M2-16  Baseline Gateway↔Cloud integration

M2-17  Baseline E2E support

M2-18  Baseline measurements

M2-19  Failure-injection framework

M2-20  Processing-error injection

M2-21  Processing-delay injection

M2-22  Cloud-timeout injection

M2-23  Cloud-unavailable injection

M2-24  Drop-message injection

M2-25  Failure-injection safety review

M2-26  Secure transport abstraction with Member 3

M2-27  Security-mode dispatch

M2-28  Legacy compatibility regression

M2-29  /health

M2-30  /ready

M2-31  Readiness behavior

M2-32  Application logging

M2-33  Logging security review

M2-34  Gateway application metrics

M2-35  Metric-label review

M2-36  Request-size protection

M2-37  Graceful shutdown

M2-38  Complete unit tests

M2-39  Route tests

M2-40  Validation boundary tests

M2-41  Sequence tests

M2-42  Frozen sequence-state timing implementation/verification

M2-43  Legacy contract tests

M2-44  Baseline Cloud contract tests

M2-45  Secure transport integration tests

M2-46  Failure propagation tests

M2-47  Retry amplification review

M2-48  Validation-bypass tests

M2-49  Dockerfile

M2-50  Compose integration

M2-51  Baseline container test

M2-52  Modernized container regression

M2-53  AI-history maintenance

M2-54  Human review of AI code

M2-55  AI decision documentation

M2-56  Gateway documentation

M2-57  Technical-debt documentation

M2-58  Review Member 1 interface PRs

M2-59  Review Member 3 integration PRs

M2-60  Review Cloud contract PRs

M2-61  CI regression coordination

M2-62  Static quality checks

M2-63  Dependency review

M2-64  Baseline freeze

M2-65  Modernized Gateway regression

M2-66  E2E failure scenarios

M2-67  Evaluation contribution

M2-68  Modernization compatibility evidence

M2-69  Final quality pass
```

# Suggested PR breakdown for Member 2

Do not implement all of this in one branch.

|PR|Scope|
|---|---|
|PR 1|Gateway config + application skeleton|
|PR 2|Legacy model + validation + error handling|
|PR 3|Canonical normalization + request ID|
|PR 4|Sequence tracking + frozen state timing|
|PR 5|Baseline Cloud client + X-Request-ID + retry|
|PR 6|Legacy route + baseline integration|
|PR 7|Gateway application failure injection|
|PR 8|Health/readiness + logging|
|PR 9|Metrics + operations refinements|
|PR 10|Secure transport integration + fail-closed/session-recovery wiring|
|PR 11|Gateway test-suite hardening|
|PR 12|Docker + E2E regression|
|PR 13|Evaluation/documentation cleanup|

This makes human review realistic and preserves useful AI-history boundaries.

# Member 2 milestone gates

## Gate A — Gateway accepts Legacy traffic

Required:

```text
configuration
app starts
Legacy route
validation
normalization
sequence tracker
```

No Cloud required yet.

## Gate B — Baseline Gateway complete

Required:

```text
Cloud client
retry
response mapping
baseline Cloud integration
```

## Gate C — Baseline system complete

Required:

```text
Legacy
→ Gateway
→ Cloud
→ storage
```

fully working.

## Gate D — Gateway operations complete

Required:

```text
failure injection
health
readiness
logging
metrics
Docker
```

## Gate E — Secure transport integrated

Required:

```text
Member 3 secure transport
security-mode switching
Legacy compatibility maintained
secure failures mapped correctly
```

## Gate F — Final Gateway complete

Required:

```text
all tests
documentation
AI review records
baseline vs modernized evaluation
technical debt
peer reviews
CI
```

# Final Definition of Done for Member 2

Member 2's work is complete only when:

```text
[ ] Gateway starts from validated configuration.

[ ] Legacy Device contract is implemented exactly.

[ ] Invalid JSON is rejected safely.

[ ] Invalid measurements are rejected before Cloud communication.

[ ] Temperature and humidity boundaries are correct.

[ ] UTC timestamp validation is correct.

[ ] Canonical transformation preserves measurement values.

[ ] Gateway adds received_at and gateway_id correctly.

[ ] Every accepted Legacy request receives a correlation/request ID.

[ ] `request_id` is not part of `CanonicalMeasurement`.

[ ] Baseline Cloud requests propagate `request_id` through `X-Request-ID`.

[ ] Sequence state is tracked independently per device.

[ ] Duplicate behavior is explicit and tested.

[ ] Out-of-order behavior is explicit and tested.

[ ] Sequence gaps are accepted/logged according to design.

[ ] Sequence state means the last valid sequence observed by Gateway.

[ ] Sequence state is committed before downstream Cloud delivery.

[ ] Cloud failure does not roll sequence state back.

[ ] Baseline Gateway→Cloud transport works.

[ ] Cloud requests use explicit timeout.

[ ] Retry behavior is bounded.

[ ] Permanent failures are not blindly retried.

[ ] Cloud failure maps predictably to Legacy response.

[ ] Baseline E2E passes.

[ ] Baseline evidence has been collected.

[ ] Gateway failure injection works.

[ ] Failure injection defaults to disabled.

[ ] Failure injection is deterministic when seeded.

[ ] Drop-message behavior does not pretend success.

[ ] Gateway application does not contain ML-KEM internals.

[ ] Member 3's secure transport plugs into a clean interface.

[ ] Baseline Mode (`classical`) and Modernized Mode (`mlkem`) are clearly separated.

[ ] Protocol v1 accepts `PQC_FAILURE_POLICY=fail_closed` only.

[ ] Modernized Mode never automatically calls the baseline endpoint after crypto/session failure.

[ ] `409 SESSION_INVALID` / `SESSION_EXPIRED` use bounded secure-session recovery.

[ ] Legacy API remains unchanged after modernization.

[ ] /health works.

[ ] /ready works.

[ ] Readiness does not require an already-active secure session.

[ ] Health endpoints expose no secrets.

[ ] Gateway application logs are structured/useful.

[ ] Gateway metrics are meaningful.

[ ] Metric labels avoid unnecessary high cardinality.

[ ] Graceful shutdown works.

[ ] Gateway Docker image works.

[ ] Legacy↔Gateway contract tests pass.

[ ] Gateway↔Cloud baseline contract tests pass.

[ ] Baseline contract tests verify `X-Request-ID` and `received_at → gateway_received_at` mapping.

[ ] Secure integration tests pass after Member 3 work.

[ ] Secure integration verifies fail-closed behavior and no automatic baseline downgrade.

[ ] Full failure propagation tests pass.

[ ] AI-generated code was manually reviewed.

[ ] Significant prompts/outputs/decisions are in AI history.

[ ] Accepted/modified/rejected AI decisions are documented.

[ ] Gateway technical debt is documented.

[ ] Relevant Member 1, 3 and 4 PRs received interface review.

[ ] Ruff/static checks pass.

[ ] Unit tests pass.

[ ] Integration tests pass.

[ ] AI-history validation passes.

[ ] CI passes.

[ ] Final PR has teammate review.
```
