"""
L.I.F.E Platform - Evidence Management System
Comprehensive evidence collection, validation, and documentation framework
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EvidenceManager:
    """Manages evidence collection and validation for L.I.F.E platform"""

    def __init__(self, evidence_path: str = None):
        self.evidence_path = (
            Path(evidence_path) if evidence_path else Path.cwd() / "evidence"
        )
        self.evidence_path.mkdir(exist_ok=True)
        self._create_evidence_structure()
        self.evidence_registry = self._load_evidence_registry()

    def _create_evidence_structure(self):
        """Create evidence directory structure"""
        directories = [
            "clinical_validation",
            "performance_benchmarks",
            "regulatory_compliance",
            "research_publications",
            "user_testimonials",
            "technical_documentation",
            "audit_trails",
            "quality_assurance",
        ]

        for directory in directories:
            (self.evidence_path / directory).mkdir(exist_ok=True)

    def _load_evidence_registry(self) -> Dict[str, Any]:
        """Load evidence registry"""
        registry_file = self.evidence_path / "evidence_registry.json"
        if registry_file.exists():
            with open(registry_file, "r") as f:
                return json.load(f)

        return {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "evidence_items": {},
            "validation_standards": self._get_validation_standards(),
            "compliance_frameworks": self._get_compliance_frameworks(),
        }

    def _save_evidence_registry(self):
        """Save evidence registry"""
        registry_file = self.evidence_path / "evidence_registry.json"
        self.evidence_registry["last_updated"] = datetime.now().isoformat()

        with open(registry_file, "w") as f:
            json.dump(self.evidence_registry, f, indent=2)

    def _get_validation_standards(self) -> Dict[str, Any]:
        """Define validation standards for different evidence types"""
        return {
            "clinical_validation": {
                "minimum_sample_size": 50,
                "statistical_significance": 0.05,
                "effect_size_threshold": 0.5,
                "required_controls": ["placebo", "baseline"],
                "duration_weeks": 12,
                "primary_endpoints": ["efficacy", "safety"],
            },
            "performance_benchmarks": {
                "accuracy_threshold": 0.95,
                "response_time_max": 200,  # milliseconds
                "uptime_requirement": 99.9,  # percentage
                "concurrent_users": 1000,
                "data_integrity": "SHA-256",
                "repeatability_trials": 100,
            },
            "regulatory_compliance": {
                "frameworks": ["FDA_510k", "CE_MDR", "ISO_13485", "ISO_14971"],
                "documentation_completeness": 100,  # percentage
                "audit_trail_integrity": "required",
                "risk_management": "mandatory",
                "post_market_surveillance": "continuous",
            },
            "research_publications": {
                "peer_review_status": "required",
                "impact_factor_min": 2.0,
                "replication_studies": 2,
                "open_access": "preferred",
                "data_availability": "mandatory",
            },
        }

    def _get_compliance_frameworks(self) -> Dict[str, Any]:
        """Define compliance frameworks"""
        return {
            "FDA_Medical_Device": {
                "classification": "Class II",
                "predicate_devices": ["EEG-based_BCI_systems"],
                "substantial_equivalence": "required",
                "clinical_data": "performance_testing",
                "quality_system": "ISO_13485",
            },
            "EU_MDR": {
                "classification": "Class IIa",
                "conformity_assessment": "Annex VII",
                "clinical_evaluation": "required",
                "post_market_surveillance": "mandatory",
                "unique_device_identification": "required",
            },
            "ISO_Standards": {
                "ISO_13485": "Quality Management Systems",
                "ISO_14971": "Risk Management",
                "ISO_62304": "Software Lifecycle",
                "ISO_27001": "Information Security",
            },
            "Privacy_Compliance": {
                "GDPR": "EU General Data Protection Regulation",
                "HIPAA": "Health Insurance Portability",
                "PIPEDA": "Personal Information Protection",
                "data_anonymization": "required",
            },
        }

    def add_evidence_item(
        self,
        evidence_type: str,
        title: str,
        description: str,
        file_path: str = None,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Add new evidence item"""

        evidence_id = self._generate_evidence_id(title)

        evidence_item = {
            "id": evidence_id,
            "type": evidence_type,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "validation_score": 0,
            "metadata": metadata or {},
            "file_references": [],
            "validation_history": [],
            "compliance_status": {},
        }

        # Add file reference if provided
        if file_path:
            file_ref = self._process_evidence_file(
                file_path, evidence_id, evidence_type
            )
            evidence_item["file_references"].append(file_ref)

        # Store evidence item
        self.evidence_registry["evidence_items"][evidence_id] = evidence_item
        self._save_evidence_registry()

        logger.info(f"Evidence item added: {title} ({evidence_id})")
        return evidence_id

    def _process_evidence_file(
        self, file_path: str, evidence_id: str, evidence_type: str
    ) -> Dict[str, Any]:
        """Process and store evidence file"""
        source_path = Path(file_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Evidence file not found: {file_path}")

        # Create evidence subdirectory
        evidence_dir = self.evidence_path / evidence_type / evidence_id
        evidence_dir.mkdir(parents=True, exist_ok=True)

        # Copy file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_file = evidence_dir / f"{timestamp}_{source_path.name}"

        # Calculate file hash for integrity
        file_hash = self._calculate_file_hash(source_path)

        # Copy file (in real implementation, would use shutil.copy2)
        # For now, just create a reference
        file_reference = {
            "original_path": str(source_path),
            "stored_path": str(dest_file),
            "file_hash": file_hash,
            "file_size": source_path.stat().st_size if source_path.exists() else 0,
            "mime_type": self._detect_mime_type(source_path),
            "added_at": datetime.now().isoformat(),
        }

        return file_reference

    def validate_evidence_item(self, evidence_id: str) -> Dict[str, Any]:
        """Validate evidence item against standards"""
        if evidence_id not in self.evidence_registry["evidence_items"]:
            return {"error": "Evidence item not found"}

        evidence_item = self.evidence_registry["evidence_items"][evidence_id]
        evidence_type = evidence_item["type"]

        # Get validation standards
        standards = self.evidence_registry["validation_standards"].get(
            evidence_type, {}
        )

        validation_result = {
            "evidence_id": evidence_id,
            "validation_timestamp": datetime.now().isoformat(),
            "criteria_met": [],
            "criteria_failed": [],
            "overall_score": 0,
            "recommendations": [],
        }

        # Validate based on evidence type
        if evidence_type == "clinical_validation":
            validation_result.update(
                self._validate_clinical_evidence(evidence_item, standards)
            )
        elif evidence_type == "performance_benchmarks":
            validation_result.update(
                self._validate_performance_evidence(evidence_item, standards)
            )
        elif evidence_type == "regulatory_compliance":
            validation_result.update(
                self._validate_regulatory_evidence(evidence_item, standards)
            )
        elif evidence_type == "research_publications":
            validation_result.update(
                self._validate_research_evidence(evidence_item, standards)
            )

        # Calculate overall score
        total_criteria = len(validation_result["criteria_met"]) + len(
            validation_result["criteria_failed"]
        )
        if total_criteria > 0:
            validation_result["overall_score"] = (
                len(validation_result["criteria_met"]) / total_criteria
            )

        # Update evidence item
        evidence_item["validation_history"].append(validation_result)
        evidence_item["validation_score"] = validation_result["overall_score"]
        evidence_item["status"] = (
            "validated"
            if validation_result["overall_score"] >= 0.8
            else "needs_improvement"
        )

        self._save_evidence_registry()

        return validation_result

    def _validate_clinical_evidence(
        self, evidence_item: Dict[str, Any], standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate clinical evidence"""
        result = {"criteria_met": [], "criteria_failed": [], "recommendations": []}

        metadata = evidence_item.get("metadata", {})

        # Check sample size
        sample_size = metadata.get("sample_size", 0)
        min_sample = standards.get("minimum_sample_size", 50)
        if sample_size >= min_sample:
            result["criteria_met"].append(
                f"Sample size adequate: {sample_size} >= {min_sample}"
            )
        else:
            result["criteria_failed"].append(
                f"Sample size insufficient: {sample_size} < {min_sample}"
            )
            result["recommendations"].append(
                "Increase sample size for statistical power"
            )

        # Check statistical significance
        p_value = metadata.get("p_value", 1.0)
        significance_threshold = standards.get("statistical_significance", 0.05)
        if p_value <= significance_threshold:
            result["criteria_met"].append(
                f"Statistical significance achieved: p={p_value}"
            )
        else:
            result["criteria_failed"].append(
                f"Not statistically significant: p={p_value}"
            )
            result["recommendations"].append("Review statistical analysis methodology")

        # Check study duration
        duration = metadata.get("duration_weeks", 0)
        min_duration = standards.get("duration_weeks", 12)
        if duration >= min_duration:
            result["criteria_met"].append(f"Study duration adequate: {duration} weeks")
        else:
            result["criteria_failed"].append(
                f"Study duration insufficient: {duration} weeks"
            )
            result["recommendations"].append(
                "Extend study duration for reliable results"
            )

        return result

    def _validate_performance_evidence(
        self, evidence_item: Dict[str, Any], standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate performance evidence"""
        result = {"criteria_met": [], "criteria_failed": [], "recommendations": []}

        metadata = evidence_item.get("metadata", {})

        # Check accuracy
        accuracy = metadata.get("accuracy", 0)
        min_accuracy = standards.get("accuracy_threshold", 0.95)
        if accuracy >= min_accuracy:
            result["criteria_met"].append(f"Accuracy meets standard: {accuracy:.3f}")
        else:
            result["criteria_failed"].append(f"Accuracy below standard: {accuracy:.3f}")
            result["recommendations"].append("Optimize algorithms for better accuracy")

        # Check response time
        response_time = metadata.get("response_time", 1000)
        max_response_time = standards.get("response_time_max", 200)
        if response_time <= max_response_time:
            result["criteria_met"].append(
                f"Response time acceptable: {response_time}ms"
            )
        else:
            result["criteria_failed"].append(
                f"Response time too high: {response_time}ms"
            )
            result["recommendations"].append("Optimize performance for faster response")

        # Check uptime
        uptime = metadata.get("uptime", 0)
        min_uptime = standards.get("uptime_requirement", 99.9)
        if uptime >= min_uptime:
            result["criteria_met"].append(f"Uptime meets requirement: {uptime}%")
        else:
            result["criteria_failed"].append(f"Uptime below requirement: {uptime}%")
            result["recommendations"].append(
                "Improve system reliability and monitoring"
            )

        return result

    def _validate_regulatory_evidence(
        self, evidence_item: Dict[str, Any], standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate regulatory evidence"""
        result = {"criteria_met": [], "criteria_failed": [], "recommendations": []}

        metadata = evidence_item.get("metadata", {})

        # Check documentation completeness
        completeness = metadata.get("documentation_completeness", 0)
        if completeness >= 100:
            result["criteria_met"].append("Documentation complete")
        else:
            result["criteria_failed"].append(
                f"Documentation incomplete: {completeness}%"
            )
            result["recommendations"].append("Complete all required documentation")

        # Check required frameworks
        frameworks = metadata.get("compliance_frameworks", [])
        required_frameworks = standards.get("frameworks", [])

        for framework in required_frameworks:
            if framework in frameworks:
                result["criteria_met"].append(f"Compliant with {framework}")
            else:
                result["criteria_failed"].append(f"Missing compliance: {framework}")
                result["recommendations"].append(f"Achieve {framework} compliance")

        return result

    def _validate_research_evidence(
        self, evidence_item: Dict[str, Any], standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate research evidence"""
        result = {"criteria_met": [], "criteria_failed": [], "recommendations": []}

        metadata = evidence_item.get("metadata", {})

        # Check peer review status
        peer_reviewed = metadata.get("peer_reviewed", False)
        if peer_reviewed:
            result["criteria_met"].append("Peer reviewed publication")
        else:
            result["criteria_failed"].append("Not peer reviewed")
            result["recommendations"].append("Submit to peer-reviewed journal")

        # Check impact factor
        impact_factor = metadata.get("impact_factor", 0)
        min_impact = standards.get("impact_factor_min", 2.0)
        if impact_factor >= min_impact:
            result["criteria_met"].append(f"High impact journal: IF={impact_factor}")
        else:
            result["criteria_failed"].append(f"Low impact factor: {impact_factor}")
            result["recommendations"].append("Target higher impact journals")

        return result

    def generate_evidence_report(self) -> Dict[str, Any]:
        """Generate comprehensive evidence report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_evidence_items": len(self.evidence_registry["evidence_items"]),
            "evidence_by_type": {},
            "validation_summary": {},
            "compliance_status": {},
            "recommendations": [],
        }

        # Analyze evidence by type
        for evidence_id, evidence_item in self.evidence_registry[
            "evidence_items"
        ].items():
            evidence_type = evidence_item["type"]

            if evidence_type not in report["evidence_by_type"]:
                report["evidence_by_type"][evidence_type] = {
                    "count": 0,
                    "validated": 0,
                    "average_score": 0,
                }

            report["evidence_by_type"][evidence_type]["count"] += 1

            if evidence_item["status"] == "validated":
                report["evidence_by_type"][evidence_type]["validated"] += 1

            # Calculate average validation score
            scores = [
                h["overall_score"] for h in evidence_item.get("validation_history", [])
            ]
            if scores:
                current_avg = report["evidence_by_type"][evidence_type]["average_score"]
                count = report["evidence_by_type"][evidence_type]["count"]
                new_avg = (current_avg * (count - 1) + max(scores)) / count
                report["evidence_by_type"][evidence_type]["average_score"] = new_avg

        # Overall validation summary
        all_items = list(self.evidence_registry["evidence_items"].values())
        validated_items = [item for item in all_items if item["status"] == "validated"]

        report["validation_summary"] = {
            "total_items": len(all_items),
            "validated_items": len(validated_items),
            "validation_rate": (
                len(validated_items) / len(all_items) if all_items else 0
            ),
            "average_validation_score": (
                sum(item["validation_score"] for item in all_items) / len(all_items)
                if all_items
                else 0
            ),
        }

        return report

    def _generate_evidence_id(self, title: str) -> str:
        """Generate unique evidence ID"""
        timestamp = str(int(datetime.now().timestamp()))
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        return f"EV_{timestamp}_{title_hash}"

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for integrity verification"""
        if not file_path.exists():
            return "file_not_found"

        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception:
            return "hash_calculation_failed"

    def _detect_mime_type(self, file_path: Path) -> str:
        """Detect MIME type based on file extension"""
        extension = file_path.suffix.lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".json": "application/json",
            ".csv": "text/csv",
            ".txt": "text/plain",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
        }
        return mime_types.get(extension, "application/octet-stream")


# Example usage and demonstration
if __name__ == "__main__":
    print("📋 L.I.F.E Platform - Evidence Management System")
    print("=" * 55)

    # Initialize evidence manager
    evidence_manager = EvidenceManager()

    # Add sample evidence items
    sample_evidence = [
        {
            "type": "clinical_validation",
            "title": "L.I.F.E Platform Clinical Trial Results",
            "description": "Multi-center randomized controlled trial demonstrating efficacy",
            "metadata": {
                "sample_size": 125,
                "p_value": 0.023,
                "duration_weeks": 16,
                "primary_endpoint": "learning_improvement",
                "effect_size": 0.73,
            },
        },
        {
            "type": "performance_benchmarks",
            "title": "EEG Processing Performance Validation",
            "description": "Comprehensive performance testing of EEG processing algorithms",
            "metadata": {
                "accuracy": 0.967,
                "response_time": 127,
                "uptime": 99.95,
                "concurrent_users": 1250,
                "test_duration_hours": 720,
            },
        },
        {
            "type": "regulatory_compliance",
            "title": "FDA 510(k) Submission Package",
            "description": "Complete regulatory submission for medical device clearance",
            "metadata": {
                "documentation_completeness": 98,
                "compliance_frameworks": ["FDA_510k", "ISO_13485", "ISO_14971"],
                "submission_date": "2025-01-15",
                "predicate_device": "EEG_BCI_System_v2",
            },
        },
        {
            "type": "research_publications",
            "title": "Adaptive Neural Learning Systems: A Breakthrough in BCI Technology",
            "description": "Peer-reviewed publication in Nature Neuroscience",
            "metadata": {
                "peer_reviewed": True,
                "impact_factor": 24.8,
                "journal": "Nature Neuroscience",
                "publication_date": "2024-12-01",
                "citations": 47,
            },
        },
    ]

    created_evidence = []

    # Create evidence items
    for evidence_data in sample_evidence:
        print(f"\n📋 Adding {evidence_data['title'][:40]}...")
        evidence_id = evidence_manager.add_evidence_item(
            evidence_data["type"],
            evidence_data["title"],
            evidence_data["description"],
            metadata=evidence_data["metadata"],
        )
        created_evidence.append(evidence_id)
        print(f"✅ Evidence added: {evidence_id}")

    # Validate evidence items
    print(f"\n🔍 Validating evidence items...")
    validation_results = []

    for evidence_id in created_evidence:
        result = evidence_manager.validate_evidence_item(evidence_id)
        validation_results.append(result)

        if "error" not in result:
            score = result["overall_score"]
            status = "✅ PASSED" if score >= 0.8 else "⚠️ NEEDS WORK"
            print(f"{status} {evidence_id[:15]}... Score: {score:.2f}")

    # Generate comprehensive report
    print(f"\n📊 Generating Evidence Report...")
    report = evidence_manager.generate_evidence_report()

    print(f"\n📈 Evidence Summary:")
    print("-" * 30)
    print(f"Total Evidence Items: {report['total_evidence_items']}")
    print(f"Validation Rate: {report['validation_summary']['validation_rate']:.1%}")
    print(
        f"Average Score: {report['validation_summary']['average_validation_score']:.3f}"
    )

    print(f"\n📂 Evidence by Type:")
    for evidence_type, data in report["evidence_by_type"].items():
        print(
            f"  {evidence_type:20} | {data['count']:2} items | {data['average_score']:.3f} avg score"
        )

    print(f"\n✅ Evidence Management System Ready!")
    print("📋 Use EvidenceManager.add_evidence_item() to add new evidence")
    print("🔍 Use EvidenceManager.validate_evidence_item() for validation")
    print("📊 Use EvidenceManager.generate_evidence_report() for reports")
