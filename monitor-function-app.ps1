# L.I.F.E. Platform Function App Live Monitoring
# Real-time log streaming and activity monitoring
# Generated: September 28, 2025

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$FunctionAppName = "life-functions-app",
    [string]$ResourceGroup = "life-platform-rg",
    [int]$LogLines = 50,
    [switch]$StreamLogs,
    [switch]$HealthCheck
)

Write-Host "🔍 L.I.F.E. Platform Function App Monitoring" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Set Azure subscription
az account set --subscription $SubscriptionId

Write-Host "📊 FUNCTION APP OVERVIEW" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow

# Get Function App details
Write-Host "🔍 Retrieving Function App information..." -ForegroundColor Green
$functionApp = az functionapp show --name $FunctionAppName --resource-group $ResourceGroup --query "{Name:name, State:state, Location:location, DefaultHostName:defaultHostName, Runtime:siteConfig.linuxFxVersion, AppServicePlan:serverFarmId}" -o json | ConvertFrom-Json

Write-Host "📋 Function App Details:" -ForegroundColor Magenta
Write-Host "   🏷️  Name: $($functionApp.Name)" -ForegroundColor White
Write-Host "   🔄 State: $($functionApp.State)" -ForegroundColor White  
Write-Host "   📍 Location: $($functionApp.Location)" -ForegroundColor White
Write-Host "   🌐 Host: $($functionApp.DefaultHostName)" -ForegroundColor White
Write-Host "   ⚙️  Runtime: $($functionApp.Runtime)" -ForegroundColor White

Write-Host ""
Write-Host "🔧 AVAILABLE FUNCTIONS" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow

