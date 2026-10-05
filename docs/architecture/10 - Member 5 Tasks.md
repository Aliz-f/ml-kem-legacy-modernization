# Member 5 — Integration, DevOps, Observability & System Testing Owner

## Overall mission

Member 5 is responsible for making sure the pieces built by Members 1–4 actually become **one reproducible, testable, observable system**.

Their primary ownership is:

```text
Legacy Device
     │
     ▼
Edge Gateway
     │
     ▼
Cloud Service
     │
     ▼
SQLite
```

plus the infrastructure around them:

```text
                 ┌───────────────────┐
                 │      CI/CD        │
                 └─────────┬─────────┘
                           │
                           ▼
┌────────────┐     ┌────────────┐     ┌────────────┐
│   Legacy   │ ──> │  Gateway   │ ──> │   Cloud    │
└────────────┘     └────────────┘     └─────┬──────┘
                                            │
                                            ▼
                                          SQLite

       │                  │                   │
       └──────── Logging / Metrics / Health ─┘

                           │
                           ▼
                  Integration / E2E Tests
```

Member 5 does **not** primarily own:

```text
Legacy data-generation logic
Gateway validation logic
ML-KEM algorithm integration internals
Cloud storage business logic
```

But Member 5 is responsible for proving that all of those components work together.

---

# Member 5 final deliverables

|Deliverable|Expected result|
|---|---|
|Repository-wide development tooling|reproducible project environment|
|Docker Compose|full system starts consistently|
|CI pipeline|automated validation on PR/push|
|Integration-test framework|component contracts tested|
|E2E tests|Legacy→Gateway→Cloud verified|
|Failure-test orchestration|controlled negative scenarios|
|Health integration|service health visible|
|Metrics integration|Gateway/Cloud metrics usable|
|Logging conventions|end-to-end traceability|
|Request correlation|Gateway↔Cloud debugging|
|Baseline benchmarking|initial system evidence|
|Modernized Mode benchmarking|ML-KEM comparison evidence|
|Security regression tests|failure/tampering/no-secret checks|
|AI-history CI validation|required AI records stay valid|
|Test-environment deployment|reproducible test deployment|
|Release/readiness checklist|peer-review submission ready|
|Technical-debt register|project-wide limitations|
|Evaluation evidence|report/presentation data|
|Documentation|runbook/deployment/testing guidance|

---

# Task M5-00 — Review all component contracts


Before infrastructure work, Member 5 should review the corrected component designs and the shared protocol specification.

The goal is not to redesign them.

The goal is to understand and preserve the frozen cross-component contract.

Review:

```text
docs/architecture/
├── legacy-device.md
├── edge-gateway.md
├── cloud-service.md
└── protocol-specification.md
```

Key items Member 5 must know:

```text
Legacy → Gateway:
POST /api/v1/measurements

Baseline Gateway → Cloud:
POST /api/v1/baseline/measurements
X-Request-ID

Modernized Gateway → Cloud:
GET  /api/v1/crypto/public-key
POST /api/v1/crypto/sessions
POST /api/v1/secure/measurements

protocol_version = "1"

ML-KEM-768

HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32
→ one session_key

session response:
protocol_version
session_id
status
expires_at

AES-256-GCM
12-byte nonce

SecureEnvelope:
protocol_version
gateway_id
session_id
request_id
nonce
ciphertext

AAD:
protocol_version
gateway_id
session_id
request_id

Ordinary retry after ambiguous/lost response:
resend the SAME already-built SecureEnvelope
same request_id
same session_id
same nonce
same ciphertext
same AAD

Session errors:
409 SESSION_INVALID
409 SESSION_EXPIRED

Session recovery:
establish one replacement session
rebuild secure envelope under replacement session
retry same logical request once

Replay:
no dedicated cryptographic anti-replay counter/window in protocol v1
business idempotency on (device_id, sequence_number)
prevents duplicate logical DB rows

Security policy:
fail closed
no runtime plaintext fallback
```

Also review:

```text
health endpoints
readiness semantics
metrics endpoints
ports
environment variables
failure modes
response codes
storage mapping
idempotency
public-key trust limitation
ML-KEM implicit-rejection caveat
```

### Acceptance criteria

```text
[ ] Member 1 interface understood
[ ] Member 2 interface understood
[ ] Member 3 secure protocol understood at integration level
[ ] Member 4 Cloud API understood
[ ] Frozen crypto/session contract understood
[ ] fixed HKDF info contract understood
[ ] four-field AAD understood
[ ] same-envelope ordinary retransmission semantics understood
[ ] no dedicated crypto anti-replay counter/window is understood as technical debt
[ ] Docker networking requirements identified
[ ] Integration dependencies documented
[ ] No infrastructure assumption changes protocol semantics
```

---

# Task M5-01 — Maintain root `uv` workspace

Member 5 should help ensure repository-wide Python dependency management is consistent.

Expected root structure:

```text
pyproject.toml
uv.lock

legacy_system/
edge_gateway/
cloud_service/
```

Responsibilities:

```text
verify workspace members
verify compatible Python version
verify uv.lock committed
ensure CI uses frozen lock
prevent requirements.txt duplication
prevent .venv commits
```

### Verification

```bash
uv sync
```

must work from a fresh clone.

### Definition of Done

```text
[ ] Workspace valid
[ ] All components install
[ ] Lockfile current
[ ] No duplicated dependency system
```

---

# Task M5-02 — Standardize repository quality tools

Member 5 should coordinate project-wide tools such as:

```text
pytest
ruff
ai-history
```

Potentially:

```text
coverage
```

if the team decides it provides useful evidence.

The goal is one predictable command set.

Example:

```bash
uv run ruff check .
uv run pytest
uv run ai-history check
```

---

# Task M5-03 — Protect repository hygiene

Member 5 should review `.gitignore`.

At minimum exclude:

```text
.venv/
__pycache__/
*.pyc
.env
local database files if not intentionally committed
coverage output
IDE temporary files
runtime logs
```

But keep:

```text
.env.example
uv.lock
test fixtures
documentation
```

---

# Task M5-04 — Maintain `.env.example`


Create one safe root configuration example containing **no secrets**.

The root `.env.example` must use **service-scoped source variables** for failure injection so one root variable cannot accidentally control all three services.

Recommended root example:

```dotenv
# Shared Gateway/Cloud protocol defaults
SECURITY_MODE=classical
SESSION_TTL_SECONDS=300

# Legacy Device
DEVICE_ID=sensor-001
GATEWAY_URL=http://edge-gateway:8000
SEND_INTERVAL_SECONDS=5
REQUEST_TIMEOUT_SECONDS=3
MAX_RETRIES=2

LEGACY_FAILURE_MODE=none
LEGACY_FAILURE_RATE=0.0
LEGACY_FAILURE_SEED=

# Edge Gateway
GATEWAY_ID=gateway-001
CLOUD_URL=http://cloud-service:9000
CLOUD_TIMEOUT_SECONDS=3
CLOUD_MAX_RETRIES=2
PQC_FAILURE_POLICY=fail_closed

GATEWAY_FAILURE_MODE=none
GATEWAY_FAILURE_RATE=0.0
GATEWAY_FAILURE_SEED=

# Cloud Service
CLOUD_ID=cloud-001
DATABASE_URL=sqlite:///data/cloud.db

CLOUD_FAILURE_MODE=none
CLOUD_FAILURE_RATE=0.0
CLOUD_FAILURE_SEED=
CLOUD_FAILURE_DELAY_SECONDS=2

# Shared non-secret defaults
LOG_LEVEL=INFO
```

Docker Compose maps each service-scoped root failure value into the generic variable names expected **inside** the corresponding process.

Conceptually:

```yaml
legacy-device:
  environment:
    FAILURE_MODE: ${LEGACY_FAILURE_MODE}
    FAILURE_RATE: ${LEGACY_FAILURE_RATE}
    FAILURE_SEED: ${LEGACY_FAILURE_SEED}

edge-gateway:
  environment:
    FAILURE_MODE: ${GATEWAY_FAILURE_MODE}
    FAILURE_RATE: ${GATEWAY_FAILURE_RATE}
    FAILURE_SEED: ${GATEWAY_FAILURE_SEED}

cloud-service:
  environment:
    FAILURE_MODE: ${CLOUD_FAILURE_MODE}
    FAILURE_RATE: ${CLOUD_FAILURE_RATE}
    FAILURE_SEED: ${CLOUD_FAILURE_SEED}
    FAILURE_DELAY_SECONDS: ${CLOUD_FAILURE_DELAY_SECONDS}
```

