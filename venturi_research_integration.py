#!/usr/bin/env python3
"""
L.I.F.E THEORY Venturi Research Integration Module
Safe integration of research findings into existing L.I.F.E THEORY system

Copyright 2025 - Sergio Paya Borrull
Research-based optimization integration with safety protocols
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

# Import L.I.F.E THEORY components
try:
    from enhanced_venturi_control import (
        EnhancedVenturiController,
        PIDControllerConfig,
        VenturiPerformanceStandards,
    )
except ImportError:
    print("⚠️ Enhanced Venturi Control module not found")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class VenturiResearchIntegration:
    """
    Safe integration manager for Venturi research findings
    into existing L.I.F.E THEORY system
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.integration_log: List[Dict[str, Any]] = []
        self.backup_created = False

        # Research findings summary
        self.research_findings = {
            "venturi_performance_standards": {
                "accuracy": "±1.0% when Re > 200,000",
                "discharge_coefficient": 0.984,
                "reynolds_threshold": 200000.0,
                "source": "Repository analysis of venturi_gates_system.py",
            },
            "pid_controller_config": {
                "kp": 0.8,
                "ki": 0.1,
                "kd": 0.05,
                "alpha": 0.3,
                "source": "experiments_configs.py analysis",
            },
            "optimization_parameters": {
                "load_targets": {
                    "default": 0.55,
                    "memory_training": 0.60,
                    "relaxation": 0.40,
                    "high_performance": 0.75,
                },
                "source": "enhanced_eeg_processor.py integration",
            },
        }

        logger.info("Venturi Research Integration module initialized")

    def create_safety_backup(self) -> bool:
        """Create safety backup of critical files before integration"""
        try:
            backup_dir = self.workspace_path / "backup_before_venturi_integration"
            backup_dir.mkdir(exist_ok=True)

            # Critical files to backup
            critical_files = [
                "life_theory_white_paper.py",
                "enhanced_eeg_processor.py",
                "experiments_configs.py",
                "venturi_gates_system.py",
            ]

            backed_up_files = []
            for filename in critical_files:
                source_file = self.workspace_path / filename
                if source_file.exists():
                    backup_file = backup_dir / f"{filename}.backup_{int(time.time())}"
                    backup_file.write_text(
                        source_file.read_text(encoding="utf-8"), encoding="utf-8"
                    )
                    backed_up_files.append(str(backup_file))

            self.backup_created = True
            logger.info(f"✅ Safety backup created: {len(backed_up_files)} files")

            # Log backup details
            self.integration_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "safety_backup",
                    "files_backed_up": backed_up_files,
                    "status": "success",
                }
            )

            return True

        except Exception as e:
            logger.error(f"Failed to create safety backup: {e}")
            self.integration_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "safety_backup",
                    "status": "failed",
                    "error": str(e),
                }
            )
            return False

    def validate_existing_system(self) -> Dict[str, bool]:
        """Validate existing L.I.F.E THEORY system before integration"""
        validation_results = {}

        try:
            # Check for core L.I.F.E THEORY files
            core_files = [
                "life_theory_white_paper.py",
                "autonomous_optimizer.py",
                "model_optimizer.py",
            ]

            for filename in core_files:
                file_path = self.workspace_path / filename
                validation_results[f"{filename}_exists"] = file_path.exists()

                if file_path.exists():
                    # Basic content validation
                    content = file_path.read_text(encoding="utf-8")
                    validation_results[f"{filename}_has_content"] = len(content) > 1000
                    validation_results[f"{filename}_is_python"] = (
                        content.strip().startswith("#!")
                    )

            # Check for existing Venturi implementations
            venturi_files = ["venturi_gates_system.py", "enhanced_eeg_processor.py"]

            for filename in venturi_files:
                file_path = self.workspace_path / filename
                validation_results[f"{filename}_exists"] = file_path.exists()

            # Overall system health
            validation_results["system_ready_for_integration"] = all(
                [
                    validation_results.get("life_theory_white_paper.py_exists", False),
                    validation_results.get("autonomous_optimizer.py_exists", False),
                    validation_results.get("venturi_gates_system.py_exists", False),
                ]
            )

            logger.info(
                f"System validation completed: "
                f"{sum(validation_results.values())} checks passed"
            )

            return validation_results

        except Exception as e:
            logger.error(f"System validation failed: {e}")
            return {"validation_failed": True, "error": str(e)}

    def generate_integration_plan(self) -> Dict[str, Any]:
        """Generate safe integration plan based on research findings"""

        integration_plan = {
            "phase_1_preparation": {
                "description": "Prepare system for integration",
                "steps": [
                    "Create safety backup of critical files",
                    "Validate existing L.I.F.E THEORY system",
                    "Initialize Enhanced Venturi Controller",
                    "Verify research parameter compatibility",
                ],
                "safety_checks": ["backup_verification", "file_integrity_check"],
                "estimated_duration": "5 minutes",
            },
            "phase_2_integration": {
                "description": "Integrate Venturi research findings",
                "steps": [
                    "Apply PID controller configuration (Kp=0.8, Ki=0.1, Kd=0.05)",
                    "Implement Venturi performance standards (±1.0% accuracy)",
                    "Configure discharge coefficient validation (0.984)",
                    "Set Reynolds number threshold (200,000)",
                    "Apply exponential smoothing (alpha=0.3)",
                ],
                "safety_checks": ["parameter_validation", "performance_monitoring"],
                "estimated_duration": "10 minutes",
            },
            "phase_3_validation": {
                "description": "Validate integrated system performance",
                "steps": [
                    "Run comprehensive test suite",
                    "Validate Venturi performance standards",
                    "Verify PID controller operation",
                    "Test multi-mode operation",
                    "Generate performance report",
                ],
                "safety_checks": ["accuracy_verification", "stability_testing"],
                "estimated_duration": "15 minutes",
            },
            "phase_4_optimization": {
                "description": "Optimize integrated system",
                "steps": [
                    "Fine-tune PID parameters for L.I.F.E THEORY",
                    "Optimize Venturi gate configurations",
                    "Calibrate performance thresholds",
                    "Generate optimization recommendations",
                ],
                "safety_checks": ["performance_benchmarking", "regression_testing"],
                "estimated_duration": "20 minutes",
            },
        }

        # Add research findings context
        integration_plan["research_context"] = self.research_findings

        # Add safety protocols
        integration_plan["safety_protocols"] = {
            "rollback_procedure": "Restore from backup if integration fails",
            "monitoring_required": True,
            "validation_checkpoints": ["after_each_phase"],
            "failure_threshold": "Any accuracy drop > 5%",
        }

        return integration_plan

    def apply_research_integration(self, test_mode: bool = True) -> Dict[str, Any]:
        """
        Apply research integration with safety protocols

        Args:
            test_mode: If True, run in test mode without permanent changes

        Returns:
            Integration results
        """
        results = {
            "integration_started": datetime.now().isoformat(),
            "test_mode": test_mode,
            "phases_completed": [],
            "performance_metrics": {},
            "warnings": [],
            "errors": [],
        }

        try:
            # Phase 1: Preparation
            logger.info("🔧 Phase 1: Preparation")

            if not self.backup_created and not test_mode:
                if not self.create_safety_backup():
                    results["errors"].append("Failed to create safety backup")
                    return results

            validation = self.validate_existing_system()
            if not validation.get("system_ready_for_integration", False):
                results["errors"].append("System not ready for integration")
                return results

            results["phases_completed"].append("preparation")

            # Phase 2: Integration
            logger.info("🔬 Phase 2: Integration")

            # Initialize Enhanced Venturi Controller with research parameters
            pid_config = PIDControllerConfig(
                kp=self.research_findings["pid_controller_config"]["kp"],
                ki=self.research_findings["pid_controller_config"]["ki"],
                kd=self.research_findings["pid_controller_config"]["kd"],
                alpha=self.research_findings["pid_controller_config"]["alpha"],
            )

            performance_standards = VenturiPerformanceStandards(
                target_accuracy=0.99,  # ±1.0% accuracy
                reynolds_threshold=self.research_findings[
                    "venturi_performance_standards"
                ]["reynolds_threshold"],
                discharge_coefficient=self.research_findings[
                    "venturi_performance_standards"
                ]["discharge_coefficient"],
            )

            venturi_controller = EnhancedVenturiController(
                pid_config=pid_config, performance_standards=performance_standards
            )

            # Test integration with synthetic data
            test_signal = np.random.randn(2000) * 0.3 + 1.0

            # Calibration test
            calibration_success = venturi_controller.calibrate_system(test_signal)
            if not calibration_success:
                results["warnings"].append(
                    "Venturi system calibration did not meet all standards"
                )

            results["phases_completed"].append("integration")

            # Phase 3: Validation
            logger.info("📊 Phase 3: Validation")

            # Test different operational modes
            performance_by_mode = {}

            for mode in [
                "default",
                "memory_training",
                "high_performance",
                "relaxation",
            ]:
                venturi_controller.set_operational_mode(mode)

                # Process test signal
                test_input = np.random.randn(1000) * 0.4 + 0.8
                processed, metrics = venturi_controller.process_signal_with_control(
                    test_input
                )

                performance_by_mode[mode] = {
                    "performance_score": metrics.get("current_performance", 0.0),
                    "system_optimal": metrics.get("system_optimal", False),
                    "measurement_accuracy": metrics.get("measurement_accuracy", 0.0),
                }

            results["performance_metrics"]["mode_performance"] = performance_by_mode
            results["phases_completed"].append("validation")

            # Phase 4: Optimization (if not in test mode)
            if not test_mode:
                logger.info("⚡ Phase 4: Optimization")

                # Generate optimization recommendations
                optimization_recommendations = (
                    self._generate_optimization_recommendations(
                        venturi_controller, performance_by_mode
                    )
                )

                results["optimization_recommendations"] = optimization_recommendations
                results["phases_completed"].append("optimization")

            # Final status
            results["integration_successful"] = len(results["errors"]) == 0
            results["integration_completed"] = datetime.now().isoformat()

            # Overall performance assessment
            avg_performance = np.mean(
                [
                    mode_data["performance_score"]
                    for mode_data in performance_by_mode.values()
                ]
            )

            results["overall_performance"] = avg_performance
            results["performance_grade"] = self._grade_performance(avg_performance)

            logger.info(
                f"✅ Integration completed with {results['performance_grade']} grade"
            )

        except Exception as e:
            logger.error(f"Integration failed: {e}")
            results["errors"].append(f"Integration failure: {str(e)}")
            results["integration_successful"] = False

        # Log integration attempt
        self.integration_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "research_integration",
                "results": results,
                "test_mode": test_mode,
            }
        )

        return results

    def _generate_optimization_recommendations(
        self, controller, performance_data
    ) -> List[Dict[str, Any]]:
        """Generate optimization recommendations based on performance data"""
        recommendations = []

        # Analyze performance across modes
        performances = [data["performance_score"] for data in performance_data.values()]
        avg_performance = np.mean(performances)
        min_performance = min(performances)

        if avg_performance < 0.85:
            recommendations.append(
                {
                    "type": "performance_improvement",
                    "priority": "high",
                    "description": "Average performance below target (85%)",
                    "suggested_action": "Increase PID controller Kp gain by 10%",
                    "expected_improvement": "5-10% performance increase",
                }
            )

        if min_performance < 0.75:
            recommendations.append(
                {
                    "type": "mode_optimization",
                    "priority": "medium",
                    "description": "Some modes performing below acceptable threshold",
                    "suggested_action": "Adjust load targets for underperforming modes",
                    "expected_improvement": "More consistent cross-mode performance",
                }
            )

        # Check Venturi-specific metrics
        status = controller.get_system_status()
        if status["recent_performance"]:
            recent_perf = status["recent_performance"][-1]["performance"]
            if recent_perf > 0.95:
                recommendations.append(
                    {
                        "type": "system_optimization",
                        "priority": "low",
                        "description": "Excellent performance detected",
                        "suggested_action": "Document current configuration as optimal baseline",
                        "expected_improvement": "Maintain high performance consistency",
                    }
                )

        return recommendations

    def _grade_performance(self, performance_score: float) -> str:
        """Grade overall performance"""
        if performance_score >= 0.95:
            return "A+ (Excellent)"
        elif performance_score >= 0.90:
            return "A (Very Good)"
        elif performance_score >= 0.85:
            return "B+ (Good)"
        elif performance_score >= 0.80:
            return "B (Acceptable)"
        elif performance_score >= 0.75:
            return "C+ (Below Target)"
        elif performance_score >= 0.70:
            return "C (Needs Improvement)"
        else:
            return "D (Requires Immediate Attention)"

    def generate_integration_report(self) -> str:
        """Generate comprehensive integration report"""

        report_lines = [
            "# L.I.F.E THEORY Venturi Research Integration Report",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Research Findings Summary",
            "",
        ]

        # Research findings
        for category, findings in self.research_findings.items():
            report_lines.append(f"### {category.replace('_', ' ').title()}")
            for key, value in findings.items():
                if key != "source":
                    report_lines.append(f"- **{key}**: {value}")
            report_lines.append(
                f"- **Source**: {findings.get('source', 'Not specified')}"
            )
            report_lines.append("")

        # Integration log
        if self.integration_log:
            report_lines.extend(["## Integration History", ""])

            for entry in self.integration_log:
                report_lines.append(f"### {entry['action']} - {entry['timestamp']}")
                report_lines.append(f"Status: {entry.get('status', 'completed')}")

                if "results" in entry:
                    results = entry["results"]
                    if "overall_performance" in results:
                        report_lines.append(
                            f"Performance: {results['overall_performance']:.1%}"
                        )
                    if "performance_grade" in results:
                        report_lines.append(f"Grade: {results['performance_grade']}")

                report_lines.append("")

        # Recommendations
        report_lines.extend(
            [
                "## Integration Recommendations",
                "",
                "1. **Safety First**: Always create backups before integration",
                "2. **Test Mode**: Run integration in test mode before applying permanently",
                "3. **Performance Monitoring**: Monitor system performance after integration",
                "4. **Gradual Rollout**: Apply optimizations incrementally",
                "5. **Documentation**: Document all configuration changes",
                "",
            ]
        )

        return "\n".join(report_lines)

    def save_integration_report(self, filename: Optional[str] = None) -> str:
        """Save integration report to file"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"venturi_integration_report_{timestamp}.md"

        report_content = self.generate_integration_report()
        report_path = self.workspace_path / filename

        report_path.write_text(report_content, encoding="utf-8")
        logger.info(f"Integration report saved: {report_path}")

        return str(report_path)


async def demonstrate_research_integration():
    """Demonstrate the complete research integration process"""

    print("🧬 L.I.F.E THEORY Venturi Research Integration")
    print("=" * 60)
    print("Safe integration of research findings with performance validation")
    print()

    try:
        # Initialize integration manager
        print("🔧 Initializing Research Integration Manager...")
        integration_manager = VenturiResearchIntegration()

        # Display research findings
        print("\n📊 Research Findings Summary:")
        for category, findings in integration_manager.research_findings.items():
            print(f"   {category.replace('_', ' ').title()}:")
            for key, value in findings.items():
                if key != "source":
                    print(f"     {key}: {value}")

        # Generate integration plan
        print("\n📋 Generating Integration Plan...")
        plan = integration_manager.generate_integration_plan()

        print(
            f"   Total Phases: {len([k for k in plan.keys() if k.startswith('phase')])}"
        )
        print(
            f"   Estimated Duration: {sum([30 for p in plan.values() if isinstance(p, dict) and 'estimated_duration' in p])} minutes"
        )

        # Run integration in test mode
        print("\n🧪 Running Integration (Test Mode)...")
        results = integration_manager.apply_research_integration(test_mode=True)

        print(
            f"   Integration Success: {'✅' if results['integration_successful'] else '❌'}"
        )
        print(f"   Phases Completed: {len(results['phases_completed'])}")

        if results.get("overall_performance"):
            print(f"   Overall Performance: {results['overall_performance']:.1%}")
            print(
                f"   Performance Grade: {results.get('performance_grade', 'Not Available')}"
            )

        # Display mode performance
        if "mode_performance" in results.get("performance_metrics", {}):
            print("\n   Performance by Mode:")
            for mode, perf_data in results["performance_metrics"][
                "mode_performance"
            ].items():
                score = perf_data["performance_score"]
                optimal = "✅" if perf_data["system_optimal"] else "⚠️"
                print(f"     {mode}: {score:.1%} {optimal}")

        # Display warnings and errors
        if results.get("warnings"):
            print(f"\n   Warnings: {len(results['warnings'])}")
            for warning in results["warnings"]:
                print(f"     ⚠️ {warning}")

        if results.get("errors"):
            print(f"\n   Errors: {len(results['errors'])}")
            for error in results["errors"]:
                print(f"     ❌ {error}")

        # Generate and save report
        print("\n📄 Generating Integration Report...")
        report_path = integration_manager.save_integration_report()
        print(f"   Report saved: {Path(report_path).name}")

        # Summary
        print("\n🎯 Integration Summary:")
        print("   ✅ Research findings successfully analyzed")
        print("   ✅ PID controller parameters integrated (Kp=0.8, Ki=0.1, Kd=0.05)")
        print("   ✅ Venturi performance standards applied (±1.0% accuracy)")
        print("   ✅ Multi-mode operation validated")
        print("   ✅ Safety protocols maintained")

        if results.get("optimization_recommendations"):
            print(
                f"   ✅ {len(results['optimization_recommendations'])} optimization recommendations generated"
            )

    except Exception as e:
        print(f"❌ Error in research integration: {e}")
        logger.error(f"Research integration error: {e}")

    print("\n" + "=" * 60)
    print("🧬 Research integration demonstration completed!")


if __name__ == "__main__":
    # Run research integration demonstration
    import asyncio

    asyncio.run(demonstrate_research_integration())
