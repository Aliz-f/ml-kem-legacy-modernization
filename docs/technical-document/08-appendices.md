# Chapter 8 — Appendices (Configurations, Runbooks and Key Source Code)

## Appendix A: Complete Deployment Configurations

### A.1 Docker Compose Multi-Container Deployment Specification
The orchestration configuration coordinates the complete three-tier IoT architecture (`legacy-device`, `edge-gateway`, `cloud-service`) alongside an optional local monitoring dashboard. It enforces health check dependencies, non-root user isolation, service-scoped failure injection mappings, and persistent SQLite storage.

```yaml
services:
  cloud-service:
    build:
      context: .
      dockerfile: cloud_service/Dockerfile
    environment:
      HOST: 0.0.0.0
      PORT: 9000
      CLOUD_ID: ${CLOUD_ID:-cloud-001}
      DATABASE_URL: ${DATABASE_URL:-sqlite:////data/cloud.db}
      SECURITY_MODE: ${SECURITY_MODE:-classical}
      SESSION_TTL_SECONDS: ${SESSION_TTL_SECONDS:-300}
      FAILURE_MODE: ${CLOUD_FAILURE_MODE:-none}
      FAILURE_RATE: ${CLOUD_FAILURE_RATE:-0.0}
      FAILURE_SEED: ${CLOUD_FAILURE_SEED-}
      FAILURE_DELAY_SECONDS: ${CLOUD_FAILURE_DELAY_SECONDS:-2}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    ports:
      - "127.0.0.1:${CLOUD_HOST_PORT:-9000}:9000"
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "from urllib.request import urlopen; urlopen('http://127.0.0.1:9000/health', timeout=3).close()"
      interval: 30s
      timeout: 5s
      start_period: 15s
      retries: 3
    volumes:
      - cloud-data:/data

  edge-gateway:
    build:
      context: .
      dockerfile: edge_gateway/Dockerfile
    depends_on:
      cloud-service:
        condition: service_healthy
    environment:
      HOST: 0.0.0.0
      PORT: 8000
      GATEWAY_ID: ${GATEWAY_ID:-gateway-001}
      CLOUD_URL: ${CLOUD_URL:-http://cloud-service:9000}
      CLOUD_TIMEOUT_SECONDS: ${CLOUD_TIMEOUT_SECONDS:-3}
      CLOUD_MAX_RETRIES: ${CLOUD_MAX_RETRIES:-2}
      SECURITY_MODE: ${SECURITY_MODE:-classical}
      SESSION_TTL_SECONDS: ${SESSION_TTL_SECONDS:-300}
      PQC_FAILURE_POLICY: fail_closed
      FAILURE_MODE: ${GATEWAY_FAILURE_MODE:-none}
      FAILURE_RATE: ${GATEWAY_FAILURE_RATE:-0.0}
      FAILURE_SEED: ${GATEWAY_FAILURE_SEED-}
      FAILURE_DELAY_SECONDS: ${GATEWAY_FAILURE_DELAY_SECONDS:-2}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    ports:
      - "127.0.0.1:${GATEWAY_HOST_PORT:-8000}:8000"
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=3).close()"
      interval: 30s
      timeout: 5s
      start_period: 15s
      retries: 3

  dashboard:
    build:
      context: .
      dockerfile: dashboard/Dockerfile
    depends_on:
      - cloud-service
      - edge-gateway
      - legacy-device
    environment:
      DASHBOARD_PORT: 8080
    ports:
      - "127.0.0.1:${DASHBOARD_HOST_PORT:-8080}:8080"
    volumes:
      # Local dashboard only: runtime overrides recreate an explicitly selected service.
      - /var/run/docker.sock:/var/run/docker.sock

  legacy-device:
    build:
      context: .
      dockerfile: legacy_system/Dockerfile
    depends_on:
      edge-gateway:
        condition: service_healthy
    environment:
      DEVICE_ID: ${DEVICE_ID:-sensor-001}
      GATEWAY_URL: ${GATEWAY_URL:-http://edge-gateway:8000}
      SEND_INTERVAL_SECONDS: ${SEND_INTERVAL_SECONDS:-5}
      REQUEST_TIMEOUT_SECONDS: ${REQUEST_TIMEOUT_SECONDS:-3}
      MAX_RETRIES: ${MAX_RETRIES:-2}
      FAILURE_MODE: ${LEGACY_FAILURE_MODE:-none}
      FAILURE_RATE: ${LEGACY_FAILURE_RATE:-0.0}
      FAILURE_SEED: ${LEGACY_FAILURE_SEED-}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}

volumes:
  cloud-data:
```

### A.2 Multi-Stage Container Image Specifications

#### A.2.1 Legacy Device Container Image
```dockerfile
# Build from the repository root: docker build -f legacy_system/Dockerfile .
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock README.md ./
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY legacy_system/src legacy_system/src

RUN uv sync --frozen --package legacy-system --no-dev --no-editable

USER 10001:10001
STOPSIGNAL SIGTERM
CMD ["python", "-m", "legacy_system.main"]
```

#### A.2.2 Edge Gateway Container Image
```dockerfile
# Build from the repository root: docker build -f edge_gateway/Dockerfile .
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000

COPY pyproject.toml uv.lock README.md ./
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY edge_gateway/src edge_gateway/src

RUN uv sync --frozen --package edge-gateway --no-dev --no-editable

USER 10001:10001
EXPOSE 8000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=3).close()"
CMD ["edge-gateway"]
```

