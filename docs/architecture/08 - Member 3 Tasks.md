# Member 3 — Gateway Security & PQC Owner

## Overall mission

Member 3 owns the **secure Gateway → Cloud path**.

Their responsibility begins after Member 2 has already produced a valid canonical measurement.

The owned path is:

```text
Canonical Measurement
        ↓
Secure Transport Abstraction
        ↓
Session Manager
        ↓
ML-KEM Encapsulation
        ↓
KDF
        ↓
AEAD Encryption
        ↓
Secure Envelope
        ↓
Cloud Client
```

Member 3 is primarily responsible for:

- selecting and integrating the ML-KEM library;
    
- wrapping ML-KEM safely;
    
- defining and implementing KDF behavior;
    
- managing secure sessions;
    
- implementing AEAD encryption;
    
- constructing authenticated metadata/AAD;
    
- creating secure envelopes;
    
- session expiry/re-key behavior;
    
- fail-closed behavior;
    
- crypto-related failure injection;
    
- crypto observability;
    
- security-specific testing;
    
- secret-safe logging;
    
- integration with Member 4's Cloud crypto implementation.
    

Member 3 does **not** own:

```text
Legacy sensor generation
Legacy HTTP protocol
Gateway input validation
Gateway sequence tracking
Cloud database/storage
Cloud query API
overall CI/CD ownership
```

---

# Member 3 final deliverables

|Deliverable|Expected result|
|---|---|
|ML-KEM library evaluation|justified library choice|
|Gateway ML-KEM wrapper|encapsulation isolated from app code|
|KDF wrapper|deterministic shared session-key derivation|
|Secure session model|lifecycle + expiry|
|Session manager|reuse + re-key|
|AEAD wrapper|authenticated encryption|
|Secure envelope builder|protocol-compliant payload|
|Secure Cloud transport|`/api/v1/crypto/*` + `/api/v1/secure/measurements`|
|Crypto failure injection|handshake/ciphertext/session faults|
|Security logging|no secret leakage|
|PQC metrics|handshake/failure/session observability|
|Crypto unit tests|wrapper-level coverage|
|Gateway↔Cloud integration tests|real secure round trip|
|Negative/security tests|corruption, wrong key, expiry, tampering|
|Documentation|security protocol + limitations|
|AI-history records|prompts, reviews, changes|
|Peer review|Member 4 Cloud security side|

---

# Task M3-00 — Review and freeze the security protocol


Before writing crypto code, Member 3 must review the corrected shared protocol specification and implement it without inventing a parallel variant.

The secure path is frozen as:

```text
Gateway
  ↓
GET /api/v1/crypto/public-key
  ↓
validate protocol_version / algorithm / key_id / public_key
  ↓
ML-KEM-768 encapsulation
  ↓
shared secret
  ↓
HKDF-SHA-256
  ↓
32-byte session key
  ↓
POST /api/v1/crypto/sessions
  ↓
receive session_id + status + expires_at
  ↓
AES-256-GCM
  ↓
SecureEnvelope
  ↓
POST /api/v1/secure/measurements
  ↓
Cloud
```

Protocol version `1` freezes:

```text
ML-KEM-768

HKDF-SHA-256
salt = None
info = "ml-kem-project:v1:gateway-cloud-session"
output = 32 bytes

AES-256-GCM
nonce = 12 bytes / 96 bits

binary JSON encoding = Base64URL

protocol_version = "1"
session TTL = 300 seconds
```

The HKDF contract is deliberately simple and exact:

```text
session_key =
HKDF-SHA-256(
    shared_secret,
    salt=None,
    info=b"ml-kem-project:v1:gateway-cloud-session",
    length=32
)
```

Member 3 must confirm with Member 4 that both sides implement exactly the same:

```text
protocol_version = "1"
gateway_id
key_id
ML-KEM parameter set
public-key encoding
ML-KEM ciphertext encoding
HKDF parameters and exact fixed info string
session TTL
nonce size
AAD fields
AAD serialization
SecureEnvelope fields
session error semantics
retransmission semantics
```

Frozen AAD fields are exactly:

```text
protocol_version
gateway_id
session_id
request_id
```

Frozen session error contract:

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

Frozen security failure policy:

```text
PQC_FAILURE_POLICY=fail_closed
```

There is no runtime plaintext fallback in protocol version `1`.

### Trust limitation

The Cloud public key is fetched from the explicitly configured Cloud endpoint in the controlled test environment.

The protocol does **not** provide production-grade Cloud identity authentication. ML-KEM provides post-quantum key establishment, not endpoint identity authentication.

Potential future improvements include:

```text
HTTPS/TLS
mTLS
public-key pinning
signed key distribution
PKI
```

### Important replay limitation

Protocol version `1` does **not** implement a dedicated cryptographic anti-replay counter/window.

Cloud storage idempotency on:

```text
(device_id, sequence_number)
```

prevents duplicate logical rows, but an authenticated envelope can still be replayed at the cryptographic layer.

This must be documented as technical debt rather than silently replaced by a different protocol.

### Definition of Done

```text
[ ] Shared protocol reviewed
[ ] Member 4 agrees on exact crypto contract
[ ] Member 2 agrees on transport abstraction
[ ] fixed HKDF info string agreed
[ ] four-field AAD agreed
[ ] same-envelope ordinary transport retry semantics agreed
[ ] no dedicated anti-replay counter/window is documented as technical debt
[ ] No coding starts with unresolved cross-component ambiguity
[ ] No local protocol variant introduced
```

---

# Task M3-01 — Evaluate ML-KEM libraries

This should be a standalone research/implementation task.

Member 3 should evaluate candidate Python-compatible libraries for:

```text
ML-KEM support
ML-KEM-768 support
maintenance status
Python version support
installation complexity
API clarity
licensing
testability
documentation quality
whether implementation is actually ML-KEM/FIPS-203 aligned
```

Do **not** simply use the first package an AI suggests.

The course explicitly says to use an existing suitable implementation instead of implementing ML-KEM from scratch.

### Expected output

A small decision record:

```text
Selected library:
...

Why:
...

Rejected alternatives:
...

Known limitations:
...
```

### Human review questions

```text
Is this maintained?
Is this actually suitable for the environment?
Are we relying on a toy implementation?
Does it support our Python version?
Does it expose the required primitives?
```

---

# Task M3-02 — Add the chosen crypto dependency with `uv`

Member 3 should add the chosen dependency through the repository's `uv` workflow.

Requirements:

```text
update correct component pyproject.toml
update uv.lock
do not add requirements.txt
do not commit .venv
document why the dependency exists
```

Member 3 should verify:

```bash
uv sync
```

works from a clean environment.

---

# Task M3-03 — Implement Gateway ML-KEM wrapper

**Primary file:**

```text
edge_gateway/
└── src/
    └── edge_gateway/
        └── crypto/
            └── mlkem.py
```

The rest of the Gateway should not depend directly on vendor/library-specific APIs.

Conceptual interface:

```python
ciphertext, shared_secret = encapsulate(public_key)
```

The wrapper should:

```text
accept Cloud public key
decode/validate as needed
call maintained ML-KEM library
return encapsulation ciphertext
return shared secret internally
translate library errors into app-level exceptions
```

### Must not

```text
log shared_secret
print public key unnecessarily
serialize shared_secret
store shared_secret on disk
implement lattice math manually
```

---

