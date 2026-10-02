"""Keep the dependency review anchored to the lock file and crypto source."""

import re
from pathlib import Path

ROOT = Path(__file__).parents[2]
SOURCES = ("edge_gateway/src", "cloud_service/src", "legacy_system/src")
OTHER_CRYPTO = (
    "pycryptodome", "pycryptodomex", "pynacl", "liboqs-python",
    "pqcrypto", "kyber-py", "quantcrypt",
)


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _locked() -> dict[str, str]:
    pairs = re.findall(r'^name = "([^"]+)"\nversion = "([^"]+)"', _text("uv.lock"), re.M)
    return dict(pairs)


def _source_files() -> list[Path]:
    return [path for root in SOURCES for path in (ROOT / root).rglob("*.py")]


def test_one_crypto_library_is_locked() -> None:
    locked = _locked()
    review = _text("edge_gateway/docs/dependency-review.md")

    assert f"`cryptography` {locked['cryptography']}" in review
    assert f"`cffi` {locked['cffi']}" in review
    for name in OTHER_CRYPTO:
        assert name not in locked
    for component in ("edge_gateway", "cloud_service"):
        assert '"cryptography>=48"' in _text(f"{component}/pyproject.toml")


def test_source_imports_only_the_reviewed_crypto_api() -> None:
    imports = re.compile(r"^\s*(?:from|import)\s+([\w.]+)", re.M)
    for path in _source_files():
        for module in imports.findall(path.read_text(encoding="utf-8")):
            top = module.split(".")[0]
            assert top not in {"Crypto", "Cryptodome", "nacl", "oqs", "pqcrypto",
                               "kyber", "quantcrypt", "ctypes", "ssl", "pickle"}, path
            if top == "cryptography":
                assert module == "cryptography.exceptions" or module.startswith(
                    "cryptography.hazmat.primitives"
                ), path


def test_random_module_is_not_a_key_or_nonce_source() -> None:
    users = {
        str(path.relative_to(ROOT))
        for path in _source_files()
        if re.search(r"^import random$", path.read_text(encoding="utf-8"), re.M)
    }
    assert users == {
        "edge_gateway/src/edge_gateway/crypto/failure.py",
        "edge_gateway/src/edge_gateway/failure/injector.py",
        "cloud_service/src/cloud_service/failure/injector.py",
        "legacy_system/src/legacy_system/sensor.py",
        "legacy_system/src/legacy_system/failure.py",
    }
    assert "secrets.token_bytes(NONCE_LENGTH)" in _text(
        "edge_gateway/src/edge_gateway/crypto/symmetric.py"
    )
