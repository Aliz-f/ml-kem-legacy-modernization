# Legacy Device AI Decisions

This register records the architectural evaluations and human review decisions for AI-assisted development of the Legacy Device component (`legacy_system/`) under Task M1-24.

Across repository history, **zero AI tasks were rejected outright** (0 `Rejected` tasks in `docs/ai/history/`). Instead, the team practiced an iterative human-in-the-loop review workflow: when an AI-generated implementation exhibited flaws, omissions, or architectural drift, the human reviewer issued a decision of **`Modified`** with explicit "Problems Found" and "Requested Modifications". In `legacy_system/`, **12 tasks underwent human-directed revisions** before achieving final acceptance.

> **Terminology Note**: In this document, **Member 1 Tasks** (`M1-XX`) refer to the architectural deliverables defined in [`docs/architecture/06 - Member 1 Tasks.md`](../../docs/architecture/06%20-%20Member%201%20Tasks.md). **AI Records** (`Record NNNN`) refer to the corresponding provenance logs in `docs/ai/history/`.

---

## 1. Component Scope and Architectural Baseline

The Legacy Device (`legacy_system/`) simulates a constrained, outbound-only IoT sensor appliance deployed at the physical edge:
- **Python Standard Library Architecture**: Implemented entirely with Python 3.12 standard library modules (`urllib.request`, `dataclasses`, `logging`, `signal`, `json`), strictly avoiding external networking or validation frameworks (`requests`, `httpx`, `pydantic`).
- **Outbound-Only Network Profile**: The device functions exclusively as an HTTP client sending data to `POST /api/v1/measurements`. It exposes zero listening ports and runs no server.
- **Outside PQC Boundary**: The legacy link remains unencrypted and unauthenticated HTTP/JSON. The component contains no ML-KEM, HKDF, or AES-GCM logic.
- **Wire Purity**: Zero diagnostic markers (e.g. `failure_simulation` flags or `X-Simulation` headers) are emitted on the wire. Downstream components evaluate every request purely on payload merits.
- **Monotonic Sequence Integrity**: The internal sensor sequence counter advances monotonically across generated readings and never rewinds or rolls back upon delivery failures.

---

## 2. Representative Case Examples from Member 1 AI Tasks

The following entries provide representative case examples across the core functional modules of the Legacy Device, detailing initial AI outputs, issues identified during human review, and the resulting human-directed revisions:

### Configuration Management — Task M1-01 (`config.py` / Record 0008)
- **AI Initial Output**: The AI generated basic environment parsing and default values in `config.py`.
- **Problems Found in Human Review**: While the runtime code parsed values, the test suite (`test_config.py`) omitted explicit tests for negative `SEND_INTERVAL_SECONDS` and negative `REQUEST_TIMEOUT_SECONDS`, both of which were mandatory contract requirements.
- **Decision**: **Modified**.
- **Human-Directed Revision**: Added focused negative boundary tests verifying that non-positive intervals and timeouts raise `ConfigurationError` and halt process startup immediately. Third-party configuration libraries (`pydantic`, `python-dotenv`) were strictly rejected in favor of an immutable frozen `Config` dataclass.

### Measurement Model & Sensor Generation — Tasks M1-02 & M1-03 (`sensor.py` / Records 0012, 0027)
- **AI Initial Output**: Created the `Measurement` model and `Sensor` generator.
- **Problems Found in Human Review**:
  - *Record 0012 (M1-02)*: Pylance emitted static type warnings when comparing float bounds against `numbers.Real` in `_validate_number`. Additionally, test coverage lacked verification that a timezone-aware timestamp with a non-UTC offset correctly normalizes to UTC with trailing `Z`.
  - *Record 0027 (M1-03)*: Review required explicit verification of monotonic sequence progression starting at `0`.
- **Decision**: **Modified**.
- **Human-Directed Revision**: Converted validated numbers to local `float` before range assertions without altering field types, enforced UTC normalization ending in `Z`, and verified strict sequence monotonicity.

