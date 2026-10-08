# Technical Documentation Plan & Structure

This specification establishes the structure, content requirements, and asset mapping for the **Part 1: Technical Documentation PDF** submission for the course *Software Development, Maintenance & Operations Project: ML-KEM Legacy Modernization with LLM Assistance* (University of Oulu, August–October 2026).

---

## 1. Submission Context & Core Constraints

Based on the course guidelines in `Group-Explanation 01.pdf` and `Group-Explanation 02.pdf`, alongside clarification from the course staff:

1. **Sole Vehicle of Technical Evaluation**: Evaluators will not clone or browse the Git repository, nor will they run the code locally. The final Technical Documentation PDF is the **sole artifact of record** for evaluating the implementation, architecture, test suites, operations, and AI collaboration.
2. **Single PDF Constraint**: The submission must be delivered as **one single PDF document**. It has no upper page limit and can be as thorough as needed.
3. **Course Deliverable Separation**:
   - **Part 1 (This Document)**: Technical documentation, architecture, code showcases, CI/CD, deployment configuration, testing, and AI evaluation (**40%** of course points).
   - **Part 2 (Handled by other team members)**: Project report focusing on one selected analytical lens (Cryptography & Mathematics, Quantum Threats & Attackers, or Organizational Cybersecurity), strictly $\le 5$ pages (**40%** of course points).
   - **Part 3 (Individual)**: 400–500 word individual reflection per student (**10%** of course points).
   - **Peer Review & Presentation**: Live demonstration and review (**10%** of course points).

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FINAL PROJECT SUBMISSION                              │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ PART 1: Technical Documentation PDF  │ PART 2: Project Report PDF           │
│ • Handled by: This Specification    │ • Handled by: Other team members     │
│ • Page Limit: Unlimited (Single PDF) │ • Page Limit: Max 5 pages            │
│ • Focus: Implementation, code,      │ • Focus: Analytical essay from 1 of  │
│   architecture, CI/CD, operations,   │   3 perspectives (math/threat/sec)   │
│   testing, and AI evaluation logs    │ • Academic citations, no raw code    │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Pedagogical Objectives to Address

The course documentation mandates that the technical documentation explicitly prove:

1. **LLM as an Untrusted Assistant**: Demonstrate that AI-generated code was treated as untrusted suggestions, validated through continuous manual review, static analysis, and automated testing.
2. **AI Audit Trail**: Report prompts used for significant tasks, relevant LLM outputs, context provided, and changes made by the students.
3. **Decisions & Rationale**: Explicitly document what was **Accepted**, **Modified**, or **Rejected**, explaining why decisions were made, how problems were found, and what residual risks remain.
4. **Baseline Analysis & Modernization**: Document the initial architecture, establish baseline measurements, and explain the safe transition to ML-KEM-768 on the Gateway-to-Cloud path while preserving legacy device compatibility.
5. **Operational Rigor**: Prove automated build and testing (CI/CD), containerized deployment (Docker Compose), health/readiness checks, secret-safe logging, and metrics.
6. **Critical Engineering Evaluation**: Document empirical mode comparisons, acknowledged technical debt, and active security/operational risks.

---

## 3. Master Table of Contents

The single PDF should be organized into eight cohesive chapters:

```text
1. Executive Summary & System Overview
2. Architecture & Protocol Specification
3. Component Design & Implementation Evidence
4. Operations, Deployment & CI/CD
5. Verification, Testing & Empirical Evaluation
6. AI-Assisted Development & Critical Evaluation
7. Technical Debt & Risk Analysis
8. Appendices (Configurations, Runbooks & Key Source Code)
```

---

## 4. Chapter-by-Chapter Content Specification

