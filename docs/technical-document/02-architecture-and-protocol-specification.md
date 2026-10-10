# Chapter 2 — Architecture and Protocol Specification

## 2.1 Protocol scope and design rules

The system uses two distinct protocol boundaries, which must never be confused:
![chapter 02 - Protocol scope and design rules.png](chapter%2002%20-%20Protocol%20scope%20and%20design%20rules.png)

The Legacy Device sends a simple, fixed JSON representation.  The Gateway is
the translation and modernization boundary: it validates legacy input,
normalizes it, enforces device sequence policy, and selects a Cloud transport.
The Cloud accepts only the Gateway canonical representation on its baseline
path or its decrypted canonical representation on its secure path.  It never
accepts the Legacy Device wire format.

The protocol design follows these invariants:

- APIs and secure messages are explicitly versioned; protocol version is
  always the string `"1"`.
- Application timestamps are ISO-8601 UTC values and JSON field names are
  `snake_case`.
- Every incoming representation is validated; secrets are never exposed in API
  responses, logs, metrics, persistence, or AI-history records.
- Baseline and secure modes use different endpoints.  Secure-mode failure
  never silently downgrades to plaintext.
- Retries are bounded and correlation is preserved through a Gateway-generated
  request ID.
- Cryptographic primitives come from maintained libraries; none is implemented
  in project code.

## 2.2 Legacy Device to Edge Gateway contract

### 2.2.1 Endpoint and payload

The Legacy Device sends one measurement to the Gateway:

```http
POST /api/v1/measurements
Content-Type: application/json
```

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "timestamp": "2026-09-21T13:45:31Z",
  "sequence_number": 184
}
```

The object contains exactly these five fields; unknown fields are rejected.

| Field | Type | Constraint |
| --- | --- | --- |
| `device_id` | string | non-empty |
| `temperature_c` | number | `-40 <= value <= 85` |
| `humidity_pct` | number | `0 <= value <= 100` |
| `timestamp` | string | ISO-8601 UTC |
| `sequence_number` | integer | `0 <= value <= 9223372036854775807` |

The Gateway returns `202 Accepted` with `{ "status": "accepted" }` only
after the Cloud has accepted the measurement for persistence.  Error semantics
are intentionally precise: malformed or unparseable request syntax is `400`;
parsed JSON with missing, wrongly typed, extra, or domain-invalid fields is
`422`; and a duplicate or out-of-order sequence is `409`.

### 2.2.2 Normalization and device sequence policy

After accepting the legacy form, the Gateway creates the canonical measurement:

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

`timestamp` becomes `measured_at`; the Gateway adds `received_at` and
`gateway_id`.  The request/correlation ID is deliberately not part of this
business object.

Sequence state is held independently for each `device_id` and records the last
valid sequence observed by the Gateway, not the last value stored by Cloud.

| Incoming sequence | Gateway action |
| --- | --- |
| First valid value | accept |
| `last + 1` | accept |
| Greater than `last + 1` | accept and record a sequence gap |
| Equal to `last` | reject as duplicate, `409` |
| Less than `last` | reject as out of order, `409` |

The Gateway commits this state after validation and sequence-policy acceptance,
but before Cloud delivery.  A later Cloud failure therefore does not roll back
an accepted device sequence.  This simple in-memory state is intentionally not
restart durable and is documented as technical debt.

## 2.3 Explicit Gateway-to-Cloud modes

Mode selection is configuration, not negotiation.

| Property | Classical baseline | Modernized ML-KEM |
| --- | --- | --- |
| Setting | `SECURITY_MODE=classical` | `SECURITY_MODE=mlkem` |
| Delivery endpoint | `POST /api/v1/baseline/measurements` | `POST /api/v1/secure/measurements` after session establishment |
| Body | plain `CanonicalMeasurement` | versioned `SecureEnvelope` |
| Correlation | `X-Request-ID` header | authenticated `request_id` in the envelope AAD |
| Secure failure policy | not applicable | `PQC_FAILURE_POLICY=fail_closed` |

Baseline Mode transmits canonical JSON with an `X-Request-ID` header.  It is
retained for baseline measurement and controlled migration comparison.  It is
not a runtime fallback target.  In Modernized Mode, a key, session, encryption,
or secure-delivery failure stays a failure; the Gateway must never automatically
retry the request through `/api/v1/baseline/measurements`.

### 2.3.1 Baseline Mode sequence with controlled fault injection

Failure injection is local configuration in the component that owns the fault;
it is never added to a network message.  The diagram shows representative
baseline cases.  Fault injection is disabled in ordinary operation and can be
made deterministic for a test with a service-scoped `FAILURE_MODE`,
`FAILURE_RATE=1.0`, and optional `FAILURE_SEED`.

![chapter 02 - Baseline Mode sequence with controlled fault injection.png](chapter%2002%20-%20Baseline%20Mode%20sequence%20with%20controlled%20fault%20injection.png)

### 2.3.2 Modernized ML-KEM Mode sequence with controlled fault injection

Modernized Mode adds public-key retrieval, ML-KEM session establishment, and a
secure envelope, but it preserves the Legacy Device interface.  The failure
branches illustrate the frozen distinction between an ordinary transport retry
(reuse the exact envelope) and session recovery (create one replacement
session, rebuild under its new key, and preserve the logical request ID).

![chapter 02 - Modernized ML-KEM Mode sequence with controlled fault injection.png](chapter%2002%20-%20Modernized%20ML-KEM%20Mode%20sequence%20with%20controlled%20fault%20injection.png)

## 2.4 Cryptographic suite and key-establishment contract

Protocol version `1` fixes one non-negotiated suite:

```text
CRYPTO_SUITE = MLKEM768-HKDFSHA256-AES256GCM
```

| Function | Frozen choice |
| --- | --- |
| Key establishment | ML-KEM-768 |
| Key derivation | HKDF-SHA-256 |
| Payload AEAD | AES-256-GCM |
| AEAD nonce | 12 bytes (96 bits) |
| Session-key output | 32 bytes |
| Protocol version | `"1"` |
| Binary JSON encoding | Base64URL, without whitespace |

The selected maintained implementation is `cryptography` version 48 or later,
which provides FIPS 203 ML-KEM-768 together with HKDF and AES-GCM.  The project
does not implement ML-KEM or any other cryptographic primitive itself.

The Cloud makes its current public key available through:

```http
GET /api/v1/crypto/public-key
```

```json
{
  "protocol_version": "1",
  "algorithm": "ML-KEM-768",
  "key_id": "cloud-key-001",
  "public_key": "<base64url>"
}
```

For this controlled course environment, the Gateway trusts the public key
returned by its explicitly configured Cloud URL.  ML-KEM establishes keying
material but does not authenticate the Cloud identity by itself; the protocol
does not claim to provide PKI, certificate validation, mTLS, or public-key
pinning.

To establish a session, the Gateway encapsulates to that public key and sends:

```http
POST /api/v1/crypto/sessions
Content-Type: application/json
```

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "key_id": "cloud-key-001",
  "encapsulation_ciphertext": "<base64url>"
}
```

