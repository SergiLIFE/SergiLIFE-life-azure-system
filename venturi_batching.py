#!/usr/bin/env python3
"""
Venturi Batching System - Dynamic Batch Size Optimization
L.I.F.E. Platform Venturi-inspired batch optimization for neural processing

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import logging
import statistics  # Use built-in statistics instead of numpy
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# import numpy as np  # Temporarily commented out due to space constraints

logger = logging.getLogger(__name__)


@dataclass
class BatchMetrics:
    """Metrics for batch processing performance"""

    batch_size: int
    processing_time: float
    throughput: float
    memory_usage: float
    accuracy: float
    timestamp: float


class VenturiBatcher:
    """
    Venturi-inspired dynamic batch sizing system
    Optimizes batch sizes based on system load and performance metrics
    """

    def __init__(
        self,
        min_batch_size: int = 1,
        max_batch_size: int = 512,
        target_latency: float = 0.1,
        adaptation_rate: float = 0.1,
    ):
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.target_latency = target_latency
        self.adaptation_rate = adaptation_rate

        self.current_batch_size = 32  # Starting batch size
        self.metrics_history: List[BatchMetrics] = []
        self.performance_window = 10  # Rolling window for metrics

        logger.info(
            f"VenturiBatcher initialized: batch_size={self.current_batch_size}, "
            f"target_latency={target_latency}s"
        )

    def optimize_batch_size(self, current_metrics: BatchMetrics) -> int:
        """
        Optimize batch size using Venturi principles
        Based on fluid dynamics: constriction factor and flow acceleration
        """
        self.metrics_history.append(current_metrics)

        # Keep only recent metrics
        if len(self.metrics_history) > self.performance_window:
            self.metrics_history.pop(0)

        if len(self.metrics_history) < 3:
            return self.current_batch_size

        # Calculate performance trends
        recent_metrics = self.metrics_history[-3:]
        avg_latency = sum(m.processing_time for m in recent_metrics) / len(
            recent_metrics
        )
        avg_throughput = sum(m.throughput for m in recent_metrics) / len(recent_metrics)

        # Venturi optimization logic
        latency_ratio = avg_latency / self.target_latency

        if latency_ratio > 1.2:  # Too slow, reduce batch size
            constriction_factor = 0.8
        elif latency_ratio < 0.8:  # Fast enough, can increase batch size
            constriction_factor = 1.1
        else:  # Optimal range
            constriction_factor = 1.0

        # Calculate new batch size
        new_batch_size = int(self.current_batch_size * constriction_factor)

        # Apply bounds
        new_batch_size = max(
            self.min_batch_size, min(self.max_batch_size, new_batch_size)
        )

        # Smooth transitions (don't change too drastically)
        max_change = int(self.current_batch_size * 0.3)
        if abs(new_batch_size - self.current_batch_size) > max_change:
            if new_batch_size > self.current_batch_size:
                new_batch_size = self.current_batch_size + max_change
            else:
                new_batch_size = self.current_batch_size - max_change

        self.current_batch_size = new_batch_size

        logger.debug(
            f"Batch size optimized: {self.current_batch_size} "
            f"(latency: {avg_latency:.3f}s, throughput: {avg_throughput:.1f})"
        )

        return self.current_batch_size

    def get_batch_suggestion(self, queue_depth: int, system_load: float) -> int:
        """
        Get batch size suggestion based on current system state
        """
        # Adjust for queue depth (more items waiting = larger batches)
        queue_factor = min(2.0, max(0.5, queue_depth / 10))

        # Adjust for system load (higher load = smaller batches)
        load_factor = max(0.3, 1.0 - system_load)

        suggested_size = int(self.current_batch_size * queue_factor * load_factor)
        suggested_size = max(
            self.min_batch_size, min(self.max_batch_size, suggested_size)
        )

        return suggested_size

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of batching performance"""
        if not self.metrics_history:
            return {"status": "no_data"}

        recent = self.metrics_history[-min(10, len(self.metrics_history)) :]

        return {
            "current_batch_size": self.current_batch_size,
            "avg_latency": sum(m.processing_time for m in recent) / len(recent),
            "avg_throughput": sum(m.throughput for m in recent) / len(recent),
            "avg_accuracy": sum(m.accuracy for m in recent) / len(recent),
            "optimization_efficiency": self._calculate_efficiency(),
            "metrics_count": len(self.metrics_history),
        }

    def _calculate_efficiency(self) -> float:
        """Calculate optimization efficiency score"""
        if len(self.metrics_history) < 2:
            return 0.0

        # Efficiency based on latency stability and throughput
        latencies = [m.processing_time for m in self.metrics_history]
        latency_std = statistics.stdev(latencies) if len(latencies) > 1 else 0
        latency_mean = sum(latencies) / len(latencies)

        # Lower coefficient of variation = higher efficiency
        cv = latency_std / latency_mean if latency_mean > 0 else 1.0
        efficiency = max(0.0, 1.0 - cv)

        return efficiency


