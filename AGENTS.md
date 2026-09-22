# AI-agent policy

This policy applies to Codex, Claude Code, Grok Build, GitHub Copilot, Cursor,
Gemini, and all other AI coding agents. Read it before any repository change.
It is the canonical AI-agent policy: more specific agent entry points may add
tool guidance, but may not weaken or override it.

## Frozen architecture is binding

Architecture and protocol documents are implementation constraints, not optional
background reading. Before generating code or changing the repository for a new
task, identify the affected components and frozen contracts. Do not begin
implementation until this is done.

### Required reading

Read `AGENTS.md`, the relevant documents below, `docs/DEVELOPMENT_WORKFLOW.md`,
and the relevant instructions under `docs/ai/` before implementation.

| Work area | Required reading |
|---|---|
| Any cross-component, API, crypto, session, retry, status-code, configuration, storage, Docker, metrics, or E2E change | `docs/architecture/04 - Shared Cross-Component Protocol Specification.md` and `docs/architecture/05 - Implementation roadmap.md` |
| Legacy Device | `docs/architecture/01 - Legacy Device.md` and `docs/architecture/06 - Member 1 Tasks.md` |
| Gateway API/application or legacy interface | `docs/architecture/02 - Edge Gateway.md` and `docs/architecture/07 - Member 2 Tasks.md` |
| Gateway PQC/security | `docs/architecture/02 - Edge Gateway.md`, `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`, and `docs/architecture/08 - Member 3 Tasks.md` |
| Cloud Service | `docs/architecture/03 - Cloud Service.md`, `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`, and `docs/architecture/09 - Member 4 Tasks.md` |
| Docker, CI, E2E, or metrics | `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`, `docs/architecture/05 - Implementation roadmap.md`, and `docs/architecture/10 - Member 5 Tasks.md` |

Always read the implementation roadmap to determine the current phase,
prerequisites, acceptance gate, exact task, required tests, and Definition of
Done. Do not implement later-phase features merely because they are described
in the architecture.

### Source-of-truth hierarchy

1. `docs/architecture/04 - Shared Cross-Component Protocol Specification.md` — cross-component protocol.
2. `docs/architecture/01 - Legacy Device.md`, `02 - Edge Gateway.md`, and `03 - Cloud Service.md` — component responsibilities and internal behavior.
3. `docs/architecture/05 - Implementation roadmap.md` — implementation order, dependencies, and milestone gates.
4. `docs/architecture/06 - Member 1 Tasks.md` through `10 - Member 5 Tasks.md` — detailed responsibilities and task-level Definition of Done.
5. `AGENTS.md`, `CLAUDE.md`, `GROK.md`, and development-workflow documents — execution workflow and agent behavior.
6. Existing code and tests — implementation state, never permission to override frozen architecture.

If code or tests conflict with frozen architecture, stop, identify and report the
mismatch, then change the implementation to match the documents. Never silently
redefine a protocol to fit existing code.

## Frozen protocol quick reference

```text
Legacy Device --HTTP + JSON--> Edge Gateway
Edge Gateway --ML-KEM-768 -> HKDF-SHA-256 -> one 32-byte session key
             -> AES-256-GCM--> Cloud Service
```

- HKDF input is the ML-KEM shared secret; `salt=None`,
  `info=b"ml-kem-project:v1:gateway-cloud-session"`, and output length `32`.
- Use AES-256-GCM with a 12-byte (96-bit) nonce. `protocol_version` is `"1"`;
  binary JSON crypto values use Base64URL; session TTL is 300 seconds.
- Public-key response fields are `protocol_version`, `algorithm` (`ML-KEM-768`),
  `key_id`, and Base64URL `public_key`. Session request fields are
  `protocol_version`, `gateway_id`, `key_id`, and Base64URL
  `encapsulation_ciphertext`. Session response fields are `protocol_version`,
  `session_id`, `status` (`established`), and `expires_at`.
- A `SecureEnvelope` has exactly `protocol_version`, `gateway_id`, `session_id`,
  `request_id`, `nonce`, and `ciphertext`. Its AAD has exactly
  `protocol_version`, `gateway_id`, `session_id`, and `request_id`, encoded as a
  UTF-8 JSON object with sorted keys and compact separators.
- Session errors are `409 SESSION_INVALID` and `409 SESSION_EXPIRED`. An
  ordinary transport retry resends the same already-built envelope: same
  request ID, session ID, nonce, ciphertext, and AAD. On session recovery,
  invalidate the old session, establish one replacement session, rebuild the
  envelope with its key, preserve the logical request ID, and retry once.
- `SECURITY_MODE=mlkem` and `PQC_FAILURE_POLICY=fail_closed`; there is no
  runtime plaintext fallback. Baseline mode is `SECURITY_MODE=classical`,
  `POST /api/v1/baseline/measurements`, and `X-Request-ID`.
- Cloud idempotency is `UNIQUE(device_id, sequence_number)`. Protocol v1 has no
  dedicated cryptographic anti-replay counter/window; business idempotency is
  not cryptographic replay protection.

