# GitHub Actions Secrets Setup Guide

This document provides instructions for configuring the required secrets for the L.I.F.E. Platform GitHub Actions workflows.

## Required Secrets

### Azure Static Web Apps

The following secret is required for Azure Static Web Apps deployment:

- **`AZURE_STATIC_WEB_APPS_API_TOKEN_GREEN_GROUND_0C65EFE0F`**
  - Purpose: Authenticates deployments to Azure Static Web Apps
  - How to obtain: 
    1. Go to your Azure Static Web App resource in the Azure Portal
    2. Navigate to "Deployment tokens" or "Manage deployment token"
    3. Copy the deployment token
  - Add to repository: Settings → Secrets and variables → Actions → New repository secret

### Azure Deployment (OIDC-based - Recommended)

For OIDC-based authentication (no secrets required):

- **`AZURE_CLIENT_ID`** (Repository Variable)
- **`AZURE_TENANT_ID`** (Repository Variable)
- **`AZURE_SUBSCRIPTION_ID`** (Repository Variable)

These should be configured as repository **variables** (not secrets) in:
Settings → Secrets and variables → Actions → Variables tab

### Azure Deployment (Service Principal - Alternative)

If not using OIDC, you can use service principal credentials:

- **`AZURE_CREDENTIALS`** (JSON format)
  ```json
  {
    "clientId": "YOUR_CLIENT_ID",
    "clientSecret": "YOUR_CLIENT_SECRET",
    "subscriptionId": "YOUR_SUBSCRIPTION_ID",
    "tenantId": "YOUR_TENANT_ID"
  }
  ```

  **Important:** 
  - The JSON must be valid and properly formatted (no extra whitespace, line breaks, or special characters)
  - Use a JSON validator before adding the secret (e.g., https://jsonlint.com/)
  - Do not include any comments or additional text with the JSON
  - Copy the JSON exactly as shown, replacing only the placeholder values
  - The workflow will automatically validate the JSON structure before attempting login

Or individual secrets:
- **`AZURE_CLIENT_ID`**
- **`AZURE_CLIENT_SECRET`**
- **`AZURE_SUBSCRIPTION_ID`**
- **`AZURE_TENANT_ID`**

### Additional Secrets (for full deployment)

- **`AZURE_RG_STAGING`** - Resource group name for staging environment
- **`AZURE_RG_PRODUCTION`** - Resource group name for production environment
- **`AZURE_LOCATION`** - Azure region (e.g., "eastus2")
- **`AZURE_WEBAPP_NAME_STAGING`** - App Service name for staging
- **`AZURE_WEBAPP_NAME_PRODUCTION`** - App Service name for production

## Workflow Behavior with Missing Secrets

### Graceful Handling

The workflows are configured to handle missing secrets gracefully:

1. **Azure Static Web Apps workflow**: Uses `skip_deploy_on_missing_secrets: true` to allow the workflow to complete even if the secret is missing.

2. **Test workflows**: Continue even if linting finds issues, using `|| echo "⚠️ Warning"` patterns.

3. **Azure deployment workflow**: Checks for credentials before attempting deployment and provides clear error messages.

## Testing Workflows Locally

To test workflows locally without secrets:

1. The test and lint workflows will run successfully without any secrets
2. Deployment steps will be skipped if secrets are not configured
3. Check workflow run logs for clear indicators of which secrets are missing

## Setting Up OIDC Authentication

For the most secure approach, set up OIDC authentication:

1. Run the `setup-azure-oidc.ps1` script in the repository
2. Follow the instructions to create a federated identity credential in Azure
3. Configure the three repository variables (CLIENT_ID, TENANT_ID, SUBSCRIPTION_ID)

See `AZURE_OIDC_SETUP.md` for detailed instructions.

## Troubleshooting

### Workflow fails with "secret not found"

- Check that the secret name matches exactly (case-sensitive)
- Verify the secret is set in the correct repository
- Ensure secrets are not accidentally set as variables (or vice versa)

### Azure Login fails with "JSON is not valid JSON"

This error occurs when the `AZURE_CREDENTIALS` secret contains malformed JSON:

**Common causes:**
- Extra whitespace or line breaks in the JSON
- Missing quotes around values
- Incorrectly escaped characters
- Additional text before or after the JSON
- Unicode or special characters in the secret values

**Solution:**
1. Validate your JSON using an online validator (https://jsonlint.com/)
2. Ensure the JSON is on a single line or properly formatted
3. Copy the exact format from the example above
4. Remove any trailing whitespace or newlines
5. The workflow now includes automatic validation that will provide specific error messages

**Example of correct format:**
```json
{"clientId":"abc123","clientSecret":"xyz789","subscriptionId":"sub123","tenantId":"tenant123"}
```

**Example of incorrect format:**
```
JSON from Azure: {"clientId":"abc123"...  (Contains extra text)
{
  "clientId": "abc123",    (Extra whitespace/formatting may cause issues)
}
```

### Deployment steps are skipped

- This is expected if optional secrets are not configured
- Check the workflow logs for messages indicating which secrets are required
- Set the required secrets to enable deployment steps

### Clear GitHub Actions Cache

If you need to clear cached workflow results (e.g., Flake8 results):

1. Go to repository Settings → Actions → Caches
2. Delete specific caches or all caches
3. Re-run the workflow

## Support

For issues specific to the L.I.F.E. Platform:
- Email: info@lifecoach121.com
- Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
- Documentation: See README.md and other markdown files in the repository

---

**Copyright 2025 - Sergio Paya Borrull**  
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
