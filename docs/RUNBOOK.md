# System runbook

This M5-92 runbook links the operational procedures for the three-service
test environment. For complete build, start, verification, shutdown, and
volume-reset commands, use the [Compose test-environment runbook](deployment/compose-test-environment.md).
For presentation-oriented deterministic examples, use the [demo scenarios](presentation/demo-scenarios.md).

## Modes and failure injection

- Baseline Mode is explicit: `SECURITY_MODE=classical`.
- Modernized Mode is explicit: `SECURITY_MODE=mlkem` and
  `PQC_FAILURE_POLICY=fail_closed`.
- Use only service-scoped root variables from `.env.example` for controlled
  failure injection: `LEGACY_FAILURE_*`, `GATEWAY_FAILURE_*`, and
  `CLOUD_FAILURE_*`. Defaults are disabled.

Health, readiness, logs, metrics, Cloud query, clean SQLite reset, and tests
are documented in the linked runbooks. Run the complete repository check set
before review:

```bash
uv sync --frozen
uv run ruff check .
uv run pytest
uv run ai-history check
```

## Frozen operational rules

- Modernized Mode never performs runtime automatic plaintext fallback.
- `409 SESSION_INVALID` and `409 SESSION_EXPIRED` trigger at most one secure
  session-recovery attempt. The logical request ID is preserved, but the
  replacement session requires a rebuilt envelope.
- An ordinary ambiguous-response retry resends the same already-built
  `SecureEnvelope`: identical request ID, session ID, nonce, ciphertext, and
  AAD.
- Cloud business idempotency prevents duplicate logical rows using
  `(device_id, sequence_number)`; it is not cryptographic replay protection.
  Protocol version 1 has no dedicated cryptographic anti-replay counter/window.
- Cloud restart creates a fresh ephemeral ML-KEM key pair and loses sessions;
  the Gateway recovers through the frozen `409 SESSION_INVALID` flow.

Do not put secrets, private keys, session keys, shared secrets, or `.env`
contents in logs, demo output, or AI-history records.
