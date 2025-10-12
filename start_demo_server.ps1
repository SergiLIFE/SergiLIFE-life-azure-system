# L.I.F.E. Platform - GDPR-Compliant Demo Server
# October 15, 2025 University Demo - 23 Colleagues
# Academic use only - No data collection

Write-Host "=============================================" -ForegroundColor Green
Write-Host "L.I.F.E. PLATFORM - UNIVERSITY DEMO SERVER" -ForegroundColor Cyan
Write-Host "GDPR-Compliant Academic Demonstration" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Get local IP address
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress

if (-not $localIP) {
    $localIP = "localhost"
    Write-Host "⚠️  Could not detect network IP, using localhost" -ForegroundColor Yellow
}

Write-Host "🎓 Starting L.I.F.E. Dashboard Server..." -ForegroundColor Green
Write-Host "📧 Share this link with your colleagues:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   🔗 http://$localIP:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "🔒 GDPR COMPLIANCE:" -ForegroundColor Green
Write-Host "   ✅ NO personal data collection" -ForegroundColor White
Write-Host "   ✅ NO cookies or tracking" -ForegroundColor White  
Write-Host "   ✅ NO analytics systems" -ForegroundColor White
Write-Host "   ✅ Academic use only" -ForegroundColor White
Write-Host ""
Write-Host "📱 Press Ctrl+C to stop server" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Check if dashboard file exists
if (-not (Test-Path "LIFE_CORE_ALGORITHM_DASHBOARD.html")) {
    Write-Host "❌ Dashboard file not found!" -ForegroundColor Red
    Write-Host "Please ensure LIFE_CORE_ALGORITHM_DASHBOARD.html is in the current directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Start Python HTTP server
try {
    python -m http.server 8000
} catch {
    Write-Host "❌ Error starting server. Please ensure Python is installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

Write-Host ""
Write-Host "🛑 Server stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"