# Task M3-04 — Test ML-KEM encapsulation wrapper

Tests should verify:

```text
valid public key accepted
invalid public key rejected
library exception translated safely
ciphertext returned in expected binary form
shared secret returned only internally
no secret appears in logs
```

Do not test lattice mathematics.

Test the wrapper and integration.

---

# Task M3-05 — Coordinate Cloud ML-KEM key endpoint contract


Member 4 owns Cloud endpoint implementation, but Member 3 owns Gateway consumption.

Expected Cloud endpoint:

```http
GET /api/v1/crypto/public-key
```

Expected response:

```json
{
  "protocol_version": "1",
  "algorithm": "ML-KEM-768",
  "key_id": "cloud-key-001",
  "public_key": "<base64url>"
}
```

Member 3 should implement strict parsing.

Reject:

```text
unsupported protocol_version
wrong algorithm
missing/empty key_id
invalid Base64URL
malformed public key
```

The Gateway uses the public key returned by the explicitly configured Cloud endpoint.

### Important trust limitation

This endpoint does not provide production-grade Cloud identity authentication when used over unauthenticated HTTP.

An active attacker that can replace the response could substitute the public key.

The project must document that limitation and must not claim that ML-KEM itself authenticates the Cloud.

---

# Task M3-06 — Implement public-key client


Member 3 should implement the secure transport's public-key retrieval.

Responsibilities:

```text
GET public key
timeout
transport error classification
response validation
binary decoding
key_id handling
```

Validate:

```text
protocol_version == "1"
algorithm == "ML-KEM-768"
key_id is non-empty
public_key is valid Base64URL / acceptable to the selected ML-KEM wrapper
```

Do not perform ML-KEM in the HTTP client itself.

Keep networking and crypto wrappers separable.

---

# Task M3-07 — Implement KDF wrapper


**Primary file:**

```text
crypto/kdf.py
```

Frozen protocol contract:

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

Both Gateway and Cloud must independently use the same literal `info` bytes.

### Critical requirements

Do not invent:

```text
SHA256(shared_secret)
custom concatenation
custom transcript binding
extra identity fields
multiple derived keys
dynamic algorithm negotiation
```

Use a standard HKDF API from a maintained cryptographic library.

The concrete library is an implementation choice; the KDF contract is not.

---

# Task M3-08 — KDF tests


Test the frozen KDF contract:

```text
same shared secret
+ salt=None
+ info=b"ml-kem-project:v1:gateway-cloud-session"
+ length=32
→ same session key

different secret
→ different session key

session_key length = 32 bytes

Gateway and Cloud derive identical bytes
```

Also verify that the exact fixed `info` value is used byte-for-byte.

No shared secret or derived session key may appear in logs.

---

# Task M3-09 — Define session model


Suggested Gateway session model:

```text
SecureSession
├── session_id
├── cloud_key_id
├── created_at
├── expires_at
├── session_key
└── state
```

Potential state enum:

```text
ESTABLISHING
ACTIVE
EXPIRED
FAILED
CLOSED
```

A session becomes `ACTIVE` after the versioned session-establishment request succeeds and the response is validated.

### Secret-handling rule

The session key must:

```text
remain in memory
never be serialized
never be logged
never be stored in SQLite
never be written to AI history
```

---

# Task M3-10 — Implement session manager


**Primary file:**

```text
crypto/session.py
```

Responsibilities:

```text
return current active session
detect expiry
establish new session when needed
invalidate failed session
close/clear session
prevent duplicate simultaneous handshakes
```

Conceptual interface:

```python
session = await session_manager.get_or_establish()
```

For the initial project, use one simple async session-establishment lock so concurrent requests do not create unnecessary duplicate handshakes.

No per-session cryptographic message counter is implemented in protocol version `1`.

---

# Task M3-11 — Handle concurrent session establishment


Concurrent requests may both observe that no active session exists.

Potential race:

```text
Request A arrives
→ no session

Request B arrives
→ no session

both attempt ML-KEM handshake
```

Use a simple:

```text
async lock
```

around session creation.

Expected:

```text
two concurrent requests
→ one logical session establishment
```

Ordinary secure sends do not require a replay-counter serialization mechanism in protocol version `1`, because the protocol does not define a cryptographic message counter/window.

Do not build distributed locking.

---

# Task M3-12 — Implement session establishment protocol


Gateway flow:

```text
GET /api/v1/crypto/public-key
↓
validate protocol_version / algorithm / key_id
↓
Base64URL-decode public key
↓
ML-KEM-768 encapsulate
↓
derive session_key with frozen HKDF
↓
POST /api/v1/crypto/sessions
↓
validate versioned response
↓
store session as ACTIVE
```

Cloud endpoint:

```http
POST /api/v1/crypto/sessions
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

Response:

```json
{
  "protocol_version": "1",
  "session_id": "sess-...",
  "status": "established",
  "expires_at": "2026-09-21T13:50:31Z"
}
```

The shared secret and session key never cross the network.

### ML-KEM implicit-rejection nuance

Do not assume that every modified, correctly sized ML-KEM ciphertext must cause an explicit decapsulation exception.

Malformed encoding or incorrect length may be rejected directly by the wrapper/library.

A modified valid-length ciphertext may instead result in different pseudorandom keying material.

Because protocol version `1` does not include an explicit key-confirmation exchange, arbitrary valid-length KEM-ciphertext modification is **not guaranteed to be rejected during session establishment itself**. A mismatch may surface when later authenticated communication fails.

Use explicit failure injection to test direct wrapper/application decapsulation-failure handling without making a false claim about all valid-length modifications.

---

# Task M3-13 — Session-establishment validation


Member 3 should validate:

```text
protocol_version
session_id non-empty
status == "established"
expires_at present
expiry parses correctly
expiry is in the future
```

The Gateway must reject malformed session responses and must not create an active local session from invalid metadata.

On establishment failure:

```text
discard provisional session state
do not send secure application data
return classified failure
log safely
increment failure metric
```

---

# Task M3-14 — Session establishment integration test


**Shared with Member 4.**

Test the normal valid path:

```text
Cloud key pair
↓
Gateway fetches versioned public key
↓
Gateway encapsulates
↓
Cloud decapsulates
↓
both sides derive the same session_key
from the same shared secret
using the frozen HKDF parameters
↓
Cloud returns session_id + status + expires_at
↓
Gateway stores active session
```

Verify:

```text
valid encapsulation produces matching shared secret
session_key bytes match
session_id association matches
expiry assumptions match
gateway ownership matches
```

Do not print any derived secret or key bytes.

### ML-KEM nuance

Also test:

```text
malformed/incorrect-length KEM input
→ wrapper/library rejection where applicable

explicit injected wrapper/application decapsulation failure
→ session establishment failure
```

Do **not** require every modified valid-length ML-KEM ciphertext to throw an explicit exception. A valid-length modification may yield different pseudorandom keying material and the mismatch can surface later during authenticated application communication.

---

# Task M3-15 — Implement session reuse

The Gateway must not do ML-KEM for every measurement.

Expected:

```text
Message 1
→ handshake
→ encrypted send

Message 2
→ reuse session

