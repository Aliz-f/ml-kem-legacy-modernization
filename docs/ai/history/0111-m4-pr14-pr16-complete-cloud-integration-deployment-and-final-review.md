# AI Task 0111 — M4 PR14-PR16 complete Cloud integration, deployment, and final review

**Status:** Complete

**Created:** 2026-10-01T23:16:37+03:00

**Updated:** 2026-10-02T00:08:20+03:00

**Agent:** Codex

---

# Task

Complete Member 4 M4-70 through M4-103 in dependency order on feat/pr14-16, preserve frozen protocol and ownership, implement feasible integration, Cloud Docker/CI, documentation, evaluation, demos, reviews, and quality checks; record unresolved external dependencies honestly; stop at Awaiting Human Review without commit, push, PR, or M4-104 work.

---

# Prompt

We are Member 4.

The current branch is:
feat/pr14-16

It was created from the latest origin/develop after PR11–PR13 were merged.

Your scope is the COMPLETE remaining Member 4 work:

M4-70 through M4-103

This corresponds to:
PR14: M4-70–M4-80
PR15: M4-81–M4-87
PR16: M4-88–M4-103

The goal is to finish Member 4 completely in this single branch and prepare one final Pull Request.

IMPORTANT:
Do not start M4-104 or invent any additional Member 4 tasks.
Do not implement Member 2, Member 3, or Member 5 tasks as if they were Member 4 tasks.
Do not redo completed M4-00–M4-69 work unless an actual integration/regression problem requires a minimal correction.
Do not make unrelated refactors.
Do not delete or modify the untracked review-0104.diff file.
Do not commit review-0104.diff.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
1. READ THE AUTHORITATIVE SOURCES FIRST
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Before changing code, read and understand:

- AGENTS.md
- docs/DEVELOPMENT_WORKFLOW.md
- the authoritative Member 4 task document
- the frozen protocol/shared contract documentation
- relevant existing AI-history records
- relevant Member 3 / Member 5 task documentation
- current PR11–PR13 implementation and tests

Build an internal checklist for every task M4-70 through M4-103.

Do not rely only on task titles. Read the detailed requirements and acceptance conditions.

Also inspect the current repository state and existing implementation before deciding what needs to be changed.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
2. TASK ORDER
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Execute the work in dependency order.

PR14:
M4-70 ML-KEM integration tests
M4-71 full secure-session integration
M4-72 secure payload round trip
M4-73 tamper tests
M4-74 unknown/expired 409 session-recovery integration
M4-75 same-envelope retry + idempotency
M4-76 storage-failure integration
M4-77 service-unavailable integration
M4-78 baseline E2E support
M4-79 secure E2E support
M4-80 Cloud/Legacy boundary verification

PR15:
M4-81 Dockerfile
M4-82 SQLite container persistence decision
M4-83 Docker readiness test
M4-84 CI Cloud checks
M4-85 AI-history workflow
M4-86 human AI-code review
M4-87 AI decision documentation

PR16:
M4-88 Cloud documentation
M4-89 Cloud technical debt
M4-90 Cloud threat model
M4-91 baseline vs modernized evaluation
M4-92 first vs steady-state analysis
M4-93 PQC observability demo
M4-94 corrupt-ciphertext demo
M4-95 storage-failure demo
M4-96 review Member 3 crypto
M4-97 review Member 2 baseline contract
M4-98 review Member 5 deployment assumptions
M4-99 dependency review
M4-100 static quality checks
M4-101 final baseline Cloud review
M4-102 modernized Cloud regression
M4-103 final Cloud quality pass

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
3. CRITICAL PROTOCOL REQUIREMENTS
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Preserve the frozen protocol.

ML-KEM:
- ML-KEM-768
- versioned public-key metadata
- compatible Gateway/Cloud byte formats
- do not assume every modified valid-length ciphertext raises an exception
- explicit failure injection must not be confused with natural ML-KEM rejection semantics

