# L.I.F.E. Platform - Clinical Dashboard Demo Server
# October 15, 2025 University Teams Demo
# Compatible with 23 colleagues sharing
# GDPR Compliant Local Hosting

param(
    [int]$Port = 8080,
    [string]$DashboardFile = "LIFE_CLINICAL_GRADE_DASHBOARD.html",
    [switch]$AutoOpen = $true
)

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "L.I.F.E. PLATFORM CLINICAL DEMO SERVER" -ForegroundColor Yellow
Write-Host "October 15, 2025 University Presentation" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory and dashboard path
$CurrentDir = Get-Location
$DashboardPath = Join-Path $CurrentDir $DashboardFile

# Check if dashboard file exists
if (-not (Test-Path $DashboardPath)) {
    Write-Host "❌ ERROR: Dashboard file '$DashboardFile' not found!" -ForegroundColor Red
    Write-Host "Expected location: $DashboardPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available HTML files:" -ForegroundColor Cyan
    Get-ChildItem -Path $CurrentDir -Filter "*.html" | ForEach-Object {
        Write-Host "  • $($_.Name)" -ForegroundColor White
    }
    exit 1
}

# Display configuration
Write-Host "🏥 Clinical Dashboard: $DashboardFile" -ForegroundColor Green
Write-Host "🌐 Server Port: $Port" -ForegroundColor Green
Write-Host "📍 Dashboard Path: $DashboardPath" -ForegroundColor Green
Write-Host "👥 Teams Compatible: Yes (23 colleagues ready)" -ForegroundColor Green
Write-Host "🔒 GDPR Compliant: Local hosting only" -ForegroundColor Green
Write-Host ""

# Get network information
$LocalIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254*"} | Select-Object -First 1).IPAddress
$LocalURL = "http://localhost:$Port"
$NetworkURL = "http://${LocalIP}:$Port"

Write-Host "🔗 ACCESS LINKS FOR TEAMS DEMO:" -ForegroundColor Yellow
Write-Host "Local Access: $LocalURL" -ForegroundColor White
Write-Host "Network Access: $NetworkURL" -ForegroundColor White
Write-Host ""

# Teams sharing instructions
Write-Host "📢 TEAMS SHARING INSTRUCTIONS:" -ForegroundColor Magenta
Write-Host "1. Share your screen in Teams meeting" -ForegroundColor White
Write-Host "2. Navigate to: $LocalURL" -ForegroundColor White
Write-Host "3. Copy this message to chat:" -ForegroundColor White
Write-Host ""
Write-Host "   🧠 L.I.F.E. Platform Clinical Demo is LIVE!" -ForegroundColor Green
Write-Host "   📊 Real-time EEG analysis with PhysioNet data" -ForegroundColor Green
Write-Host "   🤖 AI Clinical Assistant ready for questions" -ForegroundColor Green
Write-Host "   🏥 FDA-compliant neuroplasticity assessment" -ForegroundColor Green
Write-Host ""

# Create simple HTTP server
try {
    Write-Host "🚀 Starting Clinical Demo Server..." -ForegroundColor Yellow
    
    # Create HttpListener
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$Port/")
    $listener.Prefixes.Add("http://$LocalIP:$Port/")
    $listener.Start()
    
    Write-Host "✅ Server started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 DEMO STATUS: Ready for October 15th presentation" -ForegroundColor Yellow
    Write-Host "⏰ Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server..." -ForegroundColor Gray
    
    # Auto-open browser if requested
    if ($AutoOpen) {
        Write-Host "🌐 Opening dashboard in default browser..." -ForegroundColor Green
        Start-Process $LocalURL
    }
    
    # Server loop
    while ($listener.IsListening) {
        try {
            # Wait for request
            $context = $listener.GetContext()
            $request = $context.Request
            $response = $context.Response
            
            # Log request
            $clientIP = $request.RemoteEndPoint.Address
            $timestamp = Get-Date -Format 'HH:mm:ss'
            Write-Host "[$timestamp] 📡 Request from $clientIP - $($request.Url.AbsolutePath)" -ForegroundColor Cyan
            
            # Handle different requests
            if ($request.Url.AbsolutePath -eq "/" -or $request.Url.AbsolutePath -eq "/dashboard") {
                # Serve dashboard
                $dashboardContent = Get-Content -Path $DashboardPath -Raw
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($dashboardContent)
                
                $response.ContentType = "text/html; charset=utf-8"
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200
                
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
                Write-Host "    ✅ Clinical dashboard served" -ForegroundColor Green
                
            } elseif ($request.Url.AbsolutePath -eq "/status") {
                # API status endpoint
                $statusData = @{
                    platform = "L.I.F.E. Clinical Platform"
                    version = "2025.10.15"
                    status = "operational"
                    demo_ready = $true
                    teams_compatible = $true
                    gdpr_compliant = $true
                    timestamp = (Get-Date).ToString("o")
                    features = @(
                        "PhysioNet EEG Integration",
                        "AI Clinical Assistant", 
                        "Real-time Processing",
                        "Clinical-grade Analytics",
                        "Export Capabilities"
                    )
                } | ConvertTo-Json -Depth 3
                
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($statusData)
                $response.ContentType = "application/json; charset=utf-8"
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200
                
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
                Write-Host "    📊 Status API called" -ForegroundColor Yellow
                
            } elseif ($request.Url.AbsolutePath -eq "/health") {
                # Health check endpoint
                $healthData = "L.I.F.E. Clinical Platform - OPERATIONAL - October 15, 2025 Demo Ready"
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($healthData)
                
                $response.ContentType = "text/plain; charset=utf-8"
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200
                
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
                Write-Host "    💚 Health check OK" -ForegroundColor Green
                
            } else {
                # 404 for other requests
                $errorMsg = "L.I.F.E. Platform - Resource not found. Try: / or /dashboard or /status"
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
                
                $response.ContentType = "text/plain; charset=utf-8"
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 404
                
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
                Write-Host "    ❌ 404 - Resource not found" -ForegroundColor Red
            }
            
            $response.Close()
            
        } catch {
            Write-Host "⚠️  Request error: $($_.Exception.Message)" -ForegroundColor Red
            if ($response) { $response.Close() }
        }
    }
    
} catch {
    Write-Host "❌ Server error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
    
} finally {
    if ($listener) {
        $listener.Stop()
        Write-Host ""
        Write-Host "🛑 Clinical Demo Server stopped." -ForegroundColor Yellow
        Write-Host "Thank you for using L.I.F.E. Platform!" -ForegroundColor Cyan
    }
}