`SECURITY_MODE` and `SESSION_TTL_SECONDS` are defined once in the root example because Gateway and Cloud are expected to use the same values in this project.

Member 5 should ensure `.env.example`, Docker Compose, and the real configuration models stay synchronized.

### Definition of Done

```text
[ ] No secrets in .env.example
[ ] SECURITY_MODE appears once in the root example
[ ] SESSION_TTL_SECONDS appears once in the root example
[ ] Legacy failure variables are service-scoped
[ ] Gateway failure variables are service-scoped
[ ] Cloud failure variables are service-scoped
[ ] FAILURE_SEED is independently configurable per service
[ ] Cloud delay injection defaults to 2 seconds
[ ] Compose maps service-scoped root values to internal generic names
[ ] No duplicated global FAILURE_MODE/FAILURE_RATE block remains
```

---

# Task M5-05 — Design Docker Compose topology

Primary artifact:

```text
docker-compose.yml
```

Expected services:

```text
legacy-device
edge-gateway
cloud-service
```

Architecture:

```text
legacy-device
    │
    ▼
edge-gateway:8000
    │
    ▼
cloud-service:9000
```

Cloud may use:

```text
SQLite inside Cloud container
```

or a mounted volume.

No extra database service is necessary if SQLite remains the agreed choice.

---

# Task M5-06 — Define Docker service dependencies

Compose should reflect startup dependencies sensibly.

Conceptually:

```text
Cloud starts
↓
Cloud becomes ready

Gateway starts / becomes ready
↓
Legacy starts sending
```

However, the system should also tolerate temporary dependency unavailability.

Do not depend entirely on Compose startup ordering.

For example, Gateway's retry logic should still work if Cloud is not immediately reachable.

---

# Task M5-07 — Configure Docker networking

Member 5 should confirm containers use internal DNS names:

```text
http://edge-gateway:8000

http://cloud-service:9000
```

Do not configure:

```text
localhost
```

inside containers for inter-service communication.

### Test

```text
legacy-device → edge-gateway
edge-gateway → cloud-service
```

must resolve by service name.

---

# Task M5-08 — Integrate Legacy Docker image

Member 1 builds it.

Member 5 verifies:

```text
container starts
environment injected correctly
Gateway hostname resolves
no unnecessary inbound port
SIGTERM works
```

---

# Task M5-09 — Integrate Gateway Docker image

Member 2/3 build it.

Member 5 verifies:

```text
port 8000 works
Cloud URL works
health endpoint reachable
metrics endpoint reachable
ML-KEM dependency works inside container
```

---

# Task M5-10 — Integrate Cloud Docker image

Member 4 builds it.

Member 5 verifies:

```text
port 9000 works
database initializes
ML-KEM keys initialize
health works
ready works
SQLite path behaves as designed
```

---

# Task M5-11 — Implement/document SQLite persistence strategy


Coordinate with Member 4.

Support/document two practical modes.

### Development/demo persistence

Use a named Docker volume so:

```text
Cloud container restart
→ measurement database persists
```

Advantages:

```text
useful for demonstrations
query API can show accumulated records
```

### Automated/clean test mode

Use:

```text
ephemeral database
or
fresh temporary volume
```

Advantages:

```text
deterministic tests
clean isolation
no state leakage between runs
```

The same Cloud `DATABASE_URL`/initialization design should support both workflows.

Never persist:

```text
ML-KEM private key
shared secret
session key
secure-session state
```

in the SQLite volume.

---

# Task M5-12 — Create one-command test environment

Primary target:

```bash
docker compose up
```

should start the full system.

Ideally:

```bash
docker compose down
```

should cleanly stop it.

For clean test reset, document:

```bash
docker compose down -v
```

if volumes are used.

---

# Task M5-13 — Add container health checks

Gateway:

```text
GET /health
```

Cloud:

```text
GET /health
```

Potential Compose health checks should use these endpoints.

Member 5 should verify:

```text
healthy process → healthy container
dead process → unhealthy container
```

---

# Task M5-14 — Integrate readiness checks


Use:

```text
Gateway /ready
Cloud /ready
```

to distinguish:

```text
alive
```

from:

```text
ready to perform useful work
```

Example:

```text
Cloud process alive
DB unavailable
→ /health 200
→ /ready 503
```

Important secure-mode rule:

```text
no active ML-KEM session yet
```

must **not by itself** make Gateway or Cloud unready.

Sessions are established lazily.

Member 5 should verify:

```text
Gateway /ready
→ does not require an active secure session

Cloud /ready
→ does not require an active Gateway session

Modernized Mode
→ crypto subsystem initialized and usable

Baseline Mode
→ secure session state not required
```

No readiness payload should expose secret material.

---

# Task M5-15 — Design CI workflow

Primary artifact:

```text
.github/workflows/...
```

Recommended stages:

```text
Checkout
↓
Set up Python
↓
Install uv
↓
uv sync --frozen
↓
Ruff
↓
Unit tests
↓
Contract tests
↓
Integration tests
↓
AI-history check
↓
Docker build
```

Potential E2E Docker tests can run separately if they are slower.

---

# Task M5-16 — CI dependency locking

CI should use the committed lockfile.

Prefer:

```bash
uv sync --frozen
```

so CI fails if:

```text
pyproject changed
but
uv.lock not updated
```

This improves reproducibility.

---

# Task M5-17 — CI Ruff/static checks

Run:

```bash
uv run ruff check .
```

Optionally formatting validation if team uses it.

No PR should merge with obvious static issues unless intentionally justified.

---

# Task M5-18 — CI unit-test stage

Member 5 coordinates all component suites:

```text
legacy_system/tests
edge_gateway/tests
cloud_service/tests
```

Potential command:

```bash
uv run pytest
```

or separate jobs if needed.

---

# Task M5-19 — CI contract-test stage


Contract tests should ensure independently implemented components still match the frozen protocol.

Required categories:

```text
Legacy payload
→ Gateway parser

Gateway CanonicalMeasurement
→ Cloud baseline parser

Baseline request
→ X-Request-ID propagation

Gateway session request
→ Cloud session parser

Cloud public-key response
→ Gateway parser

Cloud session response
→ Gateway parser

Gateway SecureEnvelope
→ Cloud parser

Gateway AAD bytes
== Cloud AAD bytes

Gateway HKDF parameters
== Cloud HKDF parameters
```

The contract suite should verify key frozen values:

```text
protocol_version="1"
ML-KEM-768 identifier
key_id
Base64URL fields

HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32

12-byte nonce

SecureEnvelope has no message counter

AAD contains exactly:
protocol_version
gateway_id
session_id
request_id

409 SESSION_INVALID
409 SESSION_EXPIRED

received_at → gateway_received_at mapping
```

Components should not import one another's internal application models merely to make these tests pass.

---

# Task M5-20 — CI integration-test stage


Integration tests should include:

```text
Legacy ↔ Gateway

Gateway ↔ Cloud Baseline Mode

Gateway ↔ Cloud ML-KEM-768 session establishment

Gateway ↔ Cloud fixed HKDF interoperability

Gateway ↔ Cloud AES-256-GCM SecureEnvelope

four-field AAD interoperability

409 session recovery

same-envelope retry after ambiguous response

business idempotency after retransmission

fail-closed/no-baseline-downgrade behavior
```

These may use real service instances or test application servers depending on design.

The important point is that the test crosses real component boundaries and does not bypass protocol serialization/parsing with internal shortcuts.

---

# Task M5-21 — CI E2E stage


Eventually add full:

```text
Legacy
→ Gateway
→ Cloud
→ SQLite
```

tests.

Two required modes:

```text
Baseline Mode
SECURITY_MODE=classical
```

and:

```text
Modernized Mode
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
```

The same Legacy Device contract must work in both modes.

E2E does not necessarily need to run on every tiny local invocation, but it should run before merge/release or on a reliable CI path chosen by the team.

---

