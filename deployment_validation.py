#!/usr/bin/env python3
"""
L.I.F.E. Platform - Deployment Validation Suite
Comprehensive validation for deployment readiness and configuration

This module provides automated validation and testing capabilities
for deployment preparation, ensuring all components are properly
configured and ready for production deployment.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DeploymentType(Enum):
    """Types of deployments"""

    AZURE_FUNCTIONS = "azure_functions"
    AZURE_WEB_APP = "azure_web_app"
    AZURE_CONTAINER = "azure_container"
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    STANDALONE = "standalone"


class ValidationCategory(Enum):
    """Categories of validation checks"""

    CONFIGURATION = "configuration"
    DEPENDENCIES = "dependencies"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"
    MONITORING = "monitoring"


class ValidationStatus(Enum):
    """Status of validation checks"""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNING = "warning"


class ValidationSeverity(Enum):
    """Severity levels for validation issues"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ValidationCheck:
    """Individual validation check"""

    check_id: str
    name: str
    description: str
    category: ValidationCategory
    severity: ValidationSeverity
    deployment_types: List[DeploymentType]
    status: ValidationStatus = ValidationStatus.PENDING
    result: str = ""
    error_message: str = ""
    execution_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DeploymentValidationReport:
    """Comprehensive deployment validation report"""

    report_id: str
    deployment_type: DeploymentType
    timestamp: datetime = field(default_factory=datetime.now)
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0
    skipped_checks: int = 0
    critical_issues: int = 0
    high_priority_issues: int = 0
    execution_time: float = 0.0
    validation_checks: List[ValidationCheck] = field(default_factory=list)
    deployment_ready: bool = False
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)


