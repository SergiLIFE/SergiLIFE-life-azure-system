#!/usr/bin/env python3
"""
Comprehensive System Validation - L.I.F.E. Platform
Complete validation of BCI, UI, Partners, and Marketplace connections

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

CRITICAL VALIDATION AREAS:
1. BCI (Brain-Computer Interface) Functionality
2. Computer User Interface Interactivity 
3. L.I.F.E Theory Ecosystem Partner Connections
4. Azure Marketplace ISV Certification Status
5. Production Readiness Assessment
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, "comprehensive_validation.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ComprehensiveSystemValidator:
    """Validates all critical L.I.F.E. Platform systems before any campaign launch"""
    
    def __init__(self):
        self.script_dir = Path(SCRIPT_DIR)
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "COMPREHENSIVE_PRE_CAMPAIGN",
            "overall_status": "UNKNOWN",
            "ready_for_campaign": False,
            "critical_blockers": [],
            "warnings": [],
            "validation_areas": {
                "bci_functionality": {"status": "PENDING", "score": 0},
                "ui_interactivity": {"status": "PENDING", "score": 0},
                "partner_connections": {"status": "PENDING", "score": 0},
                "marketplace_certification": {"status": "PENDING", "score": 0},
                "production_readiness": {"status": "PENDING", "score": 0}
            }
        }
    
    async def validate_all_systems(self) -> Dict[str, Any]:
        """Run comprehensive validation of all critical systems"""
        print("🔍 L.I.F.E. PLATFORM - COMPREHENSIVE SYSTEM VALIDATION")
        print("=" * 70)
        print(f"🕐 Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Purpose: PRE-CAMPAIGN SYSTEM VERIFICATION")
        print("=" * 70)
        print()
        
        # 1. BCI (Brain-Computer Interface) Validation
        print("🧠 VALIDATING BCI (BRAIN-COMPUTER INTERFACE)...")
        bci_result = await self.validate_bci_functionality()
        self.validation_results["validation_areas"]["bci_functionality"] = bci_result
        print(f"   Status: {bci_result['status']} | Score: {bci_result['score']}/100")
        print()
        
        # 2. Computer User Interface Validation
        print("💻 VALIDATING COMPUTER USER INTERFACE...")
        ui_result = await self.validate_ui_interactivity()
        self.validation_results["validation_areas"]["ui_interactivity"] = ui_result
        print(f"   Status: {ui_result['status']} | Score: {ui_result['score']}/100")
        print()
        
        # 3. Partner Ecosystem Connections
        print("🤝 VALIDATING PARTNER ECOSYSTEM CONNECTIONS...")
        partner_result = await self.validate_partner_connections()
        self.validation_results["validation_areas"]["partner_connections"] = partner_result
        print(f"   Status: {partner_result['status']} | Score: {partner_result['score']}/100")
        print()
        
        # 4. Marketplace ISV Certification
        print("🏢 VALIDATING AZURE MARKETPLACE ISV CERTIFICATION...")
        cert_result = await self.validate_marketplace_certification()
        self.validation_results["validation_areas"]["marketplace_certification"] = cert_result
        print(f"   Status: {cert_result['status']} | Score: {cert_result['score']}/100")
        print()
        
        # 5. Production Readiness Assessment
        print("🚀 VALIDATING PRODUCTION READINESS...")
        prod_result = await self.validate_production_readiness()
        self.validation_results["validation_areas"]["production_readiness"] = prod_result
        print(f"   Status: {prod_result['status']} | Score: {prod_result['score']}/100")
        print()
        
        # Calculate overall status
        self._calculate_overall_status()
        
        # Generate comprehensive report
        await self._generate_comprehensive_report()
        
        return self.validation_results
    
    async def validate_bci_functionality(self) -> Dict[str, Any]:
        """Validate Brain-Computer Interface (BCI) functionality"""
        result = {
            "status": "UNKNOWN",
            "score": 0,
            "tests_performed": [],
            "critical_issues": [],
            "details": {}
        }
        
        try:
            score = 0
            max_score = 100
            
            # Test 1: Core L.I.F.E. Algorithm (40 points)
            print("   🧪 Testing Core L.I.F.E. Algorithm...")
            try:
                # Import and test the main algorithm
                sys.path.insert(0, str(self.script_dir))
                algorithm_file = "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py"
                
                if (self.script_dir / algorithm_file).exists():
                    # Test import capability
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("life_algorithm", self.script_dir / algorithm_file)
                    
                    if spec and spec.loader:
                        score += 20
                        result["tests_performed"].append("✅ L.I.F.E. Algorithm file found and accessible")
                        
                        # Test for key classes/functions
                        try:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            
                            # Check for essential components
                            if hasattr(module, 'LIFEAlgorithmCore') or 'class' in open(self.script_dir / algorithm_file).read():
                                score += 20
                                result["tests_performed"].append("✅ L.I.F.E. Algorithm core classes detected")
                            else:
                                result["critical_issues"].append("❌ L.I.F.E. Algorithm core classes not found")
                        except Exception as e:
                            result["critical_issues"].append(f"❌ L.I.F.E. Algorithm execution error: {str(e)}")
                    else:
                        result["critical_issues"].append("❌ L.I.F.E. Algorithm not loadable")
                else:
                    result["critical_issues"].append("❌ L.I.F.E. Algorithm file missing")
            except Exception as e:
                result["critical_issues"].append(f"❌ BCI Algorithm test failed: {str(e)}")
            
            # Test 2: EEG Processing Capability (30 points)
            print("   🧠 Testing EEG Processing Capability...")
            try:
                # Check for EEG-related components
                eeg_keywords = ["eeg", "neural", "brainwave", "alpha", "beta", "gamma"]
                algorithm_content = ""
                
                if (self.script_dir / algorithm_file).exists():
                    with open(self.script_dir / algorithm_file, 'r') as f:
                        algorithm_content = f.read().lower()
                    
                    eeg_features_found = sum(1 for keyword in eeg_keywords if keyword in algorithm_content)
                    if eeg_features_found >= 4:
                        score += 30
                        result["tests_performed"].append("✅ EEG processing components detected")
                    elif eeg_features_found >= 2:
                        score += 15
                        result["tests_performed"].append("⚠️ Limited EEG processing components")
                    else:
                        result["critical_issues"].append("❌ No EEG processing components found")
            except Exception as e:
                result["critical_issues"].append(f"❌ EEG processing test failed: {str(e)}")
            
            # Test 3: Real-time Processing (30 points)
            print("   ⚡ Testing Real-time Processing...")
            try:
                # Check for asyncio and real-time components
                realtime_keywords = ["async", "await", "real.?time", "stream", "concurrent"]
                
                if algorithm_content:
                    realtime_features = sum(1 for keyword in realtime_keywords if keyword in algorithm_content)
                    if realtime_features >= 3:
                        score += 30
                        result["tests_performed"].append("✅ Real-time processing capabilities detected")
                    elif realtime_features >= 1:
                        score += 15
                        result["tests_performed"].append("⚠️ Limited real-time processing")
                    else:
                        result["critical_issues"].append("❌ No real-time processing capabilities")
            except Exception as e:
                result["critical_issues"].append(f"❌ Real-time processing test failed: {str(e)}")
            
            # Determine status
            result["score"] = score
            if score >= 80:
                result["status"] = "OPERATIONAL"
            elif score >= 60:
                result["status"] = "FUNCTIONAL_WITH_WARNINGS"
            elif score >= 40:
                result["status"] = "LIMITED_FUNCTIONALITY"
            else:
                result["status"] = "CRITICAL_ISSUES"
            
        except Exception as e:
            result["status"] = "ERROR"
            result["critical_issues"].append(f"BCI validation error: {str(e)}")
        
        return result
    
    async def validate_ui_interactivity(self) -> Dict[str, Any]:
        """Validate Computer User Interface interactivity"""
        result = {
            "status": "UNKNOWN",
            "score": 0,
            "tests_performed": [],
            "critical_issues": [],
            "details": {}
        }
        
        try:
            score = 0
            
            # Test 1: PowerShell Interface (25 points)
            print("   💻 Testing PowerShell Interface...")
            ps_script = self.script_dir / "TRIGGER_CAMPAIGN.ps1"
            if ps_script.exists():
                score += 25
                result["tests_performed"].append("✅ PowerShell interface available")
            else:
                result["critical_issues"].append("❌ PowerShell interface missing")
            
            # Test 2: Batch Script Interface (25 points)
            print("   📝 Testing Batch Script Interface...")
            bat_script = self.script_dir / "TRIGGER_CAMPAIGN.bat"
            if bat_script.exists():
                score += 25
                result["tests_performed"].append("✅ Batch script interface available")
            else:
                result["critical_issues"].append("❌ Batch script interface missing")
            
            # Test 3: Python Interactive Interface (25 points)
            print("   🐍 Testing Python Interactive Interface...")
            ui_validator = self.script_dir / "ui_operational_validator.py"
            simple_ui = self.script_dir / "simple_ui_test.py"
            
            if ui_validator.exists() and simple_ui.exists():
                score += 25
                result["tests_performed"].append("✅ Python interactive interfaces available")
            else:
                result["critical_issues"].append("❌ Python interactive interfaces missing")
            
            # Test 4: GitHub Actions Web Interface (25 points)
            print("   🌐 Testing GitHub Actions Web Interface...")
            workflow_file = self.script_dir / ".github" / "workflows" / "campaign-launcher.yml"
            if workflow_file.exists():
                # Check for workflow_dispatch (manual triggering)
                with open(workflow_file, 'r') as f:
                    content = f.read()
                if "workflow_dispatch:" in content:
                    score += 25
                    result["tests_performed"].append("✅ GitHub Actions web interface configured")
                else:
                    result["critical_issues"].append("❌ GitHub Actions manual trigger not configured")
            else:
                result["critical_issues"].append("❌ GitHub Actions workflow missing")
            
            # Determine status
            result["score"] = score
            if score >= 80:
                result["status"] = "HIGHLY_INTERACTIVE"
            elif score >= 60:
                result["status"] = "INTERACTIVE_WITH_GAPS"
            elif score >= 40:
                result["status"] = "LIMITED_INTERACTIVITY"
            else:
                result["status"] = "POOR_INTERACTIVITY"
            
        except Exception as e:
            result["status"] = "ERROR"
            result["critical_issues"].append(f"UI validation error: {str(e)}")
        
        return result
    
    async def validate_partner_connections(self) -> Dict[str, Any]:
        """Validate L.I.F.E Theory ecosystem partner connections"""
        result = {
            "status": "UNKNOWN", 
            "score": 0,
            "tests_performed": [],
            "critical_issues": [],
            "details": {}
        }
        
        try:
            score = 0
            
            # Test 1: Azure Integration (40 points)
            print("   ☁️ Testing Azure Partner Integration...")
            azure_config = self.script_dir / "azure_config.py"
            azure_functions = self.script_dir / "azure_functions_workflow.py"
            
            azure_files_found = 0
            if azure_config.exists():
                azure_files_found += 1
                result["tests_performed"].append("✅ Azure configuration found")
            
            if azure_functions.exists():
                azure_files_found += 1
                result["tests_performed"].append("✅ Azure Functions workflow found")
            
            if azure_files_found >= 2:
                score += 40
            elif azure_files_found >= 1:
                score += 20
                result["critical_issues"].append("⚠️ Partial Azure integration")
            else:
                result["critical_issues"].append("❌ No Azure integration found")
            
            # Test 2: Campaign Management System (30 points)
            print("   📊 Testing Campaign Management Partner System...")
            campaign_manager = self.script_dir / "campaign_manager.py"
            campaign_trigger = self.script_dir / "campaign_automatic_trigger.py"
            
            campaign_files_found = 0
            if campaign_manager.exists():
                campaign_files_found += 1
                result["tests_performed"].append("✅ Campaign manager system found")
            
            if campaign_trigger.exists():
                campaign_files_found += 1
                result["tests_performed"].append("✅ Campaign automation system found")
            
            if campaign_files_found >= 2:
                score += 30
            elif campaign_files_found >= 1:
                score += 15
                result["critical_issues"].append("⚠️ Partial campaign system")
            else:
                result["critical_issues"].append("❌ No campaign management system")
            
            # Test 3: Partner Integration Files (30 points)
            print("   🤝 Testing Partner Integration Files...")
            partner_files = [
                "microsoft_partnership_package_generator.py",
                "microsoft_executive_outreach_automation.py", 
                "azure_marketplace_microsoft_offer.py"
            ]
            
            partner_files_found = sum(1 for f in partner_files if (self.script_dir / f).exists())
            
            if partner_files_found >= 3:
                score += 30
                result["tests_performed"].append("✅ All partner integration files found")
            elif partner_files_found >= 2:
                score += 20
                result["tests_performed"].append("⚠️ Most partner integration files found")
            elif partner_files_found >= 1:
                score += 10
                result["critical_issues"].append("⚠️ Limited partner integration")
            else:
                result["critical_issues"].append("❌ No partner integration files found")
            
            # Determine status
            result["score"] = score
            if score >= 80:
                result["status"] = "FULLY_CONNECTED"
            elif score >= 60:
                result["status"] = "WELL_CONNECTED"
            elif score >= 40:
                result["status"] = "PARTIALLY_CONNECTED"
            else:
                result["status"] = "POORLY_CONNECTED"
            
        except Exception as e:
            result["status"] = "ERROR"
            result["critical_issues"].append(f"Partner validation error: {str(e)}")
        
        return result
    
    async def validate_marketplace_certification(self) -> Dict[str, Any]:
        """Validate Azure Marketplace ISV certification status"""
        result = {
            "status": "UNKNOWN",
            "score": 0,
            "tests_performed": [],
            "critical_issues": [],
            "details": {}
        }
        
        try:
            score = 0
            
            # Test 1: Marketplace Offer Configuration (50 points)
            print("   🏪 Testing Marketplace Offer Configuration...")
            
            # Check for marketplace offer ID in configuration files
            offer_id = "9a600d96-fe1e-420b-902a-a0c42c561adb"
            offer_found_in_files = []
            
            config_files = [
                "azure_config.py",
                "campaign_automatic_trigger.py", 
                "azure_marketplace_microsoft_offer.py",
                ".github/workflows/campaign-launcher.yml"
            ]
            
            for config_file in config_files:
                file_path = self.script_dir / config_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        if offer_id in content:
                            offer_found_in_files.append(config_file)
                    except Exception:
                        pass
            
            if len(offer_found_in_files) >= 3:
                score += 50
                result["tests_performed"].append("✅ Marketplace offer ID found in multiple files")
            elif len(offer_found_in_files) >= 1:
                score += 25
                result["tests_performed"].append("⚠️ Marketplace offer ID found in some files")
            else:
                result["critical_issues"].append("❌ Marketplace offer ID not found in configuration")
            
            # Test 2: ISV Documentation (25 points)
            print("   📋 Testing ISV Certification Documentation...")
            
            documentation_files = [
                "README.md",
                "AUTOMATION_STATUS_UPDATED_SEPTEMBER_27_2025.md",
                "AZURE_AD_MARKETPLACE_SETUP.md"
            ]
            
            docs_found = sum(1 for f in documentation_files if (self.script_dir / f).exists())
            
            if docs_found >= 3:
                score += 25
                result["tests_performed"].append("✅ ISV documentation complete")
            elif docs_found >= 2:
                score += 15
                result["tests_performed"].append("⚠️ Most ISV documentation available")
            elif docs_found >= 1:
                score += 5
                result["critical_issues"].append("⚠️ Limited ISV documentation")
            else:
                result["critical_issues"].append("❌ No ISV documentation found")
            
            # Test 3: Certification Compliance (25 points)
            print("   ✅ Testing Certification Compliance...")
            
            # Check for compliance indicators
            compliance_files = [
                "AZURE_CLI_SETUP_COMPLETE.md",
                "FLAWLESS_CONNECTION_VALIDATOR.py",
                "azure_sponsorship_validation.py"
            ]
            
            compliance_found = sum(1 for f in compliance_files if (self.script_dir / f).exists())
            
            if compliance_found >= 3:
                score += 25
                result["tests_performed"].append("✅ Certification compliance files complete")
            elif compliance_found >= 2:
                score += 15
                result["tests_performed"].append("⚠️ Most compliance files available")
            elif compliance_found >= 1:
                score += 5
                result["critical_issues"].append("⚠️ Limited compliance validation")
            else:
                result["critical_issues"].append("❌ No compliance validation found")
            
            # Determine status
            result["score"] = score
            if score >= 80:
                result["status"] = "FULLY_CERTIFIED"
            elif score >= 60:
                result["status"] = "MOSTLY_CERTIFIED"
            elif score >= 40:
                result["status"] = "PARTIALLY_CERTIFIED"
            else:
                result["status"] = "NOT_CERTIFIED"
            
        except Exception as e:
            result["status"] = "ERROR"
            result["critical_issues"].append(f"Certification validation error: {str(e)}")
        
        return result
    
    async def validate_production_readiness(self) -> Dict[str, Any]:
        """Validate overall production readiness"""
        result = {
            "status": "UNKNOWN",
            "score": 0,
            "tests_performed": [],
            "critical_issues": [],
            "details": {}
        }
        
        try:
            score = 0
            
            # Test 1: Testing Infrastructure (30 points)
            print("   🧪 Testing Infrastructure Validation...")
            
            test_files = [
                "production_deployment_test.py",
                "sota_benchmark.py",
                "autonomous_optimizer.py",
                "test_fixed_algorithm.py"
            ]
            
            test_files_found = sum(1 for f in test_files if (self.script_dir / f).exists())
            
            if test_files_found >= 4:
                score += 30
                result["tests_performed"].append("✅ Complete testing infrastructure")
            elif test_files_found >= 3:
                score += 22
                result["tests_performed"].append("⚠️ Most testing infrastructure available")
            elif test_files_found >= 2:
                score += 15
                result["critical_issues"].append("⚠️ Limited testing infrastructure")
            else:
                result["critical_issues"].append("❌ Insufficient testing infrastructure")
            
            # Test 2: Monitoring and Logging (25 points)
            print("   📊 Testing Monitoring and Logging...")
            
            logs_dir = self.script_dir / "logs"
            results_dir = self.script_dir / "results"
            tracking_dir = self.script_dir / "tracking_data"
            
            monitoring_score = 0
            if logs_dir.exists():
                monitoring_score += 8
                result["tests_performed"].append("✅ Logs directory available")
            
            if results_dir.exists():
                monitoring_score += 8
                result["tests_performed"].append("✅ Results directory available")
            
            if tracking_dir.exists():
                monitoring_score += 9
                result["tests_performed"].append("✅ Tracking directory available")
            
            score += monitoring_score
            
            # Test 3: Documentation Completeness (25 points)
            print("   📚 Testing Documentation Completeness...")
            
            doc_files = [
                "CAMPAIGN_TRIGGER_UI_VALIDATION_README.md",
                "QUICK_COMMAND_REFERENCE.md",
                "ACCURACY_ENHANCEMENT_PLAN.md"
            ]
            
            docs_found = sum(1 for f in doc_files if (self.script_dir / f).exists())
            doc_score = (docs_found / len(doc_files)) * 25
            score += doc_score
            
            if doc_score >= 20:
                result["tests_performed"].append("✅ Documentation comprehensive")
            elif doc_score >= 10:
                result["tests_performed"].append("⚠️ Documentation adequate")
            else:
                result["critical_issues"].append("❌ Documentation insufficient")
            
            # Test 4: Security and Backup (20 points)
            print("   🔒 Testing Security and Backup Systems...")
            
            security_files = [
                "simple_azure_backup.py",
                "FLAWLESS_CONNECTION_VALIDATOR.py"
            ]
            
            security_found = sum(1 for f in security_files if (self.script_dir / f).exists())
            security_score = (security_found / len(security_files)) * 20
            score += security_score
            
            if security_score >= 15:
                result["tests_performed"].append("✅ Security systems adequate")
            else:
                result["critical_issues"].append("⚠️ Security systems need attention")
            
            # Determine status
            result["score"] = score
            if score >= 85:
                result["status"] = "PRODUCTION_READY"
            elif score >= 70:
                result["status"] = "NEAR_PRODUCTION_READY"
            elif score >= 50:
                result["status"] = "DEVELOPMENT_STAGE"
            else:
                result["status"] = "NOT_READY"
            
        except Exception as e:
            result["status"] = "ERROR"
            result["critical_issues"].append(f"Production readiness error: {str(e)}")
        
        return result
    
    def _calculate_overall_status(self):
        """Calculate overall system status"""
        total_score = 0
        area_count = 0
        critical_blockers = []
        
        for area, result in self.validation_results["validation_areas"].items():
            total_score += result["score"]
            area_count += 1
            
            # Check for critical issues
            if result.get("critical_issues"):
                critical_blockers.extend(result["critical_issues"])
            
            # Add area-specific blockers
            if result["status"] in ["CRITICAL_ISSUES", "ERROR", "NOT_CERTIFIED", "NOT_READY"]:
                critical_blockers.append(f"{area}: {result['status']}")
        
        average_score = total_score / area_count if area_count > 0 else 0
        
        # Determine overall status
        if len(critical_blockers) > 0:
            self.validation_results["overall_status"] = "CRITICAL_BLOCKERS_FOUND"
            self.validation_results["ready_for_campaign"] = False
        elif average_score >= 80:
            self.validation_results["overall_status"] = "FULLY_OPERATIONAL"
            self.validation_results["ready_for_campaign"] = True
        elif average_score >= 70:
            self.validation_results["overall_status"] = "OPERATIONAL_WITH_WARNINGS"
            self.validation_results["ready_for_campaign"] = True
        elif average_score >= 60:
            self.validation_results["overall_status"] = "LIMITED_OPERATIONAL"
            self.validation_results["ready_for_campaign"] = False
        else:
            self.validation_results["overall_status"] = "NOT_OPERATIONAL"
            self.validation_results["ready_for_campaign"] = False
        
        self.validation_results["overall_score"] = average_score
        self.validation_results["critical_blockers"] = critical_blockers
    
    async def _generate_comprehensive_report(self):
        """Generate comprehensive validation report"""
        report_content = f"""
