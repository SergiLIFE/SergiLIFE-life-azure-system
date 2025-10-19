"""
Azure Staging Deployment Script for L.I.F.E Platform
Deploys production-ready infrastructure using Azure CLI

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
Production-Ready: September 27, 2025
Target: $345K Q4 2025 → $50.7M by 2029
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AzureDeploymentManager:
    """Manages Azure deployment for L.I.F.E Platform using Azure CLI"""

    def __init__(self):
        self.subscription_id = "5c88cef6-f243-497d-98af-6c6086d575ca"
        self.resource_group = "life-platform-rg"
        self.location = "eastus2"
        self.deployment_name = (
            f"life-deployment-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        )

        # Resource names
        self.storage_account = "stlifeplatformprod"
        self.key_vault = "kv-life-platform-prod"
        self.service_bus = "sb-life-platform-prod"
        self.function_app = "life-functions-app"
        self.app_service_plan = "life-app-service-plan"

        self.deployment_log = []

    def run_az_command(
        self, command: List[str], capture_output: bool = True
    ) -> Dict[str, Any]:
        """Execute Azure CLI command with error handling"""
        try:
            logger.info(f"Running: {' '.join(command)}")

            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=False,
                shell=True,  # Required for Windows to find az.cmd
            )

            if result.returncode != 0:
                logger.error(f"Command failed with code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "returncode": result.returncode,
                }

            # Try to parse JSON output
            if capture_output and result.stdout:
                try:
                    return {
                        "success": True,
                        "data": json.loads(result.stdout),
                        "raw": result.stdout,
                    }
                except json.JSONDecodeError:
                    return {
                        "success": True,
                        "data": result.stdout.strip(),
                        "raw": result.stdout,
                    }

            return {"success": True, "data": None}

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {"success": False, "error": str(e)}

    def verify_azure_login(self) -> bool:
        """Verify Azure CLI is authenticated"""
        logger.info("🔐 Verifying Azure CLI authentication...")

        result = self.run_az_command(["az", "account", "show"])

        if result["success"]:
            logger.info("✅ Azure CLI authenticated successfully")
            if "data" in result and isinstance(result["data"], dict):
                logger.info(f"   Subscription: {result['data'].get('name', 'Unknown')}")
                logger.info(f"   ID: {result['data'].get('id', 'Unknown')}")
            return True
        else:
            logger.error("❌ Azure CLI not authenticated. Please run 'az login' first.")
            return False

    def set_subscription(self) -> bool:
        """Set the active Azure subscription"""
        logger.info(f"🎯 Setting subscription to: {self.subscription_id}")

        result = self.run_az_command(
            ["az", "account", "set", "--subscription", self.subscription_id]
        )

        if result["success"]:
            logger.info("✅ Subscription set successfully")
            return True
        else:
            logger.error(
                f"❌ Failed to set subscription: {result.get('error', 'Unknown error')}"
            )
            return False

    def check_resource_group(self) -> bool:
        """Check if resource group exists"""
        logger.info(f"🔍 Checking resource group: {self.resource_group}")

        result = self.run_az_command(
            ["az", "group", "exists", "--name", self.resource_group]
        )

        if result["success"]:
            exists = result["data"] == "true"
            if exists:
                logger.info(f"✅ Resource group '{self.resource_group}' exists")
            else:
                logger.info(f"ℹ️  Resource group '{self.resource_group}' does not exist")
            return exists

        return False

    def create_resource_group(self) -> bool:
        """Create Azure resource group"""
        logger.info(f"🏗️  Creating resource group: {self.resource_group}")

        result = self.run_az_command(
            [
                "az",
                "group",
                "create",
                "--name",
                self.resource_group,
                "--location",
                self.location,
                "--tags",
                f"Project=L.I.F.E-Platform",
                f"Environment=Staging",
                f"OfferID=9a600d96-fe1e-420b-902a-a0c42c561adb",
                f"CreatedBy=Sergio-Paya-Borrull",
            ]
        )

        if result["success"]:
            logger.info("✅ Resource group created successfully")
            return True
        else:
            logger.error(
                f"❌ Failed to create resource group: {result.get('error', 'Unknown error')}"
            )
            return False

    def create_storage_account(self) -> bool:
        """Create Azure Storage account"""
        logger.info(f"💾 Creating storage account: {self.storage_account}")

        result = self.run_az_command(
            [
                "az",
                "storage",
                "account",
                "create",
                "--name",
                self.storage_account,
                "--resource-group",
                self.resource_group,
                "--location",
                self.location,
                "--sku",
                "Standard_LRS",
                "--kind",
                "StorageV2",
                "--access-tier",
                "Hot",
                "--allow-blob-public-access",
                "false",
                "--min-tls-version",
                "TLS1_2",
            ]
        )

        if result["success"]:
            logger.info("✅ Storage account created successfully")
            return True
        else:
            error_msg = result.get("error", "")
            if "already exists" in error_msg.lower():
                logger.info("ℹ️  Storage account already exists")
                return True
            logger.error(f"❌ Failed to create storage account: {error_msg}")
            return False

    def create_key_vault(self) -> bool:
        """Create Azure Key Vault"""
        logger.info(f"🔐 Creating Key Vault: {self.key_vault}")

        result = self.run_az_command(
            [
                "az",
                "keyvault",
                "create",
                "--name",
                self.key_vault,
                "--resource-group",
                self.resource_group,
                "--location",
                self.location,
                "--sku",
                "standard",
                "--enable-rbac-authorization",
                "true",
            ]
        )

        if result["success"]:
            logger.info("✅ Key Vault created successfully")
            return True
        else:
            error_msg = result.get("error", "")
            if "already exists" in error_msg.lower():
                logger.info("ℹ️  Key Vault already exists")
                return True
            logger.error(f"❌ Failed to create Key Vault: {error_msg}")
            return False

    def create_service_bus(self) -> bool:
        """Create Azure Service Bus namespace"""
        logger.info(f"🚌 Creating Service Bus: {self.service_bus}")

        result = self.run_az_command(
            [
                "az",
                "servicebus",
                "namespace",
                "create",
                "--name",
                self.service_bus,
                "--resource-group",
                self.resource_group,
                "--location",
                self.location,
                "--sku",
                "Standard",
            ]
        )

        if result["success"]:
            logger.info("✅ Service Bus created successfully")
            return True
        else:
            error_msg = result.get("error", "")
            if "already exists" in error_msg.lower():
                logger.info("ℹ️  Service Bus already exists")
                return True
            logger.error(f"❌ Failed to create Service Bus: {error_msg}")
            return False

    def create_app_service_plan(self) -> bool:
        """Create Azure App Service Plan for Functions"""
        logger.info(f"📦 Creating App Service Plan: {self.app_service_plan}")

        result = self.run_az_command(
            [
                "az",
                "appservice",
                "plan",
                "create",
                "--name",
                self.app_service_plan,
                "--resource-group",
                self.resource_group,
                "--location",
                self.location,
                "--sku",
                "B1",
                "--is-linux",
            ]
        )

        if result["success"]:
            logger.info("✅ App Service Plan created successfully")
            return True
        else:
            error_msg = result.get("error", "")
            if "already exists" in error_msg.lower():
                logger.info("ℹ️  App Service Plan already exists")
                return True
            logger.error(f"❌ Failed to create App Service Plan: {error_msg}")
            return False

    def create_function_app(self) -> bool:
        """Create Azure Function App"""
        logger.info(f"⚡ Creating Function App: {self.function_app}")

        # Get storage connection string first
        conn_result = self.run_az_command(
            [
                "az",
                "storage",
                "account",
                "show-connection-string",
                "--name",
                self.storage_account,
                "--resource-group",
                self.resource_group,
                "--query",
                "connectionString",
                "--output",
                "tsv",
            ]
        )

        if not conn_result["success"]:
            logger.error("❌ Failed to get storage connection string")
            return False

        result = self.run_az_command(
            [
                "az",
                "functionapp",
                "create",
                "--name",
                self.function_app,
                "--resource-group",
                self.resource_group,
                "--plan",
                self.app_service_plan,
                "--storage-account",
                self.storage_account,
                "--runtime",
                "python",
                "--runtime-version",
                "3.11",
                "--functions-version",
                "4",
                "--os-type",
                "Linux",
            ]
        )

        if result["success"]:
            logger.info("✅ Function App created successfully")
            return True
        else:
            error_msg = result.get("error", "")
            if "already exists" in error_msg.lower():
                logger.info("ℹ️  Function App already exists")
                return True
            logger.error(f"❌ Failed to create Function App: {error_msg}")
            return False

    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get summary of deployed resources"""
        logger.info("📊 Gathering deployment summary...")

        # List all resources in the resource group
        result = self.run_az_command(
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

        resources = []
        if result["success"] and isinstance(result["data"], list):
            resources = result["data"]

        summary = {
            "deployment_name": self.deployment_name,
            "subscription_id": self.subscription_id,
            "resource_group": self.resource_group,
            "location": self.location,
            "timestamp": datetime.now().isoformat(),
            "total_resources": len(resources),
            "resources": [],
        }

        for resource in resources:
            summary["resources"].append(
                {
                    "name": resource.get("name"),
                    "type": resource.get("type"),
                    "location": resource.get("location"),
                }
            )

        return summary

    async def deploy(self) -> bool:
        """Execute full deployment"""
        logger.info("=" * 80)
        logger.info("🧠 L.I.F.E PLATFORM AZURE STAGING DEPLOYMENT")
        logger.info("=" * 80)
        logger.info(f"Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb")
        logger.info(f"Production-Ready: September 27, 2025")
        logger.info(f"Target: $345K Q4 2025 → $50.7M by 2029")
        logger.info("=" * 80)
        logger.info("")

        # Step 1: Verify authentication
        if not self.verify_azure_login():
            logger.error("❌ Deployment failed: Not authenticated")
            return False

        # Step 2: Set subscription
        if not self.set_subscription():
            logger.error("❌ Deployment failed: Could not set subscription")
            return False

        # Step 3: Check/Create resource group
        if not self.check_resource_group():
            if not self.create_resource_group():
                logger.error("❌ Deployment failed: Could not create resource group")
                return False

        # Step 4: Create storage account
        if not self.create_storage_account():
            logger.error("❌ Deployment failed: Could not create storage account")
            return False

        # Step 5: Create Key Vault
        if not self.create_key_vault():
            logger.error("❌ Deployment failed: Could not create Key Vault")
            return False

        # Step 6: Create Service Bus
        if not self.create_service_bus():
            logger.error("❌ Deployment failed: Could not create Service Bus")
            return False

        # Step 7: Create App Service Plan
        if not self.create_app_service_plan():
            logger.error("❌ Deployment failed: Could not create App Service Plan")
            return False

        # Step 8: Create Function App
        if not self.create_function_app():
            logger.error("❌ Deployment failed: Could not create Function App")
            return False

        # Step 9: Get deployment summary
        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)

        summary = self.get_deployment_summary()

        # Save summary to file
        summary_file = "AZURE_DEPLOYMENT_SUMMARY.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"📄 Deployment summary saved to: {summary_file}")
        logger.info("")
        logger.info("🎯 DEPLOYED RESOURCES:")
        logger.info(f"   • Resource Group: {self.resource_group}")
        logger.info(f"   • Storage Account: {self.storage_account}")
        logger.info(f"   • Key Vault: {self.key_vault}")
        logger.info(f"   • Service Bus: {self.service_bus}")
        logger.info(f"   • Function App: {self.function_app}")
        logger.info("")
        logger.info("🚀 NEXT STEPS:")
        logger.info("   1. Configure Function App settings")
        logger.info("   2. Deploy Function App code")
        logger.info("   3. Configure monitoring and alerts")
        logger.info("   4. Test endpoints and functionality")
        logger.info("")

        return True


async def main():
    """Main deployment entry point"""
    try:
        deployer = AzureDeploymentManager()
        success = await deployer.deploy()

        if success:
            logger.info("🎉 L.I.F.E Platform deployed successfully to Azure!")
            return 0
        else:
            logger.error("❌ Deployment failed. Please check logs above.")
            return 1

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Deployment interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Deployment failed with error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
