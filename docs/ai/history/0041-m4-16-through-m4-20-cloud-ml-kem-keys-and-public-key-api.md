# AI Task 0041 — M4-16 through M4-20 Cloud ML-KEM keys and public-key API

**Status:** Complete

**Created:** 2026-09-29T16:50:06+03:00

**Updated:** 2026-09-29T20:37:54+03:00

**Agent:** Codex

---

# Task

Implement Cloud ML-KEM-768 lifecycle, compatible maintained-library wrapper, tests and public-key endpoint. No M4-21 or later. Cloud-local changes plus authorized AI history and minimal uv.lock dependency association; preserve all locked versions.

---

# Prompt

Complete M4-16 through M4-20 as one AI-history task.

Ask before changing edge_gateway or shared/project-wide files.

Stop for human review. Do not start M4-21.

Yes. You may update uv.lock as required for Cloud's direct cryptography dependency.

Do not upgrade existing package versions or make unrelated lockfile changes.

Continue M4-16 through M4-20 and stop for human review.

---

# AI Implementation — Initial

## LLM Output

Implemented M4-16 through M4-20 Cloud code: maintained ML-KEM-768 wrapper with opaque private handles and safe failure translation; per-lifespan ephemeral key generation, rotation and cleanup; protocol-v1 Base64URL public-key endpoint; tests against existing Gateway encapsulation and public-response parser. Cloud uses the existing Member 3 cryptography selection as a direct dependency. Updated Cloud-local lifecycle documentation and recorded runtime limitations.

## Files Created

- cloud_service/src/cloud_service/crypto/__init__.py
- cloud_service/src/cloud_service/crypto/mlkem.py
- cloud_service/src/cloud_service/crypto/keys.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/tests/test_cloud_mlkem.py
- cloud_service/tests/test_cloud_public_key.py
- cloud_service/docs/mlkem-key-service.md
- docs/ai/history/0028-m4-16-through-m4-20-cloud-ml-kem-keys-and-public-key-api.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/pyproject.toml
- cloud_service/docs/application.md
- uv.lock
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv lock --offline
- uv sync --frozen --all-packages --all-extras
- uv run pytest cloud_service/tests/test_cloud_mlkem.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_app.py -q
- uv run pytest
- uv run ruff check .
- git diff --check
- uv run ai-history check
- uv run python - (TOML comparison of HEAD:uv.lock with working copy)

### Results

- Resolved 30 packages; only two Cloud cryptography dependency association entries added. No upgrades.
- Succeeded; rebuilt Cloud package. Existing versions retained. Cache hardlink fallback warning only.
- 35 passed, 1 existing Starlette TestClient deprecation warning.
- 344 passed, 1 existing Starlette TestClient deprecation warning in 15.86 seconds.
- Final run passed after correcting one E731 test lambda assignment.
- Final run passed after removing a trailing blank line. Git emitted line-ending conversion warnings only.
- Validation passed.
- Verified all lock data identical after removing the two authorized Cloud cryptography associations; all package versions preserved.

## AI Notes

Task 0028 resumed without duplication. Verified Python 3.12.14, Windows, cryptography 50.0.1, OpenSSL 4.0.2. M4-17 alignment uses existing Member 3 library decision and real wrapper/parser interoperability; no new teammate communication claimed. Container runtime verification remains outstanding: no Cloud Dockerfile or Compose service exists and Docker CLI is unavailable. This limitation is explicit in Cloud-local documentation. Ephemeral keys and unauthenticated HTTP public-key trust remain course limitations; Python memory zeroization is not guaranteed. Modernized mode currently serves keys only, rejects baseline ingestion, and keeps readiness 503; sessions and secure ingestion remain 404. No M4-21 KDF or later work, no Gateway edits, no unrelated shared edits. No secret material recorded. Awaiting human review.

---

# Human Review — Round 1

## Problems Found

M4-17 is not fully verified. The task requires verification of Cloud Docker environment compatibility, but the current work explicitly states that Cloud container runtime support has not been verified.

## Decision

Modified

## Requested Modifications

Do not add unrelated Docker infrastructure. Determine the strongest verification possible within the current repository for Cloud Docker compatibility. If actual runtime verification is impossible because the Dockerfile/environment belongs to M4-81/M4-83, record this M4-17 sub-requirement as explicitly deferred to those tasks and do not claim M4-17 fully verified.

Keep all existing M4-16–M4-20 implementation unchanged unless required by that verification.

---

# AI Revision — Round 1

## Revision Summary

Revised M4-17 status to explicitly partially verified. Documented strongest available evidence: existing native wrapper interoperability and lifecycle checks, locked Linux wheel candidates, and successful frozen Linux-target dependency dry run. Deferred the Cloud Docker compatibility sub-requirement specifically to M4-81 (Member 4 Dockerfile and crypto installation) and M4-83 (clean-image startup, DB/ML-KEM initialization, health/readiness and actual-container interoperability). Corrected Docker ownership wording. No implementation changes were required.

## Files Created

- None

## Files Modified

- cloud_service/docs/mlkem-key-service.md
- docs/ai/history/0028-m4-16-through-m4-20-cloud-ml-kem-keys-and-public-key-api.md
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- Repository/container-tool inspection and uv.lock Linux-wheel metadata inspection
- uv sync --frozen --package cloud-service --no-dev --python-platform x86_64-unknown-linux-gnu --dry-run
- uv run pytest cloud_service/tests/test_cloud_mlkem.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_app.py -q
- uv run ruff check .
- uv run ai-history check
- git diff --check

### Results

- No Cloud Dockerfile; Compose services empty; Docker and Podman not on PATH. WSL list attempt returned usage, not a usable Linux runtime. Locked cryptography 50.0.1 and cffi 2.1.1 include Linux wheel candidates; metadata is not runtime proof.
- Passed; Linux-target installation plan retains cryptography 50.0.1, cffi 2.1.1 and pydantic-core 2.46.5. No package download/installation, environment mutation, image build or Linux execution performed.
- 35 passed, 1 existing Starlette deprecation warning in 1.02 seconds.
- All checks passed.
- Validation passed.
- Passed; line-ending conversion warnings only.

## AI Notes

M4-17 is NOT fully verified. Actual Cloud Docker compatibility is explicitly deferred to M4-81/M4-83; documentation specifies completion evidence and does not treat dependency planning or Windows tests as a container test. M4-81/M4-83 not started. Existing M4-16 through M4-20 source, tests, dependencies and lockfile unchanged by this revision. No unrelated Docker infrastructure or Gateway/shared changes beyond required history. Full suite from initial output remains 344 passed; focused verification rerun for this documentation-only revision. Return to Awaiting Human Review; no acceptance or final verification inferred.

---

# Human Review — Round 2

## Problems Found

No blocking problems identified after the revision.

M4-17 Docker runtime verification is correctly documented as partially verified and explicitly deferred to M4-81/M4-83.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final task 0028 work and accept it.

---

# Final Outcome

**Status:** Complete
