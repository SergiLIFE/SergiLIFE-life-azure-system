#!/usr/bin/env python3
"""
🔗 AZURE SPONSORSHIP VALIDATION - Quick Status Check
NAKEDai L.I.F.E. Platform - Corrected Subscription Metadata

Copyright 2025 - Sergio Paya Borrull
Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
Validates Microsoft Azure Sponsorship configuration
"""

import json
import os
from datetime import datetime

# Import Azure config modules
try:
    from azure_config import AzureIntegrationManager
    from AZURE_SUBSCRIPTION_MASTER_CONFIG import AzureSubscriptionConfig

    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Module import note: {e}")
    CONFIG_AVAILABLE = False


def validate_sponsorship_metadata():
    """Validate that all Azure configs now reference Microsoft Azure Sponsorship"""

    print("=" * 80)
    print("🔗 AZURE SPONSORSHIP VALIDATION CHECK")
    print("=" * 80)
    print(f"⏰ Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Account: Sergio Paya Borrull")
    print(f"🏢 Domain: lifecoach-121.com")
    print()

    results = {
        "validation_timestamp": datetime.now().isoformat(),
        "subscription_id": "5c88cef6-f243-497d-98af-6c6086d575ca",
        "expected_offer_type": "Azure Sponsorship",
        "expected_offer_id": "MS-AZR-0036P",
        "checks": {},
        "overall_status": "PENDING",
    }

    # Check 1: AZURE_SUBSCRIPTION_MASTER_CONFIG.py
    print("📋 Checking AZURE_SUBSCRIPTION_MASTER_CONFIG.py...")
    if CONFIG_AVAILABLE:
        config = AzureSubscriptionConfig.SUBSCRIPTION_CONFIG
        offer_type = config.get("offer_type")
        offer_id = config.get("offer_id")
        subscription_name = config.get("subscription_name")

        master_config_valid = (
            offer_type == "Azure Sponsorship"
            and offer_id == "MS-AZR-0036P"
            and "Sponsorship" in subscription_name
        )

        results["checks"]["master_config"] = {
            "status": "✅ PASS" if master_config_valid else "❌ FAIL",
            "offer_type": offer_type,
            "offer_id": offer_id,
            "subscription_name": subscription_name,
            "valid": master_config_valid,
        }

        print(f"   Subscription Name: {subscription_name}")
        print(f"   Offer Type: {offer_type}")
        print(f"   Offer ID: {offer_id}")
        print(f"   Status: {'✅ CORRECT' if master_config_valid else '❌ INCORRECT'}")
    else:
        results["checks"]["master_config"] = {
            "status": "⚠️  SKIPPED",
            "reason": "Module not available",
            "valid": False,
        }
        print("   ⚠️  Skipped (module not imported)")
    print()

    # Check 2: azure_config.py
    print("📋 Checking azure_config.py...")
    if CONFIG_AVAILABLE:
        try:
            manager = AzureIntegrationManager()
            azure_cfg = manager.config
            offer_type = azure_cfg.get("offer_type")
            offer_id = azure_cfg.get("offer_id")
            subscription_name = azure_cfg.get("subscription_name")

            azure_config_valid = (
                offer_type == "Azure Sponsorship"
                and offer_id == "MS-AZR-0036P"
                and "Sponsorship" in subscription_name
            )

            results["checks"]["azure_config"] = {
                "status": "✅ PASS" if azure_config_valid else "❌ FAIL",
                "offer_type": offer_type,
                "offer_id": offer_id,
                "subscription_name": subscription_name,
                "valid": azure_config_valid,
            }

            print(f"   Subscription Name: {subscription_name}")
            print(f"   Offer Type: {offer_type}")
            print(f"   Offer ID: {offer_id}")
            print(
                f"   Status: {'✅ CORRECT' if azure_config_valid else '❌ INCORRECT'}"
            )
        except Exception as e:
            results["checks"]["azure_config"] = {
                "status": "⚠️  ERROR",
                "error": str(e),
                "valid": False,
            }
            print(f"   ⚠️  Error during check: {e}")
    else:
        results["checks"]["azure_config"] = {
            "status": "⚠️  SKIPPED",
            "reason": "Module not available",
            "valid": False,
        }
        print("   ⚠️  Skipped (module not imported)")
    print()

    # Check 3: FLAWLESS_CONNECTION_VALIDATOR.py (scan file content)
    print("📋 Checking FLAWLESS_CONNECTION_VALIDATOR.py...")
    validator_path = "FLAWLESS_CONNECTION_VALIDATOR.py"
    if os.path.exists(validator_path):
        with open(validator_path, "r", encoding="utf-8") as f:
            content = f.read()
        has_sponsorship = "Azure Sponsorship" in content
        has_offer_id = "MS-AZR-0036P" in content
        no_payasyougo = "Pay-As-You-Go" not in content

        validator_valid = has_sponsorship and has_offer_id and no_payasyougo

        results["checks"]["validator_file"] = {
            "status": "✅ PASS" if validator_valid else "❌ FAIL",
            "has_sponsorship_text": has_sponsorship,
            "has_correct_offer_id": has_offer_id,
            "no_old_offer_type": no_payasyougo,
            "valid": validator_valid,
        }

        print(f"   Contains 'Azure Sponsorship': {has_sponsorship}")
        print(f"   Contains 'MS-AZR-0036P': {has_offer_id}")
        print(f"   No 'Pay-As-You-Go' references: {no_payasyougo}")
        print(f"   Status: {'✅ CORRECT' if validator_valid else '❌ INCORRECT'}")
    else:
        results["checks"]["validator_file"] = {"status": "⚠️  NOT FOUND", "valid": False}
        print("   ⚠️  File not found")
    print()

    # Overall assessment
    all_checks_passed = all(
        check.get("valid", False)
        for check in results["checks"].values()
        if check.get("status") != "⚠️  SKIPPED"
    )

    results["overall_status"] = (
        "✅ ALL VALIDATED" if all_checks_passed else "⚠️  ISSUES DETECTED"
    )

    print("=" * 80)
    print(f"📊 OVERALL STATUS: {results['overall_status']}")
    print("=" * 80)
    print()

    # Export results - save to workspace root for compatibility
    try:
        output_file = "azure_sponsorship_validation.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print(f"📁 Validation results exported to: {output_file}")
    except Exception as e:
        print(f"⚠️  Could not write results file: {e}")
        output_file = None
    print()

    # Summary report
    print("📝 VALIDATION SUMMARY:")
    print(f"   🔐 Subscription ID: {results['subscription_id']}")
    print(f"   🏷️  Expected Offer Type: {results['expected_offer_type']}")
    print(f"   🔑 Expected Offer ID: {results['expected_offer_id']}")
    print(f"   📊 Checks Performed: {len(results['checks'])}")
    print(f"   ✅ Status: {results['overall_status']}")
    print()

    if all_checks_passed:
        print("🎉 SUCCESS: All Azure configurations correctly reference")
        print("   Microsoft Azure Sponsorship!")
        print("🚀 Platform ready with corrected subscription metadata.")
    else:
        print("⚠️  ATTENTION: Some configurations may need manual verification.")
        if output_file:
            print(f"   Review details in: {output_file}")

    print("=" * 80)

    return results


if __name__ == "__main__":
    try:
        print("\n🔧 Azure Sponsorship Metadata Validation")
        print(f"📅 Date: {datetime.now().strftime('%B %d, %Y')}\n")

        results = validate_sponsorship_metadata()

        # Exit code based on validation status
        exit_code = 0 if results["overall_status"] == "✅ ALL VALIDATED" else 1
        exit(exit_code)

    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        import traceback

        traceback.print_exc()
        exit(2)
