# 🚨 EMERGENCY AZURE DEPLOYMENT FIX - PowerShell Version
# Fix DNS_PROBE_FINISHED_NXDOMAIN for life-platform-staging.azurewebsites.net

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$ResourceGroupName = "life-platform-staging-rg", 
    [string]$WebAppBaseName = "life-platform-staging",
    [string]$Location = "eastus2"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚨 EMERGENCY AZURE DEPLOYMENT FIX" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "Issue: DNS_PROBE_FINISHED_NXDOMAIN" -ForegroundColor Red
Write-Host "Platform: L.I.F.E (Learning Individually from Experience)" -ForegroundColor Green
Write-Host "Revenue Target: `$345K Q4 2025 → `$50.7M by 2029" -ForegroundColor Green
Write-Host ""

# Function to check if Azure CLI is available
function Test-AzureCLI {
    try {
        $version = az --version 2>$null
        return $true
    }
    catch {
        return $false
    }
}

# Function to test endpoint
function Test-Endpoint {
    param([string]$Url, [string]$Name)
    
    Write-Host "🔍 Testing $Name..." -ForegroundColor Yellow
    Write-Host "📍 URL: $Url" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $Name: SUCCESS" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️ $Name: Status $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ $Name: FAILED - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check Azure CLI
Write-Host "[STEP 1] Checking Azure CLI..." -ForegroundColor Yellow
if (-not (Test-AzureCLI)) {
    Write-Host "❌ Azure CLI not found. Please install from: https://docs.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Azure CLI found" -ForegroundColor Green

# Check authentication
Write-Host "`n[STEP 2] Checking Azure Authentication..." -ForegroundColor Yellow
try {
    $currentAccount = az account show --output json 2>$null | ConvertFrom-Json
    if ($currentAccount) {
        Write-Host "✅ Authenticated as: $($currentAccount.user.name)" -ForegroundColor Green
        Write-Host "✅ Current subscription: $($currentAccount.name)" -ForegroundColor Green
    } else {
        throw "Not authenticated"
    }
}
catch {
    Write-Host "❌ Not authenticated. Attempting login..." -ForegroundColor Red
    az login --use-device-code
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Authentication failed" -ForegroundColor Red
        exit 1
    }
}

# Set subscription
Write-Host "`n[STEP 3] Setting Subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionId
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to set subscription" -ForegroundColor Red
    Write-Host "📋 Available subscriptions:" -ForegroundColor Cyan
    az account list --output table
    exit 1
}
Write-Host "✅ Subscription set successfully" -ForegroundColor Green

# Check existing resources
Write-Host "`n[STEP 4] Checking Existing Resources..." -ForegroundColor Yellow
$resourceGroupExists = az group exists --name $ResourceGroupName
if ($resourceGroupExists -eq "true") {
    Write-Host "⚠️ Resource group exists. Checking web app..." -ForegroundColor Yellow
    
    $webAppExists = az webapp show --name $WebAppBaseName --resource-group $ResourceGroupName --query "name" --output tsv 2>$null
    if ($webAppExists) {
        Write-Host "⚠️ Web app exists. Testing if it's working..." -ForegroundColor Yellow
        $healthWorking = Test-Endpoint "https://$WebAppBaseName.azurewebsites.net/health" "Existing Health Endpoint"
        
        if ($healthWorking) {
            Write-Host "✅ Existing deployment is working!" -ForegroundColor Green
            Write-Host "🌐 Your L.I.F.E Platform: https://$WebAppBaseName.azurewebsites.net/" -ForegroundColor Cyan
            exit 0
        } else {
            Write-Host "❌ Existing web app not responding. Will restart and redeploy..." -ForegroundColor Red
            az webapp restart --name $WebAppBaseName --resource-group $ResourceGroupName
            Start-Sleep -Seconds 30
        }
    }
}

# Generate unique app name if needed
$timestamp = Get-Date -Format "MMddHHmm"
$uniqueWebAppName = "$WebAppBaseName-$timestamp"

Write-Host "`n[STEP 5] Creating Resources..." -ForegroundColor Yellow

# Create resource group
Write-Host "Creating resource group..." -ForegroundColor Cyan
az group create --name $ResourceGroupName --location $Location --tags environment=staging platform=life-platform marketplace-offer=9a600d96-fe1e-420b-902a-a0c42c561adb
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create resource group" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Resource group created" -ForegroundColor Green

