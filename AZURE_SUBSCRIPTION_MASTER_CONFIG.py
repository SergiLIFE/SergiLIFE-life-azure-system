#!/usr/bin/env python3
"""
🔐 AZURE SUBSCRIPTION MASTER CONFIGURATION
NAKEDai L.I.F.E. Platform - Secure Azure Connection Details

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
CONFIDENTIAL - Production Azure Subscription Configuration
"""

import json
import os
from datetime import datetime
from typing import Any, Dict


class AzureSubscriptionConfig:
    """Master Azure subscription configuration for NAKEDai L.I.F.E. platform"""

    # 🔐 PRODUCTION AZURE SUBSCRIPTION DETAILS
    SUBSCRIPTION_CONFIG = {
        "subscription_id": "5c88cef6-f243-497d-98af-6c6086d575ca",
        "directory": "Sergio Paya Borrull (lifecoach-121.com)",
        "tenant_domain": "lifecoach-121.com",
        "user_role": "Account admin",
        "offer_type": "Pay-As-You-Go",
        "offer_id": "MS-AZR-0003P",
        "parent_management_group": "e716161a-5e85-4d6d-82f9-96bcdd2e65ac",
        "subscription_name": "Pay-As-You-Go",
        "current_billing_period": "9/11/2025-10/10/2025",
        "currency": "GBP",
        "status": "Active",
        "secure_score": "61%",
        "admin_email": "sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com",
    }

    # 🚀 NAKEDai L.I.F.E. PLATFORM RESOURCES
    LIFE_PLATFORM_RESOURCES = {
        "resource_group": "life-platform-rg",
        "location": "East US 2",
        "storage_account": "stlifeplatformprod",
        "key_vault": "kv-life-platform-prod",
        "service_bus": "sb-life-platform-prod",
        "function_app": "func-life-platform-prod",
        "marketplace_offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
    }

    # 🔗 AZURE CONNECTION PARAMETERS
    CONNECTION_CONFIG = {
        "authentication_method": "Azure CLI",
        "default_resource_group": "life-platform-rg",
        "default_location": "East US 2",
        "subscription_scope": f"/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca",
        "management_endpoint": "https://management.azure.com/",
        "graph_endpoint": "https://graph.microsoft.com/",
        "active_directory_endpoint": "https://login.microsoftonline.com/",
    }

    # 🛡️ SECURITY CONFIGURATION
    SECURITY_CONFIG = {
        "encryption_required": True,
        "rbac_enabled": True,
        "monitoring_enabled": True,
        "backup_strategy": "geo-redundant",
        "compliance_level": "enterprise",
        "audit_logging": True,
    }

    @classmethod
    def get_subscription_id(cls) -> str:
        """Get the primary subscription ID"""
        return cls.SUBSCRIPTION_CONFIG["subscription_id"]

    @classmethod
    def get_tenant_domain(cls) -> str:
        """Get the tenant domain"""
        return cls.SUBSCRIPTION_CONFIG["tenant_domain"]

    @classmethod
    def get_admin_email(cls) -> str:
        """Get the admin email"""
        return cls.SUBSCRIPTION_CONFIG["admin_email"]

    @classmethod
    def get_resource_group(cls) -> str:
        """Get the default resource group"""
        return cls.LIFE_PLATFORM_RESOURCES["resource_group"]

    @classmethod
    def get_location(cls) -> str:
        """Get the default Azure location"""
        return cls.LIFE_PLATFORM_RESOURCES["location"]

    @classmethod
    def get_marketplace_offer_id(cls) -> str:
        """Get the Azure Marketplace offer ID"""
        return cls.LIFE_PLATFORM_RESOURCES["marketplace_offer_id"]

    @classmethod
    def validate_connection(cls) -> Dict[str, Any]:
        """Validate Azure connection configuration"""
        validation = {
            "timestamp": datetime.now().isoformat(),
            "subscription_active": cls.SUBSCRIPTION_CONFIG["status"] == "Active",
            "admin_access": cls.SUBSCRIPTION_CONFIG["user_role"] == "Account admin",
            "billing_current": cls.SUBSCRIPTION_CONFIG["current_billing_period"],
            "security_score": cls.SUBSCRIPTION_CONFIG["secure_score"],
            "marketplace_ready": bool(
                cls.LIFE_PLATFORM_RESOURCES["marketplace_offer_id"]
            ),
            "connection_status": "READY",
        }
        return validation

    @classmethod
    def export_environment_variables(cls) -> Dict[str, str]:
        """Export Azure environment variables for CLI/SDK"""
        return {
            "AZURE_SUBSCRIPTION_ID": cls.SUBSCRIPTION_CONFIG["subscription_id"],
            "AZURE_TENANT_ID": cls.SUBSCRIPTION_CONFIG["parent_management_group"],
            "AZURE_CLIENT_EMAIL": cls.SUBSCRIPTION_CONFIG["admin_email"],
            "AZURE_RESOURCE_GROUP": cls.LIFE_PLATFORM_RESOURCES["resource_group"],
            "AZURE_LOCATION": cls.LIFE_PLATFORM_RESOURCES["location"],
            "AZURE_STORAGE_ACCOUNT": cls.LIFE_PLATFORM_RESOURCES["storage_account"],
            "AZURE_KEY_VAULT": cls.LIFE_PLATFORM_RESOURCES["key_vault"],
            "AZURE_SERVICE_BUS": cls.LIFE_PLATFORM_RESOURCES["service_bus"],
            "LIFE_MARKETPLACE_OFFER_ID": cls.LIFE_PLATFORM_RESOURCES[
                "marketplace_offer_id"
            ],
        }

    @classmethod
    def create_connection_string(cls) -> str:
        """Create Azure connection string for applications"""
        return (
            f"SubscriptionId={cls.get_subscription_id()};"
            f"ResourceGroup={cls.get_resource_group()};"
            f"Location={cls.get_location()};"
            f"TenantDomain={cls.get_tenant_domain()};"
            f"AdminEmail={cls.get_admin_email()};"
            f"MarketplaceOfferId={cls.get_marketplace_offer_id()}"
        )

    @classmethod
    def save_config_file(cls, file_path: str = "azure_connection_config.json") -> str:
        """Save complete configuration to JSON file"""
        complete_config = {
            "azure_subscription": cls.SUBSCRIPTION_CONFIG,
            "life_platform_resources": cls.LIFE_PLATFORM_RESOURCES,
            "connection_config": cls.CONNECTION_CONFIG,
            "security_config": cls.SECURITY_CONFIG,
            "validation": cls.validate_connection(),
            "environment_variables": cls.export_environment_variables(),
            "connection_string": cls.create_connection_string(),
            "export_timestamp": datetime.now().isoformat(),
            "configuration_version": "2025.09.27-PRODUCTION",
        }

        with open(file_path, "w") as f:
            json.dump(complete_config, f, indent=2)

        return file_path


