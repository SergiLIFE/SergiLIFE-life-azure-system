#!/usr/bin/env python3
"""
L.I.F.E. Platform - Critical Component Auditor
Production readiness validation and compliance auditing system

This module provides comprehensive auditing capabilities for critical
components of the L.I.F.E. Platform, ensuring production readiness
and regulatory compliance.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import hashlib
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AuditSeverity(Enum):
    """Audit severity levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AuditStatus(Enum):
    """Audit result status"""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


class AuditResult:
    """Individual audit check result"""

    def __init__(
        self,
        component: str,
        check_name: str,
        status: AuditStatus,
        severity: AuditSeverity,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        remediation: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.component = component
        self.check_name = check_name
        self.status = status
        self.severity = severity
        self.message = message
        self.details = details or {}
        self.remediation = remediation
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "component": self.component,
            "check_name": self.check_name,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "details": self.details,
            "remediation": self.remediation,
            "timestamp": self.timestamp.isoformat(),
        }


class CriticalComponentAuditor:
    """
    Comprehensive auditor for L.I.F.E. Platform critical components

    Performs automated checks on all critical system components to ensure
    production readiness, security compliance, and operational integrity.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.audit_results: List[AuditResult] = []
        self.audit_start_time: Optional[datetime] = None
        self.audit_end_time: Optional[datetime] = None

        # Critical components to audit
        self.critical_components = {
            "core_algorithm": "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
            "autonomous_optimizer": "autonomous_optimizer.py",
            "azure_config": "azure_config.py",
            "azure_functions": "azure_life_functions.py",
            "eeg_processor": "enhanced_eeg_processor.py",
            "venturi_control": "enhanced_venturi_control.py",
            "accuracy_classifier": "accuracy_ensemble_classifier.py",
            "kpi_config": "kpi_config.py",
            "performance_monitor": "performance_monitor.py",
            "production_deployment": "production_deployment_test.py",
        }

        logger.info(
            f"Critical Component Auditor initialized for workspace: {self.workspace_path}"
        )

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Run comprehensive audit of all critical components

        Returns:
            Complete audit report with results and summary
        """
        self.audit_start_time = datetime.now()
        self.audit_results = []

        logger.info("🚀 Starting comprehensive critical component audit...")

        try:
            # Core system checks
            self._audit_file_integrity()
            self._audit_dependencies()
            self._audit_configuration()
            self._audit_security()
            self._audit_performance()
            self._audit_compliance()
            self._audit_deployment_readiness()

            # Generate summary
            summary = self._generate_audit_summary()

            self.audit_end_time = datetime.now()
            duration = self.audit_end_time - self.audit_start_time

            logger.info(f"✅ Audit completed in {duration.total_seconds():.2f} seconds")
            logger.info(
                f"📊 Results: {summary['total_checks']} checks, "
                f"{summary['passed']} passed, {summary['failed']} failed, "
                f"{summary['warnings']} warnings"
            )

            return {
                "audit_metadata": {
                    "start_time": self.audit_start_time.isoformat(),
                    "end_time": self.audit_end_time.isoformat(),
                    "duration_seconds": duration.total_seconds(),
                    "workspace_path": str(self.workspace_path),
                    "auditor_version": "1.0.0",
                },
                "summary": summary,
                "results": [result.to_dict() for result in self.audit_results],
                "recommendations": self._generate_recommendations(),
            }

        except Exception as e:
            logger.error(f"❌ Audit failed with error: {e}")
            return {
                "error": str(e),
                "audit_metadata": {
                    "start_time": (
                        self.audit_start_time.isoformat()
                        if self.audit_start_time
                        else None
                    ),
                    "end_time": datetime.now().isoformat(),
                    "status": "failed",
                },
            }

    def _audit_file_integrity(self):
        """Audit file integrity and existence"""
        logger.info("🔍 Auditing file integrity...")

        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename

            if not filepath.exists():
                self.audit_results.append(
                    AuditResult(
                        component=component_name,
                        check_name="file_existence",
                        status=AuditStatus.FAIL,
                        severity=AuditSeverity.CRITICAL,
                        message=f"Critical component file missing: {filename}",
                        remediation=f"Ensure {filename} exists in workspace",
                    )
                )
                continue

            # Check file size
            file_size = filepath.stat().st_size
            if file_size == 0:
                self.audit_results.append(
                    AuditResult(
                        component=component_name,
                        check_name="file_integrity",
                        status=AuditStatus.FAIL,
                        severity=AuditSeverity.CRITICAL,
                        message=f"Critical component file is empty: {filename}",
                        details={"file_size": file_size},
                        remediation=f"Implement {filename} with required functionality",
                    )
                )
            elif file_size < 1000:  # Suspiciously small
                self.audit_results.append(
                    AuditResult(
                        component=component_name,
                        check_name="file_integrity",
                        status=AuditStatus.WARNING,
                        severity=AuditSeverity.MEDIUM,
                        message=f"Critical component file is very small: {filename}",
                        details={"file_size": file_size},
                        remediation=f"Verify {filename} contains complete implementation",
                    )
                )
            else:
                # Calculate file hash for integrity checking
                file_hash = self._calculate_file_hash(filepath)
                self.audit_results.append(
                    AuditResult(
                        component=component_name,
                        check_name="file_integrity",
                        status=AuditStatus.PASS,
                        severity=AuditSeverity.INFO,
                        message=f"File integrity verified: {filename}",
                        details={"file_size": file_size, "sha256_hash": file_hash},
                    )
                )

    def _audit_dependencies(self):
        """Audit Python dependencies and imports"""
        logger.info("🔍 Auditing dependencies...")

        # Check requirements.txt
        requirements_file = self.workspace_path / "requirements.txt"
        if not requirements_file.exists():
            self.audit_results.append(
                AuditResult(
                    component="dependencies",
                    check_name="requirements_file",
                    status=AuditStatus.FAIL,
                    severity=AuditSeverity.HIGH,
                    message="requirements.txt file missing",
                    remediation="Create requirements.txt with all project dependencies",
                )
            )
        else:
            try:
                with open(requirements_file, "r") as f:
                    requirements = f.read().strip()
                    if not requirements:
                        self.audit_results.append(
                            AuditResult(
                                component="dependencies",
                                check_name="requirements_content",
                                status=AuditStatus.FAIL,
                                severity=AuditSeverity.HIGH,
                                message="requirements.txt is empty",
                                remediation="Add all required Python packages to requirements.txt",
                            )
                        )
                    else:
                        # Count requirements
                        req_lines = [
                            line.strip()
                            for line in requirements.split("\n")
                            if line.strip() and not line.startswith("#")
                        ]
                        self.audit_results.append(
                            AuditResult(
                                component="dependencies",
                                check_name="requirements_content",
                                status=AuditStatus.PASS,
                                severity=AuditSeverity.INFO,
                                message=f"Found {len(req_lines)} dependency declarations",
                                details={"requirements_count": len(req_lines)},
                            )
                        )
            except Exception as e:
                self.audit_results.append(
                    AuditResult(
                        component="dependencies",
                        check_name="requirements_read",
                        status=AuditStatus.ERROR,
                        severity=AuditSeverity.MEDIUM,
                        message=f"Failed to read requirements.txt: {e}",
                        remediation="Ensure requirements.txt is properly formatted",
                    )
                )

        # Test critical imports
        critical_imports = [
            ("numpy", "numerical processing"),
            ("asyncio", "concurrent processing"),
            ("azure", "Azure integration"),
            ("psutil", "system monitoring"),
        ]

        for module_name, purpose in critical_imports:
            try:
                __import__(module_name)
                self.audit_results.append(
                    AuditResult(
                        component="dependencies",
                        check_name=f"import_{module_name}",
                        status=AuditStatus.PASS,
                        severity=AuditSeverity.INFO,
                        message=f"Successfully imported {module_name} ({purpose})",
                    )
                )
            except ImportError:
                self.audit_results.append(
                    AuditResult(
                        component="dependencies",
                        check_name=f"import_{module_name}",
                        status=AuditStatus.WARNING,
                        severity=AuditSeverity.MEDIUM,
                        message=f"Failed to import {module_name} ({purpose})",
                        remediation=f"Install {module_name}: pip install {module_name}",
                    )
                )

    def _audit_configuration(self):
        """Audit configuration files and settings"""
        logger.info("🔍 Auditing configuration...")

        # Check Azure configuration
        azure_config_file = self.workspace_path / "azure_config.py"
        if azure_config_file.exists():
            try:
                # Basic syntax check
                with open(azure_config_file, "r") as f:
                    content = f.read()

                if "AZURE_SUBSCRIPTION_ID" in content and "AZURE_CLIENT_ID" in content:
                    self.audit_results.append(
                        AuditResult(
                            component="configuration",
                            check_name="azure_config",
                            status=AuditStatus.PASS,
                            severity=AuditSeverity.INFO,
                            message="Azure configuration appears complete",
                        )
                    )
                else:
                    self.audit_results.append(
                        AuditResult(
                            component="configuration",
                            check_name="azure_config",
                            status=AuditStatus.WARNING,
                            severity=AuditSeverity.HIGH,
                            message="Azure configuration may be incomplete",
                            remediation="Verify all required Azure credentials are configured",
                        )
                    )
            except Exception as e:
                self.audit_results.append(
                    AuditResult(
                        component="configuration",
                        check_name="azure_config",
                        status=AuditStatus.ERROR,
                        severity=AuditSeverity.HIGH,
                        message=f"Failed to read Azure config: {e}",
                        remediation="Ensure azure_config.py is properly formatted",
                    )
                )

        # Check for environment variables
        required_env_vars = [
            "AZURE_SUBSCRIPTION_ID",
            "AZURE_CLIENT_ID",
            "AZURE_CLIENT_SECRET",
            "AZURE_TENANT_ID",
        ]

        missing_env_vars = []
        for env_var in required_env_vars:
            if not os.getenv(env_var):
                missing_env_vars.append(env_var)

        if missing_env_vars:
            self.audit_results.append(
                AuditResult(
                    component="configuration",
                    check_name="environment_variables",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.HIGH,
                    message=f"Missing environment variables: {', '.join(missing_env_vars)}",
                    details={"missing_vars": missing_env_vars},
                    remediation="Set required Azure environment variables",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="configuration",
                    check_name="environment_variables",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="All required environment variables are set",
                )
            )

    def _audit_security(self):
        """Audit security configurations and practices"""
        logger.info("🔍 Auditing security...")

        # Check for sensitive data in code
        sensitive_patterns = ["password", "secret", "key.*=", "token.*="]

        security_issues = []
        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        content = f.read().lower()

                    for pattern in sensitive_patterns:
                        if pattern.replace(".*=", "=") in content:
                            security_issues.append(f"{filename}: potential {pattern}")
                except Exception:
                    continue

        if security_issues:
            self.audit_results.append(
                AuditResult(
                    component="security",
                    check_name="sensitive_data",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.HIGH,
                    message="Potential sensitive data found in code",
                    details={"issues": security_issues},
                    remediation="Move sensitive data to environment variables or Azure Key Vault",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="security",
                    check_name="sensitive_data",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="No obvious sensitive data found in code",
                )
            )

        # Check file permissions (basic check)
        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename
            if filepath.exists():
                try:
                    # Check if file is readable
                    with open(filepath, "r") as f:
                        f.read(1)
                    self.audit_results.append(
                        AuditResult(
                            component="security",
                            check_name=f"file_permissions_{component_name}",
                            status=AuditStatus.PASS,
                            severity=AuditSeverity.INFO,
                            message=f"File permissions OK: {filename}",
                        )
                    )
                except Exception as e:
                    self.audit_results.append(
                        AuditResult(
                            component="security",
                            check_name=f"file_permissions_{component_name}",
                            status=AuditStatus.ERROR,
                            severity=AuditSeverity.MEDIUM,
                            message=f"File permission issue: {filename} - {e}",
                            remediation=f"Check file permissions for {filename}",
                        )
                    )

    def _audit_performance(self):
        """Audit performance-related configurations"""
        logger.info("🔍 Auditing performance...")

        # Check for performance monitoring
        perf_monitor_file = self.workspace_path / "performance_monitor.py"
        if perf_monitor_file.exists() and perf_monitor_file.stat().st_size > 0:
            self.audit_results.append(
                AuditResult(
                    component="performance",
                    check_name="performance_monitoring",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Performance monitoring system detected",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="performance",
                    check_name="performance_monitoring",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.MEDIUM,
                    message="Performance monitoring system not found",
                    remediation="Implement performance_monitor.py for system monitoring",
                )
            )

        # Check for async/await usage in critical files
        async_usage_found = False
        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                        if "async def" in content or "await " in content:
                            async_usage_found = True
                            break
                except Exception:
                    continue

        if async_usage_found:
            self.audit_results.append(
                AuditResult(
                    component="performance",
                    check_name="async_processing",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Asynchronous processing detected in critical components",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="performance",
                    check_name="async_processing",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.LOW,
                    message="Limited asynchronous processing detected",
                    remediation="Consider implementing async processing for better performance",
                )
            )

    def _audit_compliance(self):
        """Audit regulatory compliance"""
        logger.info("🔍 Auditing compliance...")

        # Check for copyright notices
        copyright_issues = []
        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                        if (
                            "Copyright 2025" not in content
                            or "Sergio Paya Borrull" not in content
                        ):
                            copyright_issues.append(filename)
                except Exception:
                    continue

        if copyright_issues:
            self.audit_results.append(
                AuditResult(
                    component="compliance",
                    check_name="copyright_notices",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.MEDIUM,
                    message="Missing copyright notices in some files",
                    details={"files_without_copyright": copyright_issues},
                    remediation="Add proper copyright notices to all source files",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="compliance",
                    check_name="copyright_notices",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Copyright notices present in all critical files",
                )
            )

        # Check for logging
        logging_usage = False
        for component_name, filename in self.critical_components.items():
            filepath = self.workspace_path / filename
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                        if "logging" in content or "logger" in content:
                            logging_usage = True
                            break
                except Exception:
                    continue

        if logging_usage:
            self.audit_results.append(
                AuditResult(
                    component="compliance",
                    check_name="logging_implementation",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Logging implementation detected",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="compliance",
                    check_name="logging_implementation",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.MEDIUM,
                    message="Limited logging implementation detected",
                    remediation="Implement comprehensive logging for auditability",
                )
            )

    def _audit_deployment_readiness(self):
        """Audit deployment readiness"""
        logger.info("🔍 Auditing deployment readiness...")

        # Check for Azure deployment files
        deployment_files = ["azure.yaml", "Dockerfile", ".github/workflows"]

        missing_deployment_files = []
        for deployment_file in deployment_files:
            if not (self.workspace_path / deployment_file).exists():
                missing_deployment_files.append(deployment_file)

        if missing_deployment_files:
            self.audit_results.append(
                AuditResult(
                    component="deployment",
                    check_name="deployment_files",
                    status=AuditStatus.WARNING,
                    severity=AuditSeverity.HIGH,
                    message="Missing deployment configuration files",
                    details={"missing_files": missing_deployment_files},
                    remediation="Create missing deployment configuration files",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="deployment",
                    check_name="deployment_files",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Deployment configuration files present",
                )
            )

        # Check production deployment test
        prod_test_file = self.workspace_path / "production_deployment_test.py"
        if prod_test_file.exists() and prod_test_file.stat().st_size > 1000:
            self.audit_results.append(
                AuditResult(
                    component="deployment",
                    check_name="production_testing",
                    status=AuditStatus.PASS,
                    severity=AuditSeverity.INFO,
                    message="Production deployment testing system detected",
                )
            )
        else:
            self.audit_results.append(
                AuditResult(
                    component="deployment",
                    check_name="production_testing",
                    status=AuditStatus.FAIL,
                    severity=AuditSeverity.CRITICAL,
                    message="Production deployment testing system missing or incomplete",
                    remediation="Implement comprehensive production_deployment_test.py",
                )
            )

    def _generate_audit_summary(self) -> Dict[str, Any]:
        """Generate audit summary statistics"""
        total_checks = len(self.audit_results)
        passed = sum(1 for r in self.audit_results if r.status == AuditStatus.PASS)
        failed = sum(1 for r in self.audit_results if r.status == AuditStatus.FAIL)
        warnings = sum(1 for r in self.audit_results if r.status == AuditStatus.WARNING)
        errors = sum(1 for r in self.audit_results if r.status == AuditStatus.ERROR)

        # Calculate severity breakdown
        critical_issues = sum(
            1
            for r in self.audit_results
            if r.severity == AuditSeverity.CRITICAL
            and r.status in [AuditStatus.FAIL, AuditStatus.ERROR]
        )

        # Overall health score (0-100)
        health_score = 0
        if total_checks > 0:
            # Weight by severity
            weighted_score = 0
            total_weight = 0
            for result in self.audit_results:
                weight = {
                    AuditSeverity.CRITICAL: 4,
                    AuditSeverity.HIGH: 3,
                    AuditSeverity.MEDIUM: 2,
                    AuditSeverity.LOW: 1,
                    AuditSeverity.INFO: 0.5,
                }.get(result.severity, 1)

                status_score = {
                    AuditStatus.PASS: 1.0,
                    AuditStatus.WARNING: 0.7,
                    AuditStatus.FAIL: 0.3,
                    AuditStatus.ERROR: 0.1,
                    AuditStatus.SKIPPED: 0.5,
                }.get(result.status, 0.5)

                weighted_score += status_score * weight
                total_weight += weight

            if total_weight > 0:
                health_score = (weighted_score / total_weight) * 100

        return {
            "total_checks": total_checks,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "errors": errors,
            "critical_issues": critical_issues,
            "health_score": round(health_score, 1),
            "overall_status": (
                "healthy"
                if health_score >= 80
                else "at_risk" if health_score >= 60 else "critical"
            ),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations based on audit results"""
        recommendations = []

        # Group issues by severity and component
        critical_failures = [
            r
            for r in self.audit_results
            if r.severity == AuditSeverity.CRITICAL
            and r.status in [AuditStatus.FAIL, AuditStatus.ERROR]
        ]

        high_priority = [
            r
            for r in self.audit_results
            if r.severity == AuditSeverity.HIGH
            and r.status in [AuditStatus.FAIL, AuditStatus.WARNING, AuditStatus.ERROR]
        ]

        # Critical recommendations
        if critical_failures:
            recommendations.append(
                "🚨 CRITICAL: Address critical failures immediately:"
            )
            for failure in critical_failures[:5]:  # Top 5
                recommendations.append(f"  • {failure.component}: {failure.message}")
                if failure.remediation:
                    recommendations.append(f"    → {failure.remediation}")

        # High priority recommendations
        if high_priority:
            recommendations.append("\n⚠️ HIGH PRIORITY: Address high-priority issues:")
            for issue in high_priority[:5]:  # Top 5
                recommendations.append(f"  • {issue.component}: {issue.message}")
                if issue.remediation:
                    recommendations.append(f"    → {issue.remediation}")

        # General recommendations
        recommendations.extend(
            [
                "\n📋 GENERAL RECOMMENDATIONS:",
                "  • Run automated tests before deployment",
                "  • Validate Azure configurations in staging environment",
                "  • Monitor performance metrics post-deployment",
                "  • Maintain comprehensive logging for auditability",
                "  • Regularly update dependencies for security",
                "  • Backup critical configurations and data",
            ]
        )

        return recommendations

    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def export_audit_report(self, filepath: str) -> bool:
        """Export audit results to JSON file"""
        try:
            if not self.audit_results:
                logger.warning("No audit results to export")
                return False

            report = self.run_full_audit()
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2, default=str)

            logger.info(f"✅ Audit report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export audit report: {e}")
            return False


# Factory function for easy instantiation
def create_critical_auditor(
    workspace_path: Optional[str] = None,
) -> CriticalComponentAuditor:
    """
    Factory function to create a critical component auditor

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured CriticalComponentAuditor instance
    """
    return CriticalComponentAuditor(workspace_path)


# Command-line interface
def main():
    """Main CLI function for critical component auditing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Critical Component Auditor"
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
        default="audit_report.json",
        help="Output file for audit report (default: audit_report.json)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("🔍 L.I.F.E. Platform - Critical Component Auditor")
    print("=" * 60)

    # Create auditor
    auditor = create_critical_auditor(args.workspace)

    # Run audit
    print("🚀 Running comprehensive audit...")
    report = auditor.run_full_audit()

    if "error" in report:
        print(f"❌ Audit failed: {report['error']}")
        return 1

    # Display summary
    summary = report["summary"]
    print("\n📊 AUDIT SUMMARY:")
    print(f"  Total Checks: {summary['total_checks']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Errors: {summary['errors']}")
    print(f"  Critical Issues: {summary['critical_issues']}")
    print(f"  Health Score: {summary['health_score']}/100")
    print(f"  Overall Status: {summary['overall_status'].upper()}")

    # Export report
    if auditor.export_audit_report(args.output):
        print(f"\n💾 Report exported to: {args.output}")
    else:
        print("\n❌ Failed to export report")

    # Exit with appropriate code
    return 0 if summary["overall_status"] == "healthy" else 1


if __name__ == "__main__":
    sys.exit(main())
