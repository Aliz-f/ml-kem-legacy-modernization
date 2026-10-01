# Gateway crypto AI-history

Generated Gateway crypto code is untrusted until a human security review accepts it. Member 3 records every significant crypto change with the repository AI-history workflow. The canonical process is `docs/DEVELOPMENT_WORKFLOW.md` and `docs/ai/README.md`. This note states how that process applies to Gateway cryptography. It does not replace those documents.

## Required sequence

For every significant crypto task the record follows this order:

```text
start
record important interactions
agent completes implementation
tests and static checks
output
human security review
accepted, modified, or rejected
revision when the decision is modified
verification
```

Acceptance is not completion. Final verification is a separate human confirmation after acceptance. Automated checks do not replace human review. An agent's own review does not replace human review.

A Modified decision records the requested corrections, then a revision, then another human review. A Rejected decision closes the task.

## Crypto changes that use this workflow

These changes are recorded even when one history file covers more than one of them:

- Evaluate ML-KEM Python libraries
- Implement ML-KEM wrapper
- Implement HKDF wrapper
- Implement secure session manager
- Implement AES-GCM wrapper
- Implement secure envelope
- Implement secure Cloud transport
- Implement crypto failure injection

The maintained-library decision is `docs/architecture/ml-kem-library-decision.md`. Gateway code calls ML-KEM, HKDF, and AES-GCM through that library. This repository does not implement those primitives.

## Records stay free of secrets

A crypto history record stores the prompt, the summary, the paths, and sanitized check results. It does not store private keys, ML-KEM shared secrets, session keys, credentials, passwords, tokens, or `.env` contents.

## Continuous evaluation

The course requires continuous manual evaluation of AI-generated code. A solution that passes tests is not, by that fact, accepted. The human review looks at correctness, security, and the frozen protocol.

## Completed records

Each area below already has a Complete history record:

| Area | Record |
|---|---|
| Evaluate ML-KEM Python libraries | `docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md` |
| Implement ML-KEM wrapper | `docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md` |
| Implement HKDF wrapper | `docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md` |
| Implement secure session manager | `docs/ai/history/0011-gateway-secure-session-establishment.md` |
| Implement AES-GCM wrapper | `docs/ai/history/0019-gateway-aes-gcm-nonce-and-aad.md` |
| Implement secure envelope | `docs/ai/history/0025-integrate-pr-10-secureenvelope-on-current-develop.md` |
| Implement secure Cloud transport | `docs/ai/history/0047-gateway-secure-measurement-transport.md` |
| Implement crypto failure injection | `docs/ai/history/0049-gateway-crypto-failure-injection.md` |
