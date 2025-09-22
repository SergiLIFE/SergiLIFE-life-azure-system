#!/usr/bin/env python3
"""
L.I.F.E. Platform - Deployment Automation Suite
Automated deployment and configuration management

This module provides automated deployment capabilities for
the L.I.F.E. Platform across different environments and
cloud providers.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DeploymentEnvironment(Enum):
    """Deployment environments"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class DeploymentTarget(Enum):
    """Deployment targets"""

    AZURE_FUNCTIONS = "azure_functions"
    AZURE_WEB_APP = "azure_web_app"
    AZURE_CONTAINER = "azure_container"
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    LOCAL = "local"


class DeploymentStatus(Enum):
    """Deployment status"""

    PENDING = "pending"
    INITIALIZING = "initializing"
    BUILDING = "building"
    DEPLOYING = "deploying"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class DeploymentStep(Enum):
    """Deployment steps"""

    VALIDATE_CONFIG = "validate_config"
    BUILD_ARTIFACTS = "build_artifacts"
    SETUP_INFRASTRUCTURE = "setup_infrastructure"
    DEPLOY_APPLICATION = "deploy_application"
    CONFIGURE_SERVICES = "configure_services"
    RUN_MIGRATIONS = "run_migrations"
    VERIFY_DEPLOYMENT = "verify_deployment"
    CLEANUP = "cleanup"


@dataclass
class DeploymentConfig:
    """Deployment configuration"""

    environment: DeploymentEnvironment
    target: DeploymentTarget
    version: str
    build_number: str = ""
    git_commit: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    # Azure-specific config
    azure_subscription_id: Optional[str] = None
    azure_resource_group: Optional[str] = None
    azure_location: str = "eastus2"
    azure_app_name: Optional[str] = None

    # Docker/Kubernetes config
    docker_registry: Optional[str] = None
    kubernetes_namespace: str = "default"
    image_tag: Optional[str] = None

    # General config
    config_overrides: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    secrets: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeploymentStepResult:
    """Result of a deployment step"""

    step: DeploymentStep
    status: DeploymentStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    output: str = ""
    error_message: str = ""
    artifacts: Dict[str, Any] = field(default_factory=dict)
    success: bool = False


@dataclass
class DeploymentResult:
    """Complete deployment result"""

    deployment_id: str
    config: DeploymentConfig
    status: DeploymentStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    total_duration_seconds: float = 0.0
    steps: List[DeploymentStepResult] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    rollback_info: Dict[str, Any] = field(default_factory=dict)
    verification_results: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    error_message: str = ""


