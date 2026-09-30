"""Crypto-only Gateway failure injection.

``FAILURE_MODE=none`` and ``FAILURE_RATE=0`` leave handshakes, sessions, and
ciphertext unchanged. The seeded generator decides only whether a configured
crypto fault happens. It is not a source of keys or nonces.
"""

from __future__ import annotations

import logging
import math
import random

from edge_gateway.config import GatewayConfig

logger = logging.getLogger(__name__)

CRYPTO_FAILURE_MODES = frozenset(
    {
        "mlkem_handshake_failure",
        "corrupt_ciphertext",
        "session_missing",
        "session_expired",
    }
)


class CryptoFailureInjector:
    """Apply one configured crypto fault, or leave the secure path unchanged."""

    def __init__(self, mode: str, failure_rate: float, failure_seed: str | None = None) -> None:
        if not isinstance(mode, str):
            raise ValueError("failure_mode must be a string.")
        if (
            isinstance(failure_rate, bool)
            or not isinstance(failure_rate, (int, float))
            or not math.isfinite(failure_rate)
            or not 0.0 <= failure_rate <= 1.0
        ):
            raise ValueError("failure_rate must be between 0.0 and 1.0.")
        self._mode = mode
        self._rate = float(failure_rate)
        self._random = random.Random(None if failure_seed is None else str(failure_seed))
        if mode in CRYPTO_FAILURE_MODES and self._rate > 0:
            logger.warning("event=failure_injection_enabled mode=%s", mode)

    @classmethod
    def disabled(cls) -> CryptoFailureInjector:
        """Return an injector that never changes the secure path."""
        return cls("none", 0.0)

    @classmethod
    def from_config(cls, config: GatewayConfig) -> CryptoFailureInjector:
        """Build an injector from validated Gateway configuration."""
        return cls(config.failure_mode, config.failure_rate, config.failure_seed)

    def handshake_failure(self) -> bool:
        """Return whether this attempt should fail before a session exists."""
        return self._selected("mlkem_handshake_failure")

    def corrupt_ciphertext(self) -> bool:
        """Return whether the outgoing ciphertext copy should be mutated."""
        return self._selected("corrupt_ciphertext")

    def session_missing(self) -> bool:
        """Return whether local session state should be dropped."""
        return self._selected("session_missing")

    def session_expired(self) -> bool:
        """Return whether the active session should be forced expired."""
        return self._selected("session_expired")

    def _selected(self, mode: str) -> bool:
        if self._mode != mode or self._rate <= 0:
            return False
        if self._rate >= 1:
            return True
        return self._random.random() < self._rate


def corrupt_ciphertext_copy(ciphertext: bytes) -> bytes:
    """Return a mutated copy. The caller's buffer is left unchanged."""
    if not ciphertext:
        return b""
    mutated = bytearray(ciphertext)
    mutated[0] ^= 0x01
    return bytes(mutated)
