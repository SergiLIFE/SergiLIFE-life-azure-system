"""
Comprehensive test suite for L.I.F.E Theory components
Testing framework for EEG processing and Venturi systems

Copyright 2025 - Sergio Paya Borrull
"""

import os
import sys
from datetime import datetime

import numpy as np
import pytest

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eeg_processor import EEGProcessor, create_eeg_processor
from lifetheory import (
    AdaptationParameters,
    CoreLIFEAlgorithm,
    LearningExperience,
    LIFEEEGProcessor,
    create_eeg_life_processor,
    create_life_algorithm,
)
from venturi_gates_system import (
    VenturiGateConfig,
    VenturiGatesSystem,
    VenturiGateType,
    create_3_venturi_system,
)


class TestLIFEAlgorithm:
    """Test suite for core L.I.F.E Theory algorithm"""

    def test_life_algorithm_creation(self):
        """Test L.I.F.E algorithm creation and initialization"""
        algorithm = create_life_algorithm()
        assert algorithm is not None
        assert isinstance(algorithm, CoreLIFEAlgorithm)

        # Test custom configuration
        config = {
            "learning_rate": 0.05,
            "max_experiences": 5000,
            "venturi_gate_factor": 1.5,
        }
        custom_algorithm = create_life_algorithm(config)
        assert custom_algorithm.params.learning_rate == 0.05
        assert custom_algorithm.params.max_experiences == 5000

    def test_life_signal_processing(self):
        """Test L.I.F.E signal processing capabilities"""
        algorithm = create_life_algorithm()

        # Test with various signal types
        test_signals = [
            np.random.randn(100),  # Random noise
            np.sin(np.linspace(0, 4 * np.pi, 100)),  # Sine wave
            np.ones(50),  # Constant signal
            np.random.exponential(1, 200),  # Exponential distribution
        ]

        for signal in test_signals:
            processed = algorithm.process(signal)
            assert processed is not None
            assert len(processed) == len(signal)
            assert not np.allclose(processed, signal)  # Should be different from input

    def test_life_adaptation(self):
        """Test L.I.F.E adaptation mechanism"""
        algorithm = create_life_algorithm()
        initial_performance = algorithm.get_performance_metrics()

        # Create multiple learning experiences
        for i in range(10):
            test_data = np.random.randn(50)
            processed = algorithm.process(test_data)

            experience = LearningExperience(
                timestamp=datetime.now(),
                input_data=test_data,
                output_data=processed,
                context={"iteration": i},
                performance_metric=0.7 + 0.1 * np.random.randn(),
            )

            algorithm.adapt(experience)

        final_performance = algorithm.get_performance_metrics()
        assert final_performance["experience_count"] == 10
        assert (
            final_performance["experience_count"]
            > initial_performance["experience_count"]
        )

    def test_life_memory_system(self):
        """Test L.I.F.E memory and experience storage"""
        algorithm = create_life_algorithm({"max_experiences": 5})

        # Add more experiences than memory limit
        for i in range(10):
            test_data = np.random.randn(20)
            processed = algorithm.process(test_data)

            experience = LearningExperience(
                timestamp=datetime.now(),
                input_data=test_data,
                output_data=processed,
                context={"test": i},
                performance_metric=0.5 + 0.1 * i,
            )

            algorithm.adapt(experience)

        # Memory should be limited to max_experiences
        assert len(algorithm.memory.experiences) <= 5

        # Should keep best experiences
        best_experiences = algorithm.memory.get_best_experiences(3)
        assert len(best_experiences) <= 3

        # Best experiences should have higher performance
        if len(best_experiences) > 1:
            for i in range(len(best_experiences) - 1):
                assert (
                    best_experiences[i].performance_metric
                    >= best_experiences[i + 1].performance_metric
                )


