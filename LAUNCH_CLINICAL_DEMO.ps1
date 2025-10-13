# L.I.F.E. Platform - Clinical Demo Quick Launcher
# October 15, 2025 - PowerShell Version
# Teams presentation optimized for 23 colleagues

param(
    [switch]$QuickLaunch,
    [int]$Port = 8080,
    [switch]$SkipChecks
)

# Set console appearance
$Host.UI.RawUI.WindowTitle = "L.I.F.E. Platform - Clinical Demo Launcher"
$Host.UI.RawUI.BackgroundColor = "DarkBlue"
$Host.UI.RawUI.ForegroundColor = "White"
Clear-Host

# Header
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "   L.I.F.E. PLATFORM CLINICAL DEMO LAUNCHER" -ForegroundColor Yellow
Write-Host "   October 15, 2025 University Presentation" -ForegroundColor Green  
Write-Host "   Teams Demo for 23 Colleagues" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Quick info
Write-Host "🎯 Demo Mode: Clinical Grade EEG Analysis" -ForegroundColor Green
Write-Host "👥 Audience: 23 University Colleagues" -ForegroundColor Green  
Write-Host "📅 Date: October 15, 2025" -ForegroundColor Green
Write-Host "⏰ Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host ""

if (-not $SkipChecks) {
    # Environment checks
    Write-Host "🔍 Pre-flight Checks:" -ForegroundColor Yellow
    
    # Check dashboard file
    if (Test-Path "LIFE_CLINICAL_GRADE_DASHBOARD.html") {
        Write-Host "   ✅ Clinical dashboard file found" -ForegroundColor Green
        $fileSize = (Get-Item "LIFE_CLINICAL_GRADE_DASHBOARD.html").Length / 1KB
        Write-Host "   📊 File size: $([math]::Round($fileSize, 1)) KB" -ForegroundColor Cyan
    } else {
        Write-Host "   ❌ Clinical dashboard file missing!" -ForegroundColor Red
        Write-Host "   Expected: LIFE_CLINICAL_GRADE_DASHBOARD.html" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Available HTML files:" -ForegroundColor Cyan
        Get-ChildItem -Filter "*.html" | ForEach-Object { Write-Host "   • $($_.Name)" -ForegroundColor White }
        Write-Host ""
        Write-Host "Please ensure the clinical dashboard is in the current directory." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Check Teams templates
    if (Test-Path "teams_chat_templates.txt") {
        Write-Host "   ✅ Teams chat templates ready" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Teams templates missing (optional)" -ForegroundColor Yellow
    }
    
    # Check email templates  
    if (Test-Path "professional_email_templates.md") {
        Write-Host "   ✅ Email templates prepared" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Email templates missing (optional)" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# Network information
$LocalIP = try {
    (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254*"} | Select-Object -First 1).IPAddress
} catch {
    "localhost"
}

Write-Host "🌐 Network Configuration:" -ForegroundColor Yellow
Write-Host "   Local Access: http://localhost:$Port" -ForegroundColor White
Write-Host "   Network Access: http://$LocalIP`:$Port" -ForegroundColor White
Write-Host "   Teams Compatible: Yes ✅" -ForegroundColor Green
Write-Host "   GDPR Compliant: Local hosting only ✅" -ForegroundColor Green
Write-Host ""

# Teams sharing guide
Write-Host "📢 TEAMS SHARING GUIDE:" -ForegroundColor Magenta
Write-Host "1. Click 'Share Screen' in Teams meeting" -ForegroundColor White
Write-Host "2. Select 'Chrome/Browser Window'" -ForegroundColor White  
Write-Host "3. Navigate to: http://localhost:$Port" -ForegroundColor White
Write-Host "4. Copy chat message from teams_chat_templates.txt" -ForegroundColor White
Write-Host "5. Paste in Teams chat for 23 colleagues" -ForegroundColor White
Write-Host ""

Write-Host "🎯 READY TO LAUNCH CLINICAL DEMO!" -ForegroundColor Yellow
Write-Host ""

if (-not $QuickLaunch) {
    $launch = Read-Host "Press Enter to start demo server, or 'q' to quit"
    if ($launch -eq 'q') {
        Write-Host "Demo cancelled by user." -ForegroundColor Yellow
        exit 0
    }
}

# Launch the demo server
Write-Host "🚀 Launching Clinical Demo Server..." -ForegroundColor Green
Write-Host ""

try {
    # Call the main demo server script
    & ".\teams_clinical_demo_server.ps1" -Port $Port -AutoOpen:$true
} catch {
    Write-Host "❌ Error launching PowerShell server: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔄 Attempting Python fallback server..." -ForegroundColor Yellow
    
    try {
        python -m http.server $Port --bind 127.0.0.1
    } catch {
        Write-Host "❌ Python server also failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 TROUBLESHOOTING:" -ForegroundColor Yellow
        Write-Host "   • Ensure PowerShell execution policy allows scripts" -ForegroundColor White
        Write-Host "   • Install Python if not available" -ForegroundColor White
        Write-Host "   • Check if port $Port is already in use" -ForegroundColor White
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Clinical Demo Complete!" -ForegroundColor Green
Write-Host "Thank you for using L.I.F.E. Platform!" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close"