# Task M5-22 — Integrate `ai-history check` into CI

The course requires AI-generated code, prompts, manual evaluation, and reporting of decisions.

CI should run:

```bash
uv run ai-history check
```

to detect malformed/incomplete history records.

Member 5 should not pretend this proves every prompt was recorded; it only validates the repository's tracked history structure.

---

# Task M5-23 — Maintain AI-history tooling compatibility

If the team extends the CLI with:

```text
interaction
```

Member 5 should help ensure:

```text
CLI works in clean environment
documentation matches commands
CI validation understands current format
```

Do not silently break existing history files.

---

# Task M5-24 — Design integration-test directory

Recommended root structure:

```text
tests/
└── integration/
    ├── test_legacy_gateway.py
    ├── test_gateway_cloud_baseline.py
    ├── test_gateway_cloud_secure.py
    ├── test_failure_paths.py
    └── test_end_to_end.py
```

Component unit tests remain inside each component.

---

# Task M5-25 — Manage shared test fixtures

Suggested:

```text
tests/
└── fixtures/
    ├── valid_legacy_measurement.json
    ├── invalid_humidity_measurement.json
    ├── canonical_measurement.json
    └── ...
```

Coordinate fixture ownership with Members 1–4.

Do not include real secret material.

Crypto keys should normally be generated during tests.

---

# Task M5-26 — Baseline Legacy→Gateway integration


Coordinate Members 1 and 2.

Required:

```text
valid Legacy measurement
→ Gateway accepts

malformed/unparseable JSON/body
→ Gateway 400

invalid temperature
→ Gateway 422

invalid humidity
→ Gateway 422

missing required field in otherwise valid JSON
→ Gateway 422

wrong field type in otherwise valid JSON
→ Gateway 422

invalid timestamp
→ Gateway 422

duplicate sequence
→ Gateway 409

out-of-order sequence
→ Gateway 409
```

These expectations must use the real HTTP boundary, not internal Gateway model shortcuts.

---

# Task M5-27 — Baseline Gateway→Cloud integration


Coordinate Members 2 and 4.

Required:

```text
CanonicalMeasurement
+ X-Request-ID
→ POST /api/v1/baseline/measurements
→ Cloud validation
→ idempotent storage
```

Verify exact field preservation and mapping:

```text
CanonicalMeasurement.received_at
→ StoredMeasurement.gateway_received_at
```

Also verify:

```text
request_id is NOT added to CanonicalMeasurement
X-Request-ID is visible to Cloud logs/tracing
cloud_received_at is added by Cloud
record_id is created
```

---

# Task M5-28 — Full baseline E2E test

This is the first major whole-system milestone.

Test:

```text
1. Start Cloud
2. Start Gateway in Baseline Mode
3. Start/send deterministic Legacy measurement
4. Gateway validates
5. Gateway forwards
6. Cloud stores
7. Query Cloud
8. Compare stored data with original
```

Example measurement:

```json
{
  "device_id": "sensor-test",
  "temperature_c": 22.5,
  "humidity_pct": 44.0,
  "timestamp": "2026-09-21T12:00:00Z",
  "sequence_number": 1
}
```

---

# Task M5-29 — Baseline E2E assertions


Assert:

```text
device_id preserved
temperature preserved
humidity preserved
sequence preserved

Legacy timestamp
=
Cloud measured_at

Gateway canonical received_at exists

Cloud stored gateway_received_at
=
Gateway canonical received_at

Cloud cloud_received_at exists

gateway_id correct

X-Request-ID correlation reaches Cloud logs/tracing

request_id is not part of CanonicalMeasurement
```

This becomes the baseline reference.

---

# Task M5-30 — Freeze baseline milestone

Once baseline works, Member 5 should coordinate a clear commit/tag/milestone.

For example:

```text
baseline-classical-complete
```

Before Modernized Mode work, record:

```text
tests passing
baseline measurements
architecture version
known limitations
```

The assignment specifically requires baseline analysis and measurements before improvement.

---

# Task M5-31 — Build baseline measurement harness

Member 5 should create a small reproducible way to measure selected system properties.

Avoid building a full benchmarking platform.

Possible measurements:

```text
Legacy→Gateway latency

Gateway→Cloud baseline latency

end-to-end latency

canonical payload size

Cloud storage latency

successful message count

retry count
```

---

# Task M5-32 — Ensure benchmarks are reproducible

Record:

```text
number of messages
environment
security mode
failure mode
configuration
measurement method
```

Example:

```text
100 messages
FAILURE_MODE=none
SECURITY_MODE=classical
```

Do not compare different workloads and call them equivalent.

---

# Task M5-33 — Gateway↔Cloud ML-KEM integration orchestration


Coordinate Members 3 and 4.

Core valid-path integration:

```text
Cloud generates ML-KEM-768 key pair
↓
Cloud publishes:
protocol_version
algorithm
key_id
public_key
↓
Gateway validates protocol/key metadata
↓
Gateway encapsulates
↓
Cloud decapsulates
↓
same shared secret on the valid path
↓
both derive the same 32-byte session_key using:
HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32
↓
Cloud creates session
↓
Gateway receives session_id + status + expires_at
```

Member 5 focuses on reproducible automated execution, not the cryptographic implementation itself.

Do not design tests that assume every modified valid-length ML-KEM ciphertext must throw a decapsulation exception. ML-KEM may use implicit-rejection behavior; explicit injected decapsulation/wrapper failures test operational error handling.

---

# Task M5-34 — Secure-session E2E test


Verify:

```text
Gateway fetches /api/v1/crypto/public-key

Gateway validates:
protocol_version
algorithm
key_id

Gateway establishes versioned ML-KEM-768 session

Gateway and Cloud derive identical:
32-byte session_key

HKDF contract:
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32

Cloud returns:
protocol_version
session_id
status
expires_at

Gateway creates request_id

Gateway encrypts CanonicalMeasurement
with AES-256-GCM

Gateway uses 12-byte nonce

Gateway sends SecureEnvelope:
protocol_version
gateway_id
session_id
request_id
nonce
ciphertext

Cloud reconstructs byte-identical four-field AAD

Cloud authenticates/decrypts

Cloud validates canonical data

Cloud stores idempotently
```

This should run without direct internal shortcuts between Gateway and Cloud.

---

# Task M5-35 — Full modernized E2E test


Complete system:

```text
Legacy Device
      ↓
Edge Gateway
      ↓
ML-KEM-768 session
      ↓
HKDF-SHA-256
      ↓
AES-256-GCM SecureEnvelope
      ↓
Cloud authentication/decryption
      ↓
Cloud Service
      ↓
SQLite
```

Then query Cloud and compare the original logical measurement with stored data.

Verify:

```text
Legacy protocol unchanged
request_id traced separately
received_at stored as gateway_received_at
cloud_received_at added
one logical row only

ordinary ambiguous retry:
same already-built SecureEnvelope
same request_id
same nonce
same ciphertext
same AAD

business idempotency prevents duplicate row
```

Also document:

```text
protocol v1 has no dedicated cryptographic anti-replay counter/window
```

---

# Task M5-36 — Legacy compatibility regression test

One of the most important system tests:

Run the **same Legacy Device** against:

```text
SECURITY_MODE=classical
```

and then:

```text
SECURITY_MODE=mlkem
```

No Legacy source/config protocol change should be necessary other than its usual Gateway address.

This proves the modernization boundary works as designed.

---

# Task M5-37 — Session reuse system test

Send several measurements:

```text
measurement 1
measurement 2
measurement 3
```

Expected:

```text
1 ML-KEM handshake
3 secure messages
```

provided the session remains active.

Member 5 should verify metrics/logs support this conclusion.

---

# Task M5-38 — Session expiry system test


Set test TTL low or use controlled time.

Expected:

```text
message 1
→ handshake/session A
→ success

advance time beyond expiry

message 2
→ Cloud rejects old session with 409 SESSION_EXPIRED
→ Gateway invalidates local session
→ Gateway fetches current public key
→ Gateway establishes session B once
→ same logical measurement/request_id rebuilt under session B
→ success
```

Also verify proactive local expiry behavior:

```text
Gateway detects its session already expired before send
→ establishes a new session directly
```

Verify:

```text
new session
new handshake/session event
successful message after re-key
no infinite recovery loop
```

