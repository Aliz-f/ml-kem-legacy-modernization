# Build from the repository root: docker build -f cloud_service/Dockerfile .
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=9000 \
    DATABASE_URL=sqlite:////data/cloud.db

COPY pyproject.toml uv.lock README.md ./
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY cloud_service/src cloud_service/src

RUN uv sync --frozen --package cloud-service --no-dev --no-editable \
    && mkdir -p /data \
    && chown 10001:10001 /data

USER 10001:10001
EXPOSE 9000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:9000/ready', timeout=3).close()"
CMD ["cloud-service"]
