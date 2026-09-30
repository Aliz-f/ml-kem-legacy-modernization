# Cloud authenticated decryption and AAD (M4-30–M4-32)

`crypto/symmetric.py` wraps the existing cryptography `AESGCM` implementation.
`decrypt(key, nonce, ciphertext, associated_data)` requires a 32-byte key,
12-byte nonce, ciphertext including the 16-byte authentication tag, and AAD
bytes. Bytes and mutable byte buffers are supported, including session key
buffers. Plaintext is returned only after authentication succeeds. Invalid
inputs and library/authentication failures raise safe `AeadError` exceptions;
vendor diagnostics are suppressed. No plaintext parsing, storage or logging
occurs in this wrapper.

`crypto/aad.py` independently constructs exactly `protocol_version`,
`gateway_id`, `session_id`, and `request_id`. Version must be `"1"`; identifiers
must be non-empty, trimmed strings. JSON uses sorted keys, compact separators,
the default ASCII escaping (matching Gateway, including non-ASCII identifiers),
and UTF-8 encoding. No Cloud identity, nonce, counter or fifth field is added.

Cloud-local tests compare bytes against the existing Gateway AAD builder,
decrypt Gateway ciphertext, and reject changes to each AAD field, key, nonce,
ciphertext and tag. For the version-tampering cryptographic test, altered AAD
bytes are built explicitly because both production builders reject version 2
before cryptography. Empty and arbitrary-byte plaintext tests demonstrate that
the wrapper does not parse data. Test-only fixed keys are not runtime randomness.

No Gateway, dependency or protocol files changed. There is no secure-envelope
model or secure-ingestion route in this task; M4-33 and later work remain
unstarted. HTTP mapping and plaintext validation belong to the later secure
processing path. This is primitive interoperability, not secure-message E2E.
M4-17 Docker runtime verification remains deferred to M4-81/M4-83.

Run `uv run pytest cloud_service/tests/test_cloud_aead.py -q` in the configured
workspace environment (`UV_NO_SYNC=1`; use `PYTHONUTF8=1` on Windows).