class AdaptiveBatchProcessor:
    """
    Adaptive batch processor using Venturi batching system
    """

    def __init__(self, batcher: Optional[VenturiBatcher] = None):
        self.batcher = batcher or VenturiBatcher()
        self.processing_queue: List[Any] = []
        self.is_processing = False

    async def add_to_batch(self, item: Any) -> None:
        """Add item to processing batch"""
        self.processing_queue.append(item)

        # Auto-trigger processing if queue gets large
        if len(self.processing_queue) >= self.batcher.current_batch_size:
            await self.process_batch()

    async def process_batch(self) -> List[Any]:
        """Process current batch with performance monitoring"""
        if not self.processing_queue or self.is_processing:
            return []

        self.is_processing = True
        batch = self.processing_queue[: self.batcher.current_batch_size]
        self.processing_queue = self.processing_queue[self.batcher.current_batch_size :]

        try:
            start_time = time.time()

            # Simulate processing (replace with actual processing logic)
            results = await self._process_batch_items(batch)

            processing_time = time.time() - start_time
            batch_size = len(batch)

            # Calculate metrics
            metrics = BatchMetrics(
                batch_size=batch_size,
                processing_time=processing_time,
                throughput=batch_size / processing_time if processing_time > 0 else 0,
                memory_usage=0.0,  # Would need actual memory monitoring
                accuracy=0.95,  # Would need actual accuracy calculation
                timestamp=time.time(),
            )

            # Optimize batch size for next iteration
            self.batcher.optimize_batch_size(metrics)

            logger.info(
                f"Processed batch of {batch_size} items in {processing_time:.3f}s "
                f"(throughput: {metrics.throughput:.1f} items/s)"
            )

            return results

        finally:
            self.is_processing = False

    async def _process_batch_items(self, batch: List[Any]) -> List[Any]:
        """Process individual batch items"""
        # Placeholder - replace with actual processing logic
        await asyncio.sleep(0.01)  # Simulate processing time
        return [f"processed_{item}" for item in batch]

    def get_status(self) -> Dict[str, Any]:
        """Get current processor status"""
        return {
            "queue_depth": len(self.processing_queue),
            "current_batch_size": self.batcher.current_batch_size,
            "is_processing": self.is_processing,
            "performance": self.batcher.get_performance_summary(),
        }


# Global instance for easy access
venturi_batcher = VenturiBatcher()
adaptive_processor = AdaptiveBatchProcessor(venturi_batcher)


if __name__ == "__main__":
    # Example usage
    async def demo():
        print("Venturi Batching System Demo")
        print("=" * 40)

        # Add items to batch
        for i in range(50):
            await adaptive_processor.add_to_batch(f"item_{i}")

        # Process remaining items
        while adaptive_processor.processing_queue:
            await adaptive_processor.process_batch()

        # Show final status
        status = adaptive_processor.get_status()
        print(f"\nFinal Status: {status}")

    asyncio.run(demo())
