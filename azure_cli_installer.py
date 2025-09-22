#!/usr/bin/env python3
"""
L.I.F.E. Platform - Azure CLI Installer
Automated installation and configuration of Azure CLI for L.I.F.E. Platform

This module provides automated installation, configuration, and validation
of Azure CLI tools required for L.I.F.E. Platform deployment and management.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import logging
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AzureCLIInstaller:
    """
    Azure CLI Installer for L.I.F.E. Platform

    Handles automated installation, configuration, and validation of Azure CLI
    across different platforms (Windows, macOS, Linux).
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.installation_status = {}
        self.azure_cli_version = None
        self.extensions_status = {}

        logger.info(f"Azure CLI Installer initialized for {self.system} {self.machine}")

    def install_azure_cli(self) -> bool:
        """
        Install Azure CLI based on the current platform

        Returns:
            True if installation successful, False otherwise
        """
        logger.info("Starting Azure CLI installation...")

        try:
            if self.system == "windows":
                success = self._install_azure_cli_windows()
            elif self.system == "darwin":  # macOS
                success = self._install_azure_cli_macos()
            elif self.system == "linux":
                success = self._install_azure_cli_linux()
            else:
                logger.error(f"Unsupported platform: {self.system}")
                return False

            if success:
                logger.info("Azure CLI installation completed successfully")
                self.installation_status["cli_installed"] = True
                return True
            else:
                logger.error("Azure CLI installation failed")
                self.installation_status["cli_installed"] = False
                return False

        except Exception as e:
            logger.error(f"Azure CLI installation error: {e}")
            self.installation_status["cli_installed"] = False
            return False

    def _install_azure_cli_windows(self) -> bool:
        """Install Azure CLI on Windows"""
        logger.info("Installing Azure CLI on Windows...")

        try:
            # Check if winget is available (Windows Package Manager)
            winget_available = self._check_command_exists("winget")

            if winget_available:
                logger.info("Using winget for installation")
                result = subprocess.run(
                    [
                        "winget",
                        "install",
                        "-e",
                        "--id",
                        "Microsoft.AzureCLI",
                        "--accept-source-agreements",
                        "--accept-package-agreements",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )

                if result.returncode == 0:
                    logger.info("Azure CLI installed via winget")
                    return True
                else:
                    logger.warning(f"Winget installation failed: {result.stderr}")

            # Fallback to MSI installer
            logger.info("Attempting MSI installer fallback")
            msi_url = "https://aka.ms/installazurecliwindows"
            logger.info(f"Download Azure CLI MSI from: {msi_url}")
            logger.info(
                "Please run the MSI installer manually and then re-run this script"
            )

            # Try PowerShell installation method
            logger.info("Attempting PowerShell installation method")
            ps_command = """
            $ProgressPreference = 'SilentlyContinue'
            Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile azure-cli.msi
            Start-Process msiexec.exe -Wait -ArgumentList '/I azure-cli.msi /quiet'
            Remove-Item azure-cli.msi
            """

            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=600,
            )

            if result.returncode == 0:
                logger.info("Azure CLI installed via PowerShell MSI")
                return True
            else:
                logger.error(f"PowerShell installation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Azure CLI installation timed out")
            return False
        except Exception as e:
            logger.error(f"Windows installation error: {e}")
            return False

    def _install_azure_cli_macos(self) -> bool:
        """Install Azure CLI on macOS"""
        logger.info("Installing Azure CLI on macOS...")

        try:
            # Check if Homebrew is available
            brew_available = self._check_command_exists("brew")

            if brew_available:
                logger.info("Using Homebrew for installation")
                result = subprocess.run(
                    ["brew", "install", "azure-cli"],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )

                if result.returncode == 0:
                    logger.info("Azure CLI installed via Homebrew")
                    return True
                else:
                    logger.warning(f"Homebrew installation failed: {result.stderr}")

            # Fallback to direct download
            logger.info("Attempting direct download installation")
            install_script = """
            curl -L https://aka.ms/InstallAzureCli | bash
            """

            result = subprocess.run(
                ["bash", "-c", install_script],
                capture_output=True,
                text=True,
                timeout=600,
            )

            if result.returncode == 0:
                logger.info("Azure CLI installed via direct download")
                return True
            else:
                logger.error(f"Direct download installation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Azure CLI installation timed out")
            return False
        except Exception as e:
            logger.error(f"macOS installation error: {e}")
            return False

    def _install_azure_cli_linux(self) -> bool:
        """Install Azure CLI on Linux"""
        logger.info("Installing Azure CLI on Linux...")

        try:
            # Detect Linux distribution
            distro = self._detect_linux_distro()

            if distro in ["ubuntu", "debian"]:
                # Ubuntu/Debian installation
                logger.info("Installing on Ubuntu/Debian")
                commands = [
                    "curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/keyrings/microsoft.gpg > /dev/null",
                    "echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ jammy main' | tee /etc/apt/sources.list.d/azure-cli.list",
                    "apt-get update",
                    "apt-get install -y azure-cli",
                ]

                for cmd in commands:
                    result = subprocess.run(
                        ["sudo", "bash", "-c", cmd],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    if result.returncode != 0:
                        logger.error(f"Command failed: {cmd}")
                        logger.error(f"Error: {result.stderr}")
                        return False

                logger.info("Azure CLI installed on Ubuntu/Debian")
                return True

            elif distro in ["centos", "rhel", "fedora"]:
                # CentOS/RHEL/Fedora installation
                logger.info("Installing on CentOS/RHEL/Fedora")
                commands = [
                    "rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                    "echo -e '[azure-cli]\nname=Azure CLI\nbaseurl=https://packages.microsoft.com/yumrepos/azure-cli\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/azure-cli.repo",
                    (
                        "dnf install -y azure-cli"
                        if distro == "fedora"
                        else "yum install -y azure-cli"
                    ),
                ]

                for cmd in commands:
                    result = subprocess.run(
                        ["sudo", "bash", "-c", cmd],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    if result.returncode != 0:
                        logger.error(f"Command failed: {cmd}")
                        logger.error(f"Error: {result.stderr}")
                        return False

                logger.info("Azure CLI installed on CentOS/RHEL/Fedora")
                return True

            else:
                # Generic installation method
                logger.info("Attempting generic installation method")
                install_script = """
                curl -L https://aka.ms/InstallAzureCli | bash
                """

                result = subprocess.run(
                    ["bash", "-c", install_script],
                    capture_output=True,
                    text=True,
                    timeout=600,
                )

                if result.returncode == 0:
                    logger.info("Azure CLI installed via generic method")
                    return True
                else:
                    logger.error(f"Generic installation failed: {result.stderr}")
                    return False

        except subprocess.TimeoutExpired:
            logger.error("Azure CLI installation timed out")
            return False
        except Exception as e:
            logger.error(f"Linux installation error: {e}")
            return False

    def _detect_linux_distro(self) -> str:
        """Detect Linux distribution"""
        try:
            # Check /etc/os-release
            if Path("/etc/os-release").exists():
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                    if "ubuntu" in content:
                        return "ubuntu"
                    elif "debian" in content:
                        return "debian"
                    elif "centos" in content:
                        return "centos"
                    elif "rhel" in content:
                        return "rhel"
                    elif "fedora" in content:
                        return "fedora"

            # Check /etc/redhat-release
            if Path("/etc/redhat-release").exists():
                with open("/etc/redhat-release", "r") as f:
                    content = f.read().lower()
                    if "centos" in content:
                        return "centos"
                    elif "red hat" in content:
                        return "rhel"

            return "unknown"

        except Exception:
            return "unknown"

    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists on the system"""
        try:
            result = subprocess.run(["which", command], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def validate_installation(self) -> bool:
        """
        Validate Azure CLI installation and configuration

        Returns:
            True if validation successful, False otherwise
        """
        logger.info("Validating Azure CLI installation...")

        try:
            # Check if az command exists
            if not self._check_command_exists("az"):
                logger.error("Azure CLI command 'az' not found")
                self.installation_status["cli_validated"] = False
                return False

            # Get version
            result = subprocess.run(
                ["az", "version", "--output", "json"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                logger.error(f"Azure CLI version check failed: {result.stderr}")
                self.installation_status["cli_validated"] = False
                return False

            version_info = json.loads(result.stdout)
            self.azure_cli_version = version_info.get("azure-cli", "unknown")
            logger.info(f"Azure CLI version: {self.azure_cli_version}")

            # Check core functionality
            result = subprocess.run(
                ["az", "account", "list", "--output", "json"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                logger.info("Azure CLI core functionality validated")
                self.installation_status["cli_validated"] = True
                return True
            else:
                logger.warning("Azure CLI installed but not logged in")
                logger.info("Please run 'az login' to authenticate")
                self.installation_status["cli_validated"] = (
                    True  # CLI works, just needs login
                )
                return True

        except subprocess.TimeoutExpired:
            logger.error("Azure CLI validation timed out")
            self.installation_status["cli_validated"] = False
            return False
        except json.JSONDecodeError:
            logger.error("Failed to parse Azure CLI version output")
            self.installation_status["cli_validated"] = False
            return False
        except Exception as e:
            logger.error(f"Azure CLI validation error: {e}")
            self.installation_status["cli_validated"] = False
            return False

    def install_extensions(self, extensions: List[str] = None) -> bool:
        """
        Install required Azure CLI extensions

        Args:
            extensions: List of extensions to install (default: common ones)

        Returns:
            True if all extensions installed successfully
        """
        if extensions is None:
            extensions = ["azure-devops", "application-insights", "containerapp"]

        logger.info(f"Installing Azure CLI extensions: {extensions}")

        success_count = 0

        for extension in extensions:
            try:
                logger.info(f"Installing extension: {extension}")
                result = subprocess.run(
                    ["az", "extension", "add", "--name", extension],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                if result.returncode == 0:
                    logger.info(f"Extension {extension} installed successfully")
                    self.extensions_status[extension] = "installed"
                    success_count += 1
                else:
                    logger.error(
                        f"Failed to install extension {extension}: {result.stderr}"
                    )
                    self.extensions_status[extension] = "failed"

            except subprocess.TimeoutExpired:
                logger.error(f"Extension {extension} installation timed out")
                self.extensions_status[extension] = "timeout"
            except Exception as e:
                logger.error(f"Extension {extension} installation error: {e}")
                self.extensions_status[extension] = "error"

        self.installation_status["extensions_installed"] = success_count == len(
            extensions
        )
        logger.info(
            f"Extensions installation: {success_count}/{len(extensions)} successful"
        )

        return success_count == len(extensions)

    def configure_environment(self) -> bool:
        """
        Configure environment for Azure CLI usage

        Returns:
            True if configuration successful
        """
        logger.info("Configuring Azure CLI environment...")

        try:
            # Set Azure CLI configuration
            configs = [
                ("core.collect_telemetry", "no"),
                ("core.output", "json"),
                ("core.only_show_errors", "yes"),
            ]

            for key, value in configs:
                result = subprocess.run(
                    ["az", "config", "set", key, value],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode != 0:
                    logger.warning(
                        f"Failed to set config {key}={value}: {result.stderr}"
                    )

            # Create Azure CLI configuration directory if it doesn't exist
            az_config_dir = Path.home() / ".azure"
            az_config_dir.mkdir(exist_ok=True)

            logger.info("Azure CLI environment configured")
            self.installation_status["environment_configured"] = True
            return True

        except Exception as e:
            logger.error(f"Environment configuration error: {e}")
            self.installation_status["environment_configured"] = False
            return False

    def run_complete_setup(self) -> Dict[str, bool]:
        """
        Run complete Azure CLI setup process

        Returns:
            Dictionary with setup status for each component
        """
        logger.info("Starting complete Azure CLI setup...")

        setup_status = {}

        # Install CLI
        setup_status["cli_installation"] = self.install_azure_cli()

        # Validate installation
        if setup_status["cli_installation"]:
            setup_status["cli_validation"] = self.validate_installation()
        else:
            setup_status["cli_validation"] = False

        # Install extensions
        if setup_status["cli_validation"]:
            setup_status["extensions"] = self.install_extensions()
        else:
            setup_status["extensions"] = False

        # Configure environment
        if setup_status["cli_validation"]:
            setup_status["environment"] = self.configure_environment()
        else:
            setup_status["environment"] = False

        # Overall success
        setup_status["overall_success"] = all(setup_status.values())

        logger.info("Complete Azure CLI setup finished")
        logger.info(f"Setup status: {setup_status}")

        return setup_status

    def get_installation_report(self) -> Dict[str, any]:
        """
        Generate installation and configuration report

        Returns:
            Comprehensive report of installation status
        """
        return {
            "platform": {
                "system": self.system,
                "machine": self.machine,
                "python_version": sys.version,
            },
            "installation_status": self.installation_status,
            "azure_cli_version": self.azure_cli_version,
            "extensions_status": self.extensions_status,
            "configuration": {
                "workspace_path": str(self.workspace_path),
                "azure_config_dir": str(Path.home() / ".azure"),
            },
        }

    def export_report(self, filepath: str) -> bool:
        """
        Export installation report to file

        Args:
            filepath: Path to export the report

        Returns:
            True if export successful
        """
        try:
            report = self.get_installation_report()
            report["export_timestamp"] = str(datetime.now())

            with open(filepath, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Installation report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export report: {e}")
            return False


# Factory function for easy instantiation
def create_azure_cli_installer(
    workspace_path: Optional[str] = None,
) -> AzureCLIInstaller:
    """
    Factory function to create Azure CLI installer

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured AzureCLIInstaller instance
    """
    return AzureCLIInstaller(workspace_path)


# Command-line interface
def main():
    """Main CLI function for Azure CLI installation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform Azure CLI Installer"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--install", "-i", action="store_true", help="Install Azure CLI"
    )
    parser.add_argument(
        "--validate", "-v", action="store_true", help="Validate Azure CLI installation"
    )
    parser.add_argument(
        "--extensions",
        "-e",
        nargs="*",
        help="Install specific extensions (default: common ones)",
    )
    parser.add_argument(
        "--configure", "-c", action="store_true", help="Configure Azure CLI environment"
    )
    parser.add_argument(
        "--complete",
        action="store_true",
        help="Run complete setup (install + validate + extensions + configure)",
    )
    parser.add_argument("--report", "-r", help="Export installation report to file")

    args = parser.parse_args()

    # Create installer
    installer = create_azure_cli_installer(args.workspace)

    if args.complete:
        print("L.I.F.E. Platform - Azure CLI Complete Setup")
        print("=" * 50)
        status = installer.run_complete_setup()

        print("\nSetup Results:")
        for component, success in status.items():
            status_icon = "✅" if success else "❌"
            print(f"  {status_icon} {component}: {'Success' if success else 'Failed'}")

        if args.report:
            installer.export_report(args.report)
            print(f"\nReport exported to: {args.report}")

        return 0 if status["overall_success"] else 1

    # Individual operations
    success = True

    if args.install:
        success &= installer.install_azure_cli()

    if args.validate:
        success &= installer.validate_installation()

    if args.extensions is not None:
        extensions = args.extensions if args.extensions else None
        success &= installer.install_extensions(extensions)

    if args.configure:
        success &= installer.configure_environment()

    if args.report:
        success &= installer.export_report(args.report)
        print(f"Report exported to: {args.report}")

    # Show current status
    report = installer.get_installation_report()
    print("\nCurrent Status:")
    print(f"  Platform: {report['platform']['system']} {report['platform']['machine']}")
    print(f"  CLI Version: {report['azure_cli_version'] or 'Not installed'}")
    print(
        f"  CLI Installed: {report['installation_status'].get('cli_installed', False)}"
    )
    print(
        f"  CLI Validated: {report['installation_status'].get('cli_validated', False)}"
    )
    print(f"  Extensions: {len(report['extensions_status'])} installed")

    return 0 if success else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
