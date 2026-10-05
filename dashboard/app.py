"""Read-only local operations dashboard for the Compose demonstration stack."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

STATIC_DIR = Path(__file__).with_name("static")
DOCKER_SOCKET = os.environ.get("DOCKER_SOCKET", "/var/run/docker.sock")
SERVICE_URLS = {
    "edge-gateway": "http://edge-gateway:8000",
    "cloud-service": "http://cloud-service:9000",
}
SERVICES = ("legacy-device", "edge-gateway", "cloud-service")
SAFE_CONFIG = {
    "legacy-device": frozenset(
        {
            "DEVICE_ID",
            "GATEWAY_URL",
            "SEND_INTERVAL_SECONDS",
            "REQUEST_TIMEOUT_SECONDS",
            "MAX_RETRIES",
            "FAILURE_MODE",
            "FAILURE_RATE",
            "FAILURE_SEED",
            "LOG_LEVEL",
        }
    ),
    "edge-gateway": frozenset(
        {
            "GATEWAY_ID",
            "CLOUD_URL",
            "CLOUD_TIMEOUT_SECONDS",
            "CLOUD_MAX_RETRIES",
            "SECURITY_MODE",
            "SESSION_TTL_SECONDS",
            "PQC_FAILURE_POLICY",
            "FAILURE_MODE",
            "FAILURE_RATE",
            "FAILURE_SEED",
            "FAILURE_DELAY_SECONDS",
            "LOG_LEVEL",
        }
    ),
    "cloud-service": frozenset(
        {
            "CLOUD_ID",
            "DATABASE_URL",
            "SECURITY_MODE",
            "SESSION_TTL_SECONDS",
            "FAILURE_MODE",
            "FAILURE_RATE",
            "FAILURE_SEED",
            "FAILURE_DELAY_SECONDS",
            "LOG_LEVEL",
        }
    ),
}


def _http(url: str, text: bool = False) -> dict[str, object]:
    try:
        with urlopen(url, timeout=2) as response:  # noqa: S310 - fixed Compose URLs
            data = response.read().decode() if text else json.load(response)
            return {"ok": True, "status": response.status, "data": data}
    except HTTPError as error:
        return {"ok": False, "status": error.code, "error": "HTTP request failed"}
    except (URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {"ok": False, "error": "Service unavailable"}


def _docker(path: str) -> tuple[int, bytes]:
    request = (
        f"GET {path} HTTP/1.1\r\nHost: docker\r\nConnection: close\r\n\r\n".encode()
    )
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(2)
        client.connect(DOCKER_SOCKET)
        client.sendall(request)
        response = bytearray()
        while chunk := client.recv(65536):
            response.extend(chunk)
    headers, _, body = bytes(response).partition(b"\r\n\r\n")
    try:
        status = int(headers.split(b"\r\n", 1)[0].split()[1])
    except (IndexError, ValueError):
        return 502, b""
    if b"transfer-encoding: chunked" in headers.lower():
        body = _decode_chunks(body)
    return status, body


def _decode_chunks(body: bytes) -> bytes:
    """Decode the chunked transfer encoding used by Docker Desktop's API."""
    decoded = bytearray()
    remainder = body
    while remainder:
        size_line, marker, remainder = remainder.partition(b"\r\n")
        if not marker:
            return body
        try:
            size = int(size_line.split(b";", 1)[0], 16)
        except ValueError:
            return body
        if size == 0:
            return bytes(decoded)
        if len(remainder) < size + 2:
            return body
        decoded.extend(remainder[:size])
        remainder = remainder[size + 2 :]
    return body


def _container(service: str) -> dict[str, object] | None:
    filters = quote(json.dumps({"label": [f"com.docker.compose.service={service}"]}))
    status, body = _docker(f"/containers/json?all=1&filters={filters}")
    containers = json.loads(body) if status == 200 else []
    return containers[0] if containers else None


def _safe_environment(values: list[str], service: str) -> dict[str, str]:
    allowed, result = SAFE_CONFIG[service], {}
    for value in values:
        name, separator, setting = value.partition("=")
        if separator and name in allowed:
            result[name] = setting
    return dict(sorted(result.items()))


def _container_info(service: str) -> dict[str, object]:
    try:
        container = _container(service)
        if container is None:
            return {"available": False, "error": "Container not found"}
        status, body = _docker(f"/containers/{container['Id']}/json")
        if status != 200:
            return {"available": False, "error": "Container inspection failed"}
        inspect = json.loads(body)
        state = inspect.get("State", {})
        return {
            "available": True,
            "id": container["Id"],
            "state": state.get("Status", "unknown"),
            "health": state.get("Health", {}).get("Status"),
            "config": _safe_environment(
                inspect.get("Config", {}).get("Env", []), service
            ),
        }
    except (OSError, ValueError, json.JSONDecodeError, KeyError):
        return {"available": False, "error": "Docker information unavailable"}


def _decode_logs(body: bytes) -> str:
    lines, offset = [], 0
    while offset + 8 <= len(body) and body[offset] in (0, 1, 2):
        end = offset + 8 + int.from_bytes(body[offset + 4 : offset + 8], "big")
        if end > len(body):
            break
        lines.append(body[offset + 8 : end])
        offset = end
    return (b"".join(lines) if lines and offset == len(body) else body).decode(
        "utf-8", errors="replace"
    )


def _logs(service: str) -> dict[str, object]:
    try:
        container = _container(service)
        if container is None:
            return {"ok": False, "error": "Container not found"}
        status, body = _docker(
            f"/containers/{container['Id']}/logs?stdout=true&stderr=true&tail=100&timestamps=true"
        )
        return (
            {"ok": True, "data": _decode_logs(body)}
            if status == 200
            else {"ok": False, "error": "Logs unavailable"}
        )
    except (OSError, ValueError, json.JSONDecodeError, KeyError):
        return {"ok": False, "error": "Logs unavailable"}


def _overview() -> dict[str, object]:
    services = {name: _container_info(name) for name in SERVICES}
    for name, base in SERVICE_URLS.items():
        services[name]["health_endpoint"] = _http(f"{base}/health")
        services[name]["ready_endpoint"] = _http(f"{base}/ready")
    services["legacy-device"].update(
        health_endpoint={"ok": False, "error": "No HTTP health endpoint"},
        ready_endpoint={"ok": False, "error": "No HTTP readiness endpoint"},
    )
    return {
        "services": services,
        "metrics": {
            name: _http(f"{base}/metrics", True) for name, base in SERVICE_URLS.items()
        },
        "measurements": _http(
            "http://cloud-service:9000/api/v1/measurements?limit=100"
        ),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/overview":
            self._json(_overview())
            return
        if parsed.path == "/api/logs":
            service = parse_qs(parsed.query).get("service", [""])[0]
            self._json(
                _logs(service)
                if service in SERVICES
                else {"ok": False, "error": "Unknown service"},
                HTTPStatus.OK if service in SERVICES else HTTPStatus.BAD_REQUEST,
            )
            return
        target = (
            STATIC_DIR
            / ("index.html" if parsed.path == "/" else parsed.path.lstrip("/"))
        ).resolve()
        if (
            STATIC_DIR not in target.parents and target != STATIC_DIR
        ) or not target.is_file():
            self.send_error(404)
            return
        content_type = {".css": "text/css", ".js": "application/javascript"}.get(
            target.suffix, "text/html"
        )
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(target.read_bytes())

    def _json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, _format: str, *_args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(
        ("0.0.0.0", int(os.environ.get("DASHBOARD_PORT", "8080"))), DashboardHandler
    ).serve_forever()
