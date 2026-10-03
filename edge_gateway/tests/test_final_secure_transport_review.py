"""Keep the final secure-transport review anchored to the frozen checklist and code."""

from pathlib import Path

ROOT = Path(__file__).parents[2]
CHECKLIST = (
    "ML-KEM library choice", "ML-KEM-768 wrapper", "Public-key response",
    "Public-key trust limitation", "HKDF-SHA-256", "Session manager",
    "Session reuse", "Session expiry", "409 `SESSION_INVALID` recovery",
    "409 `SESSION_EXPIRED` recovery", "One-recovery-attempt bound", "AES-256-GCM",
    "12-byte nonce handling", "Canonical AAD", "SecureEnvelope",
    "Ambiguous ordinary transport retry", "Session recovery", "Replay limitation",
    "Secure Cloud transport", "Fail closed", "No runtime plaintext fallback",
    "Failure injection", "Logging", "Metrics", "Tests", "Docs", "AI history",
)


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_every_checklist_item_has_a_result() -> None:
    review = _text("edge_gateway/docs/final-secure-transport-review.md")
    for item in CHECKLIST:
        assert f"| {item} | Pass |" in review, item


def test_review_matches_the_secure_path() -> None:
    transport = _text("edge_gateway/src/edge_gateway/crypto/secure_transport.py")
    send = transport.split("async def send", 1)[1].split("def _session_is_active", 1)[0]
    recover = transport.split("async def _recover", 1)[1].split("def _seal", 1)[0]
    deliver = transport.split("def _deliver", 1)[1].split("def _post", 1)[0]

    assert send.count("_recover(") == 1
    assert "self._sessions.invalidate(rejected_session_id)" in recover
    assert "self._seal(session, request_id, measurement)" in recover
    assert "asyncio.to_thread(\n                self._post," in recover
    assert deliver.count("_dump(envelope)") == 1
    assert "for attempt in range(self._max_retries + 1)" in deliver

    envelope = _text("edge_gateway/src/edge_gateway/crypto/envelope.py")
    assert "message_counter" not in envelope.split('"""', 2)[2]
    assert "secrets.token_bytes(NONCE_LENGTH)" in _text(
        "edge_gateway/src/edge_gateway/crypto/symmetric.py"
    )
    assert "UNIQUE(device_id, sequence_number)" in _text(
        "cloud_service/src/cloud_service/storage/database.py"
    )
    assert "_secure_transport(settings, registry, failures, application_registry)" in _text(
        "edge_gateway/src/edge_gateway/app.py"
    )


def test_invalidate_is_scoped_to_the_rejected_session() -> None:
    session = _text("edge_gateway/src/edge_gateway/crypto/session.py")
    invalidate = session.split("def invalidate(", 1)[1].split("def close", 1)[0]
    assert "session_id: str | None = None" in invalidate
    assert "session.session_id != session_id" in invalidate
