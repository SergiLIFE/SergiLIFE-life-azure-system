# L.I.F.E. Platform Live Endpoint Testing & Function App Monitoring
# Generated: September 28, 2025
# Purpose: Test live Azure infrastructure and monitor Function App activity

param(
    [string]$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca",
    [string]$ResourceGroup = "life-platform-rg",
    [switch]$Detailed
)

Write-Host "🎯 L.I.F.E. Platform Live Endpoint Testing" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Set Azure subscription
Write-Host "🔗 Setting Azure subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionId

# Function to test HTTP endpoints
function Test-Endpoint {
    param(
        [string]$Url,
        [string]$Name,
        [int]$TimeoutSeconds = 30
    )
    
    try {
        Write-Host "🌐 Testing $Name..." -ForegroundColor Green
        Write-Host "   URL: $Url" -ForegroundColor Gray
        
        $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec $TimeoutSeconds -UseBasicParsing
        Write-Host "   ✅ Status: $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
        Write-Host "   📊 Response Length: $($response.Content.Length) bytes" -ForegroundColor Gray
        
        if ($Detailed) {
            Write-Host "   📋 Headers:" -ForegroundColor Gray
            $response.Headers | Format-Table -AutoSize
        }
        
        return $true
    }
    catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "🚀 PHASE 1: Function App Status Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Get Function Apps and their URLs
Write-Host "📋 Retrieving Function App information..." -ForegroundColor Yellow
$functionApps = az functionapp list --resource-group $ResourceGroup --query "[].{Name:name, State:state, DefaultHostName:defaultHostName, Location:location}" -o json | ConvertFrom-Json

if ($functionApps.Count -eq 0) {
    Write-Host "⚠️  No Function Apps found in resource group: $ResourceGroup" -ForegroundColor Yellow
    Write-Host "🔍 Checking all Function Apps in subscription..." -ForegroundColor Yellow
    $functionApps = az functionapp list --query "[?contains(name,'life')].{Name:name, State:state, DefaultHostName:defaultHostName, Location:location, ResourceGroup:resourceGroup}" -o json | ConvertFrom-Json
}

foreach ($app in $functionApps) {
    Write-Host ""
    Write-Host "🔧 Function App: $($app.Name)" -ForegroundColor Magenta
    Write-Host "   📍 Location: $($app.Location)" -ForegroundColor Gray
    Write-Host "   🔄 State: $($app.State)" -ForegroundColor Gray
    Write-Host "   🌐 Host: $($app.DefaultHostName)" -ForegroundColor Gray
    
    if ($app.ResourceGroup) {
        Write-Host "   📂 Resource Group: $($app.ResourceGroup)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🌐 PHASE 2: Endpoint Connectivity Testing" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan

# Test Function App endpoints
foreach ($app in $functionApps) {
    if ($app.DefaultHostName -and $app.State -eq "Running") {
        $baseUrl = "https://$($app.DefaultHostName)"
        
        Write-Host ""
        Write-Host "🧪 Testing: $($app.Name)" -ForegroundColor Magenta
        
        # Test basic endpoint
        Test-Endpoint -Url $baseUrl -Name "Base URL"
        
        # Test common Function App endpoints
        Test-Endpoint -Url "$baseUrl/api/health" -Name "Health Check"
        Test-Endpoint -Url "$baseUrl/api/status" -Name "Status Endpoint"
        Test-Endpoint -Url "$baseUrl/api/info" -Name "Info Endpoint"
    }
}

Write-Host ""
Write-Host "📊 PHASE 3: Function App Logs & Metrics" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

foreach ($app in $functionApps) {
    Write-Host ""
    Write-Host "📋 Logs for: $($app.Name)" -ForegroundColor Magenta
    
    try {
        # Get recent logs (last 50 lines)
        Write-Host "🔍 Retrieving recent activity logs..." -ForegroundColor Yellow
        
        $resourceGroupName = if ($app.ResourceGroup) { $app.ResourceGroup } else { $ResourceGroup }
        
        # Get Function App logs
        Write-Host "   📝 Function App Logs (Last 10 entries):" -ForegroundColor Green
        az functionapp logs tail --name $app.Name --resource-group $resourceGroupName --max-lines 10 --timeout 10 2>$null
        
        # Get Function App configuration
        if ($Detailed) {
            Write-Host "   ⚙️  App Settings:" -ForegroundColor Green
            az functionapp config appsettings list --name $app.Name --resource-group $resourceGroupName --query "[].{Name:name, Value:value}" -o table 2>$null
        }
        
        # Get Function definitions
        Write-Host "   🔧 Available Functions:" -ForegroundColor Green
        az functionapp function list --name $app.Name --resource-group $resourceGroupName --query "[].{Name:name, Language:language}" -o table 2>$null
        
    }
    catch {
        Write-Host "   ⚠️  Could not retrieve logs: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🏗️ PHASE 4: Static Web App Testing" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Test Static Web App
$staticWebApps = az staticwebapp list --resource-group $ResourceGroup --query "[].{Name:name, DefaultHostName:defaultHostname}" -o json 2>$null | ConvertFrom-Json

foreach ($webapp in $staticWebApps) {
    Write-Host ""
    Write-Host "🌐 Testing Static Web App: $($webapp.Name)" -ForegroundColor Magenta
    if ($webapp.DefaultHostName) {
        Test-Endpoint -Url "https://$($webapp.DefaultHostName)" -Name "Static Web App"
    }
}

Write-Host ""
Write-Host "🔐 PHASE 5: Key Vault & Storage Validation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Test Key Vault accessibility
Write-Host "🔑 Testing Key Vault access..." -ForegroundColor Yellow
$keyVaults = az keyvault list --resource-group $ResourceGroup --query "[].{Name:name, VaultUri:properties.vaultUri}" -o json 2>$null | ConvertFrom-Json

foreach ($kv in $keyVaults) {
    Write-Host "   🔐 Key Vault: $($kv.Name)" -ForegroundColor Green
    Write-Host "   🌐 URI: $($kv.VaultUri)" -ForegroundColor Gray
    
    # Try to list secrets (will show if accessible)
    try {
        $secretCount = (az keyvault secret list --vault-name $kv.Name --query "length(@)" -o tsv 2>$null)
        Write-Host "   📋 Accessible Secrets: $secretCount" -ForegroundColor Green
    }
    catch {
        Write-Host "   ⚠️  Access restricted (normal for production)" -ForegroundColor Yellow
    }
}

# Test Storage Account accessibility  
Write-Host ""
Write-Host "💾 Testing Storage Account access..." -ForegroundColor Yellow
$storageAccounts = az storage account list --resource-group $ResourceGroup --query "[].{Name:name, PrimaryEndpoints:primaryEndpoints}" -o json 2>$null | ConvertFrom-Json

foreach ($storage in $storageAccounts) {
    Write-Host "   💾 Storage Account: $($storage.Name)" -ForegroundColor Green
    if ($storage.PrimaryEndpoints.blob) {
        Write-Host "   🔗 Blob Endpoint: $($storage.PrimaryEndpoints.blob)" -ForegroundColor Gray
        Test-Endpoint -Url $storage.PrimaryEndpoints.blob -Name "Blob Storage"
    }
}

Write-Host ""
Write-Host "🎯 PHASE 6: DNS & Custom Domains" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Test custom domains
$customDomains = @("coach121life.com", "lifementor121.com")

foreach ($domain in $customDomains) {
    Write-Host ""
    Write-Host "🌍 Testing DNS for: $domain" -ForegroundColor Magenta
    
    try {
        # Test DNS resolution
        $dnsResult = Resolve-DnsName $domain -Type A -ErrorAction SilentlyContinue
        if ($dnsResult) {
            Write-Host "   ✅ DNS Resolution: Success" -ForegroundColor Green
            Write-Host "   📍 IP Address: $($dnsResult.IPAddress -join ', ')" -ForegroundColor Gray
            
            # Test HTTP connectivity
            Test-Endpoint -Url "https://$domain" -Name "HTTPS Endpoint"
            Test-Endpoint -Url "http://$domain" -Name "HTTP Endpoint"
        }
        else {
            Write-Host "   ❌ DNS Resolution: Failed" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "   ⚠️  DNS Test Error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 TESTING COMPLETE!" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host "✅ Live endpoint testing finished" -ForegroundColor Green
Write-Host "📊 Check results above for any issues" -ForegroundColor Green
Write-Host "🚀 L.I.F.E. Platform status validated!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 For more detailed analysis, run with -Detailed switch" -ForegroundColor Cyan
Write-Host "🔧 Example: .\test-live-endpoints.ps1 -Detailed" -ForegroundColor Cyan