### Failure Simulation Engine & Wire Purity — Tasks M1-04 & M1-19 (`failure.py` / Records 0034, 0193)
Task M1-04 was the most heavily scrutinized task in the component, undergoing **4 iterative human review rounds**:
- **Problems Found in Human Review (Record 0034)**:
  - *Round 1 (Modified)*: The AI generated hardcoded, static mutation values (e.g. constant `150.0` for invalid temperature) across all runs. Tests did not verify seed-dependent variability, nor did they confirm that the underlying domain `Measurement` object remained unmutated.
  - *Round 2 (Modified)*: Injected duplicate sequence on the first reading returned the current sequence and emitted a false error log even though no prior sequence history existed. Test helpers also duplicated construction logic.
  - *Round 3 (Modified)*: Out-of-order sequence simulation lacked negative clamping checks.
- **Decision**: **Modified** (accepted in Round 4).
- **Human-Directed Revision & Safety Safeguards (Record 0193 / Task M1-19)**:
  1. *Domain / Wire Separation*: Preserved `Measurement` as an immutable domain object (`frozen=True`); mutations operate exclusively on the outbound dictionary or serialized string.
  2. *Sequence Generator Preservation*: Prohibited rewinding or resetting `Sensor._sequence_number` during duplicate or out-of-order simulation; the sensor continues incrementing while the injector overrides only the outgoing dictionary.
  3. *Wire Purity*: Strictly rejected embedding simulation markers (`failure_simulation: true` or `X-Simulation` headers) on the wire.
  4. *PRNG Isolation*: Replaced global `random.seed()` calls with an isolated `random.Random(seed)` instance to prevent polluting system or test entropy.

### Gateway HTTP Client & Retry Policy — Tasks M1-05 & M1-06 (`client.py` / Records 0052, 0053)
- **AI Initial Output**: Implemented `GatewayClient` with basic retries and HTTP exception handling.
- **Problems Found in Human Review**:
  - *Record 0052 (M1-05)*: The client failed to catch `http.client.HTTPException` variants, allowing raw protocol-level library exceptions to escape to callers instead of being classified as `ErrorCategory.CONNECTION`. An unintended `cloud.db` file was also generated during test execution.
  - *Record 0053 (M1-06)*: The public constructor accepted non-integer `max_retries` values (such as `True` or `1.5`), sleep delays occurred after the final attempt was exhausted, and mixed retryable-to-non-retryable transitions were untested.
- **Decision**: **Modified**.
- **Human-Directed Revision & Architectural Rules**:
  1. *Bounded Retries*: Rejected infinite retries; enforced `attempt_count <= self._max_retries` (default 2) with exponential backoff ($2^{\text{attempt}-1}$ seconds).
  2. *Non-Retryable Client Errors*: Categorically rejected retrying HTTP `400 Bad Request` (malformed JSON), HTTP `409 Conflict` (sequence rejection), and HTTP `422 Unprocessable Entity` (domain/schema invalidity). Retrying invalid payloads or duplicate sequences will never repair them.
  3. *Retryable Transient Faults*: Restricted retries to `500`, `502`, `503`, `504`, connection refusal, and socket timeouts.
  4. *Strict Typing & Backoff Math*: Enforced `isinstance(max_retries, int) and not isinstance(max_retries, bool)` and eliminated sleep delay after the final attempt.

### Device Controller & Graceful Shutdown — Tasks M1-07 & M1-08 (`device.py`, `main.py` / Records 0086, 0087)
- **AI Initial Output**: Implemented `DeviceController` run loop and internal signal handlers.
- **Problems Found in Human Review**:
  - *Record 0086 (M1-07)*: Dependency injection used Python truthiness checks (`self._sensor = sensor or Sensor(...)`), risking silent overwrite of valid falsey custom objects. Sequence preservation across network exceptions was also untested.
  - *Record 0087 (M1-08)*: The architecture lacked a runnable production composition root (`main.py`) or console entry point; signals were tested only by invoking handler functions directly rather than verifying OS process boundary termination.
- **Decision**: **Modified**.
- **Human-Directed Revision**:
  1. *Explicit Dependency Injection*: Replaced truthiness checks with explicit `if sensor is not None:` identity checks.
  2. *Composition Root*: Created `legacy_system/src/legacy_system/main.py` and registered the `legacy-device` console script in `pyproject.toml`.
  3. *Process-Boundary Signals*: Tested cooperative shutdown via `SIGTERM` and `SIGINT` using interruptible `threading.Event.wait()`, exiting cleanly with code 0.