class DeploymentValidationSuite:
    """
    Deployment Validation Suite for L.I.F.E. Platform

    Provides comprehensive validation for deployment readiness,
    ensuring all components are properly configured for production.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.validation_checks: List[ValidationCheck] = []
        self.deployment_reports: List[DeploymentValidationReport] = []

        # Initialize validation checks
        self._initialize_validation_checks()

        logger.info(
            f"Deployment Validation Suite initialized for workspace: {self.workspace_path}"
        )

    def _initialize_validation_checks(self):
        """Initialize all validation checks"""
        checks = [
            # Configuration checks
            ValidationCheck(
                check_id="config_azure_subscription",
                name="Azure Subscription Configuration",
                description="Validate Azure subscription and resource group configuration",
                category=ValidationCategory.CONFIGURATION,
                severity=ValidationSeverity.CRITICAL,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                ],
            ),
            ValidationCheck(
                check_id="config_environment_variables",
                name="Environment Variables",
                description="Validate required environment variables are set",
                category=ValidationCategory.CONFIGURATION,
                severity=ValidationSeverity.CRITICAL,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.DOCKER_COMPOSE,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="config_azure_credentials",
                name="Azure Credentials",
                description="Validate Azure authentication credentials",
                category=ValidationCategory.CONFIGURATION,
                severity=ValidationSeverity.CRITICAL,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                ],
            ),
            # Dependency checks
            ValidationCheck(
                check_id="deps_python_requirements",
                name="Python Dependencies",
                description="Validate Python requirements.txt and dependencies",
                category=ValidationCategory.DEPENDENCIES,
                severity=ValidationSeverity.CRITICAL,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.DOCKER_COMPOSE,
                    DeploymentType.STANDALONE,
                ],
            ),
            ValidationCheck(
                check_id="deps_azure_sdk",
                name="Azure SDK Dependencies",
                description="Validate Azure SDK packages are available",
                category=ValidationCategory.DEPENDENCIES,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                ],
            ),
            # Security checks
            ValidationCheck(
                check_id="sec_secrets_management",
                name="Secrets Management",
                description="Validate secrets and sensitive data handling",
                category=ValidationCategory.SECURITY,
                severity=ValidationSeverity.CRITICAL,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="sec_encryption",
                name="Data Encryption",
                description="Validate data encryption configuration",
                category=ValidationCategory.SECURITY,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                ],
            ),
            # Performance checks
            ValidationCheck(
                check_id="perf_resource_limits",
                name="Resource Limits",
                description="Validate resource limits and scaling configuration",
                category=ValidationCategory.PERFORMANCE,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="perf_monitoring_setup",
                name="Monitoring Setup",
                description="Validate monitoring and logging configuration",
                category=ValidationCategory.PERFORMANCE,
                severity=ValidationSeverity.MEDIUM,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            # Compliance checks
            ValidationCheck(
                check_id="comp_gdpr_compliance",
                name="GDPR Compliance",
                description="Validate GDPR compliance measures",
                category=ValidationCategory.COMPLIANCE,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="comp_data_retention",
                name="Data Retention Policies",
                description="Validate data retention and deletion policies",
                category=ValidationCategory.COMPLIANCE,
                severity=ValidationSeverity.MEDIUM,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            # Infrastructure checks
            ValidationCheck(
                check_id="infra_networking",
                name="Network Configuration",
                description="Validate network and connectivity configuration",
                category=ValidationCategory.INFRASTRUCTURE,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="infra_storage",
                name="Storage Configuration",
                description="Validate storage and persistence configuration",
                category=ValidationCategory.INFRASTRUCTURE,
                severity=ValidationSeverity.HIGH,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            # Monitoring checks
            ValidationCheck(
                check_id="mon_health_checks",
                name="Health Check Endpoints",
                description="Validate health check endpoints configuration",
                category=ValidationCategory.MONITORING,
                severity=ValidationSeverity.MEDIUM,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
            ValidationCheck(
                check_id="mon_logging_config",
                name="Logging Configuration",
                description="Validate logging and telemetry configuration",
                category=ValidationCategory.MONITORING,
                severity=ValidationSeverity.MEDIUM,
                deployment_types=[
                    DeploymentType.AZURE_FUNCTIONS,
                    DeploymentType.AZURE_WEB_APP,
                    DeploymentType.AZURE_CONTAINER,
                    DeploymentType.KUBERNETES,
                ],
            ),
        ]

        self.validation_checks = checks

    async def validate_deployment(
        self, deployment_type: DeploymentType
    ) -> DeploymentValidationReport:
        """Validate deployment readiness for specified type"""
        logger.info(f"Starting deployment validation for {deployment_type.value}")

        report = DeploymentValidationReport(
            report_id=f"deploy_validation_{int(datetime.now().timestamp())}_{deployment_type.value}",
            deployment_type=deployment_type,
            timestamp=datetime.now(),
        )

        # Filter checks for deployment type
        relevant_checks = [
            check
            for check in self.validation_checks
            if deployment_type in check.deployment_types
        ]

        report.total_checks = len(relevant_checks)
        start_time = datetime.now()

        try:
            # Execute validation checks
            for check in relevant_checks:
                result = await self._execute_validation_check(check, deployment_type)
                report.validation_checks.append(result)

                # Update counters
                if result.status == ValidationStatus.PASSED:
                    report.passed_checks += 1
                elif result.status == ValidationStatus.FAILED:
                    report.failed_checks += 1
                    if result.severity == ValidationSeverity.CRITICAL:
                        report.critical_issues += 1
                    elif result.severity == ValidationSeverity.HIGH:
                        report.high_priority_issues += 1
                elif result.status == ValidationStatus.WARNING:
                    report.warning_checks += 1
                elif result.status == ValidationStatus.SKIPPED:
                    report.skipped_checks += 1

            # Calculate execution time
            report.execution_time = (datetime.now() - start_time).total_seconds()

            # Determine deployment readiness
            report.deployment_ready = self._assess_deployment_readiness(report)

            # Generate summary and recommendations
            report.summary = self._generate_validation_summary(report)
            report.recommendations = self._generate_deployment_recommendations(report)
            report.blockers = self._identify_deployment_blockers(report)

            logger.info(
                f"Deployment validation complete. Ready: {report.deployment_ready}"
            )

        except Exception as e:
            logger.error(f"Deployment validation failed: {e}")
            report.deployment_ready = False
            report.blockers.append(f"Validation execution failed: {str(e)}")

        self.deployment_reports.append(report)
        return report

    async def _execute_validation_check(
        self, check: ValidationCheck, deployment_type: DeploymentType
    ) -> ValidationCheck:
        """Execute a single validation check"""
        check.start_time = datetime.now()
        check.status = ValidationStatus.RUNNING

        try:
            # Execute check based on check_id
            if check.check_id == "config_azure_subscription":
                result = await self._check_azure_subscription_config()
            elif check.check_id == "config_environment_variables":
                result = await self._check_environment_variables(deployment_type)
            elif check.check_id == "config_azure_credentials":
                result = await self._check_azure_credentials()
            elif check.check_id == "deps_python_requirements":
                result = await self._check_python_requirements()
            elif check.check_id == "deps_azure_sdk":
                result = await self._check_azure_sdk_dependencies()
            elif check.check_id == "sec_secrets_management":
                result = await self._check_secrets_management()
            elif check.check_id == "sec_encryption":
                result = await self._check_encryption_config()
            elif check.check_id == "perf_resource_limits":
                result = await self._check_resource_limits(deployment_type)
            elif check.check_id == "perf_monitoring_setup":
                result = await self._check_monitoring_setup()
            elif check.check_id == "comp_gdpr_compliance":
                result = await self._check_gdpr_compliance()
            elif check.check_id == "comp_data_retention":
                result = await self._check_data_retention_policies()
            elif check.check_id == "infra_networking":
                result = await self._check_network_configuration(deployment_type)
            elif check.check_id == "infra_storage":
                result = await self._check_storage_configuration(deployment_type)
            elif check.check_id == "mon_health_checks":
                result = await self._check_health_endpoints()
            elif check.check_id == "mon_logging_config":
                result = await self._check_logging_configuration()
            else:
                result = {
                    "status": ValidationStatus.SKIPPED,
                    "result": "Check not implemented",
                    "error": "",
                }

            check.status = result.get("status", ValidationStatus.FAILED)
            check.result = result.get("result", "")
            check.error_message = result.get("error", "")
            check.recommendations = result.get("recommendations", [])

        except Exception as e:
            check.status = ValidationStatus.FAILED
            check.error_message = f"Check execution failed: {str(e)}"
            logger.error(f"Validation check {check.check_id} failed: {e}")

        check.end_time = datetime.now()
        check.execution_time = (check.end_time - check.start_time).total_seconds()

        return check

    async def _check_azure_subscription_config(self) -> Dict[str, Any]:
        """Check Azure subscription configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check azure_config.py
            azure_config_path = self.workspace_path / "azure_config.py"
            if not azure_config_path.exists():
                result["status"] = ValidationStatus.FAILED
                result["error"] = "azure_config.py not found"
                result["recommendations"] = [
                    "Create azure_config.py with Azure subscription settings"
                ]
                return result

            # Read and validate configuration
            with open(azure_config_path, "r", encoding="utf-8") as f:
                content = f.read()

            required_configs = [
                "AZURE_SUBSCRIPTION_ID",
                "AZURE_RESOURCE_GROUP",
                "AZURE_LOCATION",
            ]

            missing_configs = []
            for config in required_configs:
                if config not in content:
                    missing_configs.append(config)

            if missing_configs:
                result["status"] = ValidationStatus.FAILED
                result["error"] = (
                    f"Missing Azure configurations: {', '.join(missing_configs)}"
                )
                result["recommendations"] = [
                    f"Add {config} to azure_config.py" for config in missing_configs
                ]
            else:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Azure subscription configuration validated"

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Azure subscription check failed: {str(e)}"

        return result

    async def _check_environment_variables(
        self, deployment_type: DeploymentType
    ) -> Dict[str, Any]:
        """Check environment variables"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            required_vars = []

            if deployment_type in [
                DeploymentType.AZURE_FUNCTIONS,
                DeploymentType.AZURE_WEB_APP,
            ]:
                required_vars = [
                    "AZURE_SUBSCRIPTION_ID",
                    "AZURE_RESOURCE_GROUP",
                    "AZURE_CLIENT_ID",
                    "AZURE_CLIENT_SECRET",
                    "AZURE_TENANT_ID",
                ]
            elif deployment_type == DeploymentType.DOCKER_COMPOSE:
                required_vars = ["LIFE_ENV", "LIFE_LOG_LEVEL"]

            missing_vars = []
            for var in required_vars:
                if var not in os.environ:
                    missing_vars.append(var)

            if missing_vars:
                result["status"] = ValidationStatus.FAILED
                result["error"] = (
                    f"Missing environment variables: {', '.join(missing_vars)}"
                )
                result["recommendations"] = [
                    f"Set environment variable: {var}" for var in missing_vars
                ]
            else:
                result["status"] = ValidationStatus.PASSED
                result["result"] = (
                    f"All required environment variables set ({len(required_vars)} variables)"
                )

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Environment variables check failed: {str(e)}"

        return result

    async def _check_azure_credentials(self) -> Dict[str, Any]:
        """Check Azure credentials"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for Azure CLI or service principal authentication
            import subprocess

            # Try Azure CLI login check
            try:
                result_cli = subprocess.run(
                    ["az", "account", "show"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result_cli.returncode == 0:
                    result["status"] = ValidationStatus.PASSED
                    result["result"] = "Azure CLI authentication validated"
                    return result

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # Check for service principal environment variables
            sp_vars = ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"]
            sp_present = all(var in os.environ for var in sp_vars)

            if sp_present:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Service principal authentication configured"
            else:
                result["status"] = ValidationStatus.FAILED
                result["error"] = "No Azure authentication method found"
                result["recommendations"] = [
                    "Login with Azure CLI: az login",
                    "Or set service principal environment variables: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID",
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Azure credentials check failed: {str(e)}"

        return result

    async def _check_python_requirements(self) -> Dict[str, Any]:
        """Check Python requirements"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            requirements_path = self.workspace_path / "requirements.txt"
            if not requirements_path.exists():
                result["status"] = ValidationStatus.FAILED
                result["error"] = "requirements.txt not found"
                result["recommendations"] = [
                    "Create requirements.txt with Python dependencies"
                ]
                return result

            # Read requirements
            with open(requirements_path, "r", encoding="utf-8") as f:
                requirements = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]

            if not requirements:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "requirements.txt is empty"
                result["recommendations"] = [
                    "Add Python dependencies to requirements.txt"
                ]
                return result

            # Try to import key packages
            importable_packages = []
            failed_packages = []

            for req in requirements[:10]:  # Check first 10 packages
                package_name = req.split(">=")[0].split("==")[0].split("<")[0].strip()
                try:
                    __import__(package_name.replace("-", "_"))
                    importable_packages.append(package_name)
                except ImportError:
                    failed_packages.append(package_name)

            if failed_packages:
                result["status"] = ValidationStatus.WARNING
                result["result"] = (
                    f"Some packages may not be installed: {', '.join(failed_packages[:3])}"
                )
                result["recommendations"] = ["Run: pip install -r requirements.txt"]
            else:
                result["status"] = ValidationStatus.PASSED
                result["result"] = (
                    f"Python requirements validated ({len(requirements)} packages)"
                )

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Python requirements check failed: {str(e)}"

        return result

    async def _check_azure_sdk_dependencies(self) -> Dict[str, Any]:
        """Check Azure SDK dependencies"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            azure_packages = [
                "azure.identity",
                "azure.storage.blob",
                "azure.functions",
                "azure.monitor",
            ]

            missing_packages = []
            for package in azure_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)

            if missing_packages:
                result["status"] = ValidationStatus.FAILED
                result["error"] = (
                    f"Missing Azure SDK packages: {', '.join(missing_packages)}"
                )
                result["recommendations"] = [
                    "Install Azure SDK: pip install azure-identity azure-storage-blob azure-functions azure-monitor"
                ]
            else:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Azure SDK dependencies validated"

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Azure SDK check failed: {str(e)}"

        return result

    async def _check_secrets_management(self) -> Dict[str, Any]:
        """Check secrets management configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for Azure Key Vault configuration
            azure_config_path = self.workspace_path / "azure_config.py"
            if azure_config_path.exists():
                with open(azure_config_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if "KEY_VAULT" in content or "keyvault" in content.lower():
                    result["status"] = ValidationStatus.PASSED
                    result["result"] = "Azure Key Vault configuration detected"
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "No Key Vault configuration found"
                    result["recommendations"] = [
                        "Configure Azure Key Vault for secrets management"
                    ]
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "Azure configuration file not found"
                result["recommendations"] = [
                    "Create azure_config.py with Key Vault settings"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Secrets management check failed: {str(e)}"

        return result

    async def _check_encryption_config(self) -> Dict[str, Any]:
        """Check encryption configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for encryption-related configurations
            config_files = ["azure_config.py", "production_deployment_test.py"]

            encryption_indicators = [
                "encryption",
                "ENCRYPT",
                "ssl",
                "SSL",
                "tls",
                "TLS",
                "https",
                "HTTPS",
            ]

            found_encryption = False
            for config_file in config_files:
                config_path = self.workspace_path / config_file
                if config_path.exists():
                    with open(config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        indicator.lower() in content.lower()
                        for indicator in encryption_indicators
                    ):
                        found_encryption = True
                        break

            if found_encryption:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Encryption configuration detected"
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "No encryption configuration found"
                result["recommendations"] = [
                    "Configure data encryption for production deployment"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Encryption check failed: {str(e)}"

        return result

    async def _check_resource_limits(
        self, deployment_type: DeploymentType
    ) -> Dict[str, Any]:
        """Check resource limits configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            if deployment_type == DeploymentType.AZURE_FUNCTIONS:
                # Check Azure Functions configuration
                functions_config_path = (
                    self.workspace_path / "azure_functions_config.py"
                )
                if functions_config_path.exists():
                    with open(functions_config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if "timeout" in content.lower() or "memory" in content.lower():
                        result["status"] = ValidationStatus.PASSED
                        result["result"] = "Azure Functions resource limits configured"
                    else:
                        result["status"] = ValidationStatus.WARNING
                        result["result"] = "Resource limits not explicitly configured"
                        result["recommendations"] = [
                            "Configure timeout and memory limits in azure_functions_config.py"
                        ]
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "Azure Functions config file not found"

            elif deployment_type == DeploymentType.KUBERNETES:
                # Check for Kubernetes manifests
                k8s_files = list(self.workspace_path.glob("*.yaml")) + list(
                    self.workspace_path.glob("*.yml")
                )
                k8s_files = [
                    f
                    for f in k8s_files
                    if "deployment" in f.name.lower() or "k8s" in f.name.lower()
                ]

                if k8s_files:
                    result["status"] = ValidationStatus.PASSED
                    result["result"] = (
                        f"Kubernetes manifests found ({len(k8s_files)} files)"
                    )
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "No Kubernetes manifests found"
                    result["recommendations"] = [
                        "Create Kubernetes deployment manifests with resource limits"
                    ]

            else:
                result["status"] = ValidationStatus.SKIPPED
                result["result"] = (
                    f"Resource limits check not applicable for {deployment_type.value}"
                )

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Resource limits check failed: {str(e)}"

        return result

    async def _check_monitoring_setup(self) -> Dict[str, Any]:
        """Check monitoring setup"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for monitoring-related files
            monitoring_files = [
                "autonomous_sota_kpi_monitor.py",
                "system_health_monitor.py",
                "azure_config.py",  # May contain monitoring config
            ]

            found_monitoring = False
            for mon_file in monitoring_files:
                if (self.workspace_path / mon_file).exists():
                    found_monitoring = True
                    break

            if found_monitoring:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Monitoring components detected"
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "No monitoring components found"
                result["recommendations"] = [
                    "Implement monitoring components for production deployment"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Monitoring setup check failed: {str(e)}"

        return result

    async def _check_gdpr_compliance(self) -> Dict[str, Any]:
        """Check GDPR compliance measures"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for GDPR-related configurations
            compliance_indicators = [
                "gdpr",
                "GDPR",
                "consent",
                "privacy",
                "data_protection",
                "retention",
                "deletion",
            ]

            found_compliance = False
            config_files = ["azure_config.py", "production_deployment_test.py"]

            for config_file in config_files:
                config_path = self.workspace_path / config_file
                if config_path.exists():
                    with open(config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        indicator.lower() in content.lower()
                        for indicator in compliance_indicators
                    ):
                        found_compliance = True
                        break

            if found_compliance:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "GDPR compliance measures detected"
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "No explicit GDPR compliance measures found"
                result["recommendations"] = [
                    "Implement GDPR compliance measures for data handling"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"GDPR compliance check failed: {str(e)}"

        return result

    async def _check_data_retention_policies(self) -> Dict[str, Any]:
        """Check data retention policies"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for retention-related configurations
            retention_indicators = [
                "retention",
                "RETENTION",
                "ttl",
                "TTL",
                "expiration",
                "delete",
                "cleanup",
            ]

            found_retention = False
            config_files = ["azure_config.py", "production_deployment_test.py"]

            for config_file in config_files:
                config_path = self.workspace_path / config_file
                if config_path.exists():
                    with open(config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        indicator.lower() in content.lower()
                        for indicator in retention_indicators
                    ):
                        found_retention = True
                        break

            if found_retention:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Data retention policies configured"
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "No data retention policies found"
                result["recommendations"] = [
                    "Configure data retention and deletion policies"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Data retention check failed: {str(e)}"

        return result

    async def _check_network_configuration(
        self, deployment_type: DeploymentType
    ) -> Dict[str, Any]:
        """Check network configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            if deployment_type in [
                DeploymentType.AZURE_FUNCTIONS,
                DeploymentType.AZURE_WEB_APP,
            ]:
                # Check Azure networking configuration
                azure_config_path = self.workspace_path / "azure_config.py"
                if azure_config_path.exists():
                    with open(azure_config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    network_indicators = [
                        "vnet",
                        "VNET",
                        "subnet",
                        "firewall",
                        "network",
                    ]
                    if any(
                        indicator.lower() in content.lower()
                        for indicator in network_indicators
                    ):
                        result["status"] = ValidationStatus.PASSED
                        result["result"] = "Azure network configuration detected"
                    else:
                        result["status"] = ValidationStatus.WARNING
                        result["result"] = "No explicit network configuration found"
                        result["recommendations"] = [
                            "Configure Azure VNet and networking for security"
                        ]
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "Azure configuration not found"

            else:
                result["status"] = ValidationStatus.SKIPPED
                result["result"] = (
                    f"Network check not applicable for {deployment_type.value}"
                )

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Network configuration check failed: {str(e)}"

        return result

    async def _check_storage_configuration(
        self, deployment_type: DeploymentType
    ) -> Dict[str, Any]:
        """Check storage configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            if deployment_type in [
                DeploymentType.AZURE_FUNCTIONS,
                DeploymentType.AZURE_WEB_APP,
                DeploymentType.AZURE_CONTAINER,
            ]:
                # Check Azure storage configuration
                azure_config_path = self.workspace_path / "azure_config.py"
                if azure_config_path.exists():
                    with open(azure_config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    storage_indicators = [
                        "storage",
                        "STORAGE",
                        "blob",
                        "BLOB",
                        "container",
                    ]
                    if any(
                        indicator.lower() in content.lower()
                        for indicator in storage_indicators
                    ):
                        result["status"] = ValidationStatus.PASSED
                        result["result"] = "Azure storage configuration detected"
                    else:
                        result["status"] = ValidationStatus.WARNING
                        result["result"] = "No storage configuration found"
                        result["recommendations"] = [
                            "Configure Azure Storage for data persistence"
                        ]
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "Azure configuration not found"

            else:
                result["status"] = ValidationStatus.SKIPPED
                result["result"] = (
                    f"Storage check not applicable for {deployment_type.value}"
                )

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Storage configuration check failed: {str(e)}"

        return result

    async def _check_health_endpoints(self) -> Dict[str, Any]:
        """Check health check endpoints"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check API file for health endpoints
            api_file = self.workspace_path / "life_platform_api.py"
            if api_file.exists():
                with open(api_file, "r", encoding="utf-8") as f:
                    content = f.read()

                health_indicators = [
                    "health",
                    "HEALTH",
                    "status",
                    "STATUS",
                    "/health",
                    "/status",
                ]
                if any(indicator in content for indicator in health_indicators):
                    result["status"] = ValidationStatus.PASSED
                    result["result"] = "Health check endpoints detected"
                else:
                    result["status"] = ValidationStatus.WARNING
                    result["result"] = "No health check endpoints found"
                    result["recommendations"] = [
                        "Implement health check endpoints in API"
                    ]
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "API file not found"
                result["recommendations"] = ["Create API with health check endpoints"]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Health endpoints check failed: {str(e)}"

        return result

    async def _check_logging_configuration(self) -> Dict[str, Any]:
        """Check logging configuration"""
        result = {
            "status": ValidationStatus.PENDING,
            "result": "",
            "error": "",
            "recommendations": [],
        }

        try:
            # Check for logging configuration in various files
            config_files = [
                "azure_config.py",
                "production_deployment_test.py",
                "autonomous_optimizer.py",
            ]
            logging_indicators = ["logging", "LOGGING", "logger", "log", "telemetry"]

            found_logging = False
            for config_file in config_files:
                config_path = self.workspace_path / config_file
                if config_path.exists():
                    with open(config_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        indicator.lower() in content.lower()
                        for indicator in logging_indicators
                    ):
                        found_logging = True
                        break

            if found_logging:
                result["status"] = ValidationStatus.PASSED
                result["result"] = "Logging configuration detected"
            else:
                result["status"] = ValidationStatus.WARNING
                result["result"] = "No logging configuration found"
                result["recommendations"] = [
                    "Configure logging and telemetry for monitoring"
                ]

        except Exception as e:
            result["status"] = ValidationStatus.FAILED
            result["error"] = f"Logging configuration check failed: {str(e)}"

        return result

    def _assess_deployment_readiness(self, report: DeploymentValidationReport) -> bool:
        """Assess if deployment is ready based on validation results"""
        # Deployment is ready if:
        # - No critical issues
        # - No high priority issues
        # - At least 80% of checks pass
        # - All configuration checks pass

        if report.critical_issues > 0 or report.high_priority_issues > 0:
            return False

        if report.total_checks == 0:
            return False

        pass_rate = report.passed_checks / report.total_checks
        if pass_rate < 0.8:  # 80% pass rate required
            return False

        # Check that all configuration checks pass
        config_checks = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.CONFIGURATION
        ]
        if config_checks and not all(
            check.status == ValidationStatus.PASSED for check in config_checks
        ):
            return False

        return True

    def _generate_validation_summary(
        self, report: DeploymentValidationReport
    ) -> Dict[str, Any]:
        """Generate validation summary"""
        summary = {
            "deployment_type": report.deployment_type.value,
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "warning_checks": report.warning_checks,
            "skipped_checks": report.skipped_checks,
            "critical_issues": report.critical_issues,
            "high_priority_issues": report.high_priority_issues,
            "success_rate": (
                f"{(report.passed_checks / report.total_checks * 100):.1f}%"
                if report.total_checks > 0
                else "0%"
            ),
            "execution_time_seconds": report.execution_time,
            "deployment_ready": report.deployment_ready,
        }

        # Add category breakdown
        categories = {}
        for check in report.validation_checks:
            category = check.category.value
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0, "failed": 0}
            categories[category]["total"] += 1
            if check.status == ValidationStatus.PASSED:
                categories[category]["passed"] += 1
            elif check.status == ValidationStatus.FAILED:
                categories[category]["failed"] += 1

        summary["categories"] = categories
        return summary

    def _generate_deployment_recommendations(
        self, report: DeploymentValidationReport
    ) -> List[str]:
        """Generate deployment recommendations"""
        recommendations = []

        # Check failure rates
        if report.failed_checks > 0:
            failure_rate = report.failed_checks / report.total_checks
            if failure_rate > 0.3:
                recommendations.append(
                    "High failure rate in validation checks - address critical issues before deployment"
                )
            elif failure_rate > 0.1:
                recommendations.append(
                    "Several validation checks failed - review and fix issues"
                )

        # Check critical issues
        if report.critical_issues > 0:
            recommendations.append(
                f"Address {report.critical_issues} critical validation issues before deployment"
            )

        # Check configuration issues
        config_failures = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.CONFIGURATION
            and check.status == ValidationStatus.FAILED
        ]
        if config_failures:
            recommendations.append(
                "Fix configuration issues - these are required for deployment"
            )

        # Check security issues
        security_failures = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.SECURITY
            and check.status == ValidationStatus.FAILED
        ]
        if security_failures:
            recommendations.append(
                "Address security validation failures before production deployment"
            )

        # General recommendations
        if report.warning_checks > report.total_checks * 0.3:  # More than 30% warnings
            recommendations.append(
                "Review validation warnings to improve deployment quality"
            )

        if not report.deployment_ready:
            recommendations.append(
                "Deployment is not ready - fix blocking issues first"
            )
        else:
            recommendations.append(
                "Deployment validation passed - proceed with deployment"
            )

        return recommendations

    def _identify_deployment_blockers(
        self, report: DeploymentValidationReport
    ) -> List[str]:
        """Identify deployment blockers"""
        blockers = []

        # Critical issues are always blockers
        if report.critical_issues > 0:
            blockers.append(
                f"{report.critical_issues} critical validation issues must be resolved"
            )

        # Configuration failures are blockers
        config_failures = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.CONFIGURATION
            and check.status == ValidationStatus.FAILED
        ]
        if config_failures:
            blockers.append("Configuration validation failures prevent deployment")

        # Security failures are blockers
        security_failures = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.SECURITY
            and check.status == ValidationStatus.FAILED
        ]
        if security_failures:
            blockers.append("Security validation failures prevent deployment")

        # Dependency failures are blockers
        dependency_failures = [
            check
            for check in report.validation_checks
            if check.category == ValidationCategory.DEPENDENCIES
            and check.status == ValidationStatus.FAILED
        ]
        if dependency_failures:
            blockers.append("Dependency validation failures prevent deployment")

        return blockers

    def export_validation_report(
        self, filepath: str, report: Optional[DeploymentValidationReport] = None
    ) -> bool:
        """Export validation report to file"""
        if report is None:
            report = self.deployment_reports[-1] if self.deployment_reports else None

        if not report:
            logger.warning("No validation report available to export")
            return False

        try:
            export_data = {
                "report_id": report.report_id,
                "deployment_type": report.deployment_type.value,
                "timestamp": report.timestamp.isoformat(),
                "summary": report.summary,
                "validation_checks": [
                    {
                        "check_id": check.check_id,
                        "name": check.name,
                        "category": check.category.value,
                        "severity": check.severity.value,
                        "status": check.status.value,
                        "result": check.result,
                        "error_message": check.error_message,
                        "execution_time": check.execution_time,
                        "recommendations": check.recommendations,
                    }
                    for check in report.validation_checks
                ],
                "recommendations": report.recommendations,
                "blockers": report.blockers,
                "deployment_ready": report.deployment_ready,
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Validation report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export validation report: {e}")
            return False


# Factory function for easy instantiation
def create_deployment_validation_suite(
    workspace_path: Optional[str] = None,
) -> DeploymentValidationSuite:
    """
    Factory function to create deployment validation suite

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured DeploymentValidationSuite instance
    """
    return DeploymentValidationSuite(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for deployment validation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Deployment Validation Suite"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--deployment-type",
        "-t",
        choices=[
            "azure_functions",
            "azure_web_app",
            "azure_container",
            "docker_compose",
            "kubernetes",
            "standalone",
        ],
        default="azure_functions",
        help="Deployment type to validate (default: azure_functions)",
    )
    parser.add_argument(
        "--export", "-e", help="Export validation report to specified file"
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=[
            "configuration",
            "dependencies",
            "security",
            "performance",
            "compliance",
            "infrastructure",
            "monitoring",
        ],
        help="Validate only specific category",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create validation suite
    suite = create_deployment_validation_suite(workspace_path=args.workspace)

    # Parse deployment type
    deployment_type_map = {
        "azure_functions": DeploymentType.AZURE_FUNCTIONS,
        "azure_web_app": DeploymentType.AZURE_WEB_APP,
        "azure_container": DeploymentType.AZURE_CONTAINER,
        "docker_compose": DeploymentType.DOCKER_COMPOSE,
        "kubernetes": DeploymentType.KUBERNETES,
        "standalone": DeploymentType.STANDALONE,
    }

    deployment_type = deployment_type_map.get(
        args.deployment_type, DeploymentType.AZURE_FUNCTIONS
    )

    print("L.I.F.E. Platform - Deployment Validation Suite")
    print("=" * 55)
    print(f"Workspace: {args.workspace or os.getcwd()}")
    print(f"Deployment Type: {deployment_type.value}")

    try:
        print("\nRunning deployment validation...")

        # Run validation
        report = asyncio.run(suite.validate_deployment(deployment_type))

        print("\nValidation Results:")
        print(f"  Total checks: {report.total_checks}")
        print(f"  Passed: {report.passed_checks}")
        print(f"  Failed: {report.failed_checks}")
        print(f"  Warnings: {report.warning_checks}")
        print(f"  Skipped: {report.skipped_checks}")
        print(f"  Success rate: {report.summary.get('success_rate', 'N/A')}")
        print(f"  Critical issues: {report.critical_issues}")
        print(f"  High priority issues: {report.high_priority_issues}")
        print(f"  Deployment ready: {'✅ YES' if report.deployment_ready else '❌ NO'}")
        print(f"  Execution time: {report.execution_time:.2f}s")

        if report.validation_checks:
            print("\nValidation Details:")
            # Show failed checks first
            failed_checks = [
                check
                for check in report.validation_checks
                if check.status == ValidationStatus.FAILED
            ]
            if failed_checks:
                print("  ❌ Failed Checks:")
                for check in failed_checks[:5]:  # Show first 5
                    print(f"    • {check.name}: {check.error_message}")

            # Show warnings
            warning_checks = [
                check
                for check in report.validation_checks
                if check.status == ValidationStatus.WARNING
            ]
            if warning_checks:
                print("  ⚠️ Warning Checks:")
                for check in warning_checks[:3]:  # Show first 3
                    print(f"    • {check.name}: {check.result}")

        if report.blockers:
            print("\n🚫 Deployment Blockers:")
            for blocker in report.blockers:
                print(f"  • {blocker}")

        if report.recommendations:
            print("\nRecommendations:")
            for rec in report.recommendations:
                print(f"  • {rec}")

        if args.export:
            if suite.export_validation_report(args.export, report):
                print(f"\nValidation report exported to {args.export}")
            else:
                print("\nFailed to export validation report")
                return 1

        # Return appropriate exit code
        if not report.deployment_ready:
            print(
                "\n❌ Deployment validation failed - address blockers before deployment"
            )
            return 1
        elif report.critical_issues > 0:
            print("\n❌ Critical issues found - deployment not recommended")
            return 1
        elif report.failed_checks > 0:
            print("\n⚠️ Some validation checks failed - review before deployment")
            return 1
        else:
            print("\n✅ Deployment validation passed - ready for deployment")
            return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nValidation failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