---

# Task M5-39 — Design project-wide failure-test matrix


Member 5 owns the matrix coordinating fault injection across all components.

Recommended matrix:

| ID | Fault source | Failure | Expected |
|---|---|---|---|
| F1 | Legacy | malformed JSON/body | Gateway `400`, no Cloud call |
| F2 | Legacy | missing required field | Gateway `422`, no Cloud call |
| F3 | Legacy | invalid humidity | Gateway `422`, no Cloud call |
| F4 | Legacy | invalid timestamp | Gateway `422`, no Cloud call |
| F5 | Legacy | duplicate sequence | Gateway `409` |
| F6 | Legacy | out-of-order sequence | Gateway `409` |
| F7 | Gateway | processing error | Legacy receives visible failure |
| F8 | Gateway | Cloud timeout | bounded retry |
| F9 | Gateway | ML-KEM/session failure | fail closed, no baseline call |
| F10 | Gateway | corrupt AEAD ciphertext | Cloud rejects, no storage |
| F11 | Cloud | public key unavailable | session establishment cannot start |
| F12 | Cloud | simulated decapsulation/wrapper failure | no usable session |
| F13 | Cloud | unknown session | `409 SESSION_INVALID`, bounded re-establishment |
| F14 | Cloud | expired session | `409 SESSION_EXPIRED`, bounded re-establishment |
| F15 | Cloud | decryption failure | no storage |
| F16 | Cloud | storage failure | `503`, Gateway bounded retry |
| F17 | Cloud | service unavailable | `503`, Gateway bounded retry |
| F18 | Cloud | drop response | same-envelope retry, one DB row |

Important:

```text
simulated decapsulation failure
```

is an operational fault-injection scenario. Do not present it as evidence that arbitrary valid-length ML-KEM ciphertext corruption must naturally raise a decapsulation exception.

Protocol version `1` has no dedicated cryptographic replay-rejection test because no replay counter/window is implemented.

---

# Task M5-40 — Automate Legacy fault scenarios


Coordinate Member 1's payload failure injection.

Representative tests:

```text
invalid_temperature
→ Gateway 422
→ no retry by Legacy
→ no Cloud call

invalid_humidity
→ Gateway 422
→ no retry
→ no Cloud call

invalid_timestamp
→ Gateway 422
→ no retry
→ no Cloud call

missing_field
→ Gateway 422
→ no retry
→ no Cloud call

duplicate_sequence
→ Gateway 409
→ no retry

out_of_order_sequence
→ Gateway 409
→ no retry

sequence gap
→ Gateway accepts + gap metric/log
```

Also include one separate raw HTTP contract test for:

```text
malformed/unparseable JSON
→ Gateway 400
```

because the normal Legacy `missing_field` fault remains syntactically valid JSON.

These tests should use the actual Legacy wire payload, not internal Gateway model shortcuts.

---

# Task M5-41 — Automate Gateway application faults

Coordinate Member 2.

Examples:

```text
processing_error
cloud_timeout
cloud_unavailable
drop_message
```

Verify expected response propagation.

---

# Task M5-42 — Automate Gateway security faults


Coordinate Member 3.

Representative scenarios:

```text
mlkem_handshake_failure

corrupt_ciphertext

session_missing

session_expired
```

Expected behavior must match the frozen protocol:

```text
ML-KEM/session failure
→ fail closed
→ no baseline endpoint call

corrupt AEAD ciphertext
→ Cloud secure-message rejection
→ no storage

session missing
→ 409 SESSION_INVALID
→ one bounded session re-establishment

session expired
→ 409 SESSION_EXPIRED
→ one bounded session re-establishment
```

Do not add `confirmation_tag`, `message_counter`, or cryptographic replay-window scenarios to protocol version `1`.

---

# Task M5-43 — Automate Cloud faults


Coordinate Member 4.

Representative scenarios:

```text
public_key_unavailable

mlkem_decapsulation_failure
(simulated wrapper/application failure)

session_not_found

session_expired

decryption_failure

storage_failure

service_unavailable

processing_delay

drop_response
```

Verify each result against the shared protocol.

Also verify:

```text
decryption failure stores nothing

drop_response causes ordinary same-envelope retransmission

same-envelope retransmission remains business-idempotent
```

Do not use `mlkem_decapsulation_failure` to claim that all corrupted valid-length ML-KEM ciphertexts naturally raise an exception.

---

# Task M5-44 — Idempotent retry E2E test


Critical ambiguous-response scenario:

```text
Gateway builds SecureEnvelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Gateway sends envelope
↓
Cloud authenticates/decrypts
↓
Cloud stores successfully
↓
Cloud response dropped
↓
Gateway retries the SAME already-built SecureEnvelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud authenticates/decrypts same envelope
↓
Cloud identifies duplicate logical measurement
using (device_id, sequence_number)
↓
Cloud returns 202 already_accepted
↓
one DB row only
```

Verify retry preserves:

```text
same logical measurement
same request_id
same session_id
same nonce
same ciphertext
same AAD
```

This proves transport retransmission and application-level idempotency.

It does **not** prove cryptographic anti-replay protection; protocol version `1` has no dedicated replay counter/window.

---

# Task M5-45 — Retry amplification evaluation

Recognize the layered retry effect.

If Legacy performs:

```text
3 attempts
```

and Gateway performs:

```text
3 Cloud attempts each
```

worst case may be:

```text
9 downstream attempts
```

Member 5 should measure/document this behavior.

Do not necessarily redesign it for a course-sized system.

Record it as operational technical debt if appropriate.

---

# Task M5-46 — Logging convention coordination

Member 5 should define a project-wide logging convention with Members 1–4.

Recommended common fields:

```text
event
component
request_id
device_id
gateway_id
sequence_number
```

When relevant:

```text
session_id
key_id
record_id
status
attempt
failure_type
```

---

# Task M5-47 — Ensure correlation-ID propagation


Gateway creates:

```text
request_id
```

after the Legacy request passes Gateway validation/sequence policy.

Verify both Gateway→Cloud modes.

### Baseline Mode

```text
Gateway request_id
↓
X-Request-ID
↓
Cloud logs same request_id
```

### Modernized Mode

```text
Gateway request_id
↓
SecureEnvelope.request_id
↓
same request_id authenticated as AAD
↓
Cloud logs same request_id
```

The secure envelope value is authoritative in Modernized Mode.

Member 5 should create an integration test or reproducible manual check showing one measurement can be traced end to end.

Never use `request_id` or `session_id` as high-cardinality metrics labels.

---

# Task M5-48 — End-to-end trace demo

Example:

```text
Legacy sequence=42

Gateway:
request_id=req-abc

Cloud:
request_id=req-abc
record_id=rec-xyz
```

This is a useful presentation/debugging artifact.

---

# Task M5-49 — Project-wide secret logging review

Member 5 should coordinate tests ensuring logs do not contain:

```text
ML-KEM private key
shared secret
session key
password
token
.env contents
```

Members 3 and 4 write crypto-specific tests; Member 5 ensures these tests are run project-wide.

---

# Task M5-50 — Build log-safety CI regression

Where practical:

```text
capture logs during secure E2E
↓
search for known test-secret markers
↓
assert absent
```

This is strong evidence of critical evaluation.

---

# Task M5-51 — Metrics endpoint integration

Gateway:

```text
GET /metrics
```

Cloud:

```text
GET /metrics
```

Member 5 should ensure they can be queried from the test environment.

No need for a huge monitoring stack unless useful.

---

# Task M5-52 — Define minimum Gateway metrics set


Coordinate Members 2 and 3.

Minimum Gateway set:

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

For protocol version `1`:

```text
gateway_pqc_fallback_total
```

should remain zero because runtime plaintext fallback is not implemented.

Keeping it can help detect accidental downgrade behavior.

Do not use request/session identifiers as labels.

---

# Task M5-53 — Define minimum Cloud metrics set


Coordinate Member 4.

Minimum Cloud set:

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

cloud_authenticated_messages_total
cloud_decryption_failures_total

cloud_measurements_stored_total
cloud_storage_failures_total
cloud_duplicate_measurements_total

