# NAKEDai L.I.F.E. PowerShell Instant Recovery Script
# Copyright 2025 - Sergio Paya Borrull
# Revolutionary 45 TOPS Neural Computing Glasses

Write-Host "🚀 NAKEDai L.I.F.E. PowerShell Recovery Starting..." -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Launch Date: September 27, 2025" -ForegroundColor Green
Write-Host "Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb" -ForegroundColor Green
Write-Host "Revolutionary 45 TOPS Neural Computing Glasses" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Configuration (update these with your actual values)
$SubscriptionId = "5c88cef6-f243-497d-98af-6c6086d575ca"
$StorageAccount = "nakedailifebackup"  # Update with actual storage account name
$RecoveryDir = ".\nakedai-life-recovery"

try {
    # Check Azure CLI
    Write-Host "🔧 Checking Azure CLI..." -ForegroundColor Yellow
    $azVersion = az --version 2>$null
    if (-not $azVersion) {
        Write-Host "❌ Azure CLI not found. Please install Azure CLI first:" -ForegroundColor Red
        Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Azure CLI found" -ForegroundColor Green

    # Set subscription
    Write-Host "🔧 Setting Azure subscription..." -ForegroundColor Yellow
    az account set --subscription $SubscriptionId
    Write-Host "✅ Subscription set" -ForegroundColor Green

    # Create recovery directory
    Write-Host "📁 Creating recovery directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $RecoveryDir | Out-Null
    Write-Host "✅ Recovery directory created: $RecoveryDir" -ForegroundColor Green

    # Download core NAKEDai L.I.F.E. files
    Write-Host "📥 Downloading NAKEDai L.I.F.E. Integration System..." -ForegroundColor Yellow

    $coreFiles = @(
        "NAKEDai_LIFE_Integration_System.py",
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py",
        "NAKEDAI_VISUAL_PROTOTYPES_REALISTIC_MOCKUPS.md",
        "NAKEDAI_COPYRIGHT_IP_PROTECTION_STRATEGY.md",
        "NAKEDAI_VENTURI_DUAL_FUNCTION_SYSTEM_BREAKTHROUGH.md",
        "NAKEDAI_LIFE_CORE_MATHEMATICAL_FRAMEWORK_COMPLETE.md",
        "UNBREAKABLE_AZURE_BACKUP_SYSTEM.ps1"
    )

    foreach ($file in $coreFiles) {
        Write-Host "📄 Downloading: $file" -ForegroundColor Cyan
        $downloadResult = az storage blob download `
            --account-name $StorageAccount `
            --container-name "nakedai-source-code" `
            --name $file `
            --file "$RecoveryDir\$file" `
            --auth-mode login `
            2>$null

        if (Test-Path "$RecoveryDir\$file") {
            Write-Host "✅ $file downloaded successfully" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $file download failed" -ForegroundColor Yellow
        }
    }

    # Batch download remaining files
    Write-Host "📦 Downloading remaining files..." -ForegroundColor Yellow
    az storage blob download-batch `
        --account-name $StorageAccount `
        --source "nakedai-source-code" `
        --destination $RecoveryDir `
        --auth-mode login `
        2>$null

    # Verify critical files
    Write-Host ""
    Write-Host "🔍 Verifying critical files..." -ForegroundColor Yellow
    
    $criticalFiles = @{
        "NAKEDai_LIFE_Integration_System.py" = "NAKEDai L.I.F.E. Integration System"
        "experimentP2L.I.F.E-Learning-Individually-from-Experience-Theory-Algorithm-Code-2025-Copyright-Se.py" = "L.I.F.E. Algorithm Core"
    }

    foreach ($file in $criticalFiles.GetEnumerator()) {
        if (Test-Path "$RecoveryDir\$($file.Key)") {
            Write-Host "✅ $($file.Value) recovered" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $($file.Value) not found" -ForegroundColor Yellow
        }
    }

    # List recovered files
    Write-Host ""
    Write-Host "📋 Recovered files:" -ForegroundColor Cyan
    Get-ChildItem $RecoveryDir | Format-Table Name, Length, LastWriteTime -AutoSize

    # Success message
    Write-Host ""
    Write-Host "🎉 NAKEDai L.I.F.E. Recovery Complete!" -ForegroundColor Green -BackgroundColor Black
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "🔥 Revolutionary System Features:" -ForegroundColor Magenta
    Write-Host "   • 45 TOPS Snapdragon X Elite processor" -ForegroundColor White
    Write-Host "   • Dual independent 4K OLED displays" -ForegroundColor White
    Write-Host "   • 24 EEG + 8 photonic sensors" -ForegroundColor White
    Write-Host "   • Venturi dual cooling + neural boost" -ForegroundColor White
    Write-Host "   • Sub-millisecond processing" -ForegroundColor White
    Write-Host "   • 98-99% neural accuracy" -ForegroundColor White
    Write-Host "   • 120g weight, 16+ hour battery" -ForegroundColor White
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "🌍 Ready to change the world! 🚀" -ForegroundColor Green -BackgroundColor Black
    Write-Host ""
    Write-Host "📁 Files recovered to: $RecoveryDir" -ForegroundColor Yellow
    Write-Host "🎯 Change directory: cd $RecoveryDir" -ForegroundColor Yellow
    Write-Host "🔥 Run integration: python NAKEDai_LIFE_Integration_System.py" -ForegroundColor Yellow

} catch {
    Write-Host "❌ Recovery error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Please ensure you're logged into Azure CLI: az login" -ForegroundColor Yellow
    Write-Host "💡 Verify storage account name and permissions" -ForegroundColor Yellow
}