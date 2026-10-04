# Member 4 — Cloud Service Owner

## Overall mission

Member 4 owns the complete **Cloud Service**, including both the baseline and modernized secure receiving paths.

Their responsibility begins when the Gateway sends either:

```text
Baseline canonical JSON
```

or:

```text
ML-KEM session request
+
SecureEnvelope
```

and ends when accepted measurements are safely persisted and can be queried.

The owned path is:

```text
Edge Gateway
      │
      │ baseline or secure protocol
      ▼
┌───────────────────────────────┐
│         Cloud Service         │
│                               │
│ Baseline API                  │
│ ML-KEM public key API         │
│ ML-KEM decapsulation          │
│ Session manager               │
│ HKDF                          │
│ AEAD decryption               │
│ Secure-envelope validation    │
│ Canonical validation          │
│ Idempotency                   │
│ SQLite storage                │
│ Query API                     │
│ Failure injection             │
│ Logging                       │
│ Metrics                       │
│ Health/readiness              │
└──────────────┬────────────────┘
               │
               ▼
            Storage
```

Member 4 does **not** own:

```text
Legacy Device behavior
Legacy→Gateway validation
Gateway sequence tracking
Gateway ML-KEM encapsulation
Gateway-side encryption
overall CI/CD ownership
```

But Member 4 works closely with Member 3 because both sides must implement exactly the same secure protocol.

---

# Member 4 final deliverables

|Deliverable|Expected result|
|---|---|
|Cloud configuration|validated runtime configuration|
|Cloud application skeleton|runnable service|
|Baseline measurement endpoint|classical comparison path|
|Cloud storage|SQLite persistence|
|Idempotency|safe retry behavior|
|Query API|retrieval for verification/demo|
|ML-KEM key lifecycle|Cloud public/private key ownership|
|Public-key endpoint|Gateway obtains ML-KEM public key|
|ML-KEM decapsulation wrapper|shared secret recovery|
|KDF implementation|same key as Gateway|
|Cloud session manager|session creation/lookup/expiry|
|Secure measurement endpoint|secure envelope handling|
|AEAD decryption|authenticated payload recovery|
|Secure validation|reject tampered/invalid messages|
|Cloud failure injection|crypto/storage/service failures|
|Cloud logging|operational + security events|
|Cloud metrics|storage/PQC/decryption observability|
|Health/readiness|deployment-facing service status|
|Unit tests|complete Cloud component coverage|
|Gateway↔Cloud integration tests|real secure round-trip|
|E2E support|measurement persists correctly|
|Documentation|Cloud behavior + limitations|
|AI-history records|prompts/outputs/review decisions|
|Peer review|especially Member 3 crypto code|

---

# Task M4-00 — Review and freeze Cloud boundaries


Before coding, Member 4 must review the corrected shared protocol specification and implement it exactly rather than creating a Cloud-specific variant.

The Cloud supports two application paths.

### Baseline Mode

```text
SECURITY_MODE=classical

Gateway
   ↓
POST /api/v1/baseline/measurements
+ X-Request-ID
   ↓
validate CanonicalMeasurement
   ↓
idempotent storage
```

### Modernized Mode

```text
SECURITY_MODE=mlkem

Gateway
   ↓
GET /api/v1/crypto/public-key
   ↓
POST /api/v1/crypto/sessions
   ↓
POST /api/v1/secure/measurements
   ↓
session validation
   ↓
AES-256-GCM authenticate/decrypt
   ↓
validate CanonicalMeasurement
   ↓
idempotent storage
```

The protocol-v1 crypto contract is frozen:

```text
ML-KEM-768

HKDF-SHA-256
salt = None
info = "ml-kem-project:v1:gateway-cloud-session"
output = 32-byte session key

AES-256-GCM
nonce = 12 bytes / 96 bits

binary JSON encoding = Base64URL

protocol_version = "1"
session TTL = 300 seconds
```

Member 4 and Member 3 must implement exactly the same:

```text
public-key response
session request
session response
Base64URL rules
HKDF parameters and exact fixed info string
session TTL
AAD fields
AAD serialization
SecureEnvelope schema
session-error semantics
ordinary retransmission semantics
```

Frozen AAD fields are exactly:

```text
protocol_version
gateway_id
session_id
request_id
```

Frozen session errors:

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

Frozen security-failure behavior:

```text
fail closed
no runtime plaintext fallback
```

### Trust limitation

The Cloud public key is returned by the explicitly configured Cloud endpoint in the controlled test environment.

ML-KEM provides post-quantum key establishment, but this application-layer protocol does not provide production-grade Cloud identity authentication. Over unauthenticated HTTP, an active attacker able to replace the response could substitute the public key.

Potential future improvements include TLS, mTLS, key pinning, signed key distribution, or PKI.

### Replay limitation

Protocol version `1` has **no dedicated cryptographic anti-replay counter/window**.

Cloud business idempotency on:

```text
(device_id, sequence_number)
```

prevents duplicate logical database rows, but this is not a replacement for cryptographic replay protection.

This limitation must be documented as technical debt.

### Acceptance criteria

```text
[ ] Baseline endpoint frozen
[ ] Secure endpoints frozen
[ ] Crypto parameters match Member 3 exactly
[ ] Fixed HKDF info string frozen
[ ] Four-field AAD frozen
[ ] Same-envelope ordinary retransmission behavior frozen
[ ] Storage schema frozen
[ ] Idempotency policy frozen
[ ] 409 session contract frozen
[ ] No dedicated crypto anti-replay counter/window is documented as technical debt
[ ] No automatic plaintext fallback
[ ] Cloud does not invent independent protocol changes
```

---

# Task M4-01 — Implement Cloud configuration


**Primary file:**

```text
cloud_service/
└── src/
    └── cloud_service/
        └── config.py
```

Recommended configuration:

```text
CLOUD_ID=cloud-001

HOST=0.0.0.0
PORT=9000

DATABASE_URL=sqlite:///...

SECURITY_MODE=classical
SESSION_TTL_SECONDS=300

FAILURE_MODE=none
FAILURE_RATE=0.0
FAILURE_SEED=
FAILURE_DELAY_SECONDS=2

LOG_LEVEL=INFO
```

Supported security modes:

```text
classical
mlkem
```

Terminology:

```text
SECURITY_MODE=classical
→ Baseline Mode

SECURITY_MODE=mlkem
→ Modernized Mode
```

The protocol-v1 crypto suite is fixed and should not be independently configurable:

```text
ML-KEM-768
HKDF-SHA-256
AES-256-GCM
```

### Validation

```text
CLOUD_ID
→ non-empty

PORT
→ valid TCP port

DATABASE_URL
→ valid enough for configured backend

SECURITY_MODE
→ classical | mlkem

SESSION_TTL_SECONDS
→ > 0

FAILURE_RATE
→ 0.0–1.0

FAILURE_MODE
→ supported Cloud mode

FAILURE_DELAY_SECONDS
→ >= 0 if used
```

### Tests

```text
valid defaults
custom environment values
invalid port
invalid database URL
zero session TTL
negative session TTL
unknown security mode
failure rate < 0
failure rate > 1
unknown failure mode
negative processing delay
```

---

# Task M4-02 — Implement Cloud application skeleton

**Primary file:**

```text
app.py
```

The Cloud application should eventually expose:

```text
GET  /health
GET  /ready
GET  /metrics

POST /api/v1/baseline/measurements

GET  /api/v1/crypto/public-key
POST /api/v1/crypto/sessions
POST /api/v1/secure/measurements

GET  /api/v1/measurements
GET  /api/v1/measurements/{record_id}
```

### App responsibilities

```text
load config
initialize logging
initialize storage
initialize crypto
initialize session manager
register routes
manage lifecycle
support graceful shutdown
```

### App must not contain

```text
raw SQL
ML-KEM math
KDF internals
AEAD internals
complex storage logic
```

---

# Task M4-03 — Implement canonical Cloud measurement model

The Cloud receives the Gateway canonical measurement.

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

This must match the shared protocol exactly.

Member 4 must not import Member 2's Gateway model directly.

Both sides implement the same documented contract independently.

### Tests

```text
valid canonical payload parses
field names match protocol
wrong types rejected
missing fields rejected
timestamp formats validated
```

---

# Task M4-04 — Implement Cloud-side canonical validation

Even though the Gateway already validates, Cloud validates again.

This is defense in depth.

Validate:

```text
device_id non-empty

gateway_id non-empty

temperature:
-40 <= x <= 85

humidity:
0 <= x <= 100

measured_at valid UTC/timezone-aware

received_at valid UTC/timezone-aware

0 <= sequence_number <= 9223372036854775807
```

### Additional consistency

Reject larger parsed integers with `422 INVALID_MEASUREMENT` before any SQLite
operation, in both ingestion modes. Tests must persist/query the maximum value
exactly and verify its idempotent retransmission; invalid values store no row.

If secure envelope says:

```text
gateway_id=gateway-001
```

and decrypted payload says:

```text
gateway_id=gateway-002
```

reject.

### Tests