The Cloud decapsulates, derives equivalent key material, and responds:

```json
{
  "protocol_version": "1",
  "session_id": "sess-550e8400...",
  "status": "established",
  "expires_at": "2026-09-21T13:50:31Z"
}
```

Both sides apply exactly the same KDF operation:

```text
HKDF-SHA-256(
  input_key_material = ML-KEM shared secret,
  salt = None,
  info = b"ml-kem-project:v1:gateway-cloud-session",
  length = 32
)
```

`salt=None` is part of the contract, as is the exact byte string in `info`.
Neither a transcript-bound KDF nor custom hashing/concatenation is used.  The
shared secret and the derived session key never cross the network and must not
be logged or persisted.  A malformed ML-KEM ciphertext can raise a library
error, but a modified ciphertext of the valid length can follow ML-KEM implicit
rejection and yield different keying material instead; tests do not assume that
every bit flip raises an exception.

## 2.5 Session lifecycle

Each session belongs to exactly one `gateway_id`, binds to the Cloud key ID
used for its establishment, and is held in process-local memory.  The Cloud
tracks its session ID, gateway ID, key ID, created/expiry times, state, and
secret key material; only the non-secret session ID and expiry are exposed.

The nominal session TTL is 300 seconds.  The Gateway checks local expiry before
sending, and the Cloud independently checks expiry for every secure request.
Sessions are never silently extended.  The process-local design means that a
Gateway restart loses its local session and a Cloud restart loses session and
key-pair state; recovery is a new handshake, not persistence of secrets.

```text
Gateway requests public key
  → encapsulates and derives session key
  → Cloud decapsulates and derives the same key
  → Cloud creates a 300-second, gateway-owned session
  → Gateway sends encrypted messages until expiry or invalidation
```

## 2.6 Secure-envelope contract

An established session protects one complete canonical measurement.  The
Gateway sends:

