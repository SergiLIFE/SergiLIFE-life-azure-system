#!/usr/bin/env python3
"""
Azure Integration Testing for L.I.F.E Platform
Comprehensive validation of Azure resources and connectivity
"""

import asyncio
import json
import logging
import subprocess
from datetime import datetime
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureIntegrationValidator:
    """Azure Integration Validation Suite"""

    def __init__(self):
        # L.I.F.E Platform Azure Configuration (from azure_config.py)
        self.resource_group = "life-platform-rg"
        self.storage_account = "stlifeplatformprod"
        self.cosmos_db = "life-cosmos-db"
        self.function_app = "life-functions-app"
        self.keyvault = "kv-life-platform-prod"
        self.servicebus = "sb-life-platform-prod"

        self.results = []

    def run_azure_cli_command(self, command: str) -> Dict[str, Any]:
        """Execute Azure CLI command and return result"""
        try:
            logger.info(f"Running: {command}")

            # Run the command
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out",
                "stdout": "",
                "stderr": "Timeout after 30 seconds",
            }
        except Exception as e:
            return {"success": False, "error": str(e), "stdout": "", "stderr": str(e)}

    async def test_azure_login_status(self) -> Dict[str, Any]:
        """Test Azure CLI login status"""
        logger.info("🔐 Testing Azure CLI login status...")

        result = self.run_azure_cli_command("az account show --output json")

        if result["success"]:
            try:
                account_info = json.loads(result["stdout"])
                return {
                    "test": "Azure CLI Login Status",
                    "passed": True,
                    "subscription_id": account_info.get("id", "Unknown"),
                    "tenant_id": account_info.get("tenantId", "Unknown"),
                    "account_name": account_info.get("name", "Unknown"),
                }
            except json.JSONDecodeError:
                return {
                    "test": "Azure CLI Login Status",
                    "passed": False,
                    "error": "Could not parse account information",
                }
        else:
            return {
                "test": "Azure CLI Login Status",
                "passed": False,
                "error": result.get("stderr", "Unknown error"),
                "suggestion": "Run 'az login' to authenticate",
            }

    async def test_resource_group(self) -> Dict[str, Any]:
        """Test resource group accessibility"""
        logger.info(f"📦 Testing resource group: {self.resource_group}")

        result = self.run_azure_cli_command(
            f"az group show --name {self.resource_group} --output json"
        )

        if result["success"]:
            try:
                rg_info = json.loads(result["stdout"])
                return {
                    "test": "Resource Group Access",
                    "passed": True,
                    "resource_group": self.resource_group,
                    "location": rg_info.get("location", "Unknown"),
                    "provisioning_state": rg_info.get("properties", {}).get(
                        "provisioningState", "Unknown"
                    ),
                }
            except json.JSONDecodeError:
                return {
                    "test": "Resource Group Access",
                    "passed": False,
                    "error": "Could not parse resource group information",
                }
        else:
            return {
                "test": "Resource Group Access",
                "passed": False,
                "error": result.get("stderr", "Resource group not accessible"),
                "resource_group": self.resource_group,
            }

    async def test_storage_account(self) -> Dict[str, Any]:
        """Test storage account accessibility"""
        logger.info(f"💾 Testing storage account: {self.storage_account}")

        result = self.run_azure_cli_command(
            f"az storage account show --name {self.storage_account} --resource-group {self.resource_group} --output json"
        )

        if result["success"]:
            try:
                storage_info = json.loads(result["stdout"])
                return {
                    "test": "Storage Account Access",
                    "passed": True,
                    "storage_account": self.storage_account,
                    "location": storage_info.get("location", "Unknown"),
                    "sku": storage_info.get("sku", {}).get("name", "Unknown"),
                    "provisioning_state": storage_info.get(
                        "provisioningState", "Unknown"
                    ),
                }
            except json.JSONDecodeError:
                return {
                    "test": "Storage Account Access",
                    "passed": False,
                    "error": "Could not parse storage account information",
                }
        else:
            return {
                "test": "Storage Account Access",
                "passed": False,
                "error": result.get("stderr", "Storage account not accessible"),
                "storage_account": self.storage_account,
            }

    async def test_function_app(self) -> Dict[str, Any]:
        """Test Azure Functions accessibility"""
        logger.info(f"⚡ Testing Function App: {self.function_app}")

        result = self.run_azure_cli_command(
            f"az functionapp show --name {self.function_app} --resource-group {self.resource_group} --output json"
        )

        if result["success"]:
            try:
                func_info = json.loads(result["stdout"])
                return {
                    "test": "Function App Access",
                    "passed": True,
                    "function_app": self.function_app,
                    "location": func_info.get("location", "Unknown"),
                    "state": func_info.get("state", "Unknown"),
                    "default_hostname": func_info.get("defaultHostName", "Unknown"),
                }
            except json.JSONDecodeError:
                return {
                    "test": "Function App Access",
                    "passed": False,
                    "error": "Could not parse function app information",
                }
        else:
            return {
                "test": "Function App Access",
                "passed": False,
                "error": result.get("stderr", "Function app not accessible"),
                "function_app": self.function_app,
            }

    async def test_cosmos_db(self) -> Dict[str, Any]:
        """Test Cosmos DB accessibility"""
        logger.info(f"🌌 Testing Cosmos DB: {self.cosmos_db}")

        result = self.run_azure_cli_command(
            f"az cosmosdb show --name {self.cosmos_db} --resource-group {self.resource_group} --output json"
        )

        if result["success"]:
            try:
                cosmos_info = json.loads(result["stdout"])
                return {
                    "test": "Cosmos DB Access",
                    "passed": True,
                    "cosmos_db": self.cosmos_db,
                    "location": cosmos_info.get("location", "Unknown"),
                    "provisioning_state": cosmos_info.get(
                        "provisioningState", "Unknown"
                    ),
                    "document_endpoint": cosmos_info.get("documentEndpoint", "Unknown"),
                }
            except json.JSONDecodeError:
                return {
                    "test": "Cosmos DB Access",
                    "passed": False,
                    "error": "Could not parse Cosmos DB information",
                }
        else:
            return {
                "test": "Cosmos DB Access",
                "passed": False,
                "error": result.get("stderr", "Cosmos DB not accessible"),
                "cosmos_db": self.cosmos_db,
            }

    async def test_resource_list(self) -> Dict[str, Any]:
        """List all resources in the resource group"""
        logger.info(f"📋 Listing all resources in {self.resource_group}")

        result = self.run_azure_cli_command(
            f"az resource list --resource-group {self.resource_group} --output json"
        )

        if result["success"]:
            try:
                resources = json.loads(result["stdout"])
                resource_types = {}
                for resource in resources:
                    resource_type = resource.get("type", "Unknown")
                    if resource_type in resource_types:
                        resource_types[resource_type] += 1
                    else:
                        resource_types[resource_type] = 1

                return {
                    "test": "Resource Group Inventory",
                    "passed": True,
                    "total_resources": len(resources),
                    "resource_types": resource_types,
                    "resources": [
                        {"name": r.get("name"), "type": r.get("type")}
                        for r in resources[:10]
                    ],  # First 10
                }
            except json.JSONDecodeError:
                return {
                    "test": "Resource Group Inventory",
                    "passed": False,
                    "error": "Could not parse resource list",
                }
        else:
            return {
                "test": "Resource Group Inventory",
                "passed": False,
                "error": result.get("stderr", "Could not list resources"),
            }

    async def run_complete_azure_validation(self) -> Dict[str, Any]:
        """Run complete Azure integration validation"""
        logger.info("🚀 Starting Complete Azure Integration Validation")
        start_time = datetime.now()

        # Run all tests
        test_methods = [
            self.test_azure_login_status,
            self.test_resource_group,
            self.test_resource_list,
            self.test_storage_account,
            self.test_function_app,
            self.test_cosmos_db,
        ]

        for test_method in test_methods:
            try:
                result = await test_method()
                self.results.append(result)

                status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
                logger.info(f"{status}: {result.get('test', test_method.__name__)}")

            except Exception as e:
                error_result = {
                    "test": test_method.__name__,
                    "passed": False,
                    "error": f"Test execution error: {str(e)}",
                }
                self.results.append(error_result)
                logger.error(f"❌ FAIL: {test_method.__name__} - {str(e)}")

        # Calculate results
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.get("passed", False))
        pass_rate = passed_tests / total_tests if total_tests > 0 else 0

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        # Generate report
        report = {
            "validation_timestamp": start_time.isoformat(),
            "azure_integration_results": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "pass_rate": round(pass_rate, 4),
                "execution_time_seconds": round(execution_time, 2),
            },
            "test_results": self.results,
            "production_ready": pass_rate >= 0.5,  # 50% minimum for Azure validation
            "recommendations": self._generate_recommendations(),
        }

        logger.info(
            f"🎯 Azure Validation Complete: {passed_tests}/{total_tests} tests passed ({pass_rate:.1%})"
        )

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        failed_tests = [r for r in self.results if not r.get("passed", False)]

        if any("login" in r.get("test", "").lower() for r in failed_tests):
            recommendations.append("Run 'az login' to authenticate with Azure CLI")

        if any("resource group" in r.get("test", "").lower() for r in failed_tests):
            recommendations.append("Verify resource group name and access permissions")

        if any("storage" in r.get("test", "").lower() for r in failed_tests):
            recommendations.append(
                "Check storage account configuration and permissions"
            )

        if any("function" in r.get("test", "").lower() for r in failed_tests):
            recommendations.append(
                "Verify Azure Functions deployment and configuration"
            )

        if any("cosmos" in r.get("test", "").lower() for r in failed_tests):
            recommendations.append("Check Cosmos DB deployment and access permissions")

        if not recommendations:
            recommendations.append("All Azure integration tests passed successfully!")

        return recommendations


