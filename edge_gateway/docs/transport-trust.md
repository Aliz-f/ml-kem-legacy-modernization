# Gateway transport trust

The course test environment, including Docker, may use HTTP between the
Gateway and the Cloud. Modernized mode adds application-layer ML-KEM-768 key
establishment and AES-256-GCM payload protection on that path. The default
`CLOUD_URL` is `http://cloud-service:9000`.

This is a documented trust-model limitation, not an unresolved implementation choice.
The repository does not add HTTPS, mTLS, or certificate handling unless the
shared protocol is revised.

The frozen statements are section 24 of
`docs/architecture/04 - Shared Cross-Component Protocol Specification.md` and
section 24 of `docs/architecture/02 - Edge Gateway.md`.

## What this implementation demonstrates

Application-layer post-quantum key establishment and authenticated encrypted
Gateway-to-Cloud payloads are demonstrated.

The Gateway fetches `protocol_version`, `algorithm`, `key_id`, and
`public_key` from the configured Cloud URL, encapsulates with ML-KEM-768, and
derives the session key with HKDF-SHA-256. Measurements then travel in an
AES-256-GCM SecureEnvelope. The Gateway trusts that public key because it came
from the configured endpoint. ML-KEM does not authenticate Cloud identity. On
unauthenticated HTTP, an attacker who can replace the public-key response can
substitute the key.

## Outside the initial implementation

The following stay outside the initial implementation:

- production TLS certificate lifecycle
- mTLS
- PKI
- public-key pinning
- signed key distribution

## Key confirmation

Protocol version 1 does not add a separate key-confirmation tag. A
confirmation tag can check that both sides derived the same session key. It
does not remove the risk of unauthenticated public-key substitution, because
that substitution happens before encapsulation.