```text
valid canonical measurement
invalid temperature
invalid humidity
invalid measured_at
invalid received_at
negative sequence
empty gateway ID
gateway identity mismatch
```

---

# Task M4-05 — Design and implement stored measurement model

Stored model adds Cloud metadata:

```text
StoredMeasurement
├── record_id
├── device_id
├── gateway_id
├── temperature_c
├── humidity_pct
├── measured_at
├── gateway_received_at
├── cloud_received_at
└── sequence_number
```

Mapping:

```text
Canonical.received_at
→ gateway_received_at
```

Cloud adds:

```text
cloud_received_at
record_id
```

---

# Task M4-06 — Implement SQLite storage initialization

Recommended initial backend:

```text
SQLite
```

because the course encourages keeping the project simple.

Suggested schema:

```text
measurements
├── record_id
├── device_id
├── gateway_id
├── temperature_c
├── humidity_pct
├── measured_at
├── gateway_received_at
├── cloud_received_at
└── sequence_number
```

Potential uniqueness:

```text
UNIQUE(device_id, sequence_number)
```

### Requirements

```text
database initialized at startup
schema reproducible
storage errors translated safely
no session keys/private keys stored here
```

---

# Task M4-07 — Implement storage repository

Suggested package:

```text
storage/
├── database.py
├── repository.py
└── models.py
```

Conceptual API:

```python
save(measurement)
get(record_id)
list(limit, ...)
find_by_device_sequence(device_id, sequence_number)
```

Route handlers should not execute raw SQL directly.

---

# Task M4-08 — Implement Cloud idempotency

This is essential because Gateway retries can resend the same logical measurement.

Logical uniqueness:

```text
(device_id, sequence_number)
```

If already stored:

```text
do not insert duplicate
```

Recommended behavior:

```http
202 Accepted
```

with:

```json
{
  "status": "already_accepted",
  "record_id": "rec-existing"
}
```

### Why

Gateway might send:

```text
request
Cloud stores
response gets lost
Gateway retries
```

Cloud must not create two rows.

---

# Task M4-09 — Idempotency tests

Test:

```text
first insert
→ one row

same device + same sequence again
→ still one row

same device + different sequence
→ two rows

different device + same sequence
→ two rows
```

Also test response semantics.

---

# Task M4-10 — Implement baseline measurement endpoint


Endpoint:

```http
POST /api/v1/baseline/measurements
Content-Type: application/json
X-Request-ID: req-...
```

Processing:

```text
receive canonical JSON
↓
read X-Request-ID for correlation
↓
parse
↓
validate
↓
idempotency check
↓
persist
↓
202
```

The body is `CanonicalMeasurement` only.

`request_id` is **not** inserted into the canonical model or stored as part of the measurement schema merely for tracing.

This endpoint exists for Baseline Mode and controlled before/after comparison.

It should **not** perform ML-KEM or AEAD.

It must never be called automatically because secure processing failed in Modernized Mode.

---

# Task M4-11 — Baseline endpoint tests


Test:

```text
valid canonical measurement stored

X-Request-ID accepted and visible in logs/tracing

request_id not added to CanonicalMeasurement

invalid canonical payload rejected

duplicate returns idempotent success

storage failure handled

cloud_received_at populated

record_id returned
```

Also verify the baseline endpoint is not reached by secure-error fallback logic.

---

# Task M4-12 — Implement measurement query API

Endpoints:

```http
GET /api/v1/measurements
GET /api/v1/measurements/{record_id}
```

Purpose:

```text
integration verification
demonstration
E2E testing
```

This is not intended as a large analytics API.

### Suggested options

```text
?device_id=sensor-001
&limit=100
```

Keep filters minimal.

---

# Task M4-13 — Query API limits

Avoid unbounded result sets.

Recommended:

```text
default limit = 100
maximum = sensible project limit
```

Tests:

```text
empty DB
one result
multiple results
record not found
limit applied
optional device filter
```

---

# Task M4-14 — Support baseline Gateway↔Cloud integration


**Shared with Member 2.**

Before ML-KEM, prove:

```text
Gateway CanonicalMeasurement
+ X-Request-ID
↓
POST /api/v1/baseline/measurements
↓
Cloud validates
↓
SQLite
↓
query API
```

### Acceptance

```text
all canonical fields preserved

X-Request-ID correlation preserved in logs

request_id not inserted into canonical body

CanonicalMeasurement.received_at
→ StoredMeasurement.gateway_received_at

cloud_received_at added

record_id created
```

This baseline must work before secure modernization begins.

---

# Task M4-15 — Record baseline Cloud measurements

Member 4 should help collect:

```text
baseline request latency
storage latency
payload size
successful inserts
duplicate handling
storage failure behavior
```

This contributes to the baseline analysis required by the assignment.

---

# Task M4-16 — Implement Cloud ML-KEM key lifecycle

Member 4 owns the Cloud ML-KEM key pair.

Initial simple lifecycle:

```text
Cloud startup
↓
generate ML-KEM key pair
↓
assign key_id
↓
hold private key in memory
↓
serve public key
↓
shutdown
```

For course scope, ephemeral startup-generated keys are acceptable if documented as technical debt.

### Must not

```text
return private key
log private key
store private key in SQLite
commit private key to repository
write private key to AI history
```

---

# Task M4-17 — Coordinate ML-KEM library with Member 3


Member 3 leads library evaluation, but Member 4 must verify the selected maintained implementation supports the Cloud side of the frozen protocol:

```text
ML-KEM-768 key generation
ML-KEM-768 decapsulation
Python/runtime version
Cloud Docker environment
required byte formats
testability
```

Both members should expose compatible wrapper semantics while keeping vendor/library-specific APIs behind their local wrappers.

Do not choose a different parameter set or crypto suite on the Cloud merely because a library offers other defaults.

---

# Task M4-18 — Implement Cloud ML-KEM wrapper

**Primary file:**

```text
crypto/mlkem.py
```

Conceptual interface:

```python
public_key, private_key = generate_keypair()

shared_secret = decapsulate(
    ciphertext,
    private_key
)
```

Application routes must not directly depend on vendor-specific library APIs.

---

# Task M4-19 — Cloud ML-KEM wrapper tests


Test the Cloud wrapper rather than lattice mathematics.

Required:

```text
key generation succeeds

valid Gateway ML-KEM-768 ciphertext
→ Cloud derives matching shared secret

malformed input/length errors are translated safely where the library reports them

wrapper/API failures are translated safely

private key absent from logs

shared secret absent from logs
```

### Important ML-KEM behavior

Do **not** write a test that assumes:

```text
flip one bit in every valid-length ML-KEM ciphertext
→ decapsulation must raise an exception
```

ML-KEM decapsulation can use implicit rejection semantics. A modified, correctly sized ciphertext may produce pseudorandom keying material instead of a convenient "invalid ciphertext" exception.

Therefore the project should detect end-to-end key mismatch through the later secure/session use rather than relying on a specific exception for every ciphertext mutation.

The explicit `mlkem_decapsulation_failure` failure-injection mode may simulate an application/library failure at the wrapper boundary for resilience testing, but it must be documented as a **simulated failure mode**, not proof that arbitrary ciphertext corruption naturally raises a decapsulation exception.

---

# Task M4-20 — Implement public-key endpoint


Endpoint:

```http
GET /api/v1/crypto/public-key
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

### Validate output

```text
correct protocol version
correct algorithm identifier
non-empty key_id
public key encoded correctly as Base64URL
```

No private material is returned.

### Trust note

This endpoint provides key distribution for the controlled course environment, not production-grade Cloud identity authentication.

Over unauthenticated HTTP, an active attacker could substitute the public key. Production improvements include authenticated TLS, pinning, signed key distribution, or PKI.

---

# Task M4-21 — Implement Cloud KDF wrapper


**Primary file:**

```text
crypto/kdf.py
```

Must match Member 3 exactly.

Frozen contract:

```text
Algorithm:
HKDF-SHA-256

Input key material:
ML-KEM shared secret

Salt:
None

Info:
"ml-kem-project:v1:gateway-cloud-session"