#### A.2.3 Cloud Service Container Image
```dockerfile
# Build from the repository root: docker build -f cloud_service/Dockerfile .
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=9000 \
    DATABASE_URL=sqlite:////data/cloud.db

COPY pyproject.toml uv.lock README.md ./
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY cloud_service/src cloud_service/src

RUN uv sync --frozen --package cloud-service --no-dev --no-editable \
    && mkdir -p /data \
    && chown 10001:10001 /data

USER 10001:10001
EXPOSE 9000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:9000/ready', timeout=3).close()"
CMD ["cloud-service"]
```

### A.3 Environment Variable Configuration Template
```ini
# Shared Gateway/Cloud protocol defaults
# Allowed: classical, mlkem. Use mlkem only with PQC_FAILURE_POLICY=fail_closed.
SECURITY_MODE=classical
# Frozen protocol v1 value: 300 only.
SESSION_TTL_SECONDS=300

# Legacy Device
DEVICE_ID=sensor-001
GATEWAY_URL=http://edge-gateway:8000
SEND_INTERVAL_SECONDS=5
REQUEST_TIMEOUT_SECONDS=3
MAX_RETRIES=2
LEGACY_FAILURE_MODE=none
LEGACY_FAILURE_RATE=0.0
LEGACY_FAILURE_SEED=

# Edge Gateway
GATEWAY_ID=gateway-001
CLOUD_URL=http://cloud-service:9000
CLOUD_TIMEOUT_SECONDS=3
CLOUD_MAX_RETRIES=2
PQC_FAILURE_POLICY=fail_closed
GATEWAY_FAILURE_MODE=none
GATEWAY_FAILURE_RATE=0.0
GATEWAY_FAILURE_SEED=
GATEWAY_FAILURE_DELAY_SECONDS=2

# Cloud Service
CLOUD_ID=cloud-001
DATABASE_URL=sqlite:////data/cloud.db
GATEWAY_HOST_PORT=8000
CLOUD_HOST_PORT=9000
DASHBOARD_HOST_PORT=8080
CLOUD_FAILURE_MODE=none
CLOUD_FAILURE_RATE=0.0
CLOUD_FAILURE_SEED=
CLOUD_FAILURE_DELAY_SECONDS=2

LOG_LEVEL=INFO
```

## Appendix B: Complete CI/CD Pipeline Definitions

### B.1 Repository Quality and Multi-Stage CI Pipeline Workflow
```yaml
name: Repository quality

on: [push, pull_request]

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - run: uv sync --frozen
      - run: uv run ruff check .
      - name: Verify AI-history CLI compatibility
        run: |
          uv run ai-history --help
          uv run ai-history status
          uv run ai-history list
          uv run ai-history check

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - run: uv sync --frozen
      - name: Run unit and repository tests
        run: >-
          uv run pytest legacy_system/tests edge_gateway/tests cloud_service/tests
          tests/ai_history tests/test_*.py
      - name: Run protocol contract tests
        run: >-
          uv run pytest
          edge_gateway/tests/test_gateway_models.py
          edge_gateway/tests/test_gateway_canonical_model.py
          edge_gateway/tests/test_gateway_correlation.py
          edge_gateway/tests/test_public_key_client.py
          edge_gateway/tests/test_session.py
          edge_gateway/tests/test_secure_envelope.py
          edge_gateway/tests/test_aad.py
          edge_gateway/tests/test_kdf.py
          cloud_service/tests/test_gateway_cloud_baseline_contract.py
          cloud_service/tests/test_cloud_public_key.py
          cloud_service/tests/test_cloud_session_api.py
          cloud_service/tests/test_cloud_envelope.py
          cloud_service/tests/test_cloud_kdf.py
      - name: Run Gateway crypto checks
        run: >-
          uv run pytest
          edge_gateway/tests/test_mlkem.py
          edge_gateway/tests/test_kdf.py
          edge_gateway/tests/test_symmetric.py
          edge_gateway/tests/test_secure_envelope.py
          edge_gateway/tests/test_crypto_review_checklist.py
          edge_gateway/tests/test_transport_trust.py
          edge_gateway/tests/test_security_logging.py
          edge_gateway/tests/test_secure_transport.py
          tests/integration/test_secure_message_tamper.py
          tests/integration/test_gateway_cloud_secure.py

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - run: uv sync --frozen
      - name: Run all integration tests
        run: uv run pytest tests/integration
      - name: Run observability and metrics sanity regressions
        run: >-
          uv run pytest
          tests/integration/test_observability_integration.py
          tests/integration/test_metrics_sanity.py
      - name: Run Cloud unit and cross-component checks
        run: >-
          uv run pytest
          cloud_service/tests
          tests/integration/test_gateway_cloud_secure.py
      - name: Run cross-component integration tests
        run: >-
          uv run pytest
          tests/integration/test_legacy_gateway.py
          tests/integration/test_gateway_cloud_baseline.py
          tests/integration/test_mlkem_session_orchestration.py
          tests/integration/test_gateway_cloud_secure_session.py
          tests/integration/test_gateway_cloud_secure.py

  secure-e2e:
    needs: [quality, unit-tests, integration-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - run: uv sync --frozen
      - name: Run full end-to-end tests
        run: >-
          uv run pytest
          tests/integration/test_end_to_end.py
          tests/integration/test_modernized_end_to_end.py
          tests/integration/test_legacy_mode_success_compatibility.py

  docker-build:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Legacy Device image
        run: docker build --file legacy_system/Dockerfile --tag course-legacy-device .
      - name: Build Edge Gateway image
        run: docker build --file edge_gateway/Dockerfile --tag course-edge-gateway .
      - name: Build Cloud Service image
        run: docker build --file cloud_service/Dockerfile --tag course-cloud-service .

  clean-environment:
    needs: [secure-e2e, docker-build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - name: Install from the committed lockfile
        run: uv sync --frozen
      - name: Validate the Compose configuration
        run: docker compose config --quiet
      - name: Run Compose recovery regression
        run: uv run pytest tests/integration/test_gateway_compose_e2e.py
```

