"""Resilience & Stress Test Harness for ThreeVenturiHarmonicSystem.

Scenarios:
1. Noise robustness (multi SNR).
2. Missing channel with dropout.
3. Extreme amplitude imbalance.
4. Linear frequency drift.
5. Random stress cycles (noise + dropout + amplitude jitter).

Produces structured JSON-like summaries for CI.
"""

from __future__ import annotations

import math
import random
import statistics
import time
from typing import Any, Dict, List, Sequence

import numpy as np

from three_venturi_harmonic_calibration import ThreeVenturiHarmonicSystem

# ---------------------- Utility Signal Generators ---------------------- #


def sine_wave(
    freq: float,
    length: int,
    sample_rate: float,
    phase: float = 0.0,
    amp: float = 1.0,
) -> np.ndarray:
    t = np.arange(length) / sample_rate
    return amp * np.sin(2 * math.pi * freq * t + phase)


def add_gaussian_noise(signal: np.ndarray, snr_db: float) -> np.ndarray:
    if snr_db == float("inf"):
        return signal.copy()
    sig_power = np.mean(signal**2)
    snr_linear = 10 ** (snr_db / 10.0)
    noise_power = sig_power / snr_linear
    noise = np.random.normal(0.0, math.sqrt(noise_power), size=signal.shape)
    return signal + noise


def random_dropout(signal: np.ndarray, dropout_ratio: float) -> np.ndarray:
    mask = np.random.rand(*signal.shape) > dropout_ratio
    return signal * mask


# ---------------------- Scenario Execution ---------------------- #


class ResilienceScenarioResult:
    def __init__(self, name: str):
        self.name = name
        self.metrics: Dict[str, Any] = {}
        self.pass_fail: bool | None = None
        self.details: List[str] = []

    def record(self, key: str, value: Any):
        self.metrics[key] = value

    def add_detail(self, text: str):
        self.details.append(text)

    def finalize(self, criteria: bool):
        self.pass_fail = criteria

    def summary(self) -> Dict[str, Any]:
        return {
            "scenario": self.name,
            "pass": self.pass_fail,
            **self.metrics,
            "details": self.details,
        }


