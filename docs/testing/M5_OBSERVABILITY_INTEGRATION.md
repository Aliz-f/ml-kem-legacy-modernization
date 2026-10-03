# M5 observability integration evidence

This document is the reproducible M5-47 through M5-51 trace demonstration.
It uses production Gateway and Cloud applications on isolated loopback ports;
no protocol stubs or plaintext fallback are used.

Run:

```bash
uv run pytest tests/integration/test_observability_integration.py
```

The test sends a Legacy measurement with `sequence_number=42` in each explicit
mode and proves this trace:

```text
Legacy sequence=42
        |
Gateway request_id=req-<generated>
        |
classical: X-Request-ID          mlkem: SecureEnvelope.request_id + AAD
        |                                      |
Cloud log request_id=req-<same> -> record_id=rec-<generated>
```

For Modernized Mode, the test captures the live SecureEnvelope at the Cloud
boundary and verifies that its `request_id` is the same generated Gateway ID.
The envelope has exactly the six frozen fields, so the authenticated AAD
binding remains exercised by the real Cloud decrypt path.

The same test queries both `/metrics` endpoints and confirms bounded service,
delivery, and mode-specific Cloud counters. It also rejects correlation IDs and
storage identifiers as metric text, because they must remain log correlation
data rather than high-cardinality labels.

For M5-50, the Modernized Mode run captures the actual ML-KEM shared secret
and its derived session key in test memory only, then verifies that neither
value nor an encrypted-payload marker occurs in captured Gateway or Cloud
logs. It does not print or persist those runtime values.

`tests/integration/test_gateway_compose_e2e.py` additionally queries both
metrics endpoints from the Docker Compose test environment in Classical and
Modernized modes.
