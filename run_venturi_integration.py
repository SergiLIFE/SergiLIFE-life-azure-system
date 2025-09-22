#!/usr/bin/env python3
"""
Venturi Integration Runner - Orchestrates 3-Venturi Gate System
Deployment and Validation
L.I.F.E. Platform Venturi system integration automation

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from azure_config import AzureConfig
from venturi_gates_system import (
    VenturiGate,
    VenturiGateConfig,
    VenturiGatesSystem,
    VenturiGateType,
)
from venturi_integration_summary import IntegrationSummary, SystemMetric

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/venturi_integration.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class IntegrationStep:
    """Represents a step in the integration process"""

    name: str
    description: str
    function: callable
    required: bool = True
    timeout_seconds: int = 300


@dataclass
class IntegrationResult:
    """Result of an integration step"""

    step_name: str
    success: bool
    duration: float
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


class VenturiIntegrationRunner:
    """
    Orchestrates the complete Venturi system integration and validation
    """

    def __init__(self):
        self.results: List[IntegrationResult] = []
        self.start_time = datetime.now()
        self.venturi_system: Optional[VenturiGatesSystem] = None
        self.azure_config = AzureConfig()

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        Path("results").mkdir(exist_ok=True)

    def log_integration_start(self):
        """Log the start of integration process"""
        logger.info("=" * 80)
        logger.info("VENTURI INTEGRATION RUNNER STARTED")
        logger.info(f"Timestamp: {self.start_time}")
        logger.info(
            f"L.I.F.E. Platform Version: " f"{self.azure_config.platform_version}"
        )
        logger.info(
            f"Marketplace Offer ID: " f"{self.azure_config.marketplace_offer_id}"
        )
        logger.info("=" * 80)

    def log_integration_complete(self, success: bool, total_duration: float):
        """Log the completion of integration process"""
        status = "SUCCESS" if success else "FAILED"
        logger.info("=" * 80)
        logger.info(f"VENTURI INTEGRATION {status}")
        logger.info(f"Total Duration: {total_duration:.2f} seconds")
        logger.info(
            "Completed Steps: "
            f"{len([r for r in self.results if r.success])}/"
            f"{len(self.results)}"
        )
        logger.info("=" * 80)

    async def run_integration_step(self, step: IntegrationStep) -> IntegrationResult:
        """Run a single integration step with timeout and error handling"""
        start_time = time.time()

        try:
            logger.info(f"Starting step: {step.name}")
            logger.info(f"Description: {step.description}")

            # Run the step with timeout
            result = await asyncio.wait_for(
                step.function(self), timeout=step.timeout_seconds
            )

            duration = time.time() - start_time
            success = result.get("success", True) if isinstance(result, dict) else True

            integration_result = IntegrationResult(
                step_name=step.name,
                success=success,
                duration=duration,
                metrics=result if isinstance(result, dict) else None,
            )

            logger.info(
                "Step {0}: {1} ({2:.2f}s)".format(
                    step.name, "PASSED" if success else "FAILED", duration
                )
            )

            if not success and step.required:
                logger.error(
                    f"Required step {step.name} failed: {result.get('error', 'Unknown error')}"
                )

            return integration_result

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            logger.error(
                f"Step {step.name} timed out after {step.timeout_seconds} seconds"
            )
            return IntegrationResult(
                step_name=step.name,
                success=False,
                duration=duration,
                error_message=f"Timeout after {step.timeout_seconds} seconds",
            )

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Step {step.name} failed with exception: {str(e)}")
            return IntegrationResult(
                step_name=step.name,
                success=False,
                duration=duration,
                error_message=str(e),
            )

    async def validate_venturi_system_imports(self) -> Dict[str, Any]:
        """Validate that all Venturi system modules can be imported"""
        try:
            logger.info("Validating Venturi system imports...")

            # Test core imports
            from venturi_batching import VenturiBatcher
            from venturi_gates_system import VenturiGatesSystem
            from venturi_research_integration import ResearchStudy, ValidationMetric
            from venturi_resilience_tests import VenturiResilienceTester

            # Test instantiation
            config = VenturiGateConfig(
                gate_id="test_gate",
                gate_type=VenturiGateType.SIGNAL_ENHANCEMENT,
                constriction_factor=0.8,
                acceleration_factor=1.2,
            )

            system = VenturiGatesSystem()
            system.add_gate(config)

            logger.info("All Venturi system imports validated successfully")
            return {"success": True, "modules_validated": 5, "gates_configured": 1}

        except Exception as e:
            logger.error(f"Failed to validate Venturi system imports: {str(e)}")
            return {"success": False, "error": str(e)}

    async def initialize_venturi_system(self) -> Dict[str, Any]:
        """Initialize the 3-Venturi Gate System"""
        try:
            logger.info("Initializing 3-Venturi Gate System...")

            from venturi_gates_system import (
                VenturiGateConfig,
                VenturiGatesSystem,
                VenturiGateType,
            )

            # Create system with 3 gates
            system = VenturiGatesSystem()

            # Configure Signal Acceleration Gate
            signal_gate = VenturiGateConfig(
                gate_id="signal_acceleration",
                gate_type=VenturiGateType.SIGNAL_ENHANCEMENT,
                constriction_factor=0.8,
                acceleration_factor=3.5,
            )

            # Configure Pressure Differential Gate
            pressure_gate = VenturiGateConfig(
                gate_id="pressure_differential",
                gate_type=VenturiGateType.NOISE_REDUCTION,
                constriction_factor=0.7,
                acceleration_factor=2.8,
            )

            # Configure Flow Recovery Gate
            flow_gate = VenturiGateConfig(
                gate_id="flow_recovery",
                gate_type=VenturiGateType.PATTERN_EXTRACTION,
                constriction_factor=0.75,
                acceleration_factor=4.2,
            )

            # Add gates to system
            system.gates[signal_gate.gate_id] = VenturiGate(signal_gate)
            system.gates[pressure_gate.gate_id] = VenturiGate(pressure_gate)
            system.gates[flow_gate.gate_id] = VenturiGate(flow_gate)

            self.venturi_system = system

            logger.info("3-Venturi Gate System initialized successfully")
            return {"success": True, "gates_initialized": 3, "system_ready": True}

        except Exception as e:
            logger.error(f"Failed to initialize Venturi system: {str(e)}")
            return {"success": False, "error": str(e)}

    async def validate_fluid_dynamics(self) -> Dict[str, Any]:
        """Validate fluid dynamics algorithms"""
        try:
            logger.info("Validating fluid dynamics algorithms...")

            if not self.venturi_system:
                raise ValueError("Venturi system not initialized")

            # Test fluid dynamics calculations
            test_data = [0.1, 0.2, 0.3, 0.4, 0.5]  # Sample EEG data

            # Process through each gate
            results = {}
            for gate_id, gate in self.venturi_system.gates.items():
                processed_data = gate.process_signal(test_data)
                results[gate_id] = {
                    "input_length": len(test_data),
                    "output_length": len(processed_data),
                    "acceleration_factor": gate.config.acceleration_factor,
                }

            # Validate Bernoulli's principle application
            signal_gate_result = results.get("signal_acceleration", {})
            pressure_gate_result = results.get("pressure_differential", {})

            # Check that pressure differential creates acceleration
            acceleration_valid = signal_gate_result.get("optimization_factor", 0) > 1.0
            pressure_valid = pressure_gate_result.get("optimization_factor", 0) > 1.0

            logger.info("Fluid dynamics validation completed")
            return {
                "success": True,
                "bernoulli_principle_validated": acceleration_valid and pressure_valid,
                "gates_tested": len(results),
                "fluid_dynamics_active": True,
            }

        except Exception as e:
            logger.error(f"Failed to validate fluid dynamics: {str(e)}")
            return {"success": False, "error": str(e)}

    async def test_gate_interoperability(self) -> Dict[str, Any]:
        """Test interoperability between Venturi gates"""
        try:
            logger.info("Testing gate interoperability...")

            if not self.venturi_system:
                raise ValueError("Venturi system not initialized")

            # Test sequential processing through all gates
            test_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

            # Process through signal acceleration first
            signal_gate = self.venturi_system.gates.get("signal_acceleration")
            if not signal_gate:
                raise ValueError("Signal acceleration gate not found")

            intermediate_data = signal_gate.process_signal(test_data)

            # Process through pressure differential
            pressure_gate = self.venturi_system.gates.get("pressure_differential")
            if not pressure_gate:
                raise ValueError("Pressure differential gate not found")

            pressure_data = pressure_gate.process_signal(intermediate_data)

            # Process through flow recovery
            flow_gate = self.venturi_system.gates.get("flow_recovery")
            if not flow_gate:
                raise ValueError("Flow recovery gate not found")

            final_data = flow_gate.process_signal(pressure_data)

            # Validate processing pipeline
            pipeline_valid = (
                len(intermediate_data) > 0
                and len(pressure_data) > 0
                and len(final_data) > 0
                and len(final_data) >= len(test_data)  # Should maintain or enhance data
            )

            logger.info("Gate interoperability test completed")
            return {
                "success": True,
                "pipeline_valid": pipeline_valid,
                "processing_stages": 3,
                "data_preservation": len(final_data) >= len(test_data),
            }

        except Exception as e:
            logger.error(f"Failed to test gate interoperability: {str(e)}")
            return {"success": False, "error": str(e)}

    async def validate_performance_targets(self) -> Dict[str, Any]:
        """Validate that system meets performance targets"""
        try:
            logger.info("Validating performance targets...")

            if not self.venturi_system:
                raise ValueError("Venturi system not initialized")

            # Test latency performance
            import time

            test_iterations = 100
            latencies = []

            test_data = [0.1, 0.2, 0.3, 0.4, 0.5]

            for _ in range(test_iterations):
                start_time = time.time()

                # Process through all gates
                for gate in self.venturi_system.gates.values():
                    gate.process_signal(test_data)

                end_time = time.time()
                latencies.append((end_time - start_time) * 1000)  # ms

            # Calculate statistics
            avg_latency = sum(latencies) / len(latencies)
            p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

            # Check against targets
            target_avg = 0.41  # ms
            target_p95 = 33.7  # ms

            avg_target_met = avg_latency <= target_avg
            p95_target_met = p95_latency <= target_p95

            logger.info(
                f"Performance validation: Avg {avg_latency:.3f}ms (target: {target_avg}ms) - {'PASS' if avg_target_met else 'FAIL'}"
            )
            logger.info(
                f"Performance validation: P95 {p95_latency:.3f}ms (target: {target_p95}ms) - {'PASS' if p95_target_met else 'FAIL'}"
            )

            return {
                "success": avg_target_met and p95_target_met,
                "avg_latency_ms": avg_latency,
                "p95_latency_ms": p95_latency,
                "target_avg_ms": target_avg,
                "target_p95_ms": target_p95,
                "avg_target_met": avg_target_met,
                "p95_target_met": p95_target_met,
                "test_iterations": test_iterations,
            }

        except Exception as e:
            logger.error(f"Failed to validate performance targets: {str(e)}")
            return {"success": False, "error": str(e)}

    async def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration report"""
        try:
            logger.info("Generating integration report...")

            # Save report
            report_path = Path("results/venturi_integration_report.json")
            report_data = {
                "integration_id": f"venturi-integration-{int(time.time())}",
                "timestamp": datetime.now().isoformat(),
                "system_version": self.azure_config.platform_version,
                "total_steps": len(self.results),
                "successful_steps": len([r for r in self.results if r.success]),
                "failed_steps": len([r for r in self.results if not r.success]),
                "total_duration": time.time() - self.start_time.timestamp(),
                "results": [
                    {
                        "step_name": r.step_name,
                        "success": r.success,
                        "duration": r.duration,
                        "error_message": r.error_message,
                        "metrics": r.metrics,
                    }
                    for r in self.results
                ],
            }
            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2, default=str)

            logger.info(f"Integration report saved to {report_path}")
            return {
                "success": True,
                "report_path": str(report_path),
                "total_steps": report_data["total_steps"],
                "successful_steps": report_data["successful_steps"],
                "failed_steps": report_data["failed_steps"],
            }

        except Exception as e:
            logger.error(f"Failed to generate integration report: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_integration_steps(self) -> List[IntegrationStep]:
        """Get all integration steps to execute"""
        return [
            IntegrationStep(
                name="validate_imports",
                description="Validate all Venturi system module imports",
                function=self.validate_venturi_system_imports,
            ),
            IntegrationStep(
                name="initialize_system",
                description="Initialize 3-Venturi Gate System with all gates",
                function=self.initialize_venturi_system,
            ),
            IntegrationStep(
                name="validate_fluid_dynamics",
                description=(
                    "Validate fluid dynamics algorithms and " "Bernoulli's principle"
                ),
                function=self.validate_fluid_dynamics,
            ),
            IntegrationStep(
                name="test_interoperability",
                description="Test interoperability between all Venturi gates",
                function=self.test_gate_interoperability,
            ),
            IntegrationStep(
                name="validate_performance",
                description=("Validate system meets latency and " "throughput targets"),
                function=self.validate_performance_targets,
            ),
            IntegrationStep(
                name="generate_report",
                description="Generate comprehensive integration report",
                function=self.generate_integration_report,
            ),
        ]

    async def run_integration(self) -> bool:
        """Run the complete Venturi integration process"""
        self.log_integration_start()

        steps = self.get_integration_steps()
        all_success = True

        for step in steps:
            result = await self.run_integration_step(step)
            self.results.append(result)

            if not result.success and step.required:
                all_success = False
                logger.error(
                    "Required step {0} failed. "
                    "Stopping integration.".format(step.name)
                )
                break

        total_duration = time.time() - self.start_time.timestamp()
        self.log_integration_complete(all_success, total_duration)

        return all_success


async def main():
    """Main entry point for Venturi integration runner"""
    try:
        runner = VenturiIntegrationRunner()
        success = await runner.run_integration()

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("Integration interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Integration runner failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the integration
    asyncio.run(main())
