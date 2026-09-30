# Secure-envelope model (M4-33 only)

`cloud_service.crypto.envelope.SecureEnvelope` is an immutable, slotted wire
model with exactly six string fields: `protocol_version`, `gateway_id`,
`session_id`, `request_id`, `nonce`, and `ciphertext`. The frozen protocol uses
version `"1"` and Base64URL strings for nonce/ciphertext. The model retains
those encoded values verbatim and adds no counter, Cloud identity, key,
plaintext or derived metadata.

`from_dict()` accepts an already-parsed JSON object with exactly those fields;
missing/extra fields and non-string values raise `EnvelopeSchemaError` without
echoing payload values. Direct construction also checks string types.
`to_dict()` returns a fresh dictionary with all six wire values.

This is a schema model, **not a validated or authenticated envelope**.
M4-34 will enforce version 1, non-empty identifiers, valid Base64URL, decoded
nonce length, ciphertext content and the agreed size limit. No such validation,
decoding, session lookup, AAD construction, decryption, logging, persistence or
HTTP route is added here. The current model can represent semantically invalid
strings; callers must not interpret successful construction as secure acceptance.

Tests check the exact schema, immutability, rejection without coercion, safe
errors, dictionary isolation and round-trip compatibility with the unchanged
Gateway envelope builder. This is wire-model compatibility, not secure E2E.
M4-34 and later tasks remain unstarted.

Run `uv run pytest cloud_service/tests/test_cloud_envelope.py -q` in the
configured workspace environment (`UV_NO_SYNC=1`).
