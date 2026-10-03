"""Keep key files, debug prints, and secret log arguments out of the repository."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[2]
SOURCES = ("edge_gateway/src", "cloud_service/src", "legacy_system/src")
SECRET_NAMES = ("shared_secret", "session_key", "private_key", "key_bytes", "plaintext")
# Tools and reports whose job is to print a result. None prints key material.
CLI_OUTPUT = {
    "cloud_service/tools/measure_baseline.py",
    "edge_gateway/docker/check_crypto.py",
    "edge_gateway/docker/clean_container_crypto.py",
    "edge_gateway/tests/test_gateway_baseline_integration.py",
    "scripts/measure_baseline_e2e.py",
    "scripts/measure_mode_comparison.py",
    "scripts/measure_modernized_e2e.py",
    "src/ai_history/cli.py",
}


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _tracked() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.splitlines()


def _python_files() -> list[tuple[str, Path]]:
    return [(path, ROOT / path) for path in _tracked() if path.endswith(".py")]


def test_no_key_or_env_files_are_tracked() -> None:
    risky = re.compile(r"\.(pem|key|der|p12|pfx)$|(^|/)\.env($|\.)|id_rsa")
    assert [path for path in _tracked() if risky.search(path)] == [".env.example"]


def test_no_private_key_blocks_or_debug_prints() -> None:
    pem = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
    debug = re.compile(r"^\s*(print\(|breakpoint\(|import pdb|pdb\.set_trace)", re.M)
    printing = set()
    for name, path in _python_files():
        text = path.read_text(encoding="utf-8")
        assert not pem.search(text), name
        if debug.search(text):
            printing.add(name)
    tracked_cli_output = CLI_OUTPUT.intersection(_tracked())
    assert printing == tracked_cli_output
    for name in tracked_cli_output:
        prints = re.findall(r"print\((.*)", _text(name))
        assert prints and not any(s in p for p in prints for s in SECRET_NAMES), name


def _log_calls(text: str) -> list[str]:
    """Return the full argument text of each log call, across lines."""
    calls = []
    for match in re.finditer(r"\b(?:logger\.\w+|log_security)\(", text):
        depth, end = 1, match.end()
        while depth and end < len(text):
            depth += {"(": 1, ")": -1}.get(text[end], 0)
            end += 1
        calls.append(text[match.end():end])
    return calls


def test_source_logs_do_not_receive_secret_material() -> None:
    for root in SOURCES:
        for path in (ROOT / root).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "exc_info" not in text and "logger.exception" not in text, path
            for arguments in _log_calls(text):
                for name in SECRET_NAMES:
                    assert name not in arguments, (path, arguments)