Output:
session_key = 32 bytes
```

Conceptually:

```python
session_key = hkdf_sha256(
    shared_secret,
    salt=None,
    info=b"ml-kem-project:v1:gateway-cloud-session",
    length=32,
)
```

Use a maintained library's HKDF implementation.

Do not replace the frozen design with:

```text
SHA256(shared_secret)
custom concatenation
transcript-bound identity fields
extra confirmation keys
dynamic salt negotiation
dynamic algorithm negotiation
```

---

# Task M4-22 — KDF interoperability test


**Shared with Member 3.**

Test:

```text
Gateway shared secret
Cloud shared secret
↓
same HKDF-SHA-256
same salt=None
same info=b"ml-kem-project:v1:gateway-cloud-session"
same length=32
↓
same session key
```

Also verify that the exact fixed `info` bytes match on both sides.

Do not print the shared secret or derived session key.

Use equality assertions only.

---

# Task M4-23 — Define Cloud secure-session model


Model:

```text
SecureSession
├── session_id
├── gateway_id
├── cloud_key_id
├── created_at
├── expires_at
├── session_key
└── state
```

Possible states:

```text
ACTIVE
EXPIRED
INVALIDATED
CLOSED
FAILED
```

Sessions remain:

```text
in-memory
```

initially.

The session key is secret and must never be serialized, logged, stored in SQLite, or written to AI history.

Protocol version `1` does not define a `message_counter` or dedicated cryptographic replay state.

---

# Task M4-24 — Implement Cloud session manager


**Primary file:**

```text
crypto/session.py
```

Responsibilities:

```text
create session
lookup session
verify gateway ownership
check expiration
invalidate
remove expired sessions
clear all on shutdown
```

Conceptual:

```python
session = session_manager.get(session_id)
```

The session manager does **not** maintain an authenticated message counter or replay window in protocol version `1`.

Duplicate logical persistence is handled separately by Cloud idempotency on `(device_id, sequence_number)`.

---

# Task M4-25 — Implement session-establishment endpoint


Endpoint:

```http
POST /api/v1/crypto/sessions
Content-Type: application/json
```

Request:

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "key_id": "cloud-key-001",
  "encapsulation_ciphertext": "<base64url>"
}
```

Flow:

```text
validate protocol_version
↓
validate gateway_id
↓
validate key_id
↓
Base64URL-decode encapsulation ciphertext
↓
ML-KEM-768 decapsulate
↓
derive 32-byte session_key
using the frozen HKDF contract
↓
create active in-memory session
↓
return versioned session metadata
```

Response:

```json
{
  "protocol_version": "1",
  "session_id": "sess-...",
  "status": "established",
  "expires_at": "2026-09-21T13:50:31Z"
}
```

The shared secret and session key never appear in the response.

Do not create a usable session if request validation, wrapper execution, KDF, or session creation fails.

### Important ML-KEM nuance

Do not assume that every modified, correctly sized ML-KEM ciphertext causes an explicit decapsulation exception.

Malformed encoding or incorrect length may fail directly.

A modified valid-length ciphertext may instead produce different pseudorandom keying material because of ML-KEM implicit-rejection behavior.

Because protocol version `1` has no explicit key-confirmation exchange, an arbitrary valid-length modification is **not guaranteed to be rejected during session establishment itself**. A mismatch may surface during later authenticated communication.

The explicit failure-injection mode for decapsulation/application failure remains useful for testing resilience without making an incorrect claim about primitive behavior.

---

# Task M4-26 — Session endpoint validation


Reject or safely fail on:

```text
unsupported protocol version
missing/empty gateway_id
unknown key_id
invalid Base64URL
malformed/incorrect-length ML-KEM ciphertext where detectable
ML-KEM wrapper/application failure
KDF failure
session creation failure
```

No usable session is created if establishment fails.

Do not assume every modified valid-length ML-KEM ciphertext will produce an explicit decapsulation exception.

A valid-length modified ciphertext may instead yield different pseudorandom keying material. Since protocol version `1` has no explicit key-confirmation exchange, do not claim that arbitrary valid-length modification must be rejected during session setup.

---

# Task M4-27 — Session ownership enforcement

A session belongs to one:

```text
gateway_id
```

If:

```text
session_id=sess-1
belongs to gateway-001
```

then request from:

```text
gateway-002
```

must be rejected.

### Tests

```text
correct gateway succeeds
wrong gateway rejected
```

---

# Task M4-28 — Session expiry


Use:

```text
SESSION_TTL_SECONDS
```

Default:

```text
300
```

On secure-message access:

```text
lookup
↓
expired?
↓
invalidate/remove
↓
return 409 SESSION_EXPIRED
```

Do not silently extend session lifetime.

The Gateway is responsible for one bounded re-establishment attempt after receiving this response.

---

# Task M4-29 — Session expiry tests


Use mocked/controlled time if practical.

Test:

```text
active session accepted

expired session
→ invalidated/removed
→ 409 SESSION_EXPIRED

new Gateway handshake can establish replacement

expired session is never silently extended
```

---

# Task M4-30 — Implement Cloud AEAD decryption wrapper


**Primary file:**

```text
crypto/symmetric.py
```

Frozen algorithm:

```text
AES-256-GCM
```

Inputs:

```text
32-byte session key
12-byte nonce
ciphertext/tag bytes
AAD bytes
```

Conceptual interface:

```python
plaintext = decrypt(
    key,
    nonce,
    ciphertext,
    associated_data,
)
```

On authentication failure:

```text
raise/return a safe application-level secure-message rejection
```

No plaintext may be parsed, logged, or stored after failed authentication.

Do not implement AES, GCM, or tag verification manually.

---

# Task M4-31 — Implement AAD construction identically


AAD fields are exactly:

```text
protocol_version
gateway_id
session_id
request_id
```

Logical object:

```json
{
  "gateway_id": "gateway-001",
  "protocol_version": "1",
  "request_id": "req-...",
  "session_id": "sess-..."
}
```

Frozen encoding:

```text
UTF-8
JSON object
sorted keys
compact separators "," and ":"
no irrelevant whitespace
```

Conceptually:

```python
aad_bytes = json.dumps(
    aad_object,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

This is a strict interoperability contract.

Gateway and Cloud must independently produce byte-identical AAD.

---

# Task M4-32 — AAD interoperability tests


**Shared with Member 3.**

Test:

```text
Gateway AAD bytes == Cloud AAD bytes
```

Then modify one field at a time:

```text
gateway_id
session_id
request_id
protocol_version
```

and prove Cloud cannot authenticate the message.

---

# Task M4-33 — Implement secure-envelope model


Expected:

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

Validate envelope structure before performing expensive cryptographic processing.

Protocol version `1` contains no `message_counter`.

---

# Task M4-34 — Secure-envelope structural validation


Check before expensive secure processing:

```text
protocol_version exists and == "1"

gateway_id present and non-empty

session_id present and non-empty

request_id present and non-empty

nonce is valid Base64URL

ciphertext is valid Base64URL

decoded nonce length == 12 bytes

body/envelope size <= agreed secure-envelope limit

ciphertext non-empty
```

Malformed envelope:

```text
reject before session lookup/decryption where practical
```

The secure endpoint never guesses alternate encodings or algorithms.

---

# Task M4-35 — Implement secure measurement endpoint


Endpoint:

```http
POST /api/v1/secure/measurements
```

Frozen processing order:

```text
parse envelope
↓
validate protocol version / fields / Base64URL / nonce length
↓
lookup session
↓
unknown?
→ 409 SESSION_INVALID
↓
expired?
→ invalidate/remove
→ 409 SESSION_EXPIRED
↓
verify gateway ownership
↓
construct canonical four-field AAD
↓
AES-256-GCM authenticate/decrypt
↓
authentication failure?
→ reject
→ no storage
↓
parse plaintext JSON
↓
validate CanonicalMeasurement
↓
verify decrypted gateway_id consistency
↓
idempotency check / persistence
↓
persist or return already_accepted
↓
202
```

No storage occurs before all cryptographic and application validation succeeds.

### Replay limitation

Protocol version `1` does not implement a dedicated authenticated replay counter/window.

An identical valid envelope may therefore reach application processing again, but Cloud idempotency on `(device_id, sequence_number)` prevents a second logical database row.

Do not claim cryptographic replay rejection in protocol version `1`.

---

# Task M4-36 — Ensure secure endpoint never accepts plaintext


This must be explicit.

Forbidden:

```text
secure-envelope parsing/decryption fails
→ try body as CanonicalMeasurement
```

Modernized Mode:

```text
SECURITY_MODE=mlkem

POST /api/v1/secure/measurements
→ SecureEnvelope only
```

Baseline Mode:

```text
SECURITY_MODE=classical