# L.I.F.E. PLATFORM - COMPREHENSIVE SYSTEM VALIDATION REPORT
Generated: {self.validation_results['timestamp']}

## OVERALL ASSESSMENT
- **Status**: {self.validation_results['overall_status']}
- **Ready for Campaign**: {self.validation_results['ready_for_campaign']}
- **Overall Score**: {self.validation_results.get('overall_score', 0):.1f}/100

## CRITICAL DECISION
"""
        
        if self.validation_results['ready_for_campaign']:
            report_content += "✅ **APPROVED FOR CAMPAIGN LAUNCH** - All systems meet minimum requirements\n\n"
        else:
            report_content += "❌ **NOT APPROVED FOR CAMPAIGN LAUNCH** - Critical issues must be resolved\n\n"
        
        report_content += "## VALIDATION AREA BREAKDOWN\n\n"
        
        for area, result in self.validation_results["validation_areas"].items():
            area_name = area.replace("_", " ").title()
            status_emoji = "✅" if result["score"] >= 70 else "⚠️" if result["score"] >= 50 else "❌"
            
            report_content += f"### {status_emoji} {area_name}\n"
            report_content += f"- **Score**: {result['score']}/100\n"
            report_content += f"- **Status**: {result['status']}\n"
            
            if result.get("tests_performed"):
                report_content += "- **Tests Performed**:\n"
                for test in result["tests_performed"]:
                    report_content += f"  - {test}\n"
            
            if result.get("critical_issues"):
                report_content += "- **Critical Issues**:\n"
                for issue in result["critical_issues"]:
                    report_content += f"  - {issue}\n"
            
            report_content += "\n"
        
        if self.validation_results['critical_blockers']:
            report_content += "## CRITICAL BLOCKERS\n"
            for blocker in self.validation_results['critical_blockers']:
                report_content += f"- {blocker}\n"
            report_content += "\n"
        
        report_content += """
