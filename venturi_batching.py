"""Canonical Venturi batching module.

Provides:
- Pure Python fallback function `venturi_adjust`
- Optional Numba accelerated function `venturi_adjust_numba` (auto-detected)
- Adaptive `VenturiBatcher` class with latency & throughput metrics and dynamic gamma adjustment
- Deprecation stubs for legacy symbol names found in monolithic theory file(s)
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

try:  # Optional numba acceleration
    import numba  # type: ignore

    _NUMBA_AVAILABLE = True
except Exception:  # pragma: no cover
    _NUMBA_AVAILABLE = False
    numba = None  # type: ignore

# ---------------- Core Adjustment Functions ---------------- #


def venturi_adjust(
    current_batch: int,
    last_latency: float,
    target_latency: float,
    min_batch: int,
    max_batch: int,
    gamma: float,
) -> int:
    """Pure Python Venturi adjustment.

    Expands or contracts batch size based on observed latency relative to target.
    """
    if last_latency < target_latency and current_batch < max_batch:
        return min(max_batch, int(current_batch * gamma))
    if last_latency > target_latency and current_batch > min_batch:
        return max(min_batch, int(current_batch / gamma))
    return current_batch


if _NUMBA_AVAILABLE:

    @numba.njit(cache=True, fastmath=True)  # type: ignore
    def venturi_adjust_numba(
        current_batch: int,
        last_latency: float,
        target_latency: float,
        min_batch: int,
        max_batch: int,
        gamma: float,
    ) -> int:  # pragma: no cover (compiled path)
        if last_latency < target_latency and current_batch < max_batch:
            return min(max_batch, int(current_batch * gamma))
        if last_latency > target_latency and current_batch > min_batch:
            return max(min_batch, int(current_batch / gamma))
        return current_batch

else:  # Fallback alias

    def venturi_adjust_numba(
        current_batch: int,
        last_latency: float,
        target_latency: float,
        min_batch: int,
        max_batch: int,
        gamma: float,
    ) -> int:
        return venturi_adjust(
            current_batch, last_latency, target_latency, min_batch, max_batch, gamma
        )


# ---------------- Adaptive Batcher ---------------- #


@dataclass
class VenturiBatcher:
    target_latency_ms: float = 50.0
    gamma: float = 1.5
    batch_min: int = 1
    batch_max: int = 1024
    start_batch: int = 8
    adaptive_gamma: bool = True
    smoothing: float = 0.2  # EWMA smoothing for latency
    use_numba: bool = True

    # Metrics / state
    current_batch: int = field(init=False)
    _latency_ewma: Optional[float] = field(default=None, init=False)
    history: List[Dict[str, Any]] = field(default_factory=list, init=False)
    adjustments: int = field(default=0, init=False)

    def __post_init__(self):
        self.current_batch = self.start_batch
        if self.use_numba and not _NUMBA_AVAILABLE:
            self.use_numba = False

    def _select_impl(self) -> Callable[[int, float, float, int, int, float], int]:
        if self.use_numba and _NUMBA_AVAILABLE:
            return venturi_adjust_numba  # type: ignore
        return venturi_adjust

    def _update_gamma(self, last_latency: float):
        if not self.adaptive_gamma:
            return
        if self._latency_ewma is None:
            self._latency_ewma = last_latency
        else:
            self._latency_ewma = (
                self.smoothing * last_latency
                + (1 - self.smoothing) * self._latency_ewma
            )
        # Performance ratio ( >1 means slower than target )
        ratio = (
            (self._latency_ewma / self.target_latency_ms)
            if self.target_latency_ms > 0
            else 1.0
        )
        # Adaptive gamma: shrink when system slow, expand potential when fast
        # Bound gamma into [1.1, 2.5]
        if ratio > 1.05:  # too slow
            self.gamma = max(1.1, self.gamma * 0.95)
        elif ratio < 0.85:  # plenty of headroom
            self.gamma = min(2.5, self.gamma * 1.02)

    def adjust_batch_size(self, last_latency_ms: float) -> int:
        """Adjust the batch size based on last latency measurement."""
        self._update_gamma(last_latency_ms)
        impl = self._select_impl()
        new_batch = impl(
            self.current_batch,
            last_latency_ms,
            self.target_latency_ms,
            self.batch_min,
            self.batch_max,
            self.gamma,
        )
        if new_batch != self.current_batch:
            self.adjustments += 1
        self.current_batch = new_batch
        self.history.append(
            {
                "t": time.time(),
                "latency": last_latency_ms,
                "batch": self.current_batch,
                "gamma": self.gamma,
            }
        )
        return self.current_batch

    def throughput_estimate(self) -> Optional[float]:
        if not self.history:
            return None
        # Basic inverse latency * batch heuristic
        last = self.history[-1]
        lat = last["latency"]
        if lat <= 0:
            return None
        return self.current_batch / lat

    def summary(self) -> Dict[str, Any]:
        return {
            "current_batch": self.current_batch,
            "gamma": round(self.gamma, 4),
            "adjustments": self.adjustments,
            "history_len": len(self.history),
            "throughput_estimate": self.throughput_estimate(),
        }


# ---------------- Deprecation Stubs ---------------- #


class DeprecatedVenturiBatcher(VenturiBatcher):  # pragma: no cover
    """Legacy alias. Prefer `VenturiBatcher` from `venturi_batching` module."""

    pass


# Backwards compatible exported names for legacy imports
__all__ = [
    "venturi_adjust",
    "venturi_adjust_numba",
    "VenturiBatcher",
    "DeprecatedVenturiBatcher",
]