POST /api/v1/baseline/measurements
→ CanonicalMeasurement only
```

Protocol version `1` implements no runtime plaintext fallback.

A cryptographic failure must remain a failure.

---

# Task M4-37 — Secure-message success response

Recommended:

```http
202 Accepted
```

Body:

```json
{
  "status": "accepted",
  "record_id": "rec-..."
}
```

Duplicate:

```json
{
  "status": "already_accepted",
  "record_id": "rec-existing"
}
```

---

# Task M4-38 — Design safe security error responses


Externally avoid details such as:

```text
AES-GCM tag mismatch
raw cryptographic exception
key/ciphertext internals
```

Use the common project error shape:

```json
{
  "error": {
    "code": "SECURE_MESSAGE_REJECTED",
    "message": "secure message could not be processed"
  }
}
```

Stable secure-path codes include:

```text
SECURE_MESSAGE_REJECTED
UNSUPPORTED_PROTOCOL_VERSION
SESSION_INVALID
SESSION_EXPIRED
INVALID_MEASUREMENT
STORAGE_UNAVAILABLE
INTERNAL_ERROR
```

Detailed diagnostic causes may appear only in safe internal logs where appropriate.

Never leak secret material or create a detailed crypto oracle through error messages.

---

# Task M4-39 — Session-invalid response contract


The session-error contract is frozen.

### Unknown session

```http
409 Conflict
```

```json
{
  "error": {
    "code": "SESSION_INVALID",
    "message": "secure session is invalid"
  }
}
```

### Expired session

```http
409 Conflict
```

```json
{
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "secure session has expired"
  }
}
```

Gateway behavior is:

```text
invalidate local session
↓
obtain current Cloud public key
↓
establish one new session
↓
rebuild a secure envelope under the new session
↓
retry same logical measurement/request_id once
```

Member 4 must not return `401` for these protocol conditions unless the shared protocol is explicitly revised.

---

# Task M4-40 — Base64URL utilities


Centralize Base64URL encoding/decoding for:

```text
public key
ML-KEM encapsulation ciphertext
AES-GCM nonce
AES-GCM ciphertext/tag output
```

Do not mix standard Base64 and Base64URL ad hoc across endpoints.

### Tests

```text
valid round trip
invalid encoding rejected
public-key round trip
ML-KEM ciphertext round trip
12-byte nonce round trip
ciphertext round trip
empty value rejected where protocol requires non-empty data
padding behavior consistent
```

Routes should use the centralized utility rather than duplicate encoding logic.

---

# Task M4-41 — Cloud failure-injection framework

Cloud has its own dedicated failure-injection subsystem.

Suggested:

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

Initial modes:

```text
none
public_key_unavailable
mlkem_decapsulation_failure
session_not_found
session_expired
decryption_failure
storage_failure
processing_delay
service_unavailable
drop_response
random
```

---

# Task M4-42 — Implement `public_key_unavailable`

Endpoint:

```text
/api/v1/crypto/public-key
```

can intentionally return:

```text
503
```

when failure injection triggers.

Purpose:

```text
test Gateway session-establishment resilience
```

---

# Task M4-43 — Implement `mlkem_decapsulation_failure`


This is an **explicit simulated Cloud failure mode** for testing resilience.

Flow:

```text
valid versioned session request
↓
failure injector triggers at ML-KEM wrapper boundary
↓
simulated decapsulation/application failure
↓
no session created
↓
safe log
↓
session-failure metric
↓
Gateway receives establishment failure
```

No fallback to plaintext.

### Important distinction

Do not use this injected mode to claim:

```text
any corrupted valid-length ML-KEM ciphertext naturally raises a decapsulation exception
```

ML-KEM can use implicit rejection behavior. The injected failure exists to test operational handling of a failed crypto/session-establishment operation, not to redefine the primitive's decapsulation semantics.

---

# Task M4-44 — Implement `session_not_found`


Simulate an unknown session on a secure-message request.

Expected:

```text
Cloud returns:
409 SESSION_INVALID
↓
Gateway invalidates local state
↓
Gateway establishes one replacement session
↓
same logical request retried once
```

This tests the frozen bounded session-recovery contract.

---

# Task M4-45 — Implement `session_expired`


Force an active session to behave as expired.

Expected:

```text
secure request
↓
Cloud invalidates/removes session
↓
409 SESSION_EXPIRED
↓
Gateway establishes one replacement session
↓
same logical request retried once
```

No plaintext fallback.

---

# Task M4-46 — Implement `decryption_failure`

Simulate failure after session lookup.

Expected:

```text
no plaintext used
no storage
security failure logged
decryption metric incremented
```

---

# Task M4-47 — Implement `storage_failure`


After successful secure authentication/decryption and canonical validation:

```text
storage layer raises controlled temporary failure
```

Expected:

```text
no false success
↓
503 Service Unavailable
with STORAGE_UNAVAILABLE or equivalent frozen code
↓
Gateway applies bounded transport retry
```

If Baseline Mode hits the same storage failure, the same temporary-service semantics should apply.

Do not turn a failed persistence operation into `202`.

---

# Task M4-48 — Implement `processing_delay`

Optional but useful.

Configuration:

```text
FAILURE_DELAY_SECONDS=2
```

Allows Gateway timeout/retry testing.

Must remain bounded and disabled by default.

---

# Task M4-49 — Implement `service_unavailable`

Simulate:

```text
503 Service Unavailable
```

at appropriate Cloud API boundary.

Purpose:

```text
test Gateway Cloud retry policy
```

---

# Task M4-50 — Implement `drop_response`


This simulates:

```text
Cloud successfully authenticates/processes/stores request
but Gateway does not receive a usable response
```

Scenario:

```text
Gateway sends SecureEnvelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud authenticates/decrypts/stores
↓
response dropped
↓
Gateway performs ordinary transport retry
by resending the SAME already-built SecureEnvelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud authenticates/decrypts again
↓
idempotency sees same (device_id, sequence_number)
↓
Cloud returns 202 already_accepted
↓
only one DB row exists
```

The retry preserves:

```text
same logical measurement
same request_id
same session_id
same nonce
same ciphertext
same AAD
```

Do **not** require a new encryption operation for an ordinary timeout/lost-response retry.

This scenario demonstrates transport retransmission plus business-level idempotency.

It does **not** demonstrate a full cryptographic anti-replay mechanism; protocol version `1` has no dedicated replay counter/window.

---

# Task M4-51 — Failure-injection safety review

Defaults:

```text
FAILURE_MODE=none
FAILURE_RATE=0.0
```

When enabled:

```text
WARNING event=failure_injection_enabled
```

### Critical

Normal mode must not accidentally:

```text
expire sessions
corrupt messages
fail storage
drop responses
```

### Tests

```text
none leaves behavior unchanged
rate 0 never injects
rate 1 always injects
seed deterministic
random mode uses allowed scenarios
```

---

# Task M4-52 — Cloud security logging


Recommended events:

```text
cloud_starting
cloud_ready

public_key_requested

session_establishment_started
session_established
session_establishment_failed
session_expired
session_unknown

secure_measurement_received
secure_envelope_rejected

decryption_succeeded
decryption_failed

measurement_validation_failed
measurement_stored
measurement_duplicate
storage_failed

failure_injected

cloud_shutting_down
```

---

# Task M4-53 — Safe log fields

Good:

```text
request_id
gateway_id
device_id
sequence_number
session_id
key_id
record_id
status
```

Never:

```text
private key
shared secret
session key
database password
token
full .env
```

---

# Task M4-54 — Secret-leakage tests


Create known fake markers.

Exercise:

```text
ML-KEM key generation
decapsulation
KDF
session creation
decryption
failure branches
```

Capture logs and assert:

```text
private key marker absent
shared secret marker absent
session key marker absent
```

This directly supports the assignment's requirement for critical security evaluation of AI-generated artifacts.

---

# Task M4-55 — Cloud metrics


Member 4 owns or co-owns:

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
cloud_duplicate_measurements_total
cloud_storage_failures_total

cloud_injected_failures_total
```

Avoid high-cardinality labels such as:

```text
request_id
session_id
```

---

# Task M4-56 — Metric-label safety

Avoid:

```text
request_id
session_id
record_id
```

as metric labels.

Prefer:

```text
result
reason
security_mode
failure_type
status_class
```

---

# Task M4-57 — Implement `/health`

Purpose:

```text
Is Cloud process alive?
```

Simple:

```json
{
  "status": "ok"
}
```

Do not make `/health` fail simply because SQLite has a temporary problem.

---

# Task M4-58 — Implement `/ready`


Purpose:

```text
Can the Cloud perform useful work in the configured mode?
```

Common checks:

```text
critical configuration valid
storage initialized/reachable
```

In Modernized Mode:

```text
SECURITY_MODE=mlkem
```

also require:

```text
ML-KEM subsystem initialized
Cloud key pair available in memory
session subsystem initialized
AES/KDF dependencies usable
```

In Baseline Mode:

```text
SECURITY_MODE=classical
```

an already initialized ML-KEM session is not required for readiness.

Example Modernized Mode response:

```json
{
  "status": "ready",
  "storage": "ok",
  "mlkem": "available"
}
```

No public/private/session key material is included.

Readiness must not require an active Gateway session; sessions are created lazily.

---

# Task M4-59 — Readiness tests


Test:

```text
Baseline Mode + storage ready
→ ready

Modernized Mode + storage/crypto initialized
→ ready

storage failure
→ not ready

Modernized Mode crypto initialization failure
→ not ready

no active Gateway session yet
→ still may be ready

health may still be alive while ready is false

no secret fields present
```

---

# Task M4-60 — Graceful shutdown

On:

```text
SIGTERM
Ctrl+C
Docker stop
```

Cloud should:

```text
stop accepting new work
↓
clear active session references
↓
close database resources
↓
finish safe shutdown
↓
exit
```

Do not print keys on shutdown.

---

# Task M4-61 — Cloud unit-test suite

Recommended:

```text
cloud_service/tests/
├── test_config.py
├── test_models.py
├── test_validation.py
├── test_storage.py
├── test_repository.py
├── test_baseline_routes.py
├── test_public_key_route.py
├── test_mlkem.py
├── test_kdf.py
├── test_session.py
├── test_symmetric.py
├── test_secure_routes.py
├── test_failure_injector.py
├── test_health.py
└── test_metrics.py
```

---