Message 3
→ reuse session
```

### Test

Count ML-KEM handshake calls.

For example:

```text
3 measurements
1 handshake
```

while session remains active.

---

# Task M3-16 — Implement session expiry

Default:

```text
SESSION_TTL_SECONDS=300
```

Member 3 should check local expiration before encrypting.

If expired:

```text
discard/close old session
↓
establish new session
```

Cloud independently checks too.

---

# Task M3-17 — Session expiry tests

Use a very short test TTL.

Example:

```text
TTL=1 second
```

Test:

```text
establish session
↓
use once
↓
advance/mock time
↓
session expired
↓
next request triggers new handshake
```

Do not make tests sleep in real time if avoidable.

Inject/mock clock where useful.

---

# Task M3-18 — Handle Cloud session-invalid response


The Cloud uses the frozen session-recovery contract:

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

Member 3 should map either result to:

```text
discard/invalidate local session
↓
GET /api/v1/crypto/public-key
↓
establish one new ML-KEM session
↓
retry the same logical secure request once
```

Important:

```text
409 session errors are NOT ordinary repeated HTTP retries
```

The recovery attempt is bounded to one re-establishment per send operation.

If recovery fails again:

```text
return classified failure upstream
```

Do not loop indefinitely and do not call the baseline endpoint.

---

# Task M3-19 — Implement AEAD wrapper


**Primary file:**

```text
crypto/symmetric.py
```

The algorithm is frozen:

```text
AES-256-GCM
```

Inputs:

```text
32-byte session key
12-byte nonce
plaintext bytes
AAD bytes
```

Conceptual interface:

```python
ciphertext = encrypt(
    key,
    nonce,
    plaintext,
    associated_data,
)
```

The wrapper should isolate library-specific details while application code remains generic.

No custom AES, GCM, tag handling, or authentication logic should be implemented manually.

---

# Task M3-20 — Nonce generation


The frozen AES-256-GCM nonce size is:

```text
12 bytes / 96 bits
```

For every **new encryption operation**, generate a fresh nonce using cryptographically secure randomness from the crypto/system library.

Never use:

```text
random.random()
timestamp
sequence_number alone
fixed nonce
failure-injection seeded PRNG
```

### Security invariant

Never intentionally reuse a nonce with the same session key for two different encryption operations.

### Ordinary ambiguous/lost-response retry rule

If the Gateway has already built and sent a `SecureEnvelope` but does not receive a usable response, the transport retry must resend the **same already-built SecureEnvelope**:

```text
same request_id
same nonce
same ciphertext
same AAD
same session_id
```

Do **not** re-encrypt the same plaintext with the same session key for an ordinary HTTP retry.

This is a retransmission of the same ciphertext, not a second encryption operation.

Cloud business idempotency on:

```text
(device_id, sequence_number)
```

prevents duplicate database rows if the earlier request was already committed.

---

# Task M3-21 — AEAD unit tests

Test:

```text
encrypt/decrypt round trip

wrong key fails

modified ciphertext fails

modified nonce fails

modified AAD fails

empty/invalid key rejected

nonce length validation
```

A tampered payload must not produce usable plaintext.

---

# Task M3-22 — Define canonical plaintext serialization

Before encryption, canonical measurement becomes UTF-8 JSON.

Member 3 must ensure serialization is deterministic enough for tests.

Rules:

```text
UTF-8
valid JSON
no NaN
no Infinity
agreed field names
UTC timestamp strings
```

This plaintext comes from Member 2's canonical model.

Member 3 must not change its meaning.

---

# Task M3-23 — Implement AAD construction


Authenticated but visible metadata is exactly:

```text
protocol_version
gateway_id
session_id
request_id
```

Use one canonical JSON object:

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

Cloud must independently produce byte-identical AAD.

Do not concatenate raw strings ambiguously.

---

# Task M3-24 — AAD interoperability test


**Shared with Member 4.**

Test:

```text
Gateway builds AAD
Cloud independently builds AAD
bytes identical
```

Then modify one field:

```text
gateway_id
session_id
request_id
protocol_version
```

and prove authentication fails.

---

# Task M3-25 — Implement secure envelope builder


Envelope:

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

Responsibilities:

```text
generate fresh 12-byte nonce
serialize canonical measurement
build four-field AAD
AES-256-GCM encrypt
Base64URL-encode nonce
Base64URL-encode ciphertext
build protocol object
```

The envelope deliberately contains no `message_counter` in protocol version `1`.

---

# Task M3-26 — Secure envelope tests


Test:

```text
required fields present
protocol version correct
gateway ID correct
session ID correct
request ID preserved
nonce decodes to exactly 12 bytes
ciphertext decodes
no plaintext measurement appears in envelope
message counter is absent
```

The plaintext measurement must never appear directly in the secure envelope.

---

# Task M3-27 — Implement secure Cloud transport

Expected endpoint:

```http
POST /api/v1/secure/measurements
```

Member 3 should implement:

```text
get/reuse session
encrypt measurement
construct envelope
send HTTP request
interpret response
handle session-specific failures
classify permanent vs transient failures
```

---

# Task M3-28 — Integrate with Member 2's transport abstraction

Member 2 should call a clean abstraction.

Conceptually:

```python
result = secure_transport.send(
    canonical_measurement,
    request_id=request_id
)
```

Member 2 should not care about:

```text
ML-KEM public key
session key
nonce
AES-GCM
Base64URL
```

This task is successful when secure transport can replace baseline transport without changing the Legacy route.

---

# Task M3-29 — Implement security-mode behavior


Member 3 works with Member 2 on the two explicit project modes.

### Baseline Mode

```text
SECURITY_MODE=classical
```

Member 2's baseline transport handles:

```text
POST /api/v1/baseline/measurements
```

Member 3's secure crypto path is not used.

### Modernized Mode

```text
SECURITY_MODE=mlkem
```

Member 3's secure transport handles:

```text
ML-KEM-768
HKDF-SHA-256
AES-256-GCM
POST /api/v1/secure/measurements
```

Modernized Mode must never fall through to plaintext automatically.

The same Legacy API remains unchanged in both modes.

---

# Task M3-30 — Implement fail-closed policy


Protocol version `1` supports only:

```text
PQC_FAILURE_POLICY=fail_closed
```

If ML-KEM, session establishment, key derivation, encryption, or secure transport setup fails:

```text
log safely
↓
increment appropriate metric
↓
return classified failure
↓
do not send baseline plaintext
```

Forbidden behavior:

```text
secure path failed
→ POST /api/v1/baseline/measurements
```

Member 3 should make the no-downgrade rule explicit in code structure and tests, not merely rely on convention.

### Required integration test

```text
SECURITY_MODE=mlkem
+ injected ML-KEM failure
→ zero calls to /api/v1/baseline/measurements
```

---

# Task M3-31 — Verify runtime plaintext fallback is absent


This task is no longer an optional feature-development task.

Protocol version `1` deliberately **does not implement runtime classical fallback**.

Member 3 should instead verify that no fallback path exists accidentally.

Required checks:

```text
PQC_FAILURE_POLICY accepts fail_closed only

no explicit_classical_fallback branch exists

SecureTransport cannot silently instantiate/call BaselineTransport

ML-KEM failure does not call baseline endpoint

session-establishment failure does not call baseline endpoint

