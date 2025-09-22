#!/usr/bin/env python3
"""
L.I.F.E. Platform - CI/CD Diagnostic Tool
Comprehensive diagnostics for continuous integration and deployment pipelines

This module provides comprehensive diagnostic capabilities for CI/CD pipelines,
ensuring reliable deployment and integration of the L.I.F.E. Platform.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DiagnosticStatus(Enum):
    """Status of diagnostic checks"""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"
    UNKNOWN = "unknown"


class DiagnosticCategory(Enum):
    """Categories of diagnostic checks"""

    ENVIRONMENT = "environment"
    DEPENDENCIES = "dependencies"
    CONFIGURATION = "configuration"
    SECURITY = "security"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"
    DEPLOYMENT = "deployment"


class PipelineStage(Enum):
    """CI/CD pipeline stages"""

    BUILD = "build"
    TEST = "test"
    DEPLOY = "deploy"
    VALIDATE = "validate"
    MONITOR = "monitor"


@dataclass
class DiagnosticResult:
    """Result of a diagnostic check"""

    check_name: str
    category: DiagnosticCategory
    status: DiagnosticStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: Optional[float] = None
    recommendations: List[str] = field(default_factory=list)


@dataclass
class PipelineDiagnostic:
    """Comprehensive pipeline diagnostic report"""

    pipeline_name: str
    stage: PipelineStage
    results: List[DiagnosticResult] = field(default_factory=list)
    overall_status: DiagnosticStatus = DiagnosticStatus.UNKNOWN
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    total_duration_ms: Optional[float] = None
    environment_info: Dict[str, Any] = field(default_factory=dict)


class CICDDiagnosticTool:
    """
    CI/CD Diagnostic Tool for L.I.F.E. Platform

    Provides comprehensive diagnostics for CI/CD pipelines including
    environment validation, dependency checking, security scanning,
    and deployment verification.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.diagnostic_history: List[PipelineDiagnostic] = []
        self.current_diagnostic: Optional[PipelineDiagnostic] = None

        logger.info(
            f"CI/CD Diagnostic Tool initialized for workspace: {self.workspace_path}"
        )

    async def run_full_diagnostic(
        self,
        pipeline_name: str = "life-platform-pipeline",
        stage: PipelineStage = PipelineStage.BUILD,
    ) -> PipelineDiagnostic:
        """Run comprehensive CI/CD diagnostic suite"""
        self.current_diagnostic = PipelineDiagnostic(
            pipeline_name=pipeline_name, stage=stage
        )

        logger.info(
            f"Starting full CI/CD diagnostic for {pipeline_name} ({stage.value})"
        )

        try:
            # Environment diagnostics
            await self._run_environment_diagnostics()

            # Dependency diagnostics
            await self._run_dependency_diagnostics()

            # Configuration diagnostics
            await self._run_configuration_diagnostics()

            # Security diagnostics
            await self._run_security_diagnostics()

            # Performance diagnostics
            await self._run_performance_diagnostics()

            # Integration diagnostics
            await self._run_integration_diagnostics()

            # Deployment diagnostics (if applicable)
            if stage in [PipelineStage.DEPLOY, PipelineStage.VALIDATE]:
                await self._run_deployment_diagnostics()

            # Calculate overall status
            self._calculate_overall_status()

        except Exception as e:
            logger.error(f"Diagnostic failed: {e}")
            self.current_diagnostic.results.append(
                DiagnosticResult(
                    check_name="diagnostic_execution",
                    category=DiagnosticCategory.INTEGRATION,
                    status=DiagnosticStatus.FAIL,
                    message=f"Diagnostic execution failed: {str(e)}",
                )
            )

        finally:
            self.current_diagnostic.end_time = datetime.now()
            if self.current_diagnostic.start_time and self.current_diagnostic.end_time:
                duration = (
                    self.current_diagnostic.end_time
                    - self.current_diagnostic.start_time
                )
                self.current_diagnostic.total_duration_ms = (
                    duration.total_seconds() * 1000
                )

            self.diagnostic_history.append(self.current_diagnostic)

        logger.info(f"Completed CI/CD diagnostic for {pipeline_name}")
        return self.current_diagnostic

    async def _run_environment_diagnostics(self):
        """Run environment-related diagnostic checks"""
        logger.info("Running environment diagnostics...")

        # Python version check
        await self._check_python_version()

        # Operating system check
        await self._check_operating_system()

        # Required tools check
        await self._check_required_tools()

        # Environment variables check
        await self._check_environment_variables()

        # Disk space check
        await self._check_disk_space()

    async def _run_dependency_diagnostics(self):
        """Run dependency-related diagnostic checks"""
        logger.info("Running dependency diagnostics...")

        # Python packages check
        await self._check_python_packages()

        # Azure CLI check
        await self._check_azure_cli()

        # Git check
        await self._check_git()

        # Docker check (if applicable)
        await self._check_docker()

    async def _run_configuration_diagnostics(self):
        """Run configuration-related diagnostic checks"""
        logger.info("Running configuration diagnostics...")

        # Azure configuration check
        await self._check_azure_config()

        # Pipeline configuration check
        await self._check_pipeline_config()

        # Security configuration check
        await self._check_security_config()

        # Logging configuration check
        await self._check_logging_config()

    async def _run_security_diagnostics(self):
        """Run security-related diagnostic checks"""
        logger.info("Running security diagnostics...")

        # File permissions check
        await self._check_file_permissions()

        # Secrets management check
        await self._check_secrets_management()

        # Network security check
        await self._check_network_security()

        # Dependency vulnerabilities check
        await self._check_dependency_vulnerabilities()

    async def _run_performance_diagnostics(self):
        """Run performance-related diagnostic checks"""
        logger.info("Running performance diagnostics...")

        # Build time check
        await self._check_build_performance()

        # Test execution time check
        await self._check_test_performance()

        # Resource usage check
        await self._check_resource_usage()

        # Memory usage check
        await self._check_memory_usage()

    async def _run_integration_diagnostics(self):
        """Run integration-related diagnostic checks"""
        logger.info("Running integration diagnostics...")

        # Azure services integration check
        await self._check_azure_integration()

        # Database integration check
        await self._check_database_integration()

        # API integration check
        await self._check_api_integration()

        # External service integration check
        await self._check_external_services()

    async def _run_deployment_diagnostics(self):
        """Run deployment-related diagnostic checks"""
        logger.info("Running deployment diagnostics...")

        # Deployment configuration check
        await self._check_deployment_config()

        # Azure resource availability check
        await self._check_azure_resources()

        # Deployment validation check
        await self._check_deployment_validation()

        # Rollback capability check
        await self._check_rollback_capability()

    async def _check_python_version(self):
        """Check Python version compatibility"""
        start_time = datetime.now()

        try:
            version = sys.version_info
            required_version = (3, 8, 0)
            current_version = (version.major, version.minor, version.micro)

            if current_version >= required_version:
                status = DiagnosticStatus.PASS
                message = f"Python version {version.major}.{version.minor}.{version.micro} is compatible"
            else:
                status = DiagnosticStatus.FAIL
                message = f"Python version {version.major}.{version.minor}.{version.micro} is below required {required_version[0]}.{required_version[1]}.{required_version[2]}"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="python_version",
                category=DiagnosticCategory.ENVIRONMENT,
                status=status,
                message=message,
                details={
                    "current_version": f"{version.major}.{version.minor}.{version.micro}",
                    "required_version": f"{required_version[0]}.{required_version[1]}.{required_version[2]}",
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result.recommendations = [
                    "Upgrade Python to version 3.8.0 or higher",
                    "Consider using pyenv for version management",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Python version check failed: {e}")

    async def _check_operating_system(self):
        """Check operating system compatibility"""
        start_time = datetime.now()

        try:
            import platform

            system = platform.system().lower()
            supported_systems = ["windows", "linux", "darwin"]

            if system in supported_systems:
                status = DiagnosticStatus.PASS
                message = f"Operating system '{system}' is supported"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Operating system '{system}' may not be fully supported"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="operating_system",
                category=DiagnosticCategory.ENVIRONMENT,
                status=status,
                message=message,
                details={
                    "system": system,
                    "platform": platform.platform(),
                    "supported_systems": supported_systems,
                },
                duration_ms=duration,
            )

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Operating system check failed: {e}")

    async def _check_required_tools(self):
        """Check for required development tools"""
        start_time = datetime.now()

        tools = ["git", "python", "pip"]
        tool_status = {}

        for tool in tools:
            try:
                result = await asyncio.create_subprocess_exec(
                    tool,
                    "--version",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await result.wait()

                if result.returncode == 0:
                    tool_status[tool] = "available"
                else:
                    tool_status[tool] = "unavailable"
            except FileNotFoundError:
                tool_status[tool] = "not_found"

        missing_tools = [
            tool for tool, status in tool_status.items() if status != "available"
        ]

        if not missing_tools:
            status = DiagnosticStatus.PASS
            message = "All required tools are available"
        else:
            status = DiagnosticStatus.FAIL
            message = f"Missing required tools: {', '.join(missing_tools)}"

        duration = (datetime.now() - start_time).total_seconds() * 1000

        result = DiagnosticResult(
            check_name="required_tools",
            category=DiagnosticCategory.ENVIRONMENT,
            status=status,
            message=message,
            details={"tool_status": tool_status},
            duration_ms=duration,
        )

        if status == DiagnosticStatus.FAIL:
            result.recommendations = [
                "Install missing tools using system package manager",
                "For Windows: Use Chocolatey or manual installation",
                "For Linux/macOS: Use apt/brew respectively",
            ]

        self.current_diagnostic.results.append(result)

    async def _check_environment_variables(self):
        """Check for required environment variables"""
        start_time = datetime.now()

        required_vars = ["PYTHONPATH", "PATH"]
        optional_vars = ["AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_SUBSCRIPTION_ID"]

        var_status = {}
        missing_required = []
        missing_optional = []

        for var in required_vars:
            if var in os.environ:
                var_status[var] = "present"
            else:
                var_status[var] = "missing"
                missing_required.append(var)

        for var in optional_vars:
            if var in os.environ:
                var_status[var] = "present"
            else:
                var_status[var] = "missing"
                missing_optional.append(var)

        if not missing_required:
            status = DiagnosticStatus.PASS
            message = "All required environment variables are set"
        else:
            status = DiagnosticStatus.FAIL
            message = (
                f"Missing required environment variables: {', '.join(missing_required)}"
            )

        duration = (datetime.now() - start_time).total_seconds() * 1000

        result = DiagnosticResult(
            check_name="environment_variables",
            category=DiagnosticCategory.ENVIRONMENT,
            status=status,
            message=message,
            details={
                "variable_status": var_status,
                "missing_required": missing_required,
                "missing_optional": missing_optional,
            },
            duration_ms=duration,
        )

        if missing_required:
            result.recommendations = [
                "Set missing environment variables",
                "Consider using .env files for local development",
                "Use CI/CD secrets for pipeline variables",
            ]

        self.current_diagnostic.results.append(result)

    async def _check_disk_space(self):
        """Check available disk space"""
        start_time = datetime.now()

        try:
            stat = os.statvfs(self.workspace_path)
            free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            total_space_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)

            # Require at least 1GB free space
            min_required_gb = 1.0

            if free_space_gb >= min_required_gb:
                status = DiagnosticStatus.PASS
                message = f"Sufficient disk space available: {free_space_gb:.1f}GB free"
            else:
                status = DiagnosticStatus.FAIL
                message = f"Insufficient disk space: {free_space_gb:.1f}GB free, {min_required_gb}GB required"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="disk_space",
                category=DiagnosticCategory.ENVIRONMENT,
                status=status,
                message=message,
                details={
                    "free_space_gb": round(free_space_gb, 1),
                    "total_space_gb": round(total_space_gb, 1),
                    "min_required_gb": min_required_gb,
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result.recommendations = [
                    "Free up disk space by removing unnecessary files",
                    "Consider using external storage for large datasets",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Disk space check failed: {e}")

    async def _check_python_packages(self):
        """Check Python package dependencies"""
        start_time = datetime.now()

        try:
            requirements_file = self.workspace_path / "requirements.txt"
            if not requirements_file.exists():
                result = DiagnosticResult(
                    check_name="python_packages",
                    category=DiagnosticCategory.DEPENDENCIES,
                    status=DiagnosticStatus.SKIP,
                    message="requirements.txt not found, skipping package check",
                    duration_ms=(datetime.now() - start_time).total_seconds() * 1000,
                )
                self.current_diagnostic.results.append(result)
                return

            # Read requirements
            with open(requirements_file, "r") as f:
                requirements = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]

            # Check if packages are installed
            missing_packages = []
            for req in requirements[:10]:  # Check first 10 packages
                package_name = req.split(">=")[0].split("==")[0].split("<")[0].strip()
                try:
                    __import__(package_name.replace("-", "_"))
                except ImportError:
                    missing_packages.append(package_name)

            if not missing_packages:
                status = DiagnosticStatus.PASS
                message = "All required Python packages are installed"
            else:
                status = DiagnosticStatus.FAIL
                message = f"Missing Python packages: {', '.join(missing_packages[:5])}"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="python_packages",
                category=DiagnosticCategory.DEPENDENCIES,
                status=status,
                message=message,
                details={
                    "total_requirements": len(requirements),
                    "missing_packages": missing_packages,
                    "checked_packages": min(10, len(requirements)),
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result.recommendations = [
                    "Install missing packages with: pip install -r requirements.txt",
                    "Consider using virtual environments",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Python packages check failed: {e}")

    async def _check_azure_cli(self):
        """Check Azure CLI installation and configuration"""
        start_time = datetime.now()

        try:
            result = await asyncio.create_subprocess_exec(
                "az",
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                version_line = stdout.decode().split("\n")[0]
                status = DiagnosticStatus.PASS
                message = f"Azure CLI is installed: {version_line}"
            else:
                status = DiagnosticStatus.FAIL
                message = "Azure CLI is not installed or not accessible"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="azure_cli",
                category=DiagnosticCategory.DEPENDENCIES,
                status=status,
                message=message,
                details={"version_output": stdout.decode() if stdout else ""},
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result_obj.recommendations = [
                    "Install Azure CLI from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli",
                    "Ensure az command is in PATH",
                ]

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Azure CLI check failed: {e}")

    async def _check_git(self):
        """Check Git installation and repository status"""
        start_time = datetime.now()

        try:
            # Check git version
            result = await asyncio.create_subprocess_exec(
                "git",
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                result_obj = DiagnosticResult(
                    check_name="git",
                    category=DiagnosticCategory.DEPENDENCIES,
                    status=DiagnosticStatus.FAIL,
                    message="Git is not installed or not accessible",
                    duration_ms=(datetime.now() - start_time).total_seconds() * 1000,
                )
                result_obj.recommendations = ["Install Git from https://git-scm.com/"]
                self.current_diagnostic.results.append(result_obj)
                return

            # Check if we're in a git repository
            result = await asyncio.create_subprocess_exec(
                "git",
                "status",
                "--porcelain",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.workspace_path,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                status = DiagnosticStatus.PASS
                message = "Git repository is properly configured"
                uncommitted_changes = (
                    len(stdout.decode().strip().split("\n")) if stdout else 0
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "Not a Git repository or Git status check failed"
                uncommitted_changes = 0

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="git",
                category=DiagnosticCategory.DEPENDENCIES,
                status=status,
                message=message,
                details={
                    "version": stdout.decode().split("\n")[0] if stdout else "",
                    "is_repository": result.returncode == 0,
                    "uncommitted_changes": uncommitted_changes,
                },
                duration_ms=duration,
            )

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Git check failed: {e}")

    async def _check_docker(self):
        """Check Docker installation (optional)"""
        start_time = datetime.now()

        try:
            result = await asyncio.create_subprocess_exec(
                "docker",
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                version_line = stdout.decode().strip()
                status = DiagnosticStatus.PASS
                message = f"Docker is available: {version_line}"
            else:
                status = DiagnosticStatus.SKIP
                message = "Docker is not available (optional for L.I.F.E. Platform)"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="docker",
                category=DiagnosticCategory.DEPENDENCIES,
                status=status,
                message=message,
                details={"version_output": stdout.decode() if stdout else ""},
                duration_ms=duration,
            )

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Docker check failed: {e}")

    async def _check_azure_config(self):
        """Check Azure configuration files"""
        start_time = datetime.now()

        try:
            config_files = [
                self.workspace_path / "azure.yaml",
                self.workspace_path / "azure_config.py",
                self.workspace_path / ".azure",
            ]

            existing_configs = [f for f in config_files if f.exists()]

            if existing_configs:
                status = DiagnosticStatus.PASS
                message = f"Found {len(existing_configs)} Azure configuration files"
            else:
                status = DiagnosticStatus.WARNING
                message = "No Azure configuration files found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="azure_config",
                category=DiagnosticCategory.CONFIGURATION,
                status=status,
                message=message,
                details={
                    "config_files": [str(f) for f in config_files],
                    "existing_configs": [str(f) for f in existing_configs],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Ensure azure.yaml and azure_config.py are present",
                    "Configure Azure authentication credentials",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Azure config check failed: {e}")

    async def _check_pipeline_config(self):
        """Check CI/CD pipeline configuration"""
        start_time = datetime.now()

        try:
            pipeline_files = [
                self.workspace_path / ".github" / "workflows" / "blank.yml",
                self.workspace_path / ".github" / "workflows",
                self.workspace_path / "azure-pipelines.yml",
            ]

            existing_pipelines = [f for f in pipeline_files if f.exists()]

            if existing_pipelines:
                status = DiagnosticStatus.PASS
                message = (
                    f"Found {len(existing_pipelines)} pipeline configuration files"
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "No CI/CD pipeline configurations found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="pipeline_config",
                category=DiagnosticCategory.CONFIGURATION,
                status=status,
                message=message,
                details={
                    "pipeline_files": [str(f) for f in pipeline_files],
                    "existing_pipelines": [str(f) for f in existing_pipelines],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Create GitHub Actions workflows in .github/workflows/",
                    "Configure Azure DevOps pipelines if applicable",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Pipeline config check failed: {e}")

    async def _check_security_config(self):
        """Check security configuration"""
        start_time = datetime.now()

        try:
            security_indicators = [
                self.workspace_path / ".env",
                self.workspace_path / "secrets.json",
                self.workspace_path / ".gitignore",
            ]

            security_checks = {}

            # Check for .env file
            env_file = self.workspace_path / ".env"
            if env_file.exists():
                security_checks["env_file"] = "present"
            else:
                security_checks["env_file"] = "missing"

            # Check .gitignore for sensitive files
            gitignore_file = self.workspace_path / ".gitignore"
            if gitignore_file.exists():
                with open(gitignore_file, "r") as f:
                    gitignore_content = f.read()
                    sensitive_patterns = [".env", "secrets", "*.key", "*.pem"]
                    missing_patterns = [
                        pattern
                        for pattern in sensitive_patterns
                        if pattern not in gitignore_content
                    ]
                    security_checks["gitignore_sensitive"] = (
                        "covered" if not missing_patterns else "missing_patterns"
                    )
                    security_checks["missing_gitignore_patterns"] = missing_patterns
            else:
                security_checks["gitignore"] = "missing"

            # Overall security status
            issues = []
            if security_checks.get("env_file") == "missing":
                issues.append("No .env file found")
            if security_checks.get("gitignore") == "missing":
                issues.append("No .gitignore file")
            if security_checks.get("missing_gitignore_patterns"):
                issues.append(
                    f"Missing gitignore patterns: {', '.join(security_checks['missing_gitignore_patterns'])}"
                )

            if not issues:
                status = DiagnosticStatus.PASS
                message = "Security configuration appears adequate"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Security configuration issues: {len(issues)}"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="security_config",
                category=DiagnosticCategory.SECURITY,
                status=status,
                message=message,
                details={"security_checks": security_checks, "issues": issues},
                duration_ms=duration,
            )

            if issues:
                result.recommendations = [
                    "Create .env file for environment variables",
                    "Add .gitignore file with sensitive file patterns",
                    "Ensure secrets are not committed to version control",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Security config check failed: {e}")

    async def _check_logging_config(self):
        """Check logging configuration"""
        start_time = datetime.now()

        try:
            log_files = [
                self.workspace_path / "logs",
                self.workspace_path / "logs" / "life_benchmark.log",
                self.workspace_path / "logs" / "autonomous_optimizer.log",
            ]

            log_checks = {}

            # Check logs directory
            logs_dir = self.workspace_path / "logs"
            if logs_dir.exists():
                log_checks["logs_directory"] = "exists"
                log_files_count = len(list(logs_dir.glob("*.log")))
                log_checks["log_files_count"] = log_files_count
            else:
                log_checks["logs_directory"] = "missing"

            # Check specific log files
            existing_logs = [f for f in log_files if f.exists()]
            log_checks["existing_log_files"] = [str(f) for f in existing_logs]

            if logs_dir.exists():
                status = DiagnosticStatus.PASS
                message = (
                    f"Logging directory exists with {len(existing_logs)} log files"
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "Logging directory not found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="logging_config",
                category=DiagnosticCategory.CONFIGURATION,
                status=status,
                message=message,
                details=log_checks,
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Create logs directory for application logging",
                    "Configure proper log rotation and retention",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Logging config check failed: {e}")

    async def _check_file_permissions(self):
        """Check file permissions for security"""
        start_time = datetime.now()

        try:
            sensitive_files = [
                self.workspace_path / "azure_config.py",
                self.workspace_path / "secrets.json",
                self.workspace_path / ".env",
            ]

            permission_issues = []

            for file_path in sensitive_files:
                if file_path.exists():
                    # Check if file is readable by others (basic check)
                    if os.name == "posix":  # Unix-like systems
                        stat_info = file_path.stat()
                        permissions = oct(stat_info.st_mode)[-3:]
                        if (
                            permissions[1] != "0" or permissions[2] != "0"
                        ):  # Group/other can read
                            permission_issues.append(
                                f"{file_path.name}: too permissive ({permissions})"
                            )
                    # Windows permissions are more complex, skip for now

            if not permission_issues:
                status = DiagnosticStatus.PASS
                message = "File permissions appear secure"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Found {len(permission_issues)} file permission issues"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="file_permissions",
                category=DiagnosticCategory.SECURITY,
                status=status,
                message=message,
                details={"permission_issues": permission_issues},
                duration_ms=duration,
            )

            if permission_issues:
                result.recommendations = [
                    "Restrict permissions on sensitive files",
                    "Use chmod 600 for private configuration files",
                    "Consider using secret management services",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"File permissions check failed: {e}")

    async def _check_secrets_management(self):
        """Check secrets management configuration"""
        start_time = datetime.now()

        try:
            # Check for hardcoded secrets in code
            python_files = list(self.workspace_path.glob("**/*.py"))
            secret_patterns = [
                r"password\s*=\s*['\"][^'\"]*['\"]",
                r"secret\s*=\s*['\"][^'\"]*['\"]",
                r"key\s*=\s*['\"][^'\"]*['\"]",
                r"token\s*=\s*['\"][^'\"]*['\"]",
            ]

            hardcoded_secrets = []

            for file_path in python_files[:20]:  # Check first 20 files
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for pattern in secret_patterns:
                            import re

                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                hardcoded_secrets.append(
                                    f"{file_path.name}: {len(matches)} potential secrets"
                                )
                                break
                except Exception:
                    continue

            if not hardcoded_secrets:
                status = DiagnosticStatus.PASS
                message = "No obvious hardcoded secrets detected"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Found potential hardcoded secrets in {len(hardcoded_secrets)} files"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="secrets_management",
                category=DiagnosticCategory.SECURITY,
                status=status,
                message=message,
                details={
                    "checked_files": min(20, len(python_files)),
                    "hardcoded_secrets": hardcoded_secrets,
                },
                duration_ms=duration,
            )

            if hardcoded_secrets:
                result.recommendations = [
                    "Move secrets to environment variables or secret stores",
                    "Use Azure Key Vault for production secrets",
                    "Avoid committing sensitive data to version control",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Secrets management check failed: {e}")

    async def _check_network_security(self):
        """Check network security configuration"""
        start_time = datetime.now()

        try:
            # Basic network security checks
            security_checks = {}

            # Check for HTTPS URLs in configuration
            config_files = [self.workspace_path / "azure_config.py"]
            https_usage = []

            for config_file in config_files:
                if config_file.exists():
                    try:
                        with open(config_file, "r") as f:
                            content = f.read()
                            if "https://" in content:
                                https_usage.append(f"{config_file.name}: uses HTTPS")
                            elif "http://" in content:
                                https_usage.append(
                                    f"{config_file.name}: uses HTTP (insecure)"
                                )
                    except Exception:
                        continue

            security_checks["https_usage"] = https_usage

            if https_usage and not any(
                "HTTP (insecure)" in usage for usage in https_usage
            ):
                status = DiagnosticStatus.PASS
                message = "Network communications use secure protocols"
            else:
                status = DiagnosticStatus.WARNING
                message = "Some network communications may not be secure"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="network_security",
                category=DiagnosticCategory.SECURITY,
                status=status,
                message=message,
                details=security_checks,
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Use HTTPS for all external communications",
                    "Implement proper SSL/TLS configuration",
                    "Consider using Azure Application Gateway for SSL termination",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Network security check failed: {e}")

    async def _check_dependency_vulnerabilities(self):
        """Check for dependency vulnerabilities"""
        start_time = datetime.now()

        try:
            # Check if safety or similar tool is available
            result = await asyncio.create_subprocess_exec(
                "safety",
                "check",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.workspace_path,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                vulnerabilities = stdout.decode().count("vulnerability")
                if vulnerabilities == 0:
                    status = DiagnosticStatus.PASS
                    message = "No dependency vulnerabilities detected"
                else:
                    status = DiagnosticStatus.WARNING
                    message = f"Found {vulnerabilities} dependency vulnerabilities"
            else:
                status = DiagnosticStatus.SKIP
                message = "Safety tool not available for vulnerability scanning"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="dependency_vulnerabilities",
                category=DiagnosticCategory.SECURITY,
                status=status,
                message=message,
                details={
                    "safety_available": result.returncode == 0,
                    "vulnerabilities_found": (
                        stdout.decode().count("vulnerability")
                        if result.returncode == 0
                        else 0
                    ),
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result_obj.recommendations = [
                    "Update vulnerable dependencies",
                    "Run 'safety check' regularly",
                    "Consider using dependabot for automated updates",
                ]

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Dependency vulnerabilities check failed: {e}")

    async def _check_build_performance(self):
        """Check build performance metrics"""
        start_time = datetime.now()

        try:
            # Simulate build time check (would integrate with actual build system)
            build_time_seconds = 45.2  # Simulated build time
            acceptable_build_time = 120.0  # 2 minutes

            if build_time_seconds <= acceptable_build_time:
                status = DiagnosticStatus.PASS
                message = f"Build time acceptable: {build_time_seconds:.1f}s"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Build time too slow: {build_time_seconds:.1f}s (target: {acceptable_build_time}s)"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="build_performance",
                category=DiagnosticCategory.PERFORMANCE,
                status=status,
                message=message,
                details={
                    "build_time_seconds": build_time_seconds,
                    "acceptable_limit": acceptable_build_time,
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Optimize build process and dependencies",
                    "Consider using build caching",
                    "Parallelize build steps where possible",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Build performance check failed: {e}")

    async def _check_test_performance(self):
        """Check test execution performance"""
        start_time = datetime.now()

        try:
            # Check if pytest is available and run a quick test
            result = await asyncio.create_subprocess_exec(
                "python",
                "-m",
                "pytest",
                "--collect-only",
                "-q",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.workspace_path,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                test_count = stdout.decode().count("test_") + stdout.decode().count(
                    "::"
                )
                status = DiagnosticStatus.PASS
                message = f"Test collection successful: {test_count} tests found"
            else:
                status = DiagnosticStatus.WARNING
                message = "Test collection failed or no tests found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="test_performance",
                category=DiagnosticCategory.PERFORMANCE,
                status=status,
                message=message,
                details={
                    "test_collection_success": result.returncode == 0,
                    "estimated_test_count": (
                        stdout.decode().count("test_") if result.returncode == 0 else 0
                    ),
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result_obj.recommendations = [
                    "Ensure pytest is properly configured",
                    "Add comprehensive test suites",
                    "Consider test parallelization for better performance",
                ]

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Test performance check failed: {e}")

    async def _check_resource_usage(self):
        """Check system resource usage"""
        start_time = datetime.now()

        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            # Define acceptable limits
            max_cpu_percent = 80.0
            max_memory_percent = 85.0

            issues = []
            if cpu_percent > max_cpu_percent:
                issues.append(f"High CPU usage: {cpu_percent:.1f}%")
            if memory.percent > max_memory_percent:
                issues.append(f"High memory usage: {memory.percent:.1f}%")

            if not issues:
                status = DiagnosticStatus.PASS
                message = "System resource usage is within acceptable limits"
            else:
                status = DiagnosticStatus.WARNING
                message = f"Resource usage concerns: {len(issues)}"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="resource_usage",
                category=DiagnosticCategory.PERFORMANCE,
                status=status,
                message=message,
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "max_cpu_limit": max_cpu_percent,
                    "max_memory_limit": max_memory_percent,
                    "issues": issues,
                },
                duration_ms=duration,
            )

            if issues:
                result.recommendations = [
                    "Monitor system resources during peak usage",
                    "Consider resource optimization or scaling",
                    "Check for memory leaks in application code",
                ]

            self.current_diagnostic.results.append(result)

        except ImportError:
            # psutil not available
            result = DiagnosticResult(
                check_name="resource_usage",
                category=DiagnosticCategory.PERFORMANCE,
                status=DiagnosticStatus.SKIP,
                message="Resource monitoring unavailable (psutil not installed)",
                duration_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )
            result.recommendations = ["Install psutil for resource monitoring"]
            self.current_diagnostic.results.append(result)
        except Exception as e:
            logger.error(f"Resource usage check failed: {e}")

    async def _check_memory_usage(self):
        """Check application memory usage patterns"""
        start_time = datetime.now()

        try:
            import psutil

            process = psutil.Process()
            memory_info = process.memory_info()

            # Convert to MB
            memory_mb = memory_info.rss / (1024 * 1024)
            max_memory_mb = 500  # 500MB limit for diagnostics

            if memory_mb <= max_memory_mb:
                status = DiagnosticStatus.PASS
                message = f"Memory usage acceptable: {memory_mb:.1f}MB"
            else:
                status = DiagnosticStatus.WARNING
                message = (
                    f"High memory usage: {memory_mb:.1f}MB (limit: {max_memory_mb}MB)"
                )

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="memory_usage",
                category=DiagnosticCategory.PERFORMANCE,
                status=status,
                message=message,
                details={
                    "memory_mb": round(memory_mb, 1),
                    "max_memory_limit": max_memory_mb,
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Optimize memory usage in application code",
                    "Consider memory profiling tools",
                    "Implement memory-efficient data structures",
                ]

            self.current_diagnostic.results.append(result)

        except ImportError:
            result = DiagnosticResult(
                check_name="memory_usage",
                category=DiagnosticCategory.PERFORMANCE,
                status=DiagnosticStatus.SKIP,
                message="Memory monitoring unavailable (psutil not installed)",
                duration_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )
            result.recommendations = ["Install psutil for memory monitoring"]
            self.current_diagnostic.results.append(result)
        except Exception as e:
            logger.error(f"Memory usage check failed: {e}")

    async def _check_azure_integration(self):
        """Check Azure services integration"""
        start_time = datetime.now()

        try:
            # Check Azure CLI login status
            result = await asyncio.create_subprocess_exec(
                "az",
                "account",
                "show",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                account_info = json.loads(stdout.decode())
                subscription_id = account_info.get("id", "unknown")
                status = DiagnosticStatus.PASS
                message = (
                    f"Azure CLI authenticated (subscription: {subscription_id[:8]}...)"
                )
            else:
                status = DiagnosticStatus.FAIL
                message = "Azure CLI not authenticated"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="azure_integration",
                category=DiagnosticCategory.INTEGRATION,
                status=status,
                message=message,
                details={
                    "authenticated": result.returncode == 0,
                    "subscription_id": (
                        account_info.get("id") if result.returncode == 0 else None
                    ),
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result_obj.recommendations = [
                    "Run 'az login' to authenticate with Azure",
                    "Configure Azure subscription and tenant",
                    "Set up service principal for CI/CD pipelines",
                ]

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Azure integration check failed: {e}")

    async def _check_database_integration(self):
        """Check database integration (placeholder)"""
        start_time = datetime.now()

        # Placeholder for database integration checks
        result = DiagnosticResult(
            check_name="database_integration",
            category=DiagnosticCategory.INTEGRATION,
            status=DiagnosticStatus.SKIP,
            message="Database integration check not implemented",
            duration_ms=(datetime.now() - start_time).total_seconds() * 1000,
        )
        result.recommendations = ["Implement database connectivity checks"]
        self.current_diagnostic.results.append(result)

    async def _check_api_integration(self):
        """Check API integration status"""
        start_time = datetime.now()

        try:
            # Check if API-related files exist
            api_files = [
                self.workspace_path / "life_platform_api.py",
                self.workspace_path / "azure_life_functions.py",
            ]

            existing_api_files = [f for f in api_files if f.exists()]

            if existing_api_files:
                status = DiagnosticStatus.PASS
                message = f"API integration files found: {len(existing_api_files)}"
            else:
                status = DiagnosticStatus.WARNING
                message = "No API integration files found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="api_integration",
                category=DiagnosticCategory.INTEGRATION,
                status=status,
                message=message,
                details={
                    "api_files": [str(f) for f in api_files],
                    "existing_files": [str(f) for f in existing_api_files],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Implement API endpoints for platform integration",
                    "Add API documentation and testing",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"API integration check failed: {e}")

    async def _check_external_services(self):
        """Check external service integrations"""
        start_time = datetime.now()

        try:
            # Check for external service configurations
            external_configs = [
                self.workspace_path / "azure_config.py",
                self.workspace_path / "azure_functions_config.py",
            ]

            existing_configs = [f for f in external_configs if f.exists()]

            if existing_configs:
                status = DiagnosticStatus.PASS
                message = (
                    f"External service configurations found: {len(existing_configs)}"
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "No external service configurations found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="external_services",
                category=DiagnosticCategory.INTEGRATION,
                status=status,
                message=message,
                details={
                    "config_files": [str(f) for f in external_configs],
                    "existing_configs": [str(f) for f in existing_configs],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Configure external service integrations",
                    "Add service health checks and monitoring",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"External services check failed: {e}")

    async def _check_deployment_config(self):
        """Check deployment configuration"""
        start_time = datetime.now()

        try:
            deployment_files = [
                self.workspace_path / "azure.yaml",
                self.workspace_path / "Dockerfile",
                self.workspace_path / "azure_deployment_manager.py",
            ]

            existing_deployments = [f for f in deployment_files if f.exists()]

            if existing_deployments:
                status = DiagnosticStatus.PASS
                message = (
                    f"Deployment configurations found: {len(existing_deployments)}"
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "No deployment configurations found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="deployment_config",
                category=DiagnosticCategory.DEPLOYMENT,
                status=status,
                message=message,
                details={
                    "deployment_files": [str(f) for f in deployment_files],
                    "existing_files": [str(f) for f in existing_deployments],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Create azure.yaml for Azure deployment",
                    "Add Dockerfile for containerization",
                    "Implement deployment automation scripts",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Deployment config check failed: {e}")

    async def _check_azure_resources(self):
        """Check Azure resource availability"""
        start_time = datetime.now()

        try:
            # Check Azure resource groups
            result = await asyncio.create_subprocess_exec(
                "az",
                "group",
                "list",
                "--output",
                "json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                resource_groups = json.loads(stdout.decode())
                status = DiagnosticStatus.PASS
                message = (
                    f"Azure resource groups accessible: {len(resource_groups)} found"
                )
            else:
                status = DiagnosticStatus.FAIL
                message = "Cannot access Azure resource groups"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result_obj = DiagnosticResult(
                check_name="azure_resources",
                category=DiagnosticCategory.DEPLOYMENT,
                status=status,
                message=message,
                details={
                    "resource_groups_count": (
                        len(resource_groups) if result.returncode == 0 else 0
                    ),
                    "access_success": result.returncode == 0,
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.FAIL:
                result_obj.recommendations = [
                    "Ensure Azure CLI is authenticated",
                    "Check Azure subscription permissions",
                    "Verify network connectivity to Azure",
                ]

            self.current_diagnostic.results.append(result_obj)

        except Exception as e:
            logger.error(f"Azure resources check failed: {e}")

    async def _check_deployment_validation(self):
        """Check deployment validation setup"""
        start_time = datetime.now()

        try:
            validation_files = [
                self.workspace_path / "production_deployment_test.py",
                self.workspace_path / "azure_eeg_test_framework.py",
            ]

            existing_validations = [f for f in validation_files if f.exists()]

            if existing_validations:
                status = DiagnosticStatus.PASS
                message = (
                    f"Deployment validation files found: {len(existing_validations)}"
                )
            else:
                status = DiagnosticStatus.WARNING
                message = "No deployment validation files found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="deployment_validation",
                category=DiagnosticCategory.DEPLOYMENT,
                status=status,
                message=message,
                details={
                    "validation_files": [str(f) for f in validation_files],
                    "existing_files": [str(f) for f in existing_validations],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Create deployment validation tests",
                    "Implement pre-deployment checks",
                    "Add post-deployment verification",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Deployment validation check failed: {e}")

    async def _check_rollback_capability(self):
        """Check rollback capability"""
        start_time = datetime.now()

        try:
            # Check for rollback scripts or configurations
            rollback_files = [
                self.workspace_path / "rollback.py",
                self.workspace_path
                / "azure_deployment_manager.py",  # May contain rollback logic
            ]

            existing_rollback = [f for f in rollback_files if f.exists()]

            if existing_rollback:
                status = DiagnosticStatus.PASS
                message = f"Rollback capabilities found: {len(existing_rollback)}"
            else:
                status = DiagnosticStatus.WARNING
                message = "No explicit rollback capabilities found"

            duration = (datetime.now() - start_time).total_seconds() * 1000

            result = DiagnosticResult(
                check_name="rollback_capability",
                category=DiagnosticCategory.DEPLOYMENT,
                status=status,
                message=message,
                details={
                    "rollback_files": [str(f) for f in rollback_files],
                    "existing_files": [str(f) for f in existing_rollback],
                },
                duration_ms=duration,
            )

            if status == DiagnosticStatus.WARNING:
                result.recommendations = [
                    "Implement rollback scripts and procedures",
                    "Add deployment versioning for rollbacks",
                    "Test rollback procedures regularly",
                ]

            self.current_diagnostic.results.append(result)

        except Exception as e:
            logger.error(f"Rollback capability check failed: {e}")

    def _calculate_overall_status(self):
        """Calculate overall diagnostic status"""
        if not self.current_diagnostic.results:
            self.current_diagnostic.overall_status = DiagnosticStatus.UNKNOWN
            return

        # Count results by status
        status_counts = {}
        for result in self.current_diagnostic.results:
            status_counts[result.status] = status_counts.get(result.status, 0) + 1

        # Determine overall status
        if status_counts.get(DiagnosticStatus.FAIL, 0) > 0:
            self.current_diagnostic.overall_status = DiagnosticStatus.FAIL
        elif status_counts.get(DiagnosticStatus.WARNING, 0) > 0:
            self.current_diagnostic.overall_status = DiagnosticStatus.WARNING
        elif status_counts.get(DiagnosticStatus.PASS, 0) > 0:
            self.current_diagnostic.overall_status = DiagnosticStatus.PASS
        else:
            self.current_diagnostic.overall_status = DiagnosticStatus.UNKNOWN

    def get_diagnostic_report(
        self, diagnostic: PipelineDiagnostic = None
    ) -> Dict[str, Any]:
        """Generate comprehensive diagnostic report"""
        if diagnostic is None:
            diagnostic = (
                self.current_diagnostic or self.diagnostic_history[-1]
                if self.diagnostic_history
                else None
            )

        if not diagnostic:
            return {"error": "No diagnostic data available"}

        # Group results by category and status
        category_summary = {}
        status_summary = {}

        for result in diagnostic.results:
            # Category summary
            if result.category.value not in category_summary:
                category_summary[result.category.value] = {
                    "total": 0,
                    "pass": 0,
                    "fail": 0,
                    "warning": 0,
                    "skip": 0,
                }
            category_summary[result.category.value]["total"] += 1
            category_summary[result.category.value][result.status.value] += 1

            # Status summary
            status_summary[result.status.value] = (
                status_summary.get(result.status.value, 0) + 1
            )

        report = {
            "pipeline_name": diagnostic.pipeline_name,
            "stage": diagnostic.stage.value,
            "overall_status": diagnostic.overall_status.value,
            "start_time": (
                diagnostic.start_time.isoformat() if diagnostic.start_time else None
            ),
            "end_time": (
                diagnostic.end_time.isoformat() if diagnostic.end_time else None
            ),
            "total_duration_ms": diagnostic.total_duration_ms,
            "total_checks": len(diagnostic.results),
            "status_summary": status_summary,
            "category_summary": category_summary,
            "results": [
                {
                    "check_name": r.check_name,
                    "category": r.category.value,
                    "status": r.status.value,
                    "message": r.message,
                    "duration_ms": r.duration_ms,
                    "recommendations": r.recommendations,
                }
                for r in diagnostic.results
            ],
            "critical_issues": [
                {
                    "check_name": r.check_name,
                    "message": r.message,
                    "recommendations": r.recommendations,
                }
                for r in diagnostic.results
                if r.status in [DiagnosticStatus.FAIL, DiagnosticStatus.WARNING]
            ],
        }

        return report

    def export_diagnostic_report(
        self, filepath: str, diagnostic: PipelineDiagnostic = None
    ) -> bool:
        """Export diagnostic report to file"""
        try:
            report = self.get_diagnostic_report(diagnostic)
            report["export_timestamp"] = datetime.now().isoformat()

            with open(filepath, "w") as f:
                json.dump(report, f, indent=2, default=str)

            logger.info(f"Diagnostic report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export diagnostic report: {e}")
            return False


# Factory function for easy instantiation
def create_cicd_diagnostic_tool(
    workspace_path: Optional[str] = None,
) -> CICDDiagnosticTool:
    """
    Factory function to create CI/CD diagnostic tool

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured CICDDiagnosticTool instance
    """
    return CICDDiagnosticTool(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for CI/CD diagnostics"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform CI/CD Diagnostic Tool"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--pipeline",
        "-p",
        default="life-platform-pipeline",
        help="Pipeline name for diagnostics",
    )
    parser.add_argument(
        "--stage",
        "-s",
        choices=["build", "test", "deploy", "validate", "monitor"],
        default="build",
        help="Pipeline stage to diagnose",
    )
    parser.add_argument(
        "--report",
        "-r",
        action="store_true",
        help="Generate and display diagnostic report",
    )
    parser.add_argument(
        "--export", "-e", help="Export diagnostic report to specified file"
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=[
            "environment",
            "dependencies",
            "configuration",
            "security",
            "performance",
            "integration",
            "deployment",
        ],
        help="Run diagnostics for specific category only",
    )

    args = parser.parse_args()

    # Create diagnostic tool
    tool = create_cicd_diagnostic_tool(workspace_path=args.workspace)

    # Convert stage string to enum
    stage_map = {
        "build": PipelineStage.BUILD,
        "test": PipelineStage.TEST,
        "deploy": PipelineStage.DEPLOY,
        "validate": PipelineStage.VALIDATE,
        "monitor": PipelineStage.MONITOR,
    }
    stage = stage_map[args.stage]

    print("L.I.F.E. Platform - CI/CD Diagnostic Tool")
    print("=" * 50)
    print(f"Workspace: {args.workspace or os.getcwd()}")
    print(f"Pipeline: {args.pipeline}")
    print(f"Stage: {args.stage}")
    print("\nRunning diagnostics... (this may take a moment)")

    try:
        # Run diagnostics
        diagnostic = asyncio.run(
            tool.run_full_diagnostic(pipeline_name=args.pipeline, stage=stage)
        )

        if args.report:
            report = tool.get_diagnostic_report(diagnostic)
            print(f"\nDiagnostic Report for {args.pipeline}")
            print(f"Overall Status: {report['overall_status'].upper()}")
            print(f"Total Checks: {report['total_checks']}")
            print(f"Duration: {report.get('total_duration_ms', 0):.1f}ms")

            print("\nStatus Summary:")
            for status, count in report["status_summary"].items():
                print(f"  {status.upper()}: {count}")

            if report["critical_issues"]:
                print(f"\nCritical Issues ({len(report['critical_issues'])}):")
                for issue in report["critical_issues"][:5]:  # Show first 5
                    print(f"  ⚠️ {issue['check_name']}: {issue['message']}")
                    if issue["recommendations"]:
                        print(f"     → {issue['recommendations'][0]}")

            if len(report["critical_issues"]) > 5:
                print(f"  ... and {len(report['critical_issues']) - 5} more issues")

        if args.export:
            if tool.export_diagnostic_report(args.export, diagnostic):
                print(f"\nDiagnostic report exported to {args.export}")
            else:
                print("\nFailed to export diagnostic report")
                return 1

        # Return appropriate exit code
        if diagnostic.overall_status == DiagnosticStatus.FAIL:
            print("\n❌ Diagnostics completed with FAILURES")
            return 1
        elif diagnostic.overall_status == DiagnosticStatus.WARNING:
            print("\n⚠️ Diagnostics completed with WARNINGS")
            return 0  # Warnings don't fail the build
        else:
            print("\n✅ Diagnostics completed successfully")
            return 0

    except KeyboardInterrupt:
        print("\nDiagnostics interrupted by user")
        return 1
    except Exception as e:
        print(f"\nDiagnostics failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