### Chapter 1: Executive Summary & System Overview
* **Purpose**: Establish project context, component roles, and boundaries within the first 3–4 pages.
* **Key Content**:
  * **System Role & Problem Statement**: Modernizing an IoT environmental telemetry pipeline to resist quantum threats (harvest-now-decrypt-later attacks) using ML-KEM-768 and AES-256-GCM.
  * **The Modernization Boundary**: Clarify that the Legacy Device remains unchanged (standard HTTP/JSON), while the Gateway-to-Cloud boundary implements post-quantum key establishment and authenticated encryption.
  * **High-Level Architecture Diagram**:
    ```text
    ┌─────────────────┐             ┌──────────────────┐             ┌─────────────────┐
    │  Legacy Device  │  HTTP/JSON  │   Edge Gateway   │   ML-KEM    │  Cloud Service  │
    │ (Sensor Sim)    ├────────────►│ (Seq/Validation/ ├────────────►│  (AEAD Decrypt/ │
    │                 │             │  PQC Transport)  │  AES-256-GCM│   SQLite Store) │
    └─────────────────┘             └──────────────────┘             └─────────────────┘
    ```
  * **Summary of Implemented Capabilities**:
    * Dual operating modes: Classical Baseline vs Modernized ML-KEM.
    * Fail-closed security policy (no runtime plaintext fallback).
    * Bounded retry logic and business idempotency.
* **Repository Sources**: `README.md`, `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`.

---

### Chapter 2: Architecture & Protocol Specification
* **Purpose**: Document the frozen contracts governing inter-service communication.
* **Key Content**:
  * **Dual Modes**:
    * Baseline Mode: `SECURITY_MODE=classical`, plain JSON to `POST /api/v1/baseline/measurements`, correlated via `X-Request-ID`.
    * Modernized Mode: `SECURITY_MODE=mlkem`, `PQC_FAILURE_POLICY=fail_closed`, session handshake via `POST /api/v1/pqc/sessions`, encrypted transport via `POST /api/v1/secure/measurements`.
  * **Cryptographic Protocol Definition**:
    * KEM Primitive: ML-KEM-768 (NIST FIPS 203) using a maintained library (`kyber-py`).
    * Key Derivation: HKDF-SHA-256 with `salt=None`, context `info=b"ml-kem-project:v1:gateway-cloud-session"`, deriving one 32-byte key.
    * Authenticated Encryption: AES-256-GCM with a 12-byte (96-bit) nonce.
    * Associated Data (AAD): Exactly 4 fields in sorted UTF-8 JSON (`protocol_version`, `gateway_id`, `session_id`, `request_id`).
    * Envelope: Exactly 6 fields (`protocol_version`, `gateway_id`, `session_id`, `request_id`, `nonce`, `ciphertext`). Base64URL encoding for binary fields.
  * **Session Lifecycle & Recovery Rules**:
    * 300-second session TTL, process-local memory storage.
    * Session error handling: `409 SESSION_INVALID` and `409 SESSION_EXPIRED` trigger exactly one session re-establishment attempt with an envelope rebuilt under the new session key while preserving the original `request_id`.
    * Ordinary transport retry: Resends the *identical* built envelope (same nonce, ciphertext, and AAD).
    * Business Idempotency: `UNIQUE(device_id, sequence_number)` constraint in SQLite. Explicitly document that business idempotency is *not* cryptographic anti-replay protection.
* **Repository Sources**: `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`, `docs/architecture/ml-kem-library-decision.md`.

---

### Chapter 3: Component Design & Implementation Evidence
* **Purpose**: Provide visible code excerpts and design logic for each tier since evaluators cannot browse the source tree.
* **Key Content**:
  * **Legacy Device (`legacy_system/`)**:
    * Environmental sensor simulation logic (temperature, humidity, sequence counter).
    * Serialization, HTTP client dispatch, and graceful shutdown handling.
    * Component-level fault injection mechanisms.
  * **Edge Gateway (`edge_gateway/`)**:
    * Ingestion endpoint (`POST /api/v1/measurements`).
    * Validation semantics: `400 Bad Request` for malformed JSON; `422 Unprocessable Entity` for semantic/domain validation failures; `409 Conflict` for duplicate or out-of-order sequences.
    * In-memory sequence tracking state machine per device.
    * Baseline HTTP forwarding vs PQC secure session manager and transport client.
  * **Cloud Service (`cloud_service/`)**:
    * Ephemeral ML-KEM key pair generation and public key endpoint (`GET /api/v1/pqc/public-key`).
    * Session decapsulation endpoint (`POST /api/v1/pqc/sessions`).
    * Secure ingestion endpoint (`POST /api/v1/secure/measurements`), envelope validation, AAD reconstruction, and AES-GCM decryption.
    * Storage repository with SQLite and query endpoint (`GET /api/v1/measurements`).