AES-GCM/encryption failure does not call baseline endpoint
```

The baseline endpoint remains available only for an explicit Baseline Mode run:

```text
SECURITY_MODE=classical
```

Switching from Modernized Mode to Baseline Mode requires an explicit configuration/operator decision outside the failed request.

### Definition of Done

```text
[ ] Runtime fallback absent
[ ] Tests prove no baseline call on secure failure
[ ] Documentation describes fail-closed behavior
[ ] No stale optional-fallback configuration remains
```

---

# Task M3-32 — Crypto failure-injection framework

Member 3 owns crypto-specific Gateway fault injection.

Initial modes:

```text
mlkem_handshake_failure

corrupt_ciphertext

session_missing

session_expired
```

Potentially:

```text
encryption_failure
```

if useful.

The failure injector must not alter the normal path when disabled.

---

# Task M3-33 — Implement `mlkem_handshake_failure`


Simulate handshake failure before an active session is created.

Expected:

```text
valid canonical measurement
↓
session required
↓
injected handshake failure
↓
no session
↓
safe log
↓
failure metric
↓
classified failure upstream
```

Because protocol version `1` is fail-closed:

```text
no baseline endpoint call
```

This failure mode should be one of the explicit no-downgrade integration tests.

---

# Task M3-34 — Implement `corrupt_ciphertext`

Important security scenario:

```text
correct encryption
↓
failure injector mutates ciphertext
↓
send to Cloud
↓
Cloud AEAD auth fails
↓
Cloud rejects
```

This is better than corrupting plaintext before encryption because it proves authenticated encryption detects tampering.

### Requirements

```text
do not corrupt session key
do not persist corruption
do not log secret bytes
```

---

# Task M3-35 — Implement `session_missing`

Simulate loss of local session state.

Expected:

```text
Gateway thinks session unavailable
↓
new handshake
```

This can test re-establishment logic.

---

# Task M3-36 — Implement `session_expired`

Force local session expiry.

Expected:

```text
active session
↓
injected expiry
↓
new handshake
↓
new session
```

This should not produce insecure fallback.

---

# Task M3-37 — Crypto failure-injection safety review

Defaults:

```text
FAILURE_MODE=none
FAILURE_RATE=0.0
```

When a crypto fault is enabled:

```text
WARNING event=failure_injection_enabled
```

No secret values in warning.

### Tests

```text
mode=none does not alter ciphertext
rate=0 never injects
rate=1 always injects
seed deterministic
normal secure transport unaffected when disabled
```

---

# Task M3-38 — Implement crypto/security logging


Member 3 owns events such as:

```text
mlkem_public_key_received

mlkem_handshake_started
mlkem_handshake_succeeded
mlkem_handshake_failed

session_created
session_reused
session_expired
session_invalidated
session_reestablishment_started
session_reestablishment_succeeded
session_reestablishment_failed

encryption_succeeded
encryption_failed

secure_delivery_started
secure_delivery_rejected

pqc_fail_closed
```

Useful fields:

```text
request_id
gateway_id
session_id
key_id
result
duration
reason
```

Never log:

```text
private key
shared secret
session key
raw key bytes
```

There is no runtime fallback event in protocol version `1` because runtime fallback is not implemented.

---

# Task M3-39 — Secret-leakage tests


Create known test secrets/markers.

Run:

```text
handshake
KDF
session creation
encryption
failure paths
```

capture logs and assert:

```text
shared secret absent
session key absent
private key absent
```

Also inspect exceptions/string representations if practical.

---

# Task M3-40 — PQC metrics


Member 3 owns or co-owns:

```text
gateway_mlkem_handshakes_total
gateway_mlkem_handshake_failures_total
gateway_mlkem_handshake_duration_seconds

gateway_session_reestablishments_total
gateway_active_session

gateway_encryption_failures_total

gateway_pqc_fallback_total
```

`gateway_pqc_fallback_total` should remain:

```text
0
```

in protocol version `1`, because runtime PQC fallback is not implemented.

Avoid high-cardinality labels such as:

```text
request_id
session_id
```

Member 5 helps export/standardize these metrics.

---

# Task M3-41 — Metric-label safety


Do not use:

```text
session_id
request_id
raw key_id if unbounded
device_id at high cardinality
```

as uncontrolled metric labels.

Prefer:

```text
result
reason
security_mode
failure_type
```

---

# Task M3-42 — Handshake timing measurement

The project benefits from measuring ML-KEM overhead.

Member 3 should measure:

```text
public key retrieval duration

encapsulation duration

