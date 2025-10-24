# 🔐 Azure Service Principal Creation Script for L.I.F.E Platform
# PowerShell script to create Azure service principal and display GitHub secrets

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$ServicePrincipalName = "sp-life-platform-staging",
    [string]$ResourceGroupName = "life-platform-staging-rg",
    [string]$WebAppName = "life-platform-staging",
    [string]$Location = "eastus2"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 L.I.F.E PLATFORM - Azure Service Principal Setup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Revenue Target: `$345K Q4 2025 → `$50.7M by 2029" -ForegroundColor Green
Write-Host ""

# Check if Azure CLI is installed
Write-Host "[STEP 1] Checking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>$null | Select-String "azure-cli"
    Write-Host "✅ Azure CLI installed: $azVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Login check
Write-Host ""
Write-Host "[STEP 2] Checking Azure login..." -ForegroundColor Yellow
try {
    $currentAccount = az account show --output json 2>$null | ConvertFrom-Json
    if ($currentAccount) {
        Write-Host "✅ Logged in as: $($currentAccount.user.name)" -ForegroundColor Green
        Write-Host "✅ Current subscription: $($currentAccount.name)" -ForegroundColor Green
    } else {
        throw "Not logged in"
    }
} catch {
    Write-Host "⚠️ Not logged in to Azure. Attempting login..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to login to Azure" -ForegroundColor Red
        exit 1
    }
}

# Set subscription
Write-Host ""
Write-Host "[STEP 3] Setting subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionId
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Subscription set to: $SubscriptionId" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to set subscription. Please check subscription ID." -ForegroundColor Red
    exit 1
}

# Create service principal
Write-Host ""
Write-Host "[STEP 4] Creating service principal..." -ForegroundColor Yellow
Write-Host "Name: $ServicePrincipalName" -ForegroundColor Cyan
Write-Host "Role: Contributor" -ForegroundColor Cyan
Write-Host "Scope: /subscriptions/$SubscriptionId" -ForegroundColor Cyan

$servicePrincipal = az ad sp create-for-rbac `
    --name $ServicePrincipalName `
    --role "Contributor" `
    --scopes "/subscriptions/$SubscriptionId" `
    --sdk-auth 2>$null

if ($LASTEXITCODE -eq 0 -and $servicePrincipal) {
    Write-Host "✅ Service principal created successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create service principal" -ForegroundColor Red
    Write-Host "This might be because a service principal with this name already exists." -ForegroundColor Yellow
    Write-Host "Try using a different name or delete the existing one." -ForegroundColor Yellow
    exit 1
}

# Parse JSON response
$spJson = $servicePrincipal | ConvertFrom-Json

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔑 GITHUB REPOSITORY SECRETS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Add these 5 secrets to your GitHub repository:" -ForegroundColor Green
Write-Host "📍 URL: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""

# Display secrets in a formatted table
Write-Host "SECRET NAME                   | SECRET VALUE" -ForegroundColor Yellow
Write-Host "---------------------------------------------------" -ForegroundColor Yellow
Write-Host "AZURE_CREDENTIALS            | (JSON below)" -ForegroundColor White
Write-Host "AZURE_SUBSCRIPTION_ID        | $SubscriptionId" -ForegroundColor White
Write-Host "AZURE_RG_STAGING             | $ResourceGroupName" -ForegroundColor White  
Write-Host "AZURE_WEBAPP_NAME_STAGING    | $WebAppName" -ForegroundColor White
Write-Host "AZURE_LOCATION               | $Location" -ForegroundColor White
Write-Host ""

# Display the full JSON for AZURE_CREDENTIALS
Write-Host "📋 AZURE_CREDENTIALS JSON (copy entire content):" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host $servicePrincipal -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Save to file for easy copying
$outputFile = "azure_credentials_for_github.json"
$servicePrincipal | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "💾 Credentials saved to: $outputFile" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 NEXT STEPS" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 🔐 Copy the JSON above and add as AZURE_CREDENTIALS secret" -ForegroundColor White
Write-Host "2. 🔑 Add the other 4 secrets to GitHub repository settings" -ForegroundColor White
Write-Host "3. 📤 Push your code changes to GitHub: git push origin main" -ForegroundColor White
Write-Host "4. 👀 Monitor deployment: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions" -ForegroundColor White
Write-Host "5. 🏥 Test staging: https://life-platform-staging.azurewebsites.net/health" -ForegroundColor White
Write-Host ""
Write-Host "🎯 L.I.F.E Platform ready for `$345K Q4 2025 revenue target!" -ForegroundColor Green
Write-Host ""

# Offer to open GitHub in browser
$openGitHub = Read-Host "Open GitHub repository secrets page in browser? (y/n)"
if ($openGitHub -eq "y" -or $openGitHub -eq "Y") {
    Start-Process "https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions"
}

Write-Host "✅ Service principal setup complete!" -ForegroundColor Green