cloud_injected_failures_total
```

These names should remain consistent with the Cloud component documentation and tests.

Do not use:

```text
request_id
session_id
```

as high-cardinality labels.

---

# Task M5-54 — Metrics sanity tests


Verify metrics behave correctly.

Example:

```text
send 5 valid measurements
→ received/stored counters increase
```

Inject:

```text
corrupt_ciphertext
```

Expected:

```text
decryption failure counter increases
stored counter does not increase
```

Also test:

```text
valid ordinary retry after ambiguous response
→ Gateway Cloud retry metric increases
→ one logical DB row
```

---

# Task M5-55 — Metric cardinality review

Member 5 should review labels.

Reject metrics such as:

```text
metric{request_id="unique-every-time"}
```

or:

```text
metric{session_id="..."}
```

Prefer bounded labels:

```text
result
failure_type
security_mode
```

---

# Task M5-56 — Optional monitoring dashboard decision

A dashboard is **not required** by the course documents; meaningful metrics are required.
The project now includes its deliberately small local dashboard in the default
Compose stack for easier demonstration and operations.

For trusted local demonstrations only, the dashboard may apply a confirmed,
temporary allowlisted failure-injection or log-level override by replacing and
restarting the selected service. It must not edit `.env` or Compose files, and
must keep frozen protocol/security configuration display-only. The dashboard's
loopback-only binding and documented Docker-socket trust boundary are required.

Member 5 should not introduce Grafana/Prometheus infrastructure unless:

```text
it materially helps demonstration
and
the team has time
```

A simple metrics endpoint may be entirely sufficient.

This respects the course's instruction to keep the project simple.

---

# Task M5-57 — Test environment deployment

The course requires deployment to a test environment.

Docker Compose can serve as that environment if this is the group's documented interpretation.

Member 5 should document:

```text
how to build
how to deploy
how to stop
how to reset
how to verify health
how to inspect logs
how to query data
```

---

# Task M5-58 — Create deployment runbook

Suggested:

```text
docs/deployment.md
```

Include:

```bash
uv sync
docker compose build
docker compose up
docker compose ps
docker compose logs
docker compose down
```

plus health/query verification.

Use actual repository commands.

---

# Task M5-59 — Create developer testing guide

Suggested:

```text
docs/testing.md
```

Document:

```text
unit tests
contract tests
integration tests
E2E tests
failure tests
security tests
baseline measurements
```

---

# Task M5-60 — Maintain project development workflow docs

If the project already has:

```text
docs/DEVELOPMENT_WORKFLOW.md
```

Member 5 should help keep commands current.

Do not rewrite team contribution history.

Focus on:

```text
branching
AI-history flow
testing
CI
PR review
integration
```

---

# Task M5-61 — Design CI job separation

A useful split might be:

```text
quality
unit-tests
integration-tests
docker-build
```

Potentially:

```text
secure-e2e
```

as another job.

Avoid excessive complexity if one workflow is sufficient.

---

# Task M5-62 — CI caching

Optional optimization:

```text
uv dependency cache
```

if CI becomes slow.

Do not prioritize caching over correctness.

---

# Task M5-63 — Docker build validation in CI

Build:

```text
Legacy image
Gateway image
Cloud image
```

This catches problems such as:

```text
missing file
bad entry point
ML-KEM native dependency failure
wrong package configuration
```

before demo day.

---

# Task M5-64 — Clean-environment test

Member 5 should occasionally validate from a clean environment.

Goal:

```text
fresh checkout
↓
uv sync
↓
tests
↓
docker compose build
↓
docker compose up
```

works without developer-local hidden state.

---

# Task M5-65 — Modernized performance test harness


After Modernized Mode works, repeat the baseline workload with:

```text
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
```

Use the same:

```text
number of messages
payloads
environment
failure mode
database/reset state
measurement method
```

for fair comparison.

The secure run uses the frozen protocol:

```text
ML-KEM-768
HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
AES-256-GCM
four-field AAD
```

Do not compare different workloads and attribute the difference to PQC.

---

# Task M5-66 — Separate first-message latency


Measure:

```text
first secure message
```

separately because it includes:

```text
public-key retrieval
ML-KEM encapsulation
Cloud decapsulation
HKDF-SHA-256
session establishment
```

Do not average this blindly with subsequent messages.

---

# Task M5-67 — Measure steady-state secure latency


Once session exists:

```text
Gateway AES-256-GCM encryption
network
Cloud session lookup
Cloud AES-256-GCM authentication/decryption
validation
storage
```

This is the more representative normal secure-message path.

---

# Task M5-68 — Compare payload sizes

Record approximate:

```text
baseline canonical JSON size
```

versus:

```text
SecureEnvelope JSON size
```

This demonstrates protocol overhead.

Do not claim performance effects without measurement.

---

# Task M5-69 — Collect session-establishment metrics


Member 5 should gather from Members 3 and 4:

```text
ML-KEM handshake duration
Cloud decapsulation duration
session creation count
session failures

active-session count
session re-establishment count

Cloud request retry count
decryption-failure count
```

For final evaluation, distinguish:

```text
first-message/session-establishment overhead
```

from:

```text
steady-state secure-message overhead
```

Do not use `request_id` or `session_id` as metric labels.

---

# Task M5-70 — Build baseline vs modernized comparison table


Eventually populate real measured values:

| Metric | Baseline Mode (`classical`) | Modernized Mode (`mlkem`) |
|---|---:|---:|
| First message latency | | |
| Steady-state latency | | |
| Gateway→Cloud payload size | | |
| Session setup time | N/A | |
| Successful messages | | |
| Failed messages | | |
| Storage success | | |

No invented numbers.

The first secure request must be interpreted separately because it includes public-key retrieval/session establishment.

---

# Task M5-71 — Coordinate test coverage evidence

If the team uses coverage, Member 5 can aggregate:

```text
Legacy coverage
Gateway coverage
Cloud coverage
```

But coverage percentage should not be treated as proof of correctness.

The course requires critical evaluation rather than superficial metrics.

---

# Task M5-72 — Create project-wide test matrix

Example:

|Area|Unit|Contract|Integration|E2E|Failure|
|---|---|---|---|---|---|
|Legacy|✓|✓|✓|✓|✓|
|Gateway app|✓|✓|✓|✓|✓|
|Gateway crypto|✓|✓|✓|✓|✓|
|Cloud|✓|✓|✓|✓|✓|
|Storage|✓||✓|✓|✓|
|Deployment|||✓|✓|✓|

Member 5 keeps track of gaps.

---

# Task M5-73 — Coordinate missing-test resolution

Member 5 should not personally write every missing test.

Instead:

```text
identify gap
assign to owner
verify it enters CI
```

Example:

```text
Missing ML-KEM tamper test
→ Member 3/4

Missing Legacy retry test
→ Member 1

Missing Gateway validation test
→ Member 2
```

---

# Task M5-74 — Security regression suite coordination


Ensure CI eventually covers:

```text
tampered AEAD ciphertext

tampered AAD:
protocol_version
gateway_id
session_id
request_id

wrong session

expired session

unknown session

malformed ML-KEM session input where detectable

simulated ML-KEM decapsulation/application failure

ML-KEM implicit-rejection caveat

no secret logging

no plaintext on secure endpoint

no automatic baseline fallback

ambiguous-response ordinary retry uses:
same already-built SecureEnvelope
same request_id
same nonce
same ciphertext
same AAD

retry remains idempotent

documented absence of dedicated cryptographic anti-replay counter/window
```

Do not make a brittle regression test that assumes every bit-flipped valid-length ML-KEM ciphertext must cause an explicit decapsulation exception.

---

# Task M5-75 — Verify fail-closed behavior system-wide

In:

```text
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
```

inject:

```text
mlkem_handshake_failure
```

Expected:

```text
no baseline Cloud POST
no plaintext measurement
request fails visibly
```

This should be an automated or reproducible test.

---

# Task M5-76 — Verify runtime plaintext fallback is absent


Protocol version `1` does **not** implement runtime classical fallback.

Member 5 should therefore verify the **absence** of fallback behavior.

Required system test:

```text
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
+ injected ML-KEM/session failure
↓
Gateway request fails visibly
↓
zero calls to:
POST /api/v1/baseline/measurements
```

Also verify:

```text
PQC_FAILURE_POLICY other than fail_closed
→ Gateway startup/config validation fails

