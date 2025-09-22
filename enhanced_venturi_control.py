#!/usr/bin/env python3
"""
Enhanced Venturi Control System - Advanced Fluid Dynamics Processing
Real-time adaptive control for three Venturi gates with fluid dynamics optimization

This module provides advanced control algorithms for the L.I.F.E. Platform's
three Venturi gates, implementing fluid dynamics principles for ultra-low latency
EEG signal processing.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import logging
import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VenturiGateType(Enum):
    """Types of Venturi gates for different processing functions"""

    SIGNAL_ENHANCEMENT = "signal_enhancement"
    NOISE_REDUCTION = "noise_reduction"
    PATTERN_EXTRACTION = "pattern_extraction"


@dataclass
class FluidDynamicsConfig:
    """Configuration for fluid dynamics processing"""

    constriction_ratio: float = 0.8  # Venturi constriction factor
    acceleration_factor: float = 1.2  # Signal acceleration multiplier
    pressure_drop_coefficient: float = 0.7  # Bernoulli pressure drop
    turbulence_threshold: float = 0.1  # Turbulence detection threshold
    flow_stability_factor: float = 0.95  # Flow stability coefficient
    adaptation_rate: float = 0.01  # Learning adaptation rate
    resonance_frequency: float = 10.0  # Hz, natural resonance frequency


@dataclass
class VenturiGateState:
    """Real-time state of a Venturi gate"""

    pressure: float = 1.0
    velocity: float = 1.0
    flow_rate: float = 1.0
    turbulence_level: float = 0.0
    efficiency: float = 1.0
    adaptation_level: float = 0.0
    resonance_phase: float = 0.0
    last_update: float = field(default_factory=time.time)


@dataclass
class VenturiGateConfig:
    """Configuration for individual Venturi gate"""

    gate_id: str
    gate_type: VenturiGateType
    fluid_config: FluidDynamicsConfig = field(default_factory=FluidDynamicsConfig)
    max_pressure: float = 2.0
    min_pressure: float = 0.1
    max_velocity: float = 5.0
    adaptation_enabled: bool = True


class EnhancedVenturiGate:
    """
    Enhanced Venturi Gate with advanced fluid dynamics control

    Implements Bernoulli's principle and fluid dynamics for signal processing:
    - Pressure drop creates velocity increase (signal enhancement)
    - Turbulence control for noise reduction
    - Flow resonance for pattern extraction
    """

    def __init__(self, config: VenturiGateConfig):
        self.config = config
        self.state = VenturiGateState()
        self.history = []
        self.fluid_dynamics = self._initialize_fluid_dynamics()
        self.adaptive_controller = AdaptiveController(config.fluid_config)

        logger.info(
            f"Enhanced Venturi Gate '{config.gate_id}' initialized: {config.gate_type.value}"
        )

    def _initialize_fluid_dynamics(self) -> Dict[str, Any]:
        """Initialize fluid dynamics parameters"""
        return {
            "constriction_area": 1.0 * self.config.fluid_config.constriction_ratio,
            "upstream_area": 1.0,
            "pressure_coefficient": self.config.fluid_config.pressure_drop_coefficient,
            "velocity_coefficient": 1.0
            / math.sqrt(self.config.fluid_config.constriction_ratio),
            "reynolds_number": 1000.0,  # Laminar flow
            "viscosity": 0.001,  # Fluid viscosity
            "density": 1000.0,  # Fluid density
        }

    async def process_signal(
        self, input_signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """
        Process signal through Venturi gate using fluid dynamics principles

        Args:
            input_signal: Input signal array
            context: Processing context (optional)

        Returns:
            Processed signal array
        """
        start_time = time.perf_counter()

        # Apply fluid dynamics transformation
        processed = await self._apply_fluid_dynamics(input_signal, context)

        # Update gate state
        self._update_gate_state(processed, time.perf_counter() - start_time)

        # Adaptive learning
        if self.config.adaptation_enabled:
            await self.adaptive_controller.adapt(self.state, processed)

        return processed

    async def _apply_fluid_dynamics(
        self, signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Apply fluid dynamics transformation based on gate type"""
        if self.config.gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
            return await self._enhance_signal(signal, context)
        elif self.config.gate_type == VenturiGateType.NOISE_REDUCTION:
            return await self._reduce_noise(signal, context)
        elif self.config.gate_type == VenturiGateType.PATTERN_EXTRACTION:
            return await self._extract_patterns(signal, context)
        else:
            return signal

    async def _enhance_signal(
        self, signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Signal enhancement using Venturi pressure-velocity conversion"""
        # Bernoulli's principle: P1 + 1/2ρv1² = P2 + 1/2ρv2²
        # Pressure drop creates velocity increase (signal amplification)

        pressure_drop = self.config.fluid_config.pressure_drop_coefficient
        velocity_gain = self.config.fluid_config.acceleration_factor

        # Apply pressure drop (attenuation) followed by velocity gain (amplification)
        attenuated = signal * (1.0 - pressure_drop)
        enhanced = attenuated * velocity_gain

        # Add resonance for frequency-specific enhancement
        resonance_freq = self.config.fluid_config.resonance_frequency
        enhanced = self._apply_resonance_filter(enhanced, resonance_freq)

        return enhanced

    async def _reduce_noise(
        self, signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Noise reduction using laminar flow stabilization"""
        # Turbulence creates noise - stabilize flow for noise reduction

        # Calculate turbulence level
        turbulence = self._calculate_turbulence(signal)

        # Apply laminar flow stabilization
        if turbulence > self.config.fluid_config.turbulence_threshold:
            # Reduce high-frequency turbulence (noise)
            stabilized = self._apply_laminar_filter(signal, turbulence)
        else:
            stabilized = signal

        # Apply flow stability factor
        stability_factor = self.config.fluid_config.flow_stability_factor
        stabilized = stabilized * stability_factor + signal * (1 - stability_factor)

        return stabilized

    async def _extract_patterns(
        self, signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Pattern extraction using flow resonance and harmonic analysis"""
        # Extract patterns through resonant frequency matching

        # Apply multi-harmonic resonance
        harmonics = [1.0, 2.0, 3.0]  # Fundamental and harmonics
        pattern_signal = np.zeros_like(signal)

        for harmonic in harmonics:
            freq = self.config.fluid_config.resonance_frequency * harmonic
            resonant_component = self._apply_resonance_filter(signal, freq)
            pattern_signal += resonant_component * (
                1.0 / harmonic
            )  # Weighted harmonics

        # Enhance pattern clarity through phase alignment
        pattern_signal = self._align_phases(pattern_signal)

        return pattern_signal

    def _apply_resonance_filter(
        self, signal: np.ndarray, frequency: float
    ) -> np.ndarray:
        """Apply resonant filter at specific frequency"""
        # Simple resonant filter implementation
        dt = 1.0 / 1000.0  # Assume 1000 Hz sampling
        omega = 2 * math.pi * frequency
        damping = 0.1  # Light damping for resonance

        # Second-order resonant filter
        # y[n] = (2 * (1-damping) * cos(omega) * y[n-1] - (1-damping)^2 * y[n-2] + x[n]) / (1 + damping)

        if not hasattr(self, "_resonance_state"):
            self._resonance_state = {"y1": 0.0, "y2": 0.0}

        filtered = np.zeros_like(signal)
        for i, x in enumerate(signal):
            y = (
                2 * (1 - damping) * math.cos(omega) * self._resonance_state["y1"]
                - (1 - damping) ** 2 * self._resonance_state["y2"]
                + x
            ) / (1 + damping)

            filtered[i] = y
            self._resonance_state["y2"] = self._resonance_state["y1"]
            self._resonance_state["y1"] = y

        return filtered

    def _calculate_turbulence(self, signal: np.ndarray) -> float:
        """Calculate turbulence level in signal"""
        # Turbulence measured by high-frequency energy
        if len(signal) < 10:
            return 0.0

        # Calculate second derivative (acceleration) as turbulence indicator
        acceleration = np.diff(np.diff(signal))
        turbulence_energy = np.mean(np.abs(acceleration))

        # Normalize to 0-1 range
        return min(turbulence_energy / 10.0, 1.0)

    def _apply_laminar_filter(
        self, signal: np.ndarray, turbulence: float
    ) -> np.ndarray:
        """Apply laminar flow filter to reduce turbulence"""
        # Simple low-pass filter to reduce high-frequency turbulence
        filter_strength = min(turbulence * 2.0, 0.9)  # Adaptive filter strength

        # Exponential moving average for laminar stabilization
        if not hasattr(self, "_laminar_state"):
            self._laminar_state = signal[0] if len(signal) > 0 else 0.0

        filtered = np.zeros_like(signal)
        for i, x in enumerate(signal):
            self._laminar_state = (
                self._laminar_state * (1 - filter_strength) + x * filter_strength
            )
            filtered[i] = self._laminar_state

        return filtered

    def _align_phases(self, signal: np.ndarray) -> np.ndarray:
        """Align phases for pattern enhancement"""
        # Hilbert transform for phase alignment (simplified)
        if len(signal) < 2:
            return signal

        # Simple phase alignment using correlation
        aligned = np.zeros_like(signal)

        # Use autocorrelation for pattern alignment
        for i in range(1, len(signal)):
            correlation = np.correlate(signal[:i], signal[i - 1 : i + 1], mode="valid")
            if len(correlation) > 0:
                phase_shift = correlation[0] / (
                    np.std(signal[:i]) * np.std(signal[i - 1 : i + 1]) + 1e-10
                )
                aligned[i] = signal[i] * (
                    1 + phase_shift * 0.1
                )  # Subtle phase alignment
            else:
                aligned[i] = signal[i]

        return aligned

    def _update_gate_state(self, processed_signal: np.ndarray, processing_time: float):
        """Update gate state based on processing results"""
        # Calculate fluid dynamics metrics
        signal_energy = np.mean(np.abs(processed_signal))
        signal_variance = np.var(processed_signal)

        # Update pressure (related to signal amplitude)
        self.state.pressure = min(
            self.config.max_pressure, max(self.config.min_pressure, signal_energy)
        )

        # Update velocity (related to processing speed and signal change rate)
        velocity_factor = 1.0 / (
            processing_time + 0.001
        )  # Faster processing = higher velocity
        self.state.velocity = min(self.config.max_velocity, velocity_factor)

        # Update flow rate (combination of pressure and velocity)
        self.state.flow_rate = self.state.pressure * self.state.velocity

        # Update turbulence (signal variability)
        self.state.turbulence_level = min(signal_variance / 10.0, 1.0)

        # Update efficiency (signal preservation vs processing time)
        original_energy = np.mean(np.abs(processed_signal))  # Approximation
        self.state.efficiency = min(original_energy / (signal_energy + 0.001), 1.0)

        # Update resonance phase
        self.state.resonance_phase = (self.state.resonance_phase + 0.1) % (2 * math.pi)

        self.state.last_update = time.time()

        # Store history
        self.history.append(
            {
                "timestamp": time.time(),
                "pressure": self.state.pressure,
                "velocity": self.state.velocity,
                "efficiency": self.state.efficiency,
                "turbulence": self.state.turbulence_level,
            }
        )

        # Keep history bounded
        if len(self.history) > 1000:
            self.history.pop(0)

    def get_gate_metrics(self) -> Dict[str, Any]:
        """Get comprehensive gate performance metrics"""
        if len(self.history) == 0:
            return self._get_current_metrics()

        # Calculate trends from history
        recent_history = (
            self.history[-100:] if len(self.history) > 100 else self.history
        )

        pressures = [h["pressure"] for h in recent_history]
        velocities = [h["velocity"] for h in recent_history]
        efficiencies = [h["efficiency"] for h in recent_history]
        turbulences = [h["turbulence"] for h in recent_history]

        return {
            "current_pressure": self.state.pressure,
            "current_velocity": self.state.velocity,
            "current_efficiency": self.state.efficiency,
            "current_turbulence": self.state.turbulence_level,
            "avg_pressure": np.mean(pressures),
            "avg_velocity": np.mean(velocities),
            "avg_efficiency": np.mean(efficiencies),
            "avg_turbulence": np.mean(turbulences),
            "pressure_stability": 1.0
            - np.std(pressures) / (np.mean(pressures) + 0.001),
            "velocity_stability": 1.0
            - np.std(velocities) / (np.mean(velocities) + 0.001),
            "efficiency_trend": (
                np.polyfit(range(len(efficiencies)), efficiencies, 1)[0]
                if len(efficiencies) > 1
                else 0
            ),
            "processing_history_length": len(self.history),
        }

    def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics when no history available"""
        return {
            "current_pressure": self.state.pressure,
            "current_velocity": self.state.velocity,
            "current_efficiency": self.state.efficiency,
            "current_turbulence": self.state.turbulence_level,
            "avg_pressure": self.state.pressure,
            "avg_velocity": self.state.velocity,
            "avg_efficiency": self.state.efficiency,
            "avg_turbulence": self.state.turbulence_level,
            "pressure_stability": 1.0,
            "velocity_stability": 1.0,
            "efficiency_trend": 0.0,
            "processing_history_length": 0,
        }


class AdaptiveController:
    """Adaptive controller for Venturi gate optimization"""

    def __init__(self, fluid_config: FluidDynamicsConfig):
        self.config = fluid_config
        self.learning_rate = fluid_config.adaptation_rate
        self.performance_history = []
        self.optimal_parameters = {
            "constriction_ratio": fluid_config.constriction_ratio,
            "acceleration_factor": fluid_config.acceleration_factor,
            "pressure_drop_coefficient": fluid_config.pressure_drop_coefficient,
        }

    async def adapt(self, gate_state: VenturiGateState, processed_signal: np.ndarray):
        """Adapt gate parameters based on performance"""
        # Calculate performance score
        performance = self._calculate_performance_score(gate_state, processed_signal)

        # Store performance history
        self.performance_history.append(
            {"performance": performance, "state": gate_state, "timestamp": time.time()}
        )

        # Keep history bounded
        if len(self.performance_history) > 100:
            self.performance_history.pop(0)

        # Adapt parameters if we have enough history
        if len(self.performance_history) >= 10:
            await self._update_parameters()

    def _calculate_performance_score(
        self, gate_state: VenturiGateState, processed_signal: np.ndarray
    ) -> float:
        """Calculate performance score for adaptation"""
        # Performance based on efficiency, stability, and signal quality
        efficiency_score = gate_state.efficiency
        stability_score = 1.0 - gate_state.turbulence_level
        signal_quality = 1.0 / (
            np.var(processed_signal) + 0.001
        )  # Lower variance = higher quality

        # Normalize signal quality to 0-1 range
        signal_quality = min(signal_quality / 1000.0, 1.0)

        # Weighted combination
        performance = (
            efficiency_score * 0.4 + stability_score * 0.3 + signal_quality * 0.3
        )

        return min(max(performance, 0.0), 1.0)

    async def _update_parameters(self):
        """Update optimal parameters based on performance history"""
        if len(self.performance_history) < 20:
            return

        # Find best performing configurations
        sorted_history = sorted(
            self.performance_history, key=lambda x: x["performance"], reverse=True
        )

        # Use top 10% for parameter estimation
        top_performers = sorted_history[: max(1, len(sorted_history) // 10)]

        # Calculate optimal parameters from top performers
        avg_constriction = np.mean([h["state"].pressure for h in top_performers])
        avg_acceleration = np.mean([h["state"].velocity for h in top_performers])

        # Smooth parameter updates
        self.optimal_parameters["constriction_ratio"] = (
            self.optimal_parameters["constriction_ratio"] * (1 - self.learning_rate)
            + (avg_constriction / 2.0) * self.learning_rate  # Scale to reasonable range
        )

        self.optimal_parameters["acceleration_factor"] = (
            self.optimal_parameters["acceleration_factor"] * (1 - self.learning_rate)
            + (avg_acceleration / 3.0) * self.learning_rate
        )


class EnhancedVenturiControlSystem:
    """
    Enhanced Venturi Control System - Orchestrates three Venturi gates

    Manages the complete fluid dynamics processing pipeline with:
    - Signal Enhancement Gate
    - Noise Reduction Gate
    - Pattern Extraction Gate
    """

    def __init__(self):
        self.gates = {}
        self.system_state = {
            "total_flow_rate": 0.0,
            "system_efficiency": 1.0,
            "harmonic_resonance": 0.0,
            "fluid_stability": 1.0,
        }
        self.processing_pipeline = []
        self.is_initialized = False

        logger.info("Enhanced Venturi Control System initialized")

    async def initialize_system(self) -> bool:
        """Initialize the three Venturi gates system"""
        try:
            # Create three Venturi gates
            gate_configs = [
                VenturiGateConfig(
                    gate_id="signal_enhancement_gate",
                    gate_type=VenturiGateType.SIGNAL_ENHANCEMENT,
                    fluid_config=FluidDynamicsConfig(
                        constriction_ratio=0.8,
                        acceleration_factor=1.3,
                        resonance_frequency=12.0,  # Alpha wave enhancement
                    ),
                ),
                VenturiGateConfig(
                    gate_id="noise_reduction_gate",
                    gate_type=VenturiGateType.NOISE_REDUCTION,
                    fluid_config=FluidDynamicsConfig(
                        constriction_ratio=0.9,
                        acceleration_factor=1.1,
                        turbulence_threshold=0.15,
                        flow_stability_factor=0.98,
                    ),
                ),
                VenturiGateConfig(
                    gate_id="pattern_extraction_gate",
                    gate_type=VenturiGateType.PATTERN_EXTRACTION,
                    fluid_config=FluidDynamicsConfig(
                        constriction_ratio=0.7,
                        acceleration_factor=1.4,
                        resonance_frequency=10.0,  # Fundamental EEG frequency
                    ),
                ),
            ]

            # Initialize gates
            for config in gate_configs:
                gate = EnhancedVenturiGate(config)
                self.gates[config.gate_id] = gate

            # Optimize processing pipeline
            await self._optimize_pipeline()

            self.is_initialized = True
            logger.info(
                f"Enhanced Venturi Control System initialized with {len(self.gates)} gates"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to initialize Venturi Control System: {e}")
            return False

    async def process_signal(
        self, input_signal: np.ndarray, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process signal through the complete Venturi system

        Args:
            input_signal: Input EEG signal
            context: Processing context

        Returns:
            Processing results dictionary
        """
        if not self.is_initialized:
            raise RuntimeError("Venturi Control System not initialized")

        start_time = time.perf_counter()

        results = {
            "input_signal": input_signal.copy(),
            "gate_outputs": {},
            "processing_metrics": {},
            "system_metrics": {},
        }

        current_signal = input_signal

        # Process through pipeline
        for gate_id in self.processing_pipeline:
            gate = self.gates[gate_id]

            # Process through gate
            gate_start = time.perf_counter()
            processed = await gate.process_signal(current_signal, context)
            gate_time = time.perf_counter() - gate_start

            # Store results
            results["gate_outputs"][gate_id] = processed.copy()
            results["processing_metrics"][gate_id] = {
                "processing_time": gate_time,
                "gate_metrics": gate.get_gate_metrics(),
            }

            current_signal = processed

        # Calculate system-level metrics
        total_time = time.perf_counter() - start_time
        results["system_metrics"] = self._calculate_system_metrics(results, total_time)

        # Update system state
        self._update_system_state(results)

        return results

    async def _optimize_pipeline(self):
        """Optimize the processing pipeline based on gate characteristics"""
        # Simple optimization: order by processing efficiency
        gate_efficiencies = []
        for gate_id, gate in self.gates.items():
            # Estimate efficiency (higher for signal enhancement, lower for noise reduction)
            if gate.config.gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
                efficiency = 0.9
            elif gate.config.gate_type == VenturiGateType.NOISE_REDUCTION:
                efficiency = 0.8
            else:  # PATTERN_EXTRACTION
                efficiency = 0.85

            gate_efficiencies.append((gate_id, efficiency))

        # Sort by efficiency (highest first)
        gate_efficiencies.sort(key=lambda x: x[1], reverse=True)
        self.processing_pipeline = [gate_id for gate_id, _ in gate_efficiencies]

        logger.info(f"Processing pipeline optimized: {self.processing_pipeline}")

    def _calculate_system_metrics(
        self, results: Dict[str, Any], total_time: float
    ) -> Dict[str, Any]:
        """Calculate system-level performance metrics"""
        gate_metrics = results["processing_metrics"]

        # Aggregate gate efficiencies
        efficiencies = []
        processing_times = []

        for gate_id, metrics in gate_metrics.items():
            gate_data = metrics["gate_metrics"]
            efficiencies.append(gate_data.get("current_efficiency", 1.0))
            processing_times.append(metrics["processing_time"])

        # Calculate system metrics
        system_efficiency = np.mean(efficiencies) if efficiencies else 1.0
        total_processing_time = sum(processing_times)

        # Calculate harmonic resonance (synchronization between gates)
        if len(efficiencies) > 1:
            efficiency_std = np.std(efficiencies)
            harmonic_resonance = 1.0 - min(
                efficiency_std, 1.0
            )  # Lower variance = higher resonance
        else:
            harmonic_resonance = 1.0

        # Calculate fluid stability (consistency across gates)
        fluid_stability = 1.0 - np.std(processing_times) / (
            np.mean(processing_times) + 0.001
        )

        return {
            "system_efficiency": system_efficiency,
            "total_processing_time": total_time,
            "harmonic_resonance": harmonic_resonance,
            "fluid_stability": fluid_stability,
            "throughput_hz": 1.0 / total_time if total_time > 0 else 0,
            "latency_ms": total_time * 1000,
            "gates_processed": len(gate_metrics),
        }

    def _update_system_state(self, results: Dict[str, Any]):
        """Update overall system state"""
        system_metrics = results["system_metrics"]

        self.system_state["total_flow_rate"] = system_metrics["throughput_hz"]
        self.system_state["system_efficiency"] = system_metrics["system_efficiency"]
        self.system_state["harmonic_resonance"] = system_metrics["harmonic_resonance"]
        self.system_state["fluid_stability"] = system_metrics["fluid_stability"]

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        gate_status = {}
        for gate_id, gate in self.gates.items():
            gate_status[gate_id] = {
                "type": gate.config.gate_type.value,
                "state": gate.get_gate_metrics(),
                "config": {
                    "constriction_ratio": gate.config.fluid_config.constriction_ratio,
                    "acceleration_factor": gate.config.fluid_config.acceleration_factor,
                    "resonance_frequency": gate.config.fluid_config.resonance_frequency,
                },
            }

        return {
            "system_state": self.system_state,
            "gate_status": gate_status,
            "processing_pipeline": self.processing_pipeline,
            "is_initialized": self.is_initialized,
            "total_gates": len(self.gates),
        }

    async def shutdown(self):
        """Gracefully shutdown the control system"""
        logger.info("Enhanced Venturi Control System shutdown complete")


# Factory function for easy instantiation
def create_enhanced_venturi_system() -> EnhancedVenturiControlSystem:
    """
    Factory function to create an enhanced Venturi control system

    Returns:
        Configured EnhancedVenturiControlSystem instance
    """
    return EnhancedVenturiControlSystem()


# Example usage and demonstration
async def demonstrate_venturi_system():
    """Demonstrate the enhanced Venturi control system"""
    print("🚀 Enhanced Venturi Control System Demonstration")
    print("=" * 60)

    # Create system
    system = create_enhanced_venturi_system()

    # Initialize
    print("📋 Initializing Venturi Control System...")
    success = await system.initialize_system()
    if not success:
        print("❌ Initialization failed")
        return

    print("✅ System initialized successfully")

    # Generate test EEG signal
    print("🧠 Generating test EEG signal...")
    n_samples = 1000
    t = np.linspace(0, 1, n_samples)

    # Create realistic EEG signal with multiple frequency components
    eeg_signal = (
        20e-6 * np.sin(2 * np.pi * 10 * t)  # Alpha waves
        + 15e-6 * np.sin(2 * np.pi * 20 * t)  # Beta waves
        + 5e-6 * np.random.randn(n_samples)  # Background noise
        + 30e-6 * np.sin(2 * np.pi * 0.5 * t)  # Slow oscillations
    )

    # Process signal
    print("⚡ Processing signal through Venturi system...")
    start_time = time.perf_counter()

    results = await system.process_signal(eeg_signal)

    processing_time = time.perf_counter() - start_time

    print("\n📊 PROCESSING RESULTS")
    print(f"Input signal length: {len(eeg_signal)} samples")
    print(f"Total processing time: {processing_time:.4f} seconds")
    print(f"Latency: {processing_time * 1000:.1f} ms")
    print(f"Throughput: {1.0 / processing_time:.1f} Hz")

    # Display system metrics
    system_metrics = results["system_metrics"]
    print("\n🔬 SYSTEM METRICS")
    print(f"System Efficiency: {system_metrics['system_efficiency']:.3f}")
    print(f"Harmonic Resonance: {system_metrics['harmonic_resonance']:.3f}")
    print(f"Fluid Stability: {system_metrics['fluid_stability']:.3f}")
    print(f"Gates Processed: {system_metrics['gates_processed']}")

    # Display gate-by-gate results
    print("\n🏗️ GATE PROCESSING RESULTS")
    for gate_id, gate_output in results["gate_outputs"].items():
        metrics = results["processing_metrics"][gate_id]
        gate_data = metrics["gate_metrics"]

        print(f"\n{gate_id.upper()}:")
        print(f"  Processing time: {metrics['processing_time']:.6f} seconds")
        print(f"  Current efficiency: {gate_data['current_efficiency']:.3f}")
        print(f"  Current pressure: {gate_data['current_pressure']:.3f}")
        print(f"  Current velocity: {gate_data['current_velocity']:.3f}")
        print(f"  Turbulence level: {gate_data['current_turbulence']:.3f}")

    # Display final system status
    print("\n📈 FINAL SYSTEM STATUS")
    status = system.get_system_status()
    print(f"Total flow rate: {status['system_state']['total_flow_rate']:.1f} Hz")
    print(f"System efficiency: {status['system_state']['system_efficiency']:.3f}")
    print(f"Harmonic resonance: {status['system_state']['harmonic_resonance']:.3f}")
    print(f"Fluid stability: {status['system_state']['fluid_stability']:.3f}")
    print(f"Processing pipeline: {status['processing_pipeline']}")

    print("\n🎉 Demonstration completed successfully!")
    await system.shutdown()


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_venturi_system())