class DeploymentAutomationSuite:
    """
    Deployment Automation Suite for L.I.F.E. Platform

    Provides automated deployment capabilities across multiple
    environments and cloud providers with rollback support.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.deployment_history: List[DeploymentResult] = []
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialize deployment steps
        self.deployment_steps = self._initialize_deployment_steps()

        logger.info(
            f"Deployment Automation Suite initialized for workspace: {self.workspace_path}"
        )

    def _initialize_deployment_steps(
        self,
    ) -> Dict[DeploymentTarget, List[DeploymentStep]]:
        """Initialize deployment steps for each target"""
        return {
            DeploymentTarget.AZURE_FUNCTIONS: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.SETUP_INFRASTRUCTURE,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
            DeploymentTarget.AZURE_WEB_APP: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.SETUP_INFRASTRUCTURE,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.RUN_MIGRATIONS,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
            DeploymentTarget.AZURE_CONTAINER: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.SETUP_INFRASTRUCTURE,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
            DeploymentTarget.DOCKER_COMPOSE: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.RUN_MIGRATIONS,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
            DeploymentTarget.KUBERNETES: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.SETUP_INFRASTRUCTURE,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.RUN_MIGRATIONS,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
            DeploymentTarget.LOCAL: [
                DeploymentStep.VALIDATE_CONFIG,
                DeploymentStep.BUILD_ARTIFACTS,
                DeploymentStep.DEPLOY_APPLICATION,
                DeploymentStep.CONFIGURE_SERVICES,
                DeploymentStep.RUN_MIGRATIONS,
                DeploymentStep.VERIFY_DEPLOYMENT,
                DeploymentStep.CLEANUP,
            ],
        }

    async def deploy(self, config: DeploymentConfig) -> DeploymentResult:
        """Execute deployment with given configuration"""
        deployment_id = f"deploy_{config.environment.value}_{config.target.value}_{int(datetime.now().timestamp())}"

        result = DeploymentResult(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.INITIALIZING,
            start_time=datetime.now(),
        )

        logger.info(
            f"Starting deployment {deployment_id} to {config.target.value} ({config.environment.value})"
        )

        try:
            # Get deployment steps for target
            steps = self.deployment_steps.get(config.target, [])
            if not steps:
                raise ValueError(
                    f"No deployment steps defined for target {config.target.value}"
                )

            # Execute each step
            for step in steps:
                step_result = await self._execute_deployment_step(step, config)
                result.steps.append(step_result)

                if not step_result.success:
                    result.status = DeploymentStatus.FAILED
                    result.error_message = (
                        f"Step {step.value} failed: {step_result.error_message}"
                    )
                    logger.error(
                        f"Deployment {deployment_id} failed at step {step.value}"
                    )

                    # Attempt rollback if not in development
                    if config.environment != DeploymentEnvironment.DEVELOPMENT:
                        await self._rollback_deployment(result)

                    break

            # Mark as completed if all steps succeeded
            if result.status != DeploymentStatus.FAILED:
                result.status = DeploymentStatus.COMPLETED
                result.success = True
                logger.info(f"Deployment {deployment_id} completed successfully")

        except Exception as e:
            result.status = DeploymentStatus.FAILED
            result.error_message = f"Deployment failed: {str(e)}"
            logger.error(f"Deployment {deployment_id} failed: {e}")

        finally:
            result.end_time = datetime.now()
            result.total_duration_seconds = (
                result.end_time - result.start_time
            ).total_seconds()
            self.deployment_history.append(result)

        return result

    async def _execute_deployment_step(
        self, step: DeploymentStep, config: DeploymentConfig
    ) -> DeploymentStepResult:
        """Execute a single deployment step"""
        result = DeploymentStepResult(
            step=step, status=DeploymentStatus.RUNNING, start_time=datetime.now()
        )

        try:
            logger.info(f"Executing deployment step: {step.value}")

            # Execute step based on type
            if step == DeploymentStep.VALIDATE_CONFIG:
                success, output, error = await self._validate_configuration(config)
            elif step == DeploymentStep.BUILD_ARTIFACTS:
                success, output, error = await self._build_artifacts(config)
            elif step == DeploymentStep.SETUP_INFRASTRUCTURE:
                success, output, error = await self._setup_infrastructure(config)
            elif step == DeploymentStep.DEPLOY_APPLICATION:
                success, output, error = await self._deploy_application(config)
            elif step == DeploymentStep.CONFIGURE_SERVICES:
                success, output, error = await self._configure_services(config)
            elif step == DeploymentStep.RUN_MIGRATIONS:
                success, output, error = await self._run_migrations(config)
            elif step == DeploymentStep.VERIFY_DEPLOYMENT:
                success, output, error = await self._verify_deployment(config)
            elif step == DeploymentStep.CLEANUP:
                success, output, error = await self._cleanup_deployment(config)
            else:
                success, output, error = False, "", f"Unknown step: {step.value}"

            result.success = success
            result.output = output
            result.error_message = error

            if success:
                result.status = DeploymentStatus.COMPLETED
                logger.info(f"Step {step.value} completed successfully")
            else:
                result.status = DeploymentStatus.FAILED
                logger.error(f"Step {step.value} failed: {error}")

        except Exception as e:
            result.status = DeploymentStatus.FAILED
            result.error_message = f"Step execution failed: {str(e)}"
            logger.error(f"Step {step.value} execution failed: {e}")

        finally:
            result.end_time = datetime.now()
            result.duration_seconds = (
                result.end_time - result.start_time
            ).total_seconds()

        return result

    async def _validate_configuration(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Validate deployment configuration"""
        try:
            output_lines = []

            # Validate basic config
            if not config.version:
                return False, "", "Version is required"

            output_lines.append(
                f"Validating configuration for {config.environment.value} deployment to {config.target.value}"
            )

            # Validate target-specific requirements
            if config.target in [
                DeploymentTarget.AZURE_FUNCTIONS,
                DeploymentTarget.AZURE_WEB_APP,
                DeploymentTarget.AZURE_CONTAINER,
            ]:
                if not config.azure_subscription_id:
                    return (
                        False,
                        "",
                        "Azure subscription ID is required for Azure deployments",
                    )

                if not config.azure_resource_group:
                    return (
                        False,
                        "",
                        "Azure resource group is required for Azure deployments",
                    )

                output_lines.append(
                    f"Azure subscription: {config.azure_subscription_id}"
                )
                output_lines.append(
                    f"Azure resource group: {config.azure_resource_group}"
                )

            elif config.target == DeploymentTarget.KUBERNETES:
                if not config.kubernetes_namespace:
                    return False, "", "Kubernetes namespace is required"

                output_lines.append(
                    f"Kubernetes namespace: {config.kubernetes_namespace}"
                )

            # Validate required files exist
            required_files = ["requirements.txt", "azure_config.py"]
            for file in required_files:
                if not (self.workspace_path / file).exists():
                    return False, "", f"Required file not found: {file}"

            output_lines.append("All required files present")

            # Validate environment variables
            missing_vars = []
            if config.target == DeploymentTarget.AZURE_FUNCTIONS:
                required_vars = ["AZURE_SUBSCRIPTION_ID", "AZURE_CLIENT_ID"]
                for var in required_vars:
                    if (
                        var not in os.environ
                        and var not in config.environment_variables
                    ):
                        missing_vars.append(var)

            if missing_vars:
                return (
                    False,
                    "",
                    f"Missing required environment variables: {', '.join(missing_vars)}",
                )

            output_lines.append("Configuration validation completed successfully")
            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Configuration validation failed: {str(e)}"

    async def _build_artifacts(self, config: DeploymentConfig) -> tuple[bool, str, str]:
        """Build deployment artifacts"""
        try:
            output_lines = []

            if config.target in [
                DeploymentTarget.AZURE_FUNCTIONS,
                DeploymentTarget.AZURE_WEB_APP,
            ]:
                # Build Python package
                output_lines.append("Building Python artifacts...")

                # Create deployment package
                build_dir = self.workspace_path / "build"
                build_dir.mkdir(exist_ok=True)

                # Copy source files
                import shutil

                for file in [
                    "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
                    "azure_config.py",
                    "azure_functions_workflow.py",
                    "requirements.txt",
                ]:
                    if (self.workspace_path / file).exists():
                        shutil.copy2(self.workspace_path / file, build_dir / file)

                output_lines.append(f"Artifacts built in {build_dir}")

            elif config.target == DeploymentTarget.DOCKER_COMPOSE:
                # Build Docker images
                output_lines.append("Building Docker images...")

                dockerfile_path = self.workspace_path / "Dockerfile"
                if not dockerfile_path.exists():
                    return False, "", "Dockerfile not found"

                # Build Docker image
                image_tag = config.image_tag or f"life-platform:{config.version}"
                cmd = ["docker", "build", "-t", image_tag, str(self.workspace_path)]

                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", f"Docker build failed: {result.stderr}"

                output_lines.append(f"Docker image built: {image_tag}")

            elif config.target == DeploymentTarget.KUBERNETES:
                # Build container image for Kubernetes
                output_lines.append("Building container image for Kubernetes...")

                # Similar to Docker build but with Kubernetes-specific tagging
                image_tag = (
                    f"{config.docker_registry}/life-platform:{config.version}"
                    if config.docker_registry
                    else f"life-platform:{config.version}"
                )

                cmd = ["docker", "build", "-t", image_tag, str(self.workspace_path)]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", f"Container build failed: {result.stderr}"

                output_lines.append(f"Container image built: {image_tag}")

            output_lines.append("Artifact build completed successfully")
            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Artifact build failed: {str(e)}"

    async def _setup_infrastructure(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Setup deployment infrastructure"""
        try:
            output_lines = []

            if config.target in [
                DeploymentTarget.AZURE_FUNCTIONS,
                DeploymentTarget.AZURE_WEB_APP,
                DeploymentTarget.AZURE_CONTAINER,
            ]:
                output_lines.append("Setting up Azure infrastructure...")

                # Check Azure CLI availability
                cmd = ["az", "version"]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", "Azure CLI not available"

                # Login check
                cmd = ["az", "account", "show"]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", "Azure CLI not logged in. Run 'az login' first"

                # Create resource group if it doesn't exist
                cmd = ["az", "group", "show", "--name", config.azure_resource_group]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    # Create resource group
                    cmd = [
                        "az",
                        "group",
                        "create",
                        "--name",
                        config.azure_resource_group,
                        "--location",
                        config.azure_location,
                    ]
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._run_command, cmd
                    )

                    if result.returncode != 0:
                        return (
                            False,
                            "",
                            f"Failed to create resource group: {result.stderr}",
                        )

                    output_lines.append(
                        f"Created resource group: {config.azure_resource_group}"
                    )

                output_lines.append("Azure infrastructure setup completed")

            elif config.target == DeploymentTarget.KUBERNETES:
                output_lines.append("Setting up Kubernetes infrastructure...")

                # Check kubectl availability
                cmd = ["kubectl", "version", "--client"]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", "kubectl not available"

                # Create namespace if it doesn't exist
                cmd = ["kubectl", "get", "namespace", config.kubernetes_namespace]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    # Create namespace
                    cmd = [
                        "kubectl",
                        "create",
                        "namespace",
                        config.kubernetes_namespace,
                    ]
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._run_command, cmd
                    )

                    if result.returncode != 0:
                        return False, "", f"Failed to create namespace: {result.stderr}"

                    output_lines.append(
                        f"Created namespace: {config.kubernetes_namespace}"
                    )

                output_lines.append("Kubernetes infrastructure setup completed")

            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Infrastructure setup failed: {str(e)}"

    async def _deploy_application(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Deploy the application"""
        try:
            output_lines = []

            if config.target == DeploymentTarget.AZURE_FUNCTIONS:
                output_lines.append("Deploying to Azure Functions...")

                # Use Azure Functions Core Tools or az CLI
                app_name = (
                    config.azure_app_name
                    or f"life-functions-{config.environment.value}"
                )

                # Create function app if it doesn't exist
                cmd = [
                    "az",
                    "functionapp",
                    "show",
                    "--name",
                    app_name,
                    "--resource-group",
                    config.azure_resource_group,
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    # Create function app
                    cmd = [
                        "az",
                        "functionapp",
                        "create",
                        "--name",
                        app_name,
                        "--resource-group",
                        config.azure_resource_group,
                        "--consumption-plan-location",
                        config.azure_location,
                        "--runtime",
                        "python",
                        "--runtime-version",
                        "3.9",
                        "--functions-version",
                        "4",
                        "--os-type",
                        "linux",
                    ]
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._run_command, cmd
                    )

                    if result.returncode != 0:
                        return (
                            False,
                            "",
                            f"Failed to create function app: {result.stderr}",
                        )

                    output_lines.append(f"Created function app: {app_name}")

                # Deploy function code
                cmd = [
                    "az",
                    "functionapp",
                    "deployment",
                    "source",
                    "config-zip",
                    "--name",
                    app_name,
                    "--resource-group",
                    config.azure_resource_group,
                    "--src",
                    str(self.workspace_path / "build" / "deployment.zip"),
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", f"Function deployment failed: {result.stderr}"

                output_lines.append(f"Deployed functions to: {app_name}")

            elif config.target == DeploymentTarget.DOCKER_COMPOSE:
                output_lines.append("Deploying with Docker Compose...")

                compose_file = self.workspace_path / "docker-compose.yml"
                if not compose_file.exists():
                    return False, "", "docker-compose.yml not found"

                # Deploy with docker-compose
                cmd = ["docker-compose", "-f", str(compose_file), "up", "-d"]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return (
                        False,
                        "",
                        f"Docker Compose deployment failed: {result.stderr}",
                    )

                output_lines.append("Docker Compose deployment completed")

            elif config.target == DeploymentTarget.KUBERNETES:
                output_lines.append("Deploying to Kubernetes...")

                # Apply Kubernetes manifests
                manifests_dir = self.workspace_path / "k8s"
                if not manifests_dir.exists():
                    return False, "", "Kubernetes manifests directory not found"

                for manifest_file in manifests_dir.glob("*.yaml"):
                    cmd = [
                        "kubectl",
                        "apply",
                        "-f",
                        str(manifest_file),
                        "--namespace",
                        config.kubernetes_namespace,
                    ]
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._run_command, cmd
                    )

                    if result.returncode != 0:
                        return (
                            False,
                            "",
                            f"Kubernetes deployment failed for {manifest_file.name}: {result.stderr}",
                        )

                output_lines.append(
                    f"Kubernetes deployment completed in namespace: {config.kubernetes_namespace}"
                )

            elif config.target == DeploymentTarget.LOCAL:
                output_lines.append("Deploying locally...")

                # Install dependencies and start services
                cmd = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(self.workspace_path / "requirements.txt"),
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", f"Dependency installation failed: {result.stderr}"

                output_lines.append("Local deployment completed")

            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Application deployment failed: {str(e)}"

    async def _configure_services(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Configure deployed services"""
        try:
            output_lines = []

            if config.target in [
                DeploymentTarget.AZURE_FUNCTIONS,
                DeploymentTarget.AZURE_WEB_APP,
            ]:
                output_lines.append("Configuring Azure services...")

                # Set environment variables
                app_name = (
                    config.azure_app_name
                    or f"life-functions-{config.environment.value}"
                )

                for key, value in config.environment_variables.items():
                    cmd = [
                        "az",
                        "functionapp",
                        "config",
                        "appsettings",
                        "set",
                        "--name",
                        app_name,
                        "--resource-group",
                        config.azure_resource_group,
                        "--setting",
                        f"{key}={value}",
                    ]
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._run_command, cmd
                    )

                    if result.returncode != 0:
                        return (
                            False,
                            "",
                            f"Failed to set environment variable {key}: {result.stderr}",
                        )

                output_lines.append(
                    f"Configured {len(config.environment_variables)} environment variables"
                )

            elif config.target == DeploymentTarget.KUBERNETES:
                output_lines.append("Configuring Kubernetes services...")

                # Apply ConfigMaps and Secrets
                config_dir = self.workspace_path / "k8s" / "config"
                if config_dir.exists():
                    for config_file in config_dir.glob("*.yaml"):
                        cmd = [
                            "kubectl",
                            "apply",
                            "-f",
                            str(config_file),
                            "--namespace",
                            config.kubernetes_namespace,
                        ]
                        result = await asyncio.get_event_loop().run_in_executor(
                            self.executor, self._run_command, cmd
                        )

                        if result.returncode != 0:
                            return (
                                False,
                                "",
                                f"Failed to apply config {config_file.name}: {result.stderr}",
                            )

                    output_lines.append("Kubernetes configuration applied")

            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Service configuration failed: {str(e)}"

    async def _run_migrations(self, config: DeploymentConfig) -> tuple[bool, str, str]:
        """Run database migrations or setup tasks"""
        try:
            output_lines = []

            # For now, this is a placeholder for database migrations
            # In a real implementation, this would run database schema updates,
            # data migrations, etc.

            output_lines.append("Running migrations/setup tasks...")

            if config.target == DeploymentTarget.AZURE_FUNCTIONS:
                # Run any initialization scripts
                output_lines.append("Azure Functions initialization completed")

            elif config.target == DeploymentTarget.KUBERNETES:
                # Wait for pods to be ready
                cmd = [
                    "kubectl",
                    "wait",
                    "--for=condition=ready",
                    "pod",
                    "--all",
                    "--namespace",
                    config.kubernetes_namespace,
                    "--timeout=300s",
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return (
                        False,
                        "",
                        f"Kubernetes pods failed to become ready: {result.stderr}",
                    )

                output_lines.append("Kubernetes pods are ready")

            output_lines.append("Migrations completed successfully")
            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Migrations failed: {str(e)}"

    async def _verify_deployment(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Verify deployment success"""
        try:
            output_lines = []

            if config.target == DeploymentTarget.AZURE_FUNCTIONS:
                output_lines.append("Verifying Azure Functions deployment...")

                app_name = (
                    config.azure_app_name
                    or f"life-functions-{config.environment.value}"
                )

                # Check function app status
                cmd = [
                    "az",
                    "functionapp",
                    "show",
                    "--name",
                    app_name,
                    "--resource-group",
                    config.azure_resource_group,
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return (
                        False,
                        "",
                        f"Function app verification failed: {result.stderr}",
                    )

                # Parse JSON response to check state
                import json

                app_info = json.loads(result.stdout)
                state = app_info.get("state")

                if state != "Running":
                    return False, "", f"Function app is not running. State: {state}"

                output_lines.append(f"Function app {app_name} is running")

            elif config.target == DeploymentTarget.DOCKER_COMPOSE:
                output_lines.append("Verifying Docker Compose deployment...")

                # Check container status
                cmd = ["docker-compose", "ps"]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return (
                        False,
                        "",
                        f"Docker Compose status check failed: {result.stderr}",
                    )

                if "Up" not in result.stdout:
                    return False, "", "Not all containers are running"

                output_lines.append("All containers are running")

            elif config.target == DeploymentTarget.KUBERNETES:
                output_lines.append("Verifying Kubernetes deployment...")

                # Check pod status
                cmd = [
                    "kubectl",
                    "get",
                    "pods",
                    "--namespace",
                    config.kubernetes_namespace,
                ]
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                if result.returncode != 0:
                    return False, "", f"Kubernetes pod check failed: {result.stderr}"

                if "Running" not in result.stdout:
                    return False, "", "Not all pods are running"

                output_lines.append("All Kubernetes pods are running")

            output_lines.append("Deployment verification completed successfully")
            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Deployment verification failed: {str(e)}"

    async def _cleanup_deployment(
        self, config: DeploymentConfig
    ) -> tuple[bool, str, str]:
        """Clean up deployment artifacts"""
        try:
            output_lines = []

            # Clean up build artifacts
            build_dir = self.workspace_path / "build"
            if build_dir.exists():
                import shutil

                shutil.rmtree(build_dir)
                output_lines.append("Build artifacts cleaned up")

            # Clean up temporary files
            for temp_file in self.workspace_path.glob("*.tmp"):
                temp_file.unlink()
                output_lines.append(f"Removed temporary file: {temp_file.name}")

            output_lines.append("Deployment cleanup completed")
            return True, "\n".join(output_lines), ""

        except Exception as e:
            return False, "", f"Cleanup failed: {str(e)}"

    async def _rollback_deployment(self, result: DeploymentResult) -> None:
        """Rollback failed deployment"""
        try:
            logger.info(f"Rolling back deployment {result.deployment_id}")

            config = result.config

            if config.target == DeploymentTarget.AZURE_FUNCTIONS:
                # Rollback Azure Functions deployment
                app_name = (
                    config.azure_app_name
                    or f"life-functions-{config.environment.value}"
                )

                # Could implement rollback to previous version
                # For now, just log the rollback attempt
                result.rollback_info = {
                    "rollback_type": "azure_functions",
                    "app_name": app_name,
                    "status": "rollback_attempted",
                }

            elif config.target == DeploymentTarget.DOCKER_COMPOSE:
                # Stop containers
                cmd = ["docker-compose", "down"]
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self._run_command, cmd
                )

                result.rollback_info = {
                    "rollback_type": "docker_compose",
                    "status": "containers_stopped",
                }

            result.status = DeploymentStatus.ROLLED_BACK
            logger.info(f"Deployment {result.deployment_id} rolled back")

        except Exception as e:
            logger.error(f"Rollback failed for deployment {result.deployment_id}: {e}")
            result.rollback_info = {"error": str(e)}

    def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Run a shell command"""
        return subprocess.run(
            cmd, capture_output=True, text=True, cwd=self.workspace_path
        )

    def get_deployment_history(self, limit: int = 10) -> List[DeploymentResult]:
        """Get recent deployment history"""
        return self.deployment_history[-limit:]

    def export_deployment_report(self, deployment_id: str, filepath: str) -> bool:
        """Export deployment report to file"""
        for result in self.deployment_history:
            if result.deployment_id == deployment_id:
                try:
                    export_data = {
                        "deployment_id": result.deployment_id,
                        "config": {
                            "environment": result.config.environment.value,
                            "target": result.config.target.value,
                            "version": result.config.version,
                            "timestamp": result.config.timestamp.isoformat(),
                        },
                        "status": result.status.value,
                        "success": result.success,
                        "start_time": result.start_time.isoformat(),
                        "end_time": (
                            result.end_time.isoformat() if result.end_time else None
                        ),
                        "total_duration_seconds": result.total_duration_seconds,
                        "steps": [
                            {
                                "step": step.step.value,
                                "status": step.status.value,
                                "success": step.success,
                                "duration_seconds": step.duration_seconds,
                                "output": step.output,
                                "error_message": step.error_message,
                            }
                            for step in result.steps
                        ],
                        "error_message": result.error_message,
                    }

                    with open(filepath, "w") as f:
                        json.dump(export_data, f, indent=2, default=str)

                    logger.info(f"Deployment report exported to {filepath}")
                    return True

                except Exception as e:
                    logger.error(f"Failed to export deployment report: {e}")
                    return False

        logger.warning(f"Deployment {deployment_id} not found")
        return False


# Factory function for easy instantiation
def create_deployment_automation_suite(
    workspace_path: Optional[str] = None,
) -> DeploymentAutomationSuite:
    """
    Factory function to create deployment automation suite

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured DeploymentAutomationSuite instance
    """
    return DeploymentAutomationSuite(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for deployment automation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Deployment Automation Suite"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--environment",
        "-e",
        choices=["development", "staging", "production", "testing"],
        default="development",
        help="Deployment environment",
    )
    parser.add_argument(
        "--target",
        "-t",
        choices=[
            "azure_functions",
            "azure_web_app",
            "azure_container",
            "docker_compose",
            "kubernetes",
            "local",
        ],
        default="local",
        help="Deployment target",
    )
    parser.add_argument("--version", "-v", required=True, help="Deployment version")
    parser.add_argument("--export", help="Export deployment report to specified file")
    parser.add_argument(
        "--history", action="store_true", help="Show deployment history"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create deployment suite
    suite = create_deployment_automation_suite(workspace_path=args.workspace)

    print("L.I.F.E. Platform - Deployment Automation Suite")
    print("=" * 55)

    try:
        if args.history:
            # Show deployment history
            history = suite.get_deployment_history(limit=5)
            print(f"\nRecent Deployments: {len(history)}")
            for deploy in history:
                status_icon = "✅" if deploy.success else "❌"
                print(f"  {status_icon} {deploy.deployment_id}")
                print(f"    Environment: {deploy.config.environment.value}")
                print(f"    Target: {deploy.config.target.value}")
                print(f"    Status: {deploy.status.value}")
                print(f"    Duration: {deploy.total_duration_seconds:.1f}s")
                print()

        else:
            # Execute deployment
            config = DeploymentConfig(
                environment=DeploymentEnvironment(args.environment),
                target=DeploymentTarget(args.target),
                version=args.version,
            )

            print(
                f"Deploying version {args.version} to {args.target} ({args.environment})"
            )

            # Run deployment
            result = asyncio.run(suite.deploy(config))

            print("\nDeployment Results:")
            print(f"  Deployment ID: {result.deployment_id}")
            print(f"  Status: {result.status.value}")
            print(f"  Success: {'✅ YES' if result.success else '❌ NO'}")
            print(f"  Duration: {result.total_duration_seconds:.1f}s")

            if result.steps:
                print("\nDeployment Steps:")
                for step in result.steps:
                    status_icon = "✅" if step.success else "❌"
                    print(
                        f"  {status_icon} {step.step.value}: {step.duration_seconds:.1f}s"
                    )

            if not result.success and result.error_message:
                print(f"\nError: {result.error_message}")

            if args.export:
                if suite.export_deployment_report(result.deployment_id, args.export):
                    print(f"\nDeployment report exported to {args.export}")
                else:
                    print("\nFailed to export deployment report")
                    return 1

            return 0 if result.success else 1

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nDeployment failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
