# 🔧 GitHub Actions Azure Login Fix - October 26, 2025

**Issue:** Azure login failing with JSON parsing error  
**Error:** `SyntaxError: Unexpected token 'J', "JSON from "... is not valid JSON`  
**Workflow:** `azure-deploy.yml` - Deploy to Staging job  

---

## 🔍 **ROOT CAUSE**

The `AZURE_CREDENTIALS` GitHub secret contains invalid JSON format. The Azure login action expects a properly formatted service principal credential JSON.

---

## ✅ **SOLUTION**

### **Step 1: Generate Correct Azure Credentials**

Run this command in Azure CLI to create properly formatted credentials:

```bash
az ad sp create-for-rbac \
  --name "github-actions-life-platform" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod \
  --sdk-auth
```

**Expected Output (Copy the entire JSON):**
```json
{
  "clientId": "<GUID>",
  "clientSecret": "<SECRET>",
  "subscriptionId": "5c88cef6-f243-497d-98af-6c6086d575ca",
  "tenantId": "<TENANT_GUID>",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### **Step 2: Update GitHub Secret**

1. Go to: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
2. Click on `AZURE_CREDENTIALS` secret
3. Delete the existing value
4. Paste the ENTIRE JSON output from Step 1 (including the curly braces)
5. Click "Update secret"

### **Step 3: Verify Other Required Secrets**

Make sure these secrets exist with correct values:

```yaml
AZURE_SUBSCRIPTION_ID: "5c88cef6-f243-497d-98af-6c6086d575ca"
AZURE_RG_STAGING: "life-platform-staging" 
AZURE_WEBAPP_NAME_STAGING: "life-platform-app-staging"
AZURE_LOCATION: "eastus2"
```

---

## 🔧 **ALTERNATIVE FIX: Use OIDC (Recommended)**

For better security, switch to OpenID Connect (OIDC) authentication:

### **Update Workflow to Use OIDC:**

```yaml
- name: 🔑 Azure Login
  uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### **Required Secrets for OIDC:**
- `AZURE_CLIENT_ID`: Service principal client ID
- `AZURE_TENANT_ID`: Your Azure AD tenant ID  
- `AZURE_SUBSCRIPTION_ID`: Your subscription ID

---

## 📋 **QUICK FIX COMMANDS**

### **Generate New Credentials:**
```bash
# Login to Azure
az login

# Create service principal with proper JSON output
az ad sp create-for-rbac \
  --name "github-actions-life-platform-$(date +%Y%m%d)" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca \
  --sdk-auth > azure_credentials.json

# Display the credentials
cat azure_credentials.json
```

### **Copy the output and update GitHub secret**

---

## ✅ **VERIFICATION STEPS**

After updating the secret:

1. Go to GitHub Actions: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
2. Click "Re-run all jobs" on the failed workflow
3. Monitor the "🔑 Azure Login" step
4. Should see: "Login successful"

---

## 🚨 **COMMON ISSUES**

### **Issue 1: Extra characters in secret**
- **Symptom:** "Unexpected token" error
- **Fix:** Ensure ONLY the JSON is copied (no extra spaces, quotes, or text)

### **Issue 2: Missing permissions**
- **Symptom:** "Insufficient privileges" error  
- **Fix:** Ensure service principal has "Contributor" role

### **Issue 3: Expired credentials**
- **Symptom:** "Authentication failed" error
- **Fix:** Regenerate service principal credentials

---

## 📝 **IMMEDIATE ACTION REQUIRED**

Run this command now to generate correct credentials:

```bash
az ad sp create-for-rbac \
  --name "github-actions-life-platform" \
  --role contributor \
  --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod \
  --sdk-auth
```

Then update the `AZURE_CREDENTIALS` secret in GitHub with the complete JSON output.