"""The security-debt register matches the current Gateway and Cloud limits."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "technical-debt.md"
README = ROOT / "edge_gateway" / "README.md"
ROWS = (
    (
        "Simplified Cloud public-key trust",
        "MITM/key substitution risk",
        "TLS/PKI/key pinning",
    ),
    (
        "In-memory sessions",
        "restart loses state",
        "secure persistent session strategy",
    ),
    (
        "Ephemeral Cloud key",
        "identity changes on restart",
        "persistent secure key storage",
    ),
    (
        "No HSM",
        "keys remain process-memory software keys",
        "HSM/KMS",
    ),
    (
        "No dedicated cryptographic anti-replay counter/window",
        "authenticated envelopes can be replayed at crypto layer",
        "per-session counters / replay window",
    ),
    (
        "Application-level crypto over test HTTP",
        "no transport identity",
        "TLS/mTLS",
    ),
    (
        "Simple key rotation",
        "limited lifecycle",
        "automated rotation",
    ),
    (
        "Python memory cannot guarantee zeroization",
        "residual key-memory risk",
        "lower-level secure key handling",
    ),
)


def test_security_debt_records_each_limit_risk_and_future_step() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert (
        "These future improvements are recorded only. This course system "
        "does not add TLS, a persistent session store, an HSM, a replay "
        "window, or automated key rotation."
    ) in document
    assert (
        "Cloud business idempotency prevents duplicate logical rows, but "
        "it is not a replacement for cryptographic replay protection."
    ) in document
    for debt, risk, improvement in ROWS:
        assert f"| {debt} | {risk} | {improvement} |" in document


def test_readme_points_at_the_security_debt_register() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/technical-debt.md" in readme
    assert "does not add those future controls" in readme


def test_recorded_debt_still_matches_the_implementations() -> None:
    gateway_session = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/session.py"
    ).read_text(encoding="utf-8")
    cloud_session = (
        ROOT / "cloud_service/src/cloud_service/crypto/session.py"
    ).read_text(encoding="utf-8")
    cloud_keys = (ROOT / "cloud_service/src/cloud_service/crypto/keys.py").read_text(
        encoding="utf-8"
    )
    envelope = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/envelope.py"
    ).read_text(encoding="utf-8")

    assert "process memory" in gateway_session
    assert "guarantee secure memory zeroization" in gateway_session
    assert "no persistence, counters or replay window" in cloud_session
    assert "ephemeral key pair" in cloud_keys
    assert "uuid4" in cloud_keys
    assert "message_counter" not in envelope
