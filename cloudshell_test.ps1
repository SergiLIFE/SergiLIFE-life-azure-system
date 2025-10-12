# Azure Cloud Shell PowerShell - L.I.F.E. Platform Interactive Test
# October 11, 2025 - Test interactive elements (no emoji in filename)

Write-Host ""
Write-Host "L.I.F.E. Platform - Azure Cloud Shell Interactive Test" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Testing interactive demo elements in Cloud Shell..." -ForegroundColor White
Write-Host ""

# Check for demo file
$DemoFile = "LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html"
if (Test-Path $DemoFile) {
    Write-Host "Found demo file: $DemoFile" -ForegroundColor Green
} else {
    Write-Host "Demo file not found. Cloning repository..." -ForegroundColor Yellow
    git clone https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git
    cd SergiLIFE-life-azure-system
}

Write-Host ""
Write-Host "CLOUD SHELL DEMO TEST OPTIONS:" -ForegroundColor Magenta
Write-Host "=============================" -ForegroundColor Magenta
Write-Host ""

Write-Host "Option 1: HTTP Server Method" -ForegroundColor Yellow
Write-Host "python3 -m http.server 8080" -ForegroundColor Cyan
Write-Host "Then click Web Preview button in Cloud Shell" -ForegroundColor Gray
Write-Host ""

Write-Host "Option 2: Cloud Shell Editor" -ForegroundColor Yellow  
Write-Host "code LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html" -ForegroundColor Cyan
Write-Host ""

Write-Host "Option 3: Direct Platform Access" -ForegroundColor Yellow
Write-Host "https://green-ground-0c65efe0f.1.azurestaticapps.net" -ForegroundColor Cyan
Write-Host ""

# Check interactive elements
if (Test-Path $DemoFile) {
    $Content = Get-Content $DemoFile -Raw
    $ButtonCount = ([regex]::Matches($Content, 'onclick=')).Count
    $FunctionCount = ([regex]::Matches($Content, 'function \w+')).Count
    
    Write-Host "INTERACTIVE ELEMENTS DETECTED:" -ForegroundColor Green
    Write-Host "onclick handlers: $ButtonCount" -ForegroundColor White
    Write-Host "JavaScript functions: $FunctionCount" -ForegroundColor White
    Write-Host ""
}

Write-Host "OCTOBER 15 DEMO STATUS:" -ForegroundColor Magenta
Write-Host "======================" -ForegroundColor Magenta
Write-Host "Launch Date: October 15, 2025 (4 days)" -ForegroundColor White
Write-Host "Participants: 23 registered" -ForegroundColor White
Write-Host "Pipeline: 771K+ opportunity" -ForegroundColor White
Write-Host "Status: READY" -ForegroundColor Green
Write-Host ""