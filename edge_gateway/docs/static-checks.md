# Static and code-quality verification

This note records Member 3's checks before a crypto pull request. It does not change runtime code, a dependency, or the protocol.

Checked on 2026-10-02 on `feat/gateway-static-checks`, which starts from `feat/gateway-dependency-review` at `c75a5cb`. `origin/develop` was `146064f` and was not ahead.

## Commands

```bash
uv run pytest edge_gateway/tests
uv run ruff check edge_gateway
uv run ai-history check
uv run pytest tests/integration/test_gateway_cloud_secure.py \
  tests/integration/test_secure_message_tamper.py \
  tests/integration/test_corrupt_ciphertext_demo.py \
  tests/integration/test_mlkem_handshake_failure_demo.py \
  tests/integration/test_pqc_observability.py \
  tests/integration/test_legacy_compatibility.py \
  tests/integration/test_mode_evaluation.py \
  tests/integration/test_clean_container_crypto.py \
  tests/integration/test_gateway_crypto_image.py
```

| Check | Result |
|---|---|
| Gateway tests | 500 passed, including the three scans in `test_static_checks.py` |
| Ruff on `edge_gateway` | Passed |
| AI history | Passed |
| Secure integration tests | 54 passed, 2 skipped |

The two skips are `test_clean_container_crypto.py` and `test_gateway_crypto_image.py`. Docker was not installed on the machine that ran this historical check, so the container runs did not happen there. They were subsequently run on 2026-10-04 with Docker available: `uv run pytest -q tests/integration/test_clean_container_crypto.py tests/integration/test_gateway_crypto_image.py` passed 8 tests.

## Diff inspection

The inspection covered `git diff origin/develop...HEAD` and the whole tracked tree, because most Member 3 crypto work is already merged into `develop`.

| Item | Result |
|---|---|
| Debug secret logging | No log call passes a shared secret, session key, private key, key bytes, or plaintext. Cloud log lines use `%r` only for `request_id`, `gateway_id`, `session_id`, and `device_id`. No source logs an exception with `exc_info`, `logger.exception`, or a traceback. |
| Key fixtures | Tests generate ML-KEM key pairs and run real handshakes at run time. Fixed key and secret values are repeated-byte placeholders such as `b"\x11" * 32`, `b"a" * 32`, `b"x" * 32`, and `bytes.fromhex("ab" * 32)`. They check input lengths, KDF determinism, the Cloud session store, and that shutdown wipes a key buffer. No tracked Python or JSON file holds a high-entropy literal of 40 characters or more. Cloud `/ready` uses `b"\x00" * 32` only for its library self-test. |
| Private-key files | No `.pem`, `.key`, `.der`, `.p12`, or `.pfx` file is tracked or was ever added on any branch. No `BEGIN ... PRIVATE KEY` block is tracked. |
| Temporary crypto prints | No `breakpoint` or `pdb` call is tracked. `print` appears only in command-line tools whose job is to print a result: `cloud_service/tools/measure_baseline.py` prints baseline timing JSON, the two `edge_gateway/docker` checks print a fixed `ok` line, and `src/ai_history/cli.py` prints workflow status. None prints key, secret, nonce, or plaintext material. Service source has no `print`. After the M3-78 merge from `develop`, `test_gateway_baseline_integration.py` also prints a classical-mode timing report. |
| `.env` values | Only `.env.example` is tracked or was ever added. It holds non-secret defaults. `.gitignore` excludes `.env` and `.env.*` except that file. |

In the unmerged diff, the words `shared_secret`, `session_key`, and `private_key` appear only in review prose and in test assertions that check names. No value is printed or stored.

`test_static_checks.py` repeats the file, PEM, print, and log-argument scans on every test run.

## Review result

The required checks pass. The inspection found no secret logging, key file, PEM block, debug print, or `.env` value. The Docker image tests subsequently passed on a machine with Docker on 2026-10-04.
