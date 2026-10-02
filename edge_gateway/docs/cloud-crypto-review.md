# Peer review of Cloud crypto

This note records Member 3's review of the current Cloud crypto implementation. It does not change Cloud code.

Reviewed areas: key-pair handling, the public-key endpoint, decapsulation, HKDF-SHA-256, session creation, AES-GCM decryption, session ownership, secure-envelope validation, and business idempotency.

## Same session key

Cloud derives the session key with HKDF-SHA-256, `salt=None`, `info=b"ml-kem-project:v1:gateway-cloud-session"`, and length 32. The Gateway KDF uses those same inputs. Session establishment decapsulates the encapsulation ciphertext and passes that shared secret to `derive_session_key`. The `/ready` probe also calls `derive_session_key`, but only with 32 zero bytes, and it does not create or store a session.

## Private key handling

`PrivateKey` is an opaque process-local handle. `KeyService.public_response` returns `protocol_version`, `algorithm`, `key_id`, and the Base64URL public key. `SecureSession.response` returns `protocol_version`, `session_id`, `status`, and `expires_at`. The session key is excluded from `repr`. Closing the handle drops the vendor reference. The module states that Python cannot guarantee memory zeroization.

## Secure endpoint and authentication

`POST /api/v1/secure/measurements` validates a six-field `SecureEnvelope` before session lookup. A plaintext canonical measurement is not that object, so it is rejected before storage. After a matching session is found, AES-GCM decrypts with the four-field AAD. An `AeadError` increments `cloud_decryption_failures_total` and returns `400 SECURE_MESSAGE_REJECTED` before `save_idempotent`.

## Gateway and session binding

`SessionManager.get` looks up the session, then rejects a different `gateway_id` with `400 SECURE_MESSAGE_REJECTED`. Expiry is checked after ownership and is not extended. After decryption, measurement validation requires the plaintext `gateway_id` to match the envelope `gateway_id`.

## Idempotency and replay

`save_idempotent` uses `ON CONFLICT(device_id, sequence_number) DO NOTHING`. A repeated logical measurement returns `already_accepted` and the original row. Cloud documentation and `session.py` call this business idempotency. They do not claim a cryptographic replay counter or window. An envelope that adds `message_counter` fails the six-field schema.

## Valid-length ML-KEM ciphertext

Decapsulation requires 1088 bytes and raises when the length differs. The decapsulation function states that correct-length tampering may not raise. A valid-length change can therefore still produce a shared secret and a session. Later AES-GCM authentication is what rejects a message sealed under a different key.

## Review result

The inspected Cloud code matches the frozen protocol version 1 session-key contract. The remaining limits are the ones the code and Cloud notes already state: in-memory sessions, no cryptographic replay window, no guaranteed memory zeroization, and implicit rejection for a valid-length ML-KEM ciphertext.
