# Azure Credentials Collection Script for L.I.F.E. Platform
# October 11, 2025 - GitHub Actions Setup

Write-Host "🔧 Azure Credentials Setup for L.I.F.E. Platform GitHub Actions" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

# Check if Azure CLI is installed
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✅ Azure CLI installed: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not installed or not in PATH" -ForegroundColor Red
    Write-Host "📥 Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "`n🎯 Required GitHub Repository Variables:" -ForegroundColor Magenta
Write-Host "1. AZURE_CLIENT_ID"
Write-Host "2. AZURE_TENANT_ID" 
Write-Host "3. AZURE_SUBSCRIPTION_ID"
Write-Host "4. AZURE_STATIC_WEB_APPS_API_TOKEN"

Write-Host "`n📋 Your Known Azure Information:" -ForegroundColor Blue
Write-Host "Subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca"
Write-Host "Region: East US 2"
Write-Host "Static Web App: life-platform-webapp"
Write-Host "Platform URL: https://green-ground-0c65efe0f.1.azurestaticapps.net"

Write-Host "`n🔍 Collecting Azure Information..." -ForegroundColor Yellow

try {
    Write-Host "`n--- Azure Account Information ---" -ForegroundColor Cyan
    az account show --output table
    
    Write-Host "`n--- Tenant ID ---" -ForegroundColor Cyan
    $tenantId = az account show --query tenantId -o tsv
    Write-Host "AZURE_TENANT_ID: $tenantId" -ForegroundColor Green
    
    Write-Host "`n--- Subscription ID ---" -ForegroundColor Cyan  
    $subscriptionId = az account show --query id -o tsv
    Write-Host "AZURE_SUBSCRIPTION_ID: $subscriptionId" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Azure CLI commands failed. Please login first:" -ForegroundColor Yellow
    Write-Host "   az login" -ForegroundColor White
}

Write-Host "`n🚀 GitHub Repository Setup Instructions:" -ForegroundColor Magenta
Write-Host "1. Go to: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/variables/actions"
Write-Host "2. Click 'New repository variable'"
Write-Host "3. Add each variable with the values shown above"

Write-Host "`n⚡ Quick GitHub Variable Commands:" -ForegroundColor Blue
if ($tenantId -and $subscriptionId) {
    Write-Host "gh variable set AZURE_TENANT_ID --body '$tenantId'"
    Write-Host "gh variable set AZURE_SUBSCRIPTION_ID --body '$subscriptionId'"
}

Write-Host "`n🎯 For Service Principal Creation:" -ForegroundColor Yellow
Write-Host "az ad sp create-for-rbac --name 'github-actions-life-platform' --role contributor --scopes /subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca --sdk-auth"

Write-Host "`n📅 IMPORTANT: October 15 Demo Status" -ForegroundColor Green
Write-Host "✅ Platform is ALREADY LIVE and working"
Write-Host "✅ Demo shortcuts ready"  
Write-Host "✅ 23 participants can access platform"
Write-Host "⚠️  Credentials only needed for future automated deployments"

Write-Host "`n🏆 Your demo is ready! Set up credentials after the successful presentation." -ForegroundColor Green

Read-Host "`nPress Enter to continue..."