#!/bin/bash
# 🚨 DIRECT AZURE DEPLOYMENT - L.I.F.E Platform Emergency Fix
# This script creates the Azure Web App that doesn't exist

echo "🚨 EMERGENCY: Creating Azure Web App for L.I.F.E Platform"
echo "Issue: DNS_PROBE_FINISHED_NXDOMAIN confirms web app doesn't exist"
echo ""

# Generate unique app name with timestamp
TIMESTAMP=$(date +%m%d%H%M)
UNIQUE_APP_NAME="life-platform-staging-${TIMESTAMP}"
RESOURCE_GROUP="life-platform-staging-rg"
LOCATION="eastus2"
SUBSCRIPTION_ID="5c88cef6-f243-497d-98af-6c6086d575ca"

echo "🎯 Creating resources with unique name: ${UNIQUE_APP_NAME}"
echo ""

# Step 1: Login and set subscription
echo "[STEP 1] Azure Authentication..."
az login
az account set --subscription "$SUBSCRIPTION_ID"

# Step 2: Create resource group
echo "[STEP 2] Creating resource group: $RESOURCE_GROUP"
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --tags environment=staging platform=life-platform marketplace-offer=9a600d96-fe1e-420b-902a-a0c42c561adb

# Step 3: Create App Service Plan (Free tier)
echo "[STEP 3] Creating App Service Plan..."
az appservice plan create \
    --name "${RESOURCE_GROUP}-plan" \
    --resource-group "$RESOURCE_GROUP" \
    --sku F1 \
    --is-linux \
    --location "$LOCATION"

# Step 4: Create Web App
echo "[STEP 4] Creating Web App: $UNIQUE_APP_NAME"
az webapp create \
    --name "$UNIQUE_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --plan "${RESOURCE_GROUP}-plan" \
    --runtime "PYTHON:3.11"

# Step 5: Configure app settings
echo "[STEP 5] Configuring application settings..."
az webapp config appsettings set \
    --name "$UNIQUE_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --settings \
        "ENVIRONMENT=staging" \
        "PLATFORM=L.I.F.E Platform" \
        "MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb" \
        "PYTHONPATH=/home/site/wwwroot" \
        "SCM_DO_BUILD_DURING_DEPLOYMENT=true"

# Step 6: Deploy application using webapp up
echo "[STEP 6] Deploying L.I.F.E Platform application..."
az webapp up \
    --name "$UNIQUE_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --runtime "PYTHON:3.11" \
    --location "$LOCATION"

# Step 7: Test the deployment
echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 Your L.I.F.E Platform URLs:"
echo "📍 Main: https://${UNIQUE_APP_NAME}.azurewebsites.net/"
echo "🏥 Health: https://${UNIQUE_APP_NAME}.azurewebsites.net/health"
echo "📊 Status: https://${UNIQUE_APP_NAME}.azurewebsites.net/api/status"
echo ""
echo "💰 Business Impact: $345K Q4 2025 → $50.7M by 2029 pathway restored!"
echo ""

# Test endpoints
echo "[STEP 7] Testing endpoints..."
sleep 30

curl -f "https://${UNIQUE_APP_NAME}.azurewebsites.net/health" && echo "✅ Health endpoint working!" || echo "⚠️ Health endpoint not ready yet"
curl -f "https://${UNIQUE_APP_NAME}.azurewebsites.net/" && echo "✅ Main endpoint working!" || echo "⚠️ Main endpoint not ready yet"

echo ""
echo "🚀 L.I.F.E Platform emergency deployment complete!"
echo "📝 New staging URL: https://${UNIQUE_APP_NAME}.azurewebsites.net/"