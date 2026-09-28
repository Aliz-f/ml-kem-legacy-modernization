# M4-00: Cloud boundary review

This is the prerequisite review for Member 4 PR 1 (configuration and application
skeleton). It records the existing frozen contracts; it does not create a new
protocol or certify an implementation. Human review is pending in AI task 0010.

## Sources and scope

The authoritative source is the [shared protocol](../../docs/architecture/04%20-%20Shared%20Cross-Component%20Protocol%20Specification.md).
The [Cloud design](../../docs/architecture/03%20-%20Cloud%20Service.md) supplies
component behavior, the [roadmap](../../docs/architecture/05%20-%20Implementation%20roadmap.md)
supplies phase gates, and [Member 4 tasks](../../docs/architecture/09%20-%20Member%204%20Tasks.md)
supplies the M4-00 acceptance criteria. Section numbers below refer to these
documents. [Member 3 M3-00](../../docs/architecture/08%20-%20Member%203%20Tasks.md)
was also checked for the matching security contract.

Repository policy, the development workflow, `docs/ai/README.md`, and both
`Group-Explanation` course PDFs were reviewed. The course constraints remain:
keep the system small, establish the baseline before modernization, use
maintained crypto libraries, record significant AI work and actual checks, and
require human evaluation. This review contains no personal reflection.

At reviewed commit `69eb74a`, Cloud contains only `pyproject.toml` and the package
`__init__.py`; it has no application, configuration, storage, or tests. Gateway
contains ML-KEM encapsulation and HKDF wrappers and their tests. Their presence
does not demonstrate baseline E2E completion or authorize later-phase Cloud work.
The feature branch was synchronized with fetched `origin/develop` before changes
(`git merge --ff-only origin/develop`: already up to date).

M4-00 applies the roadmap Phase 0 architecture gate to the Cloud boundary before
Phase 4 C1/C2 implementation. The workspace and AI-history infrastructure exist.
Baseline Cloud Gate A still requires configuration, app, SQLite, baseline and
query endpoints, and idempotency; Gate B requires working Gateway-to-Cloud-to-
SQLite integration. Neither gate is complete. PR 1 alone cannot satisfy them.

This task delivers the boundary review only. After its human review and final
verification, the next task is M4-01 configuration, then M4-02 application
skeleton. Storage, baseline delivery, and secure behavior retain their later
member-task order. Baseline integration and measurement precede Cloud PQC work.

## M4-00 acceptance evidence

Every row below was checked against the documents. These are design-review
results, not runtime test results or claims of teammate approval.

| Acceptance criterion | Reviewed boundary | Evidence |
|---|---|---|
| Baseline endpoint frozen | `POST /api/v1/baseline/measurements` receives canonical JSON and `X-Request-ID`; validate and persist idempotently before `202`. No crypto operation on this path. | Shared sections 15-16, 44, 63; Cloud section 67; M4-10 |
| Secure endpoints frozen | `GET /api/v1/crypto/public-key`, `POST /api/v1/crypto/sessions`, and `POST /api/v1/secure/measurements` have distinct purposes and versioned schemas. | Shared sections 20-26, 33-34; Cloud sections 10-13, 21-22 |
| Crypto parameters match Member 3 | Protocol `"1"`: ML-KEM-768, HKDF-SHA-256, one 32-byte session key, AES-256-GCM, 12-byte nonce, Base64URL without whitespace, and 300-second session TTL. | Shared sections 18-22, 28, 30, 39; M3-00; M4-00 |
| Fixed HKDF info frozen | Input is the ML-KEM shared secret; `salt=None`, `info=b"ml-kem-project:v1:gateway-cloud-session"`, output length 32. | Shared section 28; Cloud section 19; Gateway `crypto/kdf.py` |
| Four-field AAD frozen | Exactly `protocol_version`, `gateway_id`, `session_id`, `request_id`; UTF-8 JSON with sorted keys and compact comma/colon separators. | Shared sections 36-37; Cloud section 21; M3-00 |
| Same-envelope ordinary retransmission frozen | Transport retries preserve request ID, session ID, nonce, ciphertext, and AAD. Re-encryption is reserved for replacement-session recovery. | Shared sections 39, 42-43, 67; M4-39, M4-50 |
| Storage schema frozen | SQLite measurement record contains the nine fields listed below; canonical `received_at` maps to `gateway_received_at`. | Shared sections 46-47; Cloud sections 8, 26-28; roadmap C4; M4-05/M4-06 |
| Idempotency policy frozen | `UNIQUE(device_id, sequence_number)`; repeat delivery returns `202`, `status=already_accepted`, and the existing `record_id`, without a second row. | Shared section 48; Cloud sections 54-56; M4-06/M4-08 |
| 409 session contract frozen | Unknown session: `409 SESSION_INVALID`; expired session: `409 SESSION_EXPIRED`. Gateway invalidates the old session and performs one bounded replacement-session recovery. | Shared sections 32, 42-43; Cloud sections 52-53; M4-39 |
| Replay limitation documented | Protocol v1 has no dedicated cryptographic anti-replay counter/window. Business idempotency prevents duplicate rows, not cryptographic replay. | Shared sections 49, 93; M3-00; M4-00 |
| No automatic plaintext fallback | `classical` and `mlkem` are explicitly selected modes. Modernized operation fails closed; the secure endpoint accepts only SecureEnvelope. | Shared sections 64-66; Cloud sections 67-70; M4-36 |
| No independent Cloud protocol changes | This review uses the source hierarchy, records discrepancies below, and makes no endpoint, schema, status, crypto, retry, or storage change. | AGENTS.md source hierarchy; shared section 98; scope of this diff |

