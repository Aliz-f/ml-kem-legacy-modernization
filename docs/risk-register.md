# Project-wide risk register

This is the Member 5 coordination register for M5-82. It records active
security and operational events, their current controls, and residual exposure.
It is distinct from the accepted implementation limitations in the
[technical-debt register](technical-debt.md): a debt is a known design gap;
a risk is an event that can arise from that gap or from the operating context.

Likelihood and impact are qualitative course-project assessments, not measured
production probabilities or guarantees.

| ID | Risk event | Type | Linked debt | Likelihood | Impact | Current controls | Residual treatment |
|---|---|---|---|---|---|---|---|
| R-1 | An attacker substitutes the Cloud ML-KEM public key or impersonates the configured Cloud endpoint. | Security | TD-6, TD-7 | Context-dependent | High | Gateway checks protocol version, algorithm, key ID, and key encoding; controlled environment constrains exposure. | Accept only for the test environment; require authenticated Cloud identity before production use. |
| R-2 | A party spoofs or modifies Legacy → Gateway traffic. | Security | TD-1 | Context-dependent | High | Gateway validates syntax, schema, domain, and sequencing, but these do not authenticate a sender. | Treat the legacy boundary as untrusted; design device authentication before broader deployment. |
| R-3 | A captured authenticated secure envelope is replayed. | Security | TD-11 | Context-dependent | Medium | AES-GCM authenticates the envelope; Cloud business idempotency avoids a duplicate logical row. | Record that idempotency is not cryptographic replay protection; use a versioned replay design if the threat model requires it. |
| R-4 | Gateway or Cloud outage causes a measurement delivery failure or loss. | Operational | TD-2, TD-9 | Medium | Medium | Legacy and Gateway retries are bounded; failures are visible rather than falsely accepted. | Monitor delivery failures and adopt durable buffering only with redesigned acceptance semantics. |
| R-5 | Retry layers increase downstream work during an outage. | Operational | TD-9 | Medium | Medium | Retry counts are bounded and regression-tested; repeated Legacy delivery is stopped by committed sequence state. | Reassess retry budgets and ownership before higher-rate use. |
| R-6 | Gateway or Cloud restart loses sequence/session/key state. | Operational | TD-3, TD-4, TD-5 | Medium | Medium | Session-invalid/expired recovery is bounded; Cloud key/session restart behavior is documented. | Exercise restart recovery and introduce persistent state only through an approved design. |
| R-7 | Future diagnostics expose private keys, shared secrets, session keys, or plaintext. | Security / operational | TD-12 | Low in current tests; context-dependent in future changes | High | Structured logging limits fields; secret-log and static checks run in CI. | Maintain secret-safety checks in review and do not place sensitive material in logs, history, or diagnostics. |
| R-8 | SQLite corruption, contention, or single-instance loss affects Cloud availability. | Operational | TD-8 | Low to medium | Medium | Storage errors return safe failures; temporary test databases make current regression runs deterministic. | Use backups, monitoring, and a production persistence/availability design when requirements demand it. |
| R-9 | An operator intentionally selects `SECURITY_MODE=classical` in a context that requires protected Gateway → Cloud transport. | Security / operational | TD-7 | Context-dependent | High | Mode is explicit configuration; `mlkem` failures are fail closed and never automatically downgrade. | Restrict and review deployment configuration; make security-mode selection part of operational approval. |

## Scope boundary

The risk register does not claim that the current controls remove the listed
risks. In particular, fail-closed behavior prevents automatic plaintext
fallback in `SECURITY_MODE=mlkem`, but it does not authenticate the Legacy
boundary, add Cloud identity authentication, create durable buffering, or add
cryptographic replay protection.
