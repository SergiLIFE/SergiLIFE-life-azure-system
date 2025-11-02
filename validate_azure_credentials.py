#!/usr/bin/env python3
"""
Azure Credentials JSON Validator

This script validates the format of Azure service principal credentials
to ensure they are properly formatted for GitHub Actions.

Usage:
    python validate_azure_credentials.py <credentials_file.json>
    python validate_azure_credentials.py --stdin  # Read from stdin
    python validate_azure_credentials.py --generate  # Generate template

Author: L.I.F.E Platform
Date: November 2, 2025
"""

import json
import sys
import argparse
from typing import Dict, List, Tuple


# Required fields for Azure login action with service principal
REQUIRED_FIELDS = [
    "clientId",
    "clientSecret",
    "subscriptionId",
    "tenantId"
]

# Optional but recommended fields (for --sdk-auth format)
OPTIONAL_FIELDS = [
    "activeDirectoryEndpointUrl",
    "resourceManagerEndpointUrl",
    "activeDirectoryGraphResourceId",
    "sqlManagementEndpointUrl",
    "galleryEndpointUrl",
    "managementEndpointUrl"
]

# Expected default values for Azure public cloud
DEFAULT_URLS = {
    "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
    "resourceManagerEndpointUrl": "https://management.azure.com/",
    "activeDirectoryGraphResourceId": "https://graph.windows.net/",
    "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
    "galleryEndpointUrl": "https://gallery.azure.com/",
    "managementEndpointUrl": "https://management.core.windows.net/"
}


def validate_json_structure(json_str: str) -> Tuple[bool, Dict, List[str]]:
    """
    Validate the JSON structure of Azure credentials.
    
    Returns:
        Tuple of (is_valid, parsed_json, errors)
    """
    errors = []
    
    # Check for common issues before parsing
    json_str = json_str.strip()
    
    # Check for descriptive text before JSON
    if json_str.startswith(("JSON from", "Azure credentials:", "Credentials:", "Output:")):
        errors.append("❌ JSON contains descriptive text at the beginning. Remove all text before the opening '{'")
        # Try to find the actual JSON
        brace_index = json_str.find('{')
        if brace_index > 0:
            json_str = json_str[brace_index:]
            errors.append("   Attempting to extract JSON starting from first '{'...")
    
    # Check if wrapped in extra quotes
    if json_str.startswith('"') and json_str.endswith('"'):
        errors.append("❌ JSON is wrapped in extra quotes. Remove outer quotes.")
        return False, {}, errors
    
    # Try to parse JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        errors.append(f"❌ Invalid JSON format: {e}")
        errors.append(f"   Error at line {e.lineno}, column {e.colno}")
        return False, {}, errors
    
    # Check if it's a dictionary
    if not isinstance(data, dict):
        errors.append("❌ JSON root must be an object (dictionary), not an array or primitive")
        return False, {}, errors
    
    return True, data, errors


def validate_required_fields(data: Dict) -> List[str]:
    """Validate that all required fields are present."""
    errors = []
    
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"❌ Missing required field: '{field}'")
        elif not data[field]:
            errors.append(f"❌ Required field '{field}' is empty")
        elif not isinstance(data[field], str):
            errors.append(f"❌ Field '{field}' must be a string, got {type(data[field]).__name__}")
    
    return errors


def validate_field_formats(data: Dict) -> List[str]:
    """Validate the format of specific fields."""
    errors = []
    warnings = []
    
    # Validate GUID format for clientId and tenantId
    import re
    guid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    
    if "clientId" in data:
        if not re.match(guid_pattern, data["clientId"]):
            errors.append(f"❌ 'clientId' does not match GUID format: {data['clientId']}")
    
    if "tenantId" in data:
        if not re.match(guid_pattern, data["tenantId"]):
            errors.append(f"❌ 'tenantId' does not match GUID format: {data['tenantId']}")
    
    if "subscriptionId" in data:
        if not re.match(guid_pattern, data["subscriptionId"]):
            errors.append(f"❌ 'subscriptionId' does not match GUID format: {data['subscriptionId']}")
    
    # Validate clientSecret (should be a non-empty string)
    if "clientSecret" in data:
        if len(data["clientSecret"]) < 10:
            warnings.append(f"⚠️  'clientSecret' seems too short ({len(data['clientSecret'])} chars). Typical secrets are 30+ characters.")
    
    # Check URL formats
    url_fields = [
        "activeDirectoryEndpointUrl",
        "resourceManagerEndpointUrl",
        "activeDirectoryGraphResourceId",
        "sqlManagementEndpointUrl",
        "galleryEndpointUrl",
        "managementEndpointUrl"
    ]
    
    for field in url_fields:
        if field in data:
            if not data[field].startswith(("http://", "https://")):
                warnings.append(f"⚠️  '{field}' should be a URL starting with http:// or https://")
    
    return errors, warnings


def validate_completeness(data: Dict) -> List[str]:
    """Check if optional fields are present for full --sdk-auth format."""
    missing = []
    
    for field in OPTIONAL_FIELDS:
        if field not in data:
            missing.append(f"ℹ️  Optional field '{field}' is missing (OK for basic auth, required for --sdk-auth)")
    
    return missing