* **Repository Sources**: `docs/architecture/01 - Legacy Device.md`, `docs/architecture/02 - Edge Gateway.md`, `docs/architecture/03 - Cloud Service.md`, along with annotated code snippets from `legacy_system/src/`, `edge_gateway/src/`, and `cloud_service/src/`.

---

### Chapter 4: Operations, Deployment & CI/CD
* **Purpose**: Provide proof of automated operations, containerization, and observability.
* **Key Content**:
  * **Containerized Deployment**:
    * Topology walkthrough of `docker-compose.yml` orchestrating `legacy-device`, `edge-gateway`, and `cloud-service`.
    * Multi-stage or slim Dockerfile architectures ensuring minimal image footprint.
  * **Health & Readiness Architecture**:
    * Health (`/health`) and Readiness (`/ready`) probe contracts.
    * Highlight operational contract rule: *Active secure sessions are intentionally not required for service readiness*.
  * **Observability (Logging & Metrics)**:
    * Structured JSON logging format and correlation ID propagation.
    * Secret-safety audit: Formal proof and test cases verifying that private keys, shared secrets, and session keys are never written to logs.
    * Prometheus-style metrics contract (`/metrics`) exposing handshake latency, message counts, encryption durations, and failure counters.
    * Local operational monitoring dashboard overview.
  * **Continuous Integration (CI/CD)**:
    * Full architecture of GitHub Actions workflow (`.github/workflows/ai-history.yml`).
    * Document the gating stages: `uv sync --frozen`, `ruff check`, unit tests, contract tests, integration tests, `ai-history check`, Docker image builds, and Docker Compose system test.
* **Repository Sources**: `docker-compose.yml`, `.github/workflows/ai-history.yml`, `docs/RUNBOOK.md`, `docs/deployment/compose-test-environment.md`, `docs/operations/LOGGING_CONVENTIONS.md`, `docs/operations/SECRET_LOGGING_REVIEW.md`, `docs/operations/METRICS_CONVENTIONS.md`, `docs/operations/MONITORING_DASHBOARD_DECISION.md`.

---

### Chapter 5: Verification, Testing & Empirical Evaluation
* **Purpose**: Document system correctness, resilience under failure, and empirical performance differences.
* **Key Content**:
  * **Comprehensive Test Strategy**:
    * Test matrix covering unit tests, contract tests, component integration, and live end-to-end tests.
    * Component failure injection suite (simulating network timeouts, dropped responses, corrupted ciphertexts, storage failures).
  * **Security & Fail-Closed Regression Evidence**:
    * Tampered envelope test: Proof that tampered ciphertext or altered AAD is rejected with `400` without database insertion.
    * Handshake failure test: Proof that an invalid ML-KEM handshake fails closed without falling back to plaintext transmission.
    * Idempotency test: Proof that duplicate or retransmitted envelopes result in a single persistent row.
  * **Empirical Mode Comparison (Baseline vs ML-KEM)**:
    * Reproducible benchmarking methodology via `scripts/measure_mode_comparison.py`.
    * Comparative metrics table:
      * First-message latency (including handshake) vs steady-state latency.
      * Gateway-to-Cloud payload sizes (Plain JSON vs `SecureEnvelope`).
      * Handshake overhead vs per-message encryption cost.
* **Repository Sources**: `docs/testing/PROJECT_TEST_MATRIX.md`, `docs/testing/FAILURE_TEST_MATRIX.md`, `docs/testing/M5_SECURITY_REGRESSION_SUITE.md`, `docs/evaluation/baseline-vs-modernized-comparison.md`, `docs/evaluation/final-evaluation-evidence.md`.

---

