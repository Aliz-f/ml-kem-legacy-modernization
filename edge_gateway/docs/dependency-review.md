# Dependency and security review

This note records Member 3's review of the crypto dependencies in `uv.lock` and how the Gateway and Cloud source use them. It does not change a dependency, the lock, or the protocol.

Reviewed areas: unnecessary packages, unmaintained packages, duplicate crypto libraries, and unsafe low-level usage. Checked on 2026-10-04 against `uv.lock`, `uv tree --frozen`, PyPI, and the OSV database.

## One crypto stack

`cryptography` 50.0.2 from `pyca/cryptography` is the only crypto library in the lock. It provides ML-KEM-768, HKDF-SHA-256, and AES-256-GCM. Its only dependency is `cffi` 2.1.1, which needs `pycparser` 3.0. Both are also PyCA projects. `edge_gateway` and `cloud_service` both declare `cryptography>=48`, so the lock resolves them to the same release.

The lock has no `pycryptodome`, `pycryptodomex`, `pynacl`, `liboqs-python`, `pqcrypto`, `kyber-py`, or `quantcrypt`. No source file imports any of them. The library decision in `docs/architecture/ml-kem-library-decision.md` still holds.

## Unnecessary packages

| Package | Needed by | Result |
|---|---|---|
| `cryptography` | Gateway and Cloud runtime | Required |
| `fastapi`, `uvicorn` | Gateway and Cloud HTTP APIs | Required |
| `httpx` | `test` extra only | Not installed at runtime |
| `graphifyy` and the `tree-sitter-*`, `numpy`, `networkx`, `rapidfuzz` packages | Root `dev` group only | Not a component dependency |

`legacy_system` has no dependencies. The Gateway's Cloud clients use the standard library `urllib` and do not import `httpx` or `certifi`. No runtime package was found to be unnecessary.

## Maintenance and advisories

On 2026-10-02, OSV returned no advisories for the locked versions of `cryptography`, `cffi`, `pycparser`, `fastapi`, `starlette`, `uvicorn`, `h11`, `pydantic`, `pydantic-core`, `anyio`, `idna`, `click`, `httpx`, `httpcore`, and `certifi`. All of them had a release in 2026.

`cryptography` 50.0.2 was released on 2026-09-30. Its changelog says the wheels are built with OpenSSL 4.0.3 instead of 4.0.2, adds free-threaded CPython 3.15 wheels, and updates PyO3. It does not change the Python API that the Gateway or Cloud uses. The lock now uses 50.0.2; this review remains scoped to the checked source and lock, not future advisories.

## Low-level usage

All library calls use `cryptography.hazmat.primitives`. No source file imports `cryptography.hazmat.bindings`, a `backend` argument, `ctypes`, `ssl`, `pickle`, `eval`, or `exec`.

| Concern | Finding |
|---|---|
| ML-KEM | The Gateway calls only `MLKEM768PublicKey.from_public_bytes` and `encapsulate`. The Cloud calls only `MLKEM768PrivateKey.generate`, `public_bytes(Encoding.Raw, PublicFormat.Raw)`, and `decapsulate`. Neither side implements ML-KEM. Both check the 1184-byte public key, 1088-byte ciphertext, and 32-byte shared secret. |
| HKDF | Both sides call `HKDF(hashes.SHA256(), length=32, salt=None, info=b"ml-kem-project:v1:gateway-cloud-session")`. |
| AES-GCM | Both sides use `AESGCM` with a 32-byte key and a 12-byte nonce. Cloud also rejects a ciphertext shorter than the 16-byte tag before calling the library. |
| Nonce source | The Gateway nonce is `secrets.token_bytes(12)` from the operating-system CSPRNG. ML-KEM key generation and encapsulation use the library's own randomness. |
| `random` module | Used only by the Gateway and Cloud failure injectors to decide whether a fault happens, and by the Legacy sensor for simulated readings. It never produces a key, nonce, or session ID. |
| IDs | `session_id`, `key_id`, and `request_id` come from `uuid4()`. They are identifiers, not secrets. |
| Fixed inputs | Cloud `/ready` derives a key from 32 zero bytes and encrypts with a zero nonce to check that the library works. That key is never a session key, and it is not stored or sent. |
| TLS | No code disables certificate checks. The Gateway does not add TLS or key pinning. That limit is in `transport-trust.md`. |

## Observations

These items are not defects in protocol v1. They are recorded for M3-78.

- The Gateway crypto wrappers chain the library exception with `from exc`, while the Cloud wrappers use `from None`. The Gateway measurement layer detaches the cause before the HTTP response and logs only fixed event names. A future log call that prints exception chains would expose more than the Cloud does.
- Cloud `app.py` imports `AESGCM` directly for its readiness probe, outside `cloud_service/crypto`. ML-KEM use stays in `cloud_service/crypto/mlkem.py`.
- Gateway `encapsulate` parses the public key twice, once in `validate_public_key` and once to encapsulate. The result is the same, and it costs one extra parse.
- `cryptography>=48` has no upper bound. `uv.lock` pins the installed release, and `uv sync --frozen` is the install path for Docker and CI.

## Review result

The project uses one maintained crypto library for ML-KEM-768, HKDF-SHA-256, and AES-256-GCM. No duplicate crypto library, unnecessary runtime package, known advisory, or unsafe low-level call was found. The lock is updated to `cryptography` 50.0.2.