```http
POST /api/v1/secure/measurements
Content-Type: application/json
```

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "session_id": "sess-550e8400...",
  "request_id": "req-660e8400...",
  "nonce": "<base64url>",
  "ciphertext": "<base64url>"
}
```

This `SecureEnvelope` contains exactly the six fields shown.  Its ciphertext
is AES-256-GCM output for the UTF-8 JSON canonical measurement.  Binary values
(`nonce` and `ciphertext`) are Base64URL encoded.

The envelope metadata is authenticated, not merely visible.  Its AAD has
exactly four fields:

```json
{
  "gateway_id": "gateway-001",
  "protocol_version": "1",
  "request_id": "req-660e8400...",
  "session_id": "sess-550e8400..."
}
```

Both parties serialize that JSON object as UTF-8 with sorted keys and compact
separators (`","` and `":"`).  Any alteration of one of the four values
causes AES-GCM authentication/decryption to fail.  The protocol deliberately
does not add `cloud_id`, a message counter, an algorithm field, or any fifth
AAD field.

For each new logical secure message, the Gateway obtains a new 12-byte nonce
from cryptographically secure randomness and creates a new request ID and
envelope.  It must never intentionally reuse a nonce with the same session key.
The nonce is neither a sequence number nor a timestamp and must not come from a
non-cryptographic PRNG.

On receipt, Cloud validates the envelope structure, protocol version, session
existence/ownership, and expiry; reconstructs byte-identical AAD; then
authenticates/decrypts, validates the canonical measurement again, and attempts
idempotent storage.  Authentication failure prevents storage.

## 2.7 Correlation, retries, and session recovery

The Gateway creates one non-secret, UUID-like `request_id` for every accepted
Legacy request.  It is used for tracing only, never as key material.  In
baseline mode it is propagated by `X-Request-ID`; in secure mode the envelope
field authenticated as AAD is authoritative.

Ordinary transport retries (timeouts, connection failures, and HTTP `500`,
`502`, `503`, or `504`) are bounded by the common three-attempt backoff
schedule: wait one second after the first failure, two seconds after the
second, then stop.  A secure transport retry resends the *identical already
built envelope*: same request ID, session ID, nonce, ciphertext, and AAD.  It
does not re-encrypt merely because the response was lost.

Secure session errors are different:

```text
409 SESSION_INVALID or 409 SESSION_EXPIRED
  → discard the local session
  → obtain the current Cloud public key
  → establish exactly one replacement ML-KEM session
  → rebuild the envelope with the replacement key
  → retry the same logical request once, preserving request_id
```

This one recovery attempt is separate from normal HTTP retry and must not be
unbounded.  It legitimately produces a new session ID, nonce, and ciphertext
because a new session key is in use, while retaining the logical request ID.

The Legacy Device separately retries network errors, timeouts, and `500`/
`502`/`503`/`504`, but not `400`, `409`, or `422` responses.

## 2.8 Response, error, and storage contracts

All application errors have the stable outer shape:

```json
{
  "error": {
    "code": "INVALID_MEASUREMENT",
    "message": "measurement validation failed"
  }
}
```

Clients use the HTTP status and stable `error.code`, not free-text wording, to
classify a response.  The secure endpoint contract is:

| Condition | HTTP Status Code | Response / Result |
| --- | :---: | --- |
| Invalid envelope JSON or Base64URL encoding | `400` | `SECURE_MESSAGE_REJECTED` |
| Unsupported protocol version | `400` | `UNSUPPORTED_PROTOCOL_VERSION` |
| Unknown session | `409` | `SESSION_INVALID` |
| Expired session | `409` | `SESSION_EXPIRED` |
| Session does not belong to gateway | `400` | `SECURE_MESSAGE_REJECTED` |
| AEAD authentication/decryption failure | `400` | `SECURE_MESSAGE_REJECTED` |
| Invalid decrypted canonical measurement | `422` | `INVALID_MEASUREMENT` |
| Duplicate logical measurement | `202` | idempotent success |
| Temporary storage failure | `503` | `STORAGE_UNAVAILABLE` |
| Unexpected server error | `500` | `INTERNAL_ERROR` |

Session errors use `409 Conflict`, rather than HTTP user-authentication status
codes, because this protocol does not model a user login.  Externally, secure
rejection avoids cryptographic detail; internally, operational logs may record
the class of failure without keys or plaintext.

Cloud persists accepted canonical data as a record containing its `record_id`,
device and Gateway IDs, measurement values, sequence number, `measured_at`,
the Gateway's `received_at` mapped to `gateway_received_at`, and a Cloud
receipt time.  The persistent business identity is:

```text
UNIQUE(device_id, sequence_number)
```

If the same logical measurement is delivered again, Cloud does not insert a
second row and returns `202`, normally with `status: "already_accepted"` and
the existing record ID.  This supports safe retransmission but is not a
cryptographic replay defense: protocol version `1` deliberately has no
dedicated replay counter or replay window.

## 2.9 Endpoint summary and security boundaries

| Owner | Method | Endpoint | Purpose |
| --- | --- | --- | --- |
| Gateway | `POST` | `/api/v1/measurements` | Legacy measurement ingress |
| Cloud | `POST` | `/api/v1/baseline/measurements` | Baseline canonical measurement |
| Cloud | `GET` | `/api/v1/crypto/public-key` | Cloud ML-KEM public key |
| Cloud | `POST` | `/api/v1/crypto/sessions` | ML-KEM session establishment |
| Cloud | `POST` | `/api/v1/secure/measurements` | Secure-envelope ingress |
| Cloud | `GET` | `/api/v1/measurements` | Demonstration/query list |
| Cloud | `GET` | `/api/v1/measurements/{record_id}` | Demonstration/query record |
| Gateway and Cloud | `GET` | `/health`, `/ready`, `/metrics` | Operational endpoints |

The security claim is scoped precisely: **Gateway-to-Cloud** traffic gains
post-quantum key establishment and authenticated payload protection.  The
Legacy Device-to-Gateway connection remains legacy HTTP/JSON and is outside
this PQC boundary.  Likewise, Cloud key distribution is trusted only within the
configured test environment, and business idempotency is not cryptographic
anti-replay protection.  These limitations are surfaced as technical debt and
risk, not concealed as production-grade guarantees.
