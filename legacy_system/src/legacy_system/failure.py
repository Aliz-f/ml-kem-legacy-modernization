"""Controlled mutation of serialized Legacy Device payloads."""

from collections.abc import Mapping
import logging
import random

from legacy_system.config import FailureMode


_RANDOM_MODES = (
    FailureMode.INVALID_TEMPERATURE,
    FailureMode.INVALID_HUMIDITY,
    FailureMode.MISSING_FIELD,
    FailureMode.INVALID_TIMESTAMP,
    FailureMode.DUPLICATE_SEQUENCE,
    FailureMode.OUT_OF_ORDER_SEQUENCE,
)


class FailureInjector:
    """Apply configured faults to outgoing payload copies."""

    def __init__(
        self,
        mode: FailureMode,
        failure_rate: float,
        failure_seed: int | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        if not 0.0 <= failure_rate <= 1.0:
            raise ValueError("failure_rate must be between 0.0 and 1.0")
        self._mode = mode
        self._failure_rate = failure_rate
        self._random = random.Random(failure_seed)
        self._logger = logger or logging.getLogger(__name__)
        self._seen_sequences: list[int] = []

    def apply(self, payload: Mapping[str, object]) -> dict[str, object]:
        """Return a possibly mutated copy of a serialized payload."""
        outgoing = dict(payload)
        current_sequence = _sequence_number(outgoing)
        previous_sequences = tuple(self._seen_sequences)
        self._seen_sequences.append(current_sequence)

        if (
            self._mode is FailureMode.NONE
            or self._random.random() >= self._failure_rate
        ):
            return outgoing

        selected_mode = self._selected_mode(current_sequence, previous_sequences)
        if selected_mode is None:
            return outgoing

        self._mutate(outgoing, selected_mode, current_sequence, previous_sequences)
        self._logger.warning(
            "event=simulated_failure_injected component=legacy_system mode=%s sequence_number=%s",
            selected_mode.value,
            current_sequence,
        )
        return outgoing

    def _selected_mode(
        self, current_sequence: int, previous_sequences: tuple[int, ...]
    ) -> FailureMode | None:
        if self._mode is not FailureMode.RANDOM:
            return (
                self._mode
                if self._can_mutate(self._mode, current_sequence, previous_sequences)
                else None
            )
        candidates = tuple(
            mode
            for mode in _RANDOM_MODES
            if self._can_mutate(mode, current_sequence, previous_sequences)
        )
        return self._random.choice(candidates)

    @staticmethod
    def _can_mutate(
        mode: FailureMode,
        current_sequence: int,
        previous_sequences: tuple[int, ...],
    ) -> bool:
        if mode is FailureMode.DUPLICATE_SEQUENCE:
            return bool(previous_sequences)
        if mode is FailureMode.OUT_OF_ORDER_SEQUENCE:
            return any(sequence < current_sequence for sequence in previous_sequences)
        return True

    def _mutate(
        self,
        payload: dict[str, object],
        mode: FailureMode,
        current_sequence: int,
        previous_sequences: tuple[int, ...],
    ) -> None:
        if mode is FailureMode.INVALID_TEMPERATURE:
            payload["temperature_c"] = self._invalid_temperature()
        elif mode is FailureMode.INVALID_HUMIDITY:
            payload["humidity_pct"] = self._invalid_humidity()
        elif mode is FailureMode.MISSING_FIELD:
            payload.pop("timestamp", None)
        elif mode is FailureMode.INVALID_TIMESTAMP:
            payload["timestamp"] = (
                f"not-a-valid-timestamp-{self._random.randrange(1_000_000)}"
            )
        elif mode is FailureMode.DUPLICATE_SEQUENCE:
            payload["sequence_number"] = self._random.choice(previous_sequences)
        elif mode is FailureMode.OUT_OF_ORDER_SEQUENCE:
            lower_sequences = tuple(
                sequence
                for sequence in previous_sequences
                if sequence < current_sequence
            )
            payload["sequence_number"] = self._random.choice(lower_sequences)
        else:
            raise ValueError(f"Unsupported failure mode: {mode}")

    def _invalid_temperature(self) -> float:
        if self._random.choice((True, False)):
            return self._random.uniform(-100.0, -40.000001)
        return self._random.uniform(85.000001, 185.0)

    def _invalid_humidity(self) -> float:
        if self._random.choice((True, False)):
            return self._random.uniform(-100.0, -0.000001)
        return self._random.uniform(100.000001, 200.0)


def _sequence_number(payload: Mapping[str, object]) -> int:
    value = payload.get("sequence_number")
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("payload sequence_number must be an integer")
    return value