# Task M4-62 — Storage tests

Test:

```text
insert
retrieve
list
duplicate behavior
different devices
storage failure handling
timestamps preserved
cloud_received_at generated
```

---

# Task M4-63 — Baseline route tests


Test:

```text
valid canonical payload
X-Request-ID received for correlation
request_id not injected into canonical measurement
invalid canonical payload
duplicate
storage failure → 503
successful record ID
received_at maps to gateway_received_at
```

---

# Task M4-64 — Public-key endpoint tests


Test:

```text
correct algorithm
correct protocol version
non-empty key ID
public key decodable as Base64URL
private key never returned
failure injection 503
```

Also verify the response schema matches Member 3 exactly.

---

# Task M4-65 — Session route tests


Test:

```text
valid session establishment

protocol_version="1" required

unsupported protocol version rejected

missing/empty gateway_id rejected

unknown key ID rejected

bad Base64URL rejected

malformed/incorrect-length ML-KEM ciphertext handled safely where detectable

forced/simulated decapsulation failure creates no session

session response contains protocol_version

session ID returned

status="established" returned

expiry returned and in future

no secret material returned
```

Do not assert that every modified valid-length ML-KEM ciphertext must raise a decapsulation exception.

---

# Task M4-66 — Session-manager tests


Test:

```text
create
lookup
gateway ownership
unknown session
expiry
invalidate
cleanup
shutdown clearing
```

Protocol-facing expectations:

```text
unknown session
→ 409 SESSION_INVALID

expired session
→ invalidate/remove
→ 409 SESSION_EXPIRED
```

No session lookup exposes the session key through logs or API responses.

There is no message-counter/replay-state test in protocol version `1`.

---

# Task M4-67 — AEAD/decryption tests


Test the frozen AES-256-GCM contract:

```text
valid Gateway ciphertext decrypts

32-byte key accepted

12-byte nonce required

wrong key rejects

modified ciphertext rejects

modified nonce rejects

modified protocol_version AAD rejects

modified gateway_id AAD rejects

modified session_id AAD rejects

modified request_id AAD rejects

Gateway/Cloud independently build identical four-field AAD bytes

malformed ciphertext rejects safely
```

No storage may occur after failed authentication.

---

# Task M4-68 — Secure-route tests


Test:

```text
valid SecureEnvelope
→ 202

missing protocol_version
→ rejected

unsupported protocol_version
→ rejected

missing gateway_id
→ rejected

missing session_id
→ rejected

missing request_id
→ rejected

bad Base64URL
→ rejected

nonce not 12 bytes
→ rejected

unknown session
→ 409 SESSION_INVALID

expired session
→ 409 SESSION_EXPIRED

wrong gateway/session ownership
→ rejected

tampered ciphertext
→ rejected; no storage

tampered AAD field
→ rejected; no storage

invalid decrypted JSON
→ rejected; no storage

invalid canonical measurement
→ 422; no storage

duplicate logical measurement
→ 202 already_accepted

same already-built SecureEnvelope retransmitted after lost response
→ one logical DB row

storage failure
→ 503

plaintext canonical JSON sent to secure endpoint
→ rejected
```

Document separately that protocol version `1` does not implement a dedicated cryptographic anti-replay counter/window.

---

# Task M4-69 — Gateway↔Cloud baseline contract tests


**Shared with Member 2.**

Verify Member 2 output is accepted exactly.

Body:

```text
CanonicalMeasurement
```

Correlation:

```text
X-Request-ID
```

Required:

```text
field names identical

request_id absent from canonical body

X-Request-ID visible to Cloud logging/tracing

timestamp formats compatible

gateway_id present

CanonicalMeasurement.received_at
→ StoredMeasurement.gateway_received_at

idempotency works
```

No direct imports from Gateway application models.

Use shared fixtures/contracts rather than shared internal model code.

---

# Task M4-70 — Gateway↔Cloud ML-KEM integration tests


**Shared with Member 3.**

Core valid-path test:

```text
Cloud generates ML-KEM-768 key pair

Cloud publishes:
protocol_version
algorithm
key_id
public_key

Gateway validates metadata

Gateway encapsulates
→ secret A + encapsulation ciphertext

Cloud decapsulates
→ secret B

assert secret A == secret B
```

Then derive independently on both sides:

```text
HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32
→ same session_key
```

Also test:

```text
modified valid-length KEM ciphertext
→ do not require explicit decapsulation exception
→ mismatch may surface during later authenticated communication

malformed/incorrect-length ciphertext
→ reject where wrapper/library detects it

explicit simulated wrapper/application decapsulation failure
→ no usable session
```

Do not log or print any shared secret or derived key.

---

# Task M4-71 — Full secure-session integration


Test:

```text
GET /api/v1/crypto/public-key
↓
version/algorithm/key_id validated
↓
Gateway ML-KEM-768 encapsulation
↓
POST /api/v1/crypto/sessions
↓
Cloud ML-KEM-768 decapsulation
↓
both sides derive same session_key
using:
HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32
↓
Cloud returns session_id + status + expires_at
↓
Gateway AES-256-GCM encrypts with fresh 12-byte nonce
↓
Cloud reconstructs identical four-field AAD
↓
Cloud authenticates/decrypts
```

The test should also confirm:

```text
request_id is part of AAD
nonce length is 12 bytes
binary JSON values use Base64URL
```

---

# Task M4-72 — Secure payload round-trip test

Known canonical measurement:

```text
temperature=22.5
humidity=44
sequence=1
```

Gateway encrypts it.

Cloud decrypts.

Assert:

```text
same temperature
same humidity
same sequence
same device
same gateway
```

Then persist.

---

# Task M4-73 — Tampering integration tests


Test:

```text
ciphertext modified
nonce modified
request_id modified
gateway_id modified
session_id modified
protocol_version modified
```

Expected:

```text
reject
no storage
safe metric/log
```

---

# Task M4-74 — Unknown/expired session integration


**Shared with Member 3.**

Test unknown session:

```text
Gateway sends unknown session_id
↓
Cloud returns 409 SESSION_INVALID
↓
Gateway fetches current public key
↓
Gateway establishes one new session
↓
same logical measurement/request_id rebuilt under new session
↓
success
```

Test expired session:

```text
Gateway sends expired session
↓
Cloud invalidates/removes it
↓
Cloud returns 409 SESSION_EXPIRED
↓
Gateway establishes one new session
↓
same logical measurement/request_id rebuilt once
↓
success
```

Also test the recovery bound:

```text
replacement session attempt also fails
→ no infinite loop
→ classified failure upstream
```

---

# Task M4-75 — Idempotent retransmission integration


Important ambiguous-response scenario:

```text
Gateway sends:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud authenticates/decrypts
↓
Cloud stores logical measurement
↓
response deliberately dropped
↓
Gateway retries the SAME already-built SecureEnvelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud authenticates/decrypts same envelope
↓
idempotency detects existing (device_id, sequence_number)
↓
returns 202 already_accepted
↓
only one DB row
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

This demonstrates business-level idempotency under transport retransmission.

Protocol version `1` does not claim cryptographic replay rejection.

---

# Task M4-76 — Cloud storage-failure integration

Use:

```text
FAILURE_MODE=storage_failure
```

Expected:

```text
decrypt succeeds
validation succeeds
storage fails
↓
Cloud returns retryable failure
↓
Gateway retry behavior visible
```

---

# Task M4-77 — Cloud service-unavailable integration

Use:

```text
FAILURE_MODE=service_unavailable
```

Expected:

```text
Gateway receives 503
Gateway retry counter increments
```

---

# Task M4-78 — Full E2E baseline support

Shared with Members 1, 2, and 5:

```text
Legacy
↓
Gateway baseline
↓
Cloud baseline
↓
SQLite
```

Member 4 verifies final storage.

---

# Task M4-79 — Full E2E secure support


Shared with Members 1, 2, 3, and 5:

```text
Legacy
↓
Gateway
↓
ML-KEM-768 session establishment
↓
HKDF-SHA-256
↓
AES-256-GCM SecureEnvelope
↓
Cloud authentication/decryption
↓
SQLite
```

Member 4 verifies:

```text
original logical measurement == stored logical measurement
```

plus:

```text
stored gateway_received_at comes from canonical received_at
cloud_received_at added by Cloud
no duplicate row
ordinary same-envelope retry remains idempotent
```

No Legacy-side ML-KEM knowledge is introduced.

Document that no dedicated cryptographic anti-replay counter/window exists in protocol version `1`.

---

# Task M4-80 — Verify Cloud is unaware of Legacy protocol

Cloud must never depend directly on:

```text
Legacy timestamp field name
Legacy HTTP endpoint
Legacy failure modes
Legacy sensor implementation
```

Cloud only sees:

```text
canonical Gateway model
```

This keeps boundaries clean.

---

# Task M4-81 — Dockerize Cloud Service

Member 4 owns:

```text
cloud_service/Dockerfile
```

Requirements:

```text
correct Python version
uv-compatible install
port 9000
SIGTERM support
SQLite location/configuration
crypto library installs successfully
```

---

# Task M4-82 — SQLite container persistence decision


Member 4 and Member 5 should support/document two practical behaviors.

### Normal development/demo

A named Docker volume may be used so:

```text
Cloud container restart
→ measurement DB persists
```

### Automated/clean tests

Use:

```text
ephemeral database
or
fresh temporary volume
```

so tests are deterministic and independent.

The exact Compose mechanism belongs mainly to Member 5, but Member 4 must ensure `DATABASE_URL` and database initialization support both clean-test and demo workflows.

Do not persist:

```text
ML-KEM private key
session keys
shared secrets
```

in the SQLite volume.

---

# Task M4-83 — Docker readiness verification

From a clean build:

```text
Cloud starts
↓
DB initializes
↓
ML-KEM key pair initializes
↓
/health works
↓
/ready works
```

No local machine-specific assumptions.

---

# Task M4-84 — CI Cloud checks


Member 4 works with Member 5 to ensure CI runs:

```text
Cloud unit tests
storage tests
baseline API tests
ML-KEM tests
session tests
KDF tests
AEAD tests
secure-route tests
same-envelope retransmission/idempotency tests
secret-leakage tests
Gateway↔Cloud integration tests
```

---

# Task M4-85 — AI-history workflow

The course explicitly requires use of AI for code, continuous manual evaluation, prompt documentation, and reporting where/how AI was used.

Good Member 4 AI-history tasks:

```text
Implement SQLite repository

