"""
Local ingestion scheduler runner (safe, zero-drift)

Runs the existing ExternalEEGIngestionEngine for N cycles, with a local-only
storage stub to avoid Azure credential requirements. Results are saved to
results/ingestion/ as JSON files per cycle plus an aggregate summary.

Usage (Windows CMD):
  python scripts\ingestion_scheduler_runner.py --cycles 3 --sleep-seconds 5
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "results" / "ingestion"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


async def _run_cycle(engine) -> Dict[str, Any]:
    # Override storage to local file writes to avoid Azure creds during local testing
    async def _store_local(metrics, dataset) -> bool:
        payload = {
            "dataset": {
                "name": dataset.name,
                "type": dataset.dataset_type,
                "format": dataset.file_format,
                "sampling_rate": dataset.sampling_rate,
                "expected_channels": dataset.expected_channels,
                "description": dataset.description,
            },
            "metrics": {
                "alpha_power": getattr(metrics, "alpha_power", None),
                "beta_power": getattr(metrics, "beta_power", None),
                "theta_power": getattr(metrics, "theta_power", None),
                "gamma_power": getattr(metrics, "gamma_power", None),
                "coherence_score": getattr(metrics, "coherence_score", None),
                "learning_efficiency": getattr(metrics, "learning_efficiency", None),
                "processing_latency": getattr(metrics, "processing_latency", None),
                "neural_state": getattr(
                    getattr(metrics, "neural_state", None), "value", None
                ),
                "learning_stage": getattr(
                    getattr(metrics, "learning_stage", None), "value", None
                ),
                "timestamp": (
                    getattr(metrics, "timestamp").isoformat()  # type: ignore[union-attr]
                    if getattr(metrics, "timestamp", None) is not None
                    else None
                ),
            },
            "ingested_at": datetime.utcnow().isoformat(),
        }
        fn = OUT_DIR / f"local_store_{_ts()}.json"
        fn.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return True

    # Monkeypatch store method
    try:
        engine.store_ingested_data = _store_local  # type: ignore[attr-defined]
    except Exception:
        pass

    results = await engine.run_full_ingestion_cycle()
    # Persist cycle results
    cycle_path = OUT_DIR / f"cycle_{_ts()}.json"
    cycle_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


async def main(cycles: int, sleep_seconds: int) -> int:
    # Ensure import doesn't fail if MNE is missing by installing a lightweight stub
    try:
        import mne  # type: ignore
    except Exception:
        import sys
        import types

        mne = types.ModuleType("mne")
        # attach a minimal io namespace with expected attribute
        setattr(mne, "io", types.SimpleNamespace())

        def _stub_read_raw_edf(*args, **kwargs):
            raise RuntimeError(
                "MNE not installed; EDF parsing unavailable in local mode"
            )

        setattr(mne.io, "read_raw_edf", _stub_read_raw_edf)
        sys.modules["mne"] = mne

    # Provide minimal experimentP2L stubs if missing
    try:
        import experimentP2L  # type: ignore  # noqa: F401
    except Exception:
        import sys
        import types
        from dataclasses import dataclass
        from enum import Enum

        exp = types.ModuleType("experimentP2L")

        class LearningStage(Enum):
            INTEGRATION = "integration"
            ADAPTATION = "adaptation"

        class NeuralState(Enum):
            LEARNING = "learning"
            BASELINE = "baseline"

        @dataclass
        class EEGMetrics:
            alpha_power: float
            beta_power: float
            theta_power: float
            gamma_power: float
            coherence_score: float
            learning_efficiency: float
            processing_latency: float
            neural_state: NeuralState
            learning_stage: LearningStage
            timestamp: datetime

        setattr(exp, "LearningStage", LearningStage)
        setattr(exp, "NeuralState", NeuralState)
        setattr(exp, "EEGMetrics", EEGMetrics)
        sys.modules["experimentP2L"] = exp

    from external_eeg_ingestion_engine import ExternalEEGIngestionEngine

    engine = ExternalEEGIngestionEngine()
    # Prefer OpenNeuro-only datasets in local mode to avoid EDF parsing
    try:
        engine.datasets = [d for d in engine.datasets if getattr(d, "dataset_type", "") == "openneuro"]  # type: ignore[attr-defined]
    except Exception:
        pass
    all_results: List[Dict[str, Any]] = []

    for i in range(cycles):
        print(f"\n=== Ingestion cycle {i+1}/{cycles} ===")
        res = await _run_cycle(engine)
        all_results.append(res)
        if i < cycles - 1 and sleep_seconds > 0:
            await asyncio.sleep(sleep_seconds)

    # Write aggregate
    agg_path = OUT_DIR / f"aggregate_{_ts()}.json"
    agg_path.write_text(json.dumps({"cycles": all_results}, indent=2), encoding="utf-8")
    print(f"Wrote results to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=int, default=5)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.cycles, args.sleep_seconds)))
