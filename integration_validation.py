#!/usr/bin/env python3
"""
L.I.F.E. Platform - Integration Validation System
Comprehensive validation of system integrations and data flows

This module provides automated validation of all integration points
within the L.I.F.E. Platform, ensuring seamless data flow and
system interoperability.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Types of system integrations"""

    API = "api"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    NETWORK = "network"
    CLOUD_SERVICE = "cloud_service"
    EXTERNAL_SYSTEM = "external_system"


class ValidationStatus(Enum):
    """Validation result status"""

    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class IntegrationPoint:
    """Represents a system integration point"""

    def __init__(
        self,
        name: str,
        integration_type: IntegrationType,
        description: str,
        dependencies: Optional[List[str]] = None,
        config_required: bool = False,
        async_capable: bool = False,
    ):
        self.name = name
        self.integration_type = integration_type
        self.description = description
        self.dependencies = dependencies or []
        self.config_required = config_required
        self.async_capable = async_capable
        self.last_validated: Optional[datetime] = None
        self.validation_history: List[Dict[str, Any]] = []


@dataclass
class ValidationResult:
    """Result of an integration validation"""

    integration_name: str
    status: ValidationStatus
    message: str
    response_time: Optional[float] = None
    error_details: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class IntegrationValidator:
    """
    Comprehensive integration validation system for L.I.F.E. Platform

    Validates all integration points including APIs, databases, cloud services,
    and external systems to ensure operational integrity.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.integration_points: Dict[str, IntegrationPoint] = {}
        self.validation_results: List[ValidationResult] = []
        self._initialize_integration_points()

        logger.info(
            f"Integration Validator initialized for workspace: {self.workspace_path}"
        )

    def _initialize_integration_points(self):
        """Initialize all integration points for validation"""

        # Core algorithm integrations
        self.integration_points["core_algorithm"] = IntegrationPoint(
            name="core_algorithm",
            integration_type=IntegrationType.FILESYSTEM,
            description="Core L.I.F.E. learning algorithm file access",
            dependencies=["experimentP2L.py"],
            config_required=False,
            async_capable=True,
        )

        # Azure integrations
        self.integration_points["azure_functions"] = IntegrationPoint(
            name="azure_functions",
            integration_type=IntegrationType.CLOUD_SERVICE,
            description="Azure Functions serverless processing",
            dependencies=["azure_config.py", "azure_life_functions.py"],
            config_required=True,
            async_capable=True,
        )

        self.integration_points["azure_storage"] = IntegrationPoint(
            name="azure_storage",
            integration_type=IntegrationType.CLOUD_SERVICE,
            description="Azure Blob Storage for EEG data",
            dependencies=["azure_config.py"],
            config_required=True,
            async_capable=True,
        )

        self.integration_points["azure_monitor"] = IntegrationPoint(
            name="azure_monitor",
            integration_type=IntegrationType.CLOUD_SERVICE,
            description="Azure Monitor for system telemetry",
            dependencies=["azure_config.py"],
            config_required=True,
            async_capable=False,
        )

        # EEG processing integrations
        self.integration_points["eeg_processor"] = IntegrationPoint(
            name="eeg_processor",
            integration_type=IntegrationType.FILESYSTEM,
            description="Enhanced EEG signal processing",
            dependencies=["enhanced_eeg_processor.py", "numpy"],
            config_required=False,
            async_capable=True,
        )

        # Venturi system integrations
        self.integration_points["venturi_control"] = IntegrationPoint(
            name="venturi_control",
            integration_type=IntegrationType.FILESYSTEM,
            description="Venturi gate fluid dynamics processing",
            dependencies=["enhanced_venturi_control.py", "numpy"],
            config_required=False,
            async_capable=True,
        )

        # Machine learning integrations
        self.integration_points["accuracy_classifier"] = IntegrationPoint(
            name="accuracy_classifier",
            integration_type=IntegrationType.FILESYSTEM,
            description="Ensemble classification system",
            dependencies=["accuracy_ensemble_classifier.py", "numpy"],
            config_required=False,
            async_capable=True,
        )

        # Performance monitoring
        self.integration_points["performance_monitor"] = IntegrationPoint(
            name="performance_monitor",
            integration_type=IntegrationType.FILESYSTEM,
            description="Real-time performance monitoring",
            dependencies=["performance_monitor.py", "psutil"],
            config_required=False,
            async_capable=False,
        )

        # Configuration systems
        self.integration_points["kpi_config"] = IntegrationPoint(
            name="kpi_config",
            integration_type=IntegrationType.FILESYSTEM,
            description="KPI configuration and monitoring",
            dependencies=["kpi_config.py"],
            config_required=False,
            async_capable=False,
        )

        # External data sources
        self.integration_points["physionet_data"] = IntegrationPoint(
            name="physionet_data",
            integration_type=IntegrationType.EXTERNAL_SYSTEM,
            description="PhysioNet EEG dataset access",
            dependencies=["bci_data/"],
            config_required=False,
            async_capable=False,
        )

        # Network integrations
        self.integration_points["marketplace_api"] = IntegrationPoint(
            name="marketplace_api",
            integration_type=IntegrationType.NETWORK,
            description="Azure Marketplace API integration",
            dependencies=["azure_config.py"],
            config_required=True,
            async_capable=True,
        )

    async def validate_all_integrations(self) -> Dict[str, Any]:
        """
        Run comprehensive validation of all integration points

        Returns:
            Complete validation report with results and summary
        """
        start_time = datetime.now()
        self.validation_results = []

        logger.info("🚀 Starting comprehensive integration validation...")

        try:
            # Validate integrations (some async, some sync)
            await self._validate_async_integrations()
            self._validate_sync_integrations()

            # Generate summary report
            summary = self._generate_validation_summary()
            end_time = datetime.now()
            duration = end_time - start_time

            logger.info(
                f"✅ Validation completed in {duration.total_seconds():.2f} seconds"
            )
            logger.info(
                f"📊 Results: {summary['total_validations']} validations, "
                f"{summary['successful']} successful, {summary['failed']} failed"
            )

            return {
                "validation_metadata": {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "duration_seconds": duration.total_seconds(),
                    "workspace_path": str(self.workspace_path),
                    "validator_version": "1.0.0",
                },
                "summary": summary,
                "results": [
                    self._result_to_dict(result) for result in self.validation_results
                ],
                "recommendations": self._generate_recommendations(),
            }

        except Exception as e:
            logger.error(f"❌ Validation failed with error: {e}")
            return {
                "error": str(e),
                "validation_metadata": {
                    "start_time": start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "status": "failed",
                },
            }

    async def _validate_async_integrations(self):
        """Validate integrations that support async operations"""
        async_integrations = [
            name
            for name, integration in self.integration_points.items()
            if integration.async_capable
        ]

        logger.info(f"🔄 Validating {len(async_integrations)} async integrations...")

        # Create validation tasks
        tasks = []
        for integration_name in async_integrations:
            task = asyncio.create_task(
                self._validate_single_integration(integration_name)
            )
            tasks.append(task)

        # Execute all async validations concurrently
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _validate_sync_integrations(self):
        """Validate integrations that require synchronous operations"""
        sync_integrations = [
            name
            for name, integration in self.integration_points.items()
            if not integration.async_capable
        ]

        logger.info(f"🔄 Validating {len(sync_integrations)} sync integrations...")

        for integration_name in sync_integrations:
            self._validate_single_integration_sync(integration_name)

    async def _validate_single_integration(self, integration_name: str):
        """Validate a single integration point (async version)"""
        integration = self.integration_points.get(integration_name)
        if not integration:
            return

        start_time = time.time()
        try:
            if integration_name == "azure_functions":
                result = await self._validate_azure_functions()
            elif integration_name == "azure_storage":
                result = await self._validate_azure_storage()
            elif integration_name == "azure_monitor":
                result = await self._validate_azure_monitor()
            elif integration_name == "eeg_processor":
                result = await self._validate_eeg_processor()
            elif integration_name == "venturi_control":
                result = await self._validate_venturi_control()
            elif integration_name == "accuracy_classifier":
                result = await self._validate_accuracy_classifier()
            elif integration_name == "marketplace_api":
                result = await self._validate_marketplace_api()
            else:
                # Generic file-based validation
                result = await self._validate_file_integration(integration)

            response_time = time.time() - start_time
            result.response_time = response_time

        except Exception as e:
            result = ValidationResult(
                integration_name=integration_name,
                status=ValidationStatus.FAILURE,
                message=f"Validation failed: {str(e)}",
                error_details=str(e),
                response_time=time.time() - start_time,
            )

        self.validation_results.append(result)
        integration.last_validated = datetime.now()
        integration.validation_history.append(self._result_to_dict(result))

    def _validate_single_integration_sync(self, integration_name: str):
        """Validate a single integration point (sync version)"""
        integration = self.integration_points.get(integration_name)
        if not integration:
            return

        start_time = time.time()
        try:
            if integration_name == "performance_monitor":
                result = self._validate_performance_monitor()
            elif integration_name == "kpi_config":
                result = self._validate_kpi_config()
            elif integration_name == "physionet_data":
                result = self._validate_physionet_data()
            else:
                # Generic file-based validation
                result = self._validate_file_integration_sync(integration)

            response_time = time.time() - start_time
            result.response_time = response_time

        except Exception as e:
            result = ValidationResult(
                integration_name=integration_name,
                status=ValidationStatus.FAILURE,
                message=f"Validation failed: {str(e)}",
                error_details=str(e),
                response_time=time.time() - start_time,
            )

        self.validation_results.append(result)
        integration.last_validated = datetime.now()
        integration.validation_history.append(self._result_to_dict(result))

    async def _validate_file_integration(
        self, integration: IntegrationPoint
    ) -> ValidationResult:
        """Generic file-based integration validation"""
        # Check if required files exist
        missing_files = []
        for dependency in integration.dependencies:
            if dependency.endswith(".py"):
                file_path = self.workspace_path / dependency
                if not file_path.exists():
                    missing_files.append(dependency)

        if missing_files:
            return ValidationResult(
                integration_name=integration.name,
                status=ValidationStatus.FAILURE,
                message=f"Missing required files: {', '.join(missing_files)}",
                metadata={"missing_files": missing_files},
            )

        # Try to import Python modules
        import_errors = []
        for dependency in integration.dependencies:
            if dependency.endswith(".py") and not dependency.endswith("/"):
                module_name = dependency[:-3]  # Remove .py extension
                try:
                    __import__(module_name)
                except ImportError as e:
                    import_errors.append(f"{module_name}: {e}")

        if import_errors:
            return ValidationResult(
                integration_name=integration.name,
                status=ValidationStatus.WARNING,
                message=f"Import issues detected: {len(import_errors)} modules",
                metadata={"import_errors": import_errors},
            )

        return ValidationResult(
            integration_name=integration.name,
            status=ValidationStatus.SUCCESS,
            message="File integration validated successfully",
            metadata={"files_checked": len(integration.dependencies)},
        )

    def _validate_file_integration_sync(
        self, integration: IntegrationPoint
    ) -> ValidationResult:
        """Generic file-based integration validation (sync version)"""
        # Use asyncio to run the async version
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._validate_file_integration(integration))
        finally:
            loop.close()

    async def _validate_azure_functions(self) -> ValidationResult:
        """Validate Azure Functions integration"""
        try:
            # Check Azure config
            config_file = self.workspace_path / "azure_config.py"
            if not config_file.exists():
                return ValidationResult(
                    integration_name="azure_functions",
                    status=ValidationStatus.FAILURE,
                    message="Azure configuration file missing",
                )

            # Check functions file
            functions_file = self.workspace_path / "azure_life_functions.py"
            if not functions_file.exists():
                return ValidationResult(
                    integration_name="azure_functions",
                    status=ValidationStatus.FAILURE,
                    message="Azure Functions implementation missing",
                )

            # Basic syntax check
            try:
                with open(functions_file, "r") as f:
                    content = f.read()
                    compile(content, functions_file, "exec")
            except SyntaxError as e:
                return ValidationResult(
                    integration_name="azure_functions",
                    status=ValidationStatus.FAILURE,
                    message=f"Syntax error in Azure Functions: {e}",
                    error_details=str(e),
                )

            return ValidationResult(
                integration_name="azure_functions",
                status=ValidationStatus.SUCCESS,
                message="Azure Functions integration validated",
                metadata={"functions_file_size": functions_file.stat().st_size},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="azure_functions",
                status=ValidationStatus.FAILURE,
                message=f"Azure Functions validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_azure_storage(self) -> ValidationResult:
        """Validate Azure Storage integration"""
        try:
            # Check for Azure storage configuration
            config_file = self.workspace_path / "azure_config.py"
            if not config_file.exists():
                return ValidationResult(
                    integration_name="azure_storage",
                    status=ValidationStatus.FAILURE,
                    message="Azure configuration missing for storage",
                )

            # Check if storage-related imports are available
            try:
                import azure.storage.blob

                storage_available = True
            except ImportError:
                storage_available = False

            if not storage_available:
                return ValidationResult(
                    integration_name="azure_storage",
                    status=ValidationStatus.WARNING,
                    message="Azure Storage SDK not available",
                    metadata={"sdk_available": False},
                )

            return ValidationResult(
                integration_name="azure_storage",
                status=ValidationStatus.SUCCESS,
                message="Azure Storage integration ready",
                metadata={"sdk_available": True},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="azure_storage",
                status=ValidationStatus.FAILURE,
                message=f"Azure Storage validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_azure_monitor(self) -> ValidationResult:
        """Validate Azure Monitor integration"""
        try:
            # Check for monitoring configuration
            config_file = self.workspace_path / "azure_config.py"
            if not config_file.exists():
                return ValidationResult(
                    integration_name="azure_monitor",
                    status=ValidationStatus.WARNING,
                    message="Azure configuration missing for monitoring",
                )

            return ValidationResult(
                integration_name="azure_monitor",
                status=ValidationStatus.SUCCESS,
                message="Azure Monitor integration configured",
            )

        except Exception as e:
            return ValidationResult(
                integration_name="azure_monitor",
                status=ValidationStatus.FAILURE,
                message=f"Azure Monitor validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_eeg_processor(self) -> ValidationResult:
        """Validate EEG processor integration"""
        try:
            processor_file = self.workspace_path / "enhanced_eeg_processor.py"
            if not processor_file.exists():
                return ValidationResult(
                    integration_name="eeg_processor",
                    status=ValidationStatus.FAILURE,
                    message="EEG processor file missing",
                )

            # Check file size (should be substantial)
            file_size = processor_file.stat().st_size
            if file_size < 1000:
                return ValidationResult(
                    integration_name="eeg_processor",
                    status=ValidationStatus.WARNING,
                    message="EEG processor file seems too small",
                    metadata={"file_size": file_size},
                )

            return ValidationResult(
                integration_name="eeg_processor",
                status=ValidationStatus.SUCCESS,
                message="EEG processor integration validated",
                metadata={"file_size": file_size},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="eeg_processor",
                status=ValidationStatus.FAILURE,
                message=f"EEG processor validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_venturi_control(self) -> ValidationResult:
        """Validate Venturi control system integration"""
        try:
            venturi_file = self.workspace_path / "enhanced_venturi_control.py"
            if not venturi_file.exists():
                return ValidationResult(
                    integration_name="venturi_control",
                    status=ValidationStatus.FAILURE,
                    message="Venturi control file missing",
                )

            file_size = venturi_file.stat().st_size
            if file_size < 1000:
                return ValidationResult(
                    integration_name="venturi_control",
                    status=ValidationStatus.WARNING,
                    message="Venturi control file seems incomplete",
                    metadata={"file_size": file_size},
                )

            return ValidationResult(
                integration_name="venturi_control",
                status=ValidationStatus.SUCCESS,
                message="Venturi control integration validated",
                metadata={"file_size": file_size},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="venturi_control",
                status=ValidationStatus.FAILURE,
                message=f"Venturi control validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_accuracy_classifier(self) -> ValidationResult:
        """Validate accuracy classifier integration"""
        try:
            classifier_file = self.workspace_path / "accuracy_ensemble_classifier.py"
            if not classifier_file.exists():
                return ValidationResult(
                    integration_name="accuracy_classifier",
                    status=ValidationStatus.FAILURE,
                    message="Accuracy classifier file missing",
                )

            file_size = classifier_file.stat().st_size
            if file_size < 1000:
                return ValidationResult(
                    integration_name="accuracy_classifier",
                    status=ValidationStatus.WARNING,
                    message="Accuracy classifier seems incomplete",
                    metadata={"file_size": file_size},
                )

            return ValidationResult(
                integration_name="accuracy_classifier",
                status=ValidationStatus.SUCCESS,
                message="Accuracy classifier integration validated",
                metadata={"file_size": file_size},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="accuracy_classifier",
                status=ValidationStatus.FAILURE,
                message=f"Accuracy classifier validation failed: {e}",
                error_details=str(e),
            )

    async def _validate_marketplace_api(self) -> ValidationResult:
        """Validate Azure Marketplace API integration"""
        try:
            # Check for marketplace-related configuration
            config_file = self.workspace_path / "azure_config.py"
            if not config_file.exists():
                return ValidationResult(
                    integration_name="marketplace_api",
                    status=ValidationStatus.WARNING,
                    message="Marketplace configuration not found",
                )

            return ValidationResult(
                integration_name="marketplace_api",
                status=ValidationStatus.SUCCESS,
                message="Marketplace API integration configured",
            )

        except Exception as e:
            return ValidationResult(
                integration_name="marketplace_api",
                status=ValidationStatus.FAILURE,
                message=f"Marketplace API validation failed: {e}",
                error_details=str(e),
            )

    def _validate_performance_monitor(self) -> ValidationResult:
        """Validate performance monitor integration"""
        try:
            monitor_file = self.workspace_path / "performance_monitor.py"
            if not monitor_file.exists():
                return ValidationResult(
                    integration_name="performance_monitor",
                    status=ValidationStatus.FAILURE,
                    message="Performance monitor file missing",
                )

            return ValidationResult(
                integration_name="performance_monitor",
                status=ValidationStatus.SUCCESS,
                message="Performance monitor integration validated",
            )

        except Exception as e:
            return ValidationResult(
                integration_name="performance_monitor",
                status=ValidationStatus.FAILURE,
                message=f"Performance monitor validation failed: {e}",
                error_details=str(e),
            )

    def _validate_kpi_config(self) -> ValidationResult:
        """Validate KPI configuration integration"""
        try:
            kpi_file = self.workspace_path / "kpi_config.py"
            if not kpi_file.exists():
                return ValidationResult(
                    integration_name="kpi_config",
                    status=ValidationStatus.FAILURE,
                    message="KPI configuration file missing",
                )

            return ValidationResult(
                integration_name="kpi_config",
                status=ValidationStatus.SUCCESS,
                message="KPI configuration integration validated",
            )

        except Exception as e:
            return ValidationResult(
                integration_name="kpi_config",
                status=ValidationStatus.FAILURE,
                message=f"KPI config validation failed: {e}",
                error_details=str(e),
            )

    def _validate_physionet_data(self) -> ValidationResult:
        """Validate PhysioNet data access"""
        try:
            data_dir = self.workspace_path / "bci_data"
            if not data_dir.exists():
                return ValidationResult(
                    integration_name="physionet_data",
                    status=ValidationStatus.WARNING,
                    message="BCI data directory not found",
                    metadata={"data_directory_exists": False},
                )

            # Check for data files
            data_files = list(data_dir.glob("*"))
            if not data_files:
                return ValidationResult(
                    integration_name="physionet_data",
                    status=ValidationStatus.WARNING,
                    message="No data files found in BCI directory",
                    metadata={"data_files_count": 0},
                )

            return ValidationResult(
                integration_name="physionet_data",
                status=ValidationStatus.SUCCESS,
                message="PhysioNet data access validated",
                metadata={"data_files_count": len(data_files)},
            )

        except Exception as e:
            return ValidationResult(
                integration_name="physionet_data",
                status=ValidationStatus.FAILURE,
                message=f"PhysioNet data validation failed: {e}",
                error_details=str(e),
            )

    def _generate_validation_summary(self) -> Dict[str, Any]:
        """Generate validation summary statistics"""
        total_validations = len(self.validation_results)
        successful = sum(
            1 for r in self.validation_results if r.status == ValidationStatus.SUCCESS
        )
        failed = sum(
            1 for r in self.validation_results if r.status == ValidationStatus.FAILURE
        )
        warnings = sum(
            1 for r in self.validation_results if r.status == ValidationStatus.WARNING
        )
        skipped = sum(
            1 for r in self.validation_results if r.status == ValidationStatus.SKIPPED
        )

        # Calculate average response time
        response_times = [
            r.response_time
            for r in self.validation_results
            if r.response_time is not None
        ]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )

        # Overall health score (0-100)
        health_score = 0
        if total_validations > 0:
            success_rate = successful / total_validations
            health_score = success_rate * 100

            # Penalty for failures
            failure_penalty = (failed / total_validations) * 20
            health_score = max(0, health_score - failure_penalty)

        return {
            "total_validations": total_validations,
            "successful": successful,
            "failed": failed,
            "warnings": warnings,
            "skipped": skipped,
            "success_rate": (
                round(successful / total_validations * 100, 1)
                if total_validations > 0
                else 0
            ),
            "average_response_time": round(avg_response_time, 3),
            "health_score": round(health_score, 1),
            "overall_status": (
                "healthy"
                if health_score >= 80
                else "degraded" if health_score >= 60 else "critical"
            ),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations based on validation results"""
        recommendations = []

        failed_validations = [
            r for r in self.validation_results if r.status == ValidationStatus.FAILURE
        ]
        warning_validations = [
            r for r in self.validation_results if r.status == ValidationStatus.WARNING
        ]

        if failed_validations:
            recommendations.append("🚨 CRITICAL INTEGRATION ISSUES:")
            for failure in failed_validations[:5]:
                recommendations.append(
                    f"  • {failure.integration_name}: {failure.message}"
                )
                if failure.error_details:
                    recommendations.append(f"    → {failure.error_details}")

        if warning_validations:
            recommendations.append("\n⚠️ INTEGRATION WARNINGS:")
            for warning in warning_validations[:5]:
                recommendations.append(
                    f"  • {warning.integration_name}: {warning.message}"
                )

        recommendations.extend(
            [
                "\n📋 GENERAL RECOMMENDATIONS:",
                "  • Ensure all Azure credentials are properly configured",
                "  • Verify network connectivity for cloud services",
                "  • Check file permissions for data access",
                "  • Update dependencies to latest stable versions",
                "  • Monitor integration health in production",
                "  • Implement retry logic for transient failures",
            ]
        )

        return recommendations

    def _result_to_dict(self, result: ValidationResult) -> Dict[str, Any]:
        """Convert validation result to dictionary"""
        return {
            "integration_name": result.integration_name,
            "status": result.status.value,
            "message": result.message,
            "response_time": result.response_time,
            "error_details": result.error_details,
            "metadata": result.metadata,
            "timestamp": result.timestamp.isoformat(),
        }

    def export_validation_report(self, filepath: str) -> bool:
        """Export validation results to JSON file"""
        try:
            if not self.validation_results:
                logger.warning("No validation results to export")
                return False

            report = asyncio.run(self.validate_all_integrations())
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2, default=str)

            logger.info(f"✅ Validation report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export validation report: {e}")
            return False