gateway_pqc_fallback_total
→ remains zero
```

Baseline Mode remains available only through explicit configuration:

```text
SECURITY_MODE=classical
```

Switching modes is an operator/configuration action, not automatic failure recovery.

---

# Task M5-77 — Deployment failure scenarios

Member 5 should test operational failures outside internal failure injection too.

Examples:

```text
Cloud container stopped

Gateway container restarted

Legacy starts before Gateway

database unavailable/corrupted where practical

Gateway restart loses session
```

Verify expected recovery.

---

# Task M5-78 — Gateway restart scenario

Expected:

```text
Gateway stops
↓
session lost
↓
Gateway restarts
↓
next measurement triggers new ML-KEM handshake
```

Cloud's old session may eventually expire.

Document behavior.

---

# Task M5-79 — Cloud restart scenario


With ephemeral Cloud ML-KEM key/session state:

```text
Cloud restarts
↓
new ML-KEM-768 key pair
↓
old Cloud sessions disappear
↓
Gateway still attempts old session
↓
Cloud returns 409 SESSION_INVALID
↓
Gateway invalidates local session
↓
Gateway fetches new public key/key_id
↓
new ML-KEM session established
↓
same logical measurement/request_id rebuilt
under the replacement session
```

Verify:

```text
no automatic baseline fallback
no duplicate logical DB row
```

This is an excellent technical-debt and recovery scenario.

---

# Task M5-80 — Legacy continuous-operation scenario

While Gateway/Cloud experience failures:

```text
Legacy should continue producing future measurements
```

after bounded failure handling.

Member 5 should verify the overall system does not permanently stall.

---

# Task M5-81 — Build project-wide technical-debt register


Member 5 coordinates technical debt from all members.

Suggested:

```text
docs/technical-debt.md
```

Include:

| Debt | Component | Risk | Why accepted | Future improvement |
|---|---|---|---|---|

Likely entries:

```text
No Legacy authentication

No persistent Gateway queue

In-memory Gateway sequence state

In-memory secure sessions

Ephemeral Cloud ML-KEM key

Simplified Cloud public-key trust

HTTP-only controlled test environment

SQLite

Single-instance services / no HA

Simple bounded retry strategy

Idempotency based on (device_id, sequence_number)
with restart/reset caveat

No dedicated cryptographic anti-replay counter/window

Python cannot guarantee secure memory zeroization
```

Do not describe business idempotency as cryptographic replay protection.

---

# Task M5-82 — Build project-wide risk register


Separate:

```text
technical debt
```

from:

```text
security/operational risk
```

Possible risks:

```text
Cloud public-key substitution
message loss during outage
replay of an authenticated secure envelope
retry amplification
Legacy spoofing
Cloud/Gateway restart state loss
secret leakage through future debugging
```

---

# Task M5-83 — Coordinate final evaluation evidence

The final evaluation must analyze strengths, weaknesses, technical debt, and risks.

Member 5 should collect **evidence**, not write unsupported claims.

Examples:

```text
tests
measurements
failure screenshots/logs
metrics values
CI results
baseline vs secure timing
```

---

# Task M5-84 — Define system strengths based on evidence

Potential strengths, only after verified:

```text
Legacy compatibility maintained

Gateway/Cloud security path modular

tampered ciphertext rejected

bounded retries

failure injection supports repeatable testing

CI automates checks

health/readiness available
```

These must be supported by tests/results.

---

# Task M5-85 — Define system weaknesses based on evidence

Potential weaknesses:

```text
simplified trust model

no production PKI

no persistent buffering

single-instance services

SQLite limitations

restart loses sessions

Legacy side remains non-PQC
```

Do not hide them.

---

# Task M5-86 — Peer-review submission readiness

The peer-review submission deadline is earlier than the final project deadline.

Member 5 should coordinate a pre-peer-review freeze.

Checklist:

```text
system builds
tests pass
Compose works
docs readable
AI history valid
no secrets
major features present
known issues documented
```

---

# Task M5-87 — Presentation environment rehearsal

Before presentation:

```text
fresh environment
↓
start stack
↓
normal message
↓
show Cloud stored data
↓
show ML-KEM metric/session
↓
trigger one failure
↓
show rejection/metric/log
```

Member 5 should make demo steps deterministic.

---

# Task M5-88 — Prepare demo scenario 1: normal baseline

```text
SECURITY_MODE=classical
FAILURE_MODE=none
```

Show:

```text
Legacy generates
Gateway forwards
Cloud stores
```

---

# Task M5-89 — Prepare demo scenario 2: Modernized Mode


Use:

```text
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed
```

Show:

```text
same Legacy Device

Gateway obtains versioned Cloud ML-KEM-768 public key
with key_id

ML-KEM session established

HKDF-SHA-256 derives one 32-byte session key using:
salt=None
info="ml-kem-project:v1:gateway-cloud-session"

session reused for multiple messages

AES-256-GCM SecureEnvelope sent

four-field AAD authenticates:
protocol_version
gateway_id
session_id
request_id

Cloud authenticates/decrypts

secure message stored
```

This clearly demonstrates modernization while preserving the Legacy contract.

---

# Task M5-90 — Prepare demo scenario 3: tampering


Enable:

```text
Gateway FAILURE_MODE=corrupt_ciphertext
```

Show:

```text
Cloud receives SecureEnvelope
↓
AES-256-GCM authentication fails
↓
Cloud rejects
↓
no storage
↓
cloud_decryption_failures_total increases
```

Also show, if convenient:

```text
same Legacy/Gateway route remains unchanged
no fallback to baseline endpoint
```

---

# Task M5-91 — Prepare demo scenario 4: Cloud failure

Enable:

```text
Cloud FAILURE_MODE=storage_failure
```

Show:

```text
Cloud fails safely
Gateway retries
failure visible
```

---

# Task M5-92 — Document system runbook


Suggested:

```text
docs/RUNBOOK.md
```

Include:

```text
start system
stop system

run Baseline Mode:
SECURITY_MODE=classical

run Modernized Mode:
SECURITY_MODE=mlkem
PQC_FAILURE_POLICY=fail_closed

enable per-service failure injection

check health
check readiness
view logs
view metrics
query Cloud
reset test database/volumes
run tests
```

Also document:

```text
no runtime automatic fallback exists

Modernized Mode session errors use 409 recovery

ordinary ambiguous-response retry resends the same already-built SecureEnvelope

business idempotency prevents duplicate rows

no dedicated cryptographic anti-replay counter/window exists in protocol v1

Cloud restart creates a new ephemeral ML-KEM key pair
```

This is valuable technical and presentation documentation.

---

# Task M5-93 — AI-history workflow for Member 5

Member 5's own AI-assisted tasks also require human review.

Good tasks:

```text
Implement Docker Compose environment

Implement CI pipeline

Implement integration-test framework

Implement E2E tests

Implement metrics integration

Implement deployment runbook

