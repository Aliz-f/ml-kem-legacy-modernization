# Cloud ML-KEM keys and public-key API (M4-16–M4-20)

Cloud uses Member 3's existing [library decision](../../docs/architecture/ml-kem-library-decision.md):
`cryptography>=48`, with **50.0.2** retained in the workspace lockfile. It is now
a direct Cloud dependency, so Cloud does not depend on Gateway being installed
to use ML-KEM. No existing package version changed. The only lockfile additions
associate Cloud with this dependency. Production Cloud code never imports
Gateway; Cloud-local interoperability tests import its existing wrapper/parser.

## Library and contract verification (M4-17: complete)

The original local library/interoperability evidence below was later augmented
by M4-81/M4-83 deployment work. The current Cloud Dockerfile installs from the
frozen lock, and CI plus the Compose integration tests verify startup, SQLite,
ML-KEM initialization, `/health`, and `/ready` in the containerized service.

The selected PyCA library supplies ML-KEM-768 key generation, raw public-key
serialization and decapsulation. The [official ML-KEM API documentation](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/mlkem/)
defines a 1184-byte public key, 1088-byte ciphertext and 32-byte shared secret.
The vendor returns `(shared_secret, ciphertext)` from encapsulation; the
existing Gateway wrapper exposes `(ciphertext, shared_secret)`. Cloud's
`crypto/mlkem.py` exposes `generate_keypair() -> (public_bytes, private_handle)`
and `decapsulate(ciphertext, private_handle) -> shared_secret`.

Historical local verification ran on Python 3.12.14, Windows, cryptography
50.0.1 and its OpenSSL 4.0.2 backend. Tests generate Cloud keys, pass raw public bytes through
the existing Gateway encapsulation wrapper, and check equal secrets. Endpoint
tests also use the existing Gateway public-response parser. No new algorithm,
parameter negotiation, RNG or primitive implementation was introduced. Key
generation uses the maintained library's randomness; `FAILURE_SEED` is unused.

This is implementation-level alignment with Member 3's recorded decision, not
a claim of a new conversation or peer approval.

### Historical and current container compatibility evidence

The following paragraph records the original pre-deployment inspection; it is
historical evidence, not the current deployment state. The current repository
has `cloud_service/Dockerfile` and Compose Cloud/Gateway services. CI builds the
Cloud image and probes `/health` and `/ready`; the Compose E2E suite exercises
Cloud startup and delivery in both security modes.

At the time of that inspection, `uv.lock` contained cryptography 50.0.1 `cp39-abi3`
manylinux and musllinux wheel entries, including x86_64 and aarch64, and cffi
2.1.1 `cp312` Linux wheel entries. These are artifact candidates for Python
3.12, not proof that the eventual image can install or run ML-KEM.

The following additional check succeeded on the current Python 3.12 host:

```powershell
uv sync --frozen --package cloud-service --no-dev --python-platform x86_64-unknown-linux-gnu --dry-run
```

UV produced a Linux-target installation plan using the then-locked
cryptography 50.0.1, cffi 2.1.1 and pydantic-core 2.46.5 versions. This was a
**dry run**: it did not download/install Linux packages, build a Cloud image,
execute a Linux backend, or alter the project environment or lockfile. The
target is a compatibility probe, not a decision about the future Docker image.
Native Windows wrapper/lifecycle tests provide actual execution evidence only
for the host described above.

### Completion evidence

| Task | Completed evidence |
| --- | --- |
| M4-81 — Dockerize Cloud Service (Member 4) | `cloud_service/Dockerfile` uses Python 3.12 and a frozen `uv` install; the Cloud image is built by CI and Compose tests. |
| M4-83 — Docker readiness verification (Member 4, coordinated with Member 5 integration) | CI starts the Cloud image in `mlkem` mode and probes `/health` and `/ready`; Compose tests verify Cloud startup, health/readiness, and delivery in both modes. |

The pre-deployment statements above remain historical. Current container
verification is recorded in the CI workflow and
`tests/integration/test_gateway_compose_e2e.py`; unsupported key
initialization continues to fail closed.

## Lifetime and mode behavior

`create_app()` and module import generate no keys. Each `mlkem` application
lifespan initializes storage, generates one key pair and assigns a fresh
`cloud-key-<UUID>` identifier before becoming live. Repeated public-key requests
return the same key and identifier during that lifespan. Restart creates both
anew. Independent app instances hold independent keys.

The private key stays in an opaque in-memory handle with no serialization API
or value-bearing representation. Shutdown closes the handle, releases the
vendor key reference, clears app state and closes SQLite, including when the
lifespan exits exceptionally. Python/backend memory zeroization is not
guaranteed. Keys and shared secrets are not logged or written to SQLite, files,
responses or AI history. Tests serialize a key only in test memory to check its
absence from logs, responses and the disposable database.

`classical` mode does not generate keys and the public-key endpoint returns a
generic `503 SERVICE_UNAVAILABLE`. In `mlkem` mode, key initialization failure
aborts startup with a safe error and closes already-open storage. Vendor
exception messages and traceback chains are suppressed at wrapper boundaries.
Public-response failures also return a generic `503`, without vendor details.

`/health` reports liveness after initialization. `/ready` verifies initialized
storage and, in `mlkem` mode, key/session state plus KDF/AEAD usability.
Plaintext baseline ingestion remains unavailable in `mlkem` mode; it is never a
fallback. The session and secure-measurement routes implement the remaining
secure processing path using the key service described here.

## Public-key response

`GET /api/v1/crypto/public-key` returns `200` in the running `mlkem` service,
with `Cache-Control: no-store` and exactly these fields:

```json
{
  "protocol_version": "1",
  "algorithm": "ML-KEM-768",
  "key_id": "cloud-key-<generated UUID>",
  "public_key": "<unpadded Base64URL of raw 1184-byte public key>"
}
```

No private key, Cloud identity field, session key or shared secret is returned.
Only the public bytes are Base64URL encoded here; a general encoding/decoding
utility is not introduced ahead of its task. Malformed ciphertext type/length,
closed handles, library failures and malformed library results raise safe
`MlKemError` exceptions. Valid-length modified ciphertext is not assumed to
raise: ML-KEM may use implicit rejection. There is no key-confirmation scheme.

Ephemeral identity and unauthenticated HTTP key distribution are explicit
course-scope limitations. An active attacker could substitute a public key;
this endpoint does not authenticate Cloud identity. Production key management
and authenticated distribution (such as TLS or pinning) remain future work.

## Verification commands

```powershell
uv sync --frozen --all-packages --all-extras
$env:UV_NO_SYNC='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
uv run pytest cloud_service/tests/test_cloud_mlkem.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_app.py -q
uv run ruff check .
uv run pytest
uv run ai-history check
```

Tests cover wrapper agreement and input/output validation, backend error
sanitization, key rotation and independent instances, safe endpoint responses,
absence of secret material, disabled baseline mode, failure cleanup and normal
and exceptional shutdown. No test demands explicit rejection of every
valid-length ciphertext mutation.
