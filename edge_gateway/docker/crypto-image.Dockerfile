# Verification image for the Gateway crypto install.
# The service image remains edge_gateway/Dockerfile (Member 2, M2-49).
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /src
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/src/.venv \
    PATH="/src/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml uv.lock ./
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY edge_gateway/src edge_gateway/src
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY edge_gateway/docker/check_crypto.py /opt/check_crypto.py

# Bookworm provides glibc. The frozen lock supplies manylinux wheels, so this
# image installs cryptography without a compiler. A missing wheel fails the build.
RUN uv sync --frozen --package edge-gateway --no-dev

CMD ["python", "/opt/check_crypto.py"]
