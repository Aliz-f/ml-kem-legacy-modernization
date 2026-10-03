# Secure ingestion (M4-34–M4-40)

`POST /api/v1/secure/measurements` accepts only SecureEnvelope JSON in explicit
`SECURITY_MODE=mlkem`. It reuses the Cloud session, AAD, AES-GCM, canonical
validation and SQLite repository implementations. Gateway code is unchanged.

## Validation and processing order

Shared Protocol section 80 sets a **64 KiB (65536-byte)** limit on the complete
JSON body including whitespace. The endpoint requires `application/json`
(parameters permitted), rejects oversized declared lengths, and independently
counts streamed bytes before appending chunks. The exact boundary is accepted;
larger bodies fail before lookup/decryption even without Content-Length. The
standalone validator enforces the same limit.

Validation rejects invalid UTF-8/JSON, duplicate keys, non-JSON constants,
non-object input, missing/extra fields and wrong types. The existing M4-33 model
remains schema-only. The new validator requires version `"1"`, non-empty trimmed
identifiers, strict Base64URL, a decoded 12-byte nonce and non-empty ciphertext.
Correctly padded/unpadded encodings are accepted; alternate alphabets,
whitespace, malformed padding and noncanonical padding bits are rejected.
The existing AEAD wrapper rejects missing/invalid authentication tags.

Processing then follows **lookup → ownership → expiry**, builds four-field AAD,
authenticates/decrypts, parses strict plaintext JSON, validates the canonical
measurement and its Gateway identity, and finally performs idempotent storage.
This preserves the Shared Protocol/M4-00 ordering over expiry-first wording in
lower-priority documents. Authentication failure never reaches plaintext
validation or storage. Invalid authenticated plaintext never reaches storage.
CPU/storage work runs in the thread pool; acknowledgements follow commit.

## Outcomes and mode isolation

| Condition | HTTP / code |
| --- | --- |
| Invalid/oversized envelope, encoding, or authentication | `400 SECURE_MESSAGE_REJECTED` |
| Unsupported string protocol version | `400 UNSUPPORTED_PROTOCOL_VERSION` |
| Unknown/removed session | `409 SESSION_INVALID` |
| Wrong owner, including an expired session still present | `400 SECURE_MESSAGE_REJECTED` |
| Correct owner at/after expiry | `409 SESSION_EXPIRED` |
| Invalid authenticated plaintext or canonical Gateway mismatch | `422 INVALID_MEASUREMENT` |
| Storage failure | `503 STORAGE_UNAVAILABLE` |
| Unexpected processing failure | `500 INTERNAL_ERROR` |
| Inactive mode/service | `503 SERVICE_UNAVAILABLE` |

The required M4-35 acknowledgement reuses existing `202 accepted` /
`already_accepted` repository behavior and original record IDs for duplicates.
Identical valid envelopes can be processed again; `(device_id, sequence_number)`
prevents duplicate rows. This is business idempotency, not cryptographic replay
rejection. M4-37 tests additionally verify that a new session and request ID
for the same business measurement still return the original record ID.

In `mlkem` mode plaintext canonical bodies fail secure-envelope validation and
baseline ingestion remains unavailable. In `classical` mode secure ingestion
is unavailable and baseline accepts canonical measurements only. No failure
path tries plaintext, another format or another algorithm. Logs use bounded,
quoted correlation metadata; bodies, crypto material and vendor diagnostics
are not logged. At the time of this secure-ingestion task `/ready` was a
placeholder; the current mode-aware readiness behavior is documented in
`final-integration-and-operations.md`.

## Verification scope

Tests establish a real ML-KEM session through Cloud's HTTP application, encrypt
with the unchanged Gateway envelope builder, and verify persistence/query
fields and identical-envelope idempotency. Negative tests forbid downstream
calls to check validation-before-lookup and authentication-before-storage.
They cover each failure stage, wrong ownership before expiry, malformed
authenticated plaintext, Gateway mismatch, actual SQLite write failure, safe
internal errors, both mode guards, the exact byte limit, and streaming overflow
without reading the remainder. This is Cloud HTTP application integration with
Gateway primitives, not full Legacy/Gateway/Cloud deployment E2E.

At the time of this task, M4-41 and later work, including runtime failure
injection, had not started. Current failure-injection and Docker verification
is documented in `final-integration-and-operations.md`. No dependencies changed
for this task.

## Response and encoding contracts (M4-37 through M4-40)

Success bodies contain exactly `status` and `record_id`: `accepted` after the
first committed insert, or `already_accepted` with the original ID for duplicates.
Errors contain exactly `error`, with `code` and `message`. Malformed envelopes,
encoding errors, ownership mismatches and authentication failures share the
message `secure message could not be processed`. Unsupported versions return
`unsupported protocol version`. No vendor exception text is returned or logged.
The session HTTP handler maps known status/code pairs to fixed messages instead
of exposing exception text; an unknown pair becomes a generic internal error.

Unknown sessions return `409 SESSION_INVALID` / `secure session is invalid`;
expired sessions return `409 SESSION_EXPIRED` / `secure session has expired`.
Ownership is checked before expiry and expired sessions are removed, never
extended. These responses support the frozen bounded Gateway recovery contract;
this task does not modify or claim new Gateway HTTP-client E2E integration.

`cloud_service.crypto.encoding` centralizes non-empty binary encoding for public
keys, ML-KEM encapsulation ciphertext, nonces and AES-GCM ciphertext/tag data.
It emits unpadded Base64URL and accepts canonical padded or unpadded input.
Whitespace, standard Base64 `+`/`/`, malformed padding and nonzero unused pad bits
are rejected with a fixed safe error. Callers retain their protocol size checks
(1088-byte encapsulation ciphertext and 12-byte nonce); the encoder is not a
cryptographic primitive. No dependency or protocol changes are required.