Implement failure-test orchestration
```

Workflow:

```text
ai-history start
↓
significant AI interactions
↓
implementation
↓
tests
↓
ai-history output
↓
human review
↓
revision if necessary
↓
verify
```

---

# Task M5-94 — Human review of AI-generated CI/CD

CI-generated code should be reviewed for:

```text
wrong working directory
non-frozen dependencies
tests accidentally skipped
continue-on-error
secrets printed
untrusted scripts
incorrect branch trigger
Docker build not actually tested
```

A green CI pipeline is not useful if it silently ignores failures.

---

# Task M5-95 — Human review of AI-generated Docker files

Review:

```text
base image
package installation
entrypoint
working directory
ports
environment
healthcheck
root/user behavior if relevant
unnecessary packages
build reproducibility
```

---

# Task M5-96 — Document accepted/modified/rejected AI decisions

Examples:

```text
AI proposed adding Kubernetes.
→ Rejected.
Reason:
unnecessary for course test environment.
```

```text
AI proposed using Kafka for retry buffering.
→ Rejected.
Reason:
adds complexity beyond project needs.
```

```text
AI proposed running only unit tests in CI.
→ Modified.
Reason:
project requires system integration evidence.
```

```text
AI proposed using `uv sync` without `--frozen` in CI.
→ Modified.
Reason:
CI should verify committed dependency lock consistency.
```

```text
AI proposed marking test steps continue-on-error.
→ Rejected.
Reason:
failed quality checks must block merge.
```

These are good examples of the critical evaluation expected by the assignment.

---

# Task M5-97 — Peer review responsibilities


Member 5 should review PRs affecting system integration.

### Member 1

```text
Dockerfile
configuration names
Gateway URL
shutdown
serializer/payload boundary
failure-variable mapping
400=malformed/unparseable and 422=parsed-but-invalid expectations
```

### Member 2

```text
Gateway Docker
health/readiness
metrics
Cloud URL
baseline X-Request-ID
retry behavior
sequence-state timing
security-mode dispatch
```

### Member 3

```text
crypto dependency installability
secure integration tests
Base64URL assumptions
public-key key_id handling
fixed HKDF contract
four-field AAD/nonce contract
409 session recovery
same-envelope ordinary retry behavior
PQC metrics
fail-closed behavior
```

### Member 4

```text
Cloud Docker
database path/persistence
health/readiness
baseline X-Request-ID
received_at → gateway_received_at mapping
session status codes
same-envelope retransmission/idempotency
SQLite persistence
```

Member 5 does not replace the component owner's technical review; this review focuses on cross-component reproducibility and integration.

---

# Task M5-98 — Protocol regression detection


If any PR changes:

```text
endpoint
JSON field
HTTP header
port
environment variable
status code
protocol version
crypto-suite identifier
key_id semantics
HKDF salt/info/length
nonce size
AAD fields/serialization
SecureEnvelope fields
session error code
retry/retransmission semantics
storage field mapping
health/readiness behavior
```

Member 5 should ensure contract/integration tests detect the change.

The shared protocol specification must be updated **before** intentionally changing a frozen cross-component contract.

In particular, accidental introduction of these fields/features should fail review unless the protocol is intentionally revised:

```text
Cloud identity in public/session protocol messages
session_key
session response
message counter
dedicated replay counter/window
fresh encryption for ordinary transport retry
```

---

# Task M5-99 — Release branch/freeze coordination

Before final submission:

```text
freeze major architecture
stop adding optional features
only bug fixes/docs
```

Member 5 should coordinate the system-quality perspective.

---

# Task M5-100 — Final clean-build verification


From a clean checkout:

```bash
uv sync --frozen
uv run ruff check .
uv run pytest
uv run ai-history check
docker compose build
docker compose up
```

Then verify:

```text
health
readiness

Baseline Mode flow

Modernized Mode flow

X-Request-ID baseline correlation

public-key protocol_version/algorithm/key_id validation

ML-KEM session establishment

fixed HKDF interoperability

SecureEnvelope request_id/four-field-AAD correlation

query API

one Legacy validation failure

one secure tamper failure

one 409 session-recovery scenario

one fail-closed/no-baseline-call scenario

one dropped-response/idempotency scenario
using same-envelope retransmission
```

---

# Task M5-101 — Final repository security scan by inspection


Check for:

```text
.env
private keys
database credentials
shared secrets
session keys
debug dumps
local database files accidentally committed
large generated logs
```

Also use Git history awareness if secrets were accidentally committed earlier; deleting from latest version alone does not remove Git history.

---

# Task M5-102 — Final CI verification

Final main branch must show:

```text
dependency install ✓
static checks ✓
unit tests ✓
contract tests ✓
integration tests ✓
AI-history check ✓
Docker build ✓
E2E if configured ✓
```

---

# Task M5-103 — Final documentation consistency pass

Verify documentation commands actually work.

Especially:

```text
README
RUNBOOK
deployment docs
testing docs
architecture docs
```

Avoid stale commands.

---

# Task M5-104 — Final operational quality pass


Check:

```text
Docker
✓
✓ service-scoped root failure variables map correctly per service

Networking
✓

Health
✓

Readiness
✓
✓ no active secure session required merely for readiness

Logs
✓

Metrics
✓

Baseline Mode
✓ SECURITY_MODE=classical
✓ X-Request-ID

Modernized Mode
✓ SECURITY_MODE=mlkem
✓ ML-KEM-768
✓ HKDF-SHA-256
✓ salt=None
✓ info="ml-kem-project:v1:gateway-cloud-session"
✓ one 32-byte session key
✓ AES-256-GCM
✓ 12-byte nonce
✓ four-field AAD
✓ SecureEnvelope has no message counter

Session recovery
✓ 409 SESSION_INVALID
✓ 409 SESSION_EXPIRED
✓ one bounded re-establishment
✓ rebuild under replacement session

Fail-closed behavior
✓ no automatic baseline fallback

Ambiguous-response retry
✓ same already-built SecureEnvelope
✓ same request_id
✓ same session_id
✓ same nonce
✓ same ciphertext
✓ same AAD
✓ idempotent storage

Replay limitation
✓ no dedicated cryptographic anti-replay counter/window
✓ documented as technical debt

Failure injection
✓

CI
✓

Testing
✓

AI history
✓

Documentation
✓
```

---

# Recommended Member 5 task order

I would assign Member 5's tasks in this sequence:

```text
M5-00   Review component contracts

M5-01   Root uv workspace

M5-02   Quality tooling

M5-03   Repository hygiene

M5-04   .env.example

M5-05   Docker Compose topology

M5-06   Service dependency strategy

M5-07   Docker networking

M5-08   Legacy container integration

M5-09   Gateway container integration

M5-10   Cloud container integration

M5-11   SQLite persistence strategy

M5-12   One-command environment

M5-13   Container health checks

M5-14   Readiness integration

M5-15   CI workflow

M5-16   Frozen dependency install

M5-17   Ruff/static checks

M5-18   Unit-test CI

M5-19   Contract-test CI

M5-20   Integration-test CI

M5-21   E2E CI

M5-22   AI-history CI check

M5-23   AI-history tooling compatibility

M5-24   Integration-test structure

M5-25   Shared fixtures

M5-26   Legacy↔Gateway integration

M5-27   Gateway↔Cloud baseline integration

M5-28   Baseline E2E

M5-29   Baseline E2E assertions

M5-30   Baseline freeze

M5-31   Baseline measurement harness

M5-32   Measurement reproducibility

M5-33   ML-KEM + fixed-HKDF integration

M5-34   Secure-session E2E

M5-35   Modernized E2E

M5-36   Legacy compatibility regression

M5-37   Session reuse system test

M5-38   Session expiry system test

M5-39   Failure-test matrix

M5-40   Legacy failure scenarios

M5-41   Gateway application failures

M5-42   Gateway security failures

M5-43   Cloud failures

M5-44   Same-envelope retry + idempotency test

M5-45   Retry amplification analysis

M5-46   Logging convention

M5-47   Correlation propagation

M5-48   End-to-end trace demo

M5-49   Secret logging review

M5-50   Log-safety CI regression

M5-51   Metrics integration

M5-52   Gateway metrics validation

M5-53   Cloud metrics validation

M5-54   Metrics sanity tests

M5-55   Cardinality review

M5-56   Monitoring scope decision

M5-57   Test environment deployment

M5-58   Deployment runbook

M5-59   Testing guide

M5-60   Development workflow maintenance

M5-61   CI job architecture

M5-62   CI caching if needed

M5-63   Docker-build CI

M5-64   Clean-environment verification

M5-65   Modernized benchmark harness

M5-66   First-message measurement

M5-67   Steady-state measurement

M5-68   Payload-size comparison

M5-69   PQC/session metric collection

M5-70   Comparison table

M5-71   Coverage evidence if used

M5-72   Project test matrix

M5-73   Missing-test coordination

M5-74   Security regression suite

M5-75   Fail-closed verification

M5-76   Verify runtime plaintext fallback is absent

M5-77   Deployment failure tests

M5-78   Gateway restart test

M5-79   Cloud restart test

M5-80   Legacy continuity test

M5-81   Technical-debt register

M5-82   Risk register

M5-83   Evaluation evidence

M5-84   Evidence-backed strengths

M5-85   Evidence-backed weaknesses

M5-86   Peer-review submission readiness

M5-87   Presentation rehearsal

M5-88   Baseline demo

M5-89   ML-KEM demo

M5-90   Tampering demo

M5-91   Cloud failure demo

M5-92   System runbook

M5-93   AI-history workflow

