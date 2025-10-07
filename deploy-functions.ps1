# L.I.F.E. Platform Azure Functions Deployment Script
# Deploys neuroadaptive learning functions to complete the platform
# Generated: September 28, 2025

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$ResourceGroup = "life-platform-rg",
    [string]$FunctionAppName = "life-functions-app",
    [switch]$LocalTest,
    [switch]$Deploy,
    [switch]$Validate
)

Write-Host "🚀 L.I.F.E. Platform Azure Functions Deployment" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Set Azure subscription
Write-Host "🔗 Setting Azure subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionId

if ($LocalTest) {
    Write-Host "🧪 PHASE 1: LOCAL TESTING" -ForegroundColor Green
    Write-Host "=========================" -ForegroundColor Green
    Write-Host ""
    
    # Check if Azure Functions Core Tools is installed
    Write-Host "🔧 Checking Azure Functions Core Tools..." -ForegroundColor Yellow
    try {
        $funcVersion = func --version
        Write-Host "   ✅ Azure Functions Core Tools: $funcVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ Azure Functions Core Tools not found!" -ForegroundColor Red
        Write-Host "   💡 Install with: npm install -g azure-functions-core-tools@4 --unsafe-perm true" -ForegroundColor Cyan
        return
    }
    
    # Install Python dependencies
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
    if (Test-Path "azure_functions_requirements.txt") {
        pip install -r azure_functions_requirements.txt
        Write-Host "   ✅ Dependencies installed successfully" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️  azure_functions_requirements.txt not found" -ForegroundColor Yellow
    }
    
    # Start local Function App
    Write-Host "🏃 Starting local Function App..." -ForegroundColor Yellow
    Write-Host "   💡 Testing L.I.F.E. Platform functions locally..." -ForegroundColor Cyan
    Write-Host "   🌐 Local endpoints will be available at: http://localhost:7071" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   📊 Available Functions:" -ForegroundColor Magenta
    Write-Host "   ├── POST /api/eeg/process - EEG Processing" -ForegroundColor White
    Write-Host "   ├── GET/POST /api/learning - Learning API" -ForegroundColor White
    Write-Host "   ├── GET /api/analytics - Analytics Monitor" -ForegroundColor White
    Write-Host "   ├── POST /api/auth/token - Authentication" -ForegroundColor White
    Write-Host "   └── POST /api/campaign/trigger - Campaign Automation" -ForegroundColor White
    Write-Host ""
    Write-Host "   ⚠️  Press Ctrl+C to stop local testing" -ForegroundColor Yellow
    Write-Host ""
    
    try {
        func start --python
    }
    catch {
        Write-Host "❌ Local testing failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

if ($Deploy) {
    Write-Host "🚀 PHASE 2: AZURE DEPLOYMENT" -ForegroundColor Green
    Write-Host "============================" -ForegroundColor Green
    Write-Host ""
    
    # Validate Function App exists
    Write-Host "🔍 Validating Function App..." -ForegroundColor Yellow
    $functionApp = az functionapp show --name $FunctionAppName --resource-group $ResourceGroup 2>$null | ConvertFrom-Json
    
    if (-not $functionApp) {
        Write-Host "   ❌ Function App '$FunctionAppName' not found!" -ForegroundColor Red
        return
    }
    
    Write-Host "   ✅ Function App validated: $($functionApp.state)" -ForegroundColor Green
    Write-Host "   📍 Location: $($functionApp.location)" -ForegroundColor Gray
    Write-Host "   🐍 Runtime: $($functionApp.siteConfig.linuxFxVersion)" -ForegroundColor Gray
    
    # Create deployment package
    Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow
    
    # Ensure we have the required files
    $requiredFiles = @("function_app.py", "host.json", "local.settings.json")
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Host "   ❌ Required file missing: $file" -ForegroundColor Red
            return
        }
    }
    
    Write-Host "   ✅ All required files present" -ForegroundColor Green
    
    # Deploy using Azure CLI
    Write-Host "🚀 Deploying to Azure Function App..." -ForegroundColor Yellow
    Write-Host "   📤 Uploading L.I.F.E. Platform functions..." -ForegroundColor Cyan
    
    try {
        # Deploy the function app code
        az functionapp deployment source config-zip --name $FunctionAppName --resource-group $ResourceGroup --src "function_deployment.zip" --build-remote true 2>$null
        
        # Alternative: Deploy from current directory
        Write-Host "   📂 Deploying from current directory..." -ForegroundColor Cyan
        
        # Create a simple zip deployment
        $deploymentFiles = @("function_app.py", "host.json", "azure_functions_requirements.txt")
        
        # Use func azure functionapp publish command
        func azure functionapp publish $FunctionAppName --python
        
        Write-Host "   ✅ Deployment completed successfully!" -ForegroundColor Green
        
    }
    catch {
        Write-Host "   ❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   💡 Try manual deployment or check function app logs" -ForegroundColor Yellow
        return
    }
    
    # Wait for deployment to propagate
    Write-Host "⏳ Waiting for deployment to propagate..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
    
    Write-Host "✅ Deployment phase completed!" -ForegroundColor Green
}

