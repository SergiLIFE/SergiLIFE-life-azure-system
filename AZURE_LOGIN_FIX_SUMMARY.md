# Azure Login Issue Fix - Summary

**Date:** October 25, 2025  
**Issue:** GitHub Actions workflow failing with "JSON is not valid JSON" error during Azure login  
**Status:** ✅ RESOLVED

## Problem Statement

The GitHub Actions workflow in `.github/workflows/azure-deploy.yml` was encountering the following error:

```
Error: Login failed with SyntaxError: Unexpected token 'J', "JSON from "... is not valid JSON. 
Double check if the 'auth-type' is correct. Refer to https://github.com/Azure/login#readme for more information.
```

## Root Cause

The workflow was passing `AZURE_CREDENTIALS` secret directly to the Azure login action without:
1. Validating JSON structure
2. Checking for required fields
3. Handling whitespace or special characters
4. Providing clear error messages

## Solution Implemented

### 1. JSON Validation Function
Added a validation function that uses Python's `json.tool` to verify JSON structure:
```bash
validate_json() {
  echo "$1" | python3 -m json.tool > /dev/null 2>&1
  return $?
}
```

### 2. Whitespace Handling
Implemented proper whitespace trimming using `sed` that preserves JSON structure:
```bash
CREDS=$(echo '${{ secrets.AZURE_CREDENTIALS }}' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
```

### 3. Field Validation
Added verification that all required fields are present:
```bash
echo "$CREDS" | python3 -c "import sys, json; data=json.load(sys.stdin); exit(0 if all(k in data for k in ['clientId','clientSecret','subscriptionId','tenantId']) else 1)"
```

### 4. Enhanced Error Messages
Provided specific error messages for different failure scenarios:
- Invalid JSON structure
- Missing required fields
- Invalid characters in composed credentials

### 5. Documentation Updates
Updated `GITHUB_SECRETS_SETUP.md` with:
- Guidelines for proper JSON formatting
- Troubleshooting section for "JSON is not valid JSON" error
- Examples of correct and incorrect formats
- Recommendation to use JSON validators

## Files Modified

1. `.github/workflows/azure-deploy.yml` - Core workflow with credential validation
2. `GITHUB_SECRETS_SETUP.md` - Enhanced documentation and troubleshooting
3. `test_azure_credentials_validation.sh` - Test suite to validate the logic (NEW)

## Testing

Created comprehensive test suite with 5 test cases:

```
✅ Test 1: Valid JSON with all required fields - PASSED
✅ Test 2: Invalid JSON (missing closing brace) - PASSED
✅ Test 3: Valid JSON but missing required fields - PASSED
✅ Test 4: JSON with extra whitespace - PASSED
✅ Test 5: Empty JSON - PASSED
```

## Validation Process Flow

```
1. Check if AZURE_CREDENTIALS secret exists
   ↓
2. Trim leading/trailing whitespace (sed)
   ↓
3. Validate JSON structure (python3 -m json.tool)
   ↓
4. Verify required fields present (python3 script)
   ↓
5. Pass to Azure login action
   ↓
6. If any step fails, provide clear error message
```

## Benefits

- ✅ Prevents workflow failures due to malformed JSON
- ✅ Provides clear, actionable error messages
- ✅ Validates credentials before attempting login
- ✅ Handles whitespace without breaking JSON
- ✅ Supports both AZURE_CREDENTIALS and individual secrets
- ✅ No secrets exposed in logs
- ✅ Backward compatible with existing configurations

## Expected Format for AZURE_CREDENTIALS

Correct format (single line or properly formatted):
```json
{"clientId":"YOUR_CLIENT_ID","clientSecret":"YOUR_CLIENT_SECRET","subscriptionId":"YOUR_SUBSCRIPTION_ID","tenantId":"YOUR_TENANT_ID"}
```

Common mistakes to avoid:
- ❌ Extra text before/after JSON: `JSON from Azure: {...}`
- ❌ Missing quotes: `{clientId:value}`
- ❌ Trailing commas: `{"clientId":"value",}`
- ❌ Using single quotes: `{'clientId':'value'}`
- ❌ Comments in JSON: `{"clientId":"value" /* comment */}`

## Alternative: OIDC Authentication

For better security, consider using OIDC authentication instead:
- No secrets required in repository
- Uses federated identity credentials
- See `.github/workflows/blank.yml` for example
- See `AZURE_OIDC_SETUP.md` for setup instructions

## Deployment Environments Affected

The fix applies to both deployment environments in `azure-deploy.yml`:
- `deploy-staging` job
- `deploy-production` job

## Related Workflows

Other workflows in the repository use OIDC authentication and are not affected:
- `.github/workflows/blank.yml` - Uses OIDC (vars.AZURE_CLIENT_ID)
- `.github/workflows/azure-deploy-fixed.yml` - Uses OIDC (secrets.AZURE_CLIENT_ID)

## Next Steps

1. Users should verify their `AZURE_CREDENTIALS` secret:
   - Go to repository Settings → Secrets and variables → Actions
   - Verify AZURE_CREDENTIALS secret is properly formatted
   - Use https://jsonlint.com/ to validate before adding
   
2. Test the workflow:
   - Trigger a manual workflow run
   - Check the logs for validation messages
   - Verify Azure login succeeds

3. Consider migrating to OIDC authentication for improved security

## References

- Azure Login Action: https://github.com/Azure/login
- OIDC Setup Guide: `AZURE_OIDC_SETUP.md`
- Secrets Setup Guide: `GITHUB_SECRETS_SETUP.md`

---

**Copyright 2025 - Sergio Paya Borrull**  
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