## Appendix C: System Operational Runbooks

### C.1 Operational Lifecycle and Verification Commands
```bash
# 1. Clean build and configuration validation
docker compose config --quiet
docker compose build

# 2. Start Classical Baseline Stack
SECURITY_MODE=classical docker compose up --build --wait

# 3. Start Modernized ML-KEM Stack (Fail-Closed)
docker compose down
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait

# 4. Probe Health and Readiness
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:8000/ready
curl --fail http://127.0.0.1:9000/health
curl --fail http://127.0.0.1:9000/ready

# 5. Query Metrics
curl --fail http://127.0.0.1:8000/metrics
curl --fail http://127.0.0.1:9000/metrics

# 6. Query Stored Measurements from Cloud
curl --fail http://127.0.0.1:9000/api/v1/measurements

# 7. Clean Teardown and SQLite Volume Reset
docker compose down --volumes --remove-orphans
```

## Appendix D: Core Cryptographic and Protocol Source Code

### D.1 Edge Gateway ML-KEM-768 Encapsulation Module
```python
"""ML-KEM-768 encapsulation for the Gateway.

The Cloud public key is raw FIPS 203 bytes. Base64URL decoding belongs to
the protocol client, not this wrapper.
"""

from __future__ import annotations

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PublicKey

PUBLIC_KEY_LENGTH = 1184
CIPHERTEXT_LENGTH = 1088
SHARED_SECRET_LENGTH = 32


class MlKemError(Exception):
    """The Gateway could not encapsulate to the supplied public key."""


def validate_public_key(public_key: bytes) -> None:
    """Accept only a raw ML-KEM-768 public key. Does not encapsulate or log it."""
    if not isinstance(public_key, bytes) or len(public_key) != PUBLIC_KEY_LENGTH:
        raise MlKemError("ML-KEM-768 public key must be 1184 bytes.")
    try:
        MLKEM768PublicKey.from_public_bytes(public_key)
    except (ValueError, UnsupportedAlgorithm) as exc:
        raise MlKemError("ML-KEM-768 public key was rejected.") from exc


def encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
    """Return `(ciphertext, shared_secret)` for an ML-KEM-768 public key.

    The shared secret stays with the caller. This function does not log it.
    """
    validate_public_key(public_key)
    try:
        key = MLKEM768PublicKey.from_public_bytes(public_key)
        shared_secret, ciphertext = key.encapsulate()
    except (ValueError, UnsupportedAlgorithm) as exc:
        raise MlKemError("ML-KEM-768 encapsulation failed.") from exc
    if (
        len(shared_secret) != SHARED_SECRET_LENGTH
        or len(ciphertext) != CIPHERTEXT_LENGTH
    ):
        raise MlKemError("ML-KEM-768 encapsulation returned unexpected lengths.")
    return ciphertext, shared_secret
```

### D.2 HKDF-SHA-256 Session Key Derivation Module
```python
"""Session-key derivation for protocol version 1.

Both Gateway and Cloud must call this contract. `salt=None` is the
`cryptography` HKDF default: RFC 5869 expands a missing salt to HashLen
zero bytes.
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SESSION_KEY_LENGTH = 32
SESSION_KEY_INFO = b"ml-kem-project:v1:gateway-cloud-session"
SHARED_SECRET_LENGTH = 32


class KdfError(Exception):
    """The shared secret cannot be used for session-key derivation."""


def derive_session_key(shared_secret: bytes) -> bytes:
    """Derive the 32-byte AES-256-GCM session key. Does not log key material."""
    if not isinstance(shared_secret, bytes) or len(shared_secret) != SHARED_SECRET_LENGTH:
        raise KdfError("ML-KEM shared secret must be 32 bytes.")
    return HKDF(
        algorithm=hashes.SHA256(),
        length=SESSION_KEY_LENGTH,
        salt=None,
        info=SESSION_KEY_INFO,
    ).derive(shared_secret)
```

