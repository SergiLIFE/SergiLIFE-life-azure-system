# L.I.F.E Platform - KPI Monitoring System Enhancement
# Document & Compliance Integrity Monitoring

"""
Enhanced KPI monitoring to track document integrity, operational status,
and compliance document health to prevent corruption/contamination.
"""

import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class ComplianceDocumentMonitor:
    """Monitor compliance documents for integrity and operational status"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.compliance_docs = [
            "LIFE_PLATFORM_COMPLIANCE_REPORT_2025.md",
            "PRIVACY_POLICY.md", 
            "TERMS_OF_SERVICE.md",
            "AZURE_OIDC_SETUP.md",
            "setup-azure-oidc.ps1",
            "azure_config.py",
            "production_deployment_test.py"
        ]
        self.secure_backup_path = self.base_path / "COMPLIANCE_BACKUP_SECURE"
        self.monitoring_log = self.base_path / "logs" / "compliance_monitor.log"
        
        # Ensure directories exist
        os.makedirs(self.secure_backup_path, exist_ok=True)
        os.makedirs(self.base_path / "logs", exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            filename=self.monitoring_log,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate SHA-256 hash of file for integrity checking"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    def monitor_document_integrity(self) -> Dict[str, Any]:
        """Monitor all compliance documents for integrity and corruption"""
        integrity_report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "documents": {},
            "overall_status": "OPERATIONAL",
            "issues": [],
            "backup_status": "SECURED"
        }
        
        for doc_name in self.compliance_docs:
            doc_path = self.base_path / doc_name
            backup_path = self.secure_backup_path / f"{doc_name}.backup"
            
            doc_status = {
                "exists": doc_path.exists(),
                "size": 0,
                "hash": None,
                "last_modified": None,
                "backup_exists": backup_path.exists(),
                "status": "UNKNOWN"
            }
            
            if doc_path.exists():
                try:
                    stat = doc_path.stat()
                    doc_status.update({
                        "size": stat.st_size,
                        "hash": self.calculate_file_hash(doc_path),
                        "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "status": "OPERATIONAL" if stat.st_size > 0 else "CORRUPTED"
                    })
                    
                    # Check for corruption indicators
                    if stat.st_size == 0:
                        integrity_report["issues"].append(f"{doc_name}: File is empty (corrupted)")
                        integrity_report["overall_status"] = "CRITICAL"
                    elif stat.st_size < 100:  # Suspiciously small
                        integrity_report["issues"].append(f"{doc_name}: File unusually small ({stat.st_size} bytes)")
                        
                except Exception as e:
                    doc_status["status"] = "ERROR"
                    integrity_report["issues"].append(f"{doc_name}: Error accessing file - {e}")
            else:
                doc_status["status"] = "MISSING"
                integrity_report["issues"].append(f"{doc_name}: File missing")
                integrity_report["overall_status"] = "CRITICAL"
                
            integrity_report["documents"][doc_name] = doc_status
        
        # Log the report
        self.logger.info(f"Document integrity check completed: {integrity_report['overall_status']}")
        if integrity_report["issues"]:
            for issue in integrity_report["issues"]:
                self.logger.warning(f"Integrity issue: {issue}")
                
        return integrity_report

    def create_secure_backups(self) -> bool:
        """Create secure backups of all compliance documents"""
        try:
            backup_manifest = {
                "created": datetime.datetime.now().isoformat(),
                "backups": {}
            }
            
            for doc_name in self.compliance_docs:
                doc_path = self.base_path / doc_name
                if doc_path.exists():
                    backup_path = self.secure_backup_path / f"{doc_name}.backup"
                    
                    # Copy file to secure backup
                    with open(doc_path, 'rb') as src, open(backup_path, 'wb') as dst:
                        dst.write(src.read())
                    
                    # Record backup info
                    backup_manifest["backups"][doc_name] = {
                        "backup_path": str(backup_path),
                        "original_hash": self.calculate_file_hash(doc_path),
                        "backup_hash": self.calculate_file_hash(backup_path),
                        "size": doc_path.stat().st_size
                    }
            
            # Save manifest
            manifest_path = self.secure_backup_path / "backup_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(backup_manifest, f, indent=2)
                
            self.logger.info(f"Secure backups created for {len(backup_manifest['backups'])} documents")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating secure backups: {e}")
            return False

    def restore_from_backup(self, document_name: str) -> bool:
        """Restore a document from secure backup"""
        try:
            backup_path = self.secure_backup_path / f"{document_name}.backup"
            original_path = self.base_path / document_name
            
            if not backup_path.exists():
                self.logger.error(f"No backup found for {document_name}")
                return False
            
            # Restore from backup
            with open(backup_path, 'rb') as src, open(original_path, 'wb') as dst:
                dst.write(src.read())
            
            self.logger.info(f"Successfully restored {document_name} from backup")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring {document_name}: {e}")
            return False

    def marketplace_launch_status(self) -> Dict[str, Any]:
        """Check marketplace launch readiness status"""
        launch_status = {
            "timestamp": datetime.datetime.now().isoformat(),
            "launch_date": "2025-09-27",
            "readiness": "READY",
            "critical_documents": {},
            "email_verification": "PENDING",
            "issues": []
        }
        
        # Critical documents for marketplace launch
        critical_docs = [
            "LIFE_PLATFORM_COMPLIANCE_REPORT_2025.md",
            "PRIVACY_POLICY.md",
            "azure_config.py"
        ]
        
        for doc in critical_docs:
            doc_path = self.base_path / doc
            if doc_path.exists() and doc_path.stat().st_size > 0:
                launch_status["critical_documents"][doc] = "READY"
            else:
                launch_status["critical_documents"][doc] = "MISSING/CORRUPTED"
                launch_status["readiness"] = "NOT_READY"
                launch_status["issues"].append(f"Critical document {doc} missing or corrupted")
        
        # Email verification status
        launch_status["email_verification_action"] = {
            "required": "Update Partner Center email from Info@lifecoach121.com to sergio@lifecoach-121.com",
            "status": "PENDING_USER_ACTION",
            "next_steps": [
                "Go to Partner Center Dashboard",
                "Update Primary Contact Email to sergio@lifecoach-121.com", 
                "Click 'Resend' verification email",
                "Check email for 'Action needed: Verify your email account with Microsoft'"
            ]
        }
        
        return launch_status

# Integration with existing KPI monitoring
def add_compliance_monitoring_to_kpi():
    """Add compliance document monitoring to existing KPI system"""
    
    monitor = ComplianceDocumentMonitor()
    
    # Run integrity check
    integrity_report = monitor.monitor_document_integrity()
    
    # Create secure backups
    backup_success = monitor.create_secure_backups()
    
    # Check launch readiness
    launch_status = monitor.marketplace_launch_status()
    
    # Combined KPI report
    kpi_compliance_report = {
        "compliance_monitoring": {
            "document_integrity": integrity_report,
            "backup_status": "SUCCESS" if backup_success else "FAILED",
            "launch_readiness": launch_status,
            "monitoring_active": True,
            "last_check": datetime.datetime.now().isoformat()
        }
    }
    
    return kpi_compliance_report

if __name__ == "__main__":
    # Run compliance monitoring
    print("🔍 L.I.F.E Platform - Compliance Document Monitoring")
    print("=" * 60)
    
    monitor = ComplianceDocumentMonitor()
    
    # 1. Check document integrity
    print("\n📋 Checking document integrity...")
    integrity = monitor.monitor_document_integrity()
    print(f"Overall Status: {integrity['overall_status']}")
    if integrity['issues']:
        print("⚠️  Issues found:")
        for issue in integrity['issues']:
            print(f"   - {issue}")
    else:
        print("✅ All documents operational")
    
    # 2. Create secure backups
    print("\n💾 Creating secure backups...")
    backup_result = monitor.create_secure_backups()
    print(f"Backup Status: {'✅ SUCCESS' if backup_result else '❌ FAILED'}")
    
    # 3. Check marketplace launch readiness  
    print("\n🚀 Checking marketplace launch readiness...")
    launch = monitor.marketplace_launch_status()
    print(f"Launch Readiness: {launch['readiness']}")
    print(f"Email Verification: {launch['email_verification']}")
    
    if launch['issues']:
        print("⚠️  Launch blockers:")
        for issue in launch['issues']:
            print(f"   - {issue}")
    
    print("\n" + "=" * 60)
    print("🎯 NEXT ACTION: Update Partner Center email to sergio@lifecoach-121.com")
    print("📧 Then resend verification email and check inbox!")
    print("🚀 You're almost at the finish line!")    print("🚀 You're almost at the finish line!")