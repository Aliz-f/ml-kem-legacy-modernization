# Secure ingestion (M4-34–M4-36)

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
rejection. No separate M4-37 work is started.

In `mlkem` mode plaintext canonical bodies fail secure-envelope validation and
baseline ingestion remains unavailable. In `classical` mode secure ingestion
is unavailable and baseline accepts canonical measurements only. No failure
path tries plaintext, another format or another algorithm. Logs use bounded,
quoted correlation metadata; bodies, crypto material and vendor diagnostics
are not logged. `/ready` remains the existing placeholder, not a claim of full
service readiness.

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

M4-37 and later tasks remain unstarted, including runtime failure injection.
M4-17 Docker verification stays deferred to M4-81/M4-83. No dependencies changed.
