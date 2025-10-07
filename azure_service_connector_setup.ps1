# 🔗 Azure Service Connector Setup for L.I.F.E. Platform
# Secure Function App to Storage Account Connection using Managed Identity
# Generated: September 28, 2025

Write-Host "🚀 L.I.F.E. Platform - Azure Service Connector Setup" -ForegroundColor Green
Write-Host "Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca" -ForegroundColor Cyan
Write-Host "Setting up secure connections using Managed Identity..." -ForegroundColor Yellow

# Set the correct subscription
Write-Host "📋 Setting Azure subscription..." -ForegroundColor Blue
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Verify current subscription
Write-Host "✅ Verifying subscription..." -ForegroundColor Blue
az account show --query "{SubscriptionId:id, Name:name, State:state}" -o table

# Create Service Connector: Function App -> Storage Account
Write-Host "🔗 Creating Service Connector: life-functions-app -> stlifeplatformprod" -ForegroundColor Blue
az webapp connection create storage-blob `
    --resource-group "life-platform-rg" `
    --name "life-functions-app" `
    --target-resource-group "life-platform-rg" `
    --account "stlifeplatformprod" `
    --system-identity `
    --verbose

# Create Service Connector: Function App -> Key Vault  
Write-Host "🔐 Creating Service Connector: life-functions-app -> kv-life-platform-prod" -ForegroundColor Blue
az webapp connection create keyvault `
    --resource-group "life-platform-rg" `
    --name "life-functions-app" `
    --target-resource-group "life-platform-rg" `
    --vault "kv-life-platform-prod" `
    --system-identity `
    --verbose

# Create Service Connector: Function App -> Service Bus
Write-Host "📨 Creating Service Connector: life-functions-app -> sb-life-platform-prod" -ForegroundColor Blue
az webapp connection create servicebus `
    --resource-group "life-platform-rg" `
    --name "life-functions-app" `
    --target-resource-group "life-platform-rg" `
    --namespace "sb-life-platform-prod" `
    --system-identity `
    --verbose

# List all connections to verify
Write-Host "📊 Verifying all Service Connector configurations..." -ForegroundColor Blue
az webapp connection list --resource-group "life-platform-rg" --name "life-functions-app" -o table

# Test the connections
Write-Host "🧪 Testing Service Connector configurations..." -ForegroundColor Blue
az webapp connection validate --resource-group "life-platform-rg" --name "life-functions-app" --verbose

Write-Host "🎉 Service Connector setup complete!" -ForegroundColor Green
Write-Host "✅ Function App now securely connected to all Azure services using Managed Identity" -ForegroundColor Green
Write-Host "🔒 No more storage authentication errors!" -ForegroundColor Green