# Factory function for easy instantiation
def create_integration_validator(workspace_path: Optional[str] = None):
    """
    Factory function to create an integration validator

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured IntegrationValidator instance
    """
    return IntegrationValidator(workspace_path)


# Command-line interface
def main():
    """Main CLI function for integration validation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Integration Validator"
    )
    parser.add_argument(
        "--workspace",
        "-w",
        default=None,
        help="Workspace directory path (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="integration_validation_report.json",
        help="Output file for validation report",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("🔗 L.I.F.E. Platform - Integration Validator")
    print("=" * 60)

    # Create validator
    validator = create_integration_validator(args.workspace)

    # Run validation
    print("🚀 Running comprehensive integration validation...")
    report = asyncio.run(validator.validate_all_integrations())

    if "error" in report:
        print(f"❌ Validation failed: {report['error']}")
        return 1

    # Display summary
    summary = report["summary"]
    print("\nVALIDATION SUMMARY:")
    print(f"  Total Validations: {summary['total_validations']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Success Rate: {summary['success_rate']}%")
    print(f"  Health Score: {summary['health_score']}/100")
    print(f"  Overall Status: {summary['overall_status'].upper()}")

    # Export report
    if validator.export_validation_report(args.output):
        print(f"\n💾 Report exported to: {args.output}")
    else:
        print("\n❌ Failed to export report")

    # Exit with appropriate code
    return 0 if summary["overall_status"] == "healthy" else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
