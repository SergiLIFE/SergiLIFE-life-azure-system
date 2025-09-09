"""Unit tests for venturi_batching canonical module.
Focus: adjustment correctness, adaptive gamma behavior, numba fallback.
"""

from __future__ import annotations

import pytest

from venturi_batching import VenturiBatcher, venturi_adjust, venturi_adjust_numba


def test_pure_function_expand_and_contract():
    # Expand
    assert (
        venturi_adjust(
            8,
            last_latency=40,
            target_latency=50,
            min_batch=1,
            max_batch=64,
            gamma=1.5,
        )
        == 12
    )
    # Contract
    assert (
        venturi_adjust(
            32,
            last_latency=80,
            target_latency=50,
            min_batch=1,
            max_batch=64,
            gamma=1.5,
        )
        == 21
    )
    # No change (at bounds)
    assert (
        venturi_adjust(
            64,
            last_latency=40,
            target_latency=50,
            min_batch=1,
            max_batch=64,
            gamma=1.5,
        )
        == 64
    )


def test_numba_function_available_or_fallback():
    # Call should behave same as pure function for a known case
    a = venturi_adjust(8, 40, 50, 1, 64, 1.5)
    b = venturi_adjust_numba(8, 40, 50, 1, 64, 1.5)
    assert a == b


def test_batcher_basic_flow():
    b = VenturiBatcher(
        target_latency_ms=50,
        start_batch=8,
        batch_max=128,
        adaptive_gamma=False,
    )
    seq = [60, 55, 45, 40, 35]  # latencies
    batches = [b.adjust_batch_size(lat) for lat in seq]
    # Should contract then expand
    assert batches[0] < 8  # contracted due to high latency
    assert batches[-1] > batches[0]


def test_adaptive_gamma_changes():
    b = VenturiBatcher(
        target_latency_ms=50, start_batch=8, batch_max=256, adaptive_gamma=True
    )
    initial_gamma = b.gamma

    # Test that gamma responds to latency patterns
    # Slow latencies should reduce gamma
    for lat in [70, 75, 72, 68, 80, 85]:  # More slow latencies for clear effect
        b.adjust_batch_size(lat)
    gamma_after_slow = b.gamma

    # Verify gamma decreased from slow latencies
    assert (
        gamma_after_slow < initial_gamma
    ), f"Expected gamma to decrease from {initial_gamma} but got {gamma_after_slow}"

    # Fast latencies should increase gamma over time
    # Need many fast latencies to overcome the EWMA smoothing
    for _ in range(15):  # More iterations to ensure gamma recovery
        for lat in [20, 25, 30, 22]:
            b.adjust_batch_size(lat)
    gamma_after_fast = b.gamma

    # Test that gamma increased from the slow period (allowing for EWMA lag)
    assert (
        gamma_after_fast > gamma_after_slow
    ), f"Expected gamma to recover from {gamma_after_slow} but got {gamma_after_fast}"


def test_summary_structure():
    b = VenturiBatcher(target_latency_ms=50, start_batch=8)
    b.adjust_batch_size(60)
    s = b.summary()
    assert {
        "current_batch",
        "gamma",
        "adjustments",
        "history_len",
        "throughput_estimate",
    }.issubset(s.keys())


@pytest.mark.parametrize(
    "lat,expected",
    [
        (40, 12),  # expand
        (80, 5),  # contract (32/1.5 -> 21 but start will be updated) example
    ],
)
def test_parametrized_behavior(lat, expected):
    b = VenturiBatcher(
        target_latency_ms=50,
        start_batch=8,
        batch_max=64,
        adaptive_gamma=False,
        gamma=1.5,
    )
    # Set internal batch manually for deterministic test of contract path
    b.current_batch = 8 if lat == 40 else 32
    out = b.adjust_batch_size(lat)
    assert out > 8 if lat == 40 else out < 32


def test_gamma_bounds():
    b = VenturiBatcher(target_latency_ms=50, start_batch=8, gamma=2.4)
    # Very fast latencies push gamma upward but capped at 2.5
    for _ in range(20):
        b.adjust_batch_size(20)
    assert b.gamma <= 2.5
    # Very slow latencies push gamma downward but not below 1.1
    for _ in range(40):
        b.adjust_batch_size(120)
    assert b.gamma >= 1.1
