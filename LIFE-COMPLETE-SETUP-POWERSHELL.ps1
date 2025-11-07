# L.I.F.E. Platform - Complete Development Environment Setup
# Copyright 2025 - Sergio Paya Borrull
# Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   L.I.F.E. Platform - Complete Setup" -ForegroundColor Yellow
Write-Host "   Neuroadaptive Learning Platform" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check system information
Write-Host "Step 1: System Analysis..." -ForegroundColor Yellow
Write-Host "Available Drives:" -ForegroundColor White
Get-PSDrive -PSProvider FileSystem | Format-Table Name, @{Name = "Used(GB)"; Expression = { [math]::Round($_.Used / 1GB, 2) } }, @{Name = "Free(GB)"; Expression = { [math]::Round($_.Free / 1GB, 2) } }

$CurrentPath = Get-Location
Write-Host "Current Location: $CurrentPath" -ForegroundColor White
Write-Host ""

# Step 2: Determine best drive for development
$TargetDrive = $null
$DrivesToCheck = @("F:", "D:", "E:", "G:")

foreach ($Drive in $DrivesToCheck) {
    if (Test-Path $Drive) {
        $DriveInfo = Get-PSDrive ($Drive.Replace(":", ""))
        $FreeSpaceGB = [math]::Round($DriveInfo.Free / 1GB, 2)
        Write-Host "Drive $Drive available with $FreeSpaceGB GB free" -ForegroundColor Green
        if ($FreeSpaceGB -gt 50) {
            # Need at least 50GB for development
            $TargetDrive = $Drive
            break
        }
    }
}

if (-not $TargetDrive) {
    Write-Host "No suitable drive found with 50GB+ free space" -ForegroundColor Red
    Write-Host "Using current directory instead: $CurrentPath" -ForegroundColor Yellow
    $TargetPath = Join-Path $CurrentPath "LIFE-Platform-Development"
}
else {
    $TargetPath = "$TargetDrive\LIFE-Platform-Development"
    Write-Host "Selected target: $TargetPath" -ForegroundColor Green
}

Write-Host ""

# Step 3: Create directory structure
Write-Host "Step 2: Creating Development Structure..." -ForegroundColor Yellow
$Directories = @(
    $TargetPath,
    "$TargetPath\Source-Code",
    "$TargetPath\Tools",
    "$TargetPath\Azure-Deployments", 
    "$TargetPath\Documentation",
    "$TargetPath\OneDrive-Sync",
    "$TargetPath\Results",
    "$TargetPath\Logs"
)