session establishment total duration
```

At minimum:

```text
gateway_mlkem_handshake_duration_seconds
```

Do not mix first-message handshake cost with steady-state encryption cost.

---

# Task M3-43 — First-message vs steady-state measurement

Member 3 should help evaluate:

```text
first secure message
```

versus:

```text
subsequent secure message
```

because first request includes handshake.

This supports the final baseline vs modernized evaluation.

---

# Task M3-44 — Secure transport retry semantics


Member 3 must distinguish three categories.

### Retryable transport/service failure

```text
timeout
connection error
500
502
503
504
```

These use the normal bounded Cloud transport retry policy.

For an ordinary retry after an ambiguous or lost response, resend the **same already-built SecureEnvelope**:

```text
same request_id
same nonce
same ciphertext
same AAD
same session_id
```

Do not perform a fresh encryption for an ordinary transport retry.

### Session-recovery condition

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

These do **not** enter the ordinary repeated HTTP retry loop.

Instead:

```text
invalidate local session
→ fetch current Cloud public key
→ establish one new session
→ rebuild one secure envelope under the new session
→ retry same logical request once
```

### Permanent/security failure

```text
400 malformed/tampered secure message
422 invalid decrypted canonical measurement
unsupported protocol version
cryptographic rejection
gateway/session ownership rejection
```

Do not blindly retry permanent failures.

No category triggers automatic Baseline Mode fallback.

---

# Task M3-45 — Session-recovery retry bound


The recovery policy is frozen:

```text
maximum one session re-establishment
per secure send operation
```

Avoid:

```text
session invalid
→ recreate
→ invalid
→ recreate
→ forever
```

Flow:

```text
first 409 SESSION_INVALID / SESSION_EXPIRED
→ invalidate session
→ fetch current public key
→ establish one new session
→ rebuild secure envelope under new session
→ retry same logical measurement/request_id once
```

If that recovery fails:

```text
return classified failure upstream
```

Normal bounded transport retry remains a separate mechanism.

---

# Task M3-46 — Avoid retrying same nonce/envelope incorrectly


The protocol-v1 retransmission rule distinguishes **ordinary transport retry** from **new-session recovery**.

### Ordinary transport retry

If an HTTP attempt becomes ambiguous after the Gateway already sent a valid secure envelope:

```text
same already-built SecureEnvelope
same request_id
same session_id
same nonce
same ciphertext
same AAD
```

This is safe because no second AES-GCM encryption operation is performed; the existing ciphertext is merely retransmitted.

### Session recovery

If the Cloud returns:

```text
409 SESSION_INVALID
409 SESSION_EXPIRED
```

the old session cannot be reused.

Then:

```text
establish one new session
→ generate a new nonce
→ encrypt again under the new session key
→ preserve the same logical request_id
→ send one rebuilt SecureEnvelope
```

Cloud business idempotency on:

```text
(device_id, sequence_number)
```

prevents duplicate logical rows if the first request was already committed.

### Technical debt

Protocol version `1` does not implement a dedicated authenticated replay counter/window. That limitation must remain visible in documentation and tests.

---

# Task M3-47 — Secure retransmission/idempotency integration


**Shared with Member 4.**

Test the ambiguous-response case:

```text
Gateway builds secure envelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Gateway sends envelope
↓
Cloud authenticates/decrypts and stores
↓
response is lost/simulated timeout
↓
Gateway retries the SAME envelope:
request_id=req-1
nonce=N1
ciphertext=C1
↓
Cloud decrypts same logical request
↓
business idempotency detects existing (device_id, sequence_number)
↓
Cloud returns 202 already_accepted
↓
only one DB row exists
```

Verify:

```text
same request_id
same nonce
same ciphertext
same session_id
one stored logical record
```

Also document that this test demonstrates transport retransmission + business idempotency, **not** a full cryptographic anti-replay mechanism.

---

# Task M3-48 — Tamper tests


Create tests for:

```text
ciphertext bit changed
nonce changed
gateway_id changed
session_id changed
request_id changed
protocol_version changed
```

Expected:

```text
Cloud rejects authentication
or protocol validation rejects before decrypt
```

No data stored.

Do not claim that protocol version `1` provides a full cryptographic replay window/counter.

---

# Task M3-49 — Wrong-session test

Establish:

```text
Session A
Session B
```

Encrypt using A.

Send envelope claiming B.

Expected:

```text
Cloud fails authentication
```

This proves session binding is meaningful.

---

# Task M3-50 — Wrong-gateway/session ownership test

If Cloud associates:

```text
sess-1
→ gateway-001
```

attempt:

```text
gateway_id=gateway-002
session_id=sess-1
```

Expected:

```text
rejected
```

Member 3 should help Member 4 test this.

---

# Task M3-51 — Unsupported protocol-version test

Send:

```text
protocol_version="999"
```

Expected:

```text
rejected before secure processing
```

Gateway should not automatically downgrade.

---

# Task M3-52 — Base64URL encoding utilities


Binary values transported through JSON use **Base64URL** consistently.

Centralize:

```text
encode_binary
decode_binary
```

for:

```text
Cloud public key
ML-KEM encapsulation ciphertext
AES-GCM nonce
AES-GCM ciphertext/tag output
```

Avoid ad hoc standard-Base64/Base64URL mixtures.

### Tests

```text
round trip
invalid alphabet/encoding rejected
empty values rejected where protocol requires non-empty data
padding behavior consistent
public-key round trip
ML-KEM ciphertext round trip
12-byte nonce round trip
ciphertext round trip
```

Network models should validate decoded lengths where the selected cryptographic primitive defines them.

---

# Task M3-53 — Public-key trust limitation documentation


The current design assumes the Gateway trusts the explicitly configured Cloud endpoint sufficiently to consume its ML-KEM public key.

Member 3 must explicitly document:

```text
ML-KEM itself does not authenticate Cloud identity
```

and the project does not implement full production PKI.

The public-key response contains:

```text
protocol_version
algorithm
key_id
public_key
```

Over unauthenticated HTTP, an active attacker could substitute the public key.

Potential production improvements:

```text
HTTPS/TLS
certificate validation
public-key pinning
signed key distribution
PKI
```

Do not claim the current design solves this fully.

---

# Task M3-54 — Review transport-level TLS decision


The course test-environment trust decision is frozen:

```text
Docker/test communication may use HTTP
+
application-layer ML-KEM-768 / AES-256-GCM protection
```

The project does **not** claim this is production-grade endpoint authentication.

Member 3 should ensure documentation clearly states:

```text
application-layer post-quantum key establishment
and authenticated encrypted Gateway↔Cloud payloads
are demonstrated
```

while the following remain outside the initial implementation:

```text
production TLS certificate lifecycle
mTLS
PKI
public-key pinning
signed key distribution
```

This is a documented trust-model limitation, not an unresolved implementation choice.

Key confirmation improves session consistency but does not remove the unauthenticated public-key substitution risk.

Do not add HTTPS/mTLS complexity unless the team explicitly revises the shared protocol.

---

# Task M3-55 — Session-memory handling review

Member 3 should keep session secrets in process memory only.

Avoid:

```text
debug dumps
cache file
SQLite
JSON state
AI history
test snapshots containing real key bytes
```

On session replacement:

```text
old session object should be dereferenced/cleared
```

Python does not guarantee secure memory zeroization, so document that as a limitation rather than making false claims.

---

# Task M3-56 — Graceful shutdown security behavior

On Gateway shutdown:

```text
stop accepting work
↓
close secure transport
↓
clear active session references
↓
close HTTP client
```

Member 2 owns app lifecycle; Member 3 owns security cleanup.

No key material should be printed during shutdown.

---

# Task M3-57 — Crypto unit-test structure

Recommended:

```text
edge_gateway/tests/
├── test_mlkem.py
├── test_kdf.py
├── test_session.py
├── test_symmetric.py
├── test_secure_envelope.py
├── test_secure_transport.py
└── test_crypto_failures.py
```

---

# Task M3-58 — Gateway↔Cloud secure integration-test suite


**Shared with Member 4.**

Required:

```text
versioned public-key retrieval

ML-KEM-768 session establishment

Gateway/Cloud matching shared secret on valid encapsulation

fixed HKDF interoperability:
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32

secure envelope round trip

byte-identical four-field AAD construction

Cloud decrypts original canonical measurement

session reuse

local session expiry

409 SESSION_EXPIRED recovery

409 SESSION_INVALID recovery

one-recovery-attempt bound

corrupted AEAD ciphertext rejection

nonce tampering rejection

AAD tampering rejection

wrong session rejection

wrong gateway/session ownership rejection

unsupported protocol version rejection

malformed ML-KEM input handling where detectable

simulated Cloud ML-KEM wrapper/decapsulation failure

ML-KEM implicit-rejection caveat covered in tests/docs

Cloud decryption failure

fail-closed no-baseline-call behavior

same-envelope ordinary transport retry after ambiguous response

idempotent duplicate persistence
```

Do not include tests that assume:

```text
every modified valid-length ML-KEM ciphertext must raise
```

and do not claim that protocol v1 implements a dedicated cryptographic replay counter/window.

---

# Task M3-59 — Full E2E secure-system support

Once all components exist:

```text
Legacy
↓
Gateway validation
↓
Member 3 secure transport
↓
Cloud
↓
Storage
```

Member 3 verifies that security changes do not alter the measurement.

Assert:

```text
original temperature == stored temperature
original humidity == stored humidity
original sequence == stored sequence
```

---

# Task M3-60 — Legacy compatibility regression


This is critical.

Member 3's work must not require changes to Member 1's Legacy Device.

Run the same Legacy implementation with:

```text
Baseline Mode
SECURITY_MODE=classical
```

then:

```text
Modernized Mode
SECURITY_MODE=mlkem
```

The Legacy contract remains:

```text
POST /api/v1/measurements
same JSON schema
same Legacy-side response/retry semantics
```

If Legacy needs to learn about:

```text
ML-KEM
session_id
nonce
Cloud public key
AES-GCM
```

the architecture has failed.

Member 3 should verify only the Gateway→Cloud transport/security boundary changes.

---

# Task M3-61 — Docker integration

Member 3 should verify chosen crypto libraries install correctly inside Gateway Docker image.

Potential issues:

```text
native extension compilation
platform support
missing build dependency
architecture incompatibility
```

This must be tested early, not at project end.

---

# Task M3-62 — Clean-container crypto test

From a clean image:

```text
build Gateway
start Cloud
establish ML-KEM session
send secure measurement
```

No local developer environment assumptions.

---

# Task M3-63 — CI crypto checks

Member 3 should work with Member 5 to ensure CI includes:

```text
ML-KEM wrapper tests
KDF tests
AEAD tests
secure-envelope tests
key-confirmation tests
replay limitation tests
secure integration tests
secret-leakage tests
```

Do not rely solely on unit tests from other modules.

---

# Task M3-64 — AI-history workflow

Member 3's tasks are ideal candidates for detailed AI-history because crypto code must be treated as untrusted.

Possible history tasks:

```text
Evaluate ML-KEM Python libraries

