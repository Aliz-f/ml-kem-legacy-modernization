"""Small process-local Prometheus metrics for the Cloud Service.

Metric labels are intentionally limited to finite protocol and operational
outcomes.  Identifiers and measurement values are never labels.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable


class CloudMetrics:
    """Collect bounded counters, gauges, and request-duration observations."""

    def __init__(self) -> None:
        self._counters: defaultdict[tuple[str, tuple[tuple[str, str], ...]], int] = defaultdict(int)
        self._gauges: dict[str, int] = {"cloud_active_sessions": 0}
        self._duration_count = 0
        self._duration_sum = 0.0
        self._decapsulation_count = 0
        self._decapsulation_sum = 0.0

    def increment(self, name: str, /, **labels: str) -> None:
        if name not in _COUNTER_FAMILIES:
            raise ValueError("metric is not a frozen Cloud counter family")
        self._counters[(name, _labels(labels.items()))] += 1

    def set_active_sessions(self, count: int) -> None:
        self._gauges["cloud_active_sessions"] = count

    def observe_request_duration(self, seconds: float) -> None:
        self._duration_count += 1
        self._duration_sum += seconds

    def observe_decapsulation_duration(self, seconds: float) -> None:
        self._decapsulation_count += 1
        self._decapsulation_sum += seconds

    def failure_injected(self, failure_type: str) -> None:
        self.increment("cloud_injected_failures_total", failure_type=failure_type)

    def render(self) -> str:
        """Render the frozen Cloud metric families in Prometheus text format."""
        lines = [
            "# TYPE cloud_request_duration_seconds summary",
            f"cloud_request_duration_seconds_count {self._duration_count}",
            f"cloud_request_duration_seconds_sum {self._duration_sum}",
            "# TYPE cloud_mlkem_decapsulation_duration_seconds summary",
            f"cloud_mlkem_decapsulation_duration_seconds_count {self._decapsulation_count}",
            f"cloud_mlkem_decapsulation_duration_seconds_sum {self._decapsulation_sum}",
        ]
        families = {name: {()} for name in _COUNTER_FAMILIES}
        for name, labels in self._counters:
            families.setdefault(name, set()).add(labels)
        for name in sorted(families):
            lines.append(f"# TYPE {name} counter")
            for labels in sorted(families[name]):
                lines.append(f"{name}{_render_labels(labels)} {self._counters[(name, labels)]}")
        for name, value in sorted(self._gauges.items()):
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {value}")
        return "\n".join(lines) + "\n"


def _labels(items: Iterable[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    """Accept only the finite label vocabulary defined by the metrics contract."""
    allowed = {
        "result": {"accepted", "already_accepted", "rejected", "failed"},
        "failure_type": {
            "public_key_unavailable", "mlkem_decapsulation_failure", "session_not_found",
            "session_expired", "decryption_failure", "storage_failure", "processing_delay",
            "service_unavailable", "drop_response",
        },
    }
    result: list[tuple[str, str]] = []
    for name, value in items:
        if name not in allowed or value not in allowed[name]:
            raise ValueError("metric label is not in the bounded Cloud vocabulary")
        result.append((name, value))
    return tuple(sorted(result))


_COUNTER_FAMILIES = frozenset({
    "cloud_baseline_requests_total",
    "cloud_secure_requests_total",
    "cloud_secure_requests_rejected_total",
    "cloud_mlkem_sessions_created_total",
    "cloud_mlkem_session_failures_total",
    "cloud_expired_sessions_total",
    "cloud_authenticated_messages_total",
    "cloud_decryption_failures_total",
    "cloud_measurements_stored_total",
    "cloud_duplicate_measurements_total",
    "cloud_storage_failures_total",
    "cloud_injected_failures_total",
})


def _render_labels(labels: tuple[tuple[str, str], ...]) -> str:
    if not labels:
        return ""
    joined = ",".join(f'{name}="{value}"' for name, value in labels)
    return "{" + joined + "}"
