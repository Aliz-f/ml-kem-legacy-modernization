"""Process-local application metrics with fixed names and no dynamic labels."""

from contextlib import contextmanager
from threading import Lock
from time import perf_counter


COUNTERS = {
    "measurements_received": "Legacy requests received.",
    "measurements_accepted": "Measurements accepted for Cloud delivery by local policy.",
    "measurements_rejected": "Legacy requests rejected by size, validation or sequence policy.",
    "duplicate_measurements": "Equal sequence rejections.",
    "out_of_order_measurements": "Lower sequence rejections.",
    "sequence_gaps": "Accepted measurements revealing a sequence gap.",
    "cloud_requests": "Cloud measurement send attempts, including injected failures.",
    "cloud_failures": "Cloud measurement attempts without valid acceptance.",
    "cloud_retries": "Ordinary Cloud transport retry attempts, excluding session recovery.",
}


class GatewayMetrics:
    """Share one registry between the ASGI loop and Cloud worker threads."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._counts = dict.fromkeys(COUNTERS, 0)
        self._duration_sum = 0.0
        self._duration_count = 0

    def increment(self, name: str) -> None:
        # Unknown names cannot create new series or leak request data.
        with self._lock:
            if name not in self._counts:
                raise ValueError("Unknown Gateway metric")
            self._counts[name] += 1

    @contextmanager
    def cloud_attempt(self):
        """Time one attempt, excluding backoff, handshake and encryption."""
        self.increment("cloud_requests")
        started = perf_counter()
        try:
            yield
        except Exception:
            self.increment("cloud_failures")
            raise
        finally:
            elapsed = perf_counter() - started
            with self._lock:
                self._duration_sum += elapsed
                self._duration_count += 1

    def render(self) -> str:
        """Render a consistent Prometheus snapshot without identifiers or secrets."""
        with self._lock:
            counts = self._counts.copy()
            total, count = self._duration_sum, self._duration_count
        lines = []
        for name, help_text in COUNTERS.items():
            metric = f"gateway_{name}_total"
            lines.extend((f"# HELP {metric} {help_text}", f"# TYPE {metric} counter",
                          f"{metric} {counts[name]}"))
        metric = "gateway_cloud_request_duration_seconds"
        lines.extend((f"# HELP {metric} Cloud measurement attempt duration.",
                      f"# TYPE {metric} summary", f"{metric}_sum {total:.9f}",
                      f"{metric}_count {count}"))
        return "\n".join(lines) + "\n"
