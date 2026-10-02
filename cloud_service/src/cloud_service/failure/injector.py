"""Deterministic test faults; never a source of cryptographic randomness."""

from __future__ import annotations

import logging
import random
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from cloud_service.config import Config, FailureMode

logger = logging.getLogger("cloud_service")

_INJECTABLE = frozenset(
    mode
    for mode in FailureMode
    if mode not in {FailureMode.NONE, FailureMode.RANDOM}
)


@dataclass(slots=True)
class FailureSelection:
    """One request's optional fault, selected before its processing stages."""

    mode: FailureMode | None = None
    on_applied: Callable[[str], None] | None = None
    _applied: bool = False

    def inject(self, mode: FailureMode) -> bool:
        return self.mode is mode

    def apply(self, mode: FailureMode) -> bool:
        """Mark and safely log the selected fault only at its real boundary."""
        if not self.inject(mode):
            return False
        if not self._applied:
            logger.warning("event=failure_injected component=cloud_service failure_type=%s", mode.value)
            if self.on_applied is not None:
                self.on_applied(mode.value)
            self._applied = True
        return True


class FailureInjector:
    """Select configured Cloud faults without changing normal behavior."""

    def __init__(
        self, mode: FailureMode, rate: float, seed: int | None, delay_seconds: float,
        *, on_applied: Callable[[str], None] | None = None,
    ):
        self._mode = mode
        self._rate = rate
        self._delay_seconds = delay_seconds
        self._random = random.Random(seed)
        self._on_applied = on_applied
        if mode is not FailureMode.NONE and rate > 0:
            logger.warning(
                "event=failure_injection_enabled component=cloud_service mode=%s rate=%s",
                mode.value, rate,
            )

    @classmethod
    def from_config(
        cls, config: Config, *, on_applied: Callable[[str], None] | None = None,
    ) -> FailureInjector:
        return cls(
            config.failure_mode, config.failure_rate, config.failure_seed,
            config.failure_delay_seconds, on_applied=on_applied,
        )

    @property
    def delay_seconds(self) -> float:
        return self._delay_seconds

    def select(self, allowed: Iterable[FailureMode]) -> FailureSelection:
        """Choose at most one applicable fault after one rate gate.

        A request reuses its selection at every processing boundary.  This is
        deliberately separate from cryptographic randomness and makes seeded
        tests reproducible.
        """
        candidates = tuple(sorted(set(allowed) & _INJECTABLE, key=str))
        if not candidates or self._mode is FailureMode.NONE or self._rate == 0:
            return FailureSelection(on_applied=self._on_applied)
        if self._mode is FailureMode.RANDOM:
            if self._rate < 1 and self._random.random() >= self._rate:
                return FailureSelection(on_applied=self._on_applied)
            selected = self._random.choice(candidates)
        else:
            if self._mode not in candidates:
                return FailureSelection(on_applied=self._on_applied)
            if self._rate < 1 and self._random.random() >= self._rate:
                return FailureSelection()
            selected = self._mode
        return FailureSelection(selected, on_applied=self._on_applied)