### D.3 Edge Gateway AES-256-GCM Authenticated Encryption Module
```python
"""AES-256-GCM for protocol version 1.

`generate_nonce()` is only for a new logical encryption. An ordinary transport
retry resends the already-built envelope: the same nonce, ciphertext, and AAD
under the same session key. This module does not build that envelope.
"""

from __future__ import annotations

import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LENGTH = 12
KEY_LENGTH = 32


class AeadError(Exception):
    """AES-256-GCM could not encrypt or authenticate the message."""


def generate_nonce() -> bytes:
    """Return a fresh 12-byte nonce from the operating-system CSPRNG."""
    return secrets.token_bytes(NONCE_LENGTH)


def encrypt(key: bytes, nonce: bytes, plaintext: bytes, associated_data: bytes) -> bytes:
    """Encrypt and authenticate. The result includes the GCM authentication tag."""
    key_bytes = _require_key(key)
    nonce_bytes = _require_nonce(nonce)
    plaintext_bytes = _require_bytes(plaintext, "Plaintext")
    aad_bytes = _require_bytes(associated_data, "Associated data")
    try:
        return AESGCM(key_bytes).encrypt(nonce_bytes, plaintext_bytes, aad_bytes)
    except ValueError as exc:
        raise AeadError("AES-256-GCM encryption failed.") from exc


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes) -> bytes:
    """Authenticate and decrypt. A failure does not return plaintext."""
    key_bytes = _require_key(key)
    nonce_bytes = _require_nonce(nonce)
    ciphertext_bytes = _require_bytes(ciphertext, "Ciphertext")
    aad_bytes = _require_bytes(associated_data, "Associated data")
    try:
        return AESGCM(key_bytes).decrypt(nonce_bytes, ciphertext_bytes, aad_bytes)
    except (InvalidTag, ValueError) as exc:
        raise AeadError("AES-256-GCM authentication failed.") from exc


def _require_key(key: object) -> bytes:
    if not isinstance(key, (bytes, bytearray)) or len(key) != KEY_LENGTH:
        raise AeadError("AES-256-GCM key must be 32 bytes.")
    return bytes(key)


def _require_nonce(nonce: object) -> bytes:
    if not isinstance(nonce, (bytes, bytearray)) or len(nonce) != NONCE_LENGTH:
        raise AeadError("AES-256-GCM nonce must be 12 bytes.")
    return bytes(nonce)


def _require_bytes(value: object, label: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise AeadError(f"{label} must be bytes.")
    return bytes(value)
```

### D.4 Canonical 4-Field Associated Data Builder
```python
"""Four-field AES-GCM associated data for protocol version 1.

Gateway and Cloud must each produce these bytes. The object is exactly
`protocol_version`, `gateway_id`, `session_id`, and `request_id`.
"""

from __future__ import annotations

import json

PROTOCOL_VERSION = "1"


class AadError(Exception):
    """The AAD fields are not the frozen four-field object."""


def build_aad(
    *,
    protocol_version: str,
    gateway_id: str,
    session_id: str,
    request_id: str,
) -> bytes:
    """Return the canonical UTF-8 AAD object. Does not log the fields."""
    if not isinstance(protocol_version, str) or protocol_version != PROTOCOL_VERSION:
        raise AadError('protocol_version must be "1".')
    _require_id(gateway_id, "gateway_id")
    _require_id(session_id, "session_id")
    _require_id(request_id, "request_id")
    payload = {
        "protocol_version": protocol_version,
        "gateway_id": gateway_id,
        "session_id": session_id,
        "request_id": request_id,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _require_id(value: object, name: str) -> None:
    if not isinstance(value, str) or value == "" or value != value.strip():
        raise AadError(f"{name} must be a non-empty string.")
```

### D.5 Edge Gateway Monotonic Sequence Tracker
```python
"""In-memory Legacy sequence policy, independent of downstream delivery."""

import logging
from threading import Lock

from edge_gateway.application_log import log_application
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.metrics import GatewayMetrics


class SequenceTracker:
    """Track the last valid sequence accepted for each device in one process.

    Share one instance across requests. Restarting loses history. Call only
    after schema/domain validation and before Cloud delivery; accepted state
    is never rolled back for a later delivery failure.

    The lock protects only the local check and commit. Cloud I/O belongs to
    the caller after this method returns and must not hold the sequence lock.
    Instances do not share state across processes or persist it to storage.
    """

    def __init__(self, metrics: GatewayMetrics | None = None) -> None:
        self._metrics = metrics or GatewayMetrics()
        self._last_sequence: dict[str, int] = {}
        self._lock = Lock()

    def check_and_update(self, device_id: str, sequence_number: int) -> None:
        """Atomically accept a validated sequence or raise its frozen 409 error.

        First values (including zero) and higher values are accepted. Gaps are
        logged. Rejections leave the previously accepted state unchanged.
        """
        with self._lock:
            previous = self._last_sequence.get(device_id)
            if previous is not None:
                if sequence_number == previous:
                    self._metrics.increment("duplicate_measurements")
                    self._metrics.increment("measurements_rejected")
                    log_application(
                        "sequence_duplicate_detected", logging.WARNING,
                        device_id=device_id, sequence_number=sequence_number,
                    )
                    raise GatewayError(GatewayErrorCode.DUPLICATE_SEQUENCE)
                if sequence_number < previous:
                    self._metrics.increment("out_of_order_measurements")
                    self._metrics.increment("measurements_rejected")
                    log_application(
                        "sequence_out_of_order_detected", logging.WARNING,
                        device_id=device_id, sequence_number=sequence_number,
                        previous_sequence_number=previous,
                    )
                    raise GatewayError(GatewayErrorCode.OUT_OF_ORDER_SEQUENCE)
            self._last_sequence[device_id] = sequence_number

        if previous is not None and sequence_number > previous + 1:
            self._metrics.increment("sequence_gaps")
            log_application(
                "sequence_gap_detected",
                device_id=device_id,
                sequence_number=sequence_number,
                previous_sequence_number=previous,
            )
```

