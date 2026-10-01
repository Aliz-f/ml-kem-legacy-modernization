"""Member 3 crypto work follows the repository AI-history workflow."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "ai-history.md"
README = ROOT / "edge_gateway" / "README.md"
SEQUENCE = (
    "start",
    "record important interactions",
    "agent completes implementation",
    "tests and static checks",
    "output",
    "human security review",
    "accepted, modified, or rejected",
    "revision when the decision is modified",
    "verification",
)
AREAS = {
    "Evaluate ML-KEM Python libraries": (
        "docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md",
        "Selected pyca/cryptography",
    ),
    "Implement ML-KEM wrapper": (
        "docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md",
        "encapsulate()",
    ),
    "Implement HKDF wrapper": (
        "docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md",
        "derive_session_key()",
    ),
    "Implement secure session manager": (
        "docs/ai/history/0011-gateway-secure-session-establishment.md",
        "in-memory Gateway secure session",
    ),
    "Implement AES-GCM wrapper": (
        "docs/ai/history/0019-gateway-aes-gcm-nonce-and-aad.md",
        "AES-256-GCM",
    ),
    "Implement secure envelope": (
        "docs/ai/history/0025-integrate-pr-10-secureenvelope-on-current-develop.md",
        "SecureEnvelope",
    ),
    "Implement secure Cloud transport": (
        "docs/ai/history/0047-gateway-secure-measurement-transport.md",
        "/api/v1/secure/measurements",
    ),
    "Implement crypto failure injection": (
        "docs/ai/history/0049-gateway-crypto-failure-injection.md",
        "crypto failure injector",
    ),
}


def test_crypto_ai_history_requires_human_review_before_acceptance() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert (
        "Generated Gateway crypto code is untrusted until a human "
        "security review accepts it."
    ) in document
    assert "Acceptance is not completion." in document
    assert "Automated checks do not replace human review." in document
    assert "An agent's own review does not replace human review." in document
    assert "docs/DEVELOPMENT_WORKFLOW.md" in document
    assert "docs/ai/README.md" in document
    assert "docs/architecture/ml-kem-library-decision.md" in document
    assert "does not implement those primitives" in document
    assert "continuous manual evaluation of AI-generated code" in document
    assert (
        "does not store private keys, ML-KEM shared secrets, session keys"
    ) in document

    block = document.split("```text\n", 1)[1].split("\n```", 1)[0]
    assert tuple(block.splitlines()) == SEQUENCE


def test_completed_crypto_records_match_the_workflow_areas() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    for area, (relative_path, marker) in AREAS.items():
        assert area in document
        assert f"`{relative_path}`" in document
        history = (ROOT / relative_path).read_text(encoding="utf-8")
        task_id = Path(relative_path).name.split("-", 1)[0]
        assert history.startswith(f"# AI Task {task_id} ")
        assert "**Status:** Complete" in history.split("---", 1)[0]
        assert marker in history


def test_readme_points_at_the_crypto_ai_history_workflow() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/ai-history.md" in readme
    assert "untrusted until a human security review" in readme