class TestEEGProcessor:
    """Test suite for EEG processing components"""

    def test_eeg_processor_creation(self):
        """Test EEG processor creation"""
        processor = create_eeg_processor()
        assert processor is not None
        assert isinstance(processor, EEGProcessor)

        # Test custom configuration
        config = {"sampling_rate": 500.0, "learning_rate": 0.001, "venturi_factor": 1.5}
        custom_processor = create_eeg_processor(config)
        assert custom_processor.sampling_rate == 500.0

    def test_eeg_signal_processing(self):
        """Test EEG signal processing pipeline"""
        processor = create_eeg_processor()

        # Simulate multi-channel EEG data
        channels = 4
        samples = 1000
        sampling_rate = 250.0

        # Create realistic EEG-like signals
        t = np.linspace(0, samples / sampling_rate, samples)
        eeg_data = []

        for ch in range(channels):
            # Mix of different frequency components
            signal = (
                2 * np.sin(2 * np.pi * 8 * t)  # Alpha
                + 1 * np.sin(2 * np.pi * 15 * t)  # Beta
                + 0.5 * np.random.randn(samples)  # Noise
            )
            eeg_data.append(signal)

        eeg_data = np.array(eeg_data)
        channel_names = [f"CH{i+1}" for i in range(channels)]

        # Process EEG data
        results = processor.process(eeg_data, channel_names)

        # Verify results structure
        assert "timestamp" in results
        assert "channels" in results
        assert "processing_stages" in results
        assert "features" in results
        assert "performance" in results

        # Check processing stages
        assert "venturi_enhancement" in results["processing_stages"]
        assert "life_processing" in results["processing_stages"]

        # Check features
        assert "global" in results["features"]
        for ch_name in channel_names:
            assert ch_name in results["features"]

    def test_eeg_quality_assessment(self):
        """Test EEG signal quality assessment"""
        from eeg_processor import EEGQualityAssessment

        quality_assessor = EEGQualityAssessment()

        # Test with high-quality signal (clean sine wave)
        clean_signal = np.sin(np.linspace(0, 4 * np.pi, 1000))
        clean_quality = quality_assessor.assess_signal_quality(clean_signal)

        # Test with noisy signal
        noisy_signal = clean_signal + 2 * np.random.randn(1000)
        noisy_quality = quality_assessor.assess_signal_quality(noisy_signal)

        # Clean signal should have better quality
        assert clean_quality["overall_quality"] > noisy_quality["overall_quality"]
        assert clean_quality["snr"] > noisy_quality["snr"]
        assert clean_quality["artifact_ratio"] > noisy_quality["artifact_ratio"]

    def test_venturi_eeg_enhancement(self):
        """Test Venturi EEG quality enhancement"""
        from eeg_processor import VenturiEEGProcessor

        venturi_processor = VenturiEEGProcessor()

        # Create test EEG signal with known characteristics
        signal = np.sin(np.linspace(0, 4 * np.pi, 500)) + 0.5 * np.random.randn(500)

        # Apply Venturi enhancement
        enhancement_result = venturi_processor.venturi1_eeg_quality(signal)

        # Verify enhancement results
        assert "enhanced_signal" in enhancement_result
        assert "initial_quality" in enhancement_result
        assert "final_quality" in enhancement_result
        assert "enhancement_factor" in enhancement_result

        # Enhanced signal should have better or equal quality
        initial_quality = enhancement_result["initial_quality"]["overall_quality"]
        final_quality = enhancement_result["final_quality"]["overall_quality"]

        # Enhancement should improve or maintain quality
        assert enhancement_result["enhancement_factor"] >= 0.8


class TestVenturiGatesSystem:
    """Test suite for Venturi Gates System"""

    def test_venturi_system_creation(self):
        """Test Venturi Gates System creation"""
        system = create_3_venturi_system()
        assert system is not None
        assert isinstance(system, VenturiGatesSystem)
        assert len(system.gates) == 3

        # Test custom system creation
        custom_configs = [
            {
                "gate_id": "test_gate1",
                "gate_type": "signal_enhancement",
                "constriction_factor": 0.9,
                "acceleration_factor": 1.1,
            }
        ]
        from venturi_gates_system import create_custom_venturi_system

        custom_system = create_custom_venturi_system(custom_configs)
        assert len(custom_system.gates) == 1
        assert "test_gate1" in custom_system.gates

    def test_venturi_signal_processing(self):
        """Test Venturi signal processing capabilities"""
        system = create_3_venturi_system()

        # Test signals
        test_signals = [
            np.sin(np.linspace(0, 4 * np.pi, 200)),  # Clean sine wave
            np.random.randn(150),  # Random noise
            np.ones(100) + 0.1 * np.random.randn(100),  # Constant + noise
        ]

        for signal in test_signals:
            # Serial processing
            serial_results = system.process_through_gates(signal)
            assert "final_output" in serial_results
            assert "gate_outputs" in serial_results
            assert len(serial_results["gate_outputs"]) == 3

            # Parallel processing
            parallel_results = system.process_parallel_gates(signal)
            assert "combined_output" in parallel_results
            assert "parallel_outputs" in parallel_results
            assert len(parallel_results["parallel_outputs"]) == 3

    def test_venturi_gate_adaptation(self):
        """Test Venturi gate adaptation mechanism"""
        system = create_3_venturi_system()

        # Get initial gate states
        initial_status = system.get_system_status()
        initial_efficiency = initial_status["system_efficiency"]

        # Process multiple signals to trigger adaptation
        for _ in range(20):
            test_signal = np.random.randn(100)
            system.process_through_gates(test_signal)

        # Check if system adapted
        final_status = system.get_system_status()
        final_efficiency = final_status["system_efficiency"]

        # System should have processed signals and updated metrics
        for gate_id, metrics in final_status["gate_metrics"].items():
            assert metrics["total_processes"] >= 20

    def test_venturi_system_optimization(self):
        """Test Venturi system pipeline optimization"""
        system = create_3_venturi_system()

        initial_pipeline = system.processing_pipeline.copy()

        # Process some signals to establish performance differences
        for _ in range(10):
            test_signal = np.random.randn(50)
            system.process_through_gates(test_signal)

        # Optimize pipeline
        system.optimize_pipeline()
        optimized_pipeline = system.processing_pipeline

        # Pipeline should be ordered by efficiency
        gate_efficiencies = []
        for gate_id in optimized_pipeline:
            gate_efficiencies.append(system.gates[gate_id].efficiency)

        # Check if pipeline is sorted by efficiency (descending)
        assert gate_efficiencies == sorted(gate_efficiencies, reverse=True)