KDF:
- HKDF-SHA-256
- salt=None
- info exactly:
  "ml-kem-project:v1:gateway-cloud-session"
- output length exactly 32 bytes

AES-GCM:
- AES-256-GCM
- 32-byte session key
- 12-byte nonce

AAD:
exactly four frozen fields:
- protocol_version
- gateway_id
- session_id
- request_id

Do not introduce message_counter.

SecureEnvelope must contain:
- protocol_version
- gateway_id
- session_id
- request_id
- nonce
- ciphertext

No plaintext fallback or runtime downgrade path.

Session behavior:
- gateway ownership enforced
- TTL enforced
- unknown session -> 409 SESSION_INVALID
- expired session -> 409 SESSION_EXPIRED
- lookup -> ownership -> expiry ordering must remain correct
- do not silently extend expired sessions

Retry:
For an ambiguous/lost response, ordinary transport retry must resend the SAME already-built SecureEnvelope:
- same request_id
- same nonce
- same ciphertext
- same AAD
- same logical measurement

Do NOT perform a new encryption operation merely because the response was lost.

Business idempotency must ensure only one logical database row exists.

Document honestly that protocol v1 has no dedicated cryptographic anti-replay counter/window.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
4. M4-70–M4-80: INTEGRATION FIRST
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Do not merely add mocked unit tests.

Where the task requires Gateway↔Cloud integration, exercise the actual application boundaries and real implementations available in the repository.

M4-70 must prove:
Cloud public key
-> Gateway metadata validation
-> ML-KEM-768 encapsulation
-> Cloud decapsulation
-> equal shared secret
-> identical HKDF-derived session key

M4-71 must prove the complete session lifecycle.

M4-72 must prove actual encrypted canonical measurement round trip.

M4-73 must cover tampering of ciphertext and AAD-related fields and prove no unauthorized storage.

M4-74 must prove:
SESSION_INVALID / SESSION_EXPIRED
-> Gateway recovery
-> bounded retry
-> correct session replacement
-> same logical request

M4-75 must prove same-envelope retry and idempotent persistence.

M4-76 and M4-77 must exercise actual failure behavior rather than merely testing helper functions.

M4-78 and M4-79 must provide real baseline and secure E2E support using the repository's actual service boundaries.

M4-80 must verify that Cloud remains unaware of Legacy protocol internals:
- no Legacy timestamp field dependency
- no Legacy HTTP endpoint dependency
- no Legacy sensor implementation dependency
- no Legacy-specific failure semantics in Cloud

Cloud should consume the canonical Gateway contract only.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
5. MEMBER-TO-MEMBER COMPATIBILITY
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

A major goal of this work is to verify that Member 4's Cloud implementation actually interoperates with the work produced by the other members.

Do not assume compatibility just because unit tests pass.

Explicitly inspect and verify:

Member 3:
- ML-KEM-768 implementation
- key/ciphertext formats
- KDF semantics
- shared-secret derivation
- Gateway crypto wrapper behavior
- AAD construction
- secure-envelope construction

Member 2:
- CanonicalMeasurement fields
- types
- timestamps
- gateway_id
- received_at
- X-Request-ID handling
- baseline request/response behavior
- idempotency expectations

Member 5:
- service composition
- Docker/Compose topology
- ports
- environment variables
- database location
- health/readiness integration
- persistence behavior
- CI/container assumptions

If there is an actual incompatibility, determine the owning side from the authoritative task documents before modifying anything.

Do not silently redesign another member's protocol or architecture.

If another member's work is incomplete or unavailable, document the exact dependency and continue with all work that can legitimately be completed without inventing missing behavior.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
6. PR15: DOCKER / CI
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Implement M4-81–M4-87 completely.

Cloud Docker requirements include:
- correct Python/runtime version
- uv-compatible installation
- port 9000
- SIGTERM/shutdown support
- configurable SQLite location
- crypto dependencies available inside the image
- no machine-specific paths

