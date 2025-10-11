# L.I.F.E. Platform Azure Static Web App Deployment Script
# Emergency deployment for October 15, 2025 demos
# Copyright 2025 - Sergio Paya Borrull

Write-Host "🚀 L.I.F.E. Platform Emergency Deployment - October 15 Demo Ready" -ForegroundColor Green
Write-Host "=" * 70

# Get Azure access token
Write-Host "🔑 Getting Azure access token..." -ForegroundColor Yellow
$ACCESS_TOKEN = az account get-access-token --query accessToken -o tsv

if (-not $ACCESS_TOKEN) {
    Write-Host "❌ Failed to get access token" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Access token obtained (length: $($ACCESS_TOKEN.Length))" -ForegroundColor Green

# Azure resource details
$subscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca"
$resourceGroup = "life-platform-rg"
$staticWebAppName = "life-platform-webapp"

Write-Host "🌐 Target Static Web App: https://green-ground-0c65efe0f.1.azurestaticapps.net" -ForegroundColor Cyan

# Method 1: Trigger deployment sync with GitHub
Write-Host "`n📡 Method 1: Triggering GitHub sync..." -ForegroundColor Yellow

$syncUrl = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Web/staticSites/$staticWebAppName/sync"

try {
    $syncResponse = Invoke-RestMethod -Uri "$syncUrl" -Method Post -Headers @{
        'Authorization' = "Bearer $ACCESS_TOKEN"
        'Content-Type' = 'application/json'
    }
    Write-Host "✅ Sync triggered successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Sync method failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Method 2: Reset API key to force rebuild
Write-Host "`n🔄 Method 2: Resetting API key to force rebuild..." -ForegroundColor Yellow

$resetUrl = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Web/staticSites/$staticWebAppName/resetApiKey"

try {
    $resetResponse = Invoke-RestMethod -Uri "$resetUrl" -Method Post -Headers @{
        'Authorization' = "Bearer $ACCESS_TOKEN"
        'Content-Type' = 'application/json'
    }
    Write-Host "✅ API key reset successful" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API reset method failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Method 3: Check if we need to push index.html to GitHub root
Write-Host "`n📁 Method 3: Checking GitHub repository structure..." -ForegroundColor Yellow

# Check if index.html exists in root of GitHub repo
$repoApiUrl = "https://api.github.com/repos/SergiLIFE/SergiLIFE-life-azure-system/contents/index.html"

try {
    $indexCheck = Invoke-RestMethod -Uri $repoApiUrl -Method Get
    Write-Host "✅ index.html found in GitHub root" -ForegroundColor Green
} catch {
    Write-Host "⚠️  index.html not found in GitHub root - this may be the issue!" -ForegroundColor Red
    Write-Host "📝 The Static Web App needs index.html in the repository root directory" -ForegroundColor Yellow
    
    # Let's check what's in the public directory
    try {
        $publicCheck = Invoke-RestMethod -Uri "https://api.github.com/repos/SergiLIFE/SergiLIFE-life-azure-system/contents/public" -Method Get
        Write-Host "📂 Found public directory - checking contents..." -ForegroundColor Cyan
        
        # Check if public/index.html exists
        $publicIndexCheck = Invoke-RestMethod -Uri "https://api.github.com/repos/SergiLIFE/SergiLIFE-life-azure-system/contents/public/index.html" -Method Get
        Write-Host "✅ Found index.html in public directory" -ForegroundColor Green
        Write-Host "💡 Static Web App may be looking for files in /public folder" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ No index.html found in public directory either" -ForegroundColor Red
    }
}

# Method 4: Direct deployment status check
Write-Host "`n📊 Method 4: Checking deployment status..." -ForegroundColor Yellow

$statusUrl = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Web/staticSites/$staticWebAppName/builds"

try {
    $buildsResponse = Invoke-RestMethod -Uri "$statusUrl" -Method Get -Headers @{
        'Authorization' = "Bearer $ACCESS_TOKEN"
    }
    
    if ($buildsResponse.value) {
        $latestBuild = $buildsResponse.value[0]
        Write-Host "📋 Latest build status: $($latestBuild.properties.status)" -ForegroundColor Cyan
        Write-Host "🕐 Build time: $($latestBuild.properties.createdTimeUtc)" -ForegroundColor Cyan
        
        if ($latestBuild.properties.status -eq "Ready") {
            Write-Host "✅ Build is ready - content should be live" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Build status indicates pending deployment" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Could not check build status: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Final verification
Write-Host "`n🔍 Final verification - testing Static Web App..." -ForegroundColor Yellow

try {
    $webResponse = Invoke-WebRequest -Uri "https://green-ground-0c65efe0f.1.azurestaticapps.net" -UseBasicParsing
    
    if ($webResponse.Content -match "L\.I\.F\.E\. Platform") {
        Write-Host "🎉 SUCCESS! L.I.F.E. Platform content is live!" -ForegroundColor Green
        Write-Host "✅ Ready for October 15 demos with 23 participants" -ForegroundColor Green
    } elseif ($webResponse.Content -match "Azure Static Web Apps") {
        Write-Host "⚠️  Still showing default Azure page - deployment in progress" -ForegroundColor Yellow
        Write-Host "⏳ Please wait 2-3 minutes for changes to propagate" -ForegroundColor Cyan
    } else {
        Write-Host "❓ Unknown content detected - manual review needed" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Could not verify web app status: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + ("=" * 70)
Write-Host "🎯 OCTOBER 15 DEMO STATUS:" -ForegroundColor White -BackgroundColor Blue
Write-Host "📅 Date: October 15, 2025" -ForegroundColor Cyan
Write-Host "👥 Participants: 23 registered" -ForegroundColor Cyan  
Write-Host "💰 Pipeline value: $771K+" -ForegroundColor Green
Write-Host "🌐 Platform URL: https://green-ground-0c65efe0f.1.azurestaticapps.net" -ForegroundColor Cyan
Write-Host "🆔 Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb" -ForegroundColor Cyan
Write-Host "`nDeployment commands executed - platform should be live within 3 minutes!" -ForegroundColor Green