## Schema and processing boundaries

The public-key response has `protocol_version`, `algorithm` (`ML-KEM-768`),
`key_id`, and `public_key`. The session request has `protocol_version`,
`gateway_id`, `key_id`, and `encapsulation_ciphertext`. The session response has
`protocol_version`, `session_id`, `status` (`established`), and `expires_at`.
Binary crypto fields use Base64URL. There is no Cloud identity field or explicit
key-confirmation exchange in these messages.

SecureEnvelope has exactly `protocol_version`, `gateway_id`, `session_id`,
`request_id`, `nonce`, and `ciphertext`. Cloud validates the envelope, version and
encoding, then session lookup, ownership and expiry, before reconstructing
AAD and authenticating/decrypting. Only authenticated plaintext is parsed and
validated. The decrypted `gateway_id` must match the envelope/session identity.
Session-validation order follows authoritative shared section 62. Idempotency
and persistence happen after those checks; Cloud section 22 and M4-35 describe
the remaining processing stages but conflict on ownership/expiry order, as
recorded below.

The canonical measurement has `device_id`, `temperature_c`, `humidity_pct`,
`measured_at`, `sequence_number`, `received_at`, and `gateway_id`.
`request_id` remains transport metadata: the baseline header or authenticated
secure-envelope field. It is not added to the canonical or storage model.

The stored fields are `record_id`, `device_id`, `gateway_id`, `temperature_c`,
`humidity_pct`, `measured_at`, `gateway_received_at`, `cloud_received_at`, and
`sequence_number`. Cloud adds its receive timestamp and record ID; it preserves
the measurement values and renames the Gateway receive timestamp. Keys, shared
secrets, session keys, and raw envelopes are not persisted as measurements.

Ordinary transport retry follows timeout, connection failure, or retryable
`500/502/503/504` without rebuilding the envelope. For `409 SESSION_INVALID` or
`409 SESSION_EXPIRED`, Gateway discards the old session, retrieves the current
public key, establishes one replacement session, rebuilds the envelope under
the new key with a new nonce, preserves the logical `request_id`, and retries
once. Cloud never silently extends an expired session.

The secure error contract is unchanged: malformed envelope/encoding,
ownership mismatch, or authentication failure is `400 SECURE_MESSAGE_REJECTED`;
unsupported version is `400 UNSUPPORTED_PROTOCOL_VERSION`; invalid decrypted
measurement is `422 INVALID_MEASUREMENT`; temporary storage failure is
`503 STORAGE_UNAVAILABLE`; internal failure is `500 INTERNAL_ERROR`. Errors use
the structured `error.code`/`error.message` body and expose no crypto internals.

Legacy validation and sequence tracking remain Gateway responsibilities.
Cloud does not receive the Legacy wire model, generate Gateway request IDs,
encrypt Gateway messages, or implement Gateway retries. In particular, Cloud
idempotent success does not replace Gateway duplicate/out-of-order `409`
behavior. Gateway updates sequence state before Cloud delivery and does not
roll it back on Cloud failure. Gateway returns Legacy `202` only after Cloud
acceptance/persistence.

## Findings and implementation constraints

