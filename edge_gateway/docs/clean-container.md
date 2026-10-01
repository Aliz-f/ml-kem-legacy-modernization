# Clean-container crypto test

Member 3 task M3-62 runs one secure measurement from a clean image. The image
builds Gateway and Cloud from the frozen lock, starts Cloud, establishes one
ML-KEM session, and stores the measurement. It does not use a developer
virtualenv, pytest, or a mounted source tree.

`edge_gateway/docker/clean-container.Dockerfile` uses Python 3.12 on Debian
bookworm. Its install command is:

```text
uv sync --frozen --package edge-gateway --package cloud-service --no-dev --no-editable
```

Build and run it from the repository root:

```bash
docker build -f edge_gateway/docker/clean-container.Dockerfile -t gateway-clean-container .
docker run --rm gateway-clean-container
```

The expected output is `clean-container-ok`.

The check exercises Cloud's production secure-ingest route directly. Gateway's
service image remains `edge_gateway/Dockerfile`; this verification image is
separate from normal service and Compose configuration. The check does not
print keys or shared secrets.
