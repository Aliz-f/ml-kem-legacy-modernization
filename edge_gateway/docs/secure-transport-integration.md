# Member 2 secure-transport integration — M2-26 through M2-28

These tasks connect the Gateway application to Member 3's existing secure
transport. They do not implement ML-KEM, HKDF, AES-GCM, sessions, envelopes, or
cryptographic retry behavior.

## M2-26 — Mode-independent application interface

`MeasurementProcessor` now depends on the `CloudTransport` protocol in
`edge_gateway.transport`. Its `send` call contains the normalized measurement
fields and a separate `request_id`; it contains no mode, session, nonce, public
key, ciphertext, or cryptographic operation.

`BaselineCloudError` and `SecureTransportError` both inherit the common
`CloudDeliveryError`. The processor therefore maps delivery failures to the
Legacy-facing `503 CLOUD_UNAVAILABLE` without importing either concrete
transport. `CloudDispatch` remains the adapter that supplies `gateway_id` and
delegates to the configured transport. Member 3's secure implementation remains
isolated under `edge_gateway.crypto`.

## M2-27 — Explicit security-mode dispatch

The existing dispatch behavior was audited and retained:

| Gateway setting | Selected path |
|---|---|
| `SECURITY_MODE=classical` | `BaselineCloudClient` → `POST /api/v1/baseline/measurements`, with `X-Request-ID` |
| `SECURITY_MODE=mlkem` | `SecureTransport` → ML-KEM session and AES-GCM envelope → `POST /api/v1/secure/measurements` |

Configuration accepts only `classical` or `mlkem`, and protocol v1 accepts only
`PQC_FAILURE_POLICY=fail_closed`. The application constructs the baseline client
only in classical mode and the secure transport only in ML-KEM mode. A secure
handshake, encryption, session, or Cloud rejection is returned as failure; it
never causes a baseline call or changes the configured mode. Session recovery
stays inside `SecureTransport`: `SESSION_INVALID` or `SESSION_EXPIRED` permits
one replacement session for the same logical request.

## M2-28 — Unchanged Legacy contract

The Legacy Device always sends the same five-field JSON body to:

```http
POST /api/v1/measurements
```

It does not send or receive `SECURITY_MODE`, ML-KEM data, session identifiers,
nonces, Cloud keys, or secure envelopes. The Gateway returns `202` only after
the selected Cloud path confirms persistence. Validation and sequence errors
retain the same status and body in both modes.

The live compatibility evidence uses the same `legacy_system.GatewayClient` and
payload in classical and ML-KEM runs. Each run starts the production Gateway and
Cloud HTTP applications, stores the same canonical values in disposable SQLite,
and confirms that ML-KEM mode creates a secure session while classical mode does
not. The separate unavailable-Cloud suite confirms identical Legacy request,
response, and retry contracts in both modes and verifies that Legacy source code
contains no Gateway cryptographic concepts.

## Verification

```bash
uv run pytest edge_gateway/tests/test_gateway_transport_interface.py \
  edge_gateway/tests/test_dispatch.py \
  tests/integration/test_legacy_compatibility.py \
  cloud_service/tests/test_full_path_integration.py -q
```

The first test module checks the application abstraction. Dispatch tests check
exclusive mode selection and fail-closed behavior. The two integration modules
check the unchanged Legacy boundary and successful persistence through both
Cloud modes. No protocol field, endpoint, status code, KDF parameter, nonce,
AAD, retry, or session rule changes in these tasks.