1. **Query example mismatch:** Cloud design section 30 shows a bare JSON array;
   shared section 50 requires an object containing `items`. The shared contract
   takes precedence. Future M4-12 must use `{"items": [...]}`. The Cloud design
   example needs a separately approved shared-document correction; it was not
   edited by this task. No existing Cloud query implementation needs correction.
2. **Phase-specific configuration:** Cloud design section 42 shows `mlkem` as an
   example/default, while roadmap C1 and M4-01 explicitly start with
   `SECURITY_MODE=classical`. PR 1 targets baseline configuration; the modernized
   example does not authorize enabling or initializing crypto in baseline mode.
   This follows shared section 63 and the roadmap's baseline-first ordering.
3. **TTL wording:** shared section 30 fixes normal protocol-v1 lifetime at 300
   seconds and allows shorter test TTLs or a controlled clock. M4-01's positive-
   TTL validation and Cloud section 17's default wording do not by themselves
   authorize a different production protocol lifetime. Preserve the frozen
   value and distinguish test clock/TTL controls when implementing sessions.
4. **Existing Member 3 evidence is partial:** Gateway's `crypto/mlkem.py` uses
   the library ML-KEM-768 public-key API; `crypto/kdf.py` uses library
   HKDF-SHA-256 with the exact salt, info and output size. M3-00 agrees with the
   remaining documented Cloud contract. There is no Cloud crypto implementation
   to compare or round-trip yet; AAD, session and envelope interoperability tests
   belong to their later tasks. No direct imports of Gateway application models
   or wrappers into Cloud are proposed (shared sections 83-85).
5. **Encoding detail remains to coordinate:** shared section 22 specifies
   Base64URL without whitespace but does not select padding behavior. M4-40
   requires consistent padding behavior. Both sides must coordinate and test
   this before wire-encoding implementation; this review does not invent a
   padded-only or unpadded-only acceptance rule.
6. **Session-validation ordering conflict:** shared section 62 specifies
   lookup → ownership → expiry. Cloud design section 22 (also section 50) and
   M4-35 instead put expiry before ownership. The shared protocol is
   authoritative: after envelope validation, look up the session, reject an
   unknown session with `409 SESSION_INVALID`, verify Gateway ownership, then
   check expiry before constructing AAD or decrypting. An ownership mismatch
   returns `400 SECURE_MESSAGE_REJECTED` even if that session is also expired;
   `409 SESSION_EXPIRED` applies after ownership succeeds. Future session and
   secure-endpoint tests must cover this combined mismatch/expiry case. The
   earlier version of this review incorrectly repeated the lower-priority
   expiry-first order; the processing summary above now follows the shared
   contract. Shared documents remain unchanged and need separately approved
   corrections.

## Security limitations and later verification

The controlled-environment public-key endpoint is trusted by configuration;
ML-KEM does not authenticate Cloud identity. Gateway identity authentication is
also simplified. Ephemeral Cloud keys and in-memory sessions disappear on
restart. SQLite and a single service instance remain course-scale choices.
Replayed authenticated envelopes are not rejected by a cryptographic replay
window; duplicate database rows alone are prevented. Device sequence resets
across restarts remain an idempotency limitation. The Legacy-to-Gateway path
is not post-quantum protected.

Use maintained ML-KEM, HKDF, and AES-GCM libraries. Malformed/incorrect-length
ML-KEM ciphertext may raise; valid-length mutations may use implicit rejection
instead. A successful decapsulation call is not explicit key confirmation.
Failure-seed randomness is for fault injection only, never keys or nonces.
No `cloud_id`/`EXPECTED_CLOUD_ID` wire fields, transcript-bound KDF, confirmation
keys/tags, HMAC confirmation, message counters, replay windows, fifth AAD field,
or automatic downgrade may be introduced. `CLOUD_ID` is local configuration.

Later contract tests must verify independent Gateway/Cloud schema and AAD
agreement, KDF equality, authenticated round trips, rejection before storage,
409 recovery, same-envelope lost-response retries, idempotency, and safe logs.
Baseline E2E and its measurements must be demonstrated before Cloud secure
modernization. Health/readiness must be mode-aware; an active Gateway session
is never a readiness prerequisite.

For this documentation-only task, verification consists of source comparison,
local link and diff checks, and the repository-required Ruff, pytest, and
AI-history checks. Actual results are recorded in AI task 0010. No new runtime
tests are warranted until Cloud implementation exists. Human acceptance and
explicit final verification remain required before M4-00 is marked complete.
