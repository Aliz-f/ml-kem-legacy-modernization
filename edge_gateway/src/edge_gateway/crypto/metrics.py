"""In-memory Gateway PQC metrics.

Labels are a fixed set: ``result``, ``reason``, ``failure_type``, and ``phase``.
Request IDs, session IDs, device IDs, and key IDs are not labels.
``gateway_pqc_fallback_total`` has no increment path.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

HANDSHAKE_REASONS = ("injected", "transport", "rejected", "cryptographic", "unexpected")
INJECTED_FAILURES = (
    "processing_error",
    "processing_delay",
    "cloud_timeout",
    "cloud_unavailable",
    "drop_message",
    "mlkem_handshake_failure",
    "corrupt_ciphertext",
    "session_missing",
    "session_expired",
)
MESSAGE_PHASES = ("first", "steady")
_RESULTS = ("success", "failure")


@dataclass(slots=True)
class _Duration:
    total_seconds: float = 0.0
    count: int = 0

    def observe(self, seconds: float) -> None:
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
            return
        if not math.isfinite(seconds) or seconds < 0:
            return
        self.total_seconds += float(seconds)
        self.count += 1


@dataclass(slots=True)
class PqcMetrics:
    """Aggregate PQC counters for one Gateway process."""

    mlkem_handshake_failures_total: int = 0
    handshakes_succeeded: int = 0
    handshake_failures: dict[str, int] = field(
        default_factory=lambda: {reason: 0 for reason in HANDSHAKE_REASONS}
    )
    handshake_duration: _Duration = field(default_factory=_Duration)
    public_key_duration: _Duration = field(default_factory=_Duration)
    encapsulation_duration: _Duration = field(default_factory=_Duration)
    reestablishments: dict[str, int] = field(
        default_factory=lambda: {result: 0 for result in _RESULTS}
    )
    active_session: int = 0
    encryption_failures_total: int = 0
    pqc_fallback_total: int = 0
    injected_failures: dict[str, int] = field(
        default_factory=lambda: {failure_type: 0 for failure_type in INJECTED_FAILURES}
    )
    message_duration: dict[str, _Duration] = field(
        default_factory=lambda: {phase: _Duration() for phase in MESSAGE_PHASES}
    )

    def record_handshake_success(
        self,
        duration_seconds: float,
        public_key_seconds: float,
        encapsulation_seconds: float,
    ) -> None:
        """Record one completed handshake and its component timings."""
        self.handshakes_succeeded += 1
        self.handshake_duration.observe(duration_seconds)
        self.public_key_duration.observe(public_key_seconds)
        self.encapsulation_duration.observe(encapsulation_seconds)
        self.active_session = 1

    def record_handshake_failure(
        self,
        reason: str,
        duration_seconds: float,
        public_key_seconds: float | None = None,
        encapsulation_seconds: float | None = None,
    ) -> None:
        """Record one failed handshake. Component timings are optional."""
        self.mlkem_handshake_failures_total += 1
        self.handshake_failures[reason if reason in self.handshake_failures else "unexpected"] += 1
        self.handshake_duration.observe(duration_seconds)
        if public_key_seconds is not None:
            self.public_key_duration.observe(public_key_seconds)
        if encapsulation_seconds is not None:
            self.encapsulation_duration.observe(encapsulation_seconds)
        self.active_session = 0

    def set_active_session(self, active: bool) -> None:
        """Record whether this process currently holds an active session."""
        self.active_session = 1 if active else 0

    def record_reestablishment(self, result: str) -> None:
        """Record one session-recovery handshake."""
        key = result if result in self.reestablishments else "failure"
        self.reestablishments[key] += 1

    def record_encryption_failure(self) -> None:
        """Record one local seal failure."""
        self.encryption_failures_total += 1

    def record_injected(self, failure_type: str) -> None:
        """Record one configured Gateway fault."""
        if failure_type in self.injected_failures:
            self.injected_failures[failure_type] += 1

    def record_secure_message(self, phase: str, duration_seconds: float) -> None:
        """Record delivery time for a first message or a later reused session."""
        if phase in self.message_duration:
            self.message_duration[phase].observe(duration_seconds)

    def render(self) -> str:
        """Return Prometheus text. The fallback counter is always the stored zero."""
        lines: list[str] = []
        self._family(
            lines,
            "gateway_mlkem_handshakes_total",
            "counter",
            "ML-KEM handshakes by result.",
            [
                f'gateway_mlkem_handshakes_total{{result="success"}} {self.handshakes_succeeded}',
                f'gateway_mlkem_handshakes_total{{result="failure"}} {self.mlkem_handshake_failures_total}',
            ],
        )
        self._family(
            lines,
            "gateway_mlkem_handshake_failures_total",
            "counter",
            "ML-KEM handshake failures by bounded reason.",
            [
                f'gateway_mlkem_handshake_failures_total{{reason="{reason}"}} {count}'
                for reason, count in self.handshake_failures.items()
            ],
        )
        self._duration(lines, "gateway_mlkem_handshake_duration_seconds", "Full session establishment.", self.handshake_duration)
        self._duration(lines, "gateway_mlkem_public_key_duration_seconds", "Cloud public-key retrieval.", self.public_key_duration)
        self._duration(lines, "gateway_mlkem_encapsulation_duration_seconds", "Local ML-KEM encapsulation.", self.encapsulation_duration)
        self._family(
            lines,
            "gateway_session_reestablishments_total",
            "counter",
            "Session recoveries after HTTP 409.",
            [
                f'gateway_session_reestablishments_total{{result="{result}"}} {count}'
                for result, count in self.reestablishments.items()
            ],
        )
        self._family(
            lines,
            "gateway_active_session",
            "gauge",
            "1 when the Gateway holds an active session.",
            [f"gateway_active_session {self.active_session}"],
        )
        self._family(
            lines,
            "gateway_encryption_failures_total",
            "counter",
            "Local AES-GCM seal failures.",
            [f"gateway_encryption_failures_total {self.encryption_failures_total}"],
        )
        self._family(
            lines,
            "gateway_pqc_fallback_total",
            "counter",
            "Runtime plaintext fallbacks. Protocol version 1 keeps this at 0.",
            [f"gateway_pqc_fallback_total {self.pqc_fallback_total}"],
        )
        self._family(
            lines,
            "gateway_injected_failures_total",
            "counter",
            "Configured Gateway faults that were applied.",
            [
                f'gateway_injected_failures_total{{failure_type="{failure_type}"}} {count}'
                for failure_type, count in self.injected_failures.items()
            ],
        )
        self._family(
            lines,
            "gateway_secure_message_duration_seconds",
            "summary",
            "Secure delivery time. phase=first includes handshake; phase=steady reuses a session.",
            [
                sample
                for phase, duration in self.message_duration.items()
                for sample in (
                    f'gateway_secure_message_duration_seconds_sum{{phase="{phase}"}} {duration.total_seconds:.6f}',
                    f'gateway_secure_message_duration_seconds_count{{phase="{phase}"}} {duration.count}',
                )
            ],
        )
        return "\n".join(lines) + "\n"

    @staticmethod
    def _family(lines: list[str], name: str, metric_type: str, help_text: str, samples: list[str]) -> None:
        lines.append(f"# HELP {name} {help_text}")
        lines.append(f"# TYPE {name} {metric_type}")
        lines.extend(samples)

    @staticmethod
    def _duration(lines: list[str], name: str, help_text: str, duration: _Duration) -> None:
        PqcMetrics._family(
            lines,
            name,
            "summary",
            help_text,
            [
                f"{name}_sum {duration.total_seconds:.6f}",
                f"{name}_count {duration.count}",
            ],
        )
