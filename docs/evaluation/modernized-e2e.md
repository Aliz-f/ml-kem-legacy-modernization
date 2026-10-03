# Modernized E2E evidence

`tests/integration/test_modernized_end_to_end.py` exercises the complete
Legacy Device client → Edge Gateway → ML-KEM-768 session → AES-256-GCM
SecureEnvelope → Cloud → SQLite path. It keeps the Legacy five-field JSON
payload unchanged and verifies the Cloud query result after secure delivery.

The controlled ambiguous-response case drops the first Cloud response only
after its row commits. The Gateway then resends the same already-built envelope:
the same request ID, session ID, nonce, ciphertext, and four-field AAD. Cloud
business idempotency (`UNIQUE(device_id, sequence_number)`) leaves one logical
row.

Protocol version 1 has no dedicated cryptographic anti-replay counter or
window. Business idempotency is not cryptographic replay protection.