Implement Cloud baseline API

Implement ML-KEM key management

Implement session endpoint

Implement Cloud session manager

Implement AEAD decryption

Implement secure measurement endpoint

Implement Cloud failure injection

Implement Cloud observability
```

Each follows:

```text
start
↓
significant AI interactions
↓
complete implementation
↓
tests/checks
↓
output
↓
human review
↓
accepted / modified / rejected
↓
revision
↓
verification
```

---

# Task M4-86 — Human review checklist for AI-generated Cloud code


Review:

### Correctness

```text
storage schema matches design
received_at maps to gateway_received_at
canonical model correct
baseline X-Request-ID handling correct
public-key response matches frozen schema
session response matches frozen schema
secure endpoint processing order correct
idempotency correct
```

### ML-KEM/KDF

```text
ML-KEM-768
private/public roles correct
no assumption that every ciphertext corruption throws
HKDF-SHA-256
salt=None
info exactly:
"ml-kem-project:v1:gateway-cloud-session"
single 32-byte session key
same semantics as Gateway
```

### AEAD/AAD

```text
AES-256-GCM
32-byte key
12-byte nonce
AAD has exactly four frozen fields:
protocol_version
gateway_id
session_id
request_id
canonical AAD encoding matches Gateway
auth failure stops processing
```

### Session behavior

```text
gateway ownership enforced
TTL enforced
unknown session → 409 SESSION_INVALID
expired session → 409 SESSION_EXPIRED
Cloud never silently extends expiry
```

### Replay/idempotency

```text
no message_counter in protocol v1
no dedicated cryptographic replay counter/window
ordinary ambiguous transport retry resends same already-built SecureEnvelope
business idempotency prevents duplicate rows
technical debt documented honestly
```

### Security

```text
private key never exposed
shared secret never logged
session key never logged
plaintext never accepted on secure route
no runtime plaintext fallback
no detailed crypto oracle in external errors
```

### Maintainability

```text
routes thin
repository isolated
crypto wrappers isolated
session manager independent
failure injection separate
idempotency logic isolated/testable
```

### Reliability

```text
storage failure handled
duplicates handled
same-envelope ambiguous-response retry idempotent
shutdown safe
readiness mode-aware
```

### Testability

```text
clock can be controlled
failure modes deterministic
storage testable
crypto wrappers testable
session behavior testable
idempotency testable
```

---

# Task M4-87 — Document accepted/modified/rejected AI decisions


Useful examples:

```text
AI proposed storing session keys in SQLite.
→ Rejected.
Reason:
session secrets should remain in process memory.
```

```text
AI proposed returning detailed AES-GCM authentication errors.
→ Modified.
Reason:
external errors should remain generic.
```

```text
AI proposed storing duplicate retry requests as separate rows.
→ Rejected.
Reason:
Cloud must be idempotent on (device_id, sequence_number).
```

```text
AI proposed accepting plaintext if SecureEnvelope parsing failed.
→ Rejected.
Reason:
this creates a downgrade path.
```

```text
AI proposed persisting the ML-KEM private key in the project directory.
→ Rejected.
Reason:
protocol v1 uses an ephemeral in-memory Cloud key pair.
```

```text
AI assumed every corrupted valid-length ML-KEM ciphertext must throw a decapsulation exception.
→ Rejected/Modified.
Reason:
ML-KEM can use implicit rejection; do not build correctness around an exception for every modified valid-length ciphertext.
```

```text
AI proposed returning 401 for expired sessions.
→ Modified.
Reason:
the frozen protocol uses 409 SESSION_EXPIRED / SESSION_INVALID for session recovery.
```

```text
AI proposed transcript-bound HKDF with cloud_id/gateway_id/key_id and separate confirmation keys.
→ Rejected/Modified.
Reason:
protocol v1 deliberately uses the simpler fixed HKDF info:
"ml-kem-project:v1:gateway-cloud-session".
```

```text
AI proposed a message_counter and cryptographic replay window.
→ Rejected for protocol v1.
Reason:
dedicated cryptographic anti-replay remains documented technical debt.
```

```text
AI proposed fresh encryption after an ambiguous ordinary HTTP timeout.
→ Rejected/Modified.
Reason:
ordinary protocol-v1 transport retry resends the same already-built SecureEnvelope; re-encryption is needed only after establishing a replacement session.
```

These are useful examples of the critical evaluation required by the course.

---

# Task M4-88 — Cloud documentation contribution


Member 4 should maintain:

```text
docs/architecture/cloud-service.md
```

and Cloud sections of:

```text
docs/architecture/protocol-specification.md
```

Document:

```text
Baseline Mode / Modernized Mode

baseline endpoint
X-Request-ID correlation

secure endpoints

storage model
received_at → gateway_received_at mapping
idempotency

ephemeral ML-KEM-768 key lifecycle

public-key response:
protocol_version
algorithm
key_id
public_key

public-key trust limitation

HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
32-byte session key

session lifecycle
409 SESSION_INVALID
409 SESSION_EXPIRED

AES-256-GCM
12-byte nonce

AAD fields:
protocol_version
gateway_id
session_id
request_id

canonical AAD serialization

SecureEnvelope format
Base64URL encoding

ordinary ambiguous retry:
same already-built SecureEnvelope
same request_id
same session_id
same nonce
same ciphertext
same AAD

session recovery:
replacement session
new encryption under replacement session key
same logical request_id

business idempotency:
(device_id, sequence_number)

no dedicated cryptographic anti-replay counter/window
documented as technical debt

failure injection
ML-KEM implicit-rejection caveat
health/readiness
metrics
logging
trust assumptions
limitations
technical debt
```

---

# Task M4-89 — Cloud technical debt documentation


Expected items:

|Technical debt|Impact|Future improvement|
|---|---|---|
|Ephemeral ML-KEM key pair|key identity changes on restart|secure persistent key management|
|In-memory sessions|restart invalidates sessions|persistent/distributed session store|
|SQLite|limited scale/concurrency|PostgreSQL|
|Simplified Gateway/Cloud identity trust|spoofing/MITM risk|TLS/mTLS/PKI/key pinning|
|No dedicated cryptographic anti-replay counter/window|authenticated envelopes can be replayed at crypto layer|per-session counter/replay window|
|Single Cloud instance|no HA|replicated deployment|
|No HSM/KMS|keys in process memory|HSM/KMS|
|Simple key rotation|limited lifecycle|automated rotation|
|Basic query API|not production analytics|dedicated data service|

Cloud idempotency prevents duplicate logical rows, but it is not cryptographic replay protection.

---

# Task M4-90 — Cloud threat-model contribution


Member 4 should document threats such as:

```text
malformed secure envelope
wrong session
expired session
Gateway identity mismatch
malformed / modified ML-KEM ciphertext
ciphertext tampering
AAD tampering
replay of an authenticated secure envelope
duplicate logical request
storage outage
secret logging
public-key trust limitations
```

For each:

```text
threat
mitigation
remaining risk
```

For replay, state accurately:

```text
business idempotency prevents duplicate rows
but protocol v1 has no dedicated cryptographic anti-replay counter/window
```

---

# Task M4-91 — Baseline vs modernized Cloud evaluation

Member 4 should contribute measurements such as:

```text
baseline request latency

secure request latency

ML-KEM decapsulation duration

storage latency

secure envelope size

duplicate handling behavior

session count