M4-82:
support/document:
- persistent named-volume behavior for development/demo
- clean/ephemeral database behavior for automated tests
- never persist ML-KEM private keys or session secrets

M4-83:
verify clean container startup:
Cloud starts
-> DB initializes
-> ML-KEM initializes
-> /health works
-> /ready works

M4-84:
ensure CI covers the required Cloud and integration test categories.

Do not weaken existing CI checks merely to make the pipeline green.

M4-85–87:
maintain proper AI-history records and human-review documentation.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
7. PR16: DOCUMENTATION / REVIEW / EVALUATION
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Complete M4-88–M4-103, not merely code tasks.

Documentation must reflect the actual final implementation, not intended behavior.

M4-89:
document real technical debt, especially:
- ephemeral Cloud ML-KEM keys if applicable
- absence of a dedicated cryptographic replay counter/window
- any bounded course-scope limitations

M4-90:
produce a concrete Cloud threat model covering relevant assets, boundaries, threats, mitigations, and residual risks.

M4-91:
produce baseline vs modernized evaluation using actual measured data where available.
Do not invent performance results.

M4-92:
distinguish first-request/setup behavior from steady-state behavior using actual evidence.

M4-93:
PQC observability demo.

M4-94:
corrupt-ciphertext demo.
Do not falsely claim that every valid-length corrupted ML-KEM ciphertext naturally raises an exception.

M4-95:
storage-failure demo.

M4-96:
review Member 3 crypto integration and record actual findings.

M4-97:
review Member 2 baseline contract:
- CanonicalMeasurement fields
- timestamps
- gateway_id
- received_at
- X-Request-ID
- response/retry behavior
- received_at -> gateway_received_at

M4-98:
review Member 5 deployment assumptions:
- port
- database
- volume
- health/readiness
- environment variables
- crypto dependencies

M4-99:
review dependencies and remove unjustified dependencies only if this is clearly within Member 4 scope and safe.

M4-100:
run static quality verification and inspect the final diff for:
- secrets
- private keys
- DB artifacts
- .env files
- debug output
- temporary ciphertext dumps
- unrelated modifications

M4-101:
perform final baseline review.

M4-102:
perform full modernized regression and confirm:
- baseline mode still works explicitly
- ML-KEM mode works
- public-key schema remains correct
- session contract remains correct
- secure endpoint works
- AAD remains four-field
- no message_counter
- same-envelope retry remains idempotent
- 409 session recovery works
- failure injection works
- no plaintext downgrade
- query API remains intact
- health/readiness remain intact

M4-103:
final quality pass over the complete Member 4 implementation.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
8. AI-HISTORY REQUIREMENT
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

The project requires accurate AI-history.

Use separate AI-history task records where appropriate rather than creating one misleading giant history record.

Every implementation task must accurately record:
- task scope
- prompt
- significant AI work
- files created/modified
- tests/checks
- results
- decisions
- human review state
- revisions if needed

Do not mark a task Complete merely because code exists.

Do not claim a test, Docker run, CI run, E2E run, peer review, or external-member compatibility check that was not actually performed.

If something cannot be performed because a dependency is unavailable, record it honestly and continue with the remaining feasible work.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
9. CHANGE DISCIPLINE
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Prefer minimal, focused changes.

Reuse the existing implementation from M4-00–M4-69.

Do not rewrite working Cloud crypto/session/failure-injection infrastructure without a concrete reason.

Do not introduce:
- Redis
- Kafka
- Celery
- distributed databases
- unnecessary ORMs
- unrelated frameworks

unless the authoritative project requirements explicitly require them.

Do not weaken security or protocol guarantees to make tests pass.

Do not modify unrelated Member 2/3/5 implementation just to make the PR appear complete.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
10. VERIFICATION
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

At appropriate stages run focused tests.

At the end run, as applicable:

uv run pytest
uv run ruff check .
uv run ai-history check
git diff --check

