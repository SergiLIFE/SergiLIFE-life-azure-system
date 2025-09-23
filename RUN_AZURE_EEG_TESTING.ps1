# L.I.F.E. Azure EEG Testing with Azure Account Integration
# Sergio Paya Borrull - lifecoach121.com
# Azure Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb

Write-Host ""
Write-Host "==================================================================================" -ForegroundColor Cyan
Write-Host "🧠 L.I.F.E. AZURE EEG TESTING - EXECUTING WITH YOUR AZURE ACCOUNT 🧠" -ForegroundColor Yellow
Write-Host "==================================================================================" -ForegroundColor Cyan
Write-Host "⚡ Tenant: lifecoach121.com" -ForegroundColor Green
Write-Host "⚡ Azure Account: Sergio Paya Borrull" -ForegroundColor Green
Write-Host "⚡ Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb" -ForegroundColor Green
Write-Host "==================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Azure CLI authentication
Write-Host "🔐 Checking Azure authentication..." -ForegroundColor Yellow
try {
    $azAccount = az account show --output json 2>$null | ConvertFrom-Json
    if ($azAccount) {
        Write-Host "✅ Azure CLI authenticated as: $($azAccount.user.name)" -ForegroundColor Green
        Write-Host "✅ Current subscription: $($azAccount.name)" -ForegroundColor Green
        Write-Host "✅ Tenant: $($azAccount.tenantId)" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Azure CLI not authenticated. Run 'az login --tenant lifecoach121.com' to authenticate" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔍 Searching for Python installation..." -ForegroundColor Yellow

# Find Python executable
$pythonPaths = @(
    "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python3.13.exe",
    "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python*\python.exe",
    "C:\Python*\python.exe"
)

$pythonExe = $null
foreach ($path in $pythonPaths) {
    if ($path -like "*\**") {
        # Handle wildcard paths
        $resolved = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($resolved) {
            $pythonExe = $resolved.FullName
            break
        }
    } elseif (Test-Path $path) {
        $pythonExe = $path
        break
    }
}

if ($pythonExe) {
    Write-Host "✅ Found Python: $pythonExe" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Executing L.I.F.E. Azure EEG Testing..." -ForegroundColor Yellow
    Write-Host ""
    
    # Execute the Azure EEG testing
    & $pythonExe "EXECUTE_AZURE_EEG_TESTING.py"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "==================================================================================" -ForegroundColor Green
        Write-Host "✅ AZURE EEG TESTING COMPLETED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host "📊 Check azure_eeg_test_outputs/ directory for results" -ForegroundColor Cyan
        Write-Host "☁️ Azure integration ready for your lifecoach121.com tenant" -ForegroundColor Cyan
        Write-Host "🐙 GitHub integration prepared for SergiLIFE/SergiLIFE-life-azure-system" -ForegroundColor Cyan
        Write-Host "==================================================================================" -ForegroundColor Green
        
        # Show output directory contents
        if (Test-Path "azure_eeg_test_outputs") {
            Write-Host ""
            Write-Host "📁 Generated files:" -ForegroundColor Yellow
            Get-ChildItem -Path "azure_eeg_test_outputs" -Recurse | ForEach-Object {
                Write-Host "   $($_.FullName)" -ForegroundColor White
            }
        }
        
        # Offer to open results
        Write-Host ""
        $openResults = Read-Host "Would you like to open the results directory? (y/n)"
        if ($openResults -eq "y" -or $openResults -eq "Y") {
            if (Test-Path "azure_eeg_test_outputs") {
                Invoke-Item "azure_eeg_test_outputs"
            }
        }
        
    } else {
        Write-Host "❌ Azure EEG testing encountered an error. Exit code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "💡 Check the error messages above for details." -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ Python not found in expected locations." -ForegroundColor Red
    Write-Host "💡 Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   Or enable Python in Microsoft Store (Settings > Apps > App execution aliases)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")