### D.6 Cloud Service ML-KEM-768 Decapsulation Module
```python
"""ML-KEM-768 key generation and decapsulation using PyCA cryptography.

Only this module depends on the vendor ML-KEM API. Private keys are opaque
handles, never serialized. No input, key or shared secret is logged.
"""

from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

PUBLIC_KEY_LENGTH = 1184
CIPHERTEXT_LENGTH = 1088
SHARED_SECRET_LENGTH = 32


class MlKemError(Exception):
    """Safe error that contains no vendor diagnostics or input material."""


class PrivateKey:
    """Opaque process-local key handle with explicit reference release.

    Closing prevents further use. Python cannot guarantee memory zeroization.
    The default object repr deliberately includes no key fields.
    """

    __slots__ = ("_key",)

    def __init__(self, key: MLKEM768PrivateKey):
        self._key = key

    def close(self) -> None:
        self._key = None


def generate_keypair() -> tuple[bytes, PrivateKey]:
    """Return raw public bytes and an opaque private handle; use library RNG."""
    try:
        key = MLKEM768PrivateKey.generate()
        public_key = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        if not isinstance(public_key, bytes) or len(public_key) != PUBLIC_KEY_LENGTH:
            raise ValueError
    except Exception:
        # Vendor exceptions may contain sensitive diagnostics. Suppress chaining.
        raise MlKemError("ML-KEM-768 key generation failed") from None
    return public_key, PrivateKey(key)


def decapsulate(ciphertext: bytes, private_key: PrivateKey) -> bytes:
    """Return the raw 32-byte secret. Correct-length tampering may not raise."""
    if not isinstance(ciphertext, bytes) or len(ciphertext) != CIPHERTEXT_LENGTH:
        raise MlKemError("ML-KEM-768 ciphertext must be 1088 bytes")
    if not isinstance(private_key, PrivateKey) or private_key._key is None:
        raise MlKemError("ML-KEM-768 private key is unavailable")
    try:
        shared_secret = private_key._key.decapsulate(ciphertext)
        if not isinstance(shared_secret, bytes) or len(shared_secret) != SHARED_SECRET_LENGTH:
            raise ValueError
    except Exception:
        raise MlKemError("ML-KEM-768 decapsulation failed") from None
    return shared_secret
```

### D.7 Cloud Service AEAD Authenticated Decryption Module
```python
"""Authenticated decryption only; no parsing, persistence or plaintext logs."""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_LENGTH = 32
NONCE_LENGTH = 12
TAG_LENGTH = 16


class AeadError(Exception):
    """Safe secure-message rejection without vendor or secret diagnostics."""


def decrypt(key: bytes | bytearray, nonce: bytes | bytearray,
            ciphertext: bytes | bytearray, associated_data: bytes | bytearray) -> bytes:
    """Return plaintext only after library authentication succeeds."""
    if not isinstance(key, (bytes, bytearray)) or len(key) != KEY_LENGTH:
        raise AeadError("AES-256-GCM key must be 32 bytes")
    if not isinstance(nonce, (bytes, bytearray)) or len(nonce) != NONCE_LENGTH:
        raise AeadError("AES-256-GCM nonce must be 12 bytes")
    if not isinstance(ciphertext, (bytes, bytearray)) or len(ciphertext) < TAG_LENGTH:
        raise AeadError("AES-256-GCM ciphertext must include an authentication tag")
    if not isinstance(associated_data, (bytes, bytearray)):
        raise AeadError("Associated data must be bytes")
    try:
        plaintext = AESGCM(bytes(key)).decrypt(bytes(nonce), bytes(ciphertext), bytes(associated_data))
        if not isinstance(plaintext, bytes):
            raise ValueError
    except Exception:
        raise AeadError("AES-256-GCM authentication failed") from None
    return plaintext
```

## Appendix E: Empirical Evaluation and Benchmarking Infrastructure

### E.1 Matched Mode Comparison Benchmarking Harness
```python
"""Run the equivalent classical and ML-KEM M5 evaluation workloads.

Example: ``uv run python scripts/measure_mode_comparison.py --samples 10``.
The output contains actual observations from that invocation; it intentionally
does not ship fixed timing values.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def _load(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(samples: int = 10) -> dict[str, object]:
    """Run one matched workload in each explicit security mode."""
    if type(samples) is not int or not 2 <= samples <= 100:
        raise ValueError("samples must be an integer from 2 to 100")
    baseline = _load("measure_baseline_e2e.py").run(samples)
    modernized = _load("measure_modernized_e2e.py").run(samples)
    baseline_first = baseline["first_message"]
    baseline_steady = baseline["steady_state"]
    modern_first = modernized["first_message"]
    modern_steady = modernized["steady_state"]
    if not all(isinstance(value, dict) for value in (baseline_first, baseline_steady, modern_first, modern_steady)):
        raise RuntimeError("matched workload did not produce first and steady-state observations")
    session = modernized["session_establishment"]
    if not isinstance(session, dict):
        raise RuntimeError("modernized report did not contain session metrics")
    baseline_successful = baseline["successful_messages"]
    modernized_successful = modernized["successful_messages"]
    if not isinstance(baseline_successful, int) or not isinstance(modernized_successful, int):
        raise RuntimeError("workload reports did not contain successful-message counts")
    return {
        "scope": "Matched local Legacy -> Gateway -> Cloud -> SQLite workloads",
        "samples": samples,
        "comparison": {
            "first_message_latency_ms": {
                "classical": baseline_first["legacy_gateway_end_to_end_ms"],
                "mlkem": modern_first["legacy_gateway_end_to_end_ms"],
            },
            "steady_state_latency_ms": {
                "classical": baseline_steady["legacy_gateway_end_to_end_ms"],
                "mlkem": modern_steady["legacy_gateway_end_to_end_ms"],
            },
            "gateway_to_cloud_payload_bytes": {
                "classical": baseline["canonical_payload_bytes"],
                "mlkem": modernized["secure_envelope_bytes"],
            },
            "session_setup": {"classical": "not_applicable", "mlkem": session},
            "successful_messages": {
                "classical": baseline_successful,
                "mlkem": modernized_successful,
            },
            "failed_messages": {
                "classical": samples - baseline_successful,
                "mlkem": samples - modernized_successful,
            },
            "storage_success": {
                "classical": baseline["persisted_rows"],
                "mlkem": modernized["persisted_rows"],
            },
        },
        "baseline_report": baseline,
        "modernized_report": modernized,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=10)
    print(json.dumps(run(parser.parse_args().samples), indent=2, sort_keys=True))
```

