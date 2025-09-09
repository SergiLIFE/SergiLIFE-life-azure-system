"""
Advanced L.I.F.E Theory Benchmark Validation System
Comprehensive testing and validation framework for all L.I.F.E components

Copyright 2025 - Sergio Paya Borrull
"""

import numpy as np
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import traceback
import matplotlib.pyplot as plt
from pathlib import Path

# Import L.I.F.E Theory components
from lifetheory import create_life_algorithm
from eeg_processor import create_eeg_processor
from venturi_gates_system import create_3_venturi_system
from quantum_life_processor import create_quantum_processor, QuantumAlgorithmType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    """Benchmark result structure"""
    component_name: str
    test_name: str
    execution_time: float
    accuracy_score: float
    performance_metrics: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    system_version: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    overall_score: float
    execution_time: float
    benchmark_results: List[BenchmarkResult]
    system_metrics: Dict[str, Any]
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class LIFEBenchmarkSuite:
    """Comprehensive benchmark suite for L.I.F.E Theory system"""
    
    def __init__(self):
        self.results = []
        self.processors = {}
        self.test_data = {}
        self.benchmark_config = {
            "num_trials": 10,
            "timeout_seconds": 30,
            "accuracy_threshold": 0.75,
            "performance_threshold": 1.0
        }
        
        logger.info("L.I.F.E Theory Benchmark Suite initialized")
    
    def initialize_test_components(self):
        """Initialize all L.I.F.E Theory components for testing"""
        try:
            logger.info("Initializing L.I.F.E Theory components...")
            
            # Initialize core L.I.F.E algorithm
            life_config = {
                "learning_rate": 0.01,
                "max_experiences": 1000,
                "venturi_gate_factor": 1.2
            }
            self.processors["life_algorithm"] = create_life_algorithm(life_config)
            
            # Initialize EEG processor
            eeg_config = {
                "sampling_rate": 250.0,
                "learning_rate": 0.005,
                "venturi_factor": 1.2,
                "max_experiences": 1000
            }
            self.processors["eeg_processor"] = create_eeg_processor(eeg_config)
            
            # Initialize Venturi system
            self.processors["venturi_system"] = create_3_venturi_system()
            
            # Initialize quantum processor
            self.processors["quantum_processor"] = create_quantum_processor(
                num_qubits=4, 
                algorithm=QuantumAlgorithmType.LIFE_QNN
            )
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}")
            return False
    
    def generate_test_datasets(self):
        """Generate comprehensive test datasets"""
        try:
            logger.info("Generating test datasets...")
            
            # EEG test data
            self.test_data["eeg_data"] = {
                "channels": 4,
                "samples": 1000,
                "sampling_rate": 250.0,
                "data": np.random.randn(4, 1000) * 50,  # Typical EEG amplitude
                "channel_names": ["Fp1", "Fp2", "C3", "C4"]
            }
            
            # Signal processing test data
            t = np.linspace(0, 4, 1000)
            self.test_data["signals"] = {
                "sine_wave": np.sin(2 * np.pi * 10 * t),
                "noisy_signal": np.sin(2 * np.pi * 10 * t) + 0.3 * np.random.randn(1000),
                "complex_signal": (np.sin(2 * np.pi * 5 * t) + 
                                 0.5 * np.sin(2 * np.pi * 15 * t) + 
                                 0.2 * np.random.randn(1000)),
                "time": t
            }
            
            # Machine learning test data
            self.test_data["ml_data"] = {
                "classification": {
                    "X": np.random.randn(100, 10),
                    "y": np.random.randint(0, 2, 100)
                },
                "regression": {
                    "X": np.random.randn(100, 5),
                    "y": np.random.randn(100)
                }
            }
            
            # Quantum test data
            self.test_data["quantum_data"] = {
                "small_signal": np.random.randn(4),
                "medium_signal": np.random.randn(16),
                "quantum_states": [np.random.randn(16) + 1j * np.random.randn(16) for _ in range(5)]
            }
            
            logger.info("Test datasets generated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate test datasets: {str(e)}")
            return False
    
    def benchmark_life_algorithm(self) -> List[BenchmarkResult]:
        """Benchmark core L.I.F.E algorithm"""
        results = []
        algorithm = self.processors["life_algorithm"]
        
        # Test 1: Basic processing
        start_time = time.time()
        try:
            test_data = self.test_data["signals"]["noisy_signal"][:100]
            processed = algorithm.process(test_data)
            
            execution_time = time.time() - start_time
            
            # Calculate accuracy (signal enhancement)
            snr_original = self._calculate_snr(test_data)
            snr_processed = self._calculate_snr(processed)
            accuracy = min(1.0, snr_processed / (snr_original + 1e-8))
            
            metrics = algorithm.get_performance_metrics()
            
            results.append(BenchmarkResult(
                component_name="L.I.F.E Algorithm",
                test_name="Basic Signal Processing",
                execution_time=execution_time,
                accuracy_score=accuracy,
                performance_metrics=metrics,
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="L.I.F.E Algorithm",
                test_name="Basic Signal Processing",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        # Test 2: Adaptive learning
        start_time = time.time()
        try:
            # Multiple processing rounds to test adaptation
            accuracy_scores = []
            for i in range(5):
                test_signal = self.test_data["signals"]["sine_wave"] + 0.1 * np.random.randn(1000)
                processed = algorithm.process(test_signal[:50])
                snr_orig = self._calculate_snr(test_signal[:50])
                snr_proc = self._calculate_snr(processed)
                accuracy_scores.append(snr_proc / (snr_orig + 1e-8))
            
            execution_time = time.time() - start_time
            
            # Check if learning improves over time
            improvement = accuracy_scores[-1] - accuracy_scores[0]
            accuracy = min(1.0, max(0.0, improvement + 0.5))
            
            results.append(BenchmarkResult(
                component_name="L.I.F.E Algorithm",
                test_name="Adaptive Learning",
                execution_time=execution_time,
                accuracy_score=accuracy,
                performance_metrics={"improvement": improvement, "scores": accuracy_scores},
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="L.I.F.E Algorithm",
                test_name="Adaptive Learning",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def benchmark_eeg_processor(self) -> List[BenchmarkResult]:
        """Benchmark EEG processor"""
        results = []
        processor = self.processors["eeg_processor"]
        
        # Test 1: EEG signal processing
        start_time = time.time()
        try:
            eeg_data = self.test_data["eeg_data"]["data"]
            channel_names = self.test_data["eeg_data"]["channel_names"]
            
            processed_result = processor.process(eeg_data, channel_names)
            execution_time = time.time() - start_time
            
            # Evaluate processing quality
            quality_score = processed_result["performance"]["overall_score"]
            
            results.append(BenchmarkResult(
                component_name="EEG Processor",
                test_name="Multi-channel EEG Processing",
                execution_time=execution_time,
                accuracy_score=quality_score,
                performance_metrics=processed_result["performance"],
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="EEG Processor",
                test_name="Multi-channel EEG Processing",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        # Test 2: Real-time processing simulation
        start_time = time.time()
        try:
            processing_times = []
            
            # Simulate real-time chunks
            chunk_size = 125  # 0.5 seconds at 250 Hz
            for i in range(0, eeg_data.shape[1] - chunk_size, chunk_size):
                chunk_start = time.time()
                chunk_data = eeg_data[:, i:i+chunk_size]
                processor.process(chunk_data, channel_names)
                processing_times.append(time.time() - chunk_start)
            
            execution_time = time.time() - start_time
            avg_processing_time = np.mean(processing_times)
            
            # Real-time requirement: process 0.5s of data in < 0.5s
            real_time_performance = min(1.0, 0.5 / (avg_processing_time + 1e-8))
            
            results.append(BenchmarkResult(
                component_name="EEG Processor",
                test_name="Real-time Processing",
                execution_time=execution_time,
                accuracy_score=real_time_performance,
                performance_metrics={
                    "avg_processing_time": avg_processing_time,
                    "real_time_factor": real_time_performance
                },
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="EEG Processor",
                test_name="Real-time Processing",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def benchmark_venturi_system(self) -> List[BenchmarkResult]:
        """Benchmark Venturi gates system"""
        results = []
        venturi = self.processors["venturi_system"]
        
        # Test 1: Signal enhancement
        start_time = time.time()
        try:
            test_signal = self.test_data["signals"]["noisy_signal"]
            
            enhancement_result = venturi.process_through_gates(test_signal)
            execution_time = time.time() - start_time
            
            # Evaluate enhancement
            efficiency = enhancement_result["system_efficiency"]
            
            results.append(BenchmarkResult(
                component_name="Venturi System",
                test_name="Signal Enhancement",
                execution_time=execution_time,
                accuracy_score=efficiency,
                performance_metrics=enhancement_result,
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="Venturi System",
                test_name="Signal Enhancement",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        # Test 2: Parallel processing
        start_time = time.time()
        try:
            test_signal = self.test_data["signals"]["complex_signal"]
            
            parallel_result = venturi.process_parallel_gates(test_signal)
            execution_time = time.time() - start_time
            
            parallel_efficiency = parallel_result["system_efficiency"]
            
            results.append(BenchmarkResult(
                component_name="Venturi System",
                test_name="Parallel Processing",
                execution_time=execution_time,
                accuracy_score=parallel_efficiency,
                performance_metrics=parallel_result,
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="Venturi System",
                test_name="Parallel Processing",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def benchmark_quantum_processor(self) -> List[BenchmarkResult]:
        """Benchmark quantum processor"""
        results = []
        quantum = self.processors["quantum_processor"]
        
        # Test 1: Quantum neural network
        start_time = time.time()
        try:
            input_data = self.test_data["quantum_data"]["small_signal"]
            target = np.array([0.5, -0.5, 0.2, -0.2])
            
            qnn_result = quantum.life_quantum_neural_network(input_data, target)
            execution_time = time.time() - start_time
            
            # Calculate accuracy based on loss
            accuracy = max(0.0, 1.0 - qnn_result["loss"])
            
            results.append(BenchmarkResult(
                component_name="Quantum Processor",
                test_name="Quantum Neural Network",
                execution_time=execution_time,
                accuracy_score=accuracy,
                performance_metrics=qnn_result,
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="Quantum Processor",
                test_name="Quantum Neural Network",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        # Test 2: Quantum feature mapping
        start_time = time.time()
        try:
            test_data = self.test_data["quantum_data"]["small_signal"]
            
            features = quantum.quantum_feature_map(test_data)
            execution_time = time.time() - start_time
            
            # Evaluate feature quality (dimensionality and variance)
            feature_variance = np.var(features)
            feature_quality = min(1.0, feature_variance / (feature_variance + 1e-8))
            
            results.append(BenchmarkResult(
                component_name="Quantum Processor",
                test_name="Quantum Feature Mapping",
                execution_time=execution_time,
                accuracy_score=feature_quality,
                performance_metrics={
                    "feature_dimension": len(features),
                    "feature_variance": feature_variance
                },
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="Quantum Processor",
                test_name="Quantum Feature Mapping",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def benchmark_system_integration(self) -> List[BenchmarkResult]:
        """Benchmark full system integration"""
        results = []
        
        # Test 1: EEG + Venturi + L.I.F.E pipeline
        start_time = time.time()
        try:
            # Start with EEG data
            eeg_data = self.test_data["eeg_data"]["data"]
            channel_names = self.test_data["eeg_data"]["channel_names"]
            
            # Process through EEG processor
            eeg_result = self.processors["eeg_processor"].process(eeg_data, channel_names)
            
            # Extract signal for Venturi processing
            processed_signal = eeg_result["channels"]["Fp1"]["processed_signal"]
            
            # Apply Venturi enhancement
            venturi_result = self.processors["venturi_system"].process_through_gates(processed_signal)
            
            # Final L.I.F.E processing
            final_signal = venturi_result["final_output"]
            life_result = self.processors["life_algorithm"].process(final_signal[:100])
            
            execution_time = time.time() - start_time
            
            # Calculate integrated performance
            eeg_score = eeg_result["performance"]["overall_score"]
            venturi_score = venturi_result["system_efficiency"]
            
            # Signal quality improvement
            original_snr = self._calculate_snr(processed_signal)
            final_snr = self._calculate_snr(life_result)
            snr_improvement = final_snr / (original_snr + 1e-8)
            
            integrated_score = (eeg_score + venturi_score + min(1.0, snr_improvement)) / 3
            
            results.append(BenchmarkResult(
                component_name="System Integration",
                test_name="EEG-Venturi-LIFE Pipeline",
                execution_time=execution_time,
                accuracy_score=integrated_score,
                performance_metrics={
                    "eeg_score": eeg_score,
                    "venturi_score": venturi_score,
                    "snr_improvement": snr_improvement,
                    "pipeline_stages": 3
                },
                success=True
            ))
            
        except Exception as e:
            results.append(BenchmarkResult(
                component_name="System Integration",
                test_name="EEG-Venturi-LIFE Pipeline",
                execution_time=time.time() - start_time,
                accuracy_score=0.0,
                performance_metrics={},
                success=False,
                error_message=str(e)
            ))
        
        return results
    
    def _calculate_snr(self, signal: np.ndarray) -> float:
        """Calculate signal-to-noise ratio"""
        try:
            signal_power = np.mean(signal**2)
            noise_estimate = np.var(np.diff(signal)) / 2  # High-frequency variance as noise
            snr = 10 * np.log10(signal_power / (noise_estimate + 1e-8))
            return max(0, snr)
        except:
            return 0.0
    
    def run_comprehensive_benchmark(self) -> ValidationReport:
        """Run complete benchmark suite"""
        start_time = time.time()
        logger.info("Starting comprehensive L.I.F.E Theory benchmark...")
        
        # Initialize components and datasets
        if not self.initialize_test_components():
            return ValidationReport(
                system_version="1.0.0",
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                overall_score=0.0,
                execution_time=0.0,
                benchmark_results=[],
                system_metrics={"error": "Failed to initialize components"}
            )
        
        if not self.generate_test_datasets():
            return ValidationReport(
                system_version="1.0.0",
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                overall_score=0.0,
                execution_time=0.0,
                benchmark_results=[],
                system_metrics={"error": "Failed to generate test datasets"}
            )
        
        # Run all benchmarks
        all_results = []
        
        # Component benchmarks
        all_results.extend(self.benchmark_life_algorithm())
        all_results.extend(self.benchmark_eeg_processor())
        all_results.extend(self.benchmark_venturi_system())
        all_results.extend(self.benchmark_quantum_processor())
        
        # Integration benchmarks
        all_results.extend(self.benchmark_system_integration())
        
        # Calculate overall metrics
        total_time = time.time() - start_time
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.success)
        failed_tests = total_tests - passed_tests
        
        # Calculate overall score
        if total_tests > 0:
            accuracy_scores = [r.accuracy_score for r in all_results if r.success]
            overall_score = np.mean(accuracy_scores) if accuracy_scores else 0.0
        else:
            overall_score = 0.0
        
        # Collect system metrics
        system_metrics = {
            "avg_execution_time": np.mean([r.execution_time for r in all_results]),
            "max_execution_time": max([r.execution_time for r in all_results]),
            "components_tested": ["L.I.F.E Algorithm", "EEG Processor", "Venturi System", "Quantum Processor"],
            "integration_tests": 1,
            "benchmark_config": self.benchmark_config
        }
        
        # Create validation report
        report = ValidationReport(
            system_version="1.0.0",
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            overall_score=overall_score,
            execution_time=total_time,
            benchmark_results=all_results,
            system_metrics=system_metrics
        )
        
        logger.info(f"Benchmark completed: {passed_tests}/{total_tests} tests passed")
        logger.info(f"Overall score: {overall_score:.3f}")
        logger.info(f"Total execution time: {total_time:.2f} seconds")
        
        return report
    
    def save_benchmark_report(self, report: ValidationReport, output_path: str = "benchmark_report.json"):
        """Save benchmark report to file"""
        try:
            report_dict = asdict(report)
            
            with open(output_path, 'w') as f:
                json.dump(report_dict, f, indent=2, default=str)
            
            logger.info(f"Benchmark report saved to: {output_path}")
            
            # Also create a summary text report
            summary_path = output_path.replace('.json', '_summary.txt')
            self._create_text_summary(report, summary_path)
            
        except Exception as e:
            logger.error(f"Failed to save benchmark report: {str(e)}")
    
    def _create_text_summary(self, report: ValidationReport, output_path: str):
        """Create human-readable summary"""
        try:
            with open(output_path, 'w') as f:
                f.write("L.I.F.E THEORY BENCHMARK VALIDATION REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"System Version: {report.system_version}\n")
                f.write(f"Timestamp: {report.timestamp}\n")
                f.write(f"Total Execution Time: {report.execution_time:.2f} seconds\n\n")
                
                f.write("OVERALL RESULTS\n")
                f.write("-" * 20 + "\n")
                f.write(f"Tests Run: {report.total_tests}\n")
                f.write(f"Tests Passed: {report.passed_tests}\n")
                f.write(f"Tests Failed: {report.failed_tests}\n")
                f.write(f"Success Rate: {(report.passed_tests/report.total_tests)*100:.1f}%\n")
                f.write(f"Overall Score: {report.overall_score:.3f}\n\n")
                
                f.write("COMPONENT RESULTS\n")
                f.write("-" * 20 + "\n")
                
                components = {}
                for result in report.benchmark_results:
                    comp = result.component_name
                    if comp not in components:
                        components[comp] = []
                    components[comp].append(result)
                
                for comp_name, results in components.items():
                    f.write(f"\n{comp_name}:\n")
                    for result in results:
                        status = "PASS" if result.success else "FAIL"
                        f.write(f"  - {result.test_name}: {status} "
                               f"(Score: {result.accuracy_score:.3f}, "
                               f"Time: {result.execution_time:.3f}s)\n")
                        if not result.success and result.error_message:
                            f.write(f"    Error: {result.error_message}\n")
                
                f.write(f"\nReport generated: {datetime.now().isoformat()}\n")
                f.write("End of Report\n")
            
            logger.info(f"Text summary saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to create text summary: {str(e)}")

def run_life_theory_validation():
    """Main function to run L.I.F.E Theory validation"""
    print("L.I.F.E THEORY COMPREHENSIVE VALIDATION")
    print("=" * 50)
    
    # Create benchmark suite
    benchmark = LIFEBenchmarkSuite()
    
    # Run comprehensive benchmark
    report = benchmark.run_comprehensive_benchmark()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"life_theory_benchmark_{timestamp}.json"
    benchmark.save_benchmark_report(report, output_file)
    
    # Print summary
    print(f"\nVALIDATION COMPLETE")
    print(f"Total Tests: {report.total_tests}")
    print(f"Passed: {report.passed_tests}")
    print(f"Failed: {report.failed_tests}")
    print(f"Overall Score: {report.overall_score:.3f}")
    print(f"Execution Time: {report.execution_time:.2f} seconds")
    print(f"Report saved to: {output_file}")
    
    return report

if __name__ == "__main__":
    # Run validation
    validation_report = run_life_theory_validation()
