#!/bin/bash
# Microsoft Partnership Demo - Bicep Validation Script
# Validates the infrastructure template before deployment

set -e

# Configuration
RESOURCE_GROUP_NAME="rg-life-microsoft-demo"
LOCATION="eastus2"
TEMPLATE_FILE="infra/microsoft-partnership-clean.bicep"
PARAMETERS_FILE="infra/microsoft-partnership-clean.parameters.json"
SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"

echo "🔍 Microsoft Partnership Demo - Bicep Validation"
echo "================================================"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Login check
echo "🔐 Checking Azure CLI authentication..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure CLI. Please run 'az login' first."
    exit 1
fi

# Set subscription
echo "📋 Setting subscription: $SUBSCRIPTION_ID"
az account set --subscription "$SUBSCRIPTION_ID"

# Validate the current subscription
CURRENT_SUB=$(az account show --query id -o tsv)
if [ "$CURRENT_SUB" != "$SUBSCRIPTION_ID" ]; then
    echo "❌ Failed to set subscription. Current: $CURRENT_SUB, Expected: $SUBSCRIPTION_ID"
    exit 1
fi

echo "✅ Subscription set successfully"

# Create resource group if it doesn't exist
echo "🏗️  Checking resource group: $RESOURCE_GROUP_NAME"
if ! az group show --name "$RESOURCE_GROUP_NAME" &> /dev/null; then
    echo "📦 Creating resource group..."
    az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION" --tags Environment=microsoft-demo Project=L.I.F.E-Platform Partnership=Microsoft-Demo
    echo "✅ Resource group created successfully"
else
    echo "✅ Resource group already exists"
fi

# Validate Bicep template syntax
echo "🧪 Validating Bicep template syntax..."
if ! az bicep build --file "$TEMPLATE_FILE" --stdout > /dev/null; then
    echo "❌ Bicep template syntax validation failed"
    exit 1
fi
echo "✅ Bicep template syntax is valid"

# Validate template with parameters
echo "🔬 Validating template deployment..."
VALIDATION_RESULT=$(az deployment group validate \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file "$TEMPLATE_FILE" \
    --parameters "@$PARAMETERS_FILE" \
    --query "error" -o tsv 2>/dev/null || echo "validation-failed")

if [ "$VALIDATION_RESULT" != "None" ] && [ "$VALIDATION_RESULT" != "" ]; then
    echo "❌ Template validation failed:"
    az deployment group validate \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --template-file "$TEMPLATE_FILE" \
        --parameters "@$PARAMETERS_FILE"
    exit 1
fi

echo "✅ Template validation successful"

# What-if deployment preview
echo "👀 Generating deployment preview (what-if)..."
az deployment group what-if \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file "$TEMPLATE_FILE" \
    --parameters "@$PARAMETERS_FILE" \
    --result-format FullResourcePayloads

echo ""
echo "🎉 Validation Complete!"
echo "========================"
echo "✅ Azure CLI authenticated"
echo "✅ Subscription configured: $SUBSCRIPTION_ID"
echo "✅ Resource group ready: $RESOURCE_GROUP_NAME"
echo "✅ Bicep template syntax valid"
echo "✅ Template parameters valid"
echo "✅ Deployment preview generated"
echo ""
echo "🚀 Ready for deployment! Run the following command to deploy:"
echo "az deployment group create \\"
echo "    --resource-group \"$RESOURCE_GROUP_NAME\" \\"
echo "    --template-file \"$TEMPLATE_FILE\" \\"
echo "    --parameters \"@$PARAMETERS_FILE\""
echo ""
echo "💡 Or use the Azure Portal deployment option with the generated template."