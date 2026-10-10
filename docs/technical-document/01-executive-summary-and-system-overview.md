# Chapter 1 — Executive Summary and System Overview

> **Document role.** This is the standalone source for Chapter 1 of the Part 1
> Technical Documentation.  It is written to be compiled with the other
> chapter files into one PDF.  Links identify repository evidence that should
> be retained as cross-references in the final PDF.

## 1.1 Project purpose

This project modernizes a small environmental-telemetry pipeline without
requiring a redesign of its simulated legacy sensor.  The system carries
temperature and humidity measurements from a Legacy Device, through an Edge
Gateway, to a Cloud Service for durable storage.  The modernization addresses
the risk that data protected today with quantum-vulnerable public-key
cryptography could be captured now and decrypted later.  Its scope is therefore
deliberately narrow: it introduces post-quantum key establishment only on the
Gateway-to-Cloud path, where the legacy protocol can be translated and secured
without changing the device-facing interface.

The project was also an exercise in safe AI-assisted software development.  The
course requires an LLM to be used as an assistant, not as an authority.  The
team therefore treated generated code and design proposals as untrusted until
they had been checked against frozen architecture, reviewed by humans, and
validated with static analysis, automated tests, integration tests, and
operational evidence.  The complete prompts, outcomes, review decisions, and
verification records are maintained in the repository's AI-history register
and are presented in Chapter 6.

The result is a course-sized, reproducible modernization demonstrator rather
than a production IoT platform.  It provides a baseline mode for comparison,
a modernized ML-KEM mode, containerized deployment, observability, controlled
failure injection, and evidence-oriented testing.  It intentionally does not
add unrelated platform services such as a message broker, distributed database,
Kubernetes, user accounts, or device-fleet management.

## 1.2 System at a glance

```text
┌─────────────────────┐       HTTP + JSON         ┌─────────────────────┐
│    Legacy Device    │ ───────────────────────►  │    Edge Gateway     │
│                     │                           │                     │
│ • sensor simulation │                           │ • validation        │
│ • UTC timestamp     │                           │ • normalization     │
│ • sequence number   │                           │ • sequence tracking │
│ • legacy HTTP client│                           │ • mode selection    │
└─────────────────────┘                           │ • secure transport  │
                                                  └──────────┬──────────┘
                                                             │
                           Classical: canonical JSON         │
                           Modernized: ML-KEM-768, HKDF,     │
                           AES-256-GCM SecureEnvelope        │
                                                             ▼
                                                  ┌─────────────────────┐
                                                  │    Cloud Service    │
                                                  │                     │
                                                  │ • key/session side  │
                                                  │ • decrypt/validate  │
                                                  │ • idempotency       │
                                                  │ • SQLite storage    │
                                                  │ • query/operations  │
                                                  └─────────────────────┘
```

The architecture has two intentionally different communication boundaries:

1. **Legacy Device → Edge Gateway.** The device sends a five-field measurement
   through `POST /api/v1/measurements` as ordinary HTTP/JSON.  It remains
   compatible with the legacy-side representation and contains no ML-KEM or
   Cloud-specific behavior.
2. **Edge Gateway ↔ Cloud Service.** The Gateway translates validated data to a
   canonical representation and selects either the explicit baseline transport
   or the modernized secure transport.  The Cloud is never contacted directly
   by the Legacy Device.

This separation is the core migration strategy: the Gateway is both the
protocol adapter and the modernization boundary.  It lets the project add
post-quantum protection where it is feasible while preserving the device-side
interface that a real deployed legacy device could be unable to change.

## 1.3 Components, responsibilities, and boundaries

