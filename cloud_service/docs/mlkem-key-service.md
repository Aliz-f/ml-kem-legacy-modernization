# Cloud ML-KEM keys and public-key API (M4-16–M4-20)

Cloud uses Member 3's existing [library decision](../../docs/architecture/ml-kem-library-decision.md):
`cryptography>=48`, with **50.0.1** retained in the workspace lockfile. It is now
a direct Cloud dependency, so Cloud does not depend on Gateway being installed
to use ML-KEM. No existing package version changed. The only lockfile additions
associate Cloud with this dependency. Production Cloud code never imports
Gateway; Cloud-local interoperability tests import its existing wrapper/parser.

## Library and contract verification (M4-17: partially verified)

**M4-17 is not fully verified. Its Cloud Docker environment compatibility
sub-requirement is explicitly deferred to M4-81 and M4-83.** The evidence below
supports the library selection and local interoperability only; it does not
close that sub-requirement.

The selected PyCA library supplies ML-KEM-768 key generation, raw public-key
serialization and decapsulation. The [official ML-KEM API documentation](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/mlkem/)
defines a 1184-byte public key, 1088-byte ciphertext and 32-byte shared secret.
The vendor returns `(shared_secret, ciphertext)` from encapsulation; the
existing Gateway wrapper exposes `(ciphertext, shared_secret)`. Cloud's
`crypto/mlkem.py` exposes `generate_keypair() -> (public_bytes, private_handle)`
and `decapsulate(ciphertext, private_handle) -> shared_secret`.

Verified locally on Python 3.12.14, Windows, cryptography 50.0.1 and its
OpenSSL 4.0.2 backend. Tests generate Cloud keys, pass raw public bytes through
the existing Gateway encapsulation wrapper, and check equal secrets. Endpoint
tests also use the existing Gateway public-response parser. No new algorithm,
parameter negotiation, RNG or primitive implementation was introduced. Key
generation uses the maintained library's randomness; `FAILURE_SEED` is unused.

This is implementation-level alignment with Member 3's recorded decision, not
a claim of a new conversation or peer approval.

### Strongest currently available container compatibility evidence

The revision inspection confirmed that `cloud_service/Dockerfile` does not
exist and `docker-compose.yml` contains only `services: {}`. Neither Docker nor
Podman is available on PATH. The available WSL launcher returned usage text
for `wsl --list --quiet`, so it did not establish a usable Linux runtime.
There is no defined Cloud base image, architecture or container backend to
verify without starting later deployment tasks.

Static inspection of `uv.lock` found cryptography 50.0.1 `cp39-abi3`
manylinux and musllinux wheel entries, including x86_64 and aarch64, and cffi
2.1.1 `cp312` Linux wheel entries. These are artifact candidates for Python
3.12, not proof that the eventual image can install or run ML-KEM.

The following additional check succeeded on the current Python 3.12 host:

```powershell
uv sync --frozen --package cloud-service --no-dev --python-platform x86_64-unknown-linux-gnu --dry-run
```

UV produced a Linux-target installation plan using the unchanged locked
cryptography 50.0.1, cffi 2.1.1 and pydantic-core 2.46.5 versions. This was a
**dry run**: it did not download/install Linux packages, build a Cloud image,
execute a Linux backend, or alter the project environment or lockfile. The
target is a compatibility probe, not a decision about the future Docker image.
Native Windows wrapper/lifecycle tests provide actual execution evidence only
for the host described above.

### Deferred verification and completion gate

| Task | Required evidence to close the deferred M4-17 sub-requirement |
| --- | --- |
| M4-81 — Dockerize Cloud Service (Member 4) | Create the designated Cloud Dockerfile; use the required Python version and frozen uv installation; demonstrate successful crypto dependency installation on the chosen image/architecture. |
| M4-83 — Docker readiness verification (Member 4, coordinated with Member 5 integration) | From a clean image build, verify Cloud startup, SQLite initialization, ML-KEM key initialization, `/health` and the then-complete `/ready`; run the Cloud ML-KEM/Gateway interoperability tests against that actual container backend without local-machine assumptions. |

Record image/base, Python, crypto/backend versions and actual command results
when those tasks run. **Until then, Cloud container runtime compatibility is
unverified and M4-17 remains partially verified.** M4-81/M4-83 are not started
by this revision. The current `/ready` returning 503 is not successful M4-83
readiness evidence. Unsupported key initialization continues to fail closed.
No Docker infrastructure, implementation, tests, dependency versions or
lockfile changes were needed for this review revision.

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

`/health` reports liveness after initialization. `/ready` remains `503` because
the full secure processing path is unfinished. Plaintext baseline ingestion
remains unavailable in `mlkem` mode; it is never a fallback. Session and secure
measurement routes remain unimplemented (`404`). M4-21 KDF, sessions, AES-GCM,
runtime fault injection and full readiness are outside this task.

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
