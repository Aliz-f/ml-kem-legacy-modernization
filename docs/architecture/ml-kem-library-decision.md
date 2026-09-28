# ML-KEM library decision

Member 3, protocol version `1`. The algorithm suite stays ML-KEM-768, HKDF-SHA-256, and AES-256-GCM. This record selects the library only.

## Selected library

`cryptography` version 48 or newer, from the Python Cryptographic Authority (`pyca/cryptography`).

Checked on 2026-09-22 against PyPI release 50.0.1:

- Python `>=3.9`, including 3.12
- License `Apache-2.0 OR BSD-3-Clause`
- Production/Stable
- ML-KEM-768 at `cryptography.hazmat.primitives.asymmetric.mlkem`
- HKDF-SHA-256 and AES-GCM in the same package

`edge_gateway` depends on `cryptography>=48`. `uv.lock` pins the installed release. Do not add `requirements.txt`. Member 4 should use this same package for decapsulation and the same HKDF call.

`salt=None` in `cryptography.hazmat.primitives.kdf.hkdf.HKDF` follows RFC 5869: the salt is HashLen zero bytes. The protocol requires both sides to use that exact call. An implementation using another library must verify its RFC 5869 salt handling against this contract rather than substituting a salt value without validation.

The project protocol is not HPKE. Do not replace the frozen HKDF info string with an HPKE suite.

## Why

The course requires a maintained ML-KEM implementation. This package implements FIPS 203 ML-KEM-768 (1,184-byte public key, 1,088-byte ciphertext, 32-byte shared secret), publishes wheels, and already provides the HKDF and AES-GCM the protocol requires.

Gateway code calls it only through `edge_gateway.crypto`.

## Rejected alternatives

| Library | Reason |
|---|---|
| `kyber-py` | Learning implementation. Not constant-time. No cryptographic guarantee. |
| `quantcrypt` | Wraps archived PQClean and was scheduled to become read-only in July 2026. |
| `liboqs-python` | Maintained and correct, but the PyPI package builds liboqs on first import. Fallback only if a `cryptography` build cannot run ML-KEM-768. |
| `pqcrypto` 1.0.0 | Real ML-KEM-768 wheels, without this project's HKDF and AES-GCM. |

No ML-KEM algorithm is implemented in this repository.

## Known limitations

- `decapsulate` raises `UnsupportedAlgorithm` when the backend has no ML-KEM. The wrapper turns that into `MlKemError`. Docker and CI must use a build where ML-KEM-768 works.
- A modified, correctly sized ciphertext may not raise. ML-KEM can return different keying material (implicit rejection). Tests must not require every such ciphertext to throw.
- The gateway trusts a public key because it came from the configured Cloud URL. This library does not add TLS, pinning, or identity authentication.

## Sources

- https://pypi.org/project/cryptography/
- https://cryptography.io/en/latest/hazmat/primitives/asymmetric/mlkem/
- https://blog.trailofbits.com/2026/06/30/shipping-post-quantum-cryptography-to-python/
- https://github.com/GiacomoPope/kyber-py
- https://github.com/PQClean/PQClean
- https://github.com/aabmets/quantcrypt
- https://github.com/open-quantum-safe/liboqs-python