| Component | Primary responsibilities | Explicit boundary |
| --- | --- | --- |
| Legacy Device | Simulate temperature and humidity readings; assign a stable device ID, UTC timestamp, and monotonically increasing sequence number; serialize and send a legacy measurement; apply bounded device-side retries and controlled faults. | Does not implement ML-KEM, session management, Cloud communication, encryption, or storage. |
| Edge Gateway | Receive the legacy API request; validate and normalize it; enforce per-device sequence policy; create a correlation/request ID; deliver in baseline or secure mode; manage Gateway-side sessions, retries, logging, and metrics. | Returns `202 Accepted` only after Cloud acceptance.  It does not own durable measurement storage or change the meaning of validated measurements. |
| Cloud Service | Expose baseline and secure Gateway APIs; own the ML-KEM key pair and session lifecycle; authenticate/decrypt secure messages; revalidate canonical data; enforce idempotency; persist and query measurements; expose operational endpoints. | Does not accept the Legacy Device wire format and does not communicate directly with devices. |

The canonical boundary also preserves clear ownership.  The Legacy component
owns sensing and its client; the Gateway owns legacy-facing application
behavior, normalization, sequencing, baseline delivery, and secure transport;
the Cloud owns cryptographic receiving behavior, validation, idempotency, and
SQLite storage.  Repository-wide work owns Docker, CI/CD, end-to-end testing,
and metrics integration.  This division prevented the modernized protocol from
leaking into the legacy simulator and made each component independently
testable.

## 1.4 Modernization modes

The system implements two deliberately separate operating modes.  Mode choice
is configuration, not an automatic fallback decision.

| Concern | Classical baseline | Modernized ML-KEM |
| --- | --- | --- |
| Gateway setting | `SECURITY_MODE=classical` | `SECURITY_MODE=mlkem` |
| Cloud delivery | `POST /api/v1/baseline/measurements` | Public-key retrieval, session establishment, then `POST /api/v1/secure/measurements` |
| Data protection on Gateway–Cloud path | Canonical JSON over the baseline test path | ML-KEM-768 establishes a session secret; HKDF-SHA-256 derives one 32-byte key; AES-256-GCM protects each canonical payload |
| Correlation | `X-Request-ID` header | `request_id` is inside authenticated associated data (AAD) and the secure envelope |
| Failure policy | Bounded delivery retry and visible failure | `PQC_FAILURE_POLICY=fail_closed`; no runtime plaintext downgrade |

The baseline is retained as an observable comparison point, not as a silent
fallback.  In modernized mode, a cryptographic or session-establishment problem
causes the secure operation to fail closed.  That design makes the security
state explicit and enables empirical comparison of the baseline and modernized
paths in Chapter 5.

At a high level, secure mode performs the following sequence:

```text
1. Gateway obtains the Cloud ML-KEM-768 public key.
2. Gateway encapsulates a shared secret and asks Cloud to create a session.
3. Both parties derive the same 32-byte session key using the frozen HKDF context.
4. Gateway encrypts a canonical measurement with AES-256-GCM.
5. Cloud reconstructs the authenticated metadata, decrypts, validates, and stores it.
6. Gateway returns success to the Legacy Device only after the Cloud accepts it.
```

Protocol v1 fixes the security-critical details: a 300-second process-local
session lifetime; a 12-byte AES-GCM nonce; Base64URL for binary JSON values;
and a six-field `SecureEnvelope`.  Its AAD contains exactly the four visible
metadata fields `protocol_version`, `gateway_id`, `session_id`, and
`request_id`, serialized as compact, sorted UTF-8 JSON.  The full wire
contracts, KDF parameters, session recovery rules, and negative cases are
specified in Chapter 2; they are not redefined by this overview.

## 1.5 End-to-end processing and reliability model

A normal measurement follows this path:

```text
Sensor simulation
  → legacy JSON measurement
  → Gateway schema/domain validation
  → canonical measurement + sequence-policy decision
  → baseline delivery OR secure session/envelope delivery
  → Cloud validation and idempotent SQLite persistence
  → Gateway 202 response to the Legacy Device
```

The Gateway distinguishes malformed syntax (`400 Bad Request`) from parsed
JSON that is missing required fields, has wrong types, or violates a domain
constraint (`422 Unprocessable Entity`).  Duplicate and out-of-order device
sequence numbers produce `409 Conflict`; gaps are accepted and recorded as an
operational signal.  Gateway sequence state is updated after validation and
sequence-policy acceptance, before Cloud delivery, and is not rolled back if
Cloud delivery fails.  These choices make the synchronous delivery behavior
deterministic and visible during failure testing.

