"""The Gateway crypto install uses locked Linux wheels and the verification image."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

import pytest


ROOT = Path(__file__).parents[2]
DOCKERFILE = ROOT / "edge_gateway" / "docker" / "crypto-image.Dockerfile"
CHECK_SCRIPT = ROOT / "edge_gateway" / "docker" / "check_crypto.py"
PLATFORMS = {
    "aarch64-unknown-linux-gnu": "aarch64",
    "x86_64-unknown-linux-gnu": "x86_64",
}


def _locked_version(name: str) -> str:
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    versions = [package["version"] for package in lock["package"] if package["name"] == name]
    assert len(versions) == 1
    return versions[0]


def _site_packages(environment: Path) -> Path:
    matches = list(environment.glob("lib/python3.12/site-packages"))
    assert len(matches) == 1
    return matches[0]


def _install(platform: str, environment: Path) -> None:
    completed = subprocess.run(
        [
            "uv",
            "sync",
            "--frozen",
            "--package",
            "edge-gateway",
            "--no-dev",
            "--python-platform",
            platform,
        ],
        cwd=ROOT,
        env={**os.environ, "UV_PROJECT_ENVIRONMENT": str(environment)},
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_crypto_check_script_passes_on_the_installed_gateway() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "crypto-install-ok"


@pytest.mark.parametrize(("platform", "architecture"), PLATFORMS.items())
def test_frozen_gateway_install_uses_linux_wheels(
    tmp_path: Path, platform: str, architecture: str
) -> None:
    """Linux Gateway installs use manylinux wheels for the native packages."""
    if sys.platform == "win32":
        pytest.skip("Linux virtualenv wheel layout is verified on Linux CI")
    environment = tmp_path / "venv"
    _install(platform, environment)
    site = _site_packages(environment)

    cryptography_info = site / f"cryptography-{_locked_version('cryptography')}.dist-info"
    cryptography_wheel = (cryptography_info / "WHEEL").read_text(encoding="utf-8")
    assert "Root-Is-Purelib: false" in cryptography_wheel
    assert "manylinux" in cryptography_wheel
    assert architecture in cryptography_wheel
    assert (cryptography_info / "INSTALLER").read_text(encoding="utf-8").strip() == "uv"
    assert list(site.glob("cryptography/**/_rust*.so"))

    for package, library in (("cffi", "_cffi_backend"), ("pydantic-core", "_pydantic_core")):
        info_name = package.replace("-", "_")
        info = site / f"{info_name}-{_locked_version(package)}.dist-info"
        wheel = (info / "WHEEL").read_text(encoding="utf-8")
        assert "manylinux" in wheel
        assert architecture in wheel
        assert list(site.rglob(f"{library}*{architecture}-linux-gnu.so"))


def test_verification_image_installs_frozen_wheels_without_a_compiler() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "python:3.12-slim-bookworm" in text
    assert "uv sync --frozen --package edge-gateway --no-dev" in text
    assert "check_crypto.py" in text
    for compiler in ("build-essential", "gcc", "rustc", "apt-get"):
        assert compiler not in text


def test_verification_image_runs_when_docker_is_available() -> None:
    """Build and run the image when a Docker client is installed."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    build = subprocess.run(
        [
            "docker",
            "build",
            "-f",
            str(DOCKERFILE),
            "-t",
            "gateway-crypto-check",
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert build.returncode == 0, build.stderr
    run = subprocess.run(
        ["docker", "run", "--rm", "gateway-crypto-check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr
    assert run.stdout.strip() == "crypto-install-ok"