# Main execution
async def main():
    """Main execution for Azure integration testing"""
    validator = AzureIntegrationValidator()

    print("🔧 L.I.F.E Platform - Azure Integration Testing")
    print("=" * 60)

    result = await validator.run_complete_azure_validation()

    print("\n" + "=" * 60)
    print("AZURE INTEGRATION TESTING COMPLETED!")
    print("=" * 60)

    # Display results
    azure_results = result["azure_integration_results"]
    print(f"Total Tests: {azure_results['total_tests']}")
    print(f"Passed: {azure_results['passed_tests']}")
    print(f"Failed: {azure_results['failed_tests']}")
    print(f"Pass Rate: {azure_results['pass_rate']:.1%}")
    print(f"Production Ready: {result['production_ready']}")

    print("\nTest Details:")
    for test_result in result["test_results"]:
        status = "✅ PASS" if test_result.get("passed", False) else "❌ FAIL"
        print(f"  {status}: {test_result.get('test', 'Unknown')}")
        if not test_result.get("passed", False) and test_result.get("error"):
            print(f"    Error: {test_result['error']}")

    print("\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")

    # Save report
    report_file = "azure_integration_report.json"
    with open(report_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n📄 Report saved: {report_file}")

    return 0 if result["production_ready"] else 1


if __name__ == "__main__":
    import sys

    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Critical Azure integration testing error: {e}")
        sys.exit(1)
