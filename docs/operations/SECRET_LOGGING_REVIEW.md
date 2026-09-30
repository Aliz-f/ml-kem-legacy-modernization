# Project-wide secret-logging review

This is the Member 5 M5-49 review record. It coordinates existing
component-owned secret-safety tests and records the manual inspection boundary;
it is not a replacement for M5-50's future secure-E2E log-capture regression.

## Review scope and result

Reviewed application logging calls and error paths under `legacy_system/src`,
`edge_gateway/src`, and `cloud_service/src`, with particular attention to the
ML-KEM, HKDF, session, AES-GCM, HTTP route, and failure-injection paths.
The review found that the inspected production log calls use event names, safe
categories, and selected identifiers rather than raw cryptographic buffers or
configuration values. No direct `print` call or logging call containing a
private key, shared secret, session key, password, token, or `.env` content
was found in those inspected source paths.

This is evidence from a bounded source review, not a claim that any future
change is automatically safe. The conventions in
[`LOGGING_CONVENTIONS.md`](LOGGING_CONVENTIONS.md) remain the review standard.

## Prohibited data classes

The project must not log:

- ML-KEM private-key bytes, public-key bytes, encapsulation ciphertext, or
  shared secret;
- AES-GCM session key, derived key, nonce, ciphertext, tag, or plaintext;
- passwords, tokens, credentials, database connection secrets, or `.env`
  contents;
- full request/response bodies or raw vendor exception text that could contain
  one of the values above.

Safe identifiers such as `request_id`, `session_id`, `key_id`, and `record_id`
may be logged when relevant. They are correlation data, not secret material,
and must not become unbounded metrics labels.

## Existing automated coverage run project-wide

The repository-wide `uv run pytest` command includes these component-owned
tests that capture logs or error text using generated/synthetic markers:

| Component | Coverage | Safety assertion |
|---|---|---|
| Gateway | `edge_gateway/tests/test_mlkem.py::test_shared_secret_is_not_logged` | Generated ML-KEM shared secret is absent from captured logs. |
| Gateway | `edge_gateway/tests/test_kdf.py::test_session_key_is_not_logged` | Synthetic shared secret and derived session key are absent. |
| Gateway | `edge_gateway/tests/test_security_logging.py::test_handshake_and_delivery_omit_secrets_and_separate_timings` | Handshake/delivery logs omit shared secret, session key, private-key bytes, and plaintext marker. |
| Cloud | `cloud_service/tests/test_cloud_mlkem.py::test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged` | Private-key bytes and decapsulated secret representations are absent from logs/repr. |
| Cloud | `cloud_service/tests/test_cloud_mlkem.py::test_vendor_failures_are_safe` | Vendor diagnostic marker is suppressed from exceptions and logs. |
| Cloud | `cloud_service/tests/test_cloud_aead.py::test_gateway_encryption_cloud_decryption` | AES-GCM interoperability emits no log text for synthetic key/plaintext inputs. |
| Cloud | `cloud_service/tests/test_cloud_aead.py::test_vendor_error_diagnostics_are_suppressed` | Vendor diagnostic marker is absent from exception and log output. |

## Repeatable review procedure

1. Run `uv run pytest` so the listed component tests execute with the rest of
   the repository.
2. Inspect new or modified logging, exception translation, configuration, and
   crypto/session code for prohibited values and raw payload rendering.
3. Add or update a component-owned marker test when a sensitive path changes.
4. Run `uv run ruff check .`, `uv run pytest`, and `uv run ai-history check`.
5. For a secure end-to-end log capture and CI-specific regression, proceed to
   M5-50 after secure E2E prerequisites are complete.