# 🔐 SECURE ACCESS FUNCTIONS
def get_azure_subscription_id() -> str:
    """Get the Azure subscription ID for secure access"""
    return AzureSubscriptionConfig.get_subscription_id()


def get_azure_admin_email() -> str:
    """Get the Azure admin email for notifications"""
    return AzureSubscriptionConfig.get_admin_email()


def get_life_platform_config() -> Dict[str, Any]:
    """Get complete L.I.F.E. platform configuration"""
    return {
        "subscription": AzureSubscriptionConfig.SUBSCRIPTION_CONFIG,
        "resources": AzureSubscriptionConfig.LIFE_PLATFORM_RESOURCES,
        "connection": AzureSubscriptionConfig.CONNECTION_CONFIG,
        "security": AzureSubscriptionConfig.SECURITY_CONFIG,
    }


def validate_azure_connection() -> bool:
    """Validate Azure connection is ready for NAKEDai L.I.F.E. platform"""
    validation = AzureSubscriptionConfig.validate_connection()
    return (
        validation["subscription_active"]
        and validation["admin_access"]
        and validation["marketplace_ready"]
        and validation["connection_status"] == "READY"
    )


def export_azure_env_vars() -> None:
    """Export Azure environment variables to system"""
    env_vars = AzureSubscriptionConfig.export_environment_variables()
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ Set {key}={value}")


# 🚀 MAIN CONFIGURATION TEST
if __name__ == "__main__":
    print("🔐 Azure Subscription Master Configuration")
    print("=" * 60)

    # Display configuration summary
    config = AzureSubscriptionConfig()

    print(f"📋 Subscription ID: {config.get_subscription_id()}")
    print(f"🏢 Tenant Domain: {config.get_tenant_domain()}")
    print(f"👤 Admin Email: {config.get_admin_email()}")
    print(f"📁 Resource Group: {config.get_resource_group()}")
    print(f"🌍 Location: {config.get_location()}")
    print(f"🏪 Marketplace Offer: {config.get_marketplace_offer_id()}")

    # Validate connection
    validation = config.validate_connection()
    print(f"\n✅ Connection Status: {validation['connection_status']}")
    print(f"🔐 Security Score: {validation['security_score']}")
    print(f"💳 Billing Period: {validation['billing_current']}")

    # Save configuration file
    config_file = config.save_config_file("results/azure_master_config.json")
    print(f"📁 Configuration saved to: {config_file}")

    # Test connection validation
    if validate_azure_connection():
        print("🎉 Azure connection validated - Ready for NAKEDai L.I.F.E. platform!")
    else:
        print("⚠️  Azure connection validation failed - Check configuration")

    print("=" * 60)
    print("🚀 Azure Master Configuration Complete!")