## Appendix F: Representative AI Prompt Catalog

This appendix catalogs representative AI prompts and human task specifications across the project lifecycle, documenting the exact scoping, constraints, and oversight mechanisms applied during implementation. In accordance with the project governance framework (Chapter 6), all tasks were initiated with bounded, deterministic prompts and subjected to human review prior to merging.

### F.1 Governance, Tooling, and Architecture Infrastructure

#### Task 0001: AI History and Human Review Infrastructure
- **Agent / Subsystem**: OpenAI Codex / Governance Infrastructure
- **Scope & Context**: Initial repository bootstrapping. Establish the `ai-history` CLI, state journal, and review lifecycle to enforce the 4-phase human-in-the-loop workflow.
- **Human Prompt**:
  > "Implement repository-wide AI-development history, human-review, revision, and final-verification infrastructure without implementing application services. The user requested a Python/uv CLI, canonical instructions for Codex, Claude Code, GitHub Copilot, Cursor, Gemini, and other agents, Markdown task history, machine-readable active-task state, strict validation, automated tests, and a focused CI workflow. The supplied instruction requires complete AI work before human review, preservation of every review/revision round, separate final human verification, no fabricated review/check results, and no secrets or source/diff capture in history."
- **Review Outcome**: Accepted. Verified that the CLI prevents starting concurrent tasks and enforces read-only review states.

#### Task 0002: Workflow Handbook and Dependency Management Policy
- **Agent / Subsystem**: OpenAI Codex / Developer Tooling
- **Scope & Context**: Codify developer workflows, dependency pinning policies, and multi-agent instructions.
- **Human Prompt**:
  > "Implement the development workflow handbook, repository guidelines, and package dependency constraints. Enforce uv sync --frozen for deterministic dependency resolution and forbid pip/requirements.txt workflows."
- **Review Outcome**: Modified across 4 rounds. Human reviewers removed complex external CI tooling, enforced strict lockfile adherence, and added Group-Explanation course compliance checklists.

### F.2 Legacy IoT Device Subsystem (Member 1)

#### Task 0008: Legacy Configuration Validation
- **Agent / Subsystem**: OpenAI Codex / Legacy Device
- **Scope & Context**: Environment variable loading and numerical validation for simulated IoT sensor parameters.
- **Human Prompt**:
  > "Implement configuration loading and validation for legacy_system using pydantic-settings or standard library. Parse DEVICE_ID, GATEWAY_URL, SEND_INTERVAL_SECONDS, REQUEST_TIMEOUT_SECONDS, and MAX_RETRIES. Add validation for all fields and unit tests."
- **Review Outcome**: Modified (2 rounds). Reviewers rejected permissive type coercion and enforced strict positive boundary checks on timing and retry bounds.

#### Task 0012: Legacy Canonical Measurement Schema
- **Agent / Subsystem**: OpenAI Codex / Legacy Device
- **Scope & Context**: Domain dataclass for sensor readings and strict JSON serialization.
- **Human Prompt**:
  > "Implement the Legacy Measurement data model and JSON serialization according to the frozen protocol specification. Ensure field names and types match: device_id (string), sequence_number (integer), timestamp (ISO-8601 UTC string), temperature (float), humidity (float). Write focused unit tests."
- **Review Outcome**: Modified (2 rounds). Reviewers enforced strict ISO-8601 formatting with trailing 'Z' and rejected microsecond variations that could break wire compatibility.

#### Task 0027: Monotonic Sensor Simulation Engine
- **Agent / Subsystem**: OpenAI Codex / Legacy Device
- **Scope & Context**: Periodic sensor reading generation with monotonic sequence counters.
- **Human Prompt**:
  > "Implement the Legacy Device sensor simulator loop in legacy_system/sensor.py. Generate realistic temperature and humidity values, incrementing sequence_number monotonically starting from 0. Provide deterministic seeding support."
- **Review Outcome**: Modified (2 rounds). Corrected initial sequence counter offset to ensure sequence numbers strictly begin at 0.

#### Task 0034: Sensor Failure Injection Subsystem
- **Agent / Subsystem**: GitHub Copilot / Legacy Device
- **Scope & Context**: Simulating wire faults (duplicate sequences, out-of-order sequences, invalid schemas, corruption).
- **Human Prompt**:
  > "Implement task M1-04: Legacy Device failure-injection subsystem. Read and follow the repository policy, workflow, roadmap, Legacy Device design, shared protocol, Member 1 task document, relevant AI instructions, and both required Group-Explanation PDFs before implementation. Inspect existing code and tests, implement only M1-04, add focused deterministic tests, run relevant tests and Ruff plus ai-history check, record factual results, and stop for human review."