Do not introduce `cloud_id` or `EXPECTED_CLOUD_ID` into crypto protocol
messages; transcript-bound KDFs; separate confirmation keys/tags or HMAC
key-confirmation; `message_counter`; a replay window; five-field AAD; automatic
plaintext fallback; ordinary-retry re-encryption; custom ML-KEM; or custom
cryptographic primitives. `CLOUD_ID` may be local Cloud configuration only.

## Frozen component behavior and ownership

- Legacy validation: malformed/unparseable syntax is `400 Bad Request`; parsed
  JSON with a missing field, wrong type, or domain-invalid field is `422
  Unprocessable Entity`; duplicate and out-of-order sequences are `409
  Conflict`. Do not write “400 or 422” for a frozen case. Return Legacy `202`
  only after Cloud acceptance/persistence.
- Gateway sequencing is per-device in memory: first and higher values are
  accepted; gaps are accepted and logged/metriced; equal values are `409`
  duplicate; lower values are `409` out-of-order. Update state after
  schema/domain validation and sequence-policy acceptance, before Cloud
  delivery; never roll it back for a Cloud failure.
- Member 1 / `legacy_system`: sensor, serialization, Legacy HTTP client, and
  Legacy failures. Member 2 / `edge_gateway`: Legacy API, validation,
  normalization, sequence tracking, request ID, baseline Cloud transport, and
  application behavior. Member 3 / `edge_gateway`: ML-KEM, HKDF, sessions,
  AES-GCM, SecureEnvelope, and secure transport. Member 4 / `cloud_service`:
  baseline API, Cloud ML-KEM/sessions/decrypt, validation, idempotency, SQLite,
  and query API. Member 5 / repository-wide: Docker, CI/CD, integration, E2E,
  observability, reproducibility, and metrics integration.

Do not move ownership across components merely to make a task easier.

## Execution model

### Before coding

1. Read the required documents and inspect related code/tests.
2. Identify the roadmap/member task, current phase, completed prerequisites,
   acceptance gate, dependencies, and exact frozen contracts.
3. Determine whether the task is partly implemented and make a short plan.
4. Implement only the requested current-phase scope; extend working code rather
   than regenerating or blindly replacing it.

### Implement and verify

1. Make the smallest correct change, preserve ownership boundaries, and add or
   update relevant tests and documentation.
2. Run applicable checks: `uv run ruff check .`, `uv run pytest`, and
   `uv run ai-history check`; run `uv sync --frozen` for dependency changes and
   Docker plus relevant health/readiness/E2E checks for integration work.
3. Compare the result against frozen architecture again. Do not claim
   completion if relevant checks fail.

Keep the system course-sized. Without an explicit request, do not add
Kubernetes, Kafka, Redis, a service mesh, distributed database, OAuth/accounts,
frontend, HSM/KMS, complex PKI, message broker, distributed locks, large
abstraction frameworks, or unnecessary design patterns. Prefer Python 3.12,
`uv`, HTTP/JSON, SQLite, in-memory sessions and Gateway sequence state, Docker
Compose, pytest, and Ruff.

If a request changes an endpoint, field/schema, status code, crypto/KDF/nonce/
AAD parameter, retry/session/fallback behavior, or storage mapping, identify it
as an architecture/protocol change. Do not silently implement it. Update in
order: shared protocol specification, component designs, roadmap, member tasks,
tests, then implementation.

## Required course-guideline check for new features

Before planning, designing, or implementing a new feature, read
`Group-Explanation 01.pdf` and `Group-Explanation 02.pdf`. Treat these course
documents and the repository as the source of truth. Keep scope small; record
significant AI prompts, outputs, decisions, changes, risks, and verification;
manually and continuously evaluate AI code; use a maintained library for future
ML-KEM work; and never use AI for a student’s personal reflection, experiences,
or feelings.

## AI-history and human review

Before substantial AI-generated implementation, inspect existing work and the
course documents, run `uv run ai-history status`, and start exactly one task.
Record the human prompt faithfully; use the repository `uv` workflow and never
add `requirements.txt`. Complete requested code, documentation, refactoring,
tests, and checks; record only actual, sanitized results.

Run `uv run ai-history output`, then stop for human review. Never populate
human fields. Ask for Problems Found, Decision (`Accepted`, `Modified`, or
`Rejected`), and Requested Modifications when Modified. For Modified, record
the review, complete the full revision and checks, run `ai-history revision`,
and stop for another review. After Accepted, request explicit final human
verification and run `ai-history verify`. Automated checks and AI review never
substitute for human review or verification. Never store keys, shared secrets,
credentials, passwords, tokens, `.env` contents, or secret configuration in
history.

For cryptographic code, use maintained ML-KEM, HKDF, and AES-GCM libraries;
never implement these primitives or use a failure-seed/test PRNG for
cryptographic randomness. Never log or persist private keys, ML-KEM shared
secrets, or session keys. Tests must allow malformed/incorrect-length ML-KEM
ciphertext to raise, but may not require every valid-length bit flip to raise:
ML-KEM can use implicit rejection. Protocol v1 has no explicit key confirmation.