Retries are deliberately bounded.  A normal Gateway-to-Cloud transport retry
resends the exact already-built secure envelope: the request ID, session ID,
nonce, ciphertext, and AAD remain unchanged.  Only `409 SESSION_INVALID` or
`409 SESSION_EXPIRED` initiates one session-recovery attempt: the old session
is invalidated, one replacement session is created, a new envelope is built
under its new key, and the logical request ID is preserved.  This distinction
avoids accidental re-encryption during an ordinary retry while permitting
recovery from expired or invalid session state.

Cloud persistence uses the business key `UNIQUE(device_id, sequence_number)`.
It prevents duplicate logical measurement rows, including retransmission
outcomes, but is explicitly not cryptographic anti-replay protection.  Protocol
v1 intentionally has no dedicated replay counter or replay window; that
limitation, along with the in-memory session and sequence state, is documented
as technical debt and risk rather than hidden by the overview.

## 1.6 Engineering effort and evidence trail

The implementation followed a staged modernization path rather than attempting
to build a PQC system all at once:

```text
Frozen architecture and contracts
  → shared repository workflow and baseline components
  → baseline end-to-end delivery and measurements
  → ML-KEM, session, and authenticated-encryption integration
  → secure end-to-end and failure/security regression testing
  → observability, Docker Compose, CI/CD, evaluation, and documentation
```

This order matters.  A functioning classical baseline makes the added cost and
behavior of session establishment and authenticated encryption measurable.
Contract tests, component tests, integration tests, live system tests, failure
injection, static analysis, and reproducible comparison scripts were used to
check different layers of the system.  Docker Compose runs the three-service
test topology; CI validates the locked environment, quality checks, tests,
history integrity, image builds, and system-level behavior.  The operational,
verification, and empirical evidence is detailed in Chapters 4 and 5.

AI assistance was governed through a task-by-task history workflow: a task was
recorded, the proposed work was inspected against the architecture, actual
checks were recorded, and human review and final verification were required.
The project does not treat a passing test suite as a substitute for human
judgment.  Chapter 6 consolidates the prompt and decision evidence; Chapters 7
and 8 make the remaining limitations and key executable artifacts visible to
evaluators who do not inspect the source repository.

## 1.7 Scope, assumptions, and acknowledged limitations

The design is intentionally constrained to a controlled test environment.  The
Legacy-to-Gateway HTTP/JSON boundary is not post-quantum protected; the
modernization applies only after the Gateway.  The Cloud public key is trusted
at the explicitly configured endpoint in this environment.  Cloud ML-KEM key
material, Gateway session state, and Gateway sequence state are process-local,
so restarts remove that transient state.  Storage is single-instance SQLite;
the transport is HTTP-only; and the design provides neither a persistent queue
nor a distributed replay-control mechanism.

These are not claims of production readiness.  They are conscious scope
decisions that kept the work aligned with the course objective: safely integrate
a maintained ML-KEM implementation into a legacy system, demonstrate the
result, critically assess it, and document residual technical debt and risk.

## 1.8 Guide to the remaining technical documentation

| Chapter | What it contributes |
| --- | --- |
| 2. Architecture and Protocol Specification | Frozen endpoint, schema, cryptographic, session, retry, error, and storage contracts. |
| 3. Component Design and Implementation Evidence | Component-level design, selected source listings, and ownership evidence. |
| 4. Operations, Deployment and CI/CD | Compose topology, health/readiness, logging, metrics, dashboard, and CI gates. |
| 5. Verification, Testing and Empirical Evaluation | Test matrix, fault/security evidence, and baseline-versus-modernized measurements. |
| 6. AI-Assisted Development and Critical Evaluation | Prompt records, human decisions, fixes, and verification evidence. |
| 7. Technical Debt and Risk Analysis | Accepted limitations, risks, controls, and residual treatment. |
| 8. Appendices | Complete configurations, runbooks, and selected critical source listings. |