- **Review Outcome**: Modified across 4 rounds (detailed in Case Study 5, Section 6.4.5). Eliminated domain model mutation, enforced PRNG seed isolation, and ensured failure injection operates only on the outbound serialization dictionary.

#### Task 0052: Legacy Gateway HTTP Client and Error Domain Mapping
- **Agent / Subsystem**: OpenAI Codex / Legacy Device
- **Scope & Context**: Synchronous HTTP client transmitting telemetry to the Edge Gateway.
- **Human Prompt**:
  > "Implement the Legacy HTTP client in legacy_system/client.py to send serialized JSON measurements to the Edge Gateway. Handle HTTP timeouts, network connection errors, and Gateway error status codes (400, 409, 422, 503)."
- **Review Outcome**: Modified (3 rounds). Reviewers caught unhandled raw HTTP exceptions escaping the client layer and enforced categorization into domain-specific exceptions (`GatewayConnectionError`, `GatewayResponseError`).

### F.3 Edge Gateway Application and Sequence Logic (Member 2)

#### Task 0026: Gateway Configuration and Environment Parsing
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway
- **Scope & Context**: Ingestion configuration for Edge Gateway service.
- **Human Prompt**:
  > "Implement Edge Gateway configuration loading in edge_gateway/config.py. Support GATEWAY_ID, HOST, PORT, CLOUD_URL, CLOUD_TIMEOUT_SECONDS, CLOUD_MAX_RETRIES, SECURITY_MODE, and SESSION_TTL_SECONDS. Validate frozen defaults."
- **Review Outcome**: Accepted. Confirmed that `SECURITY_MODE` defaults to `classical` and `SESSION_TTL_SECONDS` is strictly validated to 300.

#### Task 0038: Legacy Measurement Ingestion Route and Validation
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway
- **Scope & Context**: FastAPI endpoint `POST /api/v1/legacy/measurements`.
- **Human Prompt**:
  > "Implement the legacy ingestion endpoint on the Edge Gateway. Validate inbound JSON syntax (400 on malformed syntax), schema and field types (422 on missing/invalid fields), and pass valid payloads to sequence validation."
- **Review Outcome**: Accepted. Enforced the frozen contract separating 400 (unparseable JSON) and 422 (schema/domain validation failure).

#### Task 0048: In-Memory Monotonic Sequence Tracking Policy
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway
- **Scope & Context**: Per-device sequence tracking with duplicate and out-of-order rejection.
- **Human Prompt**:
  > "Implement thread-safe in-memory sequence tracking for the Edge Gateway in edge_gateway/sequence.py. Reject duplicate sequence numbers with 409 DUPLICATE_SEQUENCE and lower sequence numbers with 409 OUT_OF_ORDER_SEQUENCE. Accept higher sequence numbers and log sequence gaps."
- **Review Outcome**: Accepted. Confirmed that sequence state is updated prior to Cloud delivery and never rolled back on downstream Cloud failures.

### F.4 Edge Gateway Post-Quantum Cryptography and Transport (Member 3)

#### Task 0006: ML-KEM-768 and HKDF-SHA-256 Cryptographic Wrappers
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway Cryptography
- **Scope & Context**: Core cryptographic primitive wrappers utilizing the maintained `cryptography` library.
- **Human Prompt**:
  > "Start Member 3 at the current primitive phase: record the ML-KEM-768 library decision, add it to edge_gateway with uv, and implement the Gateway encapsulate wrapper plus the frozen HKDF-SHA-256 session-key wrapper with tests. Do not implement HTTP clients, sessions, AES-GCM, the Cloud service, or any protocol change."
- **Review Outcome**: Accepted. Confirmed that HKDF info string is frozen to `b"ml-kem-project:v1:gateway-cloud-session"`, salt is `None`, output length is 32 bytes, and no key material is logged.

#### Task 0011: Gateway In-Memory Secure Session Establishment
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway Cryptography
- **Scope & Context**: Ephemeral session manager with concurrent handshake locking.
- **Human Prompt**:
  > "Member 3 tasks M3-09 through M3-13. Add an in-memory secure session and establish it with GET /api/v1/crypto/public-key, ML-KEM-768 encapsulation, the frozen HKDF call, and POST /api/v1/crypto/sessions. Use one async lock so concurrent callers share one handshake. Validate the session response and do not keep a session when establishment fails. Do not implement AES-GCM, secure measurement sends, measurement retries, or the Cloud service."
- **Review Outcome**: Accepted. Enforced single asyncio lock preventing handshake race conditions during session renewal.

#### Task 0019: AES-256-GCM Encryption and 4-Field Associated Data Builder
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway Cryptography
- **Scope & Context**: Bulk AEAD encryption and canonical AAD formatting.
- **Human Prompt**:
  > "Implement AES-256-GCM encryption with 12-byte CSPRNG nonce generation in edge_gateway/crypto/symmetric.py. Implement the canonical 4-field Associated Data (AAD) builder according to Protocol v1: protocol_version, gateway_id, session_id, request_id. Enforce sorted UTF-8 compact JSON encoding."
- **Review Outcome**: Accepted. Verified that AAD contains exactly the four frozen fields and rejects extraneous metadata.