Run the repository's Graphify refresh only according to its existing workflow and verify that only the two approved generated Graphify artifacts change.

Also inspect:

git status --short
git diff --stat
git diff --check

The final branch must contain only intended M4-70–M4-103 work plus required AI-history and approved generated artifacts.

&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;
11. FINAL STOP CONDITION
&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;&#61;

Do not commit or push anything yet.

Do not create the Pull Request yet.

When all feasible M4-70–M4-103 work is implemented and verified, stop at:

Awaiting Human Review

Then provide a concise report containing:

1. M4-70–M4-103 task-by-task status
2. Problems Found
3. Files changed
4. Tests/checks actually run and exact results
5. Member 2/3/5 compatibility findings
6. Any unresolved dependency or limitation
7. AI-history status
8. Graphify changes
9. Confirmation that M4-104+ was not started
10. Recommended human review points

Do not commit or push until I explicitly review and approve the result.

---

# AI Implementation — Initial

## LLM Output

Completed the feasible Member 4 PR14-PR16 integration, Cloud deployment, documentation, evaluation, review, and quality work. Reused the live Gateway-Cloud secure suite, added actual Legacy-Gateway-Cloud HTTP paths and Cloud/Legacy boundary checks, added a Cloud Dockerfile and explicit Cloud CI selection, and recorded measured local results and limits. Protocol v1 was not changed.

## Files Created

- cloud_service/Dockerfile
- cloud_service/docs/final-integration-and-operations.md
- cloud_service/tests/test_full_path_integration.py
- docs/ai/history/0111-m4-pr14-pr16-complete-cloud-integration-deployment-and-final-review.md

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- edge_gateway/docker/clean_container_crypto.py
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md
- tests/integration/test_gateway_cloud_secure.py
- tests/integration/test_gateway_crypto_image.py
- tests/integration/test_legacy_compatibility.py
- tests/integration/test_mode_evaluation.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest -q tests/integration/test_gateway_cloud_secure.py
- uv run pytest -q cloud_service/tests
- PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run pytest -q
- uv run ruff check .
- uv run ruff check cloud_service
- uv run ai-history check
- git diff --check
- uv run python scripts/refresh_graphify.py
- docker version

### Results

- 28 passed in 9.42s
- 503 passed, 1 Starlette deprecation warning in 8.75s
- 1190 passed, 4 skipped, 1 Starlette deprecation warning in 114.39s
- All checks passed
- All checks passed
- AI history validation passed before output
- Exit 0; only Git LF-to-CRLF notices
- Succeeded; only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md changed among tracked Graphify files
- Docker executable not installed; image/container runtime was not verified

## AI Notes

