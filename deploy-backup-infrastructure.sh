#!/bin/bash
# L.I.F.E. Platform - Azure Backup Infrastructure Deployment Script
# Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
# Directory: Sergio Paya Borrull (lifecoach-121.com)

set -e

echo "🚀 Deploying L.I.F.E. Platform Backup Infrastructure to Azure..."
echo "📊 Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca"
echo "👤 Admin: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"
echo "🔒 This will preserve ALL your repository work safely in Azure!"

# Configuration
SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"
RESOURCE_GROUP="life-platform-rg"
LOCATION="eastus2"
DEPLOYMENT_NAME="life-backup-infrastructure-$(date +%Y%m%d-%H%M%S)"

# Authenticate to Azure
echo "🔐 Authenticating to Azure..."
az login --use-device-code

# Set subscription
echo "📊 Setting Azure subscription..."
az account set --subscription $SUBSCRIPTION_ID

# Verify subscription
CURRENT_SUB=$(az account show --query id -o tsv)
if [ "$CURRENT_SUB" != "$SUBSCRIPTION_ID" ]; then
    echo "❌ Wrong subscription selected. Expected: $SUBSCRIPTION_ID, Got: $CURRENT_SUB"
    exit 1
fi

echo "✅ Authenticated to correct subscription"

# Create resource group if it doesn't exist
echo "📁 Ensuring resource group exists..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --tags "project=L.I.F.E. Platform" "purpose=backup" "admin=sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com"

# Preview deployment
echo "🔍 Previewing deployment..."
az deployment group what-if \
    --resource-group $RESOURCE_GROUP \
    --template-file infra/backup-infrastructure.bicep \
    --parameters @infra/backup-infrastructure.parameters.json

# Confirm deployment
echo ""
echo "⚠️  This will create Azure resources for backing up your L.I.F.E. Platform repository."
echo "💰 Estimated cost: ~$10-20/month for storage and functions"
echo "💾 This will SAVE ALL YOUR WORK to Azure permanently!"
read -p "🤔 Continue with deployment? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Deploy infrastructure
    echo "🚀 Deploying backup infrastructure..."
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --name $DEPLOYMENT_NAME \
        --template-file infra/backup-infrastructure.bicep \
        --parameters @infra/backup-infrastructure.parameters.json \
        --verbose

    # Get deployment outputs
    echo "📋 Getting deployment results..."
    STORAGE_ACCOUNT=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.storageAccountName.value -o tsv)
    FUNCTION_APP=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.functionAppName.value -o tsv)
    BACKUP_URL=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.backupContainerUrl.value -o tsv)

    echo ""
    echo "🎉 SUCCESS! L.I.F.E. Platform Backup Infrastructure Deployed!"
    echo "=================================================="
    echo "📊 Subscription: $SUBSCRIPTION_ID"
    echo "📁 Resource Group: $RESOURCE_GROUP"
    echo "💾 Storage Account: $STORAGE_ACCOUNT"
    echo "⚡ Function App: $FUNCTION_APP"
    echo "🔗 Backup URL: $BACKUP_URL"
    echo ""
    echo "🔄 Next Steps:"
    echo "1. Run: python azure_repository_backup_sync.py"
    echo "2. Access backups: Azure Portal → Storage Accounts → $STORAGE_ACCOUNT"
    echo "3. Daily backups will run automatically"
    echo ""
    echo "💡 Your repository is now protected! Even if your computer crashes,"
    echo "   all your work is safely stored in Azure with automatic backups."
    echo ""
    echo "🌐 Access your backups anytime at: https://portal.azure.com"

else
    echo "❌ Deployment cancelled."
    exit 1
fi