M5-94   AI CI/CD review

M5-95   AI Docker review

M5-96   AI decision documentation

M5-97   Peer reviews

M5-98   Protocol regression detection

M5-99   Final freeze coordination

M5-100  Clean-build verification

M5-101  Final security inspection

M5-102  Final CI verification

M5-103  Documentation consistency

M5-104  Final operational quality pass
```

# Suggested PR breakdown for Member 5

|PR|Scope|
|---|---|
|PR 1|Root tooling + repository hygiene|
|PR 2|Initial Docker Compose baseline|
|PR 3|CI: Ruff + unit tests + AI-history|
|PR 4|Contract/integration-test framework|
|PR 5|Baseline E2E|
|PR 6|Health/readiness integration|
|PR 7|Secure/PQC E2E + session recovery + fail-closed integration|
|PR 8|Failure-test orchestration + dropped-response/idempotency|
|PR 9|Logging/correlation integration + X-Request-ID/request_id tracing|
|PR 10|Metrics integration|
|PR 11|Docker/CI hardening|
|PR 12|Benchmark/evaluation tooling|
|PR 13|Restart/recovery tests|
|PR 14|Deployment/runbook documentation|
|PR 15|Final system regression and release readiness|

# Member 5 milestone gates

## Gate A — Development infrastructure ready

Required:

```text
uv workspace
quality commands
.gitignore
.env.example
initial CI
```

## Gate B — Baseline deployment ready

Required:

```text
Legacy container
Gateway container
Cloud container
Docker Compose
health
baseline communication
```

## Gate C — Baseline E2E ready

Required:

```text
Legacy → Gateway → Cloud → SQLite
```

with baseline evidence recorded.

## Gate D — Secure E2E ready

Required:

```text
Legacy → Gateway → ML-KEM-768 / fixed HKDF-SHA-256 / AES-256-GCM → Cloud → SQLite
```

and same Legacy compatibility.

## Gate E — Failure/observability ready

Required:

```text
failure matrix
logs
correlation IDs
metrics
health/readiness
```

## Gate F — CI/deployment production-like course environment ready

Required:

```text
unit
contract
integration
E2E
AI-history validation
Docker builds
```

## Gate G — Final project-ready system

Required:

```text
evaluation evidence
technical debt
risk register
runbook
presentation demo
clean build
CI green
```

# Final Definition of Done for Member 5

Member 5's work is complete only when:

```text
[ ] A fresh clone can install with uv.

[ ] uv.lock is respected in CI.

[ ] Ruff/static checks run automatically.

[ ] Unit tests run automatically.

[ ] Contract tests run automatically.

[ ] Integration tests run automatically.

[ ] AI-history validation runs automatically.

[ ] Docker images for all three components build successfully.

[ ] Docker Compose starts the entire system.

[ ] Root failure-injection variables are service-scoped for Legacy, Gateway, and Cloud.

[ ] No single root FAILURE_MODE / FAILURE_RATE block controls all services.

[ ] SECURITY_MODE and SESSION_TTL_SECONDS are not duplicated in the root .env.example.

[ ] Compose maps LEGACY_FAILURE_*, GATEWAY_FAILURE_*, and CLOUD_FAILURE_* into each service's internal generic failure variables.

[ ] Docker Compose networking works without localhost mistakes.

[ ] Legacy Device reaches Gateway.

[ ] Gateway reaches Cloud.

[ ] Cloud storage initializes correctly.

[ ] Canonical received_at is stored as gateway_received_at.

[ ] cloud_received_at is generated by Cloud.

[ ] Gateway health/readiness endpoints are integrated.

[ ] Cloud health/readiness endpoints are integrated.

[ ] Container health status reflects service liveness.

[ ] Baseline E2E passes.

[ ] Baseline measurements have been recorded.

[ ] Baseline behavior is frozen before modernization comparison.

[ ] ML-KEM-768 session establishment works in the integrated environment.

[ ] Gateway and Cloud derive the same 32-byte session key.

[ ] HKDF-SHA-256 uses salt=None.

[ ] HKDF info is exactly "ml-kem-project:v1:gateway-cloud-session".

[ ] Public-key response contains protocol_version, algorithm, key_id, and public_key only.

[ ] Session response contains protocol_version, session_id, status, and expires_at.

[ ] No Cloud identity protocol field is required.

[ ] No session_key or session response exists in protocol version 1.

[ ] AES-256-GCM secure messages use 12-byte nonces.

[ ] Gateway and Cloud construct byte-identical four-field AAD.

[ ] AAD contains exactly protocol_version, gateway_id, session_id, and request_id.

[ ] SecureEnvelope contains protocol_version, gateway_id, session_id, request_id, nonce, and ciphertext.

[ ] SecureEnvelope contains no message counter.

[ ] Secure E2E passes.

[ ] Same Legacy Device works in Baseline Mode (classical) and Modernized Mode (mlkem).

[ ] Baseline requests propagate X-Request-ID.

[ ] request_id remains outside CanonicalMeasurement.

[ ] Secure request_id is authenticated as AAD.

[ ] Session reuse is verified.

[ ] 409 SESSION_INVALID recovery is verified.

[ ] 409 SESSION_EXPIRED recovery is verified.

[ ] Session recovery is bounded to one re-establishment attempt.

[ ] Failure-test matrix exists.

[ ] Representative Legacy failures are tested.

[ ] Malformed/unparseable JSON is verified as 400.

[ ] Parsed JSON with missing/wrongly typed/domain-invalid required fields is verified as 422.

[ ] Representative Gateway application failures are tested.

[ ] Representative Gateway crypto failures are tested.

[ ] Representative Cloud failures are tested.

[ ] Corrupted secure ciphertext is rejected and not stored.

[ ] Tests do not rely on the assumption that every modified valid-length ML-KEM ciphertext raises a decapsulation exception.

[ ] Cloud storage failure propagates safely.

[ ] Dropped-response retry resends the same already-built SecureEnvelope.

[ ] Dropped-response retry preserves the same request_id, session_id, nonce, ciphertext, and AAD.

[ ] Idempotent retry after dropped response creates only one record.

[ ] No dedicated cryptographic anti-replay counter/window is claimed.

[ ] Absence of cryptographic replay protection is documented as technical debt.

[ ] Business idempotency is not described as cryptographic replay protection.

[ ] Fail-closed behavior is verified.

[ ] Runtime plaintext fallback is absent.

[ ] A secure failure makes zero calls to the baseline endpoint.

[ ] gateway_pqc_fallback_total remains zero.

[ ] Correlation IDs can trace Gateway→Cloud requests in both modes.

[ ] Baseline tracing uses X-Request-ID.

[ ] Secure tracing uses authenticated SecureEnvelope.request_id.

[ ] Logging conventions are consistent enough for debugging.

[ ] Secret values do not appear in integrated logs.

[ ] Gateway metrics are accessible.

[ ] Cloud metrics are accessible.

[ ] PQC/session/decryption metrics behave as expected.

[ ] Gateway/Cloud metric names match component contracts.

[ ] Metric labels avoid dangerous high cardinality.

[ ] First-message secure latency is measured separately.

[ ] Steady-state secure latency is measured.

[ ] Baseline vs ML-KEM payload sizes are compared.

[ ] Baseline vs modernized results use equivalent workloads.

[ ] Gateway restart behavior is tested.

[ ] Cloud restart behavior is tested.

[ ] Cloud restart produces a new ephemeral ML-KEM key and triggers 409 SESSION_INVALID recovery.

[ ] Test deployment is documented.

[ ] Deployment/runbook commands actually work.

[ ] Technical-debt register is current.

[ ] Technical debt explicitly includes absence of dedicated cryptographic anti-replay counter/window.

[ ] Risk register is current.

[ ] Evaluation claims are backed by tests or measurements.

[ ] Peer-review submission is reproducible.

[ ] Presentation demo has been rehearsed.

[ ] Member 5's AI-assisted work is recorded.

[ ] AI-generated CI/Docker/test code was manually reviewed.

[ ] Accepted/modified/rejected AI decisions are documented.

[ ] No .env, secrets, private keys, unintended DB files, or logs are committed.

[ ] Clean-build verification passes.

[ ] Final CI is green.

[ ] Final PR receives teammate review.
```