Task-by-task evidence and status:
PR14: M4-70 verified by test_versioned_public_key_retrieval, test_valid_encapsulation_matches_shared_secret_and_hkdf, test_malformed_mlkem_ciphertext_is_rejected, test_simulated_decapsulation_failure_leaves_no_session, and test_valid_length_mlkem_mutation_is_not_required_to_raise. M4-71 verified by secure session/envelope round-trip and AAD/nonce/Base64URL assertions. M4-72 verified by test_secure_envelope_round_trip_stores_canonical_measurement. M4-73 verified by expanded test_tampered_secure_message_is_rejected (ciphertext, nonce, request_id, gateway_id, session_id, version, tag; metrics/log and no row). M4-74 verified by expired/invalid 409 recovery and bounded second-rejection tests. M4-75 verified by test_ambiguous_transport_retries_the_same_envelope and test_duplicate_sequence_is_stored_once. M4-76 verified by test_cloud_failure_retries_the_same_secure_request_without_storage in storage_failure mode. M4-77 verifies 503 and two byte-identical retry attempts in service_unavailable mode; the requested Gateway retry counter does not exist in Member 3 PqcMetrics, so counter verification is outstanding. M4-78/79 verified at live Legacy client, Gateway app, Cloud HTTP and SQLite boundaries by test_legacy_gateway_cloud_http_path_persists_canonical_measurement, both modes; secure Gateway transport is injected because Gateway main() does not compose it. M4-80 verified by test_cloud_runtime_only_accepts_gateway_canonical_fields, including source import audit and rejection of Legacy timestamp payload.
PR15: M4-81 Cloud Dockerfile implemented (Python 3.12, frozen uv, port 9000, SIGTERM, non-root, configurable SQLite, maintained crypto dependency); image build unverified because Docker is not installed. M4-82 named-volume and ephemeral DB choices documented; local DB-reopen and empty-session-after-restart tested, container volume runtime unverified. M4-83 local startup/health/readiness and crypto initialization are covered by Cloud tests; clean Docker runtime remains unverified. M4-84 explicit Cloud and Gateway-Cloud CI selection added after existing full and Gateway checks; no CI run claimed. M4-85 task 0106 records the work and awaits review. M4-86 human checklist is in the authoritative Member 4 document; human review pending. M4-87 Cloud-local review document cites actual Modified-to-Accepted decisions for tasks 0072 and 0104, and explicitly records no observed Rejected human decision.
PR16: M4-88 operational/protocol documentation added; M4-89 technical debt and replay limitation documented; M4-90 threat/mitigation/residual-risk table added. M4-91/92 measured local baseline/secure first and steady paths plus storage, body size and decapsulation; sample and method documented without ranking. M4-93 session/expiry metric assertions and demo instructions added. M4-94 tamper/decryption metric and no-storage demo evidence added. M4-95 authenticated storage-failure, 503, same-body retry and no-row demo evidence added. M4-96 Member 3 crypto interface reviewed via live interoperability suite, with production composition and retry-counter gaps recorded. M4-97 Member 2 baseline contract reviewed via shared-fixture contract and live HTTP tests. M4-98 Cloud-side Member 5 deployment assumptions reviewed; Compose has no services and Docker runtime unavailable. M4-99 Cloud dependencies reviewed; no unjustified runtime dependency added. M4-100 Ruff, pytest, history and Git checks run and diff inspected. M4-101 baseline API/storage/query/health review passes local tests; Docker checkbox remains unverified. M4-102 secure protocol/regression tests pass; default Gateway executable composition remains external. M4-103 final Cloud quality review complete to tested scope, with the above limits carried forward.
Problems found: Windows Cloud DATABASE_URL formatting in existing integration harnesses, legacy HTTP test timeout under retries, Windows-only Linux-wheel test assumptions, and history test encoding; addressed only portable test/harness issues. No Cloud production protocol change. No secret, DB, .env or ciphertext dump was added. Untracked review-0104.diff was untouched. M4-104 and later not started. Docker/Compose and human review are not claimed complete.

---

# Human Review — Round 1

## Problems Found

No blocking problems identified during human review.

The documented limitations around the Gateway retry counter, Docker runtime verification, Gateway production-main secure transport composition, and Member 5 Compose wiring are acknowledged and considered non-blocking for this review. The implemented and verified integration, security, idempotency, regression, documentation, and quality checks are sufficient for acceptance at this stage.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- uv run pytest: 1190 passed, 4 skipped, 1 Starlette deprecation warning in 114.84s.
- uv run ruff check .: All checks passed.
- uv run ai-history check: AI history validation passed before final verification.
- git diff --check: exit 0; Git emitted only LF-to-CRLF notices.
- git status --short: only reviewed task files and the untouched pre-existing review-0104.diff; Graphify changes limited to graphify-out/graph.json and graphify-out/GRAPH_REPORT.md.

## Human-Confirmed Verification

Human review accepted task 0106 with no blocking problems, acknowledged the documented Gateway retry-counter, Docker runtime, Gateway production-main composition, and Member 5 Compose limitations as non-blocking, and requested final verification with completion if all required checks pass.

---

# Final Outcome

**Status:** Complete