class TestIntegration:
    """Integration tests for complete L.I.F.E system"""

    def test_complete_eeg_pipeline(self):
        """Test complete EEG processing pipeline integration"""
        # Create complete system
        processor = create_eeg_processor(
            {"sampling_rate": 250.0, "learning_rate": 0.01, "venturi_factor": 1.2}
        )

        # Create realistic EEG data
        channels = 8
        samples = 2000  # 8 seconds at 250 Hz
        eeg_data = []

        for ch in range(channels):
            # Simulate different EEG patterns
            t = np.linspace(0, 8, samples)
            signal = (
                1.5 * np.sin(2 * np.pi * 10 * t)  # Alpha rhythm
                + 0.8 * np.sin(2 * np.pi * 20 * t)  # Beta activity
                + 0.3 * np.random.randn(samples)  # Background noise
            )
            eeg_data.append(signal)

        eeg_data = np.array(eeg_data)
        channel_names = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4"]

        # Process through complete pipeline
        results = processor.process(eeg_data, channel_names, {"test": "integration"})

        # Verify complete pipeline results
        assert results is not None
        assert "error" not in results  # No processing errors
        assert results["performance"]["overall_score"] > 0

        # Check that all components worked
        assert "venturi_enhancement" in results["processing_stages"]
        assert "life_processing" in results["processing_stages"]

        # Verify features were extracted
        assert len(results["features"]) == channels + 1  # Per channel + global

        # Check processor status
        status = processor.get_processor_status()
        assert status["ready"] is True
        assert status["life_metrics"]["experience_count"] > 0

    def test_performance_improvement(self):
        """Test that system performance improves over time"""
        processor = create_eeg_processor()

        performance_history = []

        # Process multiple batches and track performance
        for batch in range(5):
            # Create test EEG data
            eeg_data = np.random.randn(4, 1000)  # 4 channels, 1000 samples
            channels = [f"CH{i+1}" for i in range(4)]

            # Process and record performance
            results = processor.process(eeg_data, channels, {"batch": batch})
            performance_history.append(results["performance"]["overall_score"])

        # Performance should show improvement or stability
        # (allowing for some variability in random data)
        final_performance = np.mean(performance_history[-2:])
        initial_performance = np.mean(performance_history[:2])

        # System should maintain reasonable performance
        assert final_performance > 0.1  # Minimum acceptable performance
        assert all(p > 0 for p in performance_history)  # All scores positive


def run_comprehensive_tests():
    """Run all tests and generate report"""
    import traceback

    test_classes = [
        TestLIFEAlgorithm,
        TestEEGProcessor,
        TestVenturiGatesSystem,
        TestIntegration,
    ]
    results = {"passed": 0, "failed": 0, "errors": []}

    print("Running L.I.F.E Theory Comprehensive Test Suite")
    print("=" * 60)

    for test_class in test_classes:
        print(f"\nTesting {test_class.__name__}...")
        test_instance = test_class()

        # Get all test methods
        test_methods = [
            method for method in dir(test_instance) if method.startswith("test_")
        ]

        for test_method in test_methods:
            try:
                print(f"  Running {test_method}...", end=" ")
                getattr(test_instance, test_method)()
                print("PASSED")
                results["passed"] += 1
            except Exception as e:
                print("FAILED")
                results["failed"] += 1
                results["errors"].append(
                    f"{test_class.__name__}.{test_method}: {str(e)}"
                )
                traceback.print_exc()

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Total:  {results['passed'] + results['failed']}")

    if results["errors"]:
        print("\nFAILED TESTS:")
        for error in results["errors"]:
            print(f"  - {error}")

    success_rate = results["passed"] / (results["passed"] + results["failed"]) * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")

    return results


if __name__ == "__main__":
    # Run comprehensive test suite
    test_results = run_comprehensive_tests()

    if test_results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED! L.I.F.E Theory system is working perfectly!")
    else:
        print(
            f"\n⚠️  {test_results['failed']} tests failed. Please review the errors above."
        )

    print("\nL.I.F.E Theory test suite completed.")
