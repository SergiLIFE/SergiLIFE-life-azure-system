"""
Venturi Gates System - Revolutionary Fluid Dynamics + AI Integration
Advanced control system for L.I.F.E Theory enhancement

Copyright 2025 - Sergio Paya Borrull
"""

import logging
import math
import statistics
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

# import numpy as np  # Temporarily commented out due to space constraints

logger = logging.getLogger(__name__)


class VenturiGateType(Enum):
    """Types of Venturi gates for different applications"""

    SIGNAL_ENHANCEMENT = "signal_enhancement"
    NOISE_REDUCTION = "noise_reduction"
    PATTERN_EXTRACTION = "pattern_extraction"
    ADAPTIVE_FILTERING = "adaptive_filtering"


@dataclass
class VenturiGateConfig:
    """Configuration for individual Venturi gate"""

    gate_id: str
    gate_type: VenturiGateType
    constriction_factor: float = 0.8
    acceleration_factor: float = 1.2
    adaptation_rate: float = 0.01
    efficiency_threshold: float = 0.7


class VenturiGate:
    """Individual Venturi gate implementing fluid dynamics principles"""

    def __init__(self, config: VenturiGateConfig):
        self.config = config
        self.state = 1.0  # Current gate state
        self.efficiency = 1.0  # Current efficiency
        self.processing_history: List[float] = []

        logger.info(f"Venturi Gate {config.gate_id} initialized: {config.gate_type}")

    def process_signal(self, signal: Any, context: Dict[str, Any] = None) -> Any:
        """Apply Venturi effect to signal processing"""
        if context is None:
            context = {}

        # Apply Venturi fluid dynamics principles
        processed = self._apply_venturi_effect(signal)

        # Record processing performance
        performance = self._assess_performance(signal, processed)
        self.processing_history.append(performance)

        # Adapt gate based on performance
        self._adapt_gate(performance)

        return processed

    def _apply_venturi_effect(self, signal):
        """Core Venturi effect application"""
        # Venturi equation: velocity increases as area decreases
        # P1 + 0.5*ρ*v1² = P2 + 0.5*ρ*v2²

        # Constriction phase: signal compression
        constriction_factor = self.config.constriction_factor * self.state
        constricted = [s * constriction_factor for s in signal]

        # Acceleration phase: velocity increase through narrow section
        acceleration = self.config.acceleration_factor * self.efficiency
        accelerated = [c * acceleration for c in constricted]

        # Apply gate-specific processing
        processed = self._apply_gate_specific_processing(accelerated)

        return processed

    def _apply_gate_specific_processing(self, signal):
        """Apply gate-type-specific processing"""
        if self.config.gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
            return self._enhance_signal(signal)
        elif self.config.gate_type == VenturiGateType.NOISE_REDUCTION:
            return self._reduce_noise(signal)
        elif self.config.gate_type == VenturiGateType.PATTERN_EXTRACTION:
            return self._extract_patterns(signal)
        elif self.config.gate_type == VenturiGateType.ADAPTIVE_FILTERING:
            return self._adaptive_filter(signal)
        else:
            return signal

    def _enhance_signal(self, signal):
        """Signal enhancement through Venturi acceleration"""
        # Enhance signal amplitude based on local characteristics
        local_std = statistics.stdev(signal) if len(signal) > 1 else 0.0
        enhancement_factor = 1.0 + 0.1 * self.efficiency / (1.0 + local_std)
        return [s * enhancement_factor for s in signal]

    def _reduce_noise(self, signal: List[float]) -> List[float]:
        """Noise reduction through selective Venturi filtering"""
        # Apply adaptive threshold based on signal characteristics
        threshold = statistics.stdev(signal) * (2.0 - self.efficiency)

        # Selective filtering: preserve signal, reduce noise
        filtered = signal.copy()
        noise_mask = [abs(s) < threshold for s in signal]
        filtered = [
            f * self.efficiency if mask else f for f, mask in zip(filtered, noise_mask)
        ]

        return filtered

    def _extract_patterns(self, signal: List[float]) -> List[float]:
        """Pattern extraction using Venturi flow dynamics"""
        # Use Venturi pressure differential to highlight patterns
        window_size = max(5, len(signal) // 20)

        if len(signal) < window_size:
            return signal

        # Calculate local patterns using moving windows
        patterns = []
        for i in range(len(signal) - window_size + 1):
            window = signal[i : i + window_size]
            # Calculate variance manually
            mean_val = sum(window) / len(window)
            variance = sum((x - mean_val) ** 2 for x in window) / len(window)
            pattern_strength = variance * self.efficiency
            patterns.append(pattern_strength)

        # Pad to match original length
        while len(patterns) < len(signal):
            patterns.append(patterns[-1])

        return patterns

    def _adaptive_filter(self, signal: List[float]) -> List[float]:
        """Adaptive filtering using Venturi principles"""
        # Adapt filter characteristics based on signal properties
        mean_val = sum(signal) / len(signal)
        variance = sum((x - mean_val) ** 2 for x in signal) / len(signal)
        filter_strength = self.efficiency * (1.0 + variance)

        # Simple adaptive moving average
        window_size = max(3, int(filter_strength * 10))
        if window_size >= len(signal):
            return signal

        # Manual convolution with moving average
        filtered = []
        for i in range(len(signal)):
            start = max(0, i - window_size // 2)
            end = min(len(signal), i + window_size // 2 + 1)
            window = signal[start:end]
            avg = sum(window) / len(window)
            filtered.append(avg)

        return filtered

    def _assess_performance(
        self, input_signal: List[float], output_signal: List[float]
    ) -> float:
        """Assess processing performance"""
        # Calculate improvement metrics
        input_noise = self._estimate_noise_level(input_signal)
        output_noise = self._estimate_noise_level(output_signal)

        # Performance based on noise reduction and signal preservation
        def calc_variance(sig):
            mean_val = sum(sig) / len(sig)
            return sum((x - mean_val) ** 2 for x in sig) / len(sig)

        input_var = calc_variance(input_signal)
        output_var = calc_variance(output_signal)

        noise_reduction = max(0, input_noise - output_noise) / max(input_noise, 0.001)
        signal_preservation = 1.0 - abs(output_var - input_var) / max(input_var, 0.001)

        performance = 0.6 * noise_reduction + 0.4 * signal_preservation
        return max(0.0, min(1.0, performance))

    def _estimate_noise_level(self, signal: List[float]) -> float:
        """Estimate noise level in signal"""
        # Simple noise estimation using high-frequency content
        if len(signal) < 10:
            return 0.0

        # High-frequency component as noise proxy
        diff_signal = []
        for i in range(2, len(signal)):
            # Second derivative approximation
            diff_signal.append(signal[i] - 2 * signal[i - 1] + signal[i - 2])

        if diff_signal:
            noise_level = statistics.stdev(diff_signal)
        else:
            noise_level = 0.0
        return noise_level

    def _adapt_gate(self, performance: float) -> None:
        """Adapt gate parameters based on performance"""
        # Update gate state
        performance_delta = performance - 0.5  # Target performance = 0.5
        state_adjustment = self.config.adaptation_rate * performance_delta
        self.state = max(0.1, min(2.0, self.state + state_adjustment))

        # Update efficiency
        if len(self.processing_history) >= 10:
            recent_performance = sum(self.processing_history[-10:]) / len(
                self.processing_history[-10:]
            )
            if recent_performance > self.config.efficiency_threshold:
                self.efficiency = min(2.0, self.efficiency * 1.01)
            else:
                self.efficiency = max(0.5, self.efficiency * 0.99)

    def get_gate_metrics(self) -> Dict[str, float]:
        """Get current gate metrics"""
        return {
            "state": self.state,
            "efficiency": self.efficiency,
            "recent_performance": (
                sum(self.processing_history[-10:]) / len(self.processing_history[-10:])
                if len(self.processing_history) >= 10
                else 0.0
            ),
            "total_processes": len(self.processing_history),
        }


class VenturiGatesSystem:
    """Complete Venturi Gates System - Revolutionary Control Architecture"""

    def __init__(self, gate_configs: List[VenturiGateConfig] = None):
        if gate_configs is None:
            gate_configs = self._create_default_gates()

        self.gates: Dict[str, VenturiGate] = {}
        for config in gate_configs:
            self.gates[config.gate_id] = VenturiGate(config)

        self.system_efficiency = 1.0
        self.processing_pipeline = list(self.gates.keys())

        logger.info(f"Venturi Gates System initialized with {len(self.gates)} gates")

    def _create_default_gates(self) -> List[VenturiGateConfig]:
        """Create default 3-gate Venturi system configuration"""
        return [
            VenturiGateConfig(
                gate_id="venturi1",
                gate_type=VenturiGateType.SIGNAL_ENHANCEMENT,
                constriction_factor=0.8,
                acceleration_factor=1.3,
            ),
            VenturiGateConfig(
                gate_id="venturi2",
                gate_type=VenturiGateType.NOISE_REDUCTION,
                constriction_factor=0.7,
                acceleration_factor=1.4,
            ),
            VenturiGateConfig(
                gate_id="venturi3",
                gate_type=VenturiGateType.PATTERN_EXTRACTION,
                constriction_factor=0.75,
                acceleration_factor=1.35,
            ),
        ]

    def process_through_gates(
        self, signal: List[float], context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process signal through complete Venturi gate system"""
        if context is None:
            context = {}

        results = {
            "input_signal": signal.copy(),
            "gate_outputs": {},
            "processing_metrics": {},
            "final_output": None,
        }

        current_signal = signal.copy()

        # Process through each gate in pipeline
        for gate_id in self.processing_pipeline:
            gate = self.gates[gate_id]

            # Process signal through current gate
            gate_output = gate.process_signal(current_signal, context)

            # Record results
            results["gate_outputs"][gate_id] = gate_output.copy()
            results["processing_metrics"][gate_id] = gate.get_gate_metrics()

            # Update signal for next gate
            current_signal = gate_output

        results["final_output"] = current_signal

        # Update system efficiency
        self._update_system_efficiency()
        results["system_efficiency"] = self.system_efficiency

        return results

    def process_parallel_gates(
        self, signal: List[float], context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process signal through gates in parallel configuration"""
        if context is None:
            context = {}

        results = {
            "input_signal": signal.copy(),
            "parallel_outputs": {},
            "processing_metrics": {},
            "combined_output": None,
        }

        parallel_outputs = []

        # Process through all gates in parallel
        for gate_id, gate in self.gates.items():
            gate_output = gate.process_signal(signal.copy(), context)
            results["parallel_outputs"][gate_id] = gate_output
            results["processing_metrics"][gate_id] = gate.get_gate_metrics()
            parallel_outputs.append(gate_output)

        # Combine parallel outputs
        if parallel_outputs:
            # Weighted combination based on gate efficiency
            weights = []
            for gate in self.gates.values():
                weights.append(gate.efficiency)

            total_weight = sum(weights)
            weights = [w / total_weight for w in weights]

            combined = [0.0] * len(signal)
            for i, output in enumerate(parallel_outputs):
                combined = [c + weights[i] * o for c, o in zip(combined, output)]

            results["combined_output"] = combined

        self._update_system_efficiency()
        results["system_efficiency"] = self.system_efficiency

        return results

    def _update_system_efficiency(self) -> None:
        """Update overall system efficiency"""
        gate_efficiencies = [gate.efficiency for gate in self.gates.values()]
        self.system_efficiency = sum(gate_efficiencies) / len(gate_efficiencies)

    def optimize_pipeline(self) -> None:
        """Optimize gate processing pipeline order"""
        # Sort gates by efficiency for optimal processing order
        gate_efficiencies = [
            (gate_id, self.gates[gate_id].efficiency) for gate_id in self.gates.keys()
        ]
        gate_efficiencies.sort(key=lambda x: x[1], reverse=True)

        self.processing_pipeline = [gate_id for gate_id, _ in gate_efficiencies]

        logger.info(f"Pipeline optimized: {self.processing_pipeline}")

    def add_gate(self, config: VenturiGateConfig) -> None:
        """Add new gate to system"""
        self.gates[config.gate_id] = VenturiGate(config)
        if config.gate_id not in self.processing_pipeline:
            self.processing_pipeline.append(config.gate_id)

        logger.info(f"Added gate {config.gate_id} to system")

    def remove_gate(self, gate_id: str) -> None:
        """Remove gate from system"""
        if gate_id in self.gates:
            del self.gates[gate_id]
            if gate_id in self.processing_pipeline:
                self.processing_pipeline.remove(gate_id)

            logger.info(f"Removed gate {gate_id} from system")

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "gate_count": len(self.gates),
            "system_efficiency": self.system_efficiency,
            "processing_pipeline": self.processing_pipeline,
            "gate_metrics": {},
        }

        for gate_id, gate in self.gates.items():
            status["gate_metrics"][gate_id] = gate.get_gate_metrics()

        return status

    def demonstrate_venturi_system(
        self, test_signal: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Demonstrate Venturi Gates System capabilities"""
        if test_signal is None:
            # Create test signal with noise
            import random

            t = [i / 1000 for i in range(1000)]
            test_signal = [
                math.sin(2 * math.pi * 5 * ti) + 0.3 * random.gauss(0, 1) for ti in t
            ]

        demonstration = {
            "test_signal": test_signal,
            "serial_processing": self.process_through_gates(test_signal),
            "parallel_processing": self.process_parallel_gates(test_signal),
            "system_status": self.get_system_status(),
        }

        return demonstration


# Factory functions for easy creation
def create_3_venturi_system() -> VenturiGatesSystem:
    """Create the revolutionary 3-Venturi Control System"""
    return VenturiGatesSystem()


def create_venturi_system() -> VenturiGatesSystem:
    """Create the revolutionary 3-Venturi Control System (alias)"""
    return create_3_venturi_system()


def create_custom_venturi_system(
    gate_configs: List[Dict[str, Any]],
) -> VenturiGatesSystem:
    """Create custom Venturi system from configuration"""
    configs = []
    for i, config_dict in enumerate(gate_configs):
        config = VenturiGateConfig(
            gate_id=config_dict.get("gate_id", f"venturi{i+1}"),
            gate_type=VenturiGateType(
                config_dict.get("gate_type", "signal_enhancement")
            ),
            constriction_factor=config_dict.get("constriction_factor", 0.8),
            acceleration_factor=config_dict.get("acceleration_factor", 1.2),
            adaptation_rate=config_dict.get("adaptation_rate", 0.01),
            efficiency_threshold=config_dict.get("efficiency_threshold", 0.7),
        )
        configs.append(config)

    return VenturiGatesSystem(configs)


# Example usage and demonstration
if __name__ == "__main__":
    # Create 3-Venturi Control System
    venturi_system = create_3_venturi_system()

    # Demonstrate system capabilities
    demo_results = venturi_system.demonstrate_venturi_system()

    print("3-Venturi Control System Demonstration")
    print("=" * 50)
    print(
        f"System Efficiency: {demo_results['system_status']['system_efficiency']:.3f}"
    )
    print(
        f"Processing Pipeline: {demo_results['system_status']['processing_pipeline']}"
    )

    # Show gate metrics
    print("\nGate Performance Metrics:")
    for gate_id, metrics in demo_results["system_status"]["gate_metrics"].items():
        print(
            f"  {gate_id}: Efficiency={metrics['efficiency']:.3f}, State={metrics['state']:.3f}"
        )

    # Optimize and show improvement
    venturi_system.optimize_pipeline()
    optimized_status = venturi_system.get_system_status()
    print(f"\nOptimized Pipeline: {optimized_status['processing_pipeline']}")
    print(f"Optimized Efficiency: {optimized_status['system_efficiency']:.3f}")

    print("\nVenturi Gates System demonstration completed successfully!")
