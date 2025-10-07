#!/usr/bin/env python3
"""
MODULE 10: Compliance & Fairness Auditor (CFA)
GDPR/HIPAA Compliance and Algorithmic Fairness Checker

STANDALONE DEMONSTRATION - NOT YET INTEGRATED
Created: October 6, 2025
Copyright 2025 - Sergio Paya Borrull

This module ensures data privacy compliance and algorithmic fairness for
healthcare and educational deployments of the L.I.F.E. platform.

CRITICAL FOR: Healthcare institutions (HIPAA) and EU markets (GDPR)
"""

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComplianceStandard(Enum):
    """Supported compliance standards"""

    GDPR = "gdpr"  # EU General Data Protection Regulation
    HIPAA = "hipaa"  # US Health Insurance Portability and Accountability Act
    FERPA = "ferpa"  # US Family Educational Rights and Privacy Act
    COPPA = "coppa"  # US Children's Online Privacy Protection Act
    PIPEDA = "pipeda"  # Canadian Personal Information Protection


class ViolationSeverity(Enum):
    """Severity levels for compliance violations"""

    CRITICAL = "critical"  # Immediate action required (blocks deployment)
    HIGH = "high"  # Must be fixed before production
    MEDIUM = "medium"  # Should be addressed
    LOW = "low"  # Best practice recommendation
    INFO = "info"  # Informational notice


@dataclass
class ComplianceViolation:
    """Details of a compliance violation"""

    field_name: str
    violation_type: str
    severity: ViolationSeverity
    standard: ComplianceStandard
    description: str
    recommendation: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FairnessMetrics:
    """Metrics for algorithmic fairness assessment"""

    demographic_parity: float  # Equal prediction rates across groups
    equalized_odds: float  # Equal TPR/FPR across groups
    disparate_impact: float  # Ratio of favorable outcomes
    prediction_equality: float  # Consistency across demographics
    overall_fairness_score: float
    protected_attributes_detected: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AuditReport:
    """Complete compliance and fairness audit report"""

    audit_id: str
    timestamp: str
    compliant: bool
    violations: List[ComplianceViolation]
    fairness_metrics: Optional[FairnessMetrics]
    standards_checked: List[ComplianceStandard]
    data_processed: int
    recommendations: List[str]
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL


class ComplianceFairnessAuditor:
    """
    Comprehensive compliance and fairness auditing system

    Key Features:
    - Detects PII and sensitive health information
    - Validates GDPR/HIPAA compliance
    - Assesses algorithmic fairness across demographics
    - Provides actionable remediation guidance
    """

    def __init__(self, standards: Optional[List[ComplianceStandard]] = None):
        """
        Initialize auditor with compliance standards

        Args:
            standards: List of compliance standards to check
        """
        if standards is None:
            standards = [
                ComplianceStandard.GDPR,
                ComplianceStandard.HIPAA,
                ComplianceStandard.FERPA,
            ]

        self.standards = standards

        # Define sensitive field patterns for each standard
        self._initialize_sensitive_fields()

        # Anonymization tracking
        self.anonymized_fields: Set[str] = set()

        logger.info(
            f"Compliance auditor initialized with standards: {[s.value for s in standards]}"
        )

    def _initialize_sensitive_fields(self):
        """Initialize sensitive field patterns for each compliance standard"""

        # GDPR - Personal Data
        self.gdpr_sensitive = {
            "direct_identifiers": [
                "name",
                "full_name",
                "first_name",
                "last_name",
                "email",
                "email_address",
                "phone",
                "phone_number",
                "mobile",
                "telephone",
                "address",
                "street_address",
                "postal_code",
                "zip_code",
                "passport",
                "passport_number",
                "drivers_license",
                "license_number",
                "national_id",
                "id_number",
                "ssn",
                "social_security",
            ],
            "special_categories": [
                "race",
                "ethnicity",
                "racial_origin",
                "religion",
                "religious_beliefs",
                "political_opinion",
                "political_affiliation",
                "genetic_data",
                "dna",
                "genome",
                "biometric_data",
                "fingerprint",
                "facial_recognition",
                "health_data",
                "medical_record",
                "diagnosis",
                "sex_life",
                "sexual_orientation",
            ],
        }

        # HIPAA - Protected Health Information (PHI)
        self.hipaa_phi = [
            "patient_name",
            "patient_id",
            "medical_record_number",
            "mrn",
            "health_plan_number",
            "insurance_id",
            "account_number",
            "billing_id",
            "certificate_number",
            "license_number",
            "vehicle_id",
            "device_id",
            "serial_number",
            "web_url",
            "ip_address",
            "biometric_identifier",
            "photo",
            "image",
            "diagnosis",
            "treatment",
            "prescription",
            "lab_result",
            "test_result",
            "birth_date",
            "date_of_birth",
            "dob",
            "death_date",
            "date_of_death",
            "admission_date",
            "discharge_date",
        ]

        # FERPA - Educational Records
        self.ferpa_records = [
            "student_name",
            "student_id",
            "grade",
            "gpa",
            "transcript",
            "disciplinary_record",
            "attendance",
            "parent_name",
            "guardian_name",
            "teacher_evaluation",
            "assessment_score",
        ]

        # COPPA - Children's Data (under 13)
        self.coppa_fields = [
            "child_name",
            "child_age",
            "child_photo",
            "child_video",
            "child_location",
            "geolocation",
            "child_voice",
            "audio_recording",
        ]

    def audit_data(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> AuditReport:
        """
        Perform comprehensive compliance audit on data

        Args:
            data: Data to audit (user records, learning sessions, etc.)
            context: Additional context (user_age, location, consent_status)

        Returns:
            Complete audit report with violations and recommendations
        """
        audit_id = hashlib.sha256(
            f"{datetime.now().isoformat()}{str(data)}".encode()
        ).hexdigest()[:16]

        violations: List[ComplianceViolation] = []

        # Check each compliance standard
        for standard in self.standards:
            if standard == ComplianceStandard.GDPR:
                violations.extend(self._check_gdpr(data, context))
            elif standard == ComplianceStandard.HIPAA:
                violations.extend(self._check_hipaa(data, context))
            elif standard == ComplianceStandard.FERPA:
                violations.extend(self._check_ferpa(data, context))
            elif standard == ComplianceStandard.COPPA:
                violations.extend(self._check_coppa(data, context))

        # Determine compliance status
        critical_violations = [
            v for v in violations if v.severity == ViolationSeverity.CRITICAL
        ]
        high_violations = [
            v for v in violations if v.severity == ViolationSeverity.HIGH
        ]

        compliant = len(critical_violations) == 0 and len(high_violations) == 0

        # Determine risk level
        if critical_violations:
            risk_level = "CRITICAL"
        elif high_violations:
            risk_level = "HIGH"
        elif len(violations) > 5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Generate recommendations
        recommendations = self._generate_recommendations(violations)

        report = AuditReport(
            audit_id=audit_id,
            timestamp=datetime.now().isoformat(),
            compliant=compliant,
            violations=violations,
            fairness_metrics=None,  # Computed separately
            standards_checked=self.standards,
            data_processed=len(data),
            recommendations=recommendations,
            risk_level=risk_level,
        )

        return report

    def _check_gdpr(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> List[ComplianceViolation]:
        """Check GDPR compliance"""
        violations = []

        # Check for direct identifiers
        for field in self.gdpr_sensitive["direct_identifiers"]:
            if field in data:
                violations.append(
                    ComplianceViolation(
                        field_name=field,
                        violation_type="gdpr_direct_identifier",
                        severity=ViolationSeverity.HIGH,
                        standard=ComplianceStandard.GDPR,
                        description=f"Direct identifier '{field}' detected without anonymization",
                        recommendation="Apply pseudonymization or encryption before storage",
                    )
                )

        # Check for special category data (GDPR Article 9)
        for field in self.gdpr_sensitive["special_categories"]:
            if field in data:
                violations.append(
                    ComplianceViolation(
                        field_name=field,
                        violation_type="gdpr_special_category",
                        severity=ViolationSeverity.CRITICAL,
                        standard=ComplianceStandard.GDPR,
                        description=f"Special category data '{field}' requires explicit consent",
                        recommendation="Obtain explicit consent and implement additional security measures",
                    )
                )

        # Check for consent documentation
        if context and not context.get("gdpr_consent_obtained"):
            violations.append(
                ComplianceViolation(
                    field_name="consent",
                    violation_type="gdpr_consent_missing",
                    severity=ViolationSeverity.HIGH,
                    standard=ComplianceStandard.GDPR,
                    description="No documented GDPR consent",
                    recommendation="Implement consent management system with audit trail",
                )
            )

        # Check for data minimization principle
        if len(data) > 20:  # Arbitrary threshold for demonstration
            violations.append(
                ComplianceViolation(
                    field_name="data_volume",
                    violation_type="gdpr_data_minimization",
                    severity=ViolationSeverity.MEDIUM,
                    standard=ComplianceStandard.GDPR,
                    description="Potential violation of data minimization principle",
                    recommendation="Collect only data strictly necessary for processing purpose",
                )
            )

        return violations

    def _check_hipaa(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> List[ComplianceViolation]:
        """Check HIPAA compliance (Protected Health Information)"""
        violations = []

        # Check for PHI identifiers
        for field in self.hipaa_phi:
            if field in data:
                violations.append(
                    ComplianceViolation(
                        field_name=field,
                        violation_type="hipaa_phi_detected",
                        severity=ViolationSeverity.CRITICAL,
                        standard=ComplianceStandard.HIPAA,
                        description=f"Protected Health Information '{field}' requires encryption",
                        recommendation="Encrypt at rest and in transit, implement access controls",
                    )
                )

        # Check for Business Associate Agreement
        if context and not context.get("baa_signed"):
            violations.append(
                ComplianceViolation(
                    field_name="baa",
                    violation_type="hipaa_baa_missing",
                    severity=ViolationSeverity.CRITICAL,
                    standard=ComplianceStandard.HIPAA,
                    description="Business Associate Agreement not documented",
                    recommendation="Execute BAA before processing any PHI",
                )
            )

        # Check for audit logging
        if context and not context.get("audit_logging_enabled"):
            violations.append(
                ComplianceViolation(
                    field_name="audit_log",
                    violation_type="hipaa_audit_missing",
                    severity=ViolationSeverity.HIGH,
                    standard=ComplianceStandard.HIPAA,
                    description="HIPAA-compliant audit logging not enabled",
                    recommendation="Implement comprehensive audit logging for all PHI access",
                )
            )

        return violations

    def _check_ferpa(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> List[ComplianceViolation]:
        """Check FERPA compliance (Educational Records)"""
        violations = []

        for field in self.ferpa_records:
            if field in data:
                violations.append(
                    ComplianceViolation(
                        field_name=field,
                        violation_type="ferpa_educational_record",
                        severity=ViolationSeverity.HIGH,
                        standard=ComplianceStandard.FERPA,
                        description=f"Educational record '{field}' requires parental consent",
                        recommendation="Obtain written parental consent for disclosure",
                    )
                )

        return violations

    def _check_coppa(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]]
    ) -> List[ComplianceViolation]:
        """Check COPPA compliance (Children under 13)"""
        violations = []

        # Check if data is for children
        is_child = False
        if context:
            age = context.get("user_age")
            if age and age < 13:
                is_child = True

        if is_child:
            for field in self.coppa_fields:
                if field in data:
                    violations.append(
                        ComplianceViolation(
                            field_name=field,
                            violation_type="coppa_child_data",
                            severity=ViolationSeverity.CRITICAL,
                            standard=ComplianceStandard.COPPA,
                            description=f"Child data '{field}' requires verifiable parental consent",
                            recommendation="Implement COPPA-compliant parental consent mechanism",
                        )
                    )

        return violations

    def _generate_recommendations(
        self, violations: List[ComplianceViolation]
    ) -> List[str]:
        """Generate prioritized remediation recommendations"""
        recommendations = []

        # Group by severity
        critical = [v for v in violations if v.severity == ViolationSeverity.CRITICAL]
        high = [v for v in violations if v.severity == ViolationSeverity.HIGH]

        if critical:
            recommendations.append(
                f"CRITICAL: {len(critical)} blocking violation(s) must be resolved before deployment"
            )
            recommendations.extend([v.recommendation for v in critical[:3]])

        if high:
            recommendations.append(
                f"HIGH: {len(high)} violation(s) should be addressed before production"
            )
            recommendations.extend([v.recommendation for v in high[:3]])

        # General best practices
        if violations:
            recommendations.append(
                "Implement Azure Key Vault for sensitive data encryption"
            )
            recommendations.append("Enable Azure Monitor for compliance audit logging")
            recommendations.append(
                "Configure Azure Private Link for secure data access"
            )

        return recommendations

    def anonymize_field(self, value: str, method: str = "hash") -> str:
        """
        Anonymize a sensitive field

        Args:
            value: Original value
            method: Anonymization method (hash, mask, truncate)

        Returns:
            Anonymized value
        """
        if method == "hash":
            # One-way hash
            return hashlib.sha256(value.encode()).hexdigest()[:16]

        elif method == "mask":
            # Show first/last chars only
            if len(value) <= 4:
                return "****"
            return value[0] + "*" * (len(value) - 2) + value[-1]

        elif method == "truncate":
            # Remove most specific information
            if "@" in value:  # Email
                parts = value.split("@")
                return parts[0][:3] + "***@" + parts[1]
            return value[:4] + "***"

        else:
            raise ValueError(f"Unknown anonymization method: {method}")

    def assess_algorithmic_fairness(
        self,
        predictions: List[float],
        true_labels: List[int],
        protected_attributes: Dict[str, List[Any]],
    ) -> FairnessMetrics:
        """
        Assess algorithmic fairness across demographic groups

        Args:
            predictions: Model predictions (0-1 scores)
            true_labels: Ground truth labels (0 or 1)
            protected_attributes: Dict of protected attributes (race, gender, age, etc.)

        Returns:
            Fairness metrics across all protected attributes
        """
        import numpy as np

        # Convert to binary predictions
        binary_preds = [1 if p > 0.5 else 0 for p in predictions]

        fairness_scores = []

        for attr_name, attr_values in protected_attributes.items():
            # Get unique groups
            unique_groups = list(set(attr_values))

            if len(unique_groups) < 2:
                continue  # Need at least 2 groups to compare

            # Calculate metrics per group
            group_metrics = {}
            for group in unique_groups:
                group_indices = [i for i, v in enumerate(attr_values) if v == group]

                if not group_indices:
                    continue

                group_preds = [binary_preds[i] for i in group_indices]
                group_labels = [true_labels[i] for i in group_indices]

                # Positive prediction rate
                positive_rate = (
                    sum(group_preds) / len(group_preds) if group_preds else 0
                )

                # True positive rate (sensitivity)
                true_positives = sum(
                    1 for p, l in zip(group_preds, group_labels) if p == 1 and l == 1
                )
                actual_positives = sum(group_labels)
                tpr = true_positives / actual_positives if actual_positives > 0 else 0

                # False positive rate
                false_positives = sum(
                    1 for p, l in zip(group_preds, group_labels) if p == 1 and l == 0
                )
                actual_negatives = len(group_labels) - actual_positives
                fpr = false_positives / actual_negatives if actual_negatives > 0 else 0

                group_metrics[group] = {
                    "positive_rate": positive_rate,
                    "tpr": tpr,
                    "fpr": fpr,
                }

            # Calculate fairness metrics
            if len(group_metrics) >= 2:
                positive_rates = [m["positive_rate"] for m in group_metrics.values()]
                tprs = [m["tpr"] for m in group_metrics.values()]

                # Demographic parity (equal positive rates)
                demographic_parity = 1.0 - (max(positive_rates) - min(positive_rates))

                # Equalized odds (equal TPR/FPR)
                equalized_odds = 1.0 - (max(tprs) - min(tprs))

                # Disparate impact (ratio of rates)
                disparate_impact = (
                    min(positive_rates) / max(positive_rates)
                    if max(positive_rates) > 0
                    else 1.0
                )

                fairness_scores.append(
                    {
                        "demographic_parity": demographic_parity,
                        "equalized_odds": equalized_odds,
                        "disparate_impact": disparate_impact,
                    }
                )

        # Aggregate across all protected attributes
        if fairness_scores:
            avg_demographic_parity = np.mean(
                [s["demographic_parity"] for s in fairness_scores]
            )
            avg_equalized_odds = np.mean([s["equalized_odds"] for s in fairness_scores])
            avg_disparate_impact = np.mean(
                [s["disparate_impact"] for s in fairness_scores]
            )
            prediction_equality = np.std(predictions)  # Lower is more equal

            overall_fairness = np.mean(
                [avg_demographic_parity, avg_equalized_odds, avg_disparate_impact]
            )
        else:
            avg_demographic_parity = 1.0
            avg_equalized_odds = 1.0
            avg_disparate_impact = 1.0
            prediction_equality = 0.0
            overall_fairness = 1.0

        return FairnessMetrics(
            demographic_parity=avg_demographic_parity,
            equalized_odds=avg_equalized_odds,
            disparate_impact=avg_disparate_impact,
            prediction_equality=1.0 - prediction_equality,  # Invert so higher is better
            overall_fairness_score=overall_fairness,
            protected_attributes_detected=list(protected_attributes.keys()),
        )


# ============================================================================
# DEMONSTRATION & TESTING
# ============================================================================


def demonstrate_compliance_auditor():
    """Demonstrate Compliance & Fairness Auditor"""
    print("=" * 80)
    print("MODULE 10: Compliance & Fairness Auditor - DEMONSTRATION")
    print("=" * 80)
    print()

    # Initialize auditor
    auditor = ComplianceFairnessAuditor(
        standards=[
            ComplianceStandard.GDPR,
            ComplianceStandard.HIPAA,
            ComplianceStandard.FERPA,
        ]
    )

    # Test 1: Clean data (should pass)
    print("Test 1: Compliant Data")
    print("-" * 80)

    clean_data = {
        "user_id": "usr_123456",
        "session_id": "ses_789abc",
        "learning_score": 0.85,
        "attention_index": 0.72,
        "timestamp": "2025-10-06T12:00:00Z",
    }

    clean_context = {
        "gdpr_consent_obtained": True,
        "baa_signed": True,
        "audit_logging_enabled": True,
    }

    report1 = auditor.audit_data(clean_data, clean_context)

    print(f"Audit ID: {report1.audit_id}")
    print(f"Compliant: {report1.compliant}")
    print(f"Risk Level: {report1.risk_level}")
    print(f"Violations Found: {len(report1.violations)}")
    print(f"Standards Checked: {[s.value for s in report1.standards_checked]}")
    print()
    print()

    # Test 2: Data with violations
    print("Test 2: Non-Compliant Data (Multiple Violations)")
    print("-" * 80)

    violating_data = {
        "user_id": "usr_123456",
        "full_name": "John Doe",  # GDPR violation
        "email": "john.doe@example.com",  # GDPR violation
        "phone_number": "+1-555-1234",  # GDPR violation
        "medical_record_number": "MRN-987654",  # HIPAA violation
        "diagnosis": "ADHD",  # HIPAA violation
        "student_id": "STU-456789",  # FERPA violation
        "gpa": 3.7,  # FERPA violation
        "learning_score": 0.85,
    }

    violating_context = {
        "gdpr_consent_obtained": False,  # GDPR violation
        "baa_signed": False,  # HIPAA violation
        "audit_logging_enabled": False,  # HIPAA violation
    }

    report2 = auditor.audit_data(violating_data, violating_context)

    print(f"Audit ID: {report2.audit_id}")
    print(f"Compliant: {report2.compliant}")
    print(f"Risk Level: {report2.risk_level}")
    print(f"Violations Found: {len(report2.violations)}")
    print()

    print("Violations by Severity:")
    for severity in ViolationSeverity:
        count = len([v for v in report2.violations if v.severity == severity])
        if count > 0:
            print(f"  {severity.value.upper()}: {count}")
    print()

    print("Sample Violations (first 3):")
    for v in report2.violations[:3]:
        print(f"  - Field: {v.field_name}")
        print(f"    Type: {v.violation_type}")
        print(f"    Severity: {v.severity.value}")
        print(f"    Standard: {v.standard.value.upper()}")
        print(f"    Description: {v.description}")
        print(f"    Recommendation: {v.recommendation}")
        print()

    print("Remediation Recommendations:")
    for i, rec in enumerate(report2.recommendations[:5], 1):
        print(f"  {i}. {rec}")
    print()
    print()

    # Test 3: Anonymization
    print("Test 3: Data Anonymization")
    print("-" * 80)

    sensitive_values = {
        "email": "john.doe@healthcare.com",
        "name": "John Michael Doe",
        "phone": "+1-555-123-4567",
    }

    print("Original Values:")
    for field, value in sensitive_values.items():
        print(f"  {field}: {value}")
    print()

    print("Anonymized (Hash):")
    for field, value in sensitive_values.items():
        anonymized = auditor.anonymize_field(value, method="hash")
        print(f"  {field}: {anonymized}")
    print()

    print("Anonymized (Mask):")
    for field, value in sensitive_values.items():
        anonymized = auditor.anonymize_field(value, method="mask")
        print(f"  {field}: {anonymized}")
    print()
    print()

    # Test 4: Algorithmic Fairness Assessment
    print("Test 4: Algorithmic Fairness Assessment")
    print("-" * 80)

    # Simulate predictions and demographics
    np.random.seed(42)
    n_samples = 1000

    # Generate synthetic data
    predictions = np.random.beta(2, 2, n_samples).tolist()
    true_labels = [1 if p > 0.5 else 0 for p in predictions]

    # Protected attributes
    genders = ["male", "female"] * (n_samples // 2)
    ethnicities = ["group_a", "group_b", "group_c", "group_d"] * (n_samples // 4)

    protected_attrs = {"gender": genders, "ethnicity": ethnicities}

    print(f"Analyzing {n_samples} predictions across protected attributes...")
    print(f"Protected Attributes: {list(protected_attrs.keys())}")
    print()

    fairness = auditor.assess_algorithmic_fairness(
        predictions, true_labels, protected_attrs
    )

    print("Fairness Metrics:")
    print(f"  Demographic Parity: {fairness.demographic_parity:.3f}")
    print(f"    (1.0 = perfect parity, 0.8+ = acceptable)")
    print(f"  Equalized Odds: {fairness.equalized_odds:.3f}")
    print(f"    (1.0 = equal true positive rates)")
    print(f"  Disparate Impact: {fairness.disparate_impact:.3f}")
    print(f"    (0.8-1.25 = acceptable range)")
    print(f"  Prediction Equality: {fairness.prediction_equality:.3f}")
    print(f"  Overall Fairness Score: {fairness.overall_fairness_score:.3f}")
    print()

    if fairness.overall_fairness_score >= 0.8:
        print("✅ Algorithm meets fairness criteria")
    else:
        print("⚠️ Algorithm may exhibit bias - review predictions across groups")
    print()

    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("INTEGRATION NOTES:")
    print("- Add ComplianceFairnessAuditor to data processing pipeline")
    print("- Call audit_data() before storing any user information")
    print("- Use anonymize_field() for all PII before storage")
    print("- Run assess_algorithmic_fairness() periodically on production data")
    print("- Store audit reports in Azure Blob Storage for compliance records")
    print()
    print("DEPLOYMENT REQUIREMENTS:")
    print("- Azure Key Vault: Store encrypted PHI/PII")
    print("- Azure Monitor: HIPAA-compliant audit logging")
    print("- Azure Private Link: Secure data access")
    print("- BAA with Microsoft: Required for HIPAA compliance")


if __name__ == "__main__":
    import numpy as np

    demonstrate_compliance_auditor()
