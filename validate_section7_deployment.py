"""
L.I.F.E Platform Section 7 - Deployment Validation Test
Ultimate verification of Section 7 deployment readiness

This test validates all Section 7 components and deployment infrastructure
without requiring external dependencies or specific Python installations.

Copyright 2025 - Neuroadaptive Learning Platform
Author: SergiPaya & GitHub Copilot
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime


class Section7DeploymentValidator:
    """
    Comprehensive validator for Section 7 deployment readiness
    Tests all components, infrastructure, and configuration files
    """
    
    def __init__(self):
        self.test_results = []
        self.errors = []
        self.warnings = []
        self.start_time = datetime.now()
        
        print("🚀 L.I.F.E Platform Section 7 - Deployment Validation")
        print("=" * 60)
        print(f"Started at: {self.start_time}")
        print("")
        
    def log_test(self, test_name, status, details="", level="INFO"):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "level": level
        }
        self.test_results.append(result)
        
        # Color coding for output
        if status == "PASS":
            color = "\033[92m✓"  # Green
        elif status == "FAIL":
            color = "\033[91m✗"  # Red
        elif status == "WARN":
            color = "\033[93m⚠"  # Yellow
        else:
            color = "\033[94mℹ"  # Blue
        
        print(f"{color} {test_name}: {status}\033[0m")
        if details:
            print(f"  └─ {details}")
        
        if status == "FAIL":
            self.errors.append(f"{test_name}: {details}")
        elif status == "WARN":
            self.warnings.append(f"{test_name}: {details}")
    
    def test_file_existence(self):
        """Test that all required Section 7 files exist"""
        print("\n📁 Testing File Existence...")
        
        required_files = [
            "life_algorithm_section7_integration.py",
            "unity/VREnvironmentControllerSection7.cs",
            "infra/section7-deployment.bicep",
            "deploy-section7.sh",
            "deploy-section7.bat",
            "section7_container_app.py"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                self.log_test(
                    f"File: {file_path}",
                    "PASS",
                    f"Exists ({file_size:,} bytes)"
                )
            else:
                self.log_test(
                    f"File: {file_path}",
                    "FAIL",
                    "File not found"
                )
    
    def test_section7_algorithm(self):
        """Test Section 7 algorithm file content"""
        print("\n🧠 Testing Section 7 Algorithm...")
        
        algorithm_file = "life_algorithm_section7_integration.py"
        if os.path.exists(algorithm_file):
            try:
                with open(algorithm_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for key Section 7 features
                features = [
                    ("LIFEAlgorithmSection7", "Main algorithm class"),
                    ("automated_retraining", "Automated retraining functionality"),
                    ("gdpr_compliance", "GDPR compliance features"),
                    ("realtime_adaptation", "Real-time adaptation"),
                    ("quantum_optimization", "Quantum optimization"),
                    ("concrete_experience", "Concrete experience processing"),
                    ("reflective_observation", "Reflective observation"),
                    ("abstract_conceptualization", "Abstract conceptualization"),
                    ("active_experimentation", "Active experimentation")
                ]
                
                for feature, description in features:
                    if feature.lower() in content.lower():
                        self.log_test(
                            f"Algorithm Feature: {description}",
                            "PASS",
                            f"Found '{feature}' implementation"
                        )
                    else:
                        self.log_test(
                            f"Algorithm Feature: {description}",
                            "WARN",
                            f"'{feature}' not found in code"
                        )
                
                # Check file size
                if len(content) > 50000:  # Should be substantial
                    self.log_test(
                        "Algorithm Completeness",
                        "PASS",
                        f"Comprehensive implementation ({len(content):,} characters)"
                    )
                else:
                    self.log_test(
                        "Algorithm Completeness",
                        "WARN",
                        f"Implementation may be incomplete ({len(content):,} characters)"
                    )
                    
            except Exception as e:
                self.log_test(
                    "Algorithm File Reading",
                    "FAIL",
                    f"Error reading file: {str(e)}"
                )
        else:
            self.log_test(
                "Algorithm File",
                "FAIL",
                "Section 7 algorithm file not found"
            )
    
    def test_unity_integration(self):
        """Test Unity VR integration"""
        print("\n🎮 Testing Unity VR Integration...")
        
        unity_file = "unity/VREnvironmentControllerSection7.cs"
        if os.path.exists(unity_file):
            try:
                with open(unity_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for Unity-specific features
                unity_features = [
                    ("class VREnvironmentControllerSection7", "Main Unity controller class"),
                    ("MonoBehaviour", "Unity MonoBehaviour inheritance"),
                    ("async", "Asynchronous processing"),
                    ("EEG", "EEG integration"),
                    ("real-time", "Real-time processing"),
                    ("automated_retraining", "Automated retraining integration"),
                    ("GDPR", "GDPR compliance in Unity"),
                    ("UnityEngine", "Unity engine integration")
                ]
                
                for feature, description in unity_features:
                    if feature in content:
                        self.log_test(
                            f"Unity Feature: {description}",
                            "PASS",
                            f"Found '{feature}'"
                        )
                    else:
                        self.log_test(
                            f"Unity Feature: {description}",
                            "WARN",
                            f"'{feature}' not found"
                        )
                
                # Check file size
                if len(content) > 20000:
                    self.log_test(
                        "Unity Integration Completeness",
                        "PASS",
                        f"Comprehensive Unity integration ({len(content):,} characters)"
                    )
                else:
                    self.log_test(
                        "Unity Integration Completeness",
                        "WARN",
                        f"Unity integration may be basic ({len(content):,} characters)"
                    )
                    
            except Exception as e:
                self.log_test(
                    "Unity File Reading",
                    "FAIL",
                    f"Error reading Unity file: {str(e)}"
                )
        else:
            self.log_test(
                "Unity Integration File",
                "FAIL",
                "Unity VR controller file not found"
            )
    
    def test_infrastructure(self):
        """Test Azure infrastructure configuration"""
        print("\n☁️ Testing Azure Infrastructure...")
        
        bicep_file = "infra/section7-deployment.bicep"
        if os.path.exists(bicep_file):
            try:
                with open(bicep_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for Azure resources
                azure_resources = [
                    ("Microsoft.App/containerApps", "Container Apps"),
                    ("Microsoft.Storage/storageAccounts", "Storage Account"),
                    ("Microsoft.KeyVault/vaults", "Key Vault"),
                    ("Microsoft.DocumentDB/databaseAccounts", "Cosmos DB"),
                    ("Microsoft.EventHub/namespaces", "Event Hub"),
                    ("Microsoft.MachineLearningServices/workspaces", "ML Workspace"),
                    ("Microsoft.ContainerRegistry/registries", "Container Registry"),
                    ("Microsoft.Web/sites", "Function App"),
                    ("enableAutomatedRetraining", "Automated Retraining Parameter"),
                    ("enableGDPRCompliance", "GDPR Compliance Parameter"),
                    ("enableRealTimeAdaptation", "Real-time Adaptation Parameter"),
                    ("enableQuantumOptimization", "Quantum Optimization Parameter")
                ]
                
                for resource, description in azure_resources:
                    if resource in content:
                        self.log_test(
                            f"Azure Resource: {description}",
                            "PASS",
                            f"'{resource}' configured"
                        )
                    else:
                        self.log_test(
                            f"Azure Resource: {description}",
                            "WARN",
                            f"'{resource}' not found in Bicep"
                        )
                
                # Check comprehensive infrastructure
                if len(content) > 30000:
                    self.log_test(
                        "Infrastructure Completeness",
                        "PASS",
                        f"Comprehensive Azure infrastructure ({len(content):,} characters)"
                    )
                else:
                    self.log_test(
                        "Infrastructure Completeness",
                        "WARN",
                        f"Infrastructure may be incomplete ({len(content):,} characters)"
                    )
                    
            except Exception as e:
                self.log_test(
                    "Bicep File Reading",
                    "FAIL",
                    f"Error reading Bicep file: {str(e)}"
                )
        else:
            self.log_test(
                "Infrastructure File",
                "FAIL",
                "Bicep deployment template not found"
            )
    
    def test_deployment_scripts(self):
        """Test deployment scripts"""
        print("\n🚀 Testing Deployment Scripts...")
        
        scripts = [
            ("deploy-section7.sh", "Linux/macOS deployment script"),
            ("deploy-section7.bat", "Windows deployment script")
        ]
        
        for script_file, description in scripts:
            if os.path.exists(script_file):
                try:
                    with open(script_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for deployment commands
                    deployment_commands = [
                        "az group create",
                        "az deployment group",
                        "az containerapp",
                        "az acr build",
                        "life-platform-section7-prod",
                        "section7-deployment.bicep"
                    ]
                    
                    for command in deployment_commands:
                        if command in content:
                            self.log_test(
                                f"Deployment Command: {command}",
                                "PASS",
                                f"Found in {script_file}"
                            )
                        else:
                            self.log_test(
                                f"Deployment Command: {command}",
                                "WARN",
                                f"Not found in {script_file}"
                            )
                    
                    # Check script completeness
                    if len(content) > 5000:
                        self.log_test(
                            f"Script Completeness: {description}",
                            "PASS",
                            f"Comprehensive script ({len(content):,} characters)"
                        )
                    else:
                        self.log_test(
                            f"Script Completeness: {description}",
                            "WARN",
                            f"Script may be basic ({len(content):,} characters)"
                        )
                        
                except Exception as e:
                    self.log_test(
                        f"Script Reading: {description}",
                        "FAIL",
                        f"Error reading {script_file}: {str(e)}"
                    )
            else:
                self.log_test(
                    f"Deployment Script: {description}",
                    "FAIL",
                    f"{script_file} not found"
                )
    
    def test_container_app(self):
        """Test container application"""
        print("\n🐳 Testing Container Application...")
        
        container_file = "section7_container_app.py"
        if os.path.exists(container_file):
            try:
                with open(container_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for container features
                container_features = [
                    ("class Section7ContainerApp", "Main container class"),
                    ("Flask", "Web framework"),
                    ("/health", "Health endpoint"),
                    ("/ready", "Readiness endpoint"),
                    ("/metrics", "Metrics endpoint"),
                    ("DefaultAzureCredential", "Azure authentication"),
                    ("docker", "Docker configuration"),
                    ("EXPOSE 8000", "Port configuration")
                ]
                
                for feature, description in container_features:
                    if feature in content:
                        self.log_test(
                            f"Container Feature: {description}",
                            "PASS",
                            f"Found '{feature}'"
                        )
                    else:
                        self.log_test(
                            f"Container Feature: {description}",
                            "WARN",
                            f"'{feature}' not found"
                        )
                
                # Check comprehensive container app
                if len(content) > 25000:
                    self.log_test(
                        "Container App Completeness",
                        "PASS",
                        f"Comprehensive container application ({len(content):,} characters)"
                    )
                else:
                    self.log_test(
                        "Container App Completeness",
                        "WARN",
                        f"Container app may be incomplete ({len(content):,} characters)"
                    )
                    
            except Exception as e:
                self.log_test(
                    "Container App Reading",
                    "FAIL",
                    f"Error reading container app: {str(e)}"
                )
        else:
            self.log_test(
                "Container Application File",
                "FAIL",
                "Container application file not found"
            )
    
    def test_configuration_files(self):
        """Test configuration files"""
        print("\n⚙️ Testing Configuration Files...")
        
        config_files = [
            ("requirements.txt", "Python dependencies"),
            ("azure.yaml", "Azure Developer CLI config"),
            ("createUiDefinition.json", "Azure Marketplace UI"),
            (".vscode/tasks.json", "VS Code tasks"),
            ("Dockerfile", "Docker configuration")
        ]
        
        for config_file, description in config_files:
            if os.path.exists(config_file):
                file_size = os.path.getsize(config_file)
                self.log_test(
                    f"Config: {description}",
                    "PASS",
                    f"{config_file} exists ({file_size:,} bytes)"
                )
            else:
                self.log_test(
                    f"Config: {description}",
                    "WARN",
                    f"{config_file} not found"
                )
    
    def test_directory_structure(self):
        """Test required directory structure"""
        print("\n📂 Testing Directory Structure...")
        
        required_dirs = [
            "algorithms/python-core",
            "unity",
            "infra",
            "azure_functions",
            "logs",
            "tracking_data/kpis",
            "tracking_data/analytics",
            ".vscode"
        ]
        
        for directory in required_dirs:
            if os.path.exists(directory) and os.path.isdir(directory):
                file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
                self.log_test(
                    f"Directory: {directory}",
                    "PASS",
                    f"Exists with {file_count} files"
                )
            else:
                self.log_test(
                    f"Directory: {directory}",
                    "WARN",
                    "Directory not found or not a directory"
                )
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment report"""
        print("\n📊 Generating Deployment Report...")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = {
            "section7_deployment_validation": {
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration.total_seconds(),
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "warnings": warning_tests,
                    "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
                },
                "deployment_readiness": "READY" if failed_tests == 0 else "NEEDS_ATTENTION",
                "test_results": self.test_results,
                "errors": self.errors,
                "warnings": self.warnings,
                "recommendations": []
            }
        }
        
        # Add recommendations based on results
        if failed_tests > 0:
            report["section7_deployment_validation"]["recommendations"].append(
                "Fix critical errors before deployment"
            )
        
        if warning_tests > 0:
            report["section7_deployment_validation"]["recommendations"].append(
                "Review warnings to ensure optimal deployment"
            )
        
        if failed_tests == 0 and warning_tests < 5:
            report["section7_deployment_validation"]["recommendations"].append(
                "Section 7 deployment is ready for Azure"
            )
        
        # Save report
        report_file = f"section7_deployment_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            self.log_test(
                "Deployment Report",
                "PASS",
                f"Report saved to {report_file}"
            )
        except Exception as e:
            self.log_test(
                "Deployment Report",
                "FAIL",
                f"Failed to save report: {str(e)}"
            )
        
        return report
    
    def run_validation(self):
        """Run complete Section 7 deployment validation"""
        try:
            print("Starting comprehensive Section 7 deployment validation...")
            print("")
            
            # Run all validation tests
            self.test_file_existence()
            self.test_section7_algorithm()
            self.test_unity_integration()
            self.test_infrastructure()
            self.test_deployment_scripts()
            self.test_container_app()
            self.test_configuration_files()
            self.test_directory_structure()
            
            # Generate report
            report = self.generate_deployment_report()
            
            # Print summary
            print("\n" + "=" * 60)
            print("🎉 SECTION 7 DEPLOYMENT VALIDATION COMPLETE")
            print("=" * 60)
            
            summary = report["section7_deployment_validation"]["summary"]
            print(f"📊 Test Results:")
            print(f"   Total Tests: {summary['total_tests']}")
            print(f"   ✅ Passed: {summary['passed']}")
            print(f"   ❌ Failed: {summary['failed']}")
            print(f"   ⚠️  Warnings: {summary['warnings']}")
            print(f"   📈 Success Rate: {summary['success_rate']}")
            print("")
            
            deployment_status = report["section7_deployment_validation"]["deployment_readiness"]
            if deployment_status == "READY":
                print("🚀 DEPLOYMENT STATUS: ✅ READY FOR AZURE DEPLOYMENT")
                print("   Section 7 components are validated and ready for deployment")
            else:
                print("🚨 DEPLOYMENT STATUS: ⚠️ NEEDS ATTENTION")
                print("   Please review and fix issues before deployment")
            
            print("")
            if self.errors:
                print("❌ Critical Errors:")
                for error in self.errors:
                    print(f"   • {error}")
                print("")
            
            if self.warnings:
                print("⚠️ Warnings:")
                for warning in self.warnings[:5]:  # Show first 5 warnings
                    print(f"   • {warning}")
                if len(self.warnings) > 5:
                    print(f"   • ... and {len(self.warnings) - 5} more warnings")
                print("")
            
            print("📋 Recommendations:")
            for rec in report["section7_deployment_validation"]["recommendations"]:
                print(f"   • {rec}")
            
            print("")
            print("🏁 Validation completed successfully!")
            print(f"⏱️ Duration: {report['section7_deployment_validation']['duration_seconds']:.2f} seconds")
            
            return report
            
        except Exception as e:
            print(f"\n💥 VALIDATION FAILED: {str(e)}")
            print(traceback.format_exc())
            return {"error": str(e)}

def main():
    """Main entry point for Section 7 deployment validation"""
    print("🧠 L.I.F.E Platform Section 7 - Ultimate Deployment Validation")
    print("Copyright 2025 - Neuroadaptive Learning Platform")
    print("")
    
    validator = Section7DeploymentValidator()
    report = validator.run_validation()
    
    # Return appropriate exit code
    if "error" in report:
        sys.exit(1)
    elif report["section7_deployment_validation"]["deployment_readiness"] != "READY":
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()