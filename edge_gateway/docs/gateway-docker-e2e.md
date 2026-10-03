# Gateway Docker and container regression

PR12 covers Member 2 tasks M2-49 through M2-52. The implementation keeps the
Legacy HTTP contract unchanged in both security modes.

## M2-49 — Dockerize Gateway

`edge_gateway/Dockerfile` builds the Gateway with Python 3.12 and the pinned
`uv` release from the repository lock file. The image installs only production
dependencies, runs as user `10001`, exposes port 8000, and starts the existing
`edge-gateway` console entry point without hot reload. Its health check calls
`GET /health`. Uvicorn receives Docker's `SIGTERM`, runs the application
lifespan cleanup, and exits normally.

Build the image from the repository root:

```bash
docker build -f edge_gateway/Dockerfile -t edge-gateway .
```

## M2-50 — Compose integration

The root `docker-compose.yml` builds Gateway and Cloud on the default Compose
network. Gateway reaches Cloud through Docker DNS at
`http://cloud-service:9000` and waits for Cloud's health check before starting.
Compose maps the root `GATEWAY_FAILURE_*` and `CLOUD_FAILURE_*` variables into
each process's generic `FAILURE_*` settings. `SECURITY_MODE` selects
`classical` or `mlkem`; secure mode stays fail closed.

Host ports bind to loopback and can be changed with `GATEWAY_HOST_PORT` and
`CLOUD_HOST_PORT`. Cloud stores its SQLite database in the `cloud-data` named
volume.

Member 5 owns the repository-wide Compose environment, and Member 1 owns the
Legacy image. No `legacy_system/Dockerfile` exists in the current repository,
so this change does not invent one under Member 2 ownership. Once that image is
available, its Compose service must use `GATEWAY_URL=http://edge-gateway:8000`.

## M2-51 — Baseline container test

`tests/integration/test_gateway_compose_e2e.py` starts the real Gateway and
Cloud images with `SECURITY_MODE=classical`. It sends the frozen five-field
payload using Member 1's production `GatewayClient`, checks the Legacy-facing
`202`, queries Cloud, and verifies the original values were persisted. It also
checks that the baseline request counter increments while the secure counter
does not.

## M2-52 — Modernized container regression

The same test repeats with `SECURITY_MODE=mlkem`, the same client, route, and
payload. It verifies Cloud persistence through the secure request path and
confirms the baseline counter remains zero. Both cases stop Gateway with
Docker, verify clean application shutdown, and remove their containers and
volumes.

Run the regression from the repository root with a working Docker daemon:

```bash
uv run pytest tests/test_gateway_docker_assets.py \
  tests/integration/test_gateway_compose_e2e.py -q
```

These tests prove the Member 2 boundary through two real service containers.
The roadmap's literal three-container `docker compose up` milestone still
depends on Member 1 supplying the Legacy image and Member 5 adding that service
to the shared Compose topology.