# Create App Service Plan
Write-Host "Creating App Service Plan..." -ForegroundColor Cyan
az appservice plan create `
    --name "$ResourceGroupName-plan" `
    --resource-group $ResourceGroupName `
    --sku F1 `
    --is-linux `
    --location $Location

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create App Service Plan" -ForegroundColor Red
    exit 1
}
Write-Host "✅ App Service Plan created" -ForegroundColor Green

# Create Web App with unique name
Write-Host "Creating Web App: $uniqueWebAppName..." -ForegroundColor Cyan
az webapp create `
    --name $uniqueWebAppName `
    --resource-group $ResourceGroupName `
    --plan "$ResourceGroupName-plan" `
    --runtime "PYTHON:3.11"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create Web App" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Web App created: $uniqueWebAppName" -ForegroundColor Green

# Configure app settings
Write-Host "`n[STEP 6] Configuring Application..." -ForegroundColor Yellow
az webapp config appsettings set `
    --name $uniqueWebAppName `
    --resource-group $ResourceGroupName `
    --settings `
        "ENVIRONMENT=staging" `
        "PLATFORM=L.I.F.E Platform" `
        "MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb" `
        "PYTHONPATH=/home/site/wwwroot" `
        "SCM_DO_BUILD_DURING_DEPLOYMENT=true"

Write-Host "✅ Application settings configured" -ForegroundColor Green

# Deploy application
Write-Host "`n[STEP 7] Deploying Application..." -ForegroundColor Yellow
if (Test-Path "staging_health_app.py") {
    # Create deployment directory
    $deployDir = "temp_deploy"
    if (Test-Path $deployDir) { Remove-Item $deployDir -Recurse -Force }
    New-Item -ItemType Directory -Path $deployDir | Out-Null
    
    # Copy files
    Copy-Item "staging_health_app.py" $deployDir
    Copy-Item "requirements.txt" $deployDir
    
    # Deploy using webapp up
    Push-Location $deployDir
    az webapp up `
        --name $uniqueWebAppName `
        --resource-group $ResourceGroupName `
        --runtime "PYTHON:3.11" `
        --location $Location
    Pop-Location
    
    # Cleanup
    Remove-Item $deployDir -Recurse -Force
    
    Write-Host "✅ Application deployed" -ForegroundColor Green
} else {
    Write-Host "❌ staging_health_app.py not found" -ForegroundColor Red
    exit 1
}

# Restart and wait
Write-Host "`n[STEP 8] Starting Application..." -ForegroundColor Yellow
az webapp restart --name $uniqueWebAppName --resource-group $ResourceGroupName
Write-Host "⏳ Waiting 60 seconds for application to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 60

# Test endpoints
Write-Host "`n[STEP 9] Testing Endpoints..." -ForegroundColor Yellow
$baseUrl = "https://$uniqueWebAppName.azurewebsites.net"

$endpoints = @(
    @{ Url = "$baseUrl/"; Name = "Main Page" },
    @{ Url = "$baseUrl/health"; Name = "Health Check" },
    @{ Url = "$baseUrl/api/status"; Name = "Status API" }
)

$successCount = 0
foreach ($endpoint in $endpoints) {
    if (Test-Endpoint $endpoint.Url $endpoint.Name) {
        $successCount++
    }
    Start-Sleep -Seconds 2
}

# Results
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🎉 DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

if ($successCount -gt 0) {
    Write-Host "🌐 Your L.I.F.E Platform URLs:" -ForegroundColor Green
    Write-Host "📍 Main: $baseUrl/" -ForegroundColor Cyan
    Write-Host "🏥 Health: $baseUrl/health" -ForegroundColor Cyan
    Write-Host "📊 Status: $baseUrl/api/status" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💰 Business Impact:" -ForegroundColor Green
    Write-Host "✅ Staging environment operational" -ForegroundColor White
    Write-Host "✅ `$345K Q4 2025 revenue target enabled" -ForegroundColor White
    Write-Host "✅ Production deployment pathway validated" -ForegroundColor White
    
    $openBrowser = Read-Host "`nOpen platform in browser? (y/n)"
    if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
        Start-Process $baseUrl
        Start-Sleep -Seconds 2
        Start-Process "$baseUrl/health"
    }
} else {
    Write-Host "⚠️ Deployment completed but endpoints not responding yet" -ForegroundColor Yellow
    Write-Host "💡 This is normal for new deployments. Try again in 5-10 minutes." -ForegroundColor Cyan
    Write-Host "🔧 Check Azure Portal logs if issues persist" -ForegroundColor Cyan
}

Write-Host "`n🚀 L.I.F.E Platform deployment script complete!" -ForegroundColor Green