# Project-wide AI decision register

This Member 5 register implements M5-96. It records material AI-assisted
deployment, CI, and operational design decisions for the course project. It
does not replace the per-task AI-history record, its human review, or its final
verification. The frozen architecture remains authoritative over this register.

The entries below are deliberately limited to decisions supported by the
repository's frozen scope and implementation evidence. The rejected directions
are documented scope decisions, not claims that an unrecorded conversation or
a particular person proposed them.

| ID | AI-assisted direction considered | Decision | Reason and retained evidence |
|---|---|---|---|
| AD-1 | Separate CI into quality, component/repository tests, integration tests, secure E2E, image build, and clean-environment Compose validation. | Accepted | This provides the course-required automated build, testing, and deployment evidence while keeping each job understandable. The accepted implementation is `.github/workflows/ai-history.yml`; task `0174` records human review and final verification. |
| AD-2 | Run only unit tests as the CI quality signal. | Modified | Unit tests remain a fast layer, but they are insufficient for the frozen Gateway--Cloud contracts and operational recovery. The workflow additionally runs protocol contracts, integration, secure E2E, Docker builds, and the Compose regression. |
| AD-3 | Use an unconstrained `uv sync` in CI. | Modified | CI uses `uv sync --frozen` so the committed lockfile is itself verified. This prevents a green CI run from silently resolving a different dependency graph. |
| AD-4 | Mark test or quality steps `continue-on-error`. | Rejected | A failed quality, protocol, or deployment check must block the pipeline. The workflow has no `continue-on-error` test bypass. |
| AD-5 | Add Kubernetes, a service mesh, or clustered infrastructure for the course deployment. | Rejected | The frozen scope is a small Docker/Compose test environment with single Gateway and Cloud instances. Such infrastructure adds operational complexity without satisfying a current project requirement. |
| AD-6 | Add Kafka, Redis, or a message broker for retry buffering. | Rejected | The frozen design deliberately uses bounded HTTP retries, in-memory Gateway sequence/session state, and SQLite. Durable buffering would change delivery and acceptance semantics and requires an architecture change. |
| AD-7 | Build and validate all three service images while keeping the current Compose stack limited to Cloud and Gateway. | Accepted | The Legacy Device is a client runtime and is image-validated separately; the documented Compose regression remains a two-service operational test. This boundary is implemented in task `0174` and documented in `docs/testing/DEVELOPER_TESTING_GUIDE.md`. |

## Evaluation and remaining risks

The accepted CI/Docker work was reviewed against working directories, frozen
dependency installation, skipped tests, failure propagation, secret exposure,
untrusted scripts, branch triggers, image build coverage, and clean-runner
Compose execution. It does not make the system production-grade: the project
retains the documented single-instance, SQLite, in-memory state, and simplified
Cloud-key-trust limitations in [the technical-debt register](technical-debt.md)
and [risk register](risk-register.md).

These decisions intentionally do not authorize Kubernetes, brokers, persistent
session state, a plaintext fallback, or any protocol change. A future proposal
that changes an endpoint, storage mapping, retry/session behavior, or crypto
contract must first update the frozen architecture documents and receive human
review through the normal AI-history workflow.
