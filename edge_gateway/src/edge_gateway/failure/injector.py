"""Local simulation decisions; never a source of keys, nonces, or request IDs."""

from __future__ import annotations

from collections.abc import Iterable
import logging
import math
import random

from edge_gateway.config import GatewayConfig, KNOWN_FAILURE_MODES

logger = logging.getLogger(__name__)

APPLICATION_FAILURE_MODES = frozenset({
    "processing_error", "processing_delay", "cloud_timeout",
    "cloud_unavailable", "drop_message",
})


class FailureInjector:
    """Select at most one application fault per call without executing it.

    Keep one instance per application. Call once per eligible logical request
    and retain the returned mode across its processing/transport boundaries.
    The same seed and call order reproduce decisions. Crypto modes are inert
    here and remain owned by the separate crypto injector.
    """

    def __init__(
        self, mode: str = "none", failure_rate: float = 0.0,
        failure_seed: str | None = None, *, announce: bool = True,
    ) -> None:
        if not isinstance(mode, str) or mode not in KNOWN_FAILURE_MODES:
            raise ValueError("failure_mode must be a known Gateway mode")
        if (
            isinstance(failure_rate, bool)
            or not isinstance(failure_rate, (int, float))
            or not math.isfinite(failure_rate)
            or not 0 <= failure_rate <= 1
        ):
            raise ValueError("failure_rate must be between 0.0 and 1.0")
        if failure_seed is not None and not isinstance(failure_seed, str):
            raise ValueError("failure_seed must be a string or None")
        self._mode = mode
        self._rate = failure_rate
        self._random = random.Random(failure_seed)
        if announce:
            self.log_enabled()

    def log_enabled(self) -> None:
        """Announce enabled application simulation after startup logging is configured."""
        if self._mode in APPLICATION_FAILURE_MODES | {"random"} and self._rate > 0:
            logger.warning(
                "event=failure_injection_enabled component=edge_gateway mode=%s",
                self._mode,
            )

    @classmethod
    def from_config(cls, config: GatewayConfig, *, announce: bool = True) -> FailureInjector:
        """Use the existing validated local configuration."""
        return cls(config.failure_mode, config.failure_rate, config.failure_seed, announce=announce)

    def select(self, allowed: Iterable[str] = APPLICATION_FAILURE_MODES) -> str | None:
        """Return an applicable fault or None, using one probability gate.

        Callers can restrict selection to implemented boundaries. Sorting the
        candidates makes seeded random mode independent of iterable ordering.
        Selection does not claim that the fault has actually been applied.
        """
        candidates = tuple(sorted(set(allowed) & APPLICATION_FAILURE_MODES))
        if not candidates or self._rate == 0:
            return None
        if self._mode != "random" and self._mode not in candidates:
            return None
        if self._rate < 1 and self._random.random() >= self._rate:
            return None
        selected = self._random.choice(candidates) if self._mode == "random" else self._mode
        logger.debug(
            "event=failure_selected component=edge_gateway failure_type=%s", selected
        )
        return selected
