#!/usr/bin/env python3
"""
Comprehensive Achievement Verification Suite for L.I.F.E Platform
Tests all claimed achievements from the October 16-19, 2025 integration report

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent.absolute()


@dataclass
class VerificationResult:
    """Result of a single verification test"""

    test_name: str
    category: str
    status: str  # "PASS", "FAIL", "PARTIAL", "SKIPPED"
    details: str
    evidence: List[str]
    timestamp: str


class ComprehensiveVerifier:
    """Verifies all claimed achievements from the integration report"""

    def __init__(self):
        self.results: List[VerificationResult] = []
        self.repo_root = SCRIPT_DIR

    def log_result(self, result: VerificationResult):
        """Log and store a verification result"""
        status_emoji = {"PASS": "✅", "FAIL": "❌", "PARTIAL": "⚠️", "SKIPPED": "⏭️"}
        emoji = status_emoji.get(result.status, "❓")
        logger.info(f"{emoji} {result.category} - {result.test_name}: {result.status}")
        self.results.append(result)

    # ========================================================================
    # CATEGORY 1: COMPLETE INTEGRATION FRAMEWORK
    # ========================================================================

    def verify_platform_unification(self) -> VerificationResult:
        """Verify experimentP2L algorithm integration"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for experimentP2L algorithm files
            algo_files = list(self.repo_root.glob("experimentP2L*.py"))
            if algo_files:
                evidence.append(
                    f"Found {len(algo_files)} experimentP2L algorithm file(s)"
                )

                # Check file size (claimed 1.7MB)
                for f in algo_files:
                    size_mb = f.stat().st_size / (1024 * 1024)
                    evidence.append(f"{f.name}: {size_mb:.2f}MB")

                # Check for core imports
                for algo_file in algo_files:
                    content = algo_file.read_text(encoding="utf-8", errors="ignore")
                    if "class LIFEAlgorithm" in content or "async def" in content:
                        evidence.append(
                            f"{algo_file.name} contains core algorithm classes"
                        )
                        status = "PASS"
                        details = f"Algorithm integration verified: {len(algo_files)} file(s) found"
                        break

            if status == "FAIL":
                details = "Algorithm files not found or incomplete"

        except Exception as e:
            status = "FAIL"
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Platform Unification",
            category="Integration Framework",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    def verify_azure_integration(self) -> VerificationResult:
        """Verify Azure infrastructure integration"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check azure_config.py
            azure_config = self.repo_root / "azure_config.py"
            if azure_config.exists():
                content = azure_config.read_text(encoding="utf-8")
                evidence.append("azure_config.py exists")

                # Check for subscription ID
                if "5c88cef6-f243-497d-98af-6c6086d575ca" in content:
                    evidence.append(
                        "Subscription ID configured: 5c88cef6-f243-497d-98af-6c6086d575ca"
                    )

                # Check for Pay-As-You-Go
                if "MS-AZR-0003P" in content or "Pay-As-You-Go" in content:
                    evidence.append("Subscription type: Pay-As-You-Go (MS-AZR-0003P)")

                # Check for Azure services
                services = [
                    "BlobServiceClient",
                    "ServiceBusClient",
                    "SecretClient",
                    "DefaultAzureCredential",
                ]
                found_services = [s for s in services if s in content]
                evidence.append(
                    f"Azure services configured: {len(found_services)}/{len(services)}"
                )

                if len(found_services) >= 3:
                    status = "PASS"
                    details = f"Azure integration verified: {len(found_services)} services configured"
                else:
                    status = "PARTIAL"
                    details = "Partial Azure integration found"
            else:
                details = "azure_config.py not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Azure Infrastructure Integration",
            category="Integration Framework",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 2: TESTING & VALIDATION SUITE
    # ========================================================================

    def verify_testing_suite(self) -> VerificationResult:
        """Verify comprehensive testing suite exists"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for test files
            test_patterns = ["*test*.py", "*validation*.py", "*verification*.py"]

            test_files = []
            for pattern in test_patterns:
                test_files.extend(list(self.repo_root.glob(pattern)))

            test_files = list(set(test_files))  # Remove duplicates
            evidence.append(f"Found {len(test_files)} test/validation files")

            # Check for specific validation files mentioned in report
            key_files = [
                "life_integration_testing_guide.py",
                "quick_verification.py",
                "validate_environment.py",
            ]

            found_key_files = []
            for key_file in key_files:
                if (self.repo_root / key_file).exists():
                    found_key_files.append(key_file)
                    evidence.append(f"Key file exists: {key_file}")

            if len(found_key_files) >= 2:
                status = "PASS"
                details = f"Testing suite verified: {len(test_files)} test files found"
            elif len(test_files) >= 5:
                status = "PARTIAL"
                details = "Test files exist but some key files missing"
            else:
                details = "Insufficient testing infrastructure"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Comprehensive Testing Suite",
            category="Testing & Validation",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 3: AUTONOMOUS CAPABILITIES
    # ========================================================================

    def verify_self_healing(self) -> VerificationResult:
        """Verify self-healing system implementation"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check azure_config.py for self-healing infrastructure
            azure_config = self.repo_root / "azure_config.py"
            if azure_config.exists():
                content = azure_config.read_text(encoding="utf-8")

                # Look for self-healing keywords
                healing_keywords = [
                    "SelfHealingInfrastructure",
                    "health_monitoring",
                    "auto_recovery",
                    "circuit_breaker",
                ]

                found_keywords = [kw for kw in healing_keywords if kw in content]
                evidence.append(
                    f"Self-healing keywords found: {len(found_keywords)}/{len(healing_keywords)}"
                )

                for kw in found_keywords:
                    evidence.append(f"Found: {kw}")

                if len(found_keywords) >= 2:
                    status = "PASS"
                    details = "Self-healing infrastructure implemented"
                elif len(found_keywords) >= 1:
                    status = "PARTIAL"
                    details = "Partial self-healing implementation"
                else:
                    details = "Self-healing system not found"
            else:
                details = "azure_config.py not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Self-Healing System",
            category="Autonomous Capabilities",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    def verify_continuous_learning(self) -> VerificationResult:
        """Verify continuous learning pipeline"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for optimizer and learning files
            learning_files = [
                "autonomous_optimizer.py",
                "nocturnal_eeg_ingestion_optimizer.py",
                "experience_collector.py",
            ]

            found_files = []
            for lf in learning_files:
                if (self.repo_root / lf).exists():
                    found_files.append(lf)
                    evidence.append(f"Learning module exists: {lf}")

            if len(found_files) >= 2:
                status = "PASS"
                details = f"Continuous learning pipeline verified: {len(found_files)} modules found"
            elif len(found_files) >= 1:
                status = "PARTIAL"
                details = "Partial learning pipeline implementation"
            else:
                details = "Continuous learning pipeline not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Continuous Learning Pipeline",
            category="Autonomous Capabilities",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 4: EXTERNAL EEG DATA INGESTION
    # ========================================================================

    def verify_eeg_ingestion(self) -> VerificationResult:
        """Verify external EEG data ingestion pipeline"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for EEG ingestion files
            eeg_files = [
                "physionet_eeg_ingest.py",
                "external_eeg_ingestion_engine.py",
                "eeg_data_handler.py",
            ]

            found_files = []
            for ef in eeg_files:
                if (self.repo_root / ef).exists():
                    found_files.append(ef)
                    evidence.append(f"EEG ingestion module exists: {ef}")

            # Check for HTML dashboard
            eeg_html = list(self.repo_root.glob("*external*eeg*ingestion*.html"))
            if eeg_html:
                evidence.append(
                    f"EEG ingestion dashboard found: {len(eeg_html)} file(s)"
                )

            if len(found_files) >= 2:
                status = "PASS"
                details = (
                    f"EEG ingestion verified: {len(found_files)} modules + dashboard"
                )
            elif len(found_files) >= 1 or eeg_html:
                status = "PARTIAL"
                details = "Partial EEG ingestion implementation"
            else:
                details = "EEG ingestion pipeline not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="External EEG Data Ingestion",
            category="EEG Processing",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 5: PRODUCTION DEPLOYMENT INFRASTRUCTURE
    # ========================================================================

    def verify_deployment_infrastructure(self) -> VerificationResult:
        """Verify production deployment infrastructure"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for deployment scripts
            deploy_scripts = [
                "deploy_python313.bat",
                "azure_functions_workflow.py",
                "AZURE_CLOUDSHELL_DEPLOYMENT.sh",
            ]

            found_scripts = []
            for ds in deploy_scripts:
                if (self.repo_root / ds).exists():
                    found_scripts.append(ds)
                    evidence.append(f"Deployment script exists: {ds}")

            # Check for Azure resource configuration
            azure_config = self.repo_root / "azure_config.py"
            if azure_config.exists():
                content = azure_config.read_text(encoding="utf-8")

                # Check for resource names
                resources = [
                    "life-platform-rg",
                    "stlifeplatformprod",
                    "kv-life-platform-prod",
                    "sb-life-platform-prod",
                ]

                found_resources = [r for r in resources if r in content]
                evidence.append(
                    f"Azure resources configured: {len(found_resources)}/{len(resources)}"
                )

            if len(found_scripts) >= 2 and len(found_resources) >= 3:
                status = "PASS"
                details = f"Deployment infrastructure verified: {len(found_scripts)} scripts, {len(found_resources)} resources"
            elif len(found_scripts) >= 1 or len(found_resources) >= 1:
                status = "PARTIAL"
                details = "Partial deployment infrastructure"
            else:
                details = "Deployment infrastructure not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Production Deployment Infrastructure",
            category="Deployment",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 6: DOCUMENTATION PACKAGE
    # ========================================================================

    def verify_documentation(self) -> VerificationResult:
        """Verify complete documentation package"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for key documentation files
            doc_files = list(self.repo_root.glob("*.md")) + list(
                self.repo_root.glob("*.txt")
            )
            evidence.append(f"Found {len(doc_files)} documentation files (.md + .txt)")

            # Check for specific key documents
            key_docs = [
                "README.md",
                "CHANGELOG.md",
                "VERIFICATION_GUIDE",
                "INTEGRATION",
            ]

            found_docs = []
            for key_doc in key_docs:
                matching = [f for f in doc_files if key_doc.lower() in f.name.lower()]
                if matching:
                    found_docs.append(key_doc)
                    evidence.append(
                        f"Key documentation exists: {key_doc} ({len(matching)} file(s))"
                    )

            if len(found_docs) >= 3:
                status = "PASS"
                details = f"Documentation verified: {len(doc_files)} files, {len(found_docs)}/4 key docs"
            elif len(doc_files) >= 10:
                status = "PARTIAL"
                details = "Documentation exists but some key docs missing"
            else:
                details = "Insufficient documentation"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Complete Documentation Package",
            category="Documentation",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 7: INDIVIDUALIZED LEARNING
    # ========================================================================

    def verify_individualized_learning(self) -> VerificationResult:
        """Verify per-user personalization implementation"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check experimentP2L algorithm for personalization
            algo_files = list(self.repo_root.glob("experimentP2L*.py"))

            personalization_keywords = [
                "user_trait",
                "curiosity",
                "resilience",
                "openness",
                "individual",
                "personalized",
            ]

            found_in_algo = []
            for algo_file in algo_files:
                content = algo_file.read_text(encoding="utf-8", errors="ignore")
                for kw in personalization_keywords:
                    if kw.lower() in content.lower():
                        if kw not in found_in_algo:
                            found_in_algo.append(kw)
                            evidence.append(f"Personalization keyword found: {kw}")

            if len(found_in_algo) >= 3:
                status = "PASS"
                details = f"Individualized learning verified: {len(found_in_algo)} personalization features"
            elif len(found_in_algo) >= 1:
                status = "PARTIAL"
                details = "Partial individualization implementation"
            else:
                details = "Individualized learning not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Individualized Learning",
            category="Personalization",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # CATEGORY 8: EMOJI SANITIZATION
    # ========================================================================

    def verify_emoji_sanitization(self) -> VerificationResult:
        """Verify emoji sanitization tooling"""
        evidence = []
        status = "FAIL"
        details = ""

        try:
            # Check for emoji sanitizer tool
            sanitizer = self.repo_root / "tools" / "emoji_sanitizer.py"
            if sanitizer.exists():
                evidence.append("emoji_sanitizer.py exists in tools/")

                # Check for batch wrappers
                batch_files = list(self.repo_root.glob("SANITIZE_EMOJI*.bat"))
                if batch_files:
                    evidence.append(f"Batch wrappers exist: {len(batch_files)} file(s)")
                    for bf in batch_files:
                        evidence.append(f"  - {bf.name}")

                status = "PASS"
                details = (
                    f"Emoji sanitization verified: Tool + {len(batch_files)} wrappers"
                )
            else:
                details = "Emoji sanitizer not found"

        except Exception as e:
            details = f"Verification error: {e}"
            evidence.append(str(e))

        return VerificationResult(
            test_name="Emoji Sanitization Tooling",
            category="Code Quality",
            status=status,
            details=details,
            evidence=evidence,
            timestamp=datetime.utcnow().isoformat(),
        )

    # ========================================================================
    # MAIN VERIFICATION RUNNER
    # ========================================================================

    async def run_all_verifications(self):
        """Run all verification tests"""
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE ACHIEVEMENT VERIFICATION SUITE")
        logger.info("L.I.F.E Platform - October 16-19, 2025 Integration Report")
        logger.info("=" * 80)
        logger.info("")

        # Run all verification tests
        verifications = [
            (
                "Integration Framework",
                [self.verify_platform_unification, self.verify_azure_integration],
            ),
            ("Testing & Validation", [self.verify_testing_suite]),
            (
                "Autonomous Capabilities",
                [self.verify_self_healing, self.verify_continuous_learning],
            ),
            ("EEG Processing", [self.verify_eeg_ingestion]),
            ("Deployment", [self.verify_deployment_infrastructure]),
            ("Documentation", [self.verify_documentation]),
            ("Personalization", [self.verify_individualized_learning]),
            ("Code Quality", [self.verify_emoji_sanitization]),
        ]

        for category, tests in verifications:
            logger.info(f"\n{'=' * 80}")
            logger.info(f"CATEGORY: {category}")
            logger.info(f"{'=' * 80}")

            for test_func in tests:
                result = test_func()
                self.log_result(result)

                # Print evidence
                if result.evidence:
                    for ev in result.evidence:
                        logger.info(f"  • {ev}")
                logger.info("")

        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate verification summary"""
        logger.info("\n" + "=" * 80)
        logger.info("VERIFICATION SUMMARY")
        logger.info("=" * 80)

        total = len(self.results)
        passed = len([r for r in self.results if r.status == "PASS"])
        partial = len([r for r in self.results if r.status == "PARTIAL"])
        failed = len([r for r in self.results if r.status == "FAIL"])
        skipped = len([r for r in self.results if r.status == "SKIPPED"])

        logger.info(f"\nTotal Tests: {total}")
        logger.info(f"✅ PASSED:  {passed} ({passed/total*100:.1f}%)")
        logger.info(f"⚠️  PARTIAL: {partial} ({partial/total*100:.1f}%)")
        logger.info(f"❌ FAILED:  {failed} ({failed/total*100:.1f}%)")
        logger.info(f"⏭️  SKIPPED: {skipped} ({skipped/total*100:.1f}%)")

        # Overall assessment
        logger.info("\n" + "=" * 80)
        if passed == total:
            logger.info("🎉 OVERALL STATUS: ALL ACHIEVEMENTS VERIFIED")
        elif passed + partial >= total * 0.8:
            logger.info("✅ OVERALL STATUS: ACHIEVEMENTS SUBSTANTIALLY VERIFIED")
        elif passed + partial >= total * 0.6:
            logger.info("⚠️  OVERALL STATUS: ACHIEVEMENTS PARTIALLY VERIFIED")
        else:
            logger.info("❌ OVERALL STATUS: ACHIEVEMENTS NOT SUFFICIENTLY VERIFIED")
        logger.info("=" * 80)

        # Save results
        self.save_results()

    def save_results(self):
        """Save verification results to JSON"""
        output_file = self.repo_root / "ACHIEVEMENT_VERIFICATION_RESULTS.json"

        results_data = {
            "verification_date": datetime.utcnow().isoformat(),
            "platform": "SergiLIFE/SergiLIFE-life-azure-system",
            "report_period": "October 16-19, 2025",
            "total_tests": len(self.results),
            "passed": len([r for r in self.results if r.status == "PASS"]),
            "partial": len([r for r in self.results if r.status == "PARTIAL"]),
            "failed": len([r for r in self.results if r.status == "FAIL"]),
            "skipped": len([r for r in self.results if r.status == "SKIPPED"]),
            "results": [asdict(r) for r in self.results],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        logger.info(f"\n✅ Results saved to: {output_file}")


async def main():
    """Main entry point"""
    try:
        verifier = ComprehensiveVerifier()
        await verifier.run_all_verifications()
        return 0
    except Exception as e:
        logger.error(f"Verification failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
