"""
KPI Monitor utilities for the Neuroadaptive Dashboard and backend services.
Computes:
- Engagement Level (normalized 0..1)
- Learning Efficiency (proxy for Neuroplasticity growth)
- Retention (proxy for Experience correlation)
- Adaptation Speed (self-calibration convergence proxy)
ASCII-safe logging.
"""

from __future__ import annotations

from typing import Dict, List


def engagement_level(eeg: List[float]) -> float:
    if not eeg:
        return 0.0
    mean_signal = sum(eeg) / len(eeg)
    # Normalize around nominal 10..50 range
    val = (mean_signal - 10.0) / 40.0
    return max(0.0, min(1.0, val))


def learning_efficiency(eng_history: List[float]) -> float:
    if not eng_history:
        return 0.0
    # Simple derivative proxy
    delta = eng_history[-1] - eng_history[0]
    return max(0.0, min(1.0, 0.5 + delta))


def retention_correlation(history_a: List[float], history_b: List[float]) -> float:
    if not history_a or not history_b or len(history_a) != len(history_b):
        return 0.0
    n = len(history_a)
    mean_a = sum(history_a) / n
    mean_b = sum(history_b) / n
    cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(history_a, history_b)) / max(
        1, n - 1
    )
    var_a = sum((a - mean_a) ** 2 for a in history_a) / max(1, n - 1)
    var_b = sum((b - mean_b) ** 2 for b in history_b) / max(1, n - 1)
    denom = (var_a * var_b) ** 0.5
    if denom == 0:
        return 0.0
    r = cov / denom
    # map -1..1 to 0..1
    return 0.5 + 0.5 * max(-1.0, min(1.0, r))


def adaptation_speed(calibration_errors: List[float]) -> float:
    if not calibration_errors:
        return 0.0
    # faster drop in error -> higher score
    start = calibration_errors[0]
    end = calibration_errors[-1]
    if start <= 0:
        return 0.0
    reduction = max(0.0, start - end) / start
    return max(0.0, min(1.0, reduction))


def compute_kpis(eeg: List[float], eng_history: List[float]) -> Dict[str, float]:
    return {
        "engagement_level": engagement_level(eeg),
        "learning_efficiency": learning_efficiency(eng_history),
    }
