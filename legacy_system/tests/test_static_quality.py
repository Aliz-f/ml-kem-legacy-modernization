"""Static quality and hygiene verification for Legacy Device."""

import ast
import re
from pathlib import Path

LEGACY_ROOT = Path(__file__).parents[1]
SRC_DIR = LEGACY_ROOT / "src"


def test_no_keys_or_env_files_in_legacy_system() -> None:
    """Verify no accidental secrets, private keys, or .env files exist in legacy_system."""
    risky_patterns = [
        re.compile(r"\.(pem|key|der|p12|pfx)$"),
        re.compile(r"(^|/)\.env($|\.)"),
        re.compile(r"id_rsa"),
    ]
    for path in LEGACY_ROOT.rglob("*"):
        if path.is_file():
            rel = path.relative_to(LEGACY_ROOT).as_posix()
            for pattern in risky_patterns:
                assert not pattern.search(rel), f"Risky file found in legacy_system: {rel}"


def test_no_debug_prints_or_breakpoints_in_legacy_src() -> None:
    """Verify that legacy_system/src contains no breakpoint, pdb, or rogue print calls."""
    debug_call_names = {"breakpoint", "print"}
    for py_file in SRC_DIR.rglob("*.py"):
        code = py_file.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in debug_call_names:
                    raise AssertionError(
                        f"Forbidden debug call '{node.func.id}()' found in {py_file}:{node.lineno}"
                    )
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "pdb", f"Forbidden import 'pdb' found in {py_file}:{node.lineno}"
            elif isinstance(node, ast.ImportFrom):
                assert node.module != "pdb", f"Forbidden import from 'pdb' found in {py_file}:{node.lineno}"


def test_no_private_key_blocks_in_legacy_files() -> None:
    """Verify that no file in legacy_system contains PEM private key headers."""
    pem_pattern = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
    for py_file in LEGACY_ROOT.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert not pem_pattern.search(text), f"PEM private key block found in {py_file}"


def test_no_cloud_or_crypto_imports_in_legacy_src() -> None:
    """Enforce ownership boundary: legacy_system must never import cloud or pqc/crypto modules."""
    forbidden_modules = {"cloud_service", "edge_gateway.crypto", "cryptography", "oqs"}
    for py_file in SRC_DIR.rglob("*.py"):
        code = py_file.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert not alias.name.startswith(forbidden), (
                            f"Forbidden cross-boundary import '{alias.name}' in {py_file}:{node.lineno}"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for forbidden in forbidden_modules:
                        assert not node.module.startswith(forbidden), (
                            f"Forbidden cross-boundary import '{node.module}' in {py_file}:{node.lineno}"
                        )


def test_legacy_architecture_operations_documentation_exists() -> None:
    """Verify that legacy_system/docs/architecture-operations.md exists and is non-empty."""
    doc_path = LEGACY_ROOT / "docs" / "architecture-operations.md"
    assert doc_path.is_file(), f"Expected documentation file at {doc_path}"
    assert doc_path.stat().st_size > 0, f"Expected non-empty documentation file at {doc_path}"


def test_legacy_ai_decisions_register_exists() -> None:
    """Verify that legacy_system/docs/ai-decisions.md exists and is non-empty."""
    doc_path = LEGACY_ROOT / "docs" / "ai-decisions.md"
    assert doc_path.is_file(), f"Expected AI decision register at {doc_path}"
    assert doc_path.stat().st_size > 0, f"Expected non-empty AI decision register at {doc_path}"


def test_legacy_technical_debt_register_exists() -> None:
    """Verify that legacy_system/docs/technical-debt.md exists and is non-empty."""
    doc_path = LEGACY_ROOT / "docs" / "technical-debt.md"
    assert doc_path.is_file(), f"Expected technical debt register at {doc_path}"
    assert doc_path.stat().st_size > 0, f"Expected non-empty technical debt register at {doc_path}"
