"""
L.I.F.E Platform - Artifacts Management System
Integrates build artifacts, test results, and deployment packages

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import hashlib
import json
import logging
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArtifactsManager:
    """Manages build artifacts, test results, and deployment packages"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd() / "artifacts"
        self.config = self._load_config()
        self._ensure_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Load artifacts configuration"""
        return {
            "version": "1.0.0",
            "retention_days": 30,
            "compression": True,
            "categories": {
                "builds": "Build outputs and compiled assets",
                "tests": "Test results and coverage reports",
                "deployments": "Deployment packages and configs",
                "documentation": "Generated docs and reports",
                "models": "ML models and weights",
                "data": "Processed datasets and samples",
            },
            "file_patterns": {
                "builds": ["*.exe", "*.dll", "*.so", "*.jar", "*.war"],
                "tests": ["test_*.xml", "*_results.json", "coverage.xml"],
                "deployments": ["*.zip", "*.tar.gz", "deployment_*.json"],
                "documentation": ["*.pdf", "*.html", "docs_*.zip"],
                "models": ["*.pkl", "*.h5", "*.onnx", "*.pt"],
                "data": ["*.csv", "*.json", "processed_*.npy"],
            },
        }

    def _ensure_directories(self):
        """Create necessary artifact directories"""
        for category in self.config["categories"]:
            (self.base_path / category).mkdir(parents=True, exist_ok=True)

        # Create metadata directory
        (self.base_path / "metadata").mkdir(parents=True, exist_ok=True)

    def store_artifact(
        self, file_path: str, category: str, metadata: Dict[str, Any] = None
    ) -> str:
        """Store an artifact with metadata"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {file_path}")

            # Generate unique artifact ID
            artifact_id = self._generate_artifact_id(source_path)

            # Create destination path
            dest_dir = self.base_path / category
            dest_path = dest_dir / f"{artifact_id}_{source_path.name}"

            # Copy file
            shutil.copy2(source_path, dest_path)

            # Store metadata
            artifact_metadata = {
                "id": artifact_id,
                "original_path": str(source_path),
                "stored_path": str(dest_path),
                "category": category,
                "size": source_path.stat().st_size,
                "checksum": self._calculate_checksum(source_path),
                "created_at": datetime.now().isoformat(),
                "metadata": metadata or {},
            }

            self._save_metadata(artifact_id, artifact_metadata)

            logger.info(f"Artifact stored: {artifact_id} in {category}")
            return artifact_id

        except Exception as e:
            logger.error(f"Error storing artifact: {str(e)}")
            raise

    def retrieve_artifact(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve artifact metadata and path"""
        try:
            metadata_path = self.base_path / "metadata" / f"{artifact_id}.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error retrieving artifact {artifact_id}: {str(e)}")
            return None

    def list_artifacts(self, category: str = None) -> List[Dict[str, Any]]:
        """List all artifacts or by category"""
        artifacts = []
        metadata_dir = self.base_path / "metadata"

        for metadata_file in metadata_dir.glob("*.json"):
            try:
                with open(metadata_file, "r") as f:
                    artifact = json.load(f)
                    if category is None or artifact.get("category") == category:
                        artifacts.append(artifact)
            except Exception as e:
                logger.error(f"Error reading metadata {metadata_file}: {str(e)}")

        return sorted(artifacts, key=lambda x: x.get("created_at", ""), reverse=True)

    def cleanup_old_artifacts(self, days: int = None) -> int:
        """Remove artifacts older than specified days"""
        days = days or self.config["retention_days"]
        cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)
        cleaned_count = 0

        for artifact in self.list_artifacts():
            try:
                created_at = datetime.fromisoformat(artifact["created_at"]).timestamp()
                if created_at < cutoff_date:
                    self.delete_artifact(artifact["id"])
                    cleaned_count += 1
            except Exception as e:
                logger.error(f"Error cleaning artifact {artifact['id']}: {str(e)}")

        logger.info(f"Cleaned {cleaned_count} old artifacts")
        return cleaned_count

    def delete_artifact(self, artifact_id: str) -> bool:
        """Delete an artifact and its metadata"""
        try:
            artifact = self.retrieve_artifact(artifact_id)
            if not artifact:
                return False

            # Remove file
            stored_path = Path(artifact["stored_path"])
            if stored_path.exists():
                stored_path.unlink()

            # Remove metadata
            metadata_path = self.base_path / "metadata" / f"{artifact_id}.json"
            if metadata_path.exists():
                metadata_path.unlink()

            logger.info(f"Artifact deleted: {artifact_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting artifact {artifact_id}: {str(e)}")
            return False

    def create_deployment_package(
        self, files: List[str], package_name: str, metadata: Dict[str, Any] = None
    ) -> str:
        """Create a deployment package from multiple files"""
        try:
            package_path = self.base_path / "deployments" / f"{package_name}.zip"

            with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    source_path = Path(file_path)
                    if source_path.exists():
                        if source_path.is_file():
                            zipf.write(source_path, source_path.name)
                        elif source_path.is_dir():
                            for file in source_path.rglob("*"):
                                if file.is_file():
                                    arcname = file.relative_to(source_path.parent)
                                    zipf.write(file, arcname)

            # Store as artifact
            package_metadata = {
                "type": "deployment_package",
                "files_included": len(files),
                "package_size": package_path.stat().st_size,
                **(metadata or {}),
            }

            artifact_id = self.store_artifact(
                str(package_path), "deployments", package_metadata
            )

            logger.info(f"Deployment package created: {package_name}")
            return artifact_id

        except Exception as e:
            logger.error(f"Error creating deployment package: {str(e)}")
            raise

    def generate_artifact_report(self) -> Dict[str, Any]:
        """Generate comprehensive artifacts report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_artifacts": 0,
            "total_size": 0,
            "categories": {},
            "recent_artifacts": [],
        }

        all_artifacts = self.list_artifacts()
        report["total_artifacts"] = len(all_artifacts)

        for artifact in all_artifacts:
            # Count by category
            category = artifact.get("category", "unknown")
            if category not in report["categories"]:
                report["categories"][category] = {"count": 0, "total_size": 0}

            report["categories"][category]["count"] += 1
            report["categories"][category]["total_size"] += artifact.get("size", 0)
            report["total_size"] += artifact.get("size", 0)

        # Get recent artifacts (last 10)
        report["recent_artifacts"] = all_artifacts[:10]

        return report

    def _generate_artifact_id(self, file_path: Path) -> str:
        """Generate unique artifact ID"""
        timestamp = str(int(datetime.now().timestamp()))
        file_hash = self._calculate_checksum(file_path)[:8]
        return f"{timestamp}_{file_hash}"

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def _save_metadata(self, artifact_id: str, metadata: Dict[str, Any]):
        """Save artifact metadata"""
        metadata_path = self.base_path / "metadata" / f"{artifact_id}.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)


