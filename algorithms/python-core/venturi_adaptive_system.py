"""
Venturi Adaptive System

Physics-inspired adaptive controllers used by the L.I.F.E. platform to balance
cognitive load, rendering complexity, and cloud offloading in real time. All
components are dependency-light and safe to import in offline environments.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence

try:  # Optional scientific acceleration
    import numpy as _np  # type: ignore[import]

    _NUMPY_AVAILABLE = True
except Exception:  # pragma: no cover - allow execution without NumPy
    _np = None  # type: ignore[assignment]
    _NUMPY_AVAILABLE = False


logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    if _NUMPY_AVAILABLE and _np is not None:
        return float(_np.clip(value, low, high))  # type: ignore[arg-type]
    return max(low, min(high, value))


@dataclass
class VenturiBatchController:
    """Adjusts batch sizes based on latency, queue depth, and error rates."""

    minbatch: int = 8
    maxbatch: int = 128
    targetlatency: float = 50.0
    maxqueuesize: int = 100
    batchsize: int = 8

    def __post_init__(self) -> None:
        self.batchsize = self.minbatch

    def adjust(self, lastlatency: float, queuesize: int, recenterrorrate: float) -> int:
        if queuesize > 0.8 * self.maxqueuesize or recenterrorrate > 0.1:
            self.batchsize = max(self.minbatch, int(self.batchsize / 1.5))
        elif lastlatency < self.targetlatency and queuesize < 0.5 * self.maxqueuesize:
            self.batchsize = min(self.maxbatch, int(self.batchsize * 1.5))
        if recenterrorrate > 0.2:
            self.batchsize = self.minbatch
        logger.debug(
            "VenturiBatchController.adjust -> batch=%s latency=%.3f queue=%s error=%.3f",
            self.batchsize,
            lastlatency,
            queuesize,
            recenterrorrate,
        )
        return self.batchsize


@dataclass
class VenturiBatcher:
    """Lightweight adaptive batch window using Venturi-style flow logic."""

    minbatch: int = 8
    maxbatch: int = 128
    targetlatency: float = 50.0
    gamma: float = 1.5
    batchsize: int = 8
    batchhistory: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.batchsize = max(self.minbatch, min(self.maxbatch, self.batchsize))

    def update(self, lastlatency: float) -> int:
        if lastlatency < self.targetlatency:
            self.batchsize = min(self.maxbatch, int(self.batchsize * self.gamma))
        else:
            self.batchsize = max(self.minbatch, int(self.batchsize / self.gamma))
        self.batchhistory.append(self.batchsize)
        logger.debug(
            "VenturiBatcher.update -> latency=%.3f gamma=%.2f batch=%s",
            lastlatency,
            self.gamma,
            self.batchsize,
        )
        return self.batchsize


class VenturiScheduler:
    """Splits inbound data based on current throughput capacity."""

    def __init__(self, maxthroughput: float = 1e6) -> None:
        self.maxthroughput = maxthroughput

    def optimizeflow(self, incomingdata: Sequence[Any]) -> List[Sequence[Any]]:
        if not incomingdata:
            return []
        batchsize = max(1, int(self.maxthroughput / (len(incomingdata) + 1)))
        batches: List[Sequence[Any]] = []
        for start in range(0, len(incomingdata), batchsize):
            batches.append(incomingdata[start : start + batchsize])
        logger.debug(
            "VenturiScheduler.optimizeflow -> volume=%s batch=%s batches=%s",
            len(incomingdata),
            batchsize,
            len(batches),
        )
        return batches


class CognitiveVenturi:
    """Maps EEG-derived velocity and stress to a normalized cognitive load."""

    def calculate(self, eegdata: Dict[str, float]) -> float:
        g = 9.81
        density = 1.225
        v = float(eegdata.get("focusvelocity", 0.0))
        Pg = float(eegdata.get("stresspressure", 0.0))
        z = max(0.1, float(eegdata.get("neuroplasticity", 0.5)))
        load = (v ** 2) / (2 * g * z) + Pg / (density * g)
        result = _clip(load)
        logger.debug("CognitiveVenturi.calculate -> %.5f", result)
        return result


class RenderingVenturi:
    """Balances rendering demand against hardware capacity and cognitive load."""

    def adjust(self, renderdata: Dict[str, float], cognitiveload: float) -> float:
        framerate = float(renderdata.get("framerate", 60.0))
        hardware_capacity = max(1.0, float(renderdata.get("hardwarecapacity", 10.0)))
        render_demand = float(renderdata.get("renderdemand", 0.5))
        throughput = (framerate ** 2) / hardware_capacity + 0.7 * render_demand
        adjusted = self.adaptquality(throughput, cognitiveload)
        logger.debug(
            "RenderingVenturi.adjust -> raw=%.5f adjusted=%.5f cognitive=%.5f",
            throughput,
            adjusted,
            cognitiveload,
        )
        return adjusted

    @staticmethod
    def adaptquality(renderthroughput: float, cognitiveload: float) -> float:
        if cognitiveload > 0.8:
            return renderthroughput * 0.6
        return renderthroughput


class CloudVenturi:
    """Determines optimal offload throughput based on bandwidth and latency."""

    async def optimize(self, clouddata: Dict[str, float], renderquality: float) -> float:
        bandwidth = float(clouddata.get("bandwidth", 50.0))
        latency = float(clouddata.get("latency", 20.0))
        datasensitivity = float(clouddata.get("datasensitivity", 0.5))
        throughput = (bandwidth / (latency + 1.0)) * datasensitivity + renderquality
        logger.debug(
            "CloudVenturi.optimize -> bandwidth=%.3f latency=%.3f sensitivity=%.3f result=%.5f",
            bandwidth,
            latency,
            datasensitivity,
            throughput,
        )
        await asyncio.sleep(0)
        return throughput


class VenturiSystem:
    """High-level facade exposing the three Venturi modules."""

    def __init__(self) -> None:
        self.cognitive = CognitiveVenturi()
        self.rendering = RenderingVenturi()
        self.cloud = CloudVenturi()

    async def balancesystem(
        self,
        eegdata: Dict[str, float],
        renderdata: Dict[str, float],
        clouddata: Dict[str, float],
    ) -> tuple[float, float, float]:
        cognitive_load = self.cognitive.calculate(eegdata)
        render_rate = self.rendering.adjust(renderdata, cognitive_load)
        offload = await self.cloud.optimize(clouddata, render_rate)
        return (cognitive_load, render_rate, offload)


__all__ = [
    "VenturiBatchController",
    "VenturiBatcher",
    "VenturiScheduler",
    "CognitiveVenturi",
    "RenderingVenturi",
    "CloudVenturi",
    "VenturiSystem",
]