#### Task 0098: Secure Transport Retries and Session Recovery
- **Agent / Subsystem**: OpenAI Codex / Edge Gateway Cryptography
- **Scope & Context**: Transport resilience, distinguishing ordinary network retries from session invalidation.
- **Human Prompt**:
  > "Implement bounded retry logic with exponential backoff for the Edge Gateway secure transport client. Handle transient network errors and HTTP timeout exceptions when sending telemetry envelopes to the Cloud Service."
- **Review Outcome**: Modified (detailed in Case Study 3, Section 6.4.3). Enforced that ordinary transport retries resend the identical SecureEnvelope without re-encrypting, while 409 session errors trigger session invalidation and re-handshake.

### F.5 Cloud Service Telemetry Ingestion and Storage (Member 4)

#### Task 0018: SQLite Storage Layer and Business Idempotency
- **Agent / Subsystem**: OpenAI Codex / Cloud Service
- **Scope & Context**: SQLite database initialization, schema migration, and measurement insertion repository.
- **Human Prompt**:
  > "Complete all remaining Member 4 work for PR 2: M4-05 through M4-07, as one AI-history task. Implement and test the complete remaining PR 2 storage scope, then stop once for human review. Do not start M4-08 or any later task. Do not modify shared/project-wide files other than required AI-history files without my approval."
- **Review Outcome**: Accepted. Enforced `UNIQUE(device_id, sequence_number)` database index and verified that duplicate submissions return `202 Accepted` without creating duplicate database records.

#### Task 0041: Cloud ML-KEM Key Lifecycle and Public-Key Route
- **Agent / Subsystem**: OpenAI Codex / Cloud Service
- **Scope & Context**: In-memory ML-KEM-768 keypair generation and `/api/v1/crypto/public-key` endpoint.
- **Human Prompt**:
  > "Complete M4-16 through M4-20 as one AI-history task. Implement Cloud ML-KEM-768 lifecycle, compatible maintained-library wrapper, tests and public-key endpoint. No M4-21 or later. Ask before changing edge_gateway or shared/project-wide files. Stop for human review."
- **Review Outcome**: Modified (2 rounds). Reviewers corrected Base64URL encoding rules and purged extraneous key confirmation fields proposed by the model.

#### Task 0072: Cloud Secure Envelope Decryption and Canonical Ingestion
- **Agent / Subsystem**: OpenAI Codex / Cloud Service
- **Scope & Context**: Decrypting `SecureEnvelope` at `POST /api/v1/secure/measurements`.
- **Human Prompt**:
  > "Implement Cloud SecureEnvelope ingestion endpoint. Lookup active session by session_id, decrypt AES-256-GCM ciphertext using derived session key and reconstructed 4-field AAD. Validate decrypted measurement schema and persist to database."
- **Review Outcome**: Accepted. Verified that AEAD decryption failures return `401 Unauthorized` or `422 Unprocessable Entity` without disclosing cryptographic diagnostics or secret buffers.

### F.6 Operations, Integration, and Performance Evaluation (Member 5)

#### Task 0080: Gateway-to-Cloud Cross-Service Integration Tests
- **Agent / Subsystem**: OpenAI Codex / Integration Testing
- **Scope & Context**: Automated pytest suite validating full handshake and payload delivery between Gateway and Cloud.
- **Human Prompt**:
  > "Implement cross-component integration test suite for Edge Gateway and Cloud Service in tests/integration/test_gateway_cloud_secure.py. Test full session establishment, valid telemetry encryption and persistence, expired session recovery, and corrupted ciphertext rejection."
- **Review Outcome**: Accepted. Verified test isolation using ephemeral test databases and mock server fixtures.

#### Task 0185: Complete Three-Tier Docker Compose Topology
- **Agent / Subsystem**: OpenAI Codex / Deployment & Operations
- **Scope & Context**: Multi-container Docker Compose file and healthcheck orchestration.
- **Human Prompt**:
  > "Restore the complete three-tier containerized topology in docker-compose.yml including legacy-device, edge-gateway, and cloud-service. Ensure healthcheck dependency chains, non-root user execution, and persistent SQLite storage volume."
- **Review Outcome**: Accepted (reversing premature omission from Task AD-7). Confirmed that the legacy sensor automatically waits for Gateway health before starting transmissions.

#### Task 0211: Matched-Mode Empirical Evaluation Harness
- **Agent / Subsystem**: OpenAI Codex / Empirical Evaluation
- **Scope & Context**: Benchmarking script executing matched workloads across classical and ML-KEM modes.
- **Human Prompt**:
  > "Implement the matched-mode evaluation script scripts/measure_mode_comparison.py to execute paired workloads through the complete 3-tier pipeline in classical and ML-KEM modes. Measure first-message latency, steady-state latency, wire payload bytes, and storage success. Output clean JSON."
- **Review Outcome**: Accepted. Verified that the script captures real empirical measurements without hardcoding timing constants.

#### Task 0219: Protocol Security Mode Sequence Diagrams
- **Agent / Subsystem**: OpenAI Codex / Architecture Documentation
- **Scope & Context**: Generating detailed Mermaid protocol sequence diagrams for Classical Baseline and Modernized Post-Quantum modes.
- **Human Prompt**:
  > "Create formal Mermaid sequence diagrams illustrating the end-to-end message flow for classical mode and ML-KEM modernized mode. Show transport protocols, exact status codes, payload structures, session caching, and error paths."
- **Review Outcome**: Accepted. Verified that diagrams strictly reflect frozen Protocol v1 contracts with no unauthenticated confirmations or extra parameters.

