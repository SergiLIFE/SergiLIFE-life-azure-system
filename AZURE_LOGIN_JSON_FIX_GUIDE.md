# 🔧 Azure Login JSON Syntax Error - Fix Guide

**Date:** November 2, 2025  
**Issue:** GitHub Actions Azure login failing with JSON parsing error  
**Error Message:** `Login failed with SyntaxError: Unexpected token 'J', "JSON from "... is not valid JSON`

---

## 🎯 Problem Summary

The GitHub Actions workflow is failing when attempting to authenticate with Azure because the `AZURE_CREDENTIALS` secret contains invalid JSON format.

### Common Causes:
1. ❌ Secret contains descriptive text instead of actual JSON (e.g., "JSON from Azure CLI:")
2. ❌ JSON is malformed (missing brackets, commas, or quotes)
3. ❌ Extra characters before or after the JSON
4. ❌ Line breaks or formatting issues in the secret value

---

## ✅ Solution Steps

### Step 1: Generate Valid Azure Credentials

Open Azure Cloud Shell or use Azure CLI locally:

```bash
# Login to Azure (if not already logged in)
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac

# Set the correct subscription
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

# Create a new service principal with proper JSON output
az ad sp create-for-rbac \
  --name "github-actions-life-platform-$(date +%Y%m%d%H%M)" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod \
  --sdk-auth
```

**Note:** The `--sdk-auth` flag is deprecated but still required for GitHub Actions compatibility with the `azure/login@v2` action using the `creds` parameter.

### Step 2: Copy the ENTIRE JSON Output

The command will output JSON like this. **Copy everything including the outer curly braces:**

```json
{
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
```

### Step 3: Update GitHub Secret

1. **Navigate to GitHub Secrets:**
   ```
   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
   ```

