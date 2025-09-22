#!/usr/bin/env python3
"""
L.I.F.E. Platform - Security Scanner
Comprehensive security analysis and vulnerability assessment

This module provides enterprise-grade security scanning capabilities
for the L.I.F.E. Platform, including vulnerability detection,
compliance checking, and security posture assessment.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SecuritySeverity(Enum):
    """Security vulnerability severity levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SecurityCategory(Enum):
    """Security vulnerability categories"""

    INJECTION = "injection"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    ENCRYPTION = "encryption"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    CODE_QUALITY = "code_quality"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"
    DATA_PROTECTION = "data_protection"


class ComplianceStandard(Enum):
    """Compliance standards"""

    HIPAA = "hipaa"
    GDPR = "gdpr"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    NIST = "nist"
    PCI_DSS = "pci_dss"
    AZURE_SECURITY = "azure_security"


@dataclass
class SecurityVulnerability:
    """Security vulnerability finding"""

    vulnerability_id: str
    title: str
    description: str
    severity: SecuritySeverity
    category: SecurityCategory
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: str = ""
    references: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    status: str = "open"  # open, fixed, false_positive, accepted_risk


@dataclass
class SecurityScanResult:
    """Security scan result"""

    scan_id: str
    scan_type: str
    target_path: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    vulnerabilities_found: int = 0
    vulnerabilities_by_severity: Dict[str, int] = field(default_factory=dict)
    vulnerabilities_by_category: Dict[str, int] = field(default_factory=dict)
    compliance_score: float = 100.0
    overall_risk_level: str = "low"
    summary: Dict[str, Any] = field(default_factory=dict)
    detailed_findings: List[SecurityVulnerability] = field(default_factory=list)


@dataclass
class ComplianceCheck:
    """Compliance check result"""

    standard: ComplianceStandard
    requirement: str
    description: str
    status: str  # compliant, non_compliant, not_applicable
    evidence: List[str] = field(default_factory=list)
    remediation: str = ""
    severity: SecuritySeverity = SecuritySeverity.MEDIUM


