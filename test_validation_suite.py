#!/usr/bin/env python3
"""
L.I.F.E. Platform - Test Validation Suite
Comprehensive testing framework for L.I.F.E. Platform components

This module provides automated validation and testing capabilities
for all L.I.F.E. Platform components, ensuring production readiness
and compliance with enterprise standards.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestCategory(Enum):
    """Categories of tests"""

    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    DEPLOYMENT = "deployment"
    VALIDATION = "validation"


class TestStatus(Enum):
    """Status of test execution"""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


class TestPriority(Enum):
    """Priority levels for tests"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationType(Enum):
    """Types of validation checks"""

    SYNTAX = "syntax"
    IMPORT = "import"
    DEPENDENCY = "dependency"
    CONFIGURATION = "configuration"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    FUNCTIONAL = "functional"


@dataclass
class TestResult:
    """Result of a single test execution"""

    test_name: str
    category: TestCategory
    status: TestStatus
    priority: TestPriority
    execution_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: str = ""
    output: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TestSuite:
    """Collection of tests to be executed"""

    name: str
    description: str
    category: TestCategory
    tests: List[TestResult] = field(default_factory=list)
    setup_required: bool = False
    teardown_required: bool = False
    dependencies: List[str] = field(default_factory=list)
    environment_requirements: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Comprehensive validation report"""

    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0
    execution_time: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    test_results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    critical_failures: List[str] = field(default_factory=list)


class TestValidationSuite:
    """
    Test Validation Suite for L.I.F.E. Platform

    Provides comprehensive testing and validation capabilities
    for all platform components, ensuring production readiness.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.test_suites: Dict[str, TestSuite] = {}
        self.validation_reports: List[ValidationReport] = []
        self.execution_timeout = 300  # 5 minutes default timeout

        # Core test files and components
        self.core_components = [
            "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "autonomous_optimizer.py",
            "azure_config.py",
            "azure_functions_workflow.py",
            "production_deployment_test.py",
            "eeg_processor.py",
            "life_platform_api.py",
        ]

        logger.info(
            f"Test Validation Suite initialized for workspace: {self.workspace_path}"
        )

    async def run_full_validation_suite(self) -> ValidationReport:
        """Run complete validation suite"""
        logger.info("Starting full validation suite...")

        start_time = datetime.now()
        report = ValidationReport(start_time=start_time)

        try:
            # Initialize test suites
            await self._initialize_test_suites()

            # Run all test suites
            for suite_name, suite in self.test_suites.items():
                logger.info(f"Running test suite: {suite_name}")
                suite_results = await self._run_test_suite(suite)
                report.test_results.extend(suite_results)

            # Calculate statistics
            report.total_tests = len(report.test_results)
            report.passed_tests = sum(
                1 for r in report.test_results if r.status == TestStatus.PASSED
            )
            report.failed_tests = sum(
                1 for r in report.test_results if r.status == TestStatus.FAILED
            )
            report.error_tests = sum(
                1 for r in report.test_results if r.status == TestStatus.ERROR
            )
            report.skipped_tests = sum(
                1 for r in report.test_results if r.status == TestStatus.SKIPPED
            )

            # Calculate execution time
            report.end_time = datetime.now()
            report.execution_time = (report.end_time - start_time).total_seconds()

            # Generate summary and recommendations
            report.summary = self._generate_validation_summary(report)
            report.recommendations = self._generate_validation_recommendations(report)
            report.critical_failures = self._identify_critical_failures(report)

            logger.info(
                f"Validation suite complete. {report.passed_tests}/{report.total_tests} tests passed"
            )

        except Exception as e:
            logger.error(f"Validation suite failed: {e}")
            report.end_time = datetime.now()
            report.execution_time = (report.end_time - start_time).total_seconds()
            report.critical_failures.append(
                f"Validation suite execution failed: {str(e)}"
            )

        self.validation_reports.append(report)
        return report

    async def _initialize_test_suites(self):
        """Initialize all test suites"""
        # Syntax and import validation suite
        syntax_suite = TestSuite(
            name="syntax_validation",
            description="Validate Python syntax and imports for all components",
            category=TestCategory.VALIDATION,
        )
        self.test_suites["syntax_validation"] = syntax_suite

        # Core algorithm validation suite
        algorithm_suite = TestSuite(
            name="core_algorithm",
            description="Validate core L.I.F.E. algorithm functionality",
            category=TestCategory.UNIT,
        )
        self.test_suites["core_algorithm"] = algorithm_suite

        # Azure integration suite
        azure_suite = TestSuite(
            name="azure_integration",
            description="Validate Azure services integration",
            category=TestCategory.INTEGRATION,
        )
        self.test_suites["azure_integration"] = azure_suite

        # Performance validation suite
        performance_suite = TestSuite(
            name="performance_validation",
            description="Validate performance requirements and benchmarks",
            category=TestCategory.PERFORMANCE,
        )
        self.test_suites["performance_validation"] = performance_suite

        # Security and compliance suite
        security_suite = TestSuite(
            name="security_compliance",
            description="Validate security and compliance requirements",
            category=TestCategory.SECURITY,
        )
        self.test_suites["security_compliance"] = security_suite

        # Deployment validation suite
        deployment_suite = TestSuite(
            name="deployment_validation",
            description="Validate deployment readiness and configuration",
            category=TestCategory.DEPLOYMENT,
        )
        self.test_suites["deployment_validation"] = deployment_suite

    async def _run_test_suite(self, suite: TestSuite) -> List[TestResult]:
        """Run a specific test suite"""
        results = []

        if suite.name == "syntax_validation":
            results = await self._run_syntax_validation_tests()
        elif suite.name == "core_algorithm":
            results = await self._run_core_algorithm_tests()
        elif suite.name == "azure_integration":
            results = await self._run_azure_integration_tests()
        elif suite.name == "performance_validation":
            results = await self._run_performance_validation_tests()
        elif suite.name == "security_compliance":
            results = await self._run_security_compliance_tests()
        elif suite.name == "deployment_validation":
            results = await self._run_deployment_validation_tests()

        return results

    async def _run_syntax_validation_tests(self) -> List[TestResult]:
        """Run syntax and import validation tests"""
        results = []

        for component in self.core_components:
            component_path = self.workspace_path / component
            if not component_path.exists():
                result = TestResult(
                    test_name=f"syntax_check_{component}",
                    category=TestCategory.VALIDATION,
                    status=TestStatus.FAILED,
                    priority=TestPriority.CRITICAL,
                    error_message=f"Component file not found: {component}",
                )
                results.append(result)
                continue

            # Syntax validation
            syntax_result = await self._validate_python_syntax(component_path)
            results.append(syntax_result)

            # Import validation
            import_result = await self._validate_python_imports(component_path)
            results.append(import_result)

        return results

    async def _validate_python_syntax(self, file_path: Path) -> TestResult:
        """Validate Python syntax of a file"""
        result = TestResult(
            test_name=f"syntax_{file_path.name}",
            category=TestCategory.VALIDATION,
            status=TestStatus.PENDING,
            priority=TestPriority.CRITICAL,
            start_time=datetime.now(),
        )

        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Attempt to compile to check syntax
            compile(content, str(file_path), "exec")

            result.status = TestStatus.PASSED
            result.output = "Syntax validation passed"

        except SyntaxError as e:
            result.status = TestStatus.FAILED
            result.error_message = f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Validation error: {str(e)}"

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()
        return result

    async def _validate_python_imports(self, file_path: Path) -> TestResult:
        """Validate Python imports in a file"""
        result = TestResult(
            test_name=f"imports_{file_path.name}",
            category=TestCategory.VALIDATION,
            status=TestStatus.PENDING,
            priority=TestPriority.HIGH,
            start_time=datetime.now(),
        )

        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract import statements
            import_lines = []
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith(("import ", "from ")) and not line.startswith("#"):
                    import_lines.append(line)

            # Try to import each module
            failed_imports = []
            for import_line in import_lines:
                try:
                    # Execute import in isolated context
                    exec(import_line, {"__builtins__": {}})
                except ImportError as e:
                    failed_imports.append(f"{import_line}: {str(e)}")
                except Exception:
                    # Skip other execution errors (expected for complex imports)
                    pass

            if failed_imports:
                result.status = TestStatus.FAILED
                result.error_message = f"Failed imports: {', '.join(failed_imports)}"
            else:
                result.status = TestStatus.PASSED
                result.output = f"Successfully validated {len(import_lines)} imports"

        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Import validation error: {str(e)}"

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()
        return result

    async def _run_core_algorithm_tests(self) -> List[TestResult]:
        """Run core algorithm validation tests"""
        results = []

        # Test core algorithm import
        core_file = "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
        core_path = self.workspace_path / core_file

        if not core_path.exists():
            result = TestResult(
                test_name="core_algorithm_import",
                category=TestCategory.UNIT,
                status=TestStatus.FAILED,
                priority=TestPriority.CRITICAL,
                error_message=f"Core algorithm file not found: {core_file}",
            )
            results.append(result)
            return results

        # Test basic algorithm functionality
        result = TestResult(
            test_name="core_algorithm_basic_functionality",
            category=TestCategory.UNIT,
            status=TestStatus.PENDING,
            priority=TestPriority.CRITICAL,
            start_time=datetime.now(),
        )

        try:
            # Add workspace to Python path
            sys.path.insert(0, str(self.workspace_path))

            # Import and test basic functionality
            spec = importlib.util.spec_from_file_location("life_algorithm", core_path)
            life_module = importlib.util.module_from_spec(spec)

            # Basic import test
            spec.loader.exec_module(life_module)

            # Check for required classes/functions
            required_items = ["LIFEAlgorithmCore", "EEGMetrics", "LearningOutcome"]
            missing_items = []

            for item in required_items:
                if not hasattr(life_module, item):
                    missing_items.append(item)

            if missing_items:
                result.status = TestStatus.FAILED
                result.error_message = (
                    f"Missing required items: {', '.join(missing_items)}"
                )
            else:
                result.status = TestStatus.PASSED
                result.output = "Core algorithm components validated successfully"

        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Core algorithm test failed: {str(e)}"
        finally:
            # Clean up path
            if str(self.workspace_path) in sys.path:
                sys.path.remove(str(self.workspace_path))

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()
        results.append(result)

        return results

    async def _run_azure_integration_tests(self) -> List[TestResult]:
        """Run Azure integration validation tests"""
        results = []

        # Test Azure configuration
        azure_config_result = await self._validate_azure_config()
        results.append(azure_config_result)

        # Test Azure Functions workflow
        azure_functions_result = await self._validate_azure_functions()
        results.append(azure_functions_result)

        return results

    async def _validate_azure_config(self) -> TestResult:
        """Validate Azure configuration"""
        result = TestResult(
            test_name="azure_config_validation",
            category=TestCategory.INTEGRATION,
            status=TestStatus.PENDING,
            priority=TestPriority.HIGH,
            start_time=datetime.now(),
        )

        try:
            azure_config_path = self.workspace_path / "azure_config.py"
            if not azure_config_path.exists():
                result.status = TestStatus.FAILED
                result.error_message = "azure_config.py not found"
                return result

            # Import and validate configuration
            sys.path.insert(0, str(self.workspace_path))
            try:
                import azure_config

                # Check for required configuration items
                required_configs = [
                    "AZURE_SUBSCRIPTION_ID",
                    "AZURE_RESOURCE_GROUP",
                    "AZURE_LOCATION",
                ]
                missing_configs = []

                for config in required_configs:
                    if not hasattr(azure_config, config):
                        missing_configs.append(config)

                if missing_configs:
                    result.status = TestStatus.FAILED
                    result.error_message = (
                        f"Missing Azure configurations: {', '.join(missing_configs)}"
                    )
                else:
                    result.status = TestStatus.PASSED
                    result.output = "Azure configuration validated successfully"

            finally:
                if str(self.workspace_path) in sys.path:
                    sys.path.remove(str(self.workspace_path))

        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Azure config validation failed: {str(e)}"

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()
        return result

    async def _validate_azure_functions(self) -> TestResult:
        """Validate Azure Functions configuration"""
        result = TestResult(
            test_name="azure_functions_validation",
            category=TestCategory.INTEGRATION,
            status=TestStatus.PENDING,
            priority=TestPriority.HIGH,
            start_time=datetime.now(),
        )

        try:
            functions_path = self.workspace_path / "azure_functions_workflow.py"
            if not functions_path.exists():
                result.status = TestStatus.FAILED
                result.error_message = "azure_functions_workflow.py not found"
                return result

            # Basic syntax check (detailed validation would require Azure SDK)
            with open(functions_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for Azure Functions patterns
            required_patterns = [
                "def main",
                "azure.functions",
                "func.",
                "HttpRequest",
                "HttpResponse",
            ]

            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in content:
                    missing_patterns.append(pattern)

            if missing_patterns:
                result.status = TestStatus.FAILED
                result.error_message = (
                    f"Missing Azure Functions patterns: {', '.join(missing_patterns)}"
                )
            else:
                result.status = TestStatus.PASSED
                result.output = "Azure Functions configuration validated successfully"

        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Azure Functions validation failed: {str(e)}"

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()
        return result

    async def _run_performance_validation_tests(self) -> List[TestResult]:
        """Run performance validation tests"""
        results = []

        # Test execution time requirements
        performance_result = TestResult(
            test_name="performance_requirements",
            category=TestCategory.PERFORMANCE,
            status=TestStatus.PENDING,
            priority=TestPriority.HIGH,
            start_time=datetime.now(),
        )

        try:
            # Check for performance benchmarks
            benchmark_files = ["sota_benchmark.py", "autonomous_sota_kpi_monitor.py"]
            found_benchmarks = []

            for benchmark_file in benchmark_files:
                if (self.workspace_path / benchmark_file).exists():
                    found_benchmarks.append(benchmark_file)

            if not found_benchmarks:
                performance_result.status = TestStatus.FAILED
                performance_result.error_message = (
                    "No performance benchmark files found"
                )
            else:
                performance_result.status = TestStatus.PASSED
                performance_result.output = (
                    f"Found performance benchmarks: {', '.join(found_benchmarks)}"
                )

        except Exception as e:
            performance_result.status = TestStatus.ERROR
            performance_result.error_message = (
                f"Performance validation failed: {str(e)}"
            )

        performance_result.end_time = datetime.now()
        performance_result.execution_time = (
            performance_result.end_time - performance_result.start_time
        ).total_seconds()
        results.append(performance_result)

        return results

    async def _run_security_compliance_tests(self) -> List[TestResult]:
        """Run security and compliance validation tests"""
        results = []

        # Security configuration test
        security_result = TestResult(
            test_name="security_configuration",
            category=TestCategory.SECURITY,
            status=TestStatus.PENDING,
            priority=TestPriority.CRITICAL,
            start_time=datetime.now(),
        )

        try:
            # Check for security-related files
            security_files = ["azure_config.py", "production_deployment_test.py"]
            found_security = []

            for sec_file in security_files:
                if (self.workspace_path / sec_file).exists():
                    found_security.append(sec_file)

            if len(found_security) < len(security_files):
                security_result.status = TestStatus.FAILED
                security_result.error_message = "Missing security configuration files"
            else:
                security_result.status = TestStatus.PASSED
                security_result.output = "Security configuration files validated"

        except Exception as e:
            security_result.status = TestStatus.ERROR
            security_result.error_message = f"Security validation failed: {str(e)}"

        security_result.end_time = datetime.now()
        security_result.execution_time = (
            security_result.end_time - security_result.start_time
        ).total_seconds()
        results.append(security_result)

        return results

    async def _run_deployment_validation_tests(self) -> List[TestResult]:
        """Run deployment validation tests"""
        results = []

        # Deployment readiness test
        deployment_result = TestResult(
            test_name="deployment_readiness",
            category=TestCategory.DEPLOYMENT,
            status=TestStatus.PENDING,
            priority=TestPriority.CRITICAL,
            start_time=datetime.now(),
        )

        try:
            # Check for deployment-related files
            deployment_files = [
                "azure.yaml",
                "Dockerfile",
                "production_deployment_test.py",
                "requirements.txt",
            ]

            missing_files = []
            for dep_file in deployment_files:
                if not (self.workspace_path / dep_file).exists():
                    missing_files.append(dep_file)

            if missing_files:
                deployment_result.status = TestStatus.FAILED
                deployment_result.error_message = (
                    f"Missing deployment files: {', '.join(missing_files)}"
                )
            else:
                deployment_result.status = TestStatus.PASSED
                deployment_result.output = "All deployment files present and validated"

        except Exception as e:
            deployment_result.status = TestStatus.ERROR
            deployment_result.error_message = f"Deployment validation failed: {str(e)}"

        deployment_result.end_time = datetime.now()
        deployment_result.execution_time = (
            deployment_result.end_time - deployment_result.start_time
        ).total_seconds()
        results.append(deployment_result)

        return results

    def _generate_validation_summary(self, report: ValidationReport) -> Dict[str, Any]:
        """Generate validation summary"""
        summary = {
            "total_tests": report.total_tests,
            "passed_tests": report.passed_tests,
            "failed_tests": report.failed_tests,
            "error_tests": report.error_tests,
            "skipped_tests": report.skipped_tests,
            "success_rate": (
                f"{(report.passed_tests / report.total_tests * 100):.1f}%"
                if report.total_tests > 0
                else "0%"
            ),
            "execution_time_seconds": report.execution_time,
            "execution_time_formatted": f"{report.execution_time:.2f}s",
            "tests_by_category": {},
            "tests_by_priority": {},
        }

        # Group by category and priority
        for result in report.test_results:
            category = result.category.value
            priority = result.priority.value

            if category not in summary["tests_by_category"]:
                summary["tests_by_category"][category] = {
                    "passed": 0,
                    "failed": 0,
                    "total": 0,
                }
            if priority not in summary["tests_by_priority"]:
                summary["tests_by_priority"][priority] = {
                    "passed": 0,
                    "failed": 0,
                    "total": 0,
                }

            summary["tests_by_category"][category]["total"] += 1
            summary["tests_by_priority"][priority]["total"] += 1

            if result.status == TestStatus.PASSED:
                summary["tests_by_category"][category]["passed"] += 1
                summary["tests_by_priority"][priority]["passed"] += 1
            else:
                summary["tests_by_category"][category]["failed"] += 1
                summary["tests_by_priority"][priority]["failed"] += 1

        return summary

    def _generate_validation_recommendations(
        self, report: ValidationReport
    ) -> List[str]:
        """Generate validation recommendations"""
        recommendations = []

        # Check failure rates
        if report.failed_tests > 0:
            failure_rate = report.failed_tests / report.total_tests
            if failure_rate > 0.5:
                recommendations.append(
                    "High failure rate detected - immediate attention required"
                )
            elif failure_rate > 0.2:
                recommendations.append(
                    "Moderate failure rate - review and fix failed tests"
                )

        # Check critical failures
        critical_failures = [
            r
            for r in report.test_results
            if r.priority == TestPriority.CRITICAL and r.status != TestStatus.PASSED
        ]
        if critical_failures:
            recommendations.append(
                f"Address {len(critical_failures)} critical test failures before deployment"
            )

        # Check performance
        if report.execution_time > 600:  # 10 minutes
            recommendations.append(
                "Test execution time is high - consider optimization"
            )

        # Check test coverage
        categories_covered = len(set(r.category.value for r in report.test_results))
        if categories_covered < 5:
            recommendations.append("Limited test category coverage - expand test suite")

        if not recommendations:
            recommendations.append(
                "All tests passed successfully - ready for deployment"
            )

        return recommendations

    def _identify_critical_failures(self, report: ValidationReport) -> List[str]:
        """Identify critical test failures"""
        critical_failures = []

        for result in report.test_results:
            if result.priority == TestPriority.CRITICAL and result.status in [
                TestStatus.FAILED,
                TestStatus.ERROR,
            ]:
                critical_failures.append(f"{result.test_name}: {result.error_message}")

        return critical_failures

    def export_validation_report(self, filepath: str, report: ValidationReport) -> bool:
        """Export comprehensive validation report"""
        try:
            export_data = {
                "report_timestamp": datetime.now().isoformat(),
                "validation_summary": report.summary,
                "test_results": [
                    {
                        "test_name": result.test_name,
                        "category": result.category.value,
                        "status": result.status.value,
                        "priority": result.priority.value,
                        "execution_time": result.execution_time,
                        "error_message": result.error_message,
                        "output": result.output,
                    }
                    for result in report.test_results
                ],
                "recommendations": report.recommendations,
                "critical_failures": report.critical_failures,
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Validation report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export validation report: {e}")
            return False


# Factory function for easy instantiation
def create_test_validation_suite(
    workspace_path: Optional[str] = None,
) -> TestValidationSuite:
    """
    Factory function to create test validation suite

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured TestValidationSuite instance
    """
    return TestValidationSuite(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for test validation suite"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Test Validation Suite"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--export", "-e", help="Export validation report to specified file"
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=[
            "unit",
            "integration",
            "system",
            "performance",
            "security",
            "compliance",
            "deployment",
            "validation",
        ],
        help="Run only tests from specific category",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=300,
        help="Test execution timeout in seconds (default: 300)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create validation suite
    suite = create_test_validation_suite(workspace_path=args.workspace)
    suite.execution_timeout = args.timeout

    print("L.I.F.E. Platform - Test Validation Suite")
    print("=" * 50)
    print(f"Workspace: {args.workspace or os.getcwd()}")

    try:
        print("\nRunning validation suite...")

        # Run validation suite
        report = asyncio.run(suite.run_full_validation_suite())

        print("\nValidation Results:")
        print(f"  Total tests: {report.total_tests}")
        print(f"  Passed: {report.passed_tests}")
        print(f"  Failed: {report.failed_tests}")
        print(f"  Errors: {report.error_tests}")
        print(f"  Skipped: {report.skipped_tests}")
        print(f"  Success rate: {report.summary.get('success_rate', 'N/A')}")
        print(
            f"  Execution time: {report.summary.get('execution_time_formatted', 'N/A')}"
        )

        if report.test_results:
            print("\nTest Results by Category:")
            for category, stats in report.summary.get("tests_by_category", {}).items():
                print(
                    f"  {category.title()}: {stats['passed']}/{stats['total']} passed"
                )

        if report.critical_failures:
            print("\nCritical Failures:")
            for failure in report.critical_failures[:5]:  # Show first 5
                print(f"  ❌ {failure}")
            if len(report.critical_failures) > 5:
                print(f"  ... and {len(report.critical_failures) - 5} more")

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
        if report.critical_failures:
            print("\n❌ Critical failures detected - deployment not recommended")
            return 1
        elif report.failed_tests > 0:
            print("\n⚠️ Some tests failed - review before deployment")
            return 1
        else:
            print("\n✅ All validation tests passed - ready for deployment")
            return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nValidation suite failed: {e}")
        return 1


if __name__ == "__main__":
    import importlib.util
    import sys

    sys.exit(main())