foreach ($Dir in $Directories) {
    try {
        New-Item -ItemType Directory -Path $Dir -Force -ErrorAction Stop | Out-Null
        Write-Host "✓ Created: $Dir" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to create: $Dir - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Step 4: Download Bicep CLI
Write-Host "Step 3: Downloading Bicep CLI..." -ForegroundColor Yellow
$BicepPath = "$TargetPath\Tools\bicep.exe"
$BicepUrl = "https://github.com/Azure/bicep/releases/latest/download/bicep-win-x64.exe"

try {
    Write-Host "Downloading from: $BicepUrl" -ForegroundColor White
    Invoke-WebRequest -Uri $BicepUrl -OutFile $BicepPath -UseBasicParsing -ErrorAction Stop
    Write-Host "✓ Bicep CLI downloaded successfully!" -ForegroundColor Green
    
    # Test Bicep
    $BicepVersion = & $BicepPath --version 2>$null
    if ($BicepVersion) {
        Write-Host "✓ Bicep version: $BicepVersion" -ForegroundColor Green
    }
}
catch {
    Write-Host "✗ Failed to download Bicep: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Manual download: $BicepUrl" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Copy source files
Write-Host "Step 4: Copying L.I.F.E. Platform Files..." -ForegroundColor Yellow
$SourcePath = $CurrentPath.Path
$DestinationPath = "$TargetPath\Source-Code"

try {
    # Copy all files from current directory
    Copy-Item -Path "$SourcePath\*" -Destination $DestinationPath -Recurse -Force -ErrorAction Continue
    Write-Host "✓ Source files copied to: $DestinationPath" -ForegroundColor Green
    
    # Verify key files exist
    $KeyFiles = @(
        "requirements.txt",
        "ULTIMATE_FULL_CYCLE_ECOSYSTEM_TEST.py",
        "algorithms",
        "azure_functions"
    )
    
    foreach ($File in $KeyFiles) {
        $FilePath = Join-Path $DestinationPath $File
        if (Test-Path $FilePath) {
            Write-Host "✓ Verified: $File" -ForegroundColor Green
        }
        else {
            Write-Host "⚠ Missing: $File" -ForegroundColor Yellow
        }
    }
    
}
catch {
    Write-Host "✗ Error copying files: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Step 6: Create quick access files
Write-Host "Step 5: Creating Quick Access Files..." -ForegroundColor Yellow

# Create quick start batch file
$QuickStartContent = @"
@echo off
cd /d "$DestinationPath"
echo L.I.F.E. Platform Development Environment
echo ========================================
echo Location: %CD%
echo.
echo Quick commands:
echo   run_tests.bat     - Run all tests
echo   start_platform.bat - Launch platform
echo   azure_deploy.bat  - Deploy to Azure
echo.
cmd /k
"@

$QuickStartPath = "$TargetPath\L.I.F.E-Quick-Start.bat"
$QuickStartContent | Out-File -FilePath $QuickStartPath -Encoding ASCII
Write-Host "✓ Quick start: $QuickStartPath" -ForegroundColor Green

# Create documentation index
$DocsIndexContent = @"
# L.I.F.E. Platform - Documentation Index

## Quick Reference
- **Setup Guide**: L.I.F.E-COMPLETE-SETUP-GUIDE.md
- **Architecture**: Source-Code\.github\copilot-instructions.md  
- **Azure Marketplace**: Source-Code\AZURE_MARKETPLACE_INTEGRATION_GUIDE.md
- **Security**: Source-Code\LIFE_SECURITY_README.md

## Development
- **Source Code**: Source-Code\
- **Tools**: Tools\bicep.exe
- **Deployments**: Azure-Deployments\
- **Results**: Results\
- **Logs**: Logs\

## Testing
- Run all tests: ``python ULTIMATE_FULL_CYCLE_ECOSYSTEM_TEST.py``
- Neural validation: ``python -c "from algorithms.python_core.experimentP2L_REPAIRED import LIFEAlgorithm; import asyncio; life=LIFEAlgorithm(); asyncio.run(life.run_100_cycle_eeg_test())"``
- Azure connectivity: ``python algorithms\python-core\FLAWLESS_CONNECTION_VALIDATOR.py``

## Quick Start
1. Open: L.I.F.E-Quick-Start.bat
2. Navigate to Source-Code directory
3. Install dependencies: ``pip install -r requirements.txt``
4. Run validation tests
5. Deploy to Azure using Bicep templates

*L.I.F.E. Platform - Learning Individually from Experience*
*Copyright 2025 - Sergio Paya Borrull*
"@

$DocsIndexPath = "$TargetPath\Documentation\README.md"
$DocsIndexContent | Out-File -FilePath $DocsIndexPath -Encoding UTF8
Write-Host "✓ Documentation index: $DocsIndexPath" -ForegroundColor Green

Write-Host ""

# Step 7: Final verification
Write-Host "Step 6: Final Verification..." -ForegroundColor Yellow
Write-Host "Development Environment Summary:" -ForegroundColor White
Write-Host "================================" -ForegroundColor White
Write-Host "Location: $TargetPath" -ForegroundColor Cyan
Write-Host ""

# Check directory structure
if (Test-Path $TargetPath) {
    $DirSize = (Get-ChildItem -Path $TargetPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $DirSizeMB = [math]::Round($DirSize / 1MB, 2)
    Write-Host "✓ Total size: $DirSizeMB MB" -ForegroundColor Green
    
    Write-Host "Directory structure:" -ForegroundColor White
    Get-ChildItem -Path $TargetPath -Directory | ForEach-Object {
        $ItemCount = (Get-ChildItem -Path $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "  ✓ $($_.Name) ($ItemCount items)" -ForegroundColor Green
    }
}
else {
    Write-Host "✗ Setup verification failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   L.I.F.E. Platform Setup Complete!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your neuroadaptive learning platform is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open: $TargetPath\L.I.F.E-Quick-Start.bat" -ForegroundColor White
Write-Host "2. Navigate to Source-Code directory" -ForegroundColor White  
Write-Host "3. Install Python dependencies" -ForegroundColor White
Write-Host "4. Run comprehensive validation" -ForegroundColor White
Write-Host "5. Deploy to Azure using Bicep CLI" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: $TargetPath\Documentation\" -ForegroundColor Cyan
Write-Host "Quick Start: $TargetPath\L.I.F.E-Quick-Start.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open the development environment..." -ForegroundColor Yellow
Read-Host

# Open the development environment
if (Test-Path $TargetPath) {
    explorer $TargetPath
    if (Test-Path "$TargetPath\L.I.F.E-Quick-Start.bat") {
        Start-Process -FilePath "$TargetPath\L.I.F.E-Quick-Start.bat"
    }
}