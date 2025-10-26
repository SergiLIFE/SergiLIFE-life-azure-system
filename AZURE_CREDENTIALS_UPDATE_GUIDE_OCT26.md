# 🔐 AZURE CREDENTIALS FOR GITHUB ACTIONS

**Generated:** October 26, 2025  
**Purpose:** Fix GitHub Actions Azure login error  
**Service Principal:** github-actions-life-platform-20251026  

---

## ⚠️ **SECURITY NOTICE**

These are LIVE production credentials. Protect them carefully.

---

## 📋 **STEP-BY-STEP UPDATE GUIDE**

### **Step 1: Copy the Credentials Below**

Copy this ENTIRE JSON block (including the outer curly braces):

```json
{
  "clientId": "0f2c0970-9b39-43b5-916b-1fb9442596c2",
  "clientSecret": "[REDACTED - Set in GitHub Secrets]",
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

### **Step 2: Update GitHub Secret**

1. **Go to GitHub Settings:**
   - URL: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions

2. **Update AZURE_CREDENTIALS Secret:**
   - Click on "AZURE_CREDENTIALS" (or create it if it doesn't exist)
   - Delete the old value completely
   - Paste the ENTIRE JSON from above
   - Click "Update secret" (or "Add secret")

3. **Verify the Secret:**
   - The secret should show as "Updated" with today's date

### **Step 3: Test the Fix**

1. Go to Actions: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
2. Find the failed workflow run
3. Click "Re-run all jobs"
4. Monitor the "🔑 Azure Login" step
5. Should now succeed with "Login successful"

---

## ✅ **ADDITIONAL REQUIRED SECRETS**

Verify these secrets also exist in GitHub:

| Secret Name | Value | Status |
|------------|-------|--------|
| `AZURE_CREDENTIALS` | JSON above | ✅ Update with new JSON |
| `AZURE_SUBSCRIPTION_ID` | `5c88cef6-f243-497d-98af-6c6086d575ca` | ✅ Already known |
| `AZURE_RG_STAGING` | `life-platform-prod` | ⚠️ Verify exists |
| `AZURE_WEBAPP_NAME_STAGING` | `life-functions-app-prod` | ⚠️ Verify exists |
| `AZURE_LOCATION` | `eastus2` | ⚠️ Verify exists |

---

## 🎯 **SERVICE PRINCIPAL DETAILS**

**Name:** github-actions-life-platform-20251026  
**Client ID:** 0f2c0970-9b39-43b5-916b-1fb9442596c2  
**Tenant ID:** e716161a-5e85-4d6d-82f9-96bcdd2e65ac  
**Subscription:** 5c88cef6-f243-497d-98af-6c6086d575ca  
**Role:** Contributor  
**Scope:** /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-prod  

---

## 🔄 **WHAT THIS FIXES**

**Before:** 
```
Error: Login failed with SyntaxError: Unexpected token 'J', 
"JSON from "... is not valid JSON
```

**After:**
```
✅ Login successful
✅ Deployment proceeds normally
```

---

## 🚀 **NEXT STEPS AFTER FIX**

1. ✅ Update `AZURE_CREDENTIALS` secret (instructions above)
2. ✅ Re-run failed GitHub Actions workflow
3. ✅ Verify deployment succeeds
4. ✅ Monitor future workflow runs

---

## 🔒 **SECURITY REMINDERS**

- ✅ These credentials are stored securely in GitHub Secrets
- ✅ They are never exposed in logs or output
- ✅ Service principal has least-privilege access (Contributor on specific resource group only)
- ✅ Credentials can be rotated anytime by generating new ones

---

**After updating the secret, your GitHub Actions deployments will work correctly!**