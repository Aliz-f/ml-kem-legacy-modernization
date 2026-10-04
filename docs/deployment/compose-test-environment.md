# Docker Compose test-environment runbook

This runbook implements Member 5 tasks M5-57 and M5-58. Run every command
from the repository root. Docker Compose is the project's documented test
environment: it starts the Legacy Device, Edge Gateway, and Cloud Service with
SQLite storage in the named `cloud-data` volume.

## Build and start

First validate the resolved configuration and build the images:

```bash
docker compose config --quiet
docker compose build
```

Start the Classical Baseline Mode stack and wait for the Gateway and Cloud
health checks:

```bash
SECURITY_MODE=classical docker compose up --build --wait
```

For Modernized Mode, stop the previous stack and start it with the frozen
fail-closed setting:

```bash
docker compose down
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait
```

The Legacy Device has no inbound port. Compose uses internal service DNS:
`legacy-device` sends to `http://edge-gateway:8000`, and the Gateway sends to
`http://cloud-service:9000`.

## Verify the running stack

The default loopback ports are 8000 for the Gateway and 9000 for the Cloud.
Override them with `GATEWAY_HOST_PORT` and `CLOUD_HOST_PORT` if those ports are
already in use.

```bash
docker compose ps
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/health
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/ready
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/health
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/ready
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/api/v1/measurements
```

Inspect only operational logs; do not enable logging of request bodies,
configuration values, or cryptographic material:

```bash
docker compose logs --follow legacy-device edge-gateway cloud-service
```

In Modernized Mode, an empty active-session count alone does not make either
service unready: sessions are established lazily. Secure failures remain
fail-closed and never cause a baseline request automatically.

## Stop and reset

Stop the stack while retaining the demonstration database:

```bash
docker compose down
```

For a clean test run, remove the named SQLite volume as well. This permanently
removes the locally stored measurements in that volume:

```bash
docker compose down --volumes --remove-orphans
```

Use the clean reset before a deterministic integration or demonstration run;
do not reuse a prior demonstration database for automated assertions. The
volume contains accepted measurements only: ML-KEM private keys, shared
secrets, session keys, and session state remain process-local and are never
stored there.
