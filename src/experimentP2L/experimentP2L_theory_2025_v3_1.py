"""
experimentP2L_theory_2025_v3_1.py (sanitized import)

Provenance:
- Source content provided by user as a large Python script attachment
  with mixed-language reference blocks and emojis.
- This file is a sanitized, import-friendly version suitable for the repo’s
  professional/no-emoji policy and Python syntax rules.

Notes:
- Non-Python reference/pseudo-code blocks, YAML/C#, and emojis have been
  removed or moved to docstrings/comments for clarity.
- Optional dependencies (mne, scipy, azure-eventhub) are imported lazily to
  avoid hard failures. Functions degrade gracefully when unavailable.
- This module focuses on preserving the core structures the platform may use:
  ArmStats (bandit stats), ImpactResult dataclass, and
  NeurocognitiveImpactOptimizer (wavelet/PLI-based impact model).

If you need the full verbatim original (including non-Python sections),
please store it under docs/attachments/ as a text artifact (emoji-free) or
reference it in documentation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import math
import json
import asyncio

import numpy as np

# Optional, lazy imports guarded at call sites
try:
    import pywt  # wavelets
    _PYWT_AVAILABLE = True
except Exception:
    _PYWT_AVAILABLE = False

try:
    from azure.eventhub.aio import EventHubProducerClient
    from azure.eventhub import EventData
    _AZURE_EH_AVAILABLE = True
except Exception:
    _AZURE_EH_AVAILABLE = False


# -----------------------------
# Basic bandit stats (skeleton)
# -----------------------------
@dataclass
class ArmStats:
    n: int = 0
    total_reward: float = 0.0
    alpha: float = 1.0  # Beta distribution parameters (for Thompson Sampling)
    beta: float = 1.0

    def mean_reward(self) -> float:
        return self.total_reward / self.n if self.n > 0 else 0.0

    def thompson_sample(self) -> float:
        # Simple Beta sample, if you need stochastic selection
        try:
            return np.random.beta(self.alpha, self.beta).item()
        except Exception:
            return self.mean_reward()

    def ucb(self, total_pulls: int, c: float = 2.0) -> float:
        # Upper Confidence Bound index
        if self.n == 0:
            return float("inf")
        return self.mean_reward() + math.sqrt(c * math.log(max(total_pulls, 1)) / self.n)


# -----------------------------------
# Impact analysis result (dataclass)
# -----------------------------------
@dataclass
class ImpactResult:
    total_impact: float
    band_impacts: Dict[str, float]
    wavelet_energy: float
    pli_scores: Dict[str, float]
    cognitive_noise: float
    timestamp: float


# ------------------------------------------------------------
# Neurocognitive Impact Optimizer (wavelet + PLI + aggregation)
# ------------------------------------------------------------
class NeurocognitiveImpactOptimizer:
    """
    Quantify neural engagement using orthogonal wavelet decomposition + PLI.

    Impact = sum_b sum_t |W(b,t)|^2 * PLI(b) + epsilon

    Where:
      - W(b,t): wavelet coefficients at band b and time t
      - PLI(b): Phase Lag Index per frequency band (single-channel proxy)
      - epsilon: cognitive noise floor
    """

    def __init__(
        self,
        wavelet: str = "db4",
        decomp_level: int = 5,
        threshold_factor: float = 0.1,
        noise_floor: float = 0.04,
        event_hub_conn: Optional[str] = None,
        eventhub_name: str = "neuroimpact",
    ) -> None:
        self.wavelet = wavelet
        self.decomp_level = decomp_level
        self.threshold_factor = threshold_factor
        self.cognitive_noise = noise_floor

        # Frequency bands (Hz)
        self.freq_bands: Dict[str, tuple[int, int]] = {
            "delta": (1, 4),
            "theta": (4, 8),
            "alpha": (8, 13),
            "beta": (13, 30),
            "gamma": (30, 100),
        }

        # Azure Event Hub (optional)
        self._eventhub_conn = event_hub_conn
        self._eventhub_name = eventhub_name
        self._producer_client: Optional[EventHubProducerClient] = None

    async def _get_producer(self) -> Optional[EventHubProducerClient]:
        if not (_AZURE_EH_AVAILABLE and self._eventhub_conn):
            return None
        if self._producer_client is None:
            self._producer_client = EventHubProducerClient.from_connection_string(
                self._eventhub_conn, eventhub_name=self._eventhub_name
            )
        return self._producer_client

    def orthogonal_wavelet_decomposition(self, signal: np.ndarray) -> List[np.ndarray]:
        """
        Perform orthogonal wavelet decomposition with soft thresholding.
        Returns a list of (possibly thresholded) coefficient arrays.
        """
        if signal.size == 0:
            return [np.array([])]
        if not _PYWT_AVAILABLE:
            # Fallback: no wavelet library
            return [signal.astype(float, copy=False)]

        coeffs = pywt.wavedec(signal, self.wavelet, level=self.decomp_level, mode="periodization")
        thr_coeffs: List[np.ndarray] = []
        for c in coeffs:
            if c.size == 0:
                thr_coeffs.append(c)
            else:
                threshold = self.threshold_factor * float(np.max(np.abs(c)))
                thr_coeffs.append(pywt.threshold(c, value=threshold, mode="soft"))
        return thr_coeffs

    def compute_wavelet_energy(self, coeffs: List[np.ndarray]) -> float:
        total = 0.0
        for c in coeffs:
            if c.size:
                total += float(np.sum(np.square(np.abs(c))))
        return total

    def compute_phase_lag_index(self, signal: np.ndarray, fs: int = 256) -> Dict[str, float]:
        """
        Single-channel proxy for PLI: phase difference consistency per band.
        Returns zeros if scipy is unavailable or inputs are insufficient.
        """
        pli: Dict[str, float] = {k: 0.0 for k in self.freq_bands.keys()}
        if signal.size < 4:
            return pli
        try:
            from scipy.signal import hilbert, butter, filtfilt
        except Exception:
            return pli

        nyq = fs / 2.0
        for band, (lo, hi) in self.freq_bands.items():
            lo_n = lo / nyq
            hi_n = min(hi / nyq, 0.99)
            if lo_n >= hi_n:
                pli[band] = 0.0
                continue
            try:
                b, a = butter(4, [lo_n, hi_n], btype="band")
                filtered = filtfilt(b, a, signal)
                analytic = hilbert(filtered)
                phase = np.angle(analytic)
                dphi = np.diff(phase)
                dphi_wrapped = np.angle(np.exp(1j * dphi))
                pli_val = float(np.abs(np.mean(np.sign(dphi_wrapped))))
                pli[band] = pli_val
            except Exception:
                pli[band] = 0.0
        return pli

    def compute_band_impacts(self, coeffs: List[np.ndarray], pli_scores: Dict[str, float]) -> Dict[str, float]:
        bands = list(self.freq_bands.keys())
        impacts: Dict[str, float] = {}
        # Approximate mapping: first N coeff arrays to bands
        for band, c in zip(bands, coeffs[: len(bands) ]):
            if c.size:
                energy = float(np.sum(np.square(np.abs(c))))
                impacts[band] = energy * float(pli_scores.get(band, 0.0))
            else:
                impacts[band] = 0.0
        # Any remaining bands not covered by coeffs
        for band in bands[len(impacts) :]:
            impacts[band] = 0.0
        return impacts

    async def optimize(self, eeg_signal: np.ndarray, fs: int = 256, subject_id: Optional[str] = None) -> ImpactResult:
        import time
        ts = time.time()

        # Use first channel for multi-channel arrays
        if eeg_signal.ndim > 1:
            sig = eeg_signal[0, :]
        else:
            sig = eeg_signal

        sig = sig.astype(float, copy=False)
        if sig.size:
            sig = (sig - float(np.mean(sig))) / (float(np.std(sig)) + 1e-8)

        coeffs = self.orthogonal_wavelet_decomposition(sig)
        energy = self.compute_wavelet_energy(coeffs)
        pli = self.compute_phase_lag_index(sig, fs=fs)
        band_impacts = self.compute_band_impacts(coeffs, pli)

        total_impact = float(sum(band_impacts.values())) + float(self.cognitive_noise)
        result = ImpactResult(
            total_impact=total_impact,
            band_impacts=band_impacts,
            wavelet_energy=energy,
            pli_scores=pli,
            cognitive_noise=float(self.cognitive_noise),
            timestamp=ts,
        )

        await self._stream_result(result, subject_id)
        return result

    async def _stream_result(self, result: ImpactResult, subject_id: Optional[str]) -> None:
        producer = await self._get_producer()
        if not producer:
            return
        payload = {
            "subject_id": subject_id or "unknown",
            "timestamp": result.timestamp,
            "total_impact": result.total_impact,
            "wavelet_energy": result.wavelet_energy,
            "band_impacts": result.band_impacts,
            "pli_scores": result.pli_scores,
            "cognitive_noise": result.cognitive_noise,
        }
        try:
            event = EventData(json.dumps(payload))
            async with producer:
                await producer.send_batch([event])
        except Exception:
            # Streaming is best-effort; ignore failures
            return

    async def close(self) -> None:
        if self._producer_client is not None:
            try:
                await self._producer_client.close()
            except Exception:
                pass


# -----------------
# Minimal CLI demo
# -----------------
async def _demo() -> None:
    optimizer = NeurocognitiveImpactOptimizer(wavelet="db4", decomp_level=6)
    fs = 256
    t = np.linspace(0.0, 4.0, 4 * fs, endpoint=False)
    eeg = (
        0.5 * np.sin(2 * np.pi * 2 * t) +
        0.3 * np.sin(2 * np.pi * 6 * t) +
        0.8 * np.sin(2 * np.pi * 10 * t) +
        0.2 * np.random.randn(t.size)
    )
    res = await optimizer.optimize(eeg, fs=fs, subject_id="demo_subject")
    print("Total Impact:", round(res.total_impact, 6))
    print("Wavelet Energy:", round(res.wavelet_energy, 6))
    print("Band Impacts:", {k: round(v, 6) for k, v in res.band_impacts.items()})
    print("PLI Scores:", {k: round(v, 6) for k, v in res.pli_scores.items()})
    await optimizer.close()


if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except KeyboardInterrupt:
        pass