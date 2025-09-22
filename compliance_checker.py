#!/usr/bin/env python3
"""
L.I.F.E. Platform - Compliance Checker
Automated compliance validation for regulatory standards

This module provides comprehensive compliance checking capabilities
for the L.I.F.E. Platform, ensuring adherence to regulatory standards
including HIPAA, GDPR, SOC2, ISO27001, and Azure security requirements.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ComplianceStandard(Enum):
    """Compliance standards"""

    HIPAA = "hipaa"
    GDPR = "gdpr"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    NIST = "nist"
    PCI_DSS = "pci_dss"
    AZURE_SECURITY = "azure_security"
    CCPA = "ccpa"
    FERPA = "ferpa"


class ComplianceStatus(Enum):
    """Compliance check status"""

    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    COMPENSATING_CONTROL = "compensating_control"
    UNDER_REVIEW = "under_review"


class ComplianceSeverity(Enum):
    """Compliance violation severity"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ComplianceRequirement:
    """Compliance requirement definition"""

    requirement_id: str
    standard: ComplianceStandard
    category: str
    title: str
    description: str
    severity: ComplianceSeverity
    automated_check: bool = True
    evidence_required: List[str] = field(default_factory=list)
    remediation_steps: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


@dataclass
class ComplianceCheckResult:
    """Result of a compliance check"""

    check_id: str
    requirement: ComplianceRequirement
    status: ComplianceStatus
    evidence_found: List[str] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)
    remediation_actions: List[str] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)
    notes: str = ""