class SecurityScanner:
    """
    Security Scanner for L.I.F.E. Platform

    Provides comprehensive security analysis including:
    - Code vulnerability scanning
    - Dependency analysis
    - Configuration security
    - Compliance assessment
    - Infrastructure security
    """

    def __init__(self, workspace_path: Optional[str] = None, scan_timeout: int = 300):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.scan_timeout = scan_timeout

        # Security patterns and rules
        self.vulnerability_patterns = self._initialize_vulnerability_patterns()
        self.compliance_checks = self._initialize_compliance_checks()

        # Scan results storage
        self.scan_history: List[SecurityScanResult] = []
        self.known_vulnerabilities: Set[str] = set()

        # Thread pool for parallel scanning
        self.executor = ThreadPoolExecutor(max_workers=4)

        logger.info(
            f"Security Scanner initialized for workspace: {self.workspace_path}"
        )

    def _initialize_vulnerability_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize vulnerability detection patterns"""
        return {
            "hardcoded_secrets": {
                "pattern": r"(?i)(password|secret|key|token)\s*[=:]\s*['\"]([^'\"]{8,})['\"]",
                "severity": SecuritySeverity.HIGH,
                "category": SecurityCategory.CONFIGURATION,
                "description": "Hardcoded secrets or credentials detected",
            },
            "sql_injection": {
                "pattern": r"(?i)(select|insert|update|delete)\s+.*\+.*['\"]|.*format\(.*%.*\)",
                "severity": SecuritySeverity.CRITICAL,
                "category": SecurityCategory.INJECTION,
                "description": "Potential SQL injection vulnerability",
            },
            "xss_vulnerable": {
                "pattern": r"innerHTML\s*[=:]\s*.*\+|document\.write\(.*\+",
                "severity": SecuritySeverity.HIGH,
                "category": SecurityCategory.INJECTION,
                "description": "Potential XSS vulnerability",
            },
            "weak_crypto": {
                "pattern": r"(?i)(md5|sha1)\(|hashlib\.(md5|sha1)",
                "severity": SecuritySeverity.MEDIUM,
                "category": SecurityCategory.ENCRYPTION,
                "description": "Weak cryptographic algorithm usage",
            },
            "insecure_random": {
                "pattern": r"random\.(random|randint|choice)",
                "severity": SecuritySeverity.MEDIUM,
                "category": SecurityCategory.ENCRYPTION,
                "description": "Insecure random number generation",
            },
            "debug_enabled": {
                "pattern": r"DEBUG\s*[=:]\s*True|debug\s*[=:]\s*true",
                "severity": SecuritySeverity.LOW,
                "category": SecurityCategory.CONFIGURATION,
                "description": "Debug mode enabled in production",
            },
            "eval_usage": {
                "pattern": r"\beval\s*\(",
                "severity": SecuritySeverity.HIGH,
                "category": SecurityCategory.CODE_QUALITY,
                "description": "Dangerous eval() function usage",
            },
            "exec_usage": {
                "pattern": r"\bexec\s*\(",
                "severity": SecuritySeverity.HIGH,
                "category": SecurityCategory.CODE_QUALITY,
                "description": "Dangerous exec() function usage",
            },
        }

    def _initialize_compliance_checks(self) -> List[ComplianceCheck]:
        """Initialize compliance checks"""
        return [
            ComplianceCheck(
                standard=ComplianceStandard.HIPAA,
                requirement="Data Encryption",
                description="Sensitive health data must be encrypted at rest and in transit",
                status="not_applicable",
                severity=SecuritySeverity.HIGH,
            ),
            ComplianceCheck(
                standard=ComplianceStandard.GDPR,
                requirement="Data Protection",
                description="Personal data processing must comply with GDPR principles",
                status="not_applicable",
                severity=SecuritySeverity.HIGH,
            ),
            ComplianceCheck(
                standard=ComplianceStandard.AZURE_SECURITY,
                requirement="Azure Key Vault Usage",
                description="Secrets must be stored in Azure Key Vault",
                status="compliant",
                severity=SecuritySeverity.MEDIUM,
            ),
            ComplianceCheck(
                standard=ComplianceStandard.NIST,
                requirement="Access Control",
                description="Implement role-based access control",
                status="compliant",
                severity=SecuritySeverity.MEDIUM,
            ),
            ComplianceCheck(
                standard=ComplianceStandard.ISO27001,
                requirement="Information Security Management",
                description="Implement ISMS with security controls",
                status="compliant",
                severity=SecuritySeverity.MEDIUM,
            ),
        ]

    async def perform_comprehensive_scan(
        self, scan_type: str = "full", include_dependencies: bool = True
    ) -> SecurityScanResult:
        """
        Perform comprehensive security scan

        Args:
            scan_type: Type of scan (full, quick, targeted)
            include_dependencies: Whether to include dependency analysis

        Returns:
            SecurityScanResult with findings
        """
        scan_result = SecurityScanResult(
            scan_id=f"sec_scan_{int(datetime.now().timestamp())}",
            scan_type=scan_type,
            target_path=str(self.workspace_path),
            start_time=datetime.now(),
        )

        logger.info(f"Starting {scan_type} security scan of {self.workspace_path}")

        try:
            # Run different scan types
            if scan_type == "full":
                await self._run_full_scan(scan_result, include_dependencies)
            elif scan_type == "quick":
                await self._run_quick_scan(scan_result)
            elif scan_type == "targeted":
                await self._run_targeted_scan(scan_result)

            # Calculate metrics
            scan_result.end_time = datetime.now()
            scan_result.duration_seconds = (
                scan_result.end_time - scan_result.start_time
            ).total_seconds()

            self._calculate_scan_metrics(scan_result)

            # Generate summary
            scan_result.summary = self._generate_scan_summary(scan_result)

        except Exception as e:
            logger.error(f"Security scan failed: {e}")
            scan_result.summary["error"] = str(e)

        self.scan_history.append(scan_result)
        logger.info(f"Security scan completed in {scan_result.duration_seconds:.2f}s")

        return scan_result

    async def _run_full_scan(
        self, scan_result: SecurityScanResult, include_dependencies: bool
    ) -> None:
        """Run full security scan"""
        # Code analysis
        await self._scan_code_vulnerabilities(scan_result)

        # Configuration analysis
        await self._scan_configuration_security(scan_result)

        # Infrastructure analysis
        await self._scan_infrastructure_security(scan_result)

        # Compliance analysis
        await self._scan_compliance(scan_result)

        if include_dependencies:
            await self._scan_dependencies(scan_result)

    async def _run_quick_scan(self, scan_result: SecurityScanResult) -> None:
        """Run quick security scan"""
        # Only critical and high-severity checks
        await self._scan_code_vulnerabilities(
            scan_result,
            severity_filter=[SecuritySeverity.CRITICAL, SecuritySeverity.HIGH],
        )

    async def _run_targeted_scan(self, scan_result: SecurityScanResult) -> None:
        """Run targeted security scan"""
        # Focus on specific high-risk areas
        await self._scan_configuration_security(scan_result)
        await self._scan_infrastructure_security(scan_result)

    async def _scan_code_vulnerabilities(
        self,
        scan_result: SecurityScanResult,
        severity_filter: Optional[List[SecuritySeverity]] = None,
    ) -> None:
        """Scan code for vulnerabilities"""
        logger.info("Scanning code for vulnerabilities...")

        # Find all Python files
        python_files = list(self.workspace_path.rglob("*.py"))

        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check each vulnerability pattern
                for vuln_name, vuln_config in self.vulnerability_patterns.items():
                    if (
                        severity_filter
                        and vuln_config["severity"] not in severity_filter
                    ):
                        continue

                    matches = re.finditer(vuln_config["pattern"], content, re.MULTILINE)
                    for match in matches:
                        # Create vulnerability finding
                        vulnerability = SecurityVulnerability(
                            vulnerability_id=f"{vuln_name}_{file_path.name}_{match.start()}",
                            title=f"{vuln_config['description']}",
                            description=f"Pattern match for {vuln_name} in {file_path.name}",
                            severity=vuln_config["severity"],
                            category=vuln_config["category"],
                            file_path=str(file_path),
                            line_number=self._get_line_number(content, match.start()),
                            code_snippet=self._extract_code_snippet(
                                content, match.start()
                            ),
                            remediation=self._get_remediation_advice(vuln_name),
                        )

                        scan_result.detailed_findings.append(vulnerability)

            except Exception as e:
                logger.warning(f"Failed to scan {file_path}: {e}")

    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number from character position"""
        return content[:position].count("\n") + 1

    def _extract_code_snippet(
        self, content: str, position: int, context_lines: int = 2
    ) -> str:
        """Extract code snippet around position"""
        lines = content.split("\n")
        line_num = self._get_line_number(content, position)

        start_line = max(0, line_num - context_lines - 1)
        end_line = min(len(lines), line_num + context_lines)

        snippet_lines = []
        for i in range(start_line, end_line):
            marker = ">>> " if i + 1 == line_num else "    "
            snippet_lines.append(f"{marker}{i + 1:4d}: {lines[i]}")

        return "\n".join(snippet_lines)

    def _get_remediation_advice(self, vuln_name: str) -> str:
        """Get remediation advice for vulnerability"""
        advice = {
            "hardcoded_secrets": "Move secrets to environment variables or Azure Key Vault",
            "sql_injection": "Use parameterized queries or ORM with proper sanitization",
            "xss_vulnerable": "Use proper output encoding and Content Security Policy",
            "weak_crypto": "Use SHA-256 or stronger algorithms for hashing",
            "insecure_random": "Use secrets module for cryptographically secure random numbers",
            "debug_enabled": "Disable debug mode in production environments",
            "eval_usage": "Avoid eval() - use safer alternatives like ast.literal_eval",
            "exec_usage": "Avoid exec() - refactor to use proper function calls",
        }
        return advice.get(vuln_name, "Review and fix the security issue")

    async def _scan_configuration_security(
        self, scan_result: SecurityScanResult
    ) -> None:
        """Scan configuration files for security issues"""
        logger.info("Scanning configuration security...")

        config_files = [
            "azure_config.py",
            "azure_functions_config.py",
            "requirements.txt",
            "Dockerfile",
            "azure.yaml",
            ".env",
            "config.json",
            "settings.py",
        ]

        for config_file in config_files:
            file_path = self.workspace_path / config_file
            if not file_path.exists():
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check for insecure configurations
                issues = self._check_configuration_issues(content, config_file)
                for issue in issues:
                    scan_result.detailed_findings.append(issue)

            except Exception as e:
                logger.warning(f"Failed to scan config {config_file}: {e}")

    def _check_configuration_issues(
        self, content: str, filename: str
    ) -> List[SecurityVulnerability]:
        """Check configuration content for security issues"""
        issues = []

        # Check for debug mode
        if re.search(r"DEBUG\s*[=:]\s*True", content, re.IGNORECASE):
            issues.append(
                SecurityVulnerability(
                    vulnerability_id=f"debug_enabled_{filename}",
                    title="Debug Mode Enabled",
                    description="Debug mode is enabled in configuration",
                    severity=SecuritySeverity.MEDIUM,
                    category=SecurityCategory.CONFIGURATION,
                    file_path=filename,
                    remediation="Disable debug mode in production",
                )
            )

        # Check for insecure secrets storage
        if re.search(
            r"(?i)(password|secret|key)\s*[=:]\s*['\"]([^'\"]{4,})['\"]", content
        ):
            issues.append(
                SecurityVulnerability(
                    vulnerability_id=f"hardcoded_secrets_{filename}",
                    title="Hardcoded Secrets",
                    description="Configuration contains hardcoded secrets",
                    severity=SecuritySeverity.HIGH,
                    category=SecurityCategory.CONFIGURATION,
                    file_path=filename,
                    remediation="Use Azure Key Vault or environment variables",
                )
            )

        # Check for weak permissions (if applicable)
        if "permissions" in content.lower():
            if re.search(r"777|rwxrwxrwx", content):
                issues.append(
                    SecurityVulnerability(
                        vulnerability_id=f"weak_permissions_{filename}",
                        title="Weak File Permissions",
                        description="Overly permissive file permissions detected",
                        severity=SecuritySeverity.MEDIUM,
                        category=SecurityCategory.CONFIGURATION,
                        file_path=filename,
                        remediation="Use principle of least privilege for permissions",
                    )
                )

        return issues

    async def _scan_infrastructure_security(
        self, scan_result: SecurityScanResult
    ) -> None:
        """Scan infrastructure configuration for security issues"""
        logger.info("Scanning infrastructure security...")

        # Check Azure configurations
        azure_files = ["azure.yaml", "azure_config.py", "AZURE_OIDC_SETUP.md"]

        for azure_file in azure_files:
            file_path = self.workspace_path / azure_file
            if not file_path.exists():
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check Azure security configurations
                issues = self._check_azure_security(content, azure_file)
                for issue in issues:
                    scan_result.detailed_findings.append(issue)

            except Exception as e:
                logger.warning(f"Failed to scan Azure config {azure_file}: {e}")

    def _check_azure_security(
        self, content: str, filename: str
    ) -> List[SecurityVulnerability]:
        """Check Azure configuration for security issues"""
        issues = []

        # Check for missing encryption
        if "storage" in content.lower() and "encrypt" not in content.lower():
            issues.append(
                SecurityVulnerability(
                    vulnerability_id=f"missing_encryption_{filename}",
                    title="Missing Storage Encryption",
                    description="Azure storage may not have encryption enabled",
                    severity=SecuritySeverity.HIGH,
                    category=SecurityCategory.INFRASTRUCTURE,
                    file_path=filename,
                    remediation="Enable Azure Storage encryption at rest",
                )
            )

        # Check for public access
        if re.search(r"public.*access|allow.*public", content, re.IGNORECASE):
            issues.append(
                SecurityVulnerability(
                    vulnerability_id=f"public_access_{filename}",
                    title="Potential Public Access",
                    description="Configuration may allow public access",
                    severity=SecuritySeverity.HIGH,
                    category=SecurityCategory.INFRASTRUCTURE,
                    file_path=filename,
                    remediation="Restrict access to private networks only",
                )
            )

        # Check for missing RBAC
        if "role" not in content.lower() and "rbac" not in content.lower():
            issues.append(
                SecurityVulnerability(
                    vulnerability_id=f"missing_rbac_{filename}",
                    title="Missing RBAC Configuration",
                    description="Role-based access control may not be configured",
                    severity=SecuritySeverity.MEDIUM,
                    category=SecurityCategory.INFRASTRUCTURE,
                    file_path=filename,
                    remediation="Implement Azure RBAC for access control",
                )
            )

        return issues

    async def _scan_compliance(self, scan_result: SecurityScanResult) -> None:
        """Scan for compliance with security standards"""
        logger.info("Scanning compliance...")

        # Update compliance check status based on findings
        for check in self.compliance_checks:
            if check.standard == ComplianceStandard.AZURE_SECURITY:
                # Check if Azure Key Vault is being used
                key_vault_usage = self._check_key_vault_usage()
                if not key_vault_usage:
                    check.status = "non_compliant"
                    check.remediation = (
                        "Implement Azure Key Vault for secrets management"
                    )

    def _check_key_vault_usage(self) -> bool:
        """Check if Azure Key Vault is being used"""
        # Look for Key Vault references in code
        python_files = list(self.workspace_path.rglob("*.py"))
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "keyvault" in content.lower() or "key_vault" in content.lower():
                        return True
            except Exception:
                continue
        return False

    async def _scan_dependencies(self, scan_result: SecurityScanResult) -> None:
        """Scan dependencies for known vulnerabilities"""
        logger.info("Scanning dependencies...")

        requirements_file = self.workspace_path / "requirements.txt"
        if not requirements_file.exists():
            return

        try:
            with open(requirements_file, "r") as f:
                dependencies = f.read().split("\n")

            # Check for known vulnerable packages (simplified check)
            vulnerable_packages = {"insecure-package": "1.0.0", "old-crypto": "2.1.0"}

            for dep in dependencies:
                if not dep.strip() or dep.startswith("#"):
                    continue

                package_name = dep.split("==")[0].strip()
                if package_name in vulnerable_packages:
                    scan_result.detailed_findings.append(
                        SecurityVulnerability(
                            vulnerability_id=f"vulnerable_dependency_{package_name}",
                            title=f"Vulnerable Dependency: {package_name}",
                            description=f"Package {package_name} has known security vulnerabilities",
                            severity=SecuritySeverity.HIGH,
                            category=SecurityCategory.DEPENDENCY,
                            remediation=f"Update {package_name} to latest secure version",
                        )
                    )

        except Exception as e:
            logger.warning(f"Failed to scan dependencies: {e}")

    def _calculate_scan_metrics(self, scan_result: SecurityScanResult) -> None:
        """Calculate scan result metrics"""
        findings = scan_result.detailed_findings

        # Count by severity
        severity_counts = {}
        for severity in SecuritySeverity:
            severity_counts[severity.value] = 0

        # Count by category
        category_counts = {}
        for category in SecurityCategory:
            category_counts[category.value] = 0

        for finding in findings:
            severity_counts[finding.severity.value] += 1
            category_counts[finding.category.value] += 1

        scan_result.vulnerabilities_found = len(findings)
        scan_result.vulnerabilities_by_severity = severity_counts
        scan_result.vulnerabilities_by_category = category_counts

        # Calculate compliance score
        scan_result.compliance_score = self._calculate_compliance_score(findings)

        # Determine overall risk level
        scan_result.overall_risk_level = self._calculate_risk_level(findings)

    def _calculate_compliance_score(
        self, findings: List[SecurityVulnerability]
    ) -> float:
        """Calculate compliance score based on findings"""
        if not findings:
            return 100.0

        # Weight findings by severity
        severity_weights = {
            SecuritySeverity.CRITICAL: 10,
            SecuritySeverity.HIGH: 7,
            SecuritySeverity.MEDIUM: 4,
            SecuritySeverity.LOW: 2,
            SecuritySeverity.INFO: 1,
        }

        total_weight = 0
        for finding in findings:
            total_weight += severity_weights.get(finding.severity, 1)

        # Convert to score (higher weight = lower score)
        score = max(0, 100 - (total_weight * 2))
        return round(score, 1)

    def _calculate_risk_level(self, findings: List[SecurityVulnerability]) -> str:
        """Calculate overall risk level"""
        critical_count = sum(
            1 for f in findings if f.severity == SecuritySeverity.CRITICAL
        )
        high_count = sum(1 for f in findings if f.severity == SecuritySeverity.HIGH)

        if critical_count > 0:
            return "critical"
        elif high_count > 2:
            return "high"
        elif high_count > 0 or len(findings) > 5:
            return "medium"
        elif len(findings) > 0:
            return "low"
        else:
            return "minimal"

    def _generate_scan_summary(self, scan_result: SecurityScanResult) -> Dict[str, Any]:
        """Generate scan summary"""
        return {
            "scan_type": scan_result.scan_type,
            "total_files_scanned": len(list(self.workspace_path.rglob("*.py"))),
            "vulnerabilities_found": scan_result.vulnerabilities_found,
            "compliance_score": scan_result.compliance_score,
            "risk_level": scan_result.overall_risk_level,
            "scan_duration": scan_result.duration_seconds,
            "top_categories": sorted(
                scan_result.vulnerabilities_by_category.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:3],
        }

    def get_scan_history(self, limit: int = 10) -> List[SecurityScanResult]:
        """Get scan history"""
        return self.scan_history[-limit:]

    def get_vulnerability_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get vulnerability trends over time"""
        cutoff_date = datetime.now() - timedelta(days=days)

        relevant_scans = [
            scan for scan in self.scan_history if scan.start_time >= cutoff_date
        ]

        trends = {
            "period_days": days,
            "total_scans": len(relevant_scans),
            "vulnerability_trend": [],
            "compliance_trend": [],
        }

        for scan in sorted(relevant_scans, key=lambda x: x.start_time):
            trends["vulnerability_trend"].append(
                {
                    "date": scan.start_time.date().isoformat(),
                    "count": scan.vulnerabilities_found,
                }
            )
            trends["compliance_trend"].append(
                {
                    "date": scan.start_time.date().isoformat(),
                    "score": scan.compliance_score,
                }
            )

        return trends

    def export_scan_report(
        self, scan_result: SecurityScanResult, filepath: str
    ) -> bool:
        """Export security scan report"""
        try:
            export_data = {
                "scan_id": scan_result.scan_id,
                "scan_type": scan_result.scan_type,
                "target_path": scan_result.target_path,
                "start_time": scan_result.start_time.isoformat(),
                "end_time": (
                    scan_result.end_time.isoformat() if scan_result.end_time else None
                ),
                "duration_seconds": scan_result.duration_seconds,
                "summary": scan_result.summary,
                "vulnerabilities_by_severity": scan_result.vulnerabilities_by_severity,
                "vulnerabilities_by_category": scan_result.vulnerabilities_by_category,
                "findings": [
                    {
                        "id": finding.vulnerability_id,
                        "title": finding.title,
                        "severity": finding.severity.value,
                        "category": finding.category.value,
                        "file": finding.file_path,
                        "line": finding.line_number,
                        "remediation": finding.remediation,
                    }
                    for finding in scan_result.detailed_findings
                ],
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Security scan report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export scan report: {e}")
            return False


# Factory function for easy instantiation
def create_security_scanner(
    workspace_path: Optional[str] = None, scan_timeout: int = 300
) -> SecurityScanner:
    """
    Factory function to create security scanner

    Args:
        workspace_path: Path to workspace directory
        scan_timeout: Scan timeout in seconds

    Returns:
        Configured SecurityScanner instance
    """
    return SecurityScanner(workspace_path=workspace_path, scan_timeout=scan_timeout)


# Command-line interface
def main():
    """Main CLI function for security scanning"""
    import argparse

    parser = argparse.ArgumentParser(description="L.I.F.E. Platform Security Scanner")
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--scan-type",
        "-t",
        choices=["full", "quick", "targeted"],
        default="full",
        help="Type of security scan to perform",
    )
    parser.add_argument(
        "--no-dependencies",
        action="store_true",
        help="Skip dependency vulnerability scanning",
    )
    parser.add_argument(
        "--export", "-e", help="Export scan results to specified JSON file"
    )
    parser.add_argument(
        "--timeout", type=int, default=300, help="Scan timeout in seconds"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create security scanner
    scanner = create_security_scanner(
        workspace_path=args.workspace, scan_timeout=args.timeout
    )

    print("L.I.F.E. Platform - Security Scanner")
    print("=" * 40)

    try:
        # Perform scan
        print(f"Performing {args.scan_type} security scan...")

        scan_result = asyncio.run(
            scanner.perform_comprehensive_scan(
                scan_type=args.scan_type, include_dependencies=not args.no_dependencies
            )
        )

        print("\nScan Results:")
        print(f"  Scan ID: {scan_result.scan_id}")
        print(f"  Type: {scan_result.scan_type}")
        print(f"  Duration: {scan_result.duration_seconds:.2f}s")
        print(f"  Vulnerabilities Found: {scan_result.vulnerabilities_found}")
        print(f"  Compliance Score: {scan_result.compliance_score:.1f}/100")
        print(f"  Risk Level: {scan_result.overall_risk_level}")

        if scan_result.vulnerabilities_found > 0:
            print("\nVulnerabilities by Severity:")
            for severity, count in scan_result.vulnerabilities_by_severity.items():
                if count > 0:
                    print(f"  {severity.capitalize()}: {count}")

            print("\nTop Findings:")
            for finding in scan_result.detailed_findings[:5]:  # Show first 5
                print(f"  [{finding.severity.value.upper()}] {finding.title}")
                if finding.file_path:
                    print(f"    File: {finding.file_path}")
                if finding.remediation:
                    print(f"    Fix: {finding.remediation}")
                print()

        if args.export:
            if scanner.export_scan_report(scan_result, args.export):
                print(f"\nScan report exported to {args.export}")
            else:
                print("\nFailed to export scan report")
                return 1

        # Exit with appropriate code based on findings
        if scan_result.overall_risk_level in ["critical", "high"]:
            print("\n⚠️  HIGH RISK: Critical security issues found!")
            return 1
        elif scan_result.overall_risk_level == "medium":
            print("\n⚠️  MEDIUM RISK: Security improvements recommended")
            return 0
        else:
            print("\n✅ Security scan passed")
            return 0

    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        return 1
    except Exception as e:
        print(f"\nSecurity scan failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
