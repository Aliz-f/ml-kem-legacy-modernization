"""One clean-image Gateway and Cloud complete an ML-KEM measurement."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).parents[2]
DOCKERFILE = ROOT / "edge_gateway" / "docker" / "clean-container.Dockerfile"
SCRIPT = ROOT / "edge_gateway" / "docker" / "clean_container_crypto.py"


def test_clean_container_script_stores_one_secure_measurement() -> None:
    """The container entrypoint performs one handshake and stores one row."""
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "clean-container-ok"


def test_clean_container_image_installs_from_the_frozen_lock() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "python:3.12-slim-bookworm" in text
    assert "uv sync --frozen --package edge-gateway --package cloud-service --no-dev --no-editable" in text
    assert "clean_container_crypto.py" in text
    assert "COPY .venv" not in text
    for compiler in ("build-essential", "gcc", "rustc", "apt-get"):
        assert compiler not in text


def test_clean_container_image_runs_when_docker_is_available() -> None:
    """Build and run the image when a Docker client is installed."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not installed")
    build = subprocess.run(
        ["docker", "build", "-f", str(DOCKERFILE), "-t", "gateway-clean-container", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert build.returncode == 0, build.stderr
    run = subprocess.run(
        ["docker", "run", "--rm", "gateway-clean-container"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    assert run.returncode == 0, run.stderr
    assert run.stdout.strip() == "clean-container-ok"