Implement ML-KEM wrapper

Implement HKDF wrapper

Implement secure session manager

Implement AES-GCM wrapper

Implement secure envelope

Implement secure Cloud transport

Implement crypto failure injection
```

For every significant task:

```text
start
↓
record important interactions
↓
agent completes implementation
↓
tests/static checks
↓
output
↓
human security review
↓
accepted / modified / rejected
↓
revision
↓
verification
```

The assignment explicitly requires continuous manual evaluation of AI-generated code.

---

# Task M3-65 — Human review checklist for AI-generated crypto code


Member 3 should review every generated security artifact for:

### ML-KEM correctness

```text
correct maintained library API
ML-KEM-768 parameter set
public/private key roles correct
shared secret handled internally only
no handmade lattice/KEM implementation
no brittle assumption that every modified valid-length ciphertext throws
```

### Public-key trust

```text
protocol_version / algorithm / key_id validated
unauthenticated HTTP substitution risk documented
ML-KEM not misrepresented as Cloud identity authentication
```

### KDF correctness

```text
HKDF-SHA-256
salt=None
info exactly:
"ml-kem-project:v1:gateway-cloud-session"
output length=32 bytes
same fixed parameters as Cloud
no extra transcript fields
no extra confirmation key
no ad hoc SHA256(shared_secret)
```

### Session correctness

```text
TTL enforced
session reuse
gateway/session ownership
409 SESSION_INVALID handling
409 SESSION_EXPIRED handling
maximum one re-establishment per send
```

### AEAD correctness

```text
AES-256-GCM
32-byte key
12-byte nonce
cryptographically secure nonce generation
AAD contains exactly:
protocol_version
gateway_id
session_id
request_id
canonical AAD encoding matches Cloud
authentication failure stops processing
```

### Retry correctness

```text
transport retry bounded
ordinary ambiguous retry reuses the same already-built SecureEnvelope
same request_id / nonce / ciphertext / AAD for ordinary retransmission
session recovery is separate from ordinary retry
new-session recovery rebuilds encryption only because the session changed
business idempotency handles already-stored measurement
```

### Replay limitation

```text
no message counter in protocol v1
no dedicated cryptographic anti-replay counter/window
limitation is documented as technical debt
do not claim replay protection that is not implemented
```

### Fail-closed correctness

```text
PQC_FAILURE_POLICY=fail_closed only
no runtime plaintext fallback
no baseline endpoint call after crypto/session failure
```

### Operational behavior

```text
timeouts
logging safe
metrics safe
readiness does not require an active session
shutdown clears session references
```

### Architecture

```text
crypto isolated
no crypto code in Legacy route handler
CanonicalMeasurement not modified
request_id remains separate request/transport context
no direct Legacy coupling
```

---

# Task M3-66 — Document accepted/modified/rejected AI decisions


Examples:

```text
AI proposed encrypting sensor JSON directly with ML-KEM.
→ Rejected.
Reason:
ML-KEM is a KEM for shared-secret establishment, not bulk message encryption.
```

```text
AI proposed SHA-256(shared_secret) as session-key derivation.
→ Rejected/Modified.
Reason:
use the frozen HKDF-SHA-256 contract.
```

```text
AI proposed HKDF with gateway_id/Cloud identity/key_id.
→ Rejected/Modified.
Reason:
protocol v1 deliberately uses the simpler fixed info string:
"ml-kem-project:v1:gateway-cloud-session".
```

```text
AI proposed a separate key-confirmation key and session response.
→ Rejected.
Reason:
protocol v1 does not include a key-confirmation exchange.
```

```text
AI proposed adding message counter and a replay window.
→ Rejected for protocol v1.
Reason:
dedicated cryptographic anti-replay remains documented technical debt.
```

```text
AI proposed logging shared_secret.hex() for debugging.
→ Rejected.
Reason:
secret leakage.
```

```text
AI proposed automatic plaintext fallback after ML-KEM failure.
→ Rejected.
Reason:
silent downgrade violates our fail-closed migration design.
```

```text
AI proposed creating a new ML-KEM handshake for every measurement.
→ Modified.
Reason:
reuse bounded sessions to reduce overhead.
```

```text
AI proposed re-encrypting the same request with a fresh nonce after an ambiguous HTTP timeout.
→ Rejected/Modified.
Reason:
ordinary protocol-v1 transport retry retransmits the same already-built SecureEnvelope. Re-encryption happens only after a new session is established.
```

These are strong examples for the course report/documentation.

---

# Task M3-67 — Security documentation contribution


Member 3 should maintain the security sections of:

```text
docs/architecture/edge-gateway.md

docs/architecture/protocol-specification.md
```

and, if useful:

```text
docs/architecture/security-design.md
```

Document:

```text
ML-KEM library decision
ML-KEM-768 parameter set
ML-KEM implicit-rejection caveat

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
session reuse
session expiry
409 session recovery

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

ordinary ambiguous retry semantics:
same already-built SecureEnvelope
same request_id
same nonce
same ciphertext
same AAD

session-recovery semantics:
new session
new nonce/ciphertext under new session key
same logical request_id

business idempotency:
(device_id, sequence_number)

no dedicated cryptographic anti-replay counter/window
documented as technical debt

fail-closed policy
absence of runtime plaintext fallback

failure injection
HTTP test-environment limitation
secret-handling limitations
Python memory-zeroization limitation
```

---

# Task M3-68 — Document security technical debt


Member 3 should maintain items such as:

|Technical debt|Risk|Future improvement|
|---|---|---|
|Simplified Cloud public-key trust|MITM/key substitution risk|TLS/PKI/key pinning|
|In-memory sessions|restart loses state|secure persistent session strategy|
|Ephemeral Cloud key|identity changes on restart|persistent secure key storage|
|No HSM|keys remain process-memory software keys|HSM/KMS|
|No dedicated cryptographic anti-replay counter/window|authenticated envelopes can be replayed at crypto layer|per-session counters / replay window|
|Application-level crypto over test HTTP|no transport identity|TLS/mTLS|
|Simple key rotation|limited lifecycle|automated rotation|
|Python memory cannot guarantee zeroization|residual key-memory risk|lower-level secure key handling|

Cloud business idempotency prevents duplicate logical rows, but it is not a replacement for cryptographic replay protection.

---

# Task M3-69 — Threat-model contribution


Member 3 should help document at least:

```text
tampered ciphertext
wrong/expired session
malformed / modified ML-KEM ciphertext
public-key substitution risk
secret logging
replay of an authenticated secure envelope
downgrade
Cloud unavailability
session race
```

For each:

```text
threat
mitigation
remaining limitation
```

For replay, be precise:

```text
business idempotency prevents duplicate rows
but protocol v1 has no dedicated cryptographic anti-replay counter/window
```

---

# Task M3-70 — Baseline vs modernized evaluation


Member 3 should contribute security/performance measurements for:

```text
Baseline Mode
SECURITY_MODE=classical
```

versus:

```text
Modernized Mode
SECURITY_MODE=mlkem
```

Measure/collect:

```text
ML-KEM handshake duration

