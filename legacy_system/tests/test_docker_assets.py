"""M1-13 static Legacy Device Dockerfile and packaging contract checks."""

import importlib
from pathlib import Path
import tomllib

LEGACY_ROOT = Path(__file__).parents[1]
DOCKERFILE = LEGACY_ROOT / "Dockerfile"
PYPROJECT = LEGACY_ROOT / "pyproject.toml"


def test_legacy_dockerfile_exists_and_uses_frozen_python_base() -> None:
    assert DOCKERFILE.is_file(), f"Expected Dockerfile to exist at {DOCKERFILE}"
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python:3.12-slim-bookworm" in content
    assert "COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv" in content


def test_legacy_dockerfile_uses_frozen_uv_sync() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "UV_LINK_MODE=copy" in content
    assert "UV_PROJECT_ENVIRONMENT=/app/.venv" in content
    assert 'PATH="/app/.venv/bin:${PATH}"' in content
    assert "RUN uv sync --frozen --package legacy-system --no-dev --no-editable" in content


def test_legacy_dockerfile_non_root_and_stopsignal() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "USER 10001:10001" in content
    assert "STOPSIGNAL SIGTERM" in content


def test_legacy_dockerfile_does_not_expose_ports() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    expose_lines = [line for line in lines if line.startswith("EXPOSE")]
    assert not expose_lines, (
        f"Legacy Device is strictly an outbound client and must not expose ports: {expose_lines}"
    )


def test_legacy_dockerfile_command_invokes_entrypoint() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert 'CMD ["python", "-m", "legacy_system.main"]' in content


def test_legacy_pyproject_registers_console_script() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    assert "legacy-device" in scripts
    entry_point = scripts["legacy-device"]
    assert entry_point == "legacy_system.main:main"

    module_name, func_name = entry_point.split(":")
    mod = importlib.import_module(module_name)
    func = getattr(mod, func_name)
    assert callable(func)
