"""Local operations dashboard for the Compose demonstration stack."""

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
RUNTIME_CONFIG = {
    "legacy-device": frozenset(
        {"FAILURE_MODE", "FAILURE_RATE", "FAILURE_SEED", "LOG_LEVEL"}
    ),
    "edge-gateway": frozenset(
        {
            "FAILURE_MODE",
            "FAILURE_RATE",
            "FAILURE_SEED",
            "FAILURE_DELAY_SECONDS",
            "LOG_LEVEL",
        }
    ),
    "cloud-service": frozenset(
        {
            "FAILURE_MODE",
            "FAILURE_RATE",
            "FAILURE_SEED",
            "FAILURE_DELAY_SECONDS",
            "LOG_LEVEL",
        }
    ),
}
FAILURE_MODES = {
    "legacy-device": frozenset(
        {
            "none",
            "invalid_temperature",
            "invalid_humidity",
            "missing_field",
            "invalid_timestamp",
            "duplicate_sequence",
            "out_of_order_sequence",
            "random",
        }
    ),
    "edge-gateway": frozenset(
        {
            "none",
            "processing_error",
            "processing_delay",
            "cloud_timeout",
            "cloud_unavailable",
            "drop_message",
            "random",
            "mlkem_handshake_failure",
            "corrupt_ciphertext",
            "session_missing",
            "session_expired",
        }
    ),
    "cloud-service": frozenset(
        {
            "none",
            "public_key_unavailable",
            "mlkem_decapsulation_failure",
            "session_not_found",
            "session_expired",
            "decryption_failure",
            "storage_failure",
            "processing_delay",
            "service_unavailable",
            "drop_response",
            "random",
        }
    ),
}
LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
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


def _docker(path: str, method: str = "GET", payload: object | None = None) -> tuple[int, bytes]:
    body = b"" if payload is None else json.dumps(payload).encode()
    request = (
        f"{method} {path} HTTP/1.1\r\nHost: docker\r\nConnection: close\r\n"
        f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n"
    ).encode() + body
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


def _validated_runtime_config(service: str, values: object) -> dict[str, str]:
    """Validate the small dashboard-owned runtime override surface."""
    if service not in RUNTIME_CONFIG or not isinstance(values, dict):
        raise ValueError("Invalid runtime configuration request")
    if set(values) != RUNTIME_CONFIG[service] or not all(
        isinstance(value, str) for value in values.values()
    ):
        raise ValueError("Only the approved runtime settings may be changed")

    mode = values["FAILURE_MODE"]
    if mode not in FAILURE_MODES[service]:
        raise ValueError("Unsupported failure mode")
    try:
        rate = float(values["FAILURE_RATE"])
    except ValueError as error:
        raise ValueError("FAILURE_RATE must be a number from 0 to 1") from error
    if not 0 <= rate <= 1 or rate in (float("inf"), float("-inf")):
        raise ValueError("FAILURE_RATE must be a number from 0 to 1")
    seed = values["FAILURE_SEED"].strip()
    if seed:
        try:
            int(seed)
        except ValueError as error:
            raise ValueError("FAILURE_SEED must be an integer or empty") from error
    if values["LOG_LEVEL"].upper() not in LOG_LEVELS:
        raise ValueError("Unsupported log level")
    normalized = {
        "FAILURE_MODE": mode,
        "FAILURE_RATE": str(rate),
        "FAILURE_SEED": seed,
        "LOG_LEVEL": values["LOG_LEVEL"].upper(),
    }
    if "FAILURE_DELAY_SECONDS" in values:
        try:
            delay = float(values["FAILURE_DELAY_SECONDS"])
        except ValueError as error:
            raise ValueError("FAILURE_DELAY_SECONDS must be a number from 0 to 30") from error
        if not 0 <= delay <= 30 or delay in (float("inf"), float("-inf")):
            raise ValueError("FAILURE_DELAY_SECONDS must be a number from 0 to 30")
        normalized["FAILURE_DELAY_SECONDS"] = str(delay)
    return normalized


def _replace_environment(
    values: list[str], overrides: dict[str, str]
) -> list[str]:
    result, remaining = [], dict(overrides)
    for value in values:
        name, separator, setting = value.partition("=")
        if name in remaining:
            result.append(f"{name}={remaining.pop(name)}")
        else:
            result.append(f"{name}{separator}{setting}" if separator else value)
    return result + [f"{name}={value}" for name, value in sorted(remaining.items())]


def _networking_config(inspect: dict[str, object]) -> dict[str, object]:
    networks = inspect.get("NetworkSettings", {}).get("Networks", {})
    endpoints = {
        name: {"Aliases": value.get("Aliases") or []}
        for name, value in networks.items()
    }
    return {"EndpointsConfig": endpoints}


def _restart_with_runtime_config(service: str, overrides: dict[str, str]) -> None:
    container = _container(service)
    if container is None:
        raise ValueError("Container not found")
    status, body = _docker(f"/containers/{container['Id']}/json")
    if status != 200:
        raise ValueError("Container inspection failed")
    inspect = json.loads(body)
    config = dict(inspect["Config"])
    config["Env"] = _replace_environment(config.get("Env", []), overrides)
    config["HostConfig"] = inspect["HostConfig"]
    config["NetworkingConfig"] = _networking_config(inspect)
    name = quote(str(inspect["Name"]).lstrip("/"), safe="")
    status, _ = _docker(f"/containers/{container['Id']}?force=true", "DELETE")
    if status not in (204, 404):
        raise ValueError("Container could not be replaced")
    status, body = _docker(f"/containers/create?name={name}", "POST", config)
    if status != 201:
        raise ValueError("Replacement container could not be created")
    container_id = json.loads(body)["Id"]
    status, _ = _docker(f"/containers/{container_id}/start", "POST")
    if status not in (204, 304):
        raise ValueError("Replacement container could not be started")


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

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/runtime-config":
            self.send_error(404)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(content_length))
            if request.get("confirm") is not True:
                raise ValueError("Restart confirmation is required")
            service = request.get("service")
            if not isinstance(service, str):
                raise ValueError("Unknown service")
            values = _validated_runtime_config(service, request.get("values"))
            _restart_with_runtime_config(service, values)
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
            self._json({"ok": False, "error": str(error)}, HTTPStatus.BAD_REQUEST)
            return
        self._json(
            {
                "ok": True,
                "message": (
                    f"{service} was restarted with temporary runtime overrides. "
                    "A Compose recreate restores the configured defaults."
                ),
            }
        )

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