# List all functions in the Function App
try {
    $functions = az functionapp function list --name $FunctionAppName --resource-group $ResourceGroup --query "[].{Name:name, Language:language, TriggerType:trigger.type}" -o json | ConvertFrom-Json
    
    if ($functions.Count -gt 0) {
        foreach ($func in $functions) {
            Write-Host "   ⚡ Function: $($func.Name)" -ForegroundColor Green
            Write-Host "     - Language: $($func.Language)" -ForegroundColor Gray
            Write-Host "     - Trigger: $($func.TriggerType)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  No functions found or unable to retrieve function list" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "   ❌ Error retrieving functions: $($_.Exception.Message)" -ForegroundColor Red
}

if ($HealthCheck) {
    Write-Host ""
    Write-Host "🏥 HEALTH CHECK" -ForegroundColor Yellow
    Write-Host "===============" -ForegroundColor Yellow
    
    # Test the Function App URL
    $baseUrl = "https://$($functionApp.DefaultHostName)"
    
    Write-Host "🌐 Testing Function App endpoints..." -ForegroundColor Green
    
    # Test base URL
    try {
        $response = Invoke-WebRequest -Uri $baseUrl -Method GET -TimeoutSec 30 -UseBasicParsing
        Write-Host "   ✅ Base URL ($baseUrl): $($response.StatusCode)" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ Base URL test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test common API endpoints
    $commonEndpoints = @("/api/health", "/api/status", "/api/info", "/.well-known/live", "/.well-known/ready")
    
    foreach ($endpoint in $commonEndpoints) {
        try {
            $testUrl = "$baseUrl$endpoint"
            $response = Invoke-WebRequest -Uri $testUrl -Method GET -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
            Write-Host "   ✅ $endpoint : $($response.StatusCode)" -ForegroundColor Green
        }
        catch {
            Write-Host "   ⚠️  $endpoint : Not available" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "📝 RECENT LOGS" -ForegroundColor Yellow
Write-Host "==============" -ForegroundColor Yellow

Write-Host "🔍 Retrieving last $LogLines log entries..." -ForegroundColor Green

try {
    # Get Function App logs
    Write-Host ""
    Write-Host "📋 Application Logs:" -ForegroundColor Cyan
    az functionapp logs tail --name $FunctionAppName --resource-group $ResourceGroup --max-lines $LogLines --timeout 15
    
    Write-Host ""
    Write-Host "📊 Deployment Logs:" -ForegroundColor Cyan  
    az webapp log deployment list --name $FunctionAppName --resource-group $ResourceGroup --query "[].{Time:receivedTime, Status:status, Message:message}" -o table
    
    Write-Host ""
    Write-Host "⚡ Function Execution History:" -ForegroundColor Cyan
    # This requires Application Insights, will show if available
    az monitor app-insights events show --app $FunctionAppName --event requests --offset 1h --query "value[].{Timestamp:timestamp, Name:name, ResultCode:resultCode, Duration:durationMs}" -o table 2>$null
}
catch {
    Write-Host "❌ Error retrieving logs: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Tip: Logs may be limited due to permissions or Application Insights configuration" -ForegroundColor Yellow
}

if ($StreamLogs) {
    Write-Host ""
    Write-Host "🔄 LIVE LOG STREAMING" -ForegroundColor Yellow
    Write-Host "=====================" -ForegroundColor Yellow
    Write-Host "📡 Starting live log stream... (Press Ctrl+C to stop)" -ForegroundColor Green
    Write-Host ""
    
    try {
        # Start live log streaming
        az functionapp logs tail --name $FunctionAppName --resource-group $ResourceGroup --follow
    }
    catch {
        Write-Host "❌ Error starting log stream: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📊 PERFORMANCE METRICS" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow

Write-Host "🔍 Retrieving performance data..." -ForegroundColor Green

try {
    # Get App Service Plan details for performance context
    $appServicePlan = az functionapp show --name $FunctionAppName --resource-group $ResourceGroup --query "serverFarmId" -o tsv
    if ($appServicePlan) {
        $planName = Split-Path $appServicePlan -Leaf
        $planDetails = az appservice plan show --name $planName --resource-group $ResourceGroup --query "{Name:name, Sku:sku.name, Tier:sku.tier, Capacity:sku.capacity}" -o json | ConvertFrom-Json
        
        Write-Host "📋 App Service Plan:" -ForegroundColor Magenta
        Write-Host "   🏷️  Name: $($planDetails.Name)" -ForegroundColor White
        Write-Host "   💰 SKU: $($planDetails.Sku)" -ForegroundColor White
        Write-Host "   📊 Tier: $($planDetails.Tier)" -ForegroundColor White
        Write-Host "   🔢 Capacity: $($planDetails.Capacity)" -ForegroundColor White
    }
    
    # Get recent metrics (if Application Insights is configured)
    Write-Host ""
    Write-Host "📈 Recent Performance (Last 1 hour):" -ForegroundColor Magenta
    
    # CPU and Memory metrics
    az monitor metrics list --resource "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.Web/sites/$FunctionAppName" --metric "CpuPercentage" --interval PT1M --query "value[0].timeseries[0].data[-5:]" -o table 2>$null
    
    # Request count and response time
    az monitor metrics list --resource "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.Web/sites/$FunctionAppName" --metric "Requests" --interval PT5M --query "value[0].timeseries[0].data[-5:]" -o table 2>$null
}
catch {
    Write-Host "⚠️  Performance metrics may require additional permissions or Application Insights setup" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 APPLICATION SETTINGS" -ForegroundColor Yellow  
Write-Host "======================" -ForegroundColor Yellow

Write-Host "⚙️  Retrieving app configuration..." -ForegroundColor Green

try {
    # Get app settings (will show non-sensitive settings)
    $appSettings = az functionapp config appsettings list --name $FunctionAppName --resource-group $ResourceGroup --query "[].{Name:name, Value:value}" -o json | ConvertFrom-Json
    
    Write-Host "📋 Key Application Settings:" -ForegroundColor Magenta
    foreach ($setting in $appSettings) {
        # Filter out sensitive values
        if ($setting.Name -match "KEY|SECRET|PASSWORD|TOKEN") {
            Write-Host "   🔐 $($setting.Name): [PROTECTED]" -ForegroundColor Gray
        }
        elseif ($setting.Name -match "WEBSITE|FUNCTIONS|APPINSIGHTS") {
            Write-Host "   ⚙️  $($setting.Name): $($setting.Value)" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "⚠️  Could not retrieve application settings" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 MONITORING SUMMARY" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host "✅ Function App monitoring complete!" -ForegroundColor Green
Write-Host "📊 Status: $($functionApp.State)" -ForegroundColor Green
Write-Host "🌐 Endpoint: https://$($functionApp.DefaultHostName)" -ForegroundColor Green
Write-Host ""
Write-Host "💡 To stream live logs, run: .\monitor-function-app.ps1 -StreamLogs" -ForegroundColor Cyan
Write-Host "💡 For health check, run: .\monitor-function-app.ps1 -HealthCheck" -ForegroundColor Cyan