### Chapter 6: AI-Assisted Development & Critical Evaluation
* **Purpose**: Satisfy the core pedagogical requirement of the course regarding LLM governance and critical human oversight.
* **Key Content**:
  * **AI Governance Framework**:
    * The repository's AI policy (`AGENTS.md`) and workflow (`docs/DEVELOPMENT_WORKFLOW.md`).
    * Treating the model as an untrusted code generator subject to frozen architectural constraints.
    * The custom `ai-history` CLI tracking prompts, diffs, human review states, and verification steps.
  * **Project-wide Decision Register**:
    * Inclusion of the high-level decision register (`docs/AI_DECISION_REGISTER.md`) capturing architectural choices made regarding CI, Docker, KDF parameters, and fallback prevention.
  * **Representative In-Depth Case Studies (Prompts, Outputs, Review, Fixes)**:
    * Select 4–6 concrete tasks demonstrating the full spectrum of human intervention:
      1. **Accepted Case**: E.g., baseline sensor model or CI pipeline setup where generated code complied with specifications.
      2. **Modified Case (Subtle Protocol Bug)**: E.g., AI attempted to regenerate nonces or re-encrypt on a transport retry, or introduced ad-hoc KDF parameters, caught and corrected by students to adhere to frozen contracts.
      3. **Modified Case (Security/Validation Violation)**: E.g., AI attempted to log sensitive handshake data or relaxed validation error status codes (returning 400 instead of 422), caught and corrected during code review.
      4. **Rejected Case (Architectural Scope Creep)**: E.g., AI suggested distributed message brokers (Kafka/Redis) or Kubernetes, rejected by students to preserve course scope.
      5. **Rejected Case (Security Policy Violation)**: E.g., AI proposed automatic plaintext fallback when an ML-KEM handshake failed, rejected to maintain strict `fail_closed` policy.
    * *Case Study Template*:
      * Task ID & Objective
      * Human Prompt & Context Provided
      * Raw LLM Output Summary
      * Student Critical Analysis & Flaws Identified
      * Action Taken & Code Diff / Fix Implemented
      * Verification Evidence (Tests Passed)
  * **AI History Inventory Summary**:
    * A consolidated summary table indexing all 210 tasks recorded in `docs/ai/history/` (Task ID, Name, Agent, Outcome: Accepted / Modified / Rejected).
* **Repository Sources**: `AGENTS.md`, `docs/AI_DECISION_REGISTER.md`, `legacy_system/docs/ai-decisions.md`, `edge_gateway/docs/ai-decisions.md`, `docs/ai/history/*.md`.

---

### Chapter 7: Technical Debt & Risk Analysis
* **Purpose**: Demonstrate engineering maturity by documenting accepted limitations and active operational risks.
* **Key Content**:
  * **Technical Debt Register (TD-1 through TD-12)**:
    * Unauthenticated Legacy Device boundary (TD-1).
    * In-memory sequence tracking and absence of persistent queues (TD-2, TD-3).
    * Ephemeral in-memory sessions and Cloud key pair (TD-4, TD-5).
    * Simplified Cloud public-key trust in controlled environment (TD-6).
    * HTTP transport without transport-layer authentication (TD-7).
    * SQLite single-instance storage (TD-8).
    * Bounded retry behavior (TD-9).
    * Business idempotency vs lack of cryptographic anti-replay counter/window (TD-10, TD-11).
    * Memory zeroization constraints in Python (TD-12).
  * **Risk Register (R-1 through R-9)**:
    * Public key substitution risk (R-1).
    * Legacy payload spoofing (R-2).
    * Authenticated envelope replay exposure (R-3).
    * Outage message drop risk (R-4).
    * Cascading retry amplification (R-5).
    * Restart state loss (R-6).
    * Diagnostic secret leakage (R-7).
    * Database corruption/contention (R-8).
    * Operator misconfiguration of security mode (R-9).
    * For each risk: Likelihood, Impact, Current Controls, and Residual Treatment.
* **Repository Sources**: `docs/technical-debt.md`, `docs/risk-register.md`.

---

