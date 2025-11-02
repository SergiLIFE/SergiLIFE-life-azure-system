#!/bin/bash
# Azure Credentials Quick Fix Script
# Generates properly formatted Azure service principal credentials for GitHub Actions
# L.I.F.E Platform - November 2, 2025

set -e

echo "=============================================================================="
echo "Azure Credentials Quick Fix - L.I.F.E Platform"
echo "=============================================================================="
echo ""

# L.I.F.E Platform configuration
SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
TENANT_ID="e716161a-5e85-4d6d-82f9-96bcdd2e65ac"
RESOURCE_GROUP="life-platform-prod"
TIMESTAMP=$(date +%Y%m%d%H%M)
SP_NAME="github-actions-life-platform-${TIMESTAMP}"

echo "Configuration:"
echo "  Subscription: $SUBSCRIPTION_ID"
echo "  Tenant: $TENANT_ID"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Service Principal: $SP_NAME"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found!"
    echo ""
    echo "Please install Azure CLI:"
    echo "  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    echo ""
    exit 1
fi

echo "✅ Azure CLI found: $(az version --query '\"azure-cli\"' -o tsv)"
echo ""

# Check if logged in
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure"
    echo ""
    echo "Please login first:"
    echo "  az login --tenant $TENANT_ID"
    echo ""
    exit 1
fi

CURRENT_SUBSCRIPTION=$(az account show --query id -o tsv)
echo "✅ Logged in to Azure"
echo "  Current subscription: $CURRENT_SUBSCRIPTION"
echo ""

# Set the correct subscription
if [ "$CURRENT_SUBSCRIPTION" != "$SUBSCRIPTION_ID" ]; then
    echo "Switching to L.I.F.E Platform subscription..."
    az account set --subscription "$SUBSCRIPTION_ID"
    echo "✅ Subscription set to $SUBSCRIPTION_ID"
    echo ""
fi

# Verify resource group exists
echo "Verifying resource group exists..."
if ! az group show --name "$RESOURCE_GROUP" &> /dev/null; then
    echo "⚠️  Resource group '$RESOURCE_GROUP' not found"
    echo ""
    echo "Available resource groups:"
    az group list --query "[].name" -o table
    echo ""
    read -p "Enter the resource group name to use: " RESOURCE_GROUP
fi

echo "✅ Resource group '$RESOURCE_GROUP' found"
echo ""

# Generate credentials
echo "=============================================================================="
echo "Generating Azure Service Principal Credentials"
echo "=============================================================================="
echo ""
echo "Creating service principal: $SP_NAME"
echo ""

SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"

# Create service principal with --sdk-auth format
echo "Running: az ad sp create-for-rbac --name '$SP_NAME' --role contributor --scopes '$SCOPE' --sdk-auth"
echo ""

CREDENTIALS=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "$SCOPE" \
    --sdk-auth 2>&1)

# Check if command succeeded
if [ $? -ne 0 ]; then
    echo "❌ Failed to create service principal"
    echo ""
    echo "Error output:"
    echo "$CREDENTIALS"
    echo ""
    exit 1
fi

# Extract just the JSON (filter out deprecation warning)
CREDENTIALS_JSON=$(echo "$CREDENTIALS" | grep -A 100 '^{' | grep -B 100 '^}' | head -n 20)

echo "✅ Service principal created successfully!"
echo ""

# Validate the JSON
echo "=============================================================================="
echo "Validating Credentials Format"
echo "=============================================================================="
echo ""

# Check if jq is available for validation
if command -v jq &> /dev/null; then
    echo "$CREDENTIALS_JSON" | jq . > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ JSON format is valid"
    else
        echo "❌ JSON format is invalid"
        exit 1
    fi
else
    echo "⚠️  jq not installed, skipping JSON validation"
fi

echo ""

# Display credentials
echo "=============================================================================="
echo "Azure Credentials (Copy the entire JSON below)"
echo "=============================================================================="
echo ""
echo "$CREDENTIALS_JSON"
echo ""

# Save to file
CREDS_FILE="/tmp/azure_credentials_${TIMESTAMP}.json"
echo "$CREDENTIALS_JSON" > "$CREDS_FILE"

echo "=============================================================================="
echo "Credentials saved to: $CREDS_FILE"
echo "=============================================================================="
echo ""

# Extract key values for display
CLIENT_ID=$(echo "$CREDENTIALS_JSON" | grep -o '"clientId": "[^"]*"' | cut -d'"' -f4)
SUBSCRIPTION_ID_FROM_JSON=$(echo "$CREDENTIALS_JSON" | grep -o '"subscriptionId": "[^"]*"' | cut -d'"' -f4)
TENANT_ID_FROM_JSON=$(echo "$CREDENTIALS_JSON" | grep -o '"tenantId": "[^"]*"' | cut -d'"' -f4)

echo "Service Principal Details:"
echo "  Name: $SP_NAME"
echo "  Client ID: $CLIENT_ID"
echo "  Tenant ID: $TENANT_ID_FROM_JSON"
echo "  Subscription ID: $SUBSCRIPTION_ID_FROM_JSON"
echo "  Role: Contributor"
echo "  Scope: $SCOPE"
echo ""

# Instructions
echo "=============================================================================="
echo "Next Steps"
echo "=============================================================================="
echo ""
echo "1. Copy the JSON credentials above (or from $CREDS_FILE)"
echo ""
echo "2. Go to GitHub Secrets:"
echo "   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions"
echo ""
echo "3. Create or update the 'AZURE_CREDENTIALS' secret:"
echo "   - Click 'New repository secret' or click on existing 'AZURE_CREDENTIALS'"
echo "   - Paste the ENTIRE JSON (nothing before or after)"
echo "   - Click 'Add secret' or 'Update secret'"
echo ""
echo "4. Re-run your failed GitHub Actions workflow:"
echo "   https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions"
echo ""
echo "5. Monitor the Azure Login step - it should now succeed!"
echo ""

# Optional: Test the credentials
echo "Would you like to test these credentials? (y/n)"
read -r RESPONSE
if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Testing service principal login..."
    
    CLIENT_SECRET=$(echo "$CREDENTIALS_JSON" | grep -o '"clientSecret": "[^"]*"' | cut -d'"' -f4)
    
    az login --service-principal \
        --username "$CLIENT_ID" \
        --password "$CLIENT_SECRET" \
        --tenant "$TENANT_ID_FROM_JSON" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Service principal login successful!"
        echo ""
        echo "Verifying permissions..."
        az group show --name "$RESOURCE_GROUP" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Service principal can access resource group '$RESOURCE_GROUP'"
        else
            echo "⚠️  Service principal cannot access resource group '$RESOURCE_GROUP'"
            echo "   You may need to wait a few seconds for permissions to propagate"
        fi
    else
        echo "❌ Service principal login failed"
        echo "   This might be a temporary issue. Try the GitHub Actions workflow anyway."
    fi
    
    # Logout to restore original session
    az logout > /dev/null 2>&1
    az login --tenant "$TENANT_ID" > /dev/null 2>&1
fi

echo ""
echo "=============================================================================="
echo "✅ Quick Fix Complete!"
echo "=============================================================================="
echo ""
echo "Remember to securely delete the credentials file when done:"
echo "  rm $CREDS_FILE"
echo ""
