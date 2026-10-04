# Presentation demo scenarios

This M5-87 through M5-91 guide makes the repository's four demonstration
scenarios repeatable. Run commands from the repository root. Before each
scenario, reset prior state:

```bash
docker compose down --volumes --remove-orphans
```

Use the default loopback ports unless `GATEWAY_HOST_PORT` or
`CLOUD_HOST_PORT` is set.

## 1. Classical baseline

```bash
SECURITY_MODE=classical docker compose up --build --wait
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/api/v1/measurements
docker compose logs --no-color legacy-device edge-gateway cloud-service
```

Show that the Legacy Device sends, the Gateway forwards through the baseline
endpoint, and the Cloud query returns a stored measurement.

## 2. Modernized mode

```bash
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/api/v1/measurements
```

Explain from the frozen contract that the Gateway obtains versioned
ML-KEM-768 public-key metadata, creates a session, derives one 32-byte key
with HKDF-SHA-256 (`salt=None` and the fixed project info string), and sends
an AES-256-GCM `SecureEnvelope`. The same Legacy HTTP/JSON interface remains
unchanged. Use Gateway and Cloud metrics/logs to show session establishment
and message delivery; do not display secret values.

## 3. Secure-message tampering

```bash
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed \
  GATEWAY_FAILURE_MODE=corrupt_ciphertext GATEWAY_FAILURE_RATE=1 \
  docker compose up --build --wait
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
docker compose logs --no-color edge-gateway cloud-service
```

Show the Cloud decryption-failure metric and confirm the query has no new
logical row. This is a fail-closed secure-message rejection: it does not call
the baseline endpoint.

## 4. Cloud storage failure

```bash
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed \
  CLOUD_FAILURE_MODE=storage_failure CLOUD_FAILURE_RATE=1 \
  docker compose up --build --wait
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
docker compose logs --no-color legacy-device edge-gateway cloud-service
```

Show the visible bounded failure and retry metrics. Reset the stack after the
scenario; injected faults are for demonstration only and are disabled by
default.

## Rehearsal checklist

- Use a fresh volume for each scenario and wait for health checks.
- Verify Gateway and Cloud `/ready` before presenting messages.
- Query the Cloud after every scenario and use metrics/logs only as safe
  operational evidence.
- Never show private keys, shared secrets, session keys, `.env` contents, or
  raw cryptographic payloads.