encapsulation duration if useful

first secure-message latency

steady-state secure-message latency

SecureEnvelope size

session reuse count

session re-establishment count

handshake failure behavior under injected failures

encryption/authentication failure behavior
```

Use equivalent workloads.

The first secure request should be reported separately because it includes session establishment.

Do not invent conclusions before measurements exist.

---

# Task M3-71 — PQC observability demonstration

For presentation/demo, Member 3 should help produce a scenario like:

```text
Start secure system
↓
first measurement
↓
handshake counter increments
↓
next measurements reuse session
↓
force session expiry
↓
handshake counter increments again
```

This visibly demonstrates post-quantum-related observability, which the project explicitly asks for.

---

# Task M3-72 — Corrupted-ciphertext demo

A good presentation scenario:

```text
FAILURE_MODE=corrupt_ciphertext
FAILURE_RATE=1.0
```

Then:

```text
Gateway encrypts valid measurement
↓
ciphertext corrupted
↓
Cloud rejects authentication
↓
no DB row
↓
decryption-failure metric increments
```

This demonstrates why AEAD matters.

---

# Task M3-73 — ML-KEM failure demo

Example:

```text
FAILURE_MODE=mlkem_handshake_failure
```

Expected:

```text
no secure session
no plaintext fallback
Gateway returns failure
handshake-failure metric increments
```

This demonstrates fail-closed behavior.

---

# Task M3-74 — Peer review Member 4's Cloud crypto code


Member 3 should review Member 4's implementation of:

```text
Cloud key pair handling
public-key endpoint
decapsulation
fixed HKDF-SHA-256 contract
session creation
AEAD decryption
session ownership
secure-envelope validation
business idempotency
```

Questions:

```text
Does Cloud derive exactly the same session key?

Does Cloud use:
salt=None
info="ml-kem-project:v1:gateway-cloud-session"
length=32?

Is private key ever exposed?

Does Cloud accept plaintext on secure endpoint?

Does authentication failure prevent storage?

Does Cloud correctly validate gateway/session binding?

Does ordinary duplicate transport retransmission remain idempotent?

Does documentation avoid claiming a cryptographic replay counter/window?

Does Cloud avoid assuming every modified valid-length KEM ciphertext throws?
```

---

# Task M3-75 — Peer review Member 2 integration


Member 3 should review Member 2 changes involving:

```text
SECURITY_MODE dispatch
transport abstraction
request_id propagation
PQC failure mapping
readiness behavior
failure injection boundaries
```

Questions:

```text
Can the Legacy route accidentally bypass SecureTransport in Modernized Mode?

Is `request_id` kept separate from CanonicalMeasurement?

Does Baseline Mode use X-Request-ID while Modernized Mode passes request_id into SecureTransport?

Does Modernized Mode always fail closed?

Can any crypto/session error call the baseline endpoint?

Are 409 SESSION_INVALID / SESSION_EXPIRED delegated to bounded SecureTransport recovery?

Does readiness incorrectly require an already-active session?

Are crypto exceptions translated safely?
```

---

# Task M3-76 — Dependency/security review

Member 3 should review crypto dependencies for:

```text
unnecessary packages
unmaintained packages
duplicate crypto libraries
unsafe low-level usage
```

Avoid importing several cryptographic libraries when one maintained stack is enough.

---

# Task M3-77 — Static/code-quality verification

Before crypto PRs:

```bash
uv run pytest edge_gateway/tests
uv run ruff check edge_gateway
uv run ai-history check
```

plus secure integration tests.

Inspect:

```bash
git diff
```

for accidental:

```text
debug secret logging
key fixtures
private-key files
temporary crypto prints
.env values
```

---

# Task M3-78 — Final secure-transport review


Before project freeze:

```text
ML-KEM library choice
✓

ML-KEM-768 wrapper
✓

public-key response
✓ protocol_version
✓ algorithm
✓ key_id
✓ Base64URL

public-key trust limitation
✓

HKDF-SHA-256
✓ salt=None
✓ info="ml-kem-project:v1:gateway-cloud-session"
✓ 32-byte output

session manager
✓

session reuse
✓

session expiry
✓

409 SESSION_INVALID recovery
✓

409 SESSION_EXPIRED recovery
✓

one-recovery-attempt bound
✓

AES-256-GCM
✓

12-byte nonce handling
✓

canonical AAD
✓ protocol_version
✓ gateway_id
✓ session_id
✓ request_id

SecureEnvelope
✓ no message counter
✓ request_id
✓ nonce
✓ ciphertext

ambiguous ordinary transport retry
✓ same already-built SecureEnvelope
✓ same request_id
✓ same nonce
✓ same ciphertext
✓ same AAD

session recovery
✓ new session
✓ new encryption under new session key
✓ same logical request_id

replay limitation
✓ no dedicated cryptographic anti-replay counter/window
✓ documented as technical debt
✓ business idempotency prevents duplicate DB rows

secure Cloud transport
✓

fail closed
✓

no runtime plaintext fallback
✓

failure injection
✓

logging
✓

metrics
✓

tests
✓

docs
✓

AI history
✓
```

---

# Recommended Member 3 task order

I would assign the work in this sequence:

```text
M3-00  Freeze security protocol

M3-01  Evaluate ML-KEM libraries

M3-02  Add chosen dependency with uv

M3-03  ML-KEM wrapper

M3-04  ML-KEM wrapper tests

M3-05  Public-key endpoint contract

M3-06  Public-key client

M3-07  KDF wrapper

M3-08  KDF tests

M3-09  Session model

M3-10  Session manager

M3-11  Session concurrency protection

M3-12  Session establishment protocol

M3-13  Session-response validation

M3-14  Gateway↔Cloud handshake integration

M3-15  Session reuse

M3-16  Session expiry

M3-17  Expiry tests

M3-18  Session-invalid recovery

M3-19  AEAD wrapper

M3-20  Nonce generation

M3-21  AEAD tests

M3-22  Plaintext serialization

M3-23  AAD construction

M3-24  AAD interoperability tests

M3-25  Secure envelope builder

M3-26  Secure envelope tests

M3-27  Secure Cloud transport

M3-28  Member 2 transport integration

M3-29  Security-mode integration

M3-30  Fail-closed behavior

M3-31  Verify runtime plaintext fallback is absent

M3-32  Crypto failure-injection framework

M3-33  ML-KEM failure injection

M3-34  Ciphertext corruption

M3-35  Missing-session simulation

M3-36  Session-expiry simulation

M3-37  Failure-injection safety tests

M3-38  Crypto logging

M3-39  Secret-leakage tests

M3-40  PQC metrics

M3-41  Metric-label review

M3-42  Handshake timing

M3-43  First vs steady-state measurements

M3-44  Secure retry semantics

M3-45  Session-recovery limits

M3-46  Implement frozen same-envelope ordinary retry policy

M3-47  Idempotent retry integration

M3-48  Tamper tests

M3-49  Wrong-session test

M3-50  Wrong-gateway/session test

M3-51  Unsupported protocol-version test

M3-52  Base64URL utilities

M3-53  Public-key trust documentation

