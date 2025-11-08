#!/bin/bash
# L.I.F.E. Platform - Microsoft Partnership Infrastructure Deployment
# Execute this in Azure Cloud Shell
# Date: November 7, 2025

echo "🚀 L.I.F.E. Platform Microsoft Partnership Deployment"
echo "=================================================="
echo ""
echo "📋 Deployment Details:"
echo "  - Subscription: Microsoft Azure Sponsorship"
echo "  - Subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca"
echo "  - Resource Group: rg-life-microsoft-demo"
echo "  - Location: East US 2"
echo "  - Resources: 11 Azure services"
echo ""

# Set subscription
echo "🔐 Setting Azure subscription..."
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

if [ $? -eq 0 ]; then
    echo "✅ Subscription set successfully"
else
    echo "❌ Failed to set subscription"
    exit 1
fi

# Verify current subscription
echo ""
echo "📊 Current subscription:"
az account show --output table
echo ""

# Create resource group
echo "📦 Creating resource group..."
az group create \
    --name rg-life-microsoft-demo \
    --location eastus2 \
    --tags \
        Environment=demo \
        Project="L.I.F.E. Platform" \
        Partnership="Microsoft Demo" \
        Owner="SergiLIFE"

if [ $? -eq 0 ]; then
    echo "✅ Resource group created successfully"
else
    echo "⚠️  Resource group may already exist (continuing...)"
fi

# Verify files exist
echo ""
echo "📁 Verifying deployment files..."
if [ ! -f "microsoft-partnership-clean.bicep" ]; then
    echo "❌ ERROR: microsoft-partnership-clean.bicep not found!"
    echo "   Please upload the file using Cloud Shell upload button"
    exit 1
fi

if [ ! -f "microsoft-partnership-clean.parameters.json" ]; then
    echo "❌ ERROR: microsoft-partnership-clean.parameters.json not found!"
    echo "   Please upload the file using Cloud Shell upload button"
    exit 1
fi

echo "✅ All deployment files found"
echo ""

# Show file contents summary
echo "📄 Bicep template summary:"
head -20 microsoft-partnership-clean.bicep
echo ""

# Deploy infrastructure
echo "🏗️  Starting infrastructure deployment..."
echo "⏱️  This will take approximately 10-15 minutes"
echo ""

az deployment group create \
    --resource-group rg-life-microsoft-demo \
    --template-file microsoft-partnership-clean.bicep \
    --parameters @microsoft-partnership-clean.parameters.json \
    --verbose

DEPLOYMENT_STATUS=$?

echo ""
echo "=================================================="

if [ $DEPLOYMENT_STATUS -eq 0 ]; then
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "🎉 Microsoft Partnership Infrastructure Ready!"
    echo ""
    echo "📦 Resources Deployed:"
    echo "  ✅ Managed Identity (credential-free access)"
    echo "  ✅ Key Vault (secrets management)"
    echo "  ✅ Log Analytics + Application Insights (monitoring)"
    echo "  ✅ Container Registry (Docker images)"
    echo "  ✅ Storage Account (demo data)"
    echo "  ✅ Container Apps Environment + App (L.I.F.E. Platform)"
    echo "  ✅ Function App (executive API)"
    echo "  ✅ Cosmos DB (serverless NoSQL)"
    echo "  ✅ Event Hub (EEG streaming)"
    echo ""
    echo "🔗 Quick Links:"
    echo "  Resource Group:"
    echo "  https://portal.azure.com/#@e716161a-5e85-4d6d-82f9-96bcdd2e65ac/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/rg-life-microsoft-demo"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Add secrets to Key Vault (EEG-API-KEY, OPENAI-API-KEY)"
    echo "  2. Upload L.I.F.E. Platform Docker image to Container Registry"
    echo "  3. Configure Container App environment variables"
    echo "  4. Deploy Function App code"
    echo "  5. Test API endpoints"
    echo ""
    echo "💰 Estimated Monthly Cost: ~\$25 (from Azure Sponsorship)"
    echo ""
else
    echo "❌ DEPLOYMENT FAILED!"
    echo ""
    echo "🔍 Troubleshooting:"
    echo "  1. Check deployment errors above"
    echo "  2. Verify subscription has sufficient quotas"
    echo "  3. Check Azure Portal Activity Log"
    echo "  4. Review Bicep template syntax"
    echo ""
    echo "📞 Support:"
    echo "  - Azure Portal: https://portal.azure.com"
    echo "  - Documentation: infra/ONE_CLICK_DEPLOY.md"
    exit 1
fi

# List deployed resources
echo "📊 Deployed Resources:"
az resource list \
    --resource-group rg-life-microsoft-demo \
    --output table

echo ""
echo "🎯 Deployment Complete - Ready for Microsoft Partnership Demo!"
