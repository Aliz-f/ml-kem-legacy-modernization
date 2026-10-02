"""Keep the Member 2 integration review anchored to the current Gateway."""

from pathlib import Path

ROOT = Path(__file__).parents[2]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_review_matches_dispatch_and_correlation() -> None:
    review = _text("edge_gateway/docs/member2-integration-review.md")
    app = _text("edge_gateway/src/edge_gateway/app.py")
    dispatch = _text("edge_gateway/src/edge_gateway/dispatch.py")
    measurements = _text("edge_gateway/src/edge_gateway/measurements.py")
    models = _text("edge_gateway/src/edge_gateway/models.py")
    correlation = _text("edge_gateway/src/edge_gateway/correlation.py")

    handler = app.split("async def measurements", 1)[1].split("@app.get", 1)[0]
    for term in ("SecureTransport", "encapsulate", "FAILURE_MODE", "baseline"):
        assert term not in handler
    ready = app.split("async def ready", 1)[1].split("@app.post", 1)[0]
    assert "session" not in ready
    assert "_unavailable()" in ready
    assert 'logger.error("event=gateway_internal_error component=edge_gateway")' in app
    assert "return UnavailableBaseline()" in app

    send = dispatch.split("async def send", 1)[1].split("async def _send_secure", 1)[0]
    assert '_mode == "classical"' in send
    assert "_baseline.send" in send
    secure = dispatch.split("except SecureTransportError", 1)[1]
    assert "_baseline" not in secure
    assert "pqc_fail_closed" in secure
    assert 'pqc_failure_policy != "fail_closed"' in dispatch

    canonical = models.split("class CanonicalMeasurement:", 1)[1].split("def __post_init__", 1)[0]
    assert "request_id" not in canonical
    assert 'return {"X-Request-ID": request_id}' in correlation
    assert "request_id = create_request_id()" in measurements
    assert "from None" in measurements
    assert "It does not change Gateway code." in review
    assert "It does not change the Gateway protocol." in _text("edge_gateway/README.md")


def test_review_matches_bounded_session_recovery() -> None:
    review = _text("edge_gateway/docs/member2-integration-review.md")
    transport = _text("edge_gateway/src/edge_gateway/crypto/secure_transport.py")
    send = transport.split("async def send", 1)[1].split("def _session_is_active", 1)[0]
    recover = transport.split("async def _recover", 1)[1].split("def _seal", 1)[0]

    assert send.count("_recover(") == 1
    assert "_recover(" not in recover
    assert "SESSION_INVALID" in transport
    assert "SESSION_EXPIRED" in transport
    assert "request_id=request_id" in send
    for sentence in (
        "CLOUD_UNAVAILABLE",
        "X-Request-ID",
        "fail_closed",
        "SESSION_EXPIRED",
        "does not require an already-active session",
        "FAILURE_MODE",
    ):
        assert sentence in review