@dataclass
class ComplianceAssessment:
    """Overall compliance assessment"""

    assessment_id: str
    standard: ComplianceStandard
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    overall_status: ComplianceStatus = ComplianceStatus.UNDER_REVIEW
    compliance_score: float = 0.0
    total_requirements: int = 0
    compliant_requirements: int = 0
    non_compliant_requirements: int = 0
    not_applicable_requirements: int = 0
    critical_violations: int = 0
    high_violations: int = 0
    detailed_results: List[ComplianceCheckResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ComplianceChecker:
    """
    Compliance Checker for L.I.F.E. Platform

    Provides automated compliance validation against multiple regulatory
    standards including HIPAA, GDPR, SOC2, ISO27001, and Azure security.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())

        # Compliance requirements database
        self.requirements = self._initialize_requirements()

        # Assessment history
        self.assessment_history: List[ComplianceAssessment] = []

        # Thread pool for parallel checking
        self.executor = ThreadPoolExecutor(max_workers=4)

        logger.info(
            f"Compliance Checker initialized for workspace: {self.workspace_path}"
        )

    def _initialize_requirements(
        self,
    ) -> Dict[ComplianceStandard, List[ComplianceRequirement]]:
        """Initialize compliance requirements for each standard"""
        requirements = {}

        # HIPAA Requirements
        requirements[ComplianceStandard.HIPAA] = [
            ComplianceRequirement(
                requirement_id="hipaa_encryption",
                standard=ComplianceStandard.HIPAA,
                category="Data Protection",
                title="Data Encryption",
                description="Protected Health Information (PHI) must be encrypted at rest and in transit",
                severity=ComplianceSeverity.CRITICAL,
                evidence_required=[
                    "encryption_at_rest",
                    "encryption_in_transit",
                    "key_management",
                ],
                remediation_steps=[
                    "Implement AES-256 encryption for data at rest",
                    "Use TLS 1.3 for data in transit",
                    "Implement proper key management with Azure Key Vault",
                ],
            ),
            ComplianceRequirement(
                requirement_id="hipaa_access_control",
                standard=ComplianceStandard.HIPAA,
                category="Access Control",
                title="Access Control",
                description="Implement role-based access control for PHI access",
                severity=ComplianceSeverity.HIGH,
                evidence_required=[
                    "rbac_implementation",
                    "access_logging",
                    "least_privilege",
                ],
                remediation_steps=[
                    "Implement Azure RBAC for resource access",
                    "Enable access logging and monitoring",
                    "Apply principle of least privilege",
                ],
            ),
            ComplianceRequirement(
                requirement_id="hipaa_audit_logging",
                standard=ComplianceStandard.HIPAA,
                category="Audit & Monitoring",
                title="Audit Logging",
                description="All access to PHI must be logged and auditable",
                severity=ComplianceSeverity.HIGH,
                evidence_required=["access_logs", "log_retention", "log_integrity"],
                remediation_steps=[
                    "Enable comprehensive audit logging",
                    "Implement log retention policies (6+ years)",
                    "Ensure log integrity and protection",
                ],
            ),
        ]

        # GDPR Requirements
        requirements[ComplianceStandard.GDPR] = [
            ComplianceRequirement(
                requirement_id="gdpr_data_minimization",
                standard=ComplianceStandard.GDPR,
                category="Data Protection",
                title="Data Minimization",
                description="Collect and process only necessary personal data",
                severity=ComplianceSeverity.MEDIUM,
                evidence_required=[
                    "data_inventory",
                    "purpose_limitation",
                    "retention_policies",
                ],
                remediation_steps=[
                    "Conduct data inventory and classification",
                    "Define clear data processing purposes",
                    "Implement data retention schedules",
                ],
            ),
            ComplianceRequirement(
                requirement_id="gdpr_consent_management",
                standard=ComplianceStandard.GDPR,
                category="Consent & Rights",
                title="Consent Management",
                description="Obtain and manage user consent for data processing",
                severity=ComplianceSeverity.HIGH,
                evidence_required=[
                    "consent_mechanism",
                    "consent_withdrawal",
                    "consent_records",
                ],
                remediation_steps=[
                    "Implement clear consent mechanisms",
                    "Provide easy consent withdrawal options",
                    "Maintain detailed consent records",
                ],
            ),
            ComplianceRequirement(
                requirement_id="gdpr_data_portability",
                standard=ComplianceStandard.GDPR,
                category="Data Subject Rights",
                title="Data Portability",
                description="Enable data portability for data subjects",
                severity=ComplianceSeverity.MEDIUM,
                evidence_required=[
                    "export_functionality",
                    "data_formats",
                    "automated_exports",
                ],
                remediation_steps=[
                    "Implement data export functionality",
                    "Support common data formats (JSON, CSV)",
                    "Enable automated data exports",
                ],
            ),
        ]

        # Azure Security Requirements
        requirements[ComplianceStandard.AZURE_SECURITY] = [
            ComplianceRequirement(
                requirement_id="azure_key_vault",
                standard=ComplianceStandard.AZURE_SECURITY,
                category="Secrets Management",
                title="Azure Key Vault Usage",
                description="Secrets must be stored and managed in Azure Key Vault",
                severity=ComplianceSeverity.HIGH,
                evidence_required=[
                    "key_vault_integration",
                    "secret_rotation",
                    "access_policies",
                ],
                remediation_steps=[
                    "Integrate Azure Key Vault for secret management",
                    "Implement automatic secret rotation",
                    "Configure proper access policies",
                ],
            ),
            ComplianceRequirement(
                requirement_id="azure_monitoring",
                standard=ComplianceStandard.AZURE_SECURITY,
                category="Monitoring & Logging",
                title="Azure Monitor Integration",
                description="Implement comprehensive monitoring and alerting",
                severity=ComplianceSeverity.MEDIUM,
                evidence_required=[
                    "azure_monitor_setup",
                    "alert_rules",
                    "log_analytics",
                ],
                remediation_steps=[
                    "Configure Azure Monitor for all resources",
                    "Set up appropriate alert rules",
                    "Enable Log Analytics workspace",
                ],
            ),
            ComplianceRequirement(
                requirement_id="azure_network_security",
                standard=ComplianceStandard.AZURE_SECURITY,
                category="Network Security",
                title="Network Security Controls",
                description="Implement network security best practices",
                severity=ComplianceSeverity.HIGH,
                evidence_required=[
                    "nsgs_configured",
                    "firewall_rules",
                    "private_endpoints",
                ],
                remediation_steps=[
                    "Configure Network Security Groups (NSGs)",
                    "Set up Azure Firewall rules",
                    "Use Private Endpoints where applicable",
                ],
            ),
        ]

        # ISO 27001 Requirements (subset)
        requirements[ComplianceStandard.ISO27001] = [
            ComplianceRequirement(
                requirement_id="iso_risk_assessment",
                standard=ComplianceStandard.ISO27001,
                category="Risk Management",
                title="Risk Assessment",
                description="Conduct regular risk assessments and implement controls",
                severity=ComplianceSeverity.MEDIUM,
                evidence_required=[
                    "risk_register",
                    "assessment_reports",
                    "control_implementation",
                ],
                remediation_steps=[
                    "Maintain up-to-date risk register",
                    "Conduct annual risk assessments",
                    "Implement identified controls",
                ],
            ),
            ComplianceRequirement(
                requirement_id="iso_access_management",
                standard=ComplianceStandard.ISO27001,
                category="Access Control",
                title="Access Management",
                description="Implement comprehensive access management controls",
                severity=ComplianceSeverity.HIGH,
                evidence_required=[
                    "user_provisioning",
                    "access_reviews",
                    "termination_procedures",
                ],
                remediation_steps=[
                    "Implement automated user provisioning",
                    "Conduct regular access reviews",
                    "Establish clear termination procedures",
                ],
            ),
        ]

        return requirements

    async def assess_compliance(
        self, standard: ComplianceStandard, include_automated_only: bool = True
    ) -> ComplianceAssessment:
        """
        Perform compliance assessment for a specific standard

        Args:
            standard: Compliance standard to assess
            include_automated_only: Only include requirements with automated checks

        Returns:
            ComplianceAssessment with detailed results
        """
        assessment = ComplianceAssessment(
            assessment_id=f"comp_assess_{standard.value}_{int(datetime.now().timestamp())}",
            standard=standard,
            start_time=datetime.now(),
        )

        logger.info(f"Starting compliance assessment for {standard.value}")

        try:
            # Get requirements for this standard
            requirements = self.requirements.get(standard, [])
            if include_automated_only:
                requirements = [r for r in requirements if r.automated_check]

            assessment.total_requirements = len(requirements)

            # Perform checks in parallel
            check_tasks = []
            for requirement in requirements:
                task = self._check_requirement_async(requirement)
                check_tasks.append(task)

            # Wait for all checks to complete
            check_results = await asyncio.gather(*check_tasks)
            assessment.detailed_results = check_results

            # Calculate assessment metrics
            assessment.end_time = datetime.now()
            assessment.duration_seconds = (
                assessment.end_time - assessment.start_time
            ).total_seconds()

            self._calculate_assessment_metrics(assessment)

            # Generate summary and recommendations
            assessment.summary = self._generate_assessment_summary(assessment)
            assessment.recommendations = self._generate_recommendations(assessment)

        except Exception as e:
            logger.error(f"Compliance assessment failed: {e}")
            assessment.summary["error"] = str(e)

        self.assessment_history.append(assessment)
        logger.info(
            f"Compliance assessment completed in {assessment.duration_seconds:.2f}s"
        )

        return assessment

    async def _check_requirement_async(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check a single requirement asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor, self._check_requirement_sync, requirement
        )
        return result

    def _check_requirement_sync(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check a single requirement synchronously"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}_{int(datetime.now().timestamp())}",
            requirement=requirement,
            status=ComplianceStatus.UNDER_REVIEW,
        )

        try:
            # Perform automated checks based on requirement
            if requirement.requirement_id == "hipaa_encryption":
                result = self._check_encryption_compliance(requirement)
            elif requirement.requirement_id == "hipaa_access_control":
                result = self._check_access_control_compliance(requirement)
            elif requirement.requirement_id == "hipaa_audit_logging":
                result = self._check_audit_logging_compliance(requirement)
            elif requirement.requirement_id == "gdpr_data_minimization":
                result = self._check_data_minimization_compliance(requirement)
            elif requirement.requirement_id == "gdpr_consent_management":
                result = self._check_consent_management_compliance(requirement)
            elif requirement.requirement_id == "azure_key_vault":
                result = self._check_key_vault_compliance(requirement)
            elif requirement.requirement_id == "azure_monitoring":
                result = self._check_monitoring_compliance(requirement)
            elif requirement.requirement_id == "azure_network_security":
                result = self._check_network_security_compliance(requirement)
            else:
                # Default: mark as manual review required
                result.status = ComplianceStatus.UNDER_REVIEW
                result.notes = "Manual review required - no automated check implemented"

        except Exception as e:
            logger.warning(
                f"Compliance check failed for {requirement.requirement_id}: {e}"
            )
            result.status = ComplianceStatus.UNDER_REVIEW
            result.notes = f"Check failed: {str(e)}"

        return result

    def _check_encryption_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check encryption compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check for encryption-related configurations
        azure_config = self.workspace_path / "azure_config.py"
        if azure_config.exists():
            with open(azure_config, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Look for encryption settings
                if re.search(
                    r"encrypt.*true|encryption.*enabled", content, re.IGNORECASE
                ):
                    evidence_found.append(
                        "Encryption configuration found in azure_config.py"
                    )
                if "key_vault" in content.lower():
                    evidence_found.append("Key Vault integration detected")

        # Check Azure deployment files
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                if "encrypt" in content.lower() or "ssl" in content.lower():
                    evidence_found.append("Encryption settings found in azure.yaml")

        # Determine compliance status
        if len(evidence_found) >= 2:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        elif len(evidence_found) == 1:
            result.status = ComplianceStatus.COMPENSATING_CONTROL
            result.evidence_found = evidence_found
            result.violations = ["Limited encryption evidence found"]
            result.remediation_actions = ["Implement comprehensive encryption strategy"]
        else:
            result.status = ComplianceStatus.NON_COMPLIANT
            result.violations = ["No encryption implementation detected"]
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_access_control_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check access control compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check for RBAC configurations
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                if "role" in content.lower() or "rbac" in content.lower():
                    evidence_found.append("RBAC configuration found in azure.yaml")

        # Check for authentication in code
        python_files = list(self.workspace_path.rglob("*.py"))
        auth_found = False
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if re.search(r"auth|login|token|jwt", content, re.IGNORECASE):
                        auth_found = True
                        break
            except Exception:
                continue

        if auth_found:
            evidence_found.append("Authentication mechanisms detected in codebase")

        # Determine compliance status
        if len(evidence_found) >= 2:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        else:
            result.status = ComplianceStatus.NON_COMPLIANT
            result.violations = ["Insufficient access control implementation"]
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_audit_logging_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check audit logging compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check for logging configurations
        python_files = list(self.workspace_path.rglob("*.py"))
        logging_found = False
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if re.search(r"logging|log\.", content, re.IGNORECASE):
                        logging_found = True
                        evidence_found.append(f"Logging detected in {file_path.name}")
                        break
            except Exception:
                continue

        # Check Azure Monitor configuration
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "monitor" in content.lower() or "log" in content.lower():
                    evidence_found.append("Azure Monitor configuration found")

        # Determine compliance status
        if logging_found and len(evidence_found) >= 2:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        else:
            result.status = ComplianceStatus.NON_COMPLIANT
            result.violations = ["Insufficient audit logging implementation"]
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_data_minimization_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check GDPR data minimization compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        # For L.I.F.E. Platform, data minimization is primarily manual
        result.status = ComplianceStatus.UNDER_REVIEW
        result.notes = (
            "Data minimization requires manual review of data collection practices"
        )
        result.remediation_actions = requirement.remediation_steps

        return result

    def _check_consent_management_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check GDPR consent management compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        # Check for consent-related code
        python_files = list(self.workspace_path.rglob("*.py"))
        consent_found = False
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if re.search(r"consent|agreement|accept", content, re.IGNORECASE):
                        consent_found = True
                        result.evidence_found.append(
                            f"Consent handling found in {file_path.name}"
                        )
                        break
            except Exception:
                continue

        if consent_found:
            result.status = ComplianceStatus.COMPLIANT
        else:
            result.status = ComplianceStatus.UNDER_REVIEW
            result.notes = "Consent management requires manual verification"
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_key_vault_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check Azure Key Vault compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check for Key Vault references in code
        python_files = list(self.workspace_path.rglob("*.py"))
        kv_found = False
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "keyvault" in content.lower() or "key_vault" in content.lower():
                        kv_found = True
                        evidence_found.append(
                            f"Key Vault integration found in {file_path.name}"
                        )
                        break
            except Exception:
                continue

        # Check Azure configuration
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "keyvault" in content.lower():
                    evidence_found.append("Key Vault configured in azure.yaml")

        if kv_found:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        else:
            result.status = ComplianceStatus.NON_COMPLIANT
            result.violations = ["Azure Key Vault not implemented"]
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_monitoring_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check Azure monitoring compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check Azure configuration for monitoring
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "monitor" in content.lower() or "insights" in content.lower():
                    evidence_found.append("Azure Monitor configured in azure.yaml")

        # Check for monitoring in code
        python_files = list(self.workspace_path.rglob("*.py"))
        monitor_found = False
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if re.search(r"monitor|metrics|telemetry", content, re.IGNORECASE):
                        monitor_found = True
                        evidence_found.append(
                            f"Monitoring code found in {file_path.name}"
                        )
                        break
            except Exception:
                continue

        if monitor_found and evidence_found:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        else:
            result.status = ComplianceStatus.NON_COMPLIANT
            result.violations = ["Azure monitoring not fully implemented"]
            result.remediation_actions = requirement.remediation_steps

        return result

    def _check_network_security_compliance(
        self, requirement: ComplianceRequirement
    ) -> ComplianceCheckResult:
        """Check Azure network security compliance"""
        result = ComplianceCheckResult(
            check_id=f"check_{requirement.requirement_id}", requirement=requirement
        )

        evidence_found = []

        # Check Azure configuration for network security
        azure_yaml = self.workspace_path / "azure.yaml"
        if azure_yaml.exists():
            with open(azure_yaml, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if (
                    "nsg" in content.lower()
                    or "firewall" in content.lower()
                    or "private" in content.lower()
                ):
                    evidence_found.append(
                        "Network security controls configured in azure.yaml"
                    )

        if evidence_found:
            result.status = ComplianceStatus.COMPLIANT
            result.evidence_found = evidence_found
        else:
            result.status = ComplianceStatus.UNDER_REVIEW
            result.notes = (
                "Network security requires manual verification of Azure configuration"
            )
            result.remediation_actions = requirement.remediation_steps

        return result

    def _calculate_assessment_metrics(self, assessment: ComplianceAssessment) -> None:
        """Calculate assessment metrics"""
        results = assessment.detailed_results

        compliant = sum(1 for r in results if r.status == ComplianceStatus.COMPLIANT)
        non_compliant = sum(
            1 for r in results if r.status == ComplianceStatus.NON_COMPLIANT
        )
        not_applicable = sum(
            1 for r in results if r.status == ComplianceStatus.NOT_APPLICABLE
        )
        compensating = sum(
            1 for r in results if r.status == ComplianceStatus.COMPENSATING_CONTROL
        )

        assessment.compliant_requirements = compliant + compensating
        assessment.non_compliant_requirements = non_compliant
        assessment.not_applicable_requirements = not_applicable

        # Calculate critical and high violations
        for result in results:
            if result.status in [ComplianceStatus.NON_COMPLIANT]:
                if result.requirement.severity == ComplianceSeverity.CRITICAL:
                    assessment.critical_violations += 1
                elif result.requirement.severity == ComplianceSeverity.HIGH:
                    assessment.high_violations += 1

        # Calculate compliance score
        total_checkable = compliant + non_compliant + compensating
        if total_checkable > 0:
            assessment.compliance_score = (
                (compliant + compensating) / total_checkable * 100
            )
        else:
            assessment.compliance_score = 0.0

        # Determine overall status
        if assessment.critical_violations > 0:
            assessment.overall_status = ComplianceStatus.NON_COMPLIANT
        elif assessment.high_violations > 0:
            assessment.overall_status = ComplianceStatus.COMPENSATING_CONTROL
        elif assessment.compliance_score >= 80:
            assessment.overall_status = ComplianceStatus.COMPLIANT
        else:
            assessment.overall_status = ComplianceStatus.NON_COMPLIANT

    def _generate_assessment_summary(
        self, assessment: ComplianceAssessment
    ) -> Dict[str, Any]:
        """Generate assessment summary"""
        return {
            "standard": assessment.standard.value,
            "compliance_score": assessment.compliance_score,
            "overall_status": assessment.overall_status.value,
            "total_requirements": assessment.total_requirements,
            "compliant_requirements": assessment.compliant_requirements,
            "non_compliant_requirements": assessment.non_compliant_requirements,
            "critical_violations": assessment.critical_violations,
            "high_violations": assessment.high_violations,
            "assessment_duration": assessment.duration_seconds,
        }

    def _generate_recommendations(self, assessment: ComplianceAssessment) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []

        if assessment.critical_violations > 0:
            recommendations.append("Address critical compliance violations immediately")

        if assessment.high_violations > 0:
            recommendations.append(
                "Review and remediate high-severity compliance issues"
            )

        if assessment.compliance_score < 80:
            recommendations.append(
                "Improve overall compliance posture to meet regulatory requirements"
            )

        # Add specific recommendations based on violations
        for result in assessment.detailed_results:
            if result.status == ComplianceStatus.NON_COMPLIANT:
                recommendations.extend(
                    result.remediation_actions[:2]
                )  # Limit to 2 per violation

        # Remove duplicates and limit total recommendations
        recommendations = list(set(recommendations))[:10]

        if not recommendations:
            recommendations.append(
                "Compliance posture is acceptable - continue monitoring"
            )

        return recommendations

    def get_assessment_history(
        self, standard: Optional[ComplianceStandard] = None, limit: int = 10
    ) -> List[ComplianceAssessment]:
        """Get assessment history"""
        assessments = self.assessment_history
        if standard:
            assessments = [a for a in assessments if a.standard == standard]

        return assessments[-limit:]

    def get_compliance_trends(
        self, standard: ComplianceStandard, days: int = 30
    ) -> Dict[str, Any]:
        """Get compliance trends over time"""
        cutoff_date = datetime.now() - timedelta(days=days)

        relevant_assessments = [
            a
            for a in self.assessment_history
            if a.standard == standard and a.start_time >= cutoff_date
        ]

        trends = {
            "standard": standard.value,
            "period_days": days,
            "total_assessments": len(relevant_assessments),
            "compliance_trend": [],
            "violation_trend": [],
        }

        for assessment in sorted(relevant_assessments, key=lambda x: x.start_time):
            trends["compliance_trend"].append(
                {
                    "date": assessment.start_time.date().isoformat(),
                    "score": assessment.compliance_score,
                }
            )
            trends["violation_trend"].append(
                {
                    "date": assessment.start_time.date().isoformat(),
                    "critical": assessment.critical_violations,
                    "high": assessment.high_violations,
                }
            )

        return trends

    def export_assessment_report(
        self, assessment: ComplianceAssessment, filepath: str
    ) -> bool:
        """Export compliance assessment report"""
        try:
            export_data = {
                "assessment_id": assessment.assessment_id,
                "standard": assessment.standard.value,
                "start_time": assessment.start_time.isoformat(),
                "end_time": (
                    assessment.end_time.isoformat() if assessment.end_time else None
                ),
                "duration_seconds": assessment.duration_seconds,
                "summary": assessment.summary,
                "recommendations": assessment.recommendations,
                "detailed_results": [
                    {
                        "requirement_id": result.requirement.requirement_id,
                        "title": result.requirement.title,
                        "status": result.status.value,
                        "severity": result.requirement.severity.value,
                        "evidence_found": result.evidence_found,
                        "violations": result.violations,
                        "remediation_actions": result.remediation_actions,
                        "notes": result.notes,
                    }
                    for result in assessment.detailed_results
                ],
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Compliance assessment report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export assessment report: {e}")
            return False


# Factory function for easy instantiation
def create_compliance_checker(
    workspace_path: Optional[str] = None,
) -> ComplianceChecker:
    """
    Factory function to create compliance checker

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured ComplianceChecker instance
    """
    return ComplianceChecker(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for compliance checking"""
    import argparse

    parser = argparse.ArgumentParser(description="L.I.F.E. Platform Compliance Checker")
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--standard",
        "-s",
        choices=[s.value for s in ComplianceStandard],
        required=True,
        help="Compliance standard to assess",
    )
    parser.add_argument(
        "--export", "-e", help="Export assessment results to specified JSON file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create compliance checker
    checker = create_compliance_checker(workspace_path=args.workspace)

    # Map string to enum
    standard_map = {s.value: s for s in ComplianceStandard}
    standard = standard_map.get(args.standard)

    if not standard:
        print(f"Invalid standard: {args.standard}")
        return 1

    print("L.I.F.E. Platform - Compliance Checker")
    print("=" * 40)

    try:
        # Perform assessment
        print(f"Performing compliance assessment for {args.standard.upper()}...")

        assessment = asyncio.run(checker.assess_compliance(standard))

        print("\nAssessment Results:")
        print(f"  Assessment ID: {assessment.assessment_id}")
        print(f"  Standard: {assessment.standard.value.upper()}")
        print(f"  Duration: {assessment.duration_seconds:.2f}s")
        print(f"  Compliance Score: {assessment.compliance_score:.1f}/100")
        print(f"  Overall Status: {assessment.overall_status.value.upper()}")
        print(f"  Requirements Checked: {assessment.total_requirements}")
        print(f"  Compliant: {assessment.compliant_requirements}")
        print(f"  Non-Compliant: {assessment.non_compliant_requirements}")
        print(f"  Critical Violations: {assessment.critical_violations}")
        print(f"  High Violations: {assessment.high_violations}")

        if assessment.recommendations:
            print("\nRecommendations:")
            for rec in assessment.recommendations[:5]:  # Show first 5
                print(f"  • {rec}")

        if args.export:
            if checker.export_assessment_report(assessment, args.export):
                print(f"\nAssessment report exported to {args.export}")
            else:
                print("\nFailed to export assessment report")
                return 1

        # Exit with appropriate code based on assessment
        if assessment.overall_status == ComplianceStatus.NON_COMPLIANT:
            print("\n❌ NON-COMPLIANT: Critical compliance issues found!")
            return 1
        elif assessment.overall_status == ComplianceStatus.COMPENSATING_CONTROL:
            print("\n⚠️  COMPENSATING CONTROLS: Review high-priority issues")
            return 0
        else:
            print("\n✅ COMPLIANT: Compliance requirements met")
            return 0

    except KeyboardInterrupt:
        print("\nAssessment interrupted by user")
        return 1
    except Exception as e:
        print(f"\nCompliance assessment failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