decryption failure behavior
```

Do not invent results.

Measure actual implementation.

---

# Task M4-92 — First-message vs steady-state Cloud analysis

First secure flow includes:

```text
public-key handling
session creation
ML-KEM decapsulation
KDF
```

Later messages include:

```text
session lookup
AEAD decryption
validation
storage
```

Member 4 should help distinguish these in evaluation.

---

# Task M4-93 — PQC observability demonstration

A good demo:

```text
Gateway starts secure communication
↓
Cloud session counter increments
↓
messages reuse session
↓
session expires
↓
new session created
↓
expired-session metric increments
```

This helps satisfy the project's requirement for post-quantum-related observability.

---

# Task M4-94 — Corrupted-ciphertext demo

Use Member 3's Gateway injection:

```text
corrupt_ciphertext
```

Cloud should show:

```text
secure request received
↓
authentication fails
↓
decryption failure metric increments
↓
no storage
```

Excellent presentation scenario.

---

# Task M4-95 — Storage-failure demo

Use:

```text
FAILURE_MODE=storage_failure
```

Demonstrate:

```text
valid encrypted data
↓
Cloud decrypts
↓
storage fails
↓
503
↓
Gateway retries
```

This demonstrates operational failure handling beyond crypto.

---

# Task M4-96 — Peer review Member 3 crypto code


Member 4 is the most important peer reviewer for Member 3 because both implementations must interoperate.

Review:

```text
ML-KEM-768 parameter set
public-key Base64URL format
protocol_version / algorithm / key_id
encapsulation-ciphertext format

HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
32-byte session key

session TTL
409 session recovery

AES-256-GCM
32-byte key
12-byte nonce

AAD four-field content
AAD canonical JSON encoding

SecureEnvelope format
same-envelope ordinary retry semantics

fail-closed behavior
```

Questions:

```text
Does Gateway derive exactly the same session key?

Does Gateway construct byte-identical four-field AAD?

Does Gateway use the correct session ID?

Does Gateway preserve request_id on retry?

Does ordinary transport retry resend the same already-built SecureEnvelope?

Does Gateway re-encrypt only after a replacement session is established?

Does Gateway accidentally log secrets?

Does Gateway treat 409 session errors as bounded re-establishment?

Can Gateway ever silently call the baseline endpoint after secure failure?

Does Gateway rely on invalid assumptions about ML-KEM decapsulation errors?

Does Gateway avoid inventing a message_counter/replay protocol?
```

---

# Task M4-97 — Peer review Member 2 baseline Cloud contract


Review Gateway baseline serialization and request context:

```text
CanonicalMeasurement field names
types
timestamps
gateway_id
received_at

request_id is NOT in canonical body
X-Request-ID carries baseline correlation

response expectations
retry behavior
```

Also verify:

```text
Cloud stores canonical received_at as gateway_received_at
```

Member 4 should flag any mismatch before merge.

---

# Task M4-98 — Peer review Member 5 deployment assumptions

Cloud-related deployment review should verify:

```text
correct port
correct database location
volume behavior
health endpoints
readiness behavior
environment variables
crypto dependency availability
```

---

# Task M4-99 — Dependency review

Cloud dependencies should remain limited to necessary categories:

```text
API framework
validation
SQLite/database access
ML-KEM library
standard crypto library
metrics library if needed
```

Avoid unnecessary:

```text
Redis
Kafka
Celery
distributed database
heavy ORM
```

unless justified.

---

# Task M4-100 — Static quality verification

Before each Cloud PR:

```bash
uv run pytest cloud_service/tests
uv run ruff check cloud_service
uv run ai-history check
```

plus relevant integration tests.

Inspect:

```bash
git status
git diff
```

for:

```text
private keys
DB files if not intended
.env
debug output
temporary ciphertext dumps
unrelated modifications
```

---

# Task M4-101 — Final baseline Cloud review


Before secure modernization:

```text
[ ] configuration works

[ ] app starts

[ ] Baseline Mode endpoint works

[ ] X-Request-ID correlation works

[ ] request_id is not part of CanonicalMeasurement

[ ] validation works

[ ] SQLite works

[ ] received_at → gateway_received_at mapping works

[ ] idempotency works

[ ] query API uses {record_id}

[ ] health/readiness work

[ ] Docker works

[ ] baseline integration passes
```

Freeze and measure baseline behavior before secure code changes.

---

# Task M4-102 — Final modernized Cloud regression


After security integration:

```text
Baseline Mode still works when explicitly configured

Modernized Mode works when SECURITY_MODE=mlkem

public-key endpoint is versioned
and uses Base64URL
and contains no cloud_id protocol field

session endpoint uses:
ML-KEM-768
HKDF-SHA-256
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
32-byte session key

session response contains:
protocol_version
session_id
status
expires_at

secure endpoint works

SecureEnvelope includes:
protocol_version
gateway_id
session_id
request_id
nonce
ciphertext

SecureEnvelope does NOT include message_counter

AAD matches Gateway exactly
and has four fields

AES-256-GCM uses 12-byte nonce

409 SESSION_INVALID works

409 SESSION_EXPIRED works

idempotency unchanged

ordinary ambiguous-response retry:
resends same already-built SecureEnvelope
same request_id
same nonce
same ciphertext
same AAD
and remains idempotent

no dedicated crypto anti-replay counter/window is claimed

query API unchanged

health/readiness unchanged

storage mapping unchanged

failure injection works

no plaintext downgrade

no automatic fallback path exists
```

---

# Task M4-103 — Final Cloud quality pass


Review:

```text
Configuration
✓

Baseline API
✓ X-Request-ID correlation

Canonical validation
✓

Storage
✓ received_at → gateway_received_at

Idempotency
✓

Query API
✓ {record_id}

ML-KEM-768 key lifecycle
✓ ephemeral/in-memory private key

Public-key API
✓ versioned
✓ protocol_version
✓ algorithm
✓ key_id
✓ Base64URL
✓ no cloud_id protocol field

Decapsulation wrapper
✓ implicit-rejection assumptions handled correctly

HKDF-SHA-256
✓ salt=None
✓ info="ml-kem-project:v1:gateway-cloud-session"
✓ one 32-byte session key

Sessions
✓ ownership
✓ TTL
✓ 409 invalid/expired

AES-256-GCM decryption
✓ 12-byte nonce

AAD
✓ four fields
✓ no message_counter
✓ canonical encoding

SecureEnvelope
✓ no message_counter
✓ request_id
✓ nonce
✓ ciphertext

Replay limitation
✓ no dedicated cryptographic anti-replay counter/window
✓ documented as technical debt

Secure endpoint
✓ no plaintext

Ambiguous-response retry
✓ same already-built SecureEnvelope
✓ same request_id
✓ same nonce
✓ same ciphertext
✓ same AAD
✓ idempotent persistence

Failure injection
✓

Logging
✓ secret-safe

Metrics
✓ canonical Cloud metrics
✓ bounded labels

Health/readiness
✓ mode-aware

Docker
✓

Tests
✓

Documentation
✓

AI history
✓
```

Remove:

```text
debug prints
temporary key dumps
unused dependencies
unused routes
unfinished TODOs
test-only hacks in production paths
stale 401 session behavior
stale fallback branches
stale transcript-bound / confirmation-key KDF code from an obsolete protocol variant
stale five-field AAD/message_counter code
stale fresh-encryption ordinary retry logic
```

---

# Recommended Member 4 task order

I would assign the tasks in this sequence:

```text
M4-00  Freeze Cloud boundaries

M4-01  Cloud configuration

M4-02  Application skeleton

M4-03  Canonical Cloud model

M4-04  Canonical validation

M4-05  Stored measurement model

M4-06  SQLite initialization

M4-07  Repository

M4-08  Idempotency

M4-09  Idempotency tests

M4-10  Baseline endpoint

M4-11  Baseline endpoint tests

M4-12  Query API

M4-13  Query limits

M4-14  Baseline Gateway↔Cloud integration

M4-15  Baseline measurements

M4-16  ML-KEM key lifecycle

M4-17  Coordinate crypto library with Member 3

M4-18  Cloud ML-KEM wrapper

M4-19  ML-KEM tests

M4-20  Public-key endpoint

M4-21  Frozen HKDF-SHA-256 wrapper

M4-22  KDF interoperability test

M4-23  Secure session model

M4-24  Session manager

M4-25  Session establishment

M4-26  Session endpoint validation

M4-27  Gateway ownership enforcement

M4-28  Session expiry

M4-29  Session expiry tests

M4-30  AES-256-GCM decryption wrapper

M4-31  Four-field AAD construction

M4-32  AAD interoperability tests

M4-33  SecureEnvelope

M4-34  Envelope validation

M4-35  Secure measurement endpoint

M4-36  Prevent plaintext fallback

M4-37  Success/duplicate response

M4-38  Safe security errors

M4-39  Frozen 409 session-error contract

M4-40  Base64URL utilities

M4-41  Cloud failure-injection framework

M4-42  Public-key-unavailable injection

M4-43  ML-KEM decapsulation failure

M4-44  Session-not-found injection

M4-45  Session-expired injection

M4-46  Decryption-failure injection

M4-47  Storage-failure injection

M4-48  Processing-delay injection

M4-49  Service-unavailable injection

M4-50  Drop-response injection

M4-51  Failure-injection safety review

M4-52  Cloud logging

M4-53  Safe log fields

