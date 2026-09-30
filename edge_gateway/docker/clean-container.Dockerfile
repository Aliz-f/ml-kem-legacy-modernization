# Clean image for one Gateway-to-Cloud ML-KEM measurement.
# The service images remain edge_gateway/Dockerfile and cloud_service/Dockerfile.
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
COPY cloud_service/src cloud_service/src
COPY edge_gateway/docker/clean_container_crypto.py /opt/clean_container_crypto.py

# Install from the frozen lock into this image. No host virtualenv is copied.
RUN uv sync --frozen --package edge-gateway --package cloud-service --no-dev --no-editable

CMD ["python", "/opt/clean_container_crypto.py"]
