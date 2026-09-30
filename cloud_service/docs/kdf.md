# Cloud HKDF and interoperability (M4-21/M4-22)

`cloud_service.crypto.kdf.derive_session_key(shared_secret)` accepts exactly
32 bytes of ML-KEM shared secret and returns one 32-byte session key using the
existing `cryptography` dependency. Every call creates a fresh HKDF object with
SHA-256, `salt=None`, and the exact fixed info bytes
`b"ml-kem-project:v1:gateway-cloud-session"`. No protocol values are configurable.

The wrapper rejects invalid input before HKDF and translates library failures
or invalid output into a generic `KdfError`, suppressing vendor exception
chains. It never logs or persists inputs or outputs. There is no custom KDF,
transcript binding, extra confirmation key, or key confirmation.

Cloud-local tests use the unchanged Gateway wrappers: Cloud generates an
ML-KEM-768 pair, Gateway encapsulates, Cloud decapsulates, then each side calls
its own HKDF wrapper. Tests compare secrets and derived keys without printing
them, verify identical fixed info bytes, and check the exact Cloud library
parameters including `salt=None`. Separate tests cover deterministic derivation,
input validation and safe vendor failures.

This is primitive interoperability, not an HTTP session or secure E2E test.
No Gateway code or dependency changes are needed. M4-23 session models and
later processing are not started. The M4-17 Docker runtime verification deferral
to M4-81/M4-83 remains unchanged.

Run from the configured workspace environment:

```powershell
$env:UV_NO_SYNC='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
uv run pytest cloud_service/tests/test_cloud_kdf.py -q
```