M3-54  Document frozen HTTP/test trust boundary

M3-55  Session-memory review

M3-56  Secure shutdown behavior

M3-57  Crypto unit-test suite

M3-58  Secure integration suite

M3-59  Full secure E2E support

M3-60  Legacy compatibility regression

M3-61  Docker crypto compatibility

M3-62  Clean-container secure test

M3-63  CI crypto checks

M3-64  AI-history workflow

M3-65  Human security review

M3-66  AI decision documentation

M3-67  Security documentation

M3-68  Security technical debt

M3-69  Threat model

M3-70  Baseline vs secure evaluation

M3-71  PQC observability demo

M3-72  Corrupt-ciphertext demo

M3-73  ML-KEM-failure demo

M3-74  Review Cloud crypto PRs

M3-75  Review Gateway integration PRs

M3-76  Dependency/security review

M3-77  Static/code-quality verification

M3-78  Final security quality pass
```

# Suggested PR breakdown for Member 3

|PR|Scope|
|---|---|
|PR 1|ML-KEM library decision + dependency|
|PR 2|ML-KEM wrapper|
|PR 3|Frozen HKDF-SHA-256 session-key derivation|
|PR 4|Session model + manager + establishment locking|
|PR 5|Session establishment + public-key validation|
|PR 6|AES-256-GCM + 12-byte nonce + four-field canonical AAD|
|PR 7|SecureEnvelope|
|PR 8|Secure Cloud transport + fail-closed dispatch|
|PR 9|Session reuse/expiry + bounded 409 recovery + same-envelope transport retry|
|PR 10|Crypto failure injection|
|PR 11|Security logging + metrics|
|PR 12|Negative/tamper/security tests|
|PR 13|Docker/CI crypto hardening|
|PR 14|Evaluation + documentation|

---

# Member 3 milestone gates

## Gate A — ML-KEM primitive proven

Required:

```text
chosen library
Gateway encapsulation works
Cloud decapsulation works
shared secrets match
```

## Gate B — Secure session proven

Required:

```text
HKDF-SHA-256
fixed info="ml-kem-project:v1:gateway-cloud-session"
session ID
session key agreement
session expiry
session reuse
409 recovery contract
```

## Gate C — Secure message proven

Required:

```text
AES-256-GCM
12-byte nonce
canonical four-field AAD
secure envelope
Cloud decrypts correctly
```

## Gate D — Secure transport integrated

Required:

```text
Gateway application
→ secure transport
→ Cloud
```

without Legacy API changes.

## Gate E — Failure/security behavior proven

Required:

```text
corrupt ciphertext rejected
expired/invalid session recover once
ordinary ambiguous transport retry resends the same built envelope
replay limitation is documented
ML-KEM failure fails closed
no baseline fallback occurs
no secret logging
```

## Gate F — Final PQC subsystem complete

Required:

```text
metrics
Docker
CI
documentation
AI history
technical debt
evaluation
peer review
```

---

# Final Definition of Done for Member 3

Member 3 is finished only when:

```text
[ ] A suitable existing ML-KEM library has been evaluated and justified.

[ ] No ML-KEM algorithm is implemented manually.

[ ] ML-KEM-768 behavior is consistent with the protocol design.

[ ] Gateway can retrieve and validate Cloud public key.

[ ] ML-KEM encapsulation works.

[ ] Cloud decapsulation produces matching shared secret.

[ ] Shared secrets are never sent over the network.

[ ] Shared secrets are never logged.

[ ] HKDF is implemented through a standard library.

[ ] Gateway and Cloud use identical HKDF-SHA-256 parameters.

[ ] Gateway and Cloud use the exact same fixed HKDF `info` bytes.

[ ] HKDF uses `salt=None`.

[ ] HKDF uses `info=b"ml-kem-project:v1:gateway-cloud-session"`.

[ ] HKDF output is 32 bytes.

[ ] Derived session keys match.

[ ] Session response contains `protocol_version`, `session_id`, `status`, and `expires_at`.

[ ] Session keys never leave process memory intentionally.

[ ] Session manager supports establishment.

[ ] Active sessions are reused.

[ ] Expired sessions are replaced.

[ ] Concurrent session establishment is safe.

[ ] `409 SESSION_INVALID` triggers one bounded recovery attempt.

[ ] `409 SESSION_EXPIRED` triggers one bounded recovery attempt.

[ ] AES-256-GCM is implemented using a maintained library.

[ ] Nonces are safely generated.

[ ] Every new logical secure request uses a 12-byte nonce.

[ ] Nonce reuse with the same key is not intentionally possible.

[ ] Ordinary ambiguous/lost-response retries resend the same already-built `SecureEnvelope`.

[ ] AAD contains exactly `protocol_version`, `gateway_id`, `session_id`, and `request_id`.

[ ] AAD construction is deterministic and byte-compatible with Cloud.

[ ] Tampering with AAD causes rejection.

[ ] Secure envelope exactly matches protocol.

[ ] SecureEnvelope contains no `message_counter` in protocol version `1`.

[ ] Binary JSON fields use Base64URL.

[ ] Secure Cloud endpoint is used in Modernized Mode (`SECURITY_MODE=mlkem`).

[ ] Plaintext baseline endpoint is never automatically used in Modernized Mode.

[ ] `PQC_FAILURE_POLICY=fail_closed` is the only supported protocol-v1 policy.

[ ] PQC failure behavior is fail-closed.

[ ] Runtime migration fallback is not implemented.

[ ] Tests prove secure failures make zero baseline-endpoint calls.

[ ] Ciphertext corruption is detected by Cloud.

[ ] Wrong key/session fails.

[ ] Expired and unknown sessions fail/re-establish according to the frozen `409` contract.

[ ] Unsupported protocol version is rejected.

[ ] Crypto failure injection is configurable and disabled by default.

[ ] ML-KEM failure injection works.

[ ] Tests do not assume every modified valid-length ML-KEM ciphertext raises an explicit decapsulation exception.

[ ] Ciphertext corruption injection works.

[ ] Session failure injection works.

[ ] Secret-safe crypto logging is implemented.

[ ] Secret-leakage tests pass.

[ ] PQC metrics exist.

[ ] `gateway_pqc_fallback_total` remains zero in protocol version `1`.

[ ] Handshake duration is measurable.

[ ] First secure request and steady-state requests can be compared.

[ ] Secure transport works in Docker.

[ ] Secure integration tests pass in CI.

[ ] Legacy Device remains unchanged after PQC integration.

[ ] Full E2E secure path preserves original measurement data.

[ ] Security limitations are documented.

[ ] Public-key trust limitation is documented.

[ ] Documentation states that key confirmation does not authenticate a substituted public key.

[ ] HTTP-in-controlled-test-environment trust assumption is documented.

[ ] Lack of a dedicated cryptographic anti-replay counter/window is documented as technical debt.

[ ] AI-generated crypto code was manually reviewed.

[ ] Significant prompts/outputs/decisions are recorded.

[ ] Accepted/modified/rejected AI suggestions are documented.

[ ] Member 4 Cloud crypto code has been peer reviewed.

[ ] Member 2 secure integration has been reviewed.

[ ] Ruff/static checks pass.

[ ] Unit tests pass.

[ ] Security tests pass.

[ ] Integration tests pass.

[ ] AI-history validation passes.

[ ] CI passes.

[ ] Final PR has teammate review.
```