### Chapter 8: Appendices (Complete Configurations & Key Code Listings)
* **Purpose**: Provide full source text for critical artifacts since the Git repository will not be submitted.
* **Key Content**:
  * **Appendix A: Deployment Configurations**:
    * Complete `docker-compose.yml`.
    * Complete Dockerfiles (`legacy_system/Dockerfile`, `edge_gateway/Dockerfile`, `cloud_service/Dockerfile`).
    * Complete `.env.example`.
  * **Appendix B: CI/CD Pipeline Definition**:
    * Complete `.github/workflows/ai-history.yml`.
  * **Appendix C: System Operational Runbook**:
    * Complete `docs/RUNBOOK.md` and presentation demo commands (`docs/presentation/demo-scenarios.md`).
  * **Appendix D: Core Cryptographic & Protocol Source Code**:
    * Gateway ML-KEM client and session manager (`edge_gateway/src/edge_gateway/crypto/`).
    * Secure envelope builder and AAD serializer.
    * Cloud ML-KEM service and AEAD decryption handler (`cloud_service/src/cloud_service/crypto/`).
    * Gateway sequence state machine (`edge_gateway/src/edge_gateway/sequence.py`).

---

## 5. Asset Mapping Table (Existing Docs $\rightarrow$ PDF Chapters)

| PDF Chapter | Primary Existing Repository Documents |
|---|---|
| **Ch 1: System Overview** | `README.md`, `docs/architecture/04 - Shared Cross-Component Protocol Specification.md` |
| **Ch 2: Architecture & Protocol** | `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`, `docs/architecture/ml-kem-library-decision.md` |
| **Ch 3: Component Design** | `docs/architecture/01 - Legacy Device.md`, `02 - Edge Gateway.md`, `03 - Cloud Service.md` |
| **Ch 4: Operations & CI/CD** | `docker-compose.yml`, `.github/workflows/ai-history.yml`, `docs/RUNBOOK.md`, `docs/deployment/compose-test-environment.md`, `docs/operations/*` |
| **Ch 5: Testing & Evaluation** | `docs/testing/PROJECT_TEST_MATRIX.md`, `docs/testing/FAILURE_TEST_MATRIX.md`, `docs/testing/M5_SECURITY_REGRESSION_SUITE.md`, `docs/evaluation/baseline-vs-modernized-comparison.md`, `docs/evaluation/final-evaluation-evidence.md` |
| **Ch 6: AI-Assisted Development** | `AGENTS.md`, `docs/AI_DECISION_REGISTER.md`, `legacy_system/docs/ai-decisions.md`, `edge_gateway/docs/ai-decisions.md`, `docs/ai/history/*.md` |
| **Ch 7: Technical Debt & Risks** | `docs/technical-debt.md`, `docs/risk-register.md` |
| **Ch 8: Appendices** | `docker-compose.yml`, Dockerfiles, `.github/workflows/ai-history.yml`, `docs/RUNBOOK.md`, selected files from `src/` |

---

## 6. Execution Strategy for Document Generation

To compile these materials into a unified PDF without formatting errors:

1. **Format Base**: Maintain chapters as modular Markdown files in a compilation directory (e.g., `docs/pdf_export/`).
2. **Recommended Tooling**:
   * **Pandoc + Typst**: Highly recommended for rapid, high-quality typography, code block syntax highlighting, and clean page numbering.
   * **Pandoc + LaTeX (Eisvogel template)**: Industry standard for academic/technical project reports.
   * **Python WeasyPrint Script**: Alternative lightweight HTML/CSS-to-PDF generation.
3. **Review Checklist Before Final Export**:
   - [ ] Ensure no secret keys, private keys, or actual credentials appear in code listings, logs, or AI history logs.
   - [ ] Verify that all code listings include line numbers and language syntax tags.
   - [ ] Confirm all tables (especially the 12 technical debts and 9 risks) render without text truncation.
   - [ ] Ensure the AI section clearly presents student critical evaluation (not just raw AI output).
   - [ ] Confirm table of contents hyperlinks and page numbers are consistent.

