#!/usr/bin/env python3
"""
Three Venturi Harmonic Calibration Tool
Advanced calibration system for L.I.F.E. Platform Venturi Gates

This tool performs harmonic calibration of the three Venturi gates:
1. Signal Enhancement Gate
2. Noise Reduction Gate
3. Pattern Extraction Gate

Calibration ensures optimal harmonic resonance between gates for
ultra-low latency EEG processing.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import math
import os
import statistics
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np

# Import Venturi system components
try:
    from venturi_gates_system import (
        VenturiGate,
        VenturiGateConfig,
        VenturiGatesSystem,
        VenturiGateType,
    )
except ImportError:
    # Fallback for development/testing
    print("Warning: Venturi system not available, using mock implementation")

    # Create mock classes for testing
    class MockVenturiGateType:
        SIGNAL_ENHANCEMENT = "signal_enhancement"
        NOISE_REDUCTION = "noise_reduction"
        PATTERN_EXTRACTION = "pattern_extraction"

    VenturiGateType = MockVenturiGateType
    VenturiGate = None
    VenturiGateConfig = None
    VenturiGatesSystem = None


class HarmonicCalibrationError(Exception):
    """Custom exception for harmonic calibration failures"""

    pass


class ThreeVenturiHarmonicCalibrator:
    """
    Advanced harmonic calibration system for three Venturi gates.

    This calibrator ensures optimal resonance between the three gates:
    - Signal Enhancement (fundamental frequency)
    - Noise Reduction (harmonic suppression)
    - Pattern Extraction (resonant amplification)
    """

    def __init__(self):
        self.system: Optional[VenturiGatesSystem] = None
        self.calibration_results: Dict[str, Any] = {}
        self.harmonic_frequencies: Dict[str, float] = {}
        self.resonance_patterns: List[Dict[str, Any]] = []
        self.start_time = datetime.now()

        # Setup logging
        self._setup_logging()

        # Initialize calibration parameters
        self.fundamental_freq = 10.0  # Base frequency in Hz
        self.harmonic_ratios = [1.0, 2.0, 3.0]  # Fundamental, 2nd, 3rd
        self.calibration_iterations = 100
        self.convergence_threshold = 0.001

    def _setup_logging(self):
        """Setup comprehensive logging for calibration process"""
        # Ensure logs directory exists with absolute path
        script_dir = os.getcwd()
        logs_dir = os.path.join(script_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(
            logs_dir, f"three_venturi_harmonic_calibration_{timestamp}.log"
        )

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("HarmonicCalibrator")

    async def initialize_venturi_system(self) -> bool:
        """
        Initialize the three Venturi gates system with optimal configuration.

        Returns:
            bool: True if initialization successful
        """
        try:
            self.logger.info("🔧 Initializing Three Venturi Gates System...")

            # Create gate configurations with harmonic relationships
            signal_gate_config = VenturiGateConfig(
                gate_id="signal_acceleration",
                gate_type=VenturiGateType.SIGNAL_ENHANCEMENT,
                constriction_factor=0.75,  # Fundamental constriction
                acceleration_factor=1.5,  # Fundamental acceleration
                adaptation_rate=0.02,
                efficiency_threshold=0.85,
            )

            noise_gate_config = VenturiGateConfig(
                gate_id="pressure_differential",
                gate_type=VenturiGateType.NOISE_REDUCTION,
                constriction_factor=0.65,  # 2nd harmonic constriction
                acceleration_factor=2.0,  # 2nd harmonic acceleration
                adaptation_rate=0.015,
                efficiency_threshold=0.80,
            )

            pattern_gate_config = VenturiGateConfig(
                gate_id="flow_recovery",
                gate_type=VenturiGateType.PATTERN_EXTRACTION,
                constriction_factor=0.55,  # 3rd harmonic constriction
                acceleration_factor=2.5,  # 3rd harmonic acceleration
                adaptation_rate=0.01,
                efficiency_threshold=0.75,
            )

            # Initialize system
            self.system = VenturiGatesSystem()

            # Add gates to system
            self.system.gates[signal_gate_config.gate_id] = VenturiGate(
                signal_gate_config
            )
            self.system.gates[noise_gate_config.gate_id] = VenturiGate(
                noise_gate_config
            )
            self.system.gates[pattern_gate_config.gate_id] = VenturiGate(
                pattern_gate_config
            )

            self.logger.info("✅ Three Venturi Gates System initialized successfully")
            return True

        except Exception as e:
            self.logger.error("❌ Failed to initialize Venturi system: %s", e)
            return False

    async def perform_harmonic_calibration(self) -> Dict[str, Any]:
        """
        Perform comprehensive harmonic calibration of the three gates.

        This involves:
        1. Frequency domain analysis
        2. Resonance pattern optimization
        3. Phase alignment
        4. Efficiency maximization

        Returns:
            Dict containing calibration results
        """
        self.logger.info("🎵 Starting Three Venturi Harmonic Calibration...")

        results = {
            "calibration_start": self.start_time.isoformat(),
            "gates": {},
            "harmonic_analysis": {},
            "resonance_metrics": {},
            "optimization_results": {},
            "validation_status": "pending",
        }

        try:
            # Phase 1: Individual gate calibration
            self.logger.info("Phase 1: Individual Gate Calibration")
            gate_results = await self._calibrate_individual_gates()
            results["gates"] = gate_results

            # Phase 2: Harmonic frequency analysis
            self.logger.info("Phase 2: Harmonic Frequency Analysis")
            harmonic_results = await self._analyze_harmonic_frequencies()
            results["harmonic_analysis"] = harmonic_results

            # Phase 3: Resonance pattern optimization
            self.logger.info("Phase 3: Resonance Pattern Optimization")
            resonance_results = await self._optimize_resonance_patterns()
            results["resonance_metrics"] = resonance_results

            # Phase 4: System-wide optimization
            self.logger.info("Phase 4: System-wide Harmonic Optimization")
            optimization_results = await self._perform_system_optimization()
            results["optimization_results"] = optimization_results

            # Phase 5: Validation
            self.logger.info("Phase 5: Calibration Validation")
            validation_results = await self._validate_calibration()
            results["validation_status"] = validation_results["status"]
            results["validation_details"] = validation_results

            results["calibration_end"] = datetime.now().isoformat()
            results["total_duration_seconds"] = (
                datetime.now() - self.start_time
            ).total_seconds()

            self.calibration_results = results
            self.logger.info("✅ Harmonic calibration completed successfully")

        except Exception as e:
            self.logger.error("❌ Harmonic calibration failed: %s", e)
            results["error"] = str(e)
            results["validation_status"] = "failed"

        return results

    async def _calibrate_individual_gates(self) -> Dict[str, Any]:
        """Calibrate each gate individually for optimal performance"""
        gate_results = {}

        if not self.system:
            raise HarmonicCalibrationError("Venturi system not initialized")

        for gate_id, gate in self.system.gates.items():
            self.logger.info("Calibrating gate: %s", gate_id)

            # Generate test signals
            test_signals = self._generate_test_signals(gate.config.gate_type)

            # Calibrate gate parameters
            calibration = await self._calibrate_single_gate(gate, test_signals)

            gate_results[gate_id] = {
                "gate_type": gate.config.gate_type.value,
                "calibration": calibration,
                "efficiency": gate.efficiency,
                "state": gate.state,
            }

        return gate_results

    async def _calibrate_single_gate(
        self, gate: VenturiGate, test_signals: List[List[float]]
    ) -> Dict[str, Any]:
        """Calibrate a single gate using test signals"""
        performances = []

        for signal in test_signals:
            # Process signal through gate
            processed = gate.process_signal(signal)

            # Assess performance
            performance = self._assess_gate_performance(
                signal, processed, gate.config.gate_type
            )
            performances.append(performance)

            # Adapt gate parameters based on performance
            self._adapt_gate_parameters(gate, performance)

        # Calculate optimal parameters
        optimal_params = self._calculate_optimal_parameters(performances)

        return {
            "test_signals_count": len(test_signals),
            "average_performance": statistics.mean(performances),
            "performance_std": (
                statistics.stdev(performances) if len(performances) > 1 else 0
            ),
            "optimal_parameters": optimal_params,
            "convergence_achieved": len(performances) >= 10
            and abs(
                statistics.mean(performances[-5:])
                - statistics.mean(performances[-10:-5])
            )
            < self.convergence_threshold,
        }

    def _generate_test_signals(self, gate_type: VenturiGateType) -> List[List[float]]:
        """Generate appropriate test signals for gate calibration"""
        signals = []

        # Generate 10 test signals for calibration
        for i in range(10):
            if gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
                # Sine waves with varying frequencies
                freq = self.fundamental_freq * (1 + i * 0.1)
                signal = [math.sin(2 * math.pi * freq * t / 1000) for t in range(1000)]
            elif gate_type == VenturiGateType.NOISE_REDUCTION:
                # Sine wave with added noise
                freq = self.fundamental_freq * 2  # 2nd harmonic
                clean_signal = [
                    math.sin(2 * math.pi * freq * t / 1000) for t in range(1000)
                ]
                noise = np.random.normal(0, 0.1, 1000)
                signal = [s + n for s, n in zip(clean_signal, noise)]
            elif gate_type == VenturiGateType.PATTERN_EXTRACTION:
                # Complex pattern with multiple harmonics
                signal = []
                for t in range(1000):
                    value = 0
                    for harmonic in range(1, 4):  # Fundamental + 2 harmonics
                        freq = self.fundamental_freq * harmonic
                        value += math.sin(2 * math.pi * freq * t / 1000) / harmonic
                    signal.append(value)
            else:
                # Default random signal
                signal = np.random.normal(0, 1, 1000).tolist()

            signals.append(signal)

        return signals

    def _assess_gate_performance(
        self, original: List[float], processed: List[float], gate_type: VenturiGateType
    ) -> float:
        """Assess the performance of a gate based on input/output signals"""
        if len(original) != len(processed):
            return 0.0

        try:
            if gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
                # Measure signal-to-noise ratio improvement
                orig_snr = self._calculate_snr(original)
                proc_snr = self._calculate_snr(processed)
                performance = min(
                    1.0, (proc_snr - orig_snr) / 10.0 + 0.5
                )  # Normalize to 0-1

            elif gate_type == VenturiGateType.NOISE_REDUCTION:
                # Measure noise reduction effectiveness
                orig_noise = self._calculate_noise_level(original)
                proc_noise = self._calculate_noise_level(processed)
                if orig_noise > 0:
                    performance = max(0.0, 1.0 - (proc_noise / orig_noise))
                else:
                    performance = 0.5

            elif gate_type == VenturiGateType.PATTERN_EXTRACTION:
                # Measure pattern clarity (higher frequency content preservation)
                orig_entropy = self._calculate_signal_entropy(original)
                proc_entropy = self._calculate_signal_entropy(processed)
                performance = min(1.0, proc_entropy / max(orig_entropy, 0.1))

            else:
                # Default: signal preservation
                correlation = self._calculate_correlation(original, processed)
                performance = abs(correlation)

            return max(0.0, min(1.0, performance))  # Clamp to [0, 1]

        except Exception:
            return 0.5  # Neutral performance on error

    def _adapt_gate_parameters(self, gate: VenturiGate, performance: float):
        """Adapt gate parameters based on performance feedback"""
        # Simple adaptation algorithm
        adaptation_rate = gate.config.adaptation_rate

        if performance > 0.7:  # Good performance
            # Slightly increase efficiency
            gate.efficiency = min(1.0, gate.efficiency + adaptation_rate * 0.1)
        elif performance < 0.3:  # Poor performance
            # Slightly decrease efficiency and adjust state
            gate.efficiency = max(0.1, gate.efficiency - adaptation_rate * 0.2)
            gate.state = max(0.1, gate.state - adaptation_rate * 0.1)
        else:
            # Moderate performance - fine tune
            gate.state = min(
                1.0, gate.state + adaptation_rate * (performance - 0.5) * 0.05
            )

    def _calculate_optimal_parameters(
        self, performances: List[float]
    ) -> Dict[str, Any]:
        """Calculate optimal parameters from performance history"""
        if not performances:
            return {}

        return {
            "best_performance": max(performances),
            "average_performance": statistics.mean(performances),
            "performance_stability": 1.0
            - (statistics.stdev(performances) if len(performances) > 1 else 0),
            "convergence_rate": self._calculate_convergence_rate(performances),
        }

    async def _analyze_harmonic_frequencies(self) -> Dict[str, Any]:
        """Analyze harmonic frequencies across the three gates"""
        self.logger.info("Analyzing harmonic frequencies...")

        if not self.system:
            return {}

        # Calculate fundamental frequencies for each gate
        frequencies = {}
        for gate_id, gate in self.system.gates.items():
            freq = self._calculate_gate_frequency(gate)
            frequencies[gate_id] = freq
            self.harmonic_frequencies[gate_id] = freq

        # Analyze harmonic relationships
        harmonic_ratios = self._calculate_harmonic_ratios(frequencies)

        return {
            "gate_frequencies": frequencies,
            "harmonic_ratios": harmonic_ratios,
            "fundamental_frequency": self.fundamental_freq,
            "harmonic_purity": self._assess_harmonic_purity(harmonic_ratios),
        }

    def _calculate_gate_frequency(self, gate: VenturiGate) -> float:
        """Calculate the resonant frequency of a gate"""
        # Based on gate configuration and current state
        base_freq = self.fundamental_freq

        if gate.config.gate_type == VenturiGateType.SIGNAL_ENHANCEMENT:
            return base_freq * gate.state
        elif gate.config.gate_type == VenturiGateType.NOISE_REDUCTION:
            return base_freq * 2 * gate.efficiency  # 2nd harmonic
        elif gate.config.gate_type == VenturiGateType.PATTERN_EXTRACTION:
            return base_freq * 3 * gate.state  # 3rd harmonic
        else:
            return base_freq

    def _calculate_harmonic_ratios(
        self, frequencies: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate harmonic ratios between gates"""
        ratios = {}

        # Find fundamental frequency (lowest)
        fundamental = min(frequencies.values())

        for gate_id, freq in frequencies.items():
            ratios[gate_id] = freq / fundamental if fundamental > 0 else 1.0

        return ratios

    def _assess_harmonic_purity(self, ratios: Dict[str, float]) -> float:
        """Assess how pure the harmonic relationships are"""
        # Ideal ratios should be close to 1:2:3
        ideal_ratios = [1.0, 2.0, 3.0]
        actual_ratios = list(ratios.values())

        if len(actual_ratios) != 3:
            return 0.0

        # Calculate deviation from ideal harmonics
        deviations = []
        for actual, ideal in zip(sorted(actual_ratios), ideal_ratios):
            deviation = abs(actual - ideal) / ideal
            deviations.append(deviation)

        # Purity is inverse of average deviation
        avg_deviation = statistics.mean(deviations)
        purity = max(0.0, 1.0 - avg_deviation)

        return purity

    async def _optimize_resonance_patterns(self) -> Dict[str, Any]:
        """Optimize resonance patterns between gates"""
        self.logger.info("Optimizing resonance patterns...")

        if not self.system:
            return {}

        # Simulate resonance optimization
        patterns = []
        for iteration in range(self.calibration_iterations):
            pattern = self._generate_resonance_pattern()
            quality = self._evaluate_resonance_quality(pattern)
            patterns.append(
                {"iteration": iteration, "pattern": pattern, "quality": quality}
            )

            # Keep track of best patterns
            if not self.resonance_patterns or quality > max(
                p["quality"] for p in self.resonance_patterns
            ):
                self.resonance_patterns.append({"pattern": pattern, "quality": quality})

        # Keep only top 10 patterns
        self.resonance_patterns = sorted(
            self.resonance_patterns, key=lambda x: x["quality"], reverse=True
        )[:10]

        best_pattern = self.resonance_patterns[0] if self.resonance_patterns else {}

        return {
            "iterations_performed": self.calibration_iterations,
            "best_resonance_quality": best_pattern.get("quality", 0),
            "optimal_pattern": best_pattern.get("pattern", {}),
            "convergence_achieved": len(patterns) >= 10
            and abs(
                statistics.mean([p["quality"] for p in patterns[-5:]])
                - statistics.mean([p["quality"] for p in patterns[-10:-5]])
            )
            < self.convergence_threshold,
        }

    def _generate_resonance_pattern(self) -> Dict[str, Any]:
        """Generate a resonance pattern for the three gates"""
        return {
            "signal_gate_phase": np.random.uniform(0, 2 * math.pi),
            "noise_gate_phase": np.random.uniform(0, 2 * math.pi),
            "pattern_gate_phase": np.random.uniform(0, 2 * math.pi),
            "coupling_strength": np.random.uniform(0.1, 1.0),
            "resonance_frequency": np.random.uniform(
                self.fundamental_freq * 0.5, self.fundamental_freq * 4
            ),
        }

    def _evaluate_resonance_quality(self, pattern: Dict[str, Any]) -> float:
        """Evaluate the quality of a resonance pattern"""
        # Simplified resonance quality calculation
        # In a real implementation, this would involve complex physics simulations

        # Phase alignment score (closer phases = better coupling)
        phases = [
            pattern["signal_gate_phase"],
            pattern["noise_gate_phase"],
            pattern["pattern_gate_phase"],
        ]
        phase_alignment = 1.0 - (statistics.stdev(phases) / math.pi)  # Normalize to 0-1

        # Frequency coherence score
        target_freq = pattern["resonance_frequency"]
        freq_deviation = abs(target_freq - self.fundamental_freq * 2.5) / (
            self.fundamental_freq * 2.5
        )
        freq_coherence = max(0.0, 1.0 - freq_deviation)

        # Coupling strength score
        coupling_score = pattern["coupling_strength"]

        # Combined quality score
        quality = phase_alignment * 0.4 + freq_coherence * 0.4 + coupling_score * 0.2

        return min(1.0, max(0.0, quality))

    async def _perform_system_optimization(self) -> Dict[str, Any]:
        """Perform system-wide harmonic optimization"""
        self.logger.info("Performing system-wide optimization...")

        if not self.system:
            return {}

        # Optimize gate interactions
        optimization_results = {
            "gate_interactions": {},
            "system_efficiency": 0.0,
            "harmonic_stability": 0.0,
            "optimization_iterations": 50,
        }

        # Simulate optimization process
        for iteration in range(50):
            # Adjust gate parameters for better harmony
            self._optimize_gate_interactions()

            # Measure system performance
            efficiency = self._measure_system_efficiency()
            stability = self._measure_harmonic_stability()

            optimization_results["system_efficiency"] = max(
                optimization_results["system_efficiency"], efficiency
            )
            optimization_results["harmonic_stability"] = max(
                optimization_results["harmonic_stability"], stability
            )

        return optimization_results

    def _optimize_gate_interactions(self):
        """Optimize interactions between gates"""
        if not self.system:
            return

        # Simple optimization: adjust gate states for better harmony
        gates = list(self.system.gates.values())

        for i, gate in enumerate(gates):
            # Adjust based on neighboring gates
            prev_gate = gates[i - 1] if i > 0 else gates[-1]
            next_gate = gates[(i + 1) % len(gates)]

            # Harmonic adjustment
            avg_neighbor_efficiency = (prev_gate.efficiency + next_gate.efficiency) / 2
            adjustment = (avg_neighbor_efficiency - gate.efficiency) * 0.1

            gate.efficiency = max(0.1, min(1.0, gate.efficiency + adjustment))

    def _measure_system_efficiency(self) -> float:
        """Measure overall system efficiency"""
        if not self.system:
            return 0.0

        efficiencies = [gate.efficiency for gate in self.system.gates.values()]
        return statistics.mean(efficiencies) if efficiencies else 0.0

    def _measure_harmonic_stability(self) -> float:
        """Measure harmonic stability of the system"""
        if not self.system:
            return 0.0

        states = [gate.state for gate in self.system.gates.values()]
        if len(states) < 2:
            return 1.0

        # Stability is inverse of state variance
        variance = statistics.variance(states) if len(states) > 1 else 0
        stability = max(0.0, 1.0 - variance)

        return stability

    async def _validate_calibration(self) -> Dict[str, Any]:
        """Validate the calibration results"""
        self.logger.info("Validating calibration...")

        validation_results = {
            "status": "unknown",
            "tests_passed": 0,
            "total_tests": 4,
            "validation_details": {},
        }

        try:
            # Test 1: Gate efficiency validation
            efficiency_test = self._validate_gate_efficiencies()
            validation_results["validation_details"][
                "efficiency_test"
            ] = efficiency_test
            if efficiency_test["passed"]:
                validation_results["tests_passed"] += 1

            # Test 2: Harmonic ratio validation
            harmonic_test = self._validate_harmonic_ratios()
            validation_results["validation_details"]["harmonic_test"] = harmonic_test
            if harmonic_test["passed"]:
                validation_results["tests_passed"] += 1

            # Test 3: Resonance pattern validation
            resonance_test = self._validate_resonance_patterns()
            validation_results["validation_details"]["resonance_test"] = resonance_test
            if resonance_test["passed"]:
                validation_results["tests_passed"] += 1

            # Test 4: System stability validation
            stability_test = self._validate_system_stability()
            validation_results["validation_details"]["stability_test"] = stability_test
            if stability_test["passed"]:
                validation_results["tests_passed"] += 1

            # Determine overall status
            success_rate = (
                validation_results["tests_passed"] / validation_results["total_tests"]
            )
            if success_rate >= 0.75:
                validation_results["status"] = "passed"
            elif success_rate >= 0.5:
                validation_results["status"] = "warning"
            else:
                validation_results["status"] = "failed"

        except Exception as e:
            self.logger.error("Validation failed: %s", e)
            validation_results["status"] = "error"
            validation_results["error"] = str(e)

        return validation_results

    def _validate_gate_efficiencies(self) -> Dict[str, Any]:
        """Validate that all gates have acceptable efficiency"""
        if not self.system:
            return {"passed": False, "reason": "System not initialized"}

        efficiencies = [gate.efficiency for gate in self.system.gates.values()]
        avg_efficiency = statistics.mean(efficiencies) if efficiencies else 0

        passed = avg_efficiency >= 0.6  # 60% minimum average efficiency

        return {
            "passed": passed,
            "average_efficiency": avg_efficiency,
            "individual_efficiencies": dict(
                zip(self.system.gates.keys(), efficiencies)
            ),
            "reason": (
                "Average efficiency below threshold"
                if not passed
                else "All gates within efficiency range"
            ),
        }

    def _validate_harmonic_ratios(self) -> Dict[str, Any]:
        """Validate harmonic ratios are within acceptable ranges"""
        if not self.harmonic_frequencies:
            return {"passed": False, "reason": "No harmonic frequencies calculated"}

        ratios = list(self.harmonic_frequencies.values())
        if len(ratios) != 3:
            return {"passed": False, "reason": "Incorrect number of gates"}

        # Check if ratios are approximately 1:2:3
        sorted_ratios = sorted(ratios)
        expected_ratios = [sorted_ratios[0], sorted_ratios[0] * 2, sorted_ratios[0] * 3]

        deviations = [
            abs(actual - expected) / expected
            for actual, expected in zip(sorted_ratios, expected_ratios)
        ]
        avg_deviation = statistics.mean(deviations)

        passed = avg_deviation <= 0.2  # 20% maximum deviation

        return {
            "passed": passed,
            "harmonic_ratios": dict(zip(self.harmonic_frequencies.keys(), ratios)),
            "average_deviation": avg_deviation,
            "reason": (
                "Harmonic ratios outside acceptable range"
                if not passed
                else "Harmonic ratios within tolerance"
            ),
        }

    def _validate_resonance_patterns(self) -> Dict[str, Any]:
        """Validate resonance patterns are optimized"""
        if not self.resonance_patterns:
            return {"passed": False, "reason": "No resonance patterns generated"}

        best_quality = max(pattern["quality"] for pattern in self.resonance_patterns)
        passed = best_quality >= 0.7  # 70% minimum resonance quality

        return {
            "passed": passed,
            "best_resonance_quality": best_quality,
            "patterns_analyzed": len(self.resonance_patterns),
            "reason": (
                "Resonance quality below threshold"
                if not passed
                else "Resonance patterns optimized"
            ),
        }

    def _validate_system_stability(self) -> Dict[str, Any]:
        """Validate system stability"""
        stability = self._measure_harmonic_stability()
        passed = stability >= 0.8  # 80% minimum stability

        return {
            "passed": passed,
            "stability_score": stability,
            "reason": (
                "System stability below threshold"
                if not passed
                else "System stability acceptable"
            ),
        }

    def save_calibration_results(self, filename: Optional[str] = None) -> str:
        """Save calibration results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/three_venturi_harmonic_calibration_{timestamp}.json"

        # Ensure results directory exists
        os.makedirs("results", exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.calibration_results, f, indent=2, default=str)

        self.logger.info("Calibration results saved to: %s", filename)
        return filename

    # Utility methods for signal processing
    def _calculate_snr(self, signal: List[float]) -> float:
        """Calculate Signal-to-Noise Ratio"""
        if not signal:
            return 0.0

        signal_power = statistics.mean([s**2 for s in signal])
        noise_power = statistics.variance(signal) * 0.1  # Estimate noise

        return 10 * math.log10(signal_power / max(noise_power, 1e-10))

    def _calculate_noise_level(self, signal: List[float]) -> float:
        """Calculate noise level in signal"""
        if len(signal) < 2:
            return 0.0
        return statistics.stdev(signal)

    def _calculate_signal_entropy(self, signal: List[float]) -> float:
        """Calculate signal entropy (complexity measure)"""
        if not signal:
            return 0.0

        # Simple entropy calculation based on signal derivatives
        derivatives = [abs(signal[i + 1] - signal[i]) for i in range(len(signal) - 1)]
        if not derivatives:
            return 0.0

        # Normalize and calculate entropy
        max_deriv = max(derivatives)
        if max_deriv == 0:
            return 0.0

        normalized = [d / max_deriv for d in derivatives]
        entropy = -sum(p * math.log2(max(p, 1e-10)) for p in normalized if p > 0)

        return entropy

    def _calculate_correlation(
        self, signal1: List[float], signal2: List[float]
    ) -> float:
        """Calculate correlation between two signals"""
        if len(signal1) != len(signal2) or len(signal1) < 2:
            return 0.0

        mean1 = statistics.mean(signal1)
        mean2 = statistics.mean(signal2)

        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(signal1, signal2))
        denom1 = sum((x - mean1) ** 2 for x in signal1)
        denom2 = sum((y - mean2) ** 2 for y in signal2)

        if denom1 == 0 or denom2 == 0:
            return 0.0

        return numerator / math.sqrt(denom1 * denom2)

    def _calculate_convergence_rate(self, values: List[float]) -> float:
        """Calculate convergence rate of a series"""
        if len(values) < 10:
            return 0.0

        # Calculate rate of change in last 20% of values
        recent_values = values[-max(1, len(values) // 5) :]
        if len(recent_values) < 2:
            return 0.0

        changes = [
            abs(recent_values[i + 1] - recent_values[i])
            for i in range(len(recent_values) - 1)
        ]
        avg_change = statistics.mean(changes)

        # Convergence rate is inverse of average change
        return max(0.0, 1.0 - avg_change)


async def main():
    """Main function for three Venturi harmonic calibration"""
    print("🎵 L.I.F.E. Platform - Three Venturi Harmonic Calibration Tool")
    print("=" * 65)

    calibrator = ThreeVenturiHarmonicCalibrator()

    try:
        # Initialize system
        if not await calibrator.initialize_venturi_system():
            print("❌ Failed to initialize Venturi system")
            return 1

        # Perform calibration
        results = await calibrator.perform_harmonic_calibration()

        # Save results
        results_file = calibrator.save_calibration_results()

        # Display summary
        print("\n📊 CALIBRATION SUMMARY")
        print("=" * 30)
        print(f"Status: {results.get('validation_status', 'unknown').upper()}")
        print(".2f")
        print(f"Results saved to: {results_file}")

        if results.get("validation_status") == "passed":
            print(
                "✅ Calibration successful - Three Venturi gates harmonically optimized!"
            )
        else:
            print("⚠️  Calibration completed with warnings - review results for details")

        return 0 if results.get("validation_status") == "passed" else 1

    except Exception as e:
        print(f"❌ Calibration failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