M4-54  Secret-leakage tests

M4-55  Cloud metrics

M4-56  Metric-label review

M4-57  /health

M4-58  /ready

M4-59  Readiness tests

M4-60  Graceful shutdown

M4-61  Complete unit-test suite

M4-62  Storage tests

M4-63  Baseline route tests

M4-64  Public-key endpoint tests

M4-65  Session route tests

M4-66  Session manager tests

M4-67  AEAD tests

M4-68  Secure route tests

M4-69  Baseline contract tests

M4-70  ML-KEM integration tests

M4-71  Full session integration

M4-72  Secure payload round trip

M4-73  Tamper tests

M4-74  Unknown/expired 409 session-recovery integration

M4-75  Same-envelope retry + idempotency

M4-76  Storage-failure integration

M4-77  Service-unavailable integration

M4-78  Baseline E2E support

M4-79  Secure E2E support

M4-80  Cloud/Legacy boundary verification

M4-81  Dockerfile

M4-82  SQLite persistence decision

M4-83  Docker readiness test

M4-84  CI Cloud checks

M4-85  AI-history workflow

M4-86  Human AI-code review

M4-87  AI decision documentation

M4-88  Cloud documentation

M4-89  Cloud technical debt

M4-90  Cloud threat model

M4-91  Baseline vs modernized evaluation

M4-92  First vs steady-state analysis

M4-93  PQC observability demo

M4-94  Corrupt-ciphertext demo

M4-95  Storage-failure demo

M4-96  Review Member 3 crypto

M4-97  Review Member 2 contract

M4-98  Review Member 5 deployment

M4-99  Dependency review

M4-100 Static quality checks

M4-101 Baseline freeze

M4-102 Modernized regression

M4-103 Final quality pass
```

# Suggested PR breakdown for Member 4

|PR|Scope|
|---|---|
|PR 1|Cloud config + app skeleton|
|PR 2|Storage schema + repository|
|PR 3|Baseline endpoint + idempotency|
|PR 4|Query API|
|PR 5|ML-KEM key lifecycle + public-key endpoint|
|PR 6|Cloud ML-KEM-768 decapsulation + frozen HKDF|
|PR 7|Session manager + session endpoint + 409 errors|
|PR 8|AES-256-GCM decryption + four-field canonical AAD|
|PR 9|SecureEnvelope + secure endpoint + no-plaintext enforcement|
|PR 10|Cloud failure injection|
|PR 11|Cloud logging + health/readiness|
|PR 12|Metrics + PQC observability|
|PR 13|Security/negative tests|
|PR 14|Gateway↔Cloud integration + retry/idempotency/session recovery|
|PR 15|Docker/CI hardening|
|PR 16|Evaluation + documentation|

---

# Member 4 milestone gates

## Gate A — Baseline Cloud ready

Required:

```text
configuration
app
SQLite
baseline endpoint
query API
idempotency
```

## Gate B — Baseline integration ready

Required:

```text
Gateway
→ Cloud
→ SQLite
```

working.

## Gate C — Cloud PQC primitive ready

Required:

```text
ML-KEM-768 key generation
versioned public-key endpoint
decapsulation
HKDF-SHA-256
fixed info="ml-kem-project:v1:gateway-cloud-session"
32-byte session key
```

## Gate D — Secure session ready

Required:

```text
versioned session endpoint
session manager
ownership
expiry
409 SESSION_INVALID / SESSION_EXPIRED
```

## Gate E — Secure Cloud path ready

Required:

```text
SecureEnvelope
AES-256-GCM decryption
canonical four-field AAD
12-byte nonce validation
canonical validation
idempotent storage
no plaintext fallback
```

## Gate F — Failure and operations ready

Required:

```text
failure injection
logging
metrics
health
readiness
Docker
```

## Gate G — Final Cloud complete

Required:

```text
integration tests
E2E
AI review
docs
technical debt
evaluation
CI
peer review
```

---

# Final Definition of Done for Member 4

Member 4 is finished only when:

```text
[ ] Cloud starts from validated configuration.

[ ] Baseline endpoint accepts canonical Gateway measurements.

[ ] Baseline endpoint accepts `X-Request-ID` for correlation.

[ ] `request_id` is not part of `CanonicalMeasurement`.

[ ] Cloud validates canonical measurements independently.

[ ] SQLite storage works.

[ ] Stored schema matches design.

[ ] Canonical `received_at` maps to stored `gateway_received_at`.

[ ] Cloud_received_at is generated correctly.

[ ] Idempotency prevents duplicate logical records.

[ ] Query API can verify stored measurements.

[ ] ML-KEM key pair is generated using maintained implementation.

[ ] ML-KEM private key never leaves Cloud.

[ ] Public-key endpoint returns only public material.

[ ] Public-key response contains `protocol_version="1"`, `algorithm="ML-KEM-768"`, `key_id`, and `public_key`.

[ ] Public key uses Base64URL.

[ ] ML-KEM decapsulation interoperates with Gateway encapsulation.

[ ] Gateway and Cloud derive the same shared secret.

[ ] HKDF-SHA-256 settings match Gateway exactly.

[ ] HKDF uses `salt=None`.

[ ] Gateway and Cloud use the exact same fixed HKDF `info` bytes.

[ ] Derived session key is 32 bytes.

[ ] Derived session keys match.

[ ] Session response contains `protocol_version`, `session_id`, `status`, and `expires_at`.

[ ] Shared/session keys are never logged.

[ ] Session manager supports create, lookup, ownership, expiry and invalidation.

[ ] Sessions are associated with correct gateway_id.

[ ] Unknown sessions return `409 SESSION_INVALID`.

[ ] Expired sessions return `409 SESSION_EXPIRED`.

[ ] Expired sessions are invalidated/removed rather than extended.

[ ] Secure-envelope schema matches protocol.

[ ] SecureEnvelope contains no `message_counter` in protocol version `1`.

[ ] Envelope is validated before crypto processing.

[ ] AAD contains exactly `protocol_version`, `gateway_id`, `session_id`, and `request_id`.

[ ] AAD construction is canonical and byte-compatible with Gateway.

[ ] AES-256-GCM is used for secure-message authentication/decryption.

[ ] Secure nonces decode to exactly 12 bytes.

[ ] Valid secure messages decrypt correctly.

[ ] Modified ciphertext is rejected.

[ ] Modified nonce is rejected.

[ ] Modified AAD is rejected.

[ ] Wrong gateway/session is rejected.

[ ] Plaintext is never accepted by secure endpoint.

[ ] Authentication failure prevents storage.

[ ] Invalid decrypted canonical data prevents storage.

[ ] Ambiguous-response retry preserves the same logical `request_id`.

[ ] Ordinary ambiguous-response retries resend the same already-built `SecureEnvelope`.

[ ] Duplicate logical retries do not create duplicate rows.

[ ] Cloud failure injection supports agreed scenarios.

[ ] Failure injection defaults to disabled.

[ ] ML-KEM decapsulation/application failure can be simulated.

[ ] Tests do not assume every modified valid-length ML-KEM ciphertext must raise an exception.

[ ] Session failures can be simulated.

[ ] Decryption failures can be simulated.

[ ] Storage failures can be simulated.

[ ] Service unavailability can be simulated.

[ ] Dropped-response/idempotency scenario works by retransmitting the same already-built `SecureEnvelope`.

[ ] Cloud logs are useful and secret-safe.

[ ] Secret-leakage tests pass.

[ ] Cloud metrics are meaningful.

[ ] PQC/session/decryption metrics exist.

[ ] /health works.

[ ] /ready works.

[ ] Health/readiness expose no secrets.

[ ] Graceful shutdown works.

[ ] Docker image works from a clean build.

[ ] SQLite persistence behavior is documented.

[ ] Baseline Gateway↔Cloud contract tests pass.

[ ] ML-KEM integration tests pass.

[ ] Secure round-trip tests pass.

[ ] Tamper tests pass.

[ ] Unknown-session recovery works with Gateway.

[ ] Expired-session recovery works with Gateway.

[ ] Session recovery is bounded to one re-establishment attempt.

[ ] Full baseline E2E passes.

[ ] Full secure E2E passes.

[ ] Cloud remains independent from Legacy Device implementation.

[ ] AI-generated Cloud code was manually reviewed.

[ ] Significant prompts/outputs/decisions are recorded.

[ ] Accepted/modified/rejected AI decisions are documented.

[ ] Cloud technical debt is documented.

[ ] Cloud security limitations are documented.

[ ] Simplified public-key trust is documented.

[ ] ML-KEM implicit-rejection caveat is documented.

[ ] Runtime plaintext fallback is explicitly absent.

[ ] Member 3 crypto implementation has been peer reviewed.

[ ] Member 2 baseline contract has been reviewed.

[ ] Deployment assumptions have been reviewed with Member 5.

[ ] Ruff/static checks pass.

[ ] Unit tests pass.

[ ] Security tests pass.

[ ] Integration tests pass.

[ ] AI-history validation passes.

[ ] CI passes.

[ ] Final PR receives teammate review.
```