### Structured Logging & Observability — Task M1-09 (`logging` / Record 0090)
- **AI Initial Output**: Implemented operational event logging.
- **Problems Found in Human Review**: The initial AI implementation included a test that ran the controller loop indefinitely, causing pytest to hang. Additionally, the AI attempted an unauthorized global monkeypatch of `pathlib` across the repository to address Windows console encoding issues, and duplicated retry log events.
- **Decision**: **Modified**.
- **Human-Directed Revision**: Replaced the hanging test with a deterministic, event-bounded loop test; stripped the unauthorized global monkeypatch; and enforced structured key-value log formatting (`event=... device_id=... sequence_number=... status_code=...`) while omitting raw payloads and private sensor values.

### Container Packaging & Security Profile — Tasks M1-13 & M1-14 (`Dockerfile` / Records 0186, 0187)
- **AI Initial Output**: Containerized the Legacy Device using Docker and Docker Compose.
- **Review Evaluation**:
  1. *Non-Root Execution*: Enforced `USER 10001:10001` unprivileged execution.
  2. *Zero Exposed Ports*: Rejected proposals to expose HTTP ingress ports (`/health` or `/metrics`). Legacy Device is an outbound client only; listening on open ports mismodels edge sensor hardware and expands attack surface.
  3. *Signal Orchestration*: Configured `STOPSIGNAL SIGTERM` to ensure immediate container shutdown without hitting Docker `SIGKILL` timeouts.
- **Decision**: **Accepted**.

### Static Code Quality & Hygiene Enforcement — Task M1-20 (`test_static_quality.py` / Record 0194)
- **Review Evaluation**: Built automated AST static verification to mechanically enforce component hygiene: zero `breakpoint()`/`pdb`/debug prints, no PEM private key blocks, no `.env` files, and clean component boundaries (blocking imports of `cloud_service`, `edge_gateway.crypto`, `cryptography`, or `oqs`).
- **Decision**: **Accepted**.

---

## 3. Critical Reflection on AI-Assisted Engineering

### Observed AI Failure Patterns
Across Member 1 tasks, AI code generation repeatedly exhibited characteristic failure modes:
1. **Shallow Happy-Path Testing**: AI routinely generated tests asserting only successful execution or mock-only behaviors, omitting negative boundary conditions (e.g. Tasks M1-01, M1-06).
2. **Global State Pollution**: AI frequently resorted to global mutations to solve local problems, such as proposing global `random.seed()` in Task M1-04 or injecting an unauthorized global `pathlib` monkeypatch in Task M1-09.
3. **Python Truthiness Hazards**: Defaulting to `x or default` instead of explicit identity checks (`if x is not None:` in Task M1-07), creating subtle object replacement bugs.
4. **Architectural Boundary Drift**: Proposing unnecessary third-party frameworks (`requests`, `pydantic`, `FastAPI`) or proposing wire diagnostic markers (`failure_simulation: true`) that violate component simplicity and wire purity.
5. **Infinite Loops in Async/Timer Logic**: Creating tests that block or run indefinitely because loop termination conditions were not bounded by deterministic events (Task M1-09).

### Effectiveness of Human-in-the-Loop Oversight
The 12 `Modified` human review decisions demonstrate that manual human inspection was indispensable. Automated linters (`ruff`) and initial passing test suites verified syntax and local mechanics, but could not detect architectural boundary erosion, leaking exceptions, or state pollution.

By combining prompt discipline, rigorous manual code review, and automated AST static guardrails, the team leveraged AI acceleration while maintaining absolute architectural integrity.

---

## 4. Retained Operational Risks and Technical Debt

The Legacy Device intentionally retains several operational limitations characteristic of older embedded equipment:
- **In-Memory Sequence State**: The sequence counter resets to `0` upon container restart. If the Gateway has recorded higher sequence numbers, subsequent readings will be rejected as `409 Conflict` until the counter advances beyond the high-water mark.
- **Absence of Local Store-and-Forward**: If the Edge Gateway is unreachable, unsent measurements are dropped once `MAX_RETRIES` are exhausted. No local disk queue exists.
- **Cleartext Legacy Transport**: Communication between Legacy Device and Edge Gateway is unencrypted HTTP/JSON, reflecting a legacy edge environment.

These items are tracked in the [Legacy Technical Debt Register](technical-debt.md) (Task M1-25) and project-wide registers ([`docs/technical-debt.md`](../../docs/technical-debt.md)).
