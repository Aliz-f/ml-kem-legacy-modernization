# Project-wide failure-test matrix

This matrix is the Member 5 coordination plan for M5-39. It translates the
frozen protocol into later automated tests; it does not introduce a new
endpoint, status code, retry policy, or failure mode. Fault injection remains
local to the originating process and is disabled by default.

Each later test uses `FAILURE_RATE=1.0` and a service-scoped root setting where
applicable, so the selected fault is deterministic. Tests must assert that the
Legacy-facing response is never a false `202 Accepted` and that Cloud storage
has the stated result.

| ID | Fault owner | Injected scenario | Expected observable result | Later automation |
|---|---|---|---|---|
| F1 | Legacy | Malformed/unparseable JSON body | Gateway returns `400 INVALID_JSON`; no Cloud call or row. | M5-40 |
| F2 | Legacy | Missing required field in parsed JSON | Gateway returns `422 INVALID_MEASUREMENT`; no Cloud call or row. | M5-40 |
| F3 | Legacy | Humidity outside `0..100` | Gateway returns `422 INVALID_MEASUREMENT`; no Cloud call or row. | M5-40 |
| F4 | Legacy | Invalid timestamp | Gateway returns `422 INVALID_MEASUREMENT`; no Cloud call or row. | M5-40 |
| F5 | Legacy | Duplicate sequence | Gateway returns `409 DUPLICATE_SEQUENCE`; no duplicate Cloud row. | M5-40 |
| F6 | Legacy | Lower, out-of-order sequence | Gateway returns `409 OUT_OF_ORDER_SEQUENCE`; no Cloud row. | M5-40 |
| F7 | Gateway | Processing error | Legacy receives a visible safe failure, not `202`; no false Cloud acceptance. | M5-41 |
| F8 | Gateway | Cloud timeout | Gateway uses its bounded transport retry policy; no false `202` after exhaustion. | M5-41 |
| F9 | Gateway | ML-KEM handshake or session failure | Fail closed: no baseline call or plaintext fallback. | M5-42 |
| F10 | Gateway | Corrupt AEAD ciphertext | Cloud rejects the secure request; no measurement is stored. | M5-42 |
| F11 | Cloud | Public key unavailable | Gateway cannot start secure session establishment; no protected measurement is accepted. | M5-43 |
| F12 | Cloud | Simulated ML-KEM wrapper/decapsulation failure | No usable session is created; no protected measurement is accepted. | M5-43 |
| F13 | Cloud | Unknown session | Cloud returns `409 SESSION_INVALID`; Gateway performs one bounded re-establishment attempt. | M5-43 |
| F14 | Cloud | Expired session | Cloud returns `409 SESSION_EXPIRED`; Gateway performs one bounded re-establishment attempt. | M5-43 |
| F15 | Cloud | AEAD decryption failure | Cloud rejects the secure request; no measurement is stored. | M5-43 |
| F16 | Cloud | Storage failure | Cloud returns `503`; Gateway applies bounded retry; no false `202`. | M5-43 |
| F17 | Cloud | Service unavailable | Cloud returns `503`; Gateway applies bounded retry; no false `202`. | M5-43 |
| F18 | Cloud | Response dropped after successful persistence | Gateway resends the same already-built SecureEnvelope; Cloud has exactly one logical row. | M5-44 |

## Secure-path invariants

F9–F18 run in `SECURITY_MODE=mlkem` with
`PQC_FAILURE_POLICY=fail_closed`. A fault in that path must not cause a retry
through `POST /api/v1/baseline/measurements`.

For F13 and F14, recovery creates one replacement session, preserves the
logical request ID, rebuilds the envelope under the replacement key, and
retries once. This is distinct from F18's ordinary transport retry, which
resends the identical already-built envelope: the same request ID, session ID,
nonce, ciphertext, and AAD.

## ML-KEM and replay boundaries

F12 is an explicit simulated operational wrapper/decapsulation failure. It is
not evidence that every modified valid-length ML-KEM ciphertext naturally
raises an exception: ML-KEM may use implicit rejection.

Protocol version 1 has no dedicated cryptographic replay counter or window.
Therefore this matrix does not define a cryptographic replay-rejection test.
F18 instead verifies the separately frozen business idempotency rule,
`UNIQUE(device_id, sequence_number)`, for an ordinary retransmission.
