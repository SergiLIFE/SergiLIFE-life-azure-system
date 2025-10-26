"""
L.I.F.E Platform - Complete Deployment Workflow
Combines: Configuration + Validation + Code Deployment

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
from typing import Any, Dict, List, Tuple

# Get script directory - handle Windows paths with spaces
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")

# Create directories if they don't exist - with error handling
try:
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create directories: {e}")
    print(f"SCRIPT_DIR: {SCRIPT_DIR}")
    print(f"LOGS_DIR: {LOGS_DIR}")
    print(f"RESULTS_DIR: {RESULTS_DIR}")
    # Try using current directory as fallback
    LOGS_DIR = "logs"
    RESULTS_DIR = "results"
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(RESULTS_DIR, exist_ok=True)
        print(f"Using current directory fallback: {os.getcwd()}")
    except Exception as e2:
        print(f"Critical error: Cannot create directories: {e2}")
        sys.exit(1)

# Configure logging
log_file = os.path.join(
    LOGS_DIR, f'complete_deployment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class CompleteDeploymentWorkflow:
    """Orchestrates complete deployment: configure, validate, deploy code."""

    def __init__(self):
        self.resource_group = "life-platform-rg"
        self.function_app = "life-functions-app"
        self.storage_account = "stlifeplatformprod"
        self.key_vault = "kv-life-platform-prod"
        self.service_bus = "sb-life-platform-prod"
        self.region = "eastus2"

        self.results = {
            "timestamp": datetime.now().isoformat(),
            "workflow_status": "in_progress",
            "steps": {},
        }

    def run_command(self, cmd: str, description: str) -> Tuple[bool, str]:
        """Run Azure CLI command and return success status and output."""
        logger.info(f"Running: {description}")
        logger.debug(f"Command: {cmd}")

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=120
            )

            success = result.returncode == 0
            output = result.stdout.strip() if success else result.stderr.strip()

            if success:
                logger.info(f"✅ {description}: SUCCESS")
            else:
                logger.error(f"❌ {description}: FAILED")
                logger.error(f"Error: {output}")

            return success, output

        except subprocess.TimeoutExpired:
            logger.error(f"❌ {description}: TIMEOUT")
            return False, "Command timed out after 120 seconds"
        except Exception as e:
            logger.error(f"❌ {description}: EXCEPTION - {str(e)}")
            return False, str(e)

    async def step_1_configure_function_app(self) -> bool:
        """Configure Function App with required settings."""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: CONFIGURE FUNCTION APP")
        logger.info("=" * 60)

        step_results = {"status": "running", "tests": []}

        # Test 1: Enable Python worker extensions
        success, output = self.run_command(
            f"az functionapp config appsettings set --name {self.function_app} "
            f"--resource-group {self.resource_group} "
            f"--settings PYTHON_ENABLE_WORKER_EXTENSIONS=1 "
            f"FUNCTIONS_WORKER_RUNTIME=python "
            f"FUNCTIONS_EXTENSION_VERSION=~4",
            "Enable Python worker extensions",
        )
        step_results["tests"].append(
            {
                "test": "Python worker extensions",
                "status": "passed" if success else "failed",
                "output": output[:200] if output else None,
            }
        )

        # Test 2: Get storage connection string
        success_storage, storage_conn = self.run_command(
            f"az storage account show-connection-string "
            f"--name {self.storage_account} "
            f"--resource-group {self.resource_group} "
            f"--query connectionString --output tsv",
            "Get storage connection string",
        )
        step_results["tests"].append(
            {
                "test": "Storage connection string",
                "status": "passed" if success_storage else "failed",
                "output": "Retrieved" if success_storage else storage_conn[:200],
            }
        )

        # Test 3: Get Service Bus connection string
        success_sb, sb_conn = self.run_command(
            f"az servicebus namespace authorization-rule keys list "
            f"--resource-group {self.resource_group} "
            f"--namespace-name {self.service_bus} "
            f"--name RootManageSharedAccessKey "
            f"--query primaryConnectionString --output tsv",
            "Get Service Bus connection string",
        )
        step_results["tests"].append(
            {
                "test": "Service Bus connection string",
                "status": "passed" if success_sb else "failed",
                "output": "Retrieved" if success_sb else sb_conn[:200],
            }
        )

        # Test 4: Configure storage connection in Function App
        if success_storage:
            success_config, config_output = self.run_command(
                f"az functionapp config appsettings set --name {self.function_app} "
                f"--resource-group {self.resource_group} "
                f'--settings AzureWebJobsStorage="{storage_conn}"',
                "Configure storage connection",
            )
            step_results["tests"].append(
                {
                    "test": "Configure AzureWebJobsStorage",
                    "status": "passed" if success_config else "failed",
                    "output": "Configured" if success_config else config_output[:200],
                }
            )

        # Determine overall step status
        all_passed = all(t["status"] == "passed" for t in step_results["tests"])
        step_results["status"] = "completed" if all_passed else "failed"

        self.results["steps"]["step_1_configure"] = step_results

        logger.info(f"\nStep 1 Result: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        return all_passed

    async def step_2_validate_deployment(self) -> bool:
        """Validate all Azure resources are properly deployed."""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: VALIDATE DEPLOYMENT")
        logger.info("=" * 60)

        step_results = {"status": "running", "tests": []}

        # Test 1: Verify resource group
        success, output = self.run_command(
            f"az group show --name {self.resource_group} --query properties.provisioningState --output tsv",
            "Verify resource group exists",
        )
        step_results["tests"].append(
            {
                "test": "Resource group",
                "status": "passed" if success and output == "Succeeded" else "failed",
                "output": output,
            }
        )

        # Test 2: Verify storage account
        success, output = self.run_command(
            f"az storage account show --name {self.storage_account} "
            f"--resource-group {self.resource_group} "
            f"--query provisioningState --output tsv",
            "Verify storage account",
        )
        step_results["tests"].append(
            {
                "test": "Storage account",
                "status": "passed" if success and output == "Succeeded" else "failed",
                "output": output,
            }
        )

        # Test 3: Verify Key Vault
        success, output = self.run_command(
            f"az keyvault show --name {self.key_vault} "
            f"--resource-group {self.resource_group} "
            f"--query properties.provisioningState --output tsv",
            "Verify Key Vault",
        )
        step_results["tests"].append(
            {
                "test": "Key Vault",
                "status": "passed" if success else "failed",
                "output": output,
            }
        )

        # Test 4: Verify Service Bus
        success, output = self.run_command(
            f"az servicebus namespace show --name {self.service_bus} "
            f"--resource-group {self.resource_group} "
            f"--query provisioningState --output tsv",
            "Verify Service Bus",
        )
        step_results["tests"].append(
            {
                "test": "Service Bus",
                "status": "passed" if success and output == "Succeeded" else "failed",
                "output": output,
            }
        )

        # Test 5: Verify Function App
        success, output = self.run_command(
            f"az functionapp show --name {self.function_app} "
            f"--resource-group {self.resource_group} "
            f"--query state --output tsv",
            "Verify Function App",
        )
        step_results["tests"].append(
            {
                "test": "Function App",
                "status": "passed" if success and output == "Running" else "failed",
                "output": output,
            }
        )

        # Test 6: List all resources
        success, output = self.run_command(
            f'az resource list --resource-group {self.resource_group} --query "length(@)" --output tsv',
            "Count deployed resources",
        )
        step_results["tests"].append(
            {
                "test": "Resource count",
                "status": "passed" if success and int(output) >= 5 else "failed",
                "output": f"{output} resources" if success else output,
            }
        )

        # Determine overall step status
        all_passed = all(t["status"] == "passed" for t in step_results["tests"])
        step_results["status"] = "completed" if all_passed else "failed"

        self.results["steps"]["step_2_validate"] = step_results

        logger.info(f"\nStep 2 Result: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        return all_passed

    async def step_3_prepare_code_deployment(self) -> bool:
        """Prepare and provide guidance for code deployment."""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: PREPARE CODE DEPLOYMENT")
        logger.info("=" * 60)

        step_results = {"status": "running", "tests": [], "deployment_options": []}

        # Test 1: Check if Azure Functions Core Tools is installed
        success, output = self.run_command(
            "func --version", "Check Azure Functions Core Tools"
        )
        step_results["tests"].append(
            {
                "test": "Azure Functions Core Tools",
                "status": "passed" if success else "failed",
                "output": output if success else "Not installed",
            }
        )

        # Test 2: Check if function.json or host.json exists
        function_config_exists = os.path.exists(os.path.join(SCRIPT_DIR, "host.json"))
        step_results["tests"].append(
            {
                "test": "Function configuration",
                "status": "passed" if function_config_exists else "info",
                "output": (
                    "host.json found"
                    if function_config_exists
                    else "No host.json - needs creation"
                ),
            }
        )

        # Provide deployment options
        if success:  # func tools installed
            step_results["deployment_options"].append(
                {
                    "method": "Azure Functions Core Tools",
                    "command": f"func azure functionapp publish {self.function_app}",
                    "recommended": True,
                    "description": "Deploy directly from command line using func CLI",
                }
            )

        step_results["deployment_options"].append(
            {
                "method": "VS Code Extension",
                "steps": [
                    "1. Install 'Azure Functions' extension in VS Code",
                    "2. Sign in to Azure (Ctrl+Shift+P → Azure: Sign In)",
                    "3. Right-click function app in Azure panel → Deploy to Function App",
                ],
                "recommended": not success,
                "description": "Visual deployment using VS Code GUI",
            }
        )

        step_results["deployment_options"].append(
            {
                "method": "Azure CLI (ZIP Deploy)",
                "command": f"az functionapp deployment source config-zip --resource-group {self.resource_group} --name {self.function_app} --src deployment.zip",
                "recommended": False,
                "description": "Deploy pre-packaged ZIP file",
            }
        )

        step_results["status"] = "completed"
        self.results["steps"]["step_3_prepare_deployment"] = step_results

        logger.info("\n📦 CODE DEPLOYMENT OPTIONS:")
        for idx, option in enumerate(step_results["deployment_options"], 1):
            logger.info(f"\n{idx}. {option['method']}")
            if option.get("recommended"):
                logger.info("   ⭐ RECOMMENDED")
            logger.info(f"   {option['description']}")
            if "command" in option:
                logger.info(f"   Command: {option['command']}")
            if "steps" in option:
                for step in option["steps"]:
                    logger.info(f"   {step}")

        logger.info(f"\nStep 3 Result: ✅ COMPLETED (Guidance provided)")
        return True

    async def run_complete_workflow(self):
        """Execute all deployment steps in sequence."""
        logger.info("\n" + "=" * 60)
        logger.info("🚀 L.I.F.E PLATFORM - COMPLETE DEPLOYMENT WORKFLOW")
        logger.info("=" * 60)
        logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Resource Group: {self.resource_group}")
        logger.info(f"Function App: {self.function_app}")
        logger.info(f"Region: {self.region}")
        logger.info("=" * 60)

        try:
            # Step 1: Configure
            step1_success = await self.step_1_configure_function_app()
            if not step1_success:
                logger.warning("⚠️ Configuration had issues, but continuing...")

            # Step 2: Validate
            step2_success = await self.step_2_validate_deployment()
            if not step2_success:
                logger.error("❌ Validation failed - deployment may have issues!")
                self.results["workflow_status"] = "failed"
            else:
                self.results["workflow_status"] = "validation_passed"

            # Step 3: Prepare deployment
            step3_success = await self.step_3_prepare_code_deployment()

            # Generate final report
            self.generate_report()

            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("📊 WORKFLOW SUMMARY")
            logger.info("=" * 60)
            logger.info(
                f"Step 1 (Configure):  {'✅ PASSED' if step1_success else '❌ FAILED'}"
            )
            logger.info(
                f"Step 2 (Validate):   {'✅ PASSED' if step2_success else '❌ FAILED'}"
            )
            logger.info(
                f"Step 3 (Prepare):    {'✅ COMPLETED' if step3_success else '❌ FAILED'}"
            )
            logger.info("=" * 60)

            if step2_success:
                logger.info("\n🎉 YOUR L.I.F.E PLATFORM IS READY FOR CODE DEPLOYMENT!")
                logger.info("\n📋 NEXT STEPS:")
                logger.info("1. Review deployment options above")
                logger.info("2. Choose your preferred deployment method")
                logger.info("3. Deploy your L.I.F.E Platform code")
                logger.info(f"4. Check logs: {log_file}")
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_path = os.path.join(
                    RESULTS_DIR, f"complete_deployment_report_{timestamp_str}.json"
                )
                logger.info(f"5. View report: {report_path}")
            else:
                logger.error("\n⚠️ DEPLOYMENT VALIDATION FAILED")
                logger.error("Please review errors above and retry failed steps")

            return step2_success

        except Exception as e:
            logger.error(f"\n❌ WORKFLOW FAILED: {str(e)}")
            self.results["workflow_status"] = "error"
            self.results["error"] = str(e)
            self.generate_report()
            return False

    def generate_report(self):
        """Generate JSON report of deployment workflow."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(
            RESULTS_DIR, f"complete_deployment_report_{timestamp}.json"
        )

        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"\n📄 Report saved: {report_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")


async def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("🧠 L.I.F.E PLATFORM - COMPLETE DEPLOYMENT WORKFLOW")
    print("=" * 60)
    print("This workflow will:")
    print("1. ⚙️  Configure your Function App settings")
    print("2. ✅ Validate all deployed Azure resources")
    print("3. 📦 Prepare for code deployment")
    print("=" * 60)

    # Confirmation
    response = input("\nStart complete deployment workflow? (yes/no): ").strip().lower()
    if response != "yes":
        print("❌ Workflow cancelled by user")
        return False

    workflow = CompleteDeploymentWorkflow()
    success = await workflow.run_complete_workflow()

    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Workflow interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
