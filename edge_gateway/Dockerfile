# Build from the repository root: docker build -f edge_gateway/Dockerfile .
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000

COPY pyproject.toml uv.lock README.md ./
COPY legacy_system/pyproject.toml legacy_system/pyproject.toml
COPY edge_gateway/pyproject.toml edge_gateway/pyproject.toml
COPY cloud_service/pyproject.toml cloud_service/pyproject.toml
COPY edge_gateway/src edge_gateway/src

RUN uv sync --frozen --package edge-gateway --no-dev --no-editable

USER 10001:10001
EXPOSE 8000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=3).close()"
CMD ["edge-gateway"]