def validate_known_values(data: Dict) -> List[str]:
    """Validate against known values for L.I.F.E Platform."""
    warnings = []
    
    # Check subscription ID
    expected_subscription = "5c88cef6-f243-497d-98af-6c6086d575ca"
    if "subscriptionId" in data and data["subscriptionId"] != expected_subscription:
        warnings.append(f"⚠️  Subscription ID doesn't match expected L.I.F.E Platform subscription")
        warnings.append(f"   Expected: {expected_subscription}")
        warnings.append(f"   Got: {data['subscriptionId']}")
    
    # Check tenant ID
    expected_tenant = "e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
    if "tenantId" in data and data["tenantId"] != expected_tenant:
        warnings.append(f"⚠️  Tenant ID doesn't match expected L.I.F.E Platform tenant")
        warnings.append(f"   Expected: {expected_tenant}")
        warnings.append(f"   Got: {data['tenantId']}")
    
    # Check default URLs for Azure public cloud
    for field, expected_url in DEFAULT_URLS.items():
        if field in data and data[field] != expected_url:
            warnings.append(f"⚠️  '{field}' has non-standard value")
            warnings.append(f"   Expected: {expected_url}")
            warnings.append(f"   Got: {data[field]}")
    
    return warnings


def generate_template():
    """Generate a template for Azure credentials."""
    template = {
        "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "subscriptionId": "5c88cef6-f243-497d-98af-6c6086d575ca",
        "tenantId": "e716161a-5e85-4d6d-82f9-96bcdd2e65ac",
        "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
        "resourceManagerEndpointUrl": "https://management.azure.com/",
        "activeDirectoryGraphResourceId": "https://graph.windows.net/",
        "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
        "galleryEndpointUrl": "https://gallery.azure.com/",
        "managementEndpointUrl": "https://management.core.windows.net/"
    }
    
    print("=" * 80)
    print("Azure Credentials Template (--sdk-auth format)")
    print("=" * 80)
    print("\nReplace the 'x' characters with your actual values:\n")
    print(json.dumps(template, indent=2))
    print("\n" + "=" * 80)
    print("To generate actual credentials, run:")
    print("=" * 80)
    print("\naz ad sp create-for-rbac \\")
    print("  --name 'github-actions-life-platform' \\")
    print("  --role contributor \\")
    print("  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod \\")
    print("  --sdk-auth")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate Azure service principal credentials for GitHub Actions",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to JSON file containing Azure credentials"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read JSON from stdin"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate a template for Azure credentials"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation information"
    )
    
    args = parser.parse_args()
    
    # Generate template mode
    if args.generate:
        generate_template()
        return 0
    
    # Read input
    if args.stdin:
        json_str = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                json_str = f.read()
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found")
            return 1
        except IOError as e:
            print(f"❌ Error reading file: {e}")
            return 1
    else:
        parser.print_help()
        return 1
    
    # Validate
    print("=" * 80)
    print("Azure Credentials Validation Report")
    print("=" * 80)
    print()
    
    # Step 1: Validate JSON structure
    print("Step 1: Validating JSON structure...")
    is_valid, data, struct_errors = validate_json_structure(json_str)
    
    if struct_errors:
        for error in struct_errors:
            print(error)
    
    if not is_valid:
        print("\n❌ VALIDATION FAILED: Invalid JSON structure")
        print("\nPlease fix the JSON format and try again.")
        return 1
    
    print("✅ JSON structure is valid")
    print()
    
    # Step 2: Validate required fields
    print("Step 2: Checking required fields...")
    field_errors = validate_required_fields(data)
    
    if field_errors:
        for error in field_errors:
            print(error)
        print("\n❌ VALIDATION FAILED: Missing or invalid required fields")
        return 1
    
    print("✅ All required fields are present")
    print()
    
    # Step 3: Validate field formats
    print("Step 3: Validating field formats...")
    format_errors, format_warnings = validate_field_formats(data)
    
    if format_errors:
        for error in format_errors:
            print(error)
        print("\n❌ VALIDATION FAILED: Invalid field formats")
        return 1
    
    print("✅ Field formats are valid")
    
    if format_warnings:
        print()
        for warning in format_warnings:
            print(warning)
    
    print()
    
    # Step 4: Check completeness
    if args.verbose:
        print("Step 4: Checking completeness (--sdk-auth format)...")
        missing = validate_completeness(data)
        
        if missing:
            for info in missing:
                print(info)
        else:
            print("✅ All optional fields are present (full --sdk-auth format)")
        
        print()
    
    # Step 5: Validate known values
    print("Step 5: Validating against L.I.F.E Platform configuration...")
    value_warnings = validate_known_values(data)
    
    if value_warnings:
        for warning in value_warnings:
            print(warning)
    else:
        print("✅ All values match expected L.I.F.E Platform configuration")
    
    print()
    
    # Summary
    print("=" * 80)
    print("✅ VALIDATION SUCCESSFUL")
    print("=" * 80)
    print()
    print("Your Azure credentials are properly formatted for GitHub Actions!")
    print()
    print("Next steps:")
    print("1. Copy the JSON to GitHub Secrets:")
    print("   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions")
    print("2. Create or update the 'AZURE_CREDENTIALS' secret")
    print("3. Paste the ENTIRE JSON (no extra text)")
    print("4. Save the secret")
    print("5. Re-run your failed GitHub Actions workflow")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
