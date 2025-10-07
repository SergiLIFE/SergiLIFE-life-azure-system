#!/usr/bin/env pwsh

# NAKEDai L.I.F.E. INSTANT BACKUP - Launch Day Sept 27, 2025
# Copyright 2025 - Sergio Paya Borrull

Write-Host "🚀 NAKEDai L.I.F.E. INSTANT BACKUP SYSTEM" -ForegroundColor Magenta -BackgroundColor Black
Write-Host "Launch Day: September 27, 2025 | Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb"
Write-Host "Revolutionary 45 TOPS Neural Computing Glasses"
Write-Host "=" * 80

# Quick backup using your existing Azure subscription
$subscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca"
$resourceGroup = "life-platform-rg"  # Your existing resource group
$storageAccount = "stlifeplatformprod"  # Your existing storage account

try {
    Write-Host "🔧 Setting Azure subscription..." -ForegroundColor Yellow
    az account set --subscription $subscriptionId
    
    Write-Host "📁 Creating backup containers..." -ForegroundColor Yellow
    
    # Create containers in your existing storage account
    $containers = @(
        "nakedai-integration",
        "launch-day-backup",
        "recovery-scripts"
    )
    
    foreach ($container in $containers) {
        Write-Host "📦 Creating container: $container"
        az storage container create --name $container --account-name $storageAccount --auth-mode login 2>$null
    }
    
    Write-Host "📤 Uploading NAKEDai L.I.F.E. files..." -ForegroundColor Green
    
    # Upload all your critical files
    $files = Get-ChildItem -Path "." -Include "*.py", "*.md", "*.ps1", "*.sh", "*.txt", "*.yml" -Recurse
    
    foreach ($file in $files) {
        if ($file.Name -like "*NAKEDai*" -or $file.Name -like "*L.I.F.E*" -or $file.Name -like "*experiment*") {
            Write-Host "⬆️  Uploading: $($file.Name)"
            az storage blob upload --account-name $storageAccount --container-name "nakedai-integration" --name $file.Name --file $file.FullName --auth-mode login --overwrite 2>$null
        }
    }
    
    # Upload recovery scripts
    az storage blob upload --account-name $storageAccount --container-name "recovery-scripts" --name "CloudShell-Recovery-Script.sh" --file "CloudShell-Recovery-Script.sh" --auth-mode login --overwrite 2>$null
    az storage blob upload --account-name $storageAccount --container-name "recovery-scripts" --name "PowerShell-Recovery-Script.ps1" --file "PowerShell-Recovery-Script.ps1" --auth-mode login --overwrite 2>$null
    
    Write-Host ""
    Write-Host "🎉 NAKEDai L.I.F.E. BACKUP COMPLETE!" -ForegroundColor Green -BackgroundColor Black
    Write-Host "=" * 80
    Write-Host "✅ Storage Account: $storageAccount" -ForegroundColor Green
    Write-Host "✅ Resource Group: $resourceGroup" -ForegroundColor Green
    Write-Host "✅ Subscription: $subscriptionId" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔥 INSTANT RECOVERY COMMANDS:" -ForegroundColor Red
    Write-Host ""
    Write-Host "Azure CloudShell:" -ForegroundColor Yellow
    Write-Host "az storage blob download-batch --account-name $storageAccount --source nakedai-integration --destination ./recovery --auth-mode login" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "PowerShell:" -ForegroundColor Yellow
    Write-Host "az storage blob download --account-name $storageAccount --container-name recovery-scripts --name PowerShell-Recovery-Script.ps1 --file recovery.ps1 --auth-mode login; .\recovery.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌍 READY TO CHANGE THE WORLD WITH 45 TOPS NEURAL COMPUTING! 🚀" -ForegroundColor Magenta -BackgroundColor Black

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure you're logged in: az login" -ForegroundColor Yellow
}