2. **Update AZURE_CREDENTIALS:**
   - Click on the `AZURE_CREDENTIALS` secret (or create it if it doesn't exist)
   - **Delete the entire old value**
   - **Paste ONLY the JSON** (no extra text, no "JSON from Azure CLI:", just the JSON)
   - Ensure no extra spaces before or after the JSON
   - Click "Update secret" or "Add secret"

### Step 4: Verify the Fix

1. Navigate to the failed workflow run:
   ```
   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions/runs/18773338571
   ```

2. Click "Re-run failed jobs" or "Re-run all jobs"

3. Monitor the "🔑 Azure Login" step - it should now succeed

---

## 🔍 How to Identify Invalid JSON

### ❌ WRONG - Contains Descriptive Text:
```
JSON from Azure CLI:
{
  "clientId": "...",
  ...
}
```

### ❌ WRONG - Missing Outer Braces:
```
"clientId": "...",
"clientSecret": "...",
...
```

### ❌ WRONG - Extra Quotes:
```
"{\"clientId\": \"...\", ...}"
```

### ✅ CORRECT - Clean JSON Only:
```json
{
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
```

---

## 🚀 Alternative: Switch to OIDC (Recommended)

For better security and to avoid the deprecated `--sdk-auth` flag, consider switching to OpenID Connect (OIDC) authentication:

### Benefits:
- ✅ No stored secrets (uses federated identity)
- ✅ Automatic credential rotation
- ✅ Better security posture
- ✅ No deprecation warnings

### Implementation Steps:

#### 1. Update Workflow Files

Replace the Azure login step in your workflow files:

**Before (using credentials):**
```yaml
- name: 🔑 Azure Login
  uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```

**After (using OIDC):**
```yaml
- name: 🔑 Azure Login
  uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

#### 2. Configure Federated Credentials in Azure

```bash
# Get your GitHub repository details
GITHUB_ORG="SergiLIFE"
GITHUB_REPO="SergiLIFE-life-azure-system"
APP_ID="<your-service-principal-app-id>"

# Add federated credential for main branch
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-actions-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'$GITHUB_ORG'/'$GITHUB_REPO':ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Add federated credential for pull requests (optional)
az ad app federated-credential create \
  --id $APP_ID \
  --parameters '{
    "name": "github-actions-pr",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:'$GITHUB_ORG'/'$GITHUB_REPO':pull_request",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

#### 3. Update GitHub Secrets

Replace `AZURE_CREDENTIALS` with these three secrets:

- `AZURE_CLIENT_ID`: The service principal's application (client) ID
- `AZURE_TENANT_ID`: `e716161a-5e85-4d6d-82f9-96bcdd2e65ac`
- `AZURE_SUBSCRIPTION_ID`: `5c88cef6-f243-497d-98af-6c6086d575ca`

#### 4. Add Required Workflow Permissions

Add this to the top of your workflow file:

```yaml
permissions:
  id-token: write
  contents: read
```

---

## 🔧 Validation Script

To validate your Azure credentials JSON format before adding to GitHub:

```bash
# Save your credentials to a temporary file
az ad sp create-for-rbac \
  --name "github-actions-life-platform-validation" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod \
  --sdk-auth > /tmp/azure_creds.json

# Validate JSON format
python3 -m json.tool /tmp/azure_creds.json

# If no errors, the JSON is valid
# Copy the content to GitHub secrets
cat /tmp/azure_creds.json

# Clean up
rm /tmp/azure_creds.json
```

---

## 📋 Required GitHub Secrets Checklist

After fixing, ensure all these secrets are configured:

- ✅ `AZURE_CREDENTIALS` - Valid JSON service principal credentials
- ✅ `AZURE_SUBSCRIPTION_ID` - `5c88cef6-f243-497d-98af-6c6086d575ca`
- ✅ `AZURE_TENANT_ID` - `e716161a-5e85-4d6d-82f9-96bcdd2e65ac`
- ⚠️  `AZURE_CLIENT_ID` - (Required only for OIDC)
- ⚠️  `AZURE_RG_STAGING` - Resource group name (if used in workflows)
- ⚠️  `AZURE_WEBAPP_NAME_STAGING` - Web app name (if used in workflows)
- ⚠️  `AZURE_LOCATION` - Azure region (if used in workflows)

---

## 🚨 Troubleshooting

### Issue: Still Getting JSON Error After Update

**Possible causes:**
1. Extra whitespace before/after JSON in GitHub secret
2. Copied from a terminal that added formatting
3. Secret not saved correctly

**Solution:**
1. Delete the secret completely from GitHub
2. Create a new secret (don't update existing)
3. Paste the JSON carefully
4. Verify by re-running the workflow

### Issue: "Insufficient Privileges" Error

**Cause:** Service principal lacks necessary permissions

**Solution:**
```bash
# Grant Contributor role at resource group level
az role assignment create \
  --assignee <client-id-from-credentials> \
  --role "Contributor" \
  --scope /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod
```

### Issue: "Authentication Failed" Error

**Cause:** Service principal credentials may be expired or revoked

**Solution:**
1. Create a new service principal (Step 1 above)
2. Update GitHub secret with new credentials
3. Delete old service principal if no longer needed

---

## 📞 Quick Commands Reference

### Check Current Azure Login
```bash
az account show
```

### List Available Subscriptions
```bash
az account list --output table
```

### Test Service Principal Login
```bash
# Use credentials from the JSON
az login --service-principal \
  --username <clientId> \
  --password <clientSecret> \
  --tenant <tenantId>
```

### Verify Service Principal Permissions
```bash
az role assignment list \
  --assignee <clientId> \
  --output table
```

---

## ✅ Success Criteria

After following this guide, you should see:

1. ✅ GitHub Actions workflow runs without JSON parsing errors
2. ✅ Azure login step shows "Login successful"
3. ✅ Subsequent deployment steps execute normally
4. ✅ Resources are created/updated in Azure

---

## 📚 Additional Resources

- [Azure Login Action Documentation](https://github.com/Azure/login)
- [Azure Service Principal Documentation](https://learn.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)
- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OIDC with Azure Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure)

---

**Important:** After fixing the `AZURE_CREDENTIALS` secret, re-run the failed workflow to verify the fix works correctly.

**L.I.F.E Platform** - Learning Individually from Experience  
**Azure Marketplace Offer ID:** `9a600d96-fe1e-420b-902a-a0c42c561adb`  
**Copyright 2025** - Sergio Paya Borrull
