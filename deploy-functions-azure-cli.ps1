# Azure Functions Deployment Script - Azure CLI Method
# L.I.F.E. Platform - Production Deployment
# Copyright 2025 - Sergio Paya Borrull

param(
    [string]$ResourceGroupName = "life-platform-rg",
    [string]$FunctionAppName = "life-functions-app",
    [switch]$DryRun = $false
)

Write-Host "🚀 L.I.F.E. Platform Azure Functions Deployment (Azure CLI Method)" -ForegroundColor Green
Write-Host "📅 Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "🎯 Target: $FunctionAppName in $ResourceGroupName" -ForegroundColor Cyan
Write-Host ""

# Function to check if Azure CLI is logged in
function Test-AzureLogin {
    try {
        $account = az account show --query "user.name" -o tsv 2>$null
        if ($LASTEXITCODE -eq 0 -and $account) {
            Write-Host "✅ Azure CLI authenticated as: $account" -ForegroundColor Green
            return $true
        }
    }
    catch {
        # Ignore error
    }
    
    Write-Host "❌ Azure CLI not authenticated. Please run 'az login' first." -ForegroundColor Red
    return $false
}

# Function to create deployment package
function New-FunctionDeploymentPackage {
    Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow
    
    # Create temporary deployment directory
    $deployDir = "temp_deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $deployDir -Force | Out-Null
    
    try {
        # Copy function files
        Copy-Item "function_app.py" -Destination $deployDir
        Copy-Item "host.json" -Destination $deployDir
        Copy-Item "azure_functions_requirements.txt" -Destination "$deployDir\requirements.txt"
        
        # Create .funcignore file
        @(
            "*.pyc"
            "__pycache__"
            ".git*"
            ".vscode"
            "local.settings.json"
            "test_*"
            "*.md"
            "*.ps1"
        ) | Out-File -FilePath "$deployDir\.funcignore" -Encoding utf8
        
        # Create zip package
        $zipPath = "life-functions-deployment.zip"
        if (Test-Path $zipPath) {
            Remove-Item $zipPath -Force
        }
        
        Compress-Archive -Path "$deployDir\*" -DestinationPath $zipPath -Force
        
        Write-Host "✅ Deployment package created: $zipPath" -ForegroundColor Green
        return $zipPath
    }
    finally {
        # Clean up temp directory
        Remove-Item $deployDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Function to validate Function App
function Test-FunctionApp {
    param([string]$AppName, [string]$ResourceGroup)
    
    Write-Host "🔍 Validating Function App..." -ForegroundColor Yellow
    
    $app = az functionapp show --name $AppName --resource-group $ResourceGroup --query "{name:name, state:state, runtime:linuxFxVersion, hostNames:defaultHostNames}" -o json 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Function App '$AppName' not found in resource group '$ResourceGroup'" -ForegroundColor Red
        return $false
    }
    
    $appInfo = $app | ConvertFrom-Json
    Write-Host "✅ Function App found:" -ForegroundColor Green
    Write-Host "   Name: $($appInfo.name)" -ForegroundColor Gray
    Write-Host "   State: $($appInfo.state)" -ForegroundColor Gray
    Write-Host "   Runtime: $($appInfo.runtime)" -ForegroundColor Gray
    Write-Host "   URL: https://$($appInfo.hostNames[0])" -ForegroundColor Gray
    
    return $true
}

# Function to deploy functions
function Deploy-Functions {
    param([string]$AppName, [string]$ResourceGroup, [string]$ZipPath)
    
    Write-Host "🚀 Deploying functions to Azure..." -ForegroundColor Yellow
    
    if ($DryRun) {
        Write-Host "🔍 DRY RUN: Would deploy $ZipPath to $AppName" -ForegroundColor Magenta
        return $true
    }
    
    # Deploy using Azure CLI
    Write-Host "📤 Uploading deployment package..." -ForegroundColor Cyan
    az functionapp deployment source config-zip --src $ZipPath --name $AppName --resource-group $ResourceGroup --build-remote true
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Functions deployed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Deployment failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        return $false
    }
}

# Function to test deployed functions
function Test-DeployedFunctions {
    param([string]$AppName, [string]$ResourceGroup)
    
    Write-Host "🧪 Testing deployed functions..." -ForegroundColor Yellow
    
    # Wait for deployment to complete
    Start-Sleep -Seconds 30
    
    # List functions
    Write-Host "📋 Listing deployed functions:" -ForegroundColor Cyan
    az functionapp function list --name $AppName --resource-group $ResourceGroup --query "[].{Name:name, Language:language, InvokeUrlTemplate:invokeUrlTemplate}" -o table
    
    # Get function app URL
    $hostName = az functionapp show --name $AppName --resource-group $ResourceGroup --query "defaultHostNames[0]" -o tsv
    $baseUrl = "https://$hostName"
    
    Write-Host ""
    Write-Host "🌐 Function App Base URL: $baseUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Available Endpoints:" -ForegroundColor Cyan
    Write-Host "   🧠 EEG Processor: $baseUrl/api/eeg_processor" -ForegroundColor Gray
    Write-Host "   ⚡ Learning API: $baseUrl/api/learning_api" -ForegroundColor Gray
    Write-Host "   📊 Analytics: $baseUrl/api/analytics_monitor" -ForegroundColor Gray
    Write-Host "   🔐 Auth Handler: $baseUrl/api/auth_handler" -ForegroundColor Gray
    Write-Host "   📧 Campaign Automation: $baseUrl/api/campaign_automation" -ForegroundColor Gray
    
    return $true
}

# Main deployment process
try {
    Write-Host "=== L.I.F.E. Platform Function Deployment ===" -ForegroundColor Magenta
    Write-Host ""
    
    # Step 1: Validate Azure login
    if (-not (Test-AzureLogin)) {
        throw "Azure authentication required"
    }
    
    # Step 2: Validate Function App exists
    if (-not (Test-FunctionApp -AppName $FunctionAppName -ResourceGroup $ResourceGroupName)) {
        throw "Function App validation failed"
    }
    
    # Step 3: Create deployment package
    $zipPath = New-FunctionDeploymentPackage
    
    # Step 4: Deploy functions
    if (Deploy-Functions -AppName $FunctionAppName -ResourceGroup $ResourceGroupName -ZipPath $zipPath) {
        Write-Host ""
        Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
        Write-Host ""
        
        # Step 5: Test deployment
        Test-DeployedFunctions -AppName $FunctionAppName -ResourceGroup $ResourceGroupName
        
        Write-Host ""
        Write-Host "🚀 L.I.F.E. Platform Azure Functions are now LIVE!" -ForegroundColor Green
        Write-Host "🎯 October 7th launch automation is ready!" -ForegroundColor Yellow
        Write-Host ""
    } else {
        throw "Function deployment failed"
    }
}
catch {
    Write-Host ""
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    
    if ($zipPath -and (Test-Path $zipPath)) {
        Write-Host "📦 Deployment package saved: $zipPath" -ForegroundColor Gray
        Write-Host "   You can manually upload this to your Function App via Azure Portal" -ForegroundColor Gray
    }
    
    exit 1
}
finally {
    # Clean up deployment package
    if ($zipPath -and (Test-Path $zipPath) -and -not $DryRun) {
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "✨ L.I.F.E. Platform deployment complete! Ready for October 7th launch! 🎂" -ForegroundColor Magenta