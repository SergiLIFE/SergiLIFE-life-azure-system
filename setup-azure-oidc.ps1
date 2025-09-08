# Azure OIDC Setup Script for GitHub Actions
# Run this script in PowerShell with Azure CLI installed

param(
    [Parameter(Mandatory = $false)]
    [string]$AppName = "GitHub-SergiLIFE-life-azure-system",
    
    [Parameter(Mandatory = $false)]
    [string]$RepoOwner = "SergiLIFE",
    
    [Parameter(Mandatory = $false)]
    [string]$RepoName = "SergiLIFE-life-azure-system"
)

Write-Host "🚀 Setting up Azure OIDC authentication for GitHub Actions..." -ForegroundColor Green

# Check if user is logged in to Azure
Write-Host "📋 Checking Azure login status..." -ForegroundColor Yellow
try {
    $account = az account show --query "user.name" -o tsv 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Please login to Azure first: az login" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Logged in as: $account" -ForegroundColor Green
}
catch {
    Write-Host "❌ Please install Azure CLI and login: az login" -ForegroundColor Red
    exit 1
}

# Get current subscription info
$subscriptionId = az account show --query "id" -o tsv
$tenantId = az account show --query "tenantId" -o tsv
$subscriptionName = az account show --query "name" -o tsv

Write-Host "📋 Current Azure context:" -ForegroundColor Yellow
Write-Host "  Subscription: $subscriptionName ($subscriptionId)" -ForegroundColor Cyan
Write-Host "  Tenant: $tenantId" -ForegroundColor Cyan

# Create Azure AD application
Write-Host "🔧 Creating Azure AD application: $AppName..." -ForegroundColor Yellow
$appOutput = az ad app create --display-name $AppName --sign-in-audience "AzureADMyOrg" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  App might already exist, trying to get existing app..." -ForegroundColor Yellow
    $appOutput = az ad app list --display-name $AppName --query "[0]" 2>$null
}

$appId = ($appOutput | ConvertFrom-Json).appId
Write-Host "✅ Application ID (Client ID): $appId" -ForegroundColor Green

# Create service principal
Write-Host "🔧 Creating service principal..." -ForegroundColor Yellow
$spOutput = az ad sp create --id $appId 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Service principal might already exist" -ForegroundColor Yellow
}

# Assign Contributor role
Write-Host "🔧 Assigning Contributor role to service principal..." -ForegroundColor Yellow
$roleAssignment = az role assignment create --assignee $appId --role "Contributor" --scope "/subscriptions/$subscriptionId" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Role assignment might already exist" -ForegroundColor Yellow
}

# Create federated credentials
Write-Host "🔧 Creating federated credentials for GitHub..." -ForegroundColor Yellow

# Main branch credential
$mainCredential = @{
    name        = "github-main"
    issuer      = "https://token.actions.githubusercontent.com"
    subject     = "repo:$RepoOwner/${RepoName}:ref:refs/heads/main"
    description = "GitHub Actions for main branch"
    audiences   = @("api://AzureADTokenExchange")
} | ConvertTo-Json -Depth 3

$tempFile1 = [System.IO.Path]::GetTempFileName()
$mainCredential | Out-File -FilePath $tempFile1 -Encoding utf8

az ad app federated-credential create --id $appId --parameters $tempFile1 2>$null
Remove-Item $tempFile1

# Pull request credential
$prCredential = @{
    name        = "github-pr"
    issuer      = "https://token.actions.githubusercontent.com"
    subject     = "repo:$RepoOwner/${RepoName}:pull_request"
    description = "GitHub Actions for pull requests"
    audiences   = @("api://AzureADTokenExchange")
} | ConvertTo-Json -Depth 3

$tempFile2 = [System.IO.Path]::GetTempFileName()
$prCredential | Out-File -FilePath $tempFile2 -Encoding utf8

az ad app federated-credential create --id $appId --parameters $tempFile2 2>$null
Remove-Item $tempFile2

Write-Host "✅ Federated credentials created successfully!" -ForegroundColor Green

# Output summary
Write-Host "`n🎉 Setup completed! Please add these variables to your GitHub repository:" -ForegroundColor Green
Write-Host "   Go to: https://github.com/$RepoOwner/$RepoName/settings/variables/actions" -ForegroundColor Cyan
Write-Host "`n📋 Repository Variables to add:" -ForegroundColor Yellow
Write-Host "   AZURE_CLIENT_ID: $appId" -ForegroundColor White
Write-Host "   AZURE_TENANT_ID: $tenantId" -ForegroundColor White
Write-Host "   AZURE_SUBSCRIPTION_ID: $subscriptionId" -ForegroundColor White

Write-Host "`n🔗 Useful links:" -ForegroundColor Yellow
Write-Host "   GitHub Variables: https://github.com/$RepoOwner/$RepoName/settings/variables/actions" -ForegroundColor Cyan
Write-Host "   GitHub Actions: https://github.com/$RepoOwner/$RepoName/actions" -ForegroundColor Cyan
Write-Host "   Azure Portal: https://portal.azure.com" -ForegroundColor Cyan

Write-Host "`n✅ Your GitHub Actions workflow is now ready to use OIDC authentication!" -ForegroundColor Green
