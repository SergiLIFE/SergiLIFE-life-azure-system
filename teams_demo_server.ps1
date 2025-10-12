# L.I.F.E. Platform - Teams-Optimized GDPR Demo Server
# October 15, 2025 University Demo - 23 Colleagues
# Optimized for Microsoft Teams screen sharing and browser access

Write-Host "=============================================" -ForegroundColor Green
Write-Host "L.I.F.E. PLATFORM - TEAMS DEMO SERVER" -ForegroundColor Cyan
Write-Host "Microsoft Teams + GDPR-Compliant Demo" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Get multiple IP addresses for Teams flexibility
$wifiIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Wi-Fi*" | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
$ethernetIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Ethernet*" | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress

$localIP = if ($wifiIP) { $wifiIP } elseif ($ethernetIP) { $ethernetIP } else { "localhost" }

Write-Host "🎓 Starting Teams-Optimized L.I.F.E. Dashboard..." -ForegroundColor Green
Write-Host ""
Write-Host "📺 TEAMS SHARING OPTIONS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Option 1 - Screen Share Dashboard:" -ForegroundColor White
Write-Host "   🔗 http://localhost:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "   Option 2 - Colleagues Access Directly:" -ForegroundColor White
Write-Host "   🔗 http://$localIP:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "💡 TEAMS DEMO STRATEGIES:" -ForegroundColor Yellow
Write-Host "   ✅ Share screen with dashboard open (localhost link)" -ForegroundColor White
Write-Host "   ✅ Share direct link in Teams chat (network IP)" -ForegroundColor White
Write-Host "   ✅ Both options work simultaneously" -ForegroundColor White
Write-Host "   ✅ Attendees can follow along on own devices" -ForegroundColor White
Write-Host ""
Write-Host "🔒 GDPR COMPLIANCE:" -ForegroundColor Green
Write-Host "   ✅ NO personal data collection" -ForegroundColor White
Write-Host "   ✅ NO Teams recording interference" -ForegroundColor White
Write-Host "   ✅ NO cookies or tracking" -ForegroundColor White  
Write-Host "   ✅ Academic use only" -ForegroundColor White
Write-Host ""
Write-Host "📋 TEAMS CHAT MESSAGE (Copy & Paste):" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "🧠 L.I.F.E. Platform Live Demo" -ForegroundColor White
Write-Host "Access: http://$localIP:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html" -ForegroundColor White
Write-Host "GDPR Compliant • No Data Collection • Academic Only" -ForegroundColor Gray
Write-Host "=============================================" -ForegroundColor Gray
Write-Host ""
Write-Host "📱 Press Ctrl+C to stop server" -ForegroundColor Yellow
Write-Host "🎯 Ready for Teams demo with 23 colleagues!" -ForegroundColor Green
Write-Host ""

# Check if dashboard file exists
if (-not (Test-Path "LIFE_CORE_ALGORITHM_DASHBOARD.html")) {
    Write-Host "❌ Dashboard file not found!" -ForegroundColor Red
    Write-Host "Please ensure LIFE_CORE_ALGORITHM_DASHBOARD.html is in the current directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Start Python HTTP server with Teams-friendly settings
try {
    # Open browser automatically for screen sharing
    Start-Process "http://localhost:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html"
    Write-Host "🌐 Dashboard opened for Teams screen sharing" -ForegroundColor Green
    Write-Host ""
    
    # Start server
    python -m http.server 8000 --bind 0.0.0.0
} catch {
    Write-Host "❌ Error starting server. Please ensure Python is installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

Write-Host ""
Write-Host "🛑 Server stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"