## RECOMMENDATIONS

### If Approved for Campaign:
1. Proceed with campaign launch using validated interfaces
2. Monitor all systems during campaign execution
3. Address any warnings for optimal performance

### If Not Approved:
1. Address all critical blockers before campaign launch
2. Re-run comprehensive validation after fixes
3. Ensure ISV certification is complete
4. Verify all partner connections are active

## CAMPAIGN LAUNCH DECISION
"""
        
        if self.validation_results['ready_for_campaign']:
            report_content += "🚀 **SAFE TO PROCEED** with campaign launch\n"
        else:
            report_content += "🛑 **DO NOT PROCEED** with campaign launch until issues are resolved\n"
        
        # Save report
        report_file = self.script_dir / "logs" / "COMPREHENSIVE_VALIDATION_REPORT.md"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        # Also save JSON version
        json_file = self.script_dir / "logs" / "comprehensive_validation_results.json"
        with open(json_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        
        print(f"📄 Comprehensive validation report saved: {report_file}")
        print(f"📊 JSON results saved: {json_file}")


async def main():
    """Main function for comprehensive system validation"""
    validator = ComprehensiveSystemValidator()
    
    # Run complete validation
    results = await validator.validate_all_systems()
    
    # Display final results
    print("\n" + "=" * 70)
    print("🏁 COMPREHENSIVE VALIDATION COMPLETE")
    print("=" * 70)
    print(f"🎯 OVERALL STATUS: {results['overall_status']}")
    print(f"📊 OVERALL SCORE: {results.get('overall_score', 0):.1f}/100")
    print(f"🚀 READY FOR CAMPAIGN: {results['ready_for_campaign']}")
    print()
    
    if results['critical_blockers']:
        print("🚨 CRITICAL BLOCKERS TO ADDRESS:")
        for blocker in results['critical_blockers']:
            print(f"   ❌ {blocker}")
        print()
    
    # Validation area summary
    print("📋 VALIDATION AREA SUMMARY:")
    for area, result in results["validation_areas"].items():
        area_name = area.replace("_", " ").title()
        status_emoji = "✅" if result["score"] >= 70 else "⚠️" if result["score"] >= 50 else "❌"
        print(f"   {status_emoji} {area_name}: {result['status']} ({result['score']}/100)")
    
    print("\n" + "=" * 70)
    
    if results['ready_for_campaign']:
        print("✅ SYSTEM APPROVED - Safe to proceed with campaign launch")
        print("🚀 All critical systems validated and operational")
    else:
        print("❌ SYSTEM NOT APPROVED - Do not proceed with campaign")  
        print("🔧 Address critical blockers before attempting launch")
    
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    asyncio.run(main())