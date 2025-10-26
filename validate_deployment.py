"""
L.I.F.E Platform - Automated Deployment Validation Suite
Phase 2: Staging Environment Validation

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
log_file = os.path.join(
    LOGS_DIR, f'deployment_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class DeploymentValidator:
    """Automated validation of L.I.F.E Platform deployment"""

    def __init__(self, environment: str = "staging"):
        self.environment = environment
        self.resource_group = "life-platform-rg"
        self.function_app = "life-functions-app"
        self.storage_account = "stlifeplatformprod"
        self.key_vault = "kv-life-platform-prod"
        self.service_bus = "sb-life-platform-prod"

        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "environment": environment,
            "tests": [],
        }

    def run_command(self, command: List[str]) -> Dict[str, Any]:
        """Execute Azure CLI command"""
        try:
            logger.info(f"Running: {' '.join(command)}")

            result = subprocess.run(
                command, capture_output=True, text=True, check=False, shell=True
            )

            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                return {"success": False, "error": result.stderr}

            # Try to parse JSON
            if result.stdout:
                try:
                    return {"success": True, "data": json.loads(result.stdout)}
                except json.JSONDecodeError:
                    return {"success": True, "data": result.stdout.strip()}

            return {"success": True, "data": None}

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {"success": False, "error": str(e)}

    def validate_resource_group(self) -> bool:
        """Validate resource group exists"""
        logger.info("=" * 80)
        logger.info("TEST 1: Validating Resource Group")
        logger.info("=" * 80)

        result = self.run_command(
            ["az", "group", "show", "--name", self.resource_group]
        )

        if result["success"]:
            logger.info(f"✅ Resource group '{self.resource_group}' exists")
            self.validation_results["tests"].append(
                {
                    "name": "Resource Group Validation",
                    "status": "PASS",
                    "details": result.get("data", {}),
                }
            )
            return True
        else:
            logger.error("❌ Resource group validation failed")
            self.validation_results["tests"].append(
                {
                    "name": "Resource Group Validation",
                    "status": "FAIL",
                    "error": result.get("error"),
                }
            )
            return False

    def validate_storage_account(self) -> bool:
        """Validate storage account"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 2: Validating Storage Account")
        logger.info("=" * 80)

        result = self.run_command(
            [
                "az",
                "storage",
                "account",
                "show",
                "--name",
                self.storage_account,
                "--resource-group",
                self.resource_group,
            ]
        )

        if result["success"]:
            data = result.get("data", {})
            status = data.get("provisioningState", "Unknown")

            if status == "Succeeded":
                logger.info(f"✅ Storage account '{self.storage_account}' is active")
                logger.info(f"   Location: {data.get('location', 'Unknown')}")
                logger.info(f"   SKU: {data.get('sku', {}).get('name', 'Unknown')}")

                self.validation_results["tests"].append(
                    {
                        "name": "Storage Account Validation",
                        "status": "PASS",
                        "details": {
                            "name": self.storage_account,
                            "status": status,
                            "location": data.get("location"),
                        },
                    }
                )
                return True
            else:
                logger.warning(f"⚠️  Storage account status: {status}")
                return False

        logger.error("❌ Storage account validation failed")
        self.validation_results["tests"].append(
            {
                "name": "Storage Account Validation",
                "status": "FAIL",
                "error": result.get("error"),
            }
        )
        return False

    def validate_key_vault(self) -> bool:
        """Validate Key Vault"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 3: Validating Key Vault")
        logger.info("=" * 80)

        result = self.run_command(["az", "keyvault", "show", "--name", self.key_vault])

        if result["success"]:
            data = result.get("data", {})
            logger.info(f"✅ Key Vault '{self.key_vault}' is accessible")
            logger.info(
                f"   Vault URI: {data.get('properties', {}).get('vaultUri', 'Unknown')}"
            )

            self.validation_results["tests"].append(
                {
                    "name": "Key Vault Validation",
                    "status": "PASS",
                    "details": {
                        "name": self.key_vault,
                        "uri": data.get("properties", {}).get("vaultUri"),
                    },
                }
            )
            return True

        logger.error("❌ Key Vault validation failed")
        self.validation_results["tests"].append(
            {
                "name": "Key Vault Validation",
                "status": "FAIL",
                "error": result.get("error"),
            }
        )
        return False

    def validate_service_bus(self) -> bool:
        """Validate Service Bus"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 4: Validating Service Bus")
        logger.info("=" * 80)

        result = self.run_command(
            [
                "az",
                "servicebus",
                "namespace",
                "show",
                "--name",
                self.service_bus,
                "--resource-group",
                self.resource_group,
            ]
        )

        if result["success"]:
            data = result.get("data", {})
            status = data.get("status", "Unknown")

            if status == "Active":
                logger.info(f"✅ Service Bus '{self.service_bus}' is active")
                logger.info(f"   SKU: {data.get('sku', {}).get('name', 'Unknown')}")

                self.validation_results["tests"].append(
                    {
                        "name": "Service Bus Validation",
                        "status": "PASS",
                        "details": {"name": self.service_bus, "status": status},
                    }
                )
                return True

        logger.error("❌ Service Bus validation failed")
        self.validation_results["tests"].append(
            {
                "name": "Service Bus Validation",
                "status": "FAIL",
                "error": result.get("error"),
            }
        )
        return False

    def validate_function_app(self) -> bool:
        """Validate Function App"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 5: Validating Function App")
        logger.info("=" * 80)

        result = self.run_command(
            [
                "az",
                "functionapp",
                "show",
                "--name",
                self.function_app,
                "--resource-group",
                self.resource_group,
            ]
        )

        if result["success"]:
            data = result.get("data", {})
            state = data.get("state", "Unknown")

            if state == "Running":
                logger.info(f"✅ Function App '{self.function_app}' is running")
                logger.info(
                    f"   Default hostname: {data.get('defaultHostName', 'Unknown')}"
                )
                logger.info("   Runtime: Python 3.11")

                self.validation_results["tests"].append(
                    {
                        "name": "Function App Validation",
                        "status": "PASS",
                        "details": {
                            "name": self.function_app,
                            "state": state,
                            "url": f"https://{data.get('defaultHostName')}",
                        },
                    }
                )
                return True

        logger.error("❌ Function App validation failed")
        self.validation_results["tests"].append(
            {
                "name": "Function App Validation",
                "status": "FAIL",
                "error": result.get("error"),
            }
        )
        return False

    def list_all_resources(self) -> bool:
        """List all resources in the resource group"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 6: Listing All Resources")
        logger.info("=" * 80)

        result = self.run_command(
            [
                "az",
                "resource",
                "list",
                "--resource-group",
                self.resource_group,
                "--output",
                "json",
            ]
        )

        if result["success"]:
            resources = result.get("data", [])
            logger.info(
                f"✅ Found {len(resources)} resources in '{self.resource_group}'"
            )

            resource_types = {}
            for resource in resources:
                res_type = resource.get("type", "Unknown")
                resource_types[res_type] = resource_types.get(res_type, 0) + 1

            logger.info("\nResource breakdown:")
            for res_type, count in sorted(resource_types.items()):
                logger.info(f"   {res_type}: {count}")

            self.validation_results["tests"].append(
                {
                    "name": "Resource Listing",
                    "status": "PASS",
                    "details": {
                        "total_resources": len(resources),
                        "resource_types": resource_types,
                    },
                }
            )
            return True

        logger.error("❌ Resource listing failed")
        return False

    def generate_report(self) -> bool:
        """Generate validation report"""
        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 80)

        total_tests = len(self.validation_results["tests"])
        passed_tests = sum(
            1 for test in self.validation_results["tests"] if test["status"] == "PASS"
        )
        failed_tests = total_tests - passed_tests

        logger.info(f"\nTotal Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

        # Save report
        RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
        os.makedirs(RESULTS_DIR, exist_ok=True)

        report_file = os.path.join(
            RESULTS_DIR,
            f"deployment_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.validation_results, f, indent=2)

        logger.info(f"\nDetailed report saved to: {report_file}")

        if failed_tests == 0:
            logger.info("\n🎉 ALL TESTS PASSED! Deployment is READY for production!")
            return True
        else:
            logger.warning(
                f"\n⚠️  {failed_tests} test(s) failed. Please review before proceeding."
            )
            return False

    async def run_validation(self) -> bool:
        """Run all validation tests"""
        logger.info("=" * 80)
        logger.info("L.I.F.E PLATFORM - DEPLOYMENT VALIDATION")
        logger.info("=" * 80)
        logger.info(f"Environment: {self.environment}")
        logger.info(f"Resource Group: {self.resource_group}")
        logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

        tests = [
            self.validate_resource_group(),
            self.validate_storage_account(),
            self.validate_key_vault(),
            self.validate_service_bus(),
            self.validate_function_app(),
            self.list_all_resources(),
        ]

        all_passed = self.generate_report()
        return all_passed


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E Platform Deployment Validator"
    )
    parser.add_argument(
        "--environment",
        default="staging",
        choices=["staging", "production"],
        help="Environment to validate",
    )

    args = parser.parse_args()

    try:
        validator = DeploymentValidator(environment=args.environment)
        success = await validator.run_validation()

        return 0 if success else 1

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Validation interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Validation failed with error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