# Integration with L.I.F.E Platform
class LIFEArtifactsIntegration:
    """Integrates artifacts management with L.I.F.E platform"""

    def __init__(self):
        self.artifacts_manager = ArtifactsManager()
        self.life_artifacts = {
            "models": [
                "lifetheory.py",
                "eeg_processor.py",
                "quantum_life_processor.py",
            ],
            "modules": [
                "life_module1_signal_processing.py",
                "life_module2_pattern_recognition.py",
                "life_module3_cognitive_behavioral.py",
                "life_module4_adaptive_neural_networks.py",
                "life_module5_realtime_processing.py",
            ],
            "tests": [
                "comprehensive_life_test.py",
                "comprehensive_life_test_extended.py",
            ],
            "configs": ["azure_config.py", "azure.yaml"],
            "deployment": ["azure_functions_workflow.py"],
        }

    def archive_life_platform(self) -> str:
        """Create comprehensive L.I.F.E platform archive"""
        files_to_archive = []

        # Collect all L.I.F.E files
        for category, files in self.life_artifacts.items():
            for file in files:
                file_path = Path.cwd() / file
                if file_path.exists():
                    files_to_archive.append(str(file_path))

        # Create deployment package
        package_metadata = {
            "platform": "L.I.F.E",
            "version": "1.0.0",
            "components": len(files_to_archive),
            "description": "Complete L.I.F.E platform deployment package",
        }

        return self.artifacts_manager.create_deployment_package(
            files_to_archive,
            f"life_platform_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            package_metadata,
        )

    def store_test_results(self, test_file: str, results: Dict[str, Any]) -> str:
        """Store test results as artifacts"""
        results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_path = Path.cwd() / results_file

        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)

        metadata = {
            "test_type": "L.I.F.E platform validation",
            "test_file": test_file,
            "success_rate": results.get("success_rate", 0),
            "total_tests": results.get("total_tests", 0),
        }

        artifact_id = self.artifacts_manager.store_artifact(
            str(results_path), "tests", metadata
        )

        # Cleanup temporary file
        results_path.unlink()

        return artifact_id


# Example usage and demonstration
if __name__ == "__main__":
    print("🗂️ L.I.F.E Platform - Artifacts Management System")
    print("=" * 50)

    # Initialize artifacts manager
    artifacts = ArtifactsManager()
    life_integration = LIFEArtifactsIntegration()

    try:
        # Generate report
        report = artifacts.generate_artifact_report()
        print(f"📊 Total Artifacts: {report['total_artifacts']}")
        print(f"💾 Total Size: {report['total_size']:,} bytes")
        print(f"📂 Categories: {list(report['categories'].keys())}")

        # Create L.I.F.E platform archive if files exist
        life_files_exist = any(
            Path.cwd() / file
            for files in life_integration.life_artifacts.values()
            for file in files
            if (Path.cwd() / file).exists()
        )

        if life_files_exist:
            print("\n🚀 Creating L.I.F.E Platform Archive...")
            archive_id = life_integration.archive_life_platform()
            print(f"✅ Archive created with ID: {archive_id}")

        print("\n✅ Artifacts Management System Ready!")
        print("📦 Use ArtifactsManager for build artifact management")
        print("🔧 Use LIFEArtifactsIntegration for platform-specific operations")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
