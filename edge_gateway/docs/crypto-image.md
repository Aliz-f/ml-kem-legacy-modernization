# Gateway crypto image install

Member 3 task M3-61 checks that the selected `cryptography` package installs
inside a Gateway image without compiling native extensions.

The service image is still Member 2's `edge_gateway/Dockerfile`. Compose
services are still empty. This document covers only the crypto install.

## Verification image

`edge_gateway/docker/crypto-image.Dockerfile` uses Python 3.12 on Debian
bookworm. Bookworm provides glibc, so the frozen lock can install manylinux
wheels. The image has no compiler. The install command is:

```text
uv sync --frozen --package edge-gateway --no-dev
```

A missing wheel fails that build. The image does not listen on port 8000 and
does not start a Cloud handshake.

Build and run it from the repository root:

```bash
docker build -f edge_gateway/docker/crypto-image.Dockerfile -t gateway-crypto-check .
docker run --rm gateway-crypto-check
```

The expected output is `crypto-install-ok`. The check generates an ML-KEM-768
keypair, encapsulates with the Gateway wrapper, decapsulates with the installed
library, derives the session key with HKDF-SHA-256, and round-trips AES-256-GCM.
It does not print keys or shared secrets.

## Locked Linux wheels

The same frozen install resolves binary wheels for the two architectures a
Gateway image is expected to use:

```text
aarch64-unknown-linux-gnu
x86_64-unknown-linux-gnu
```

`cryptography` 50.0.1, `cffi`, and `pydantic-core` are the native packages in
that install. Their selected artifacts are manylinux wheels. The sdist remains
in the lock as the upstream source archive and is not the install artifact for
these platforms.
