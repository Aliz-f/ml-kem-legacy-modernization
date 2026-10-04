"""The repository quality workflow runs the Gateway crypto suites by name."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github/workflows/ai-history.yml"

# These paths are the Member 3 suites. Full pytest still runs every other test.
CRYPTO_SUITES = (
    "edge_gateway/tests/test_mlkem.py",
    "edge_gateway/tests/test_kdf.py",
    "edge_gateway/tests/test_symmetric.py",
    "edge_gateway/tests/test_secure_envelope.py",
    "edge_gateway/tests/test_crypto_review_checklist.py",
    "edge_gateway/tests/test_transport_trust.py",
    "edge_gateway/tests/test_security_logging.py",
    "edge_gateway/tests/test_secure_transport.py",
    "tests/integration/test_secure_message_tamper.py",
    "tests/integration/test_gateway_cloud_secure.py",
)


def test_quality_workflow_names_the_gateway_crypto_suites() -> None:
    """The split unit-test job retains the named Gateway crypto suites."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    unit_tests = workflow.index("  unit-tests:")
    crypto_step = workflow.index("name: Run Gateway crypto checks")
    integration_tests = workflow.index("  integration-tests:")
    assert unit_tests < crypto_step < integration_tests
    for path in CRYPTO_SUITES:
        assert (ROOT / path).is_file()
        assert workflow.index(path, crypto_step) > crypto_step
