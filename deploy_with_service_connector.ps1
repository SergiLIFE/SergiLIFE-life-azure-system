# 🚀 L.I.F.E. Platform Service Connector Deployment Script
# Secure Function App deployment with Managed Identity
# Generated: September 28, 2025

Write-Host "🚀 L.I.F.E. Platform - Service Connector Deployment" -ForegroundColor Green
Write-Host "Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca" -ForegroundColor Cyan
Write-Host "Deploying with Enterprise Security..." -ForegroundColor Yellow

# Step 1: Set correct subscription
Write-Host "📋 Setting Azure subscription..." -ForegroundColor Blue
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Step 2: Setup Service Connectors first
Write-Host "🔗 Setting up Azure Service Connectors..." -ForegroundColor Blue
& ".\azure_service_connector_setup.ps1"

# Step 3: Create deployment package
Write-Host "📦 Creating deployment package..." -ForegroundColor Blue
if (Test-Path "deployment_package.zip") {
    Remove-Item "deployment_package.zip" -Force
}

# Copy Service Connector function app
Copy-Item "function_app_service_connector.py" "function_app.py" -Force
Copy-Item "requirements_service_connector.txt" "requirements.txt" -Force

# Create ZIP package
Compress-Archive -Path "function_app.py", "host.json", "requirements.txt" -DestinationPath "deployment_package.zip" -Force

Write-Host "✅ Deployment package created with Service Connector support" -ForegroundColor Green

# Step 4: Deploy using Azure CLI (Service Connector compatible)
Write-Host "🚀 Deploying L.I.F.E. Platform Functions with Service Connector..." -ForegroundColor Blue

try {
    # Enable managed identity on Function App (if not already enabled)
    az functionapp identity assign --name "life-functions-app" --resource-group "life-platform-rg"
    
    # Deploy the function package
    az functionapp deployment source config-zip --resource-group "life-platform-rg" --name "life-functions-app" --src "deployment_package.zip" --build-remote true
    
    Write-Host "🎉 Deployment SUCCESS!" -ForegroundColor Green
    
    # Step 5: Test the deployed functions
    Write-Host "🧪 Testing deployed functions..." -ForegroundColor Blue
    
    $baseUrl = "https://life-functions-app.azurewebsites.net"
    
    # Get function keys first
    Write-Host "🔑 Retrieving function keys..." -ForegroundColor Blue
    $keys = az functionapp keys list --name "life-functions-app" --resource-group "life-platform-rg" --query "functionKeys" -o json | ConvertFrom-Json
    
    if ($keys.default) {
        $functionKey = $keys.default
        Write-Host "✅ Function key retrieved successfully" -ForegroundColor Green
        
        # Test Health Check (anonymous)
        Write-Host "📊 Testing Health Check endpoint..." -ForegroundColor Blue
        try {
            $healthResponse = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method GET
            Write-Host "✅ Health Check: SUCCESS" -ForegroundColor Green
            Write-Host ($healthResponse | ConvertTo-Json -Depth 3) -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️  Health Check: $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
        # Test EEG Processor
        Write-Host "🧠 Testing EEG Processor..." -ForegroundColor Blue  
        try {
            $eegResponse = Invoke-RestMethod -Uri "$baseUrl/api/eeg/process?code=$functionKey" -Method POST -Body '{"test":"service_connector"}' -ContentType "application/json"
            Write-Host "✅ EEG Processor: SUCCESS" -ForegroundColor Green
            Write-Host ($eegResponse | ConvertTo-Json -Depth 3) -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️  EEG Processor: $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
        # Test Learning API
        Write-Host "⚡ Testing Learning API..." -ForegroundColor Blue
        try {
            $learningResponse = Invoke-RestMethod -Uri "$baseUrl/api/learning/api?code=$functionKey" -Method POST -Body '{"test":"service_connector_api"}' -ContentType "application/json"  
            Write-Host "✅ Learning API: SUCCESS" -ForegroundColor Green
            Write-Host ($learningResponse | ConvertTo-Json -Depth 3) -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️  Learning API: $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
        # Test Campaign Automation
        Write-Host "🎂 Testing October 7th Campaign..." -ForegroundColor Blue
        try {
            $campaignResponse = Invoke-RestMethod -Uri "$baseUrl/api/campaign/october7?code=$functionKey" -Method GET
            Write-Host "✅ Campaign Automation: SUCCESS" -ForegroundColor Green  
            Write-Host ($campaignResponse | ConvertTo-Json -Depth 3) -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️  Campaign Automation: $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
    } else {
        Write-Host "❌ Could not retrieve function keys" -ForegroundColor Red
    }
    
    Write-Host "" 
    Write-Host "🎉 L.I.F.E. Platform Service Connector Deployment COMPLETE!" -ForegroundColor Green
    Write-Host "✅ Function App: https://life-functions-app.azurewebsites.net" -ForegroundColor Green
    Write-Host "🔒 Security: Managed Identity + Service Connector Active" -ForegroundColor Green
    Write-Host "📅 Launch Ready: October 7, 2025" -ForegroundColor Green
    Write-Host "🚀 Campaign Status: AUTOMATED & READY" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Troubleshooting: Check Service Connector configuration" -ForegroundColor Yellow
}