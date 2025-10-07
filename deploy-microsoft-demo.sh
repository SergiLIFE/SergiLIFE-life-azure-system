#!/bin/bash
# Microsoft Partnership Demo Deployment Script
# Date: September 30, 2025
# L.I.F.E. Theory Platform - Azure Demo Infrastructure

echo "🚀 Starting Microsoft Partnership Demo Deployment..."
echo "📅 Date: $(date)"
echo "🆔 Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca"
echo ""

# Set subscription
echo "🔧 Setting Azure subscription..."
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

# Create resource group
echo "📦 Creating resource group rg-microsoft-demo-env..."
az group create --name rg-microsoft-demo-env --location eastus2

# Deploy infrastructure
echo "🏗️  Deploying L.I.F.E. Theory Platform infrastructure..."
az deployment group create \
  --resource-group rg-microsoft-demo-env \
  --template-file microsoft-demo.bicep \
  --parameters @microsoft-demo.parameters.json \
  --name microsoft-demo-deployment \
  --verbose

# Check deployment status
echo ""
echo "✅ Deployment completed! Getting outputs..."
az deployment group show \
  --resource-group rg-microsoft-demo-env \
  --name microsoft-demo-deployment \
  --query "properties.outputs"

echo ""
echo "🌐 Your Container App URL:"
az deployment group show \
  --resource-group rg-microsoft-demo-env \
  --name microsoft-demo-deployment \
  --query "properties.outputs.containerAppUrl.value" \
  --output tsv

echo ""
echo "⚡ Your Function App URL:"
az deployment group show \
  --resource-group rg-microsoft-demo-env \
  --name microsoft-demo-deployment \
  --query "properties.outputs.functionAppUrl.value" \
  --output tsv

echo ""
echo "🎉 Microsoft Partnership Demo deployment complete!"
echo "🚀 Ready for executive outreach to:"
echo "   • Satya Nadella (Microsoft CEO)"
echo "   • Scott Guthrie (Executive VP, Cloud + AI)"
echo "   • Sam Altman (OpenAI CEO)"
echo "   • Kevin Scott (Microsoft CTO)"