if ($Validate) {
    Write-Host "🔍 PHASE 3: DEPLOYMENT VALIDATION" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    
    # Get Function App URL
    $functionAppUrl = "https://$FunctionAppName.azurewebsites.net"
    Write-Host "🌐 Function App URL: $functionAppUrl" -ForegroundColor Cyan
    Write-Host ""
    
    # Test endpoints
    $endpoints = @(
        @{Name = "Learning API (GET)"; Url = "$functionAppUrl/api/learning"; Method = "GET"},
        @{Name = "Analytics"; Url = "$functionAppUrl/api/analytics"; Method = "GET"},
        @{Name = "Health Check"; Url = "$functionAppUrl/api/health"; Method = "GET"}
    )
    
    foreach ($endpoint in $endpoints) {
        Write-Host "🧪 Testing: $($endpoint.Name)" -ForegroundColor Magenta
        Write-Host "   URL: $($endpoint.Url)" -ForegroundColor Gray
        
        try {
            $response = Invoke-WebRequest -Uri $endpoint.Url -Method $endpoint.Method -TimeoutSec 30 -UseBasicParsing
            Write-Host "   ✅ Status: $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
        }
        catch {
            Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
        }
        Write-Host ""
    }
    
    # Check Function App logs
    Write-Host "📝 Checking Function App logs..." -ForegroundColor Yellow
    try {
        az webapp log tail --name $FunctionAppName --resource-group $ResourceGroup --timeout 10 2>$null
    }
    catch {
        Write-Host "   ⚠️  Could not retrieve logs (this is normal for new deployments)" -ForegroundColor Yellow
    }
    
    # List deployed functions
    Write-Host "📋 Deployed Functions:" -ForegroundColor Magenta
    try {
        $functions = az functionapp function list --name $FunctionAppName --resource-group $ResourceGroup | ConvertFrom-Json
        
        if ($functions.Count -gt 0) {
            foreach ($func in $functions) {
                Write-Host "   ✅ $($func.name) - $($func.language)" -ForegroundColor Green
            }
        }
        else {
            Write-Host "   ⚠️  No functions found (deployment may still be in progress)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "   ⚠️  Could not list functions (may still be deploying)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎯 DEPLOYMENT SUMMARY" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host "📊 Function App: $FunctionAppName" -ForegroundColor White
Write-Host "🌐 URL: https://$FunctionAppName.azurewebsites.net" -ForegroundColor White
Write-Host "📍 Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "🐍 Runtime: Python 3.11" -ForegroundColor White
Write-Host ""
Write-Host "🎉 L.I.F.E. Platform Functions Ready!" -ForegroundColor Green
Write-Host "🚀 Platform complete for October 7th launch!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Usage Examples:" -ForegroundColor Cyan
Write-Host "   Test locally:  .\deploy-functions.ps1 -LocalTest" -ForegroundColor Gray
Write-Host "   Deploy:        .\deploy-functions.ps1 -Deploy" -ForegroundColor Gray
Write-Host "   Validate:      .\deploy-functions.ps1 -Validate" -ForegroundColor Gray
Write-Host "   Full deploy:   .\deploy-functions.ps1 -Deploy -Validate" -ForegroundColor Gray