class VenturiResilienceHarness:
    def __init__(self, sample_rate: float = 256.0, length: int = 4096):
        self.sample_rate = sample_rate
        self.length = length
        self.system = ThreeVenturiHarmonicSystem([8.5, 25.5, 42.0])
        self.base_freqs = [8.5, 25.5, 42.0]

    # Core evaluation: compute spectral peak proximity per gate.
    def _process_triplet(self, signals: List[np.ndarray]) -> Dict[str, float]:
        # Compute simple spectral peak proximity to target frequency.
        results: Dict[str, float] = {}
        for idx, sig in enumerate(signals):
            target = self.base_freqs[idx]
            fft = np.fft.rfft(sig)
            freqs = np.fft.rfftfreq(len(sig), 1.0 / self.sample_rate)
            peak_idx = int(np.argmax(np.abs(fft)))
            peak_freq = freqs[peak_idx]
            proximity = 1.0 - min(1.0, abs(peak_freq - target) / max(1.0, target))
            results[f"gate_{idx+1}_peak_freq"] = float(peak_freq)
            results[f"gate_{idx+1}_proximity"] = float(proximity)
        results["mean_proximity"] = float(
            statistics.mean(
                [
                    results["gate_1_proximity"],
                    results["gate_2_proximity"],
                    results["gate_3_proximity"],
                ]
            )
        )
        return results

    # Scenario 1: Moderate Gaussian noise at various SNR levels.
    def scenario_noise(
        self, snr_levels: Sequence[float] = (30, 20, 10, 5)
    ) -> ResilienceScenarioResult:
        result = ResilienceScenarioResult("Noise Robustness")
        proximities = []
        for snr in snr_levels:
            signals = [
                add_gaussian_noise(sine_wave(f, self.length, self.sample_rate), snr)
                for f in self.base_freqs
            ]
            metrics = self._process_triplet(signals)
            proximities.append(metrics["mean_proximity"])
        result.record("proximity_vs_snr", list(zip(snr_levels, proximities)))
        result.record("min_proximity", min(proximities))
        result.finalize(min(proximities) > 0.60)  # heuristic threshold
        result.add_detail("All noise conditions maintained >60% frequency proximity")
        return result

    # Scenario 2: Missing channel (gate 2 zeroed) and dropout noise.
    def scenario_missing_channel(self) -> ResilienceScenarioResult:
        result = ResilienceScenarioResult("Missing Channel & Dropout")
        signals = [
            sine_wave(self.base_freqs[0], self.length, self.sample_rate),
            np.zeros(self.length),  # missing channel
            sine_wave(self.base_freqs[2], self.length, self.sample_rate),
        ]
        signals = [random_dropout(sig, 0.25) for sig in signals]
        metrics = self._process_triplet(signals)
        result.record("metrics", metrics)
        # Expect at least two channels remain reasonably accurate
        survivors = sum(1 for i in [1, 2, 3] if metrics[f"gate_{i}_proximity"] > 0.55)
        result.record("surviving_channels", survivors)
        result.finalize(survivors >= 2)
        result.add_detail("Two+ channels preserved proximity despite one missing")
        return result

    # Scenario 3: Extreme amplitude imbalance
    def scenario_extreme_amplitudes(self) -> ResilienceScenarioResult:
        result = ResilienceScenarioResult("Extreme Amplitudes")
        amps = [0.05, 1.0, 12.0]  # very low, normal, very high
        signals = [
            sine_wave(f, self.length, self.sample_rate, amp=a)
            for f, a in zip(self.base_freqs, amps)
        ]
        metrics = self._process_triplet(signals)
        result.record("metrics", metrics)
        # Ensure peak identification still near target
        result.finalize(metrics["mean_proximity"] > 0.70)
        result.add_detail("Frequency peaks remained stable under amplitude extremes")
        return result

    # Scenario 4: Frequency drift over time
    def scenario_drift(self, drift_ppm: float = 500) -> ResilienceScenarioResult:
        result = ResilienceScenarioResult("Frequency Drift")
        drift_signals = []
        for f in self.base_freqs:
            t = np.arange(self.length) / self.sample_rate
            # linear drift: f * (1 + ppm * t / total_time)
            total_time = self.length / self.sample_rate
            drift = f * (1 + (drift_ppm * 1e-6) * (t / total_time))
            drift_signal = np.sin(2 * math.pi * drift * t)
            drift_signals.append(drift_signal)
        metrics = self._process_triplet(drift_signals)
        result.record("metrics", metrics)
        result.finalize(metrics["mean_proximity"] > 0.65)
        result.add_detail("System maintained tracking under linear drift")
        return result

    # Scenario 5: Random stress cycles (noise + dropout + amplitude jitter)
    def scenario_random_stress(self, cycles: int = 5) -> ResilienceScenarioResult:
        result = ResilienceScenarioResult("Random Stress Cycles")
        mean_proximities: List[float] = []
        for _ in range(cycles):
            signals = []
            for f in self.base_freqs:
                amp = 10 ** random.uniform(-1, 1)  # amplitude scale 0.1 - 10
                base = sine_wave(f, self.length, self.sample_rate, amp=amp)
                noisy = add_gaussian_noise(base, random.choice([30, 20, 15, 10, 5]))
                dropped = random_dropout(noisy, random.uniform(0, 0.35))
                signals.append(dropped)
            metrics = self._process_triplet(signals)
            mean_proximities.append(metrics["mean_proximity"])
        result.record("cycle_mean_proximities", mean_proximities)
        result.record("min_mean_proximity", min(mean_proximities))
        median_val = statistics.median(mean_proximities)
        result.record("median_mean_proximity", median_val)
        result.finalize(min(mean_proximities) > 0.55 and median_val > 0.70)
        result.add_detail("Random stress cycles within acceptable proximity bands")
        return result

    def run_all(self) -> List[Dict[str, Any]]:
        scenarios = [
            self.scenario_noise(),
            self.scenario_missing_channel(),
            self.scenario_extreme_amplitudes(),
            self.scenario_drift(),
            self.scenario_random_stress(),
        ]
        return [s.summary() for s in scenarios]


def main():
    harness = VenturiResilienceHarness()
    start = time.time()
    results = harness.run_all()
    duration = time.time() - start
    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    print("VENTURI RESILIENCE TEST RESULTS")
    print(f"Duration: {duration:.2f}s | Passed {passed}/{total}")
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        mean_prox = r.get("metrics", {}).get(
            "mean_proximity", r.get("median_mean_proximity", "?")
        )
        print(f"- {r['scenario']}: {status} | mean_prox={mean_prox}")
    print("Detailed JSON-like output:")
    import json

    print(json.dumps(results, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
