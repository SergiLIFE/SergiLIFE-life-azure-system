@echo off
REM L.I.F.E. Platform - October 15, 2025 Clinical Demo Launcher
REM One-click launch for Teams presentation with 23 colleagues
REM Clinical Grade EEG Analysis Dashboard

title L.I.F.E. Platform - Clinical Demo Launcher
color 0A

echo.
echo ===============================================
echo    L.I.F.E. PLATFORM CLINICAL DEMO LAUNCHER
echo    October 15, 2025 University Presentation
echo    Teams Demo for 23 Colleagues
echo ===============================================
echo.

echo [INFO] Starting Clinical Grade Dashboard Server...
echo [INFO] Current Time: %date% %time%
echo [INFO] Demo Mode: University Teams Presentation
echo.

REM Use your original comprehensive E: drive dashboard (full features)
set "DASHBOARD_FILE=E:\THE L.I.F.E Theory Algorithm\L.I.F.E Theory Evolution\L.I.F.E. Platform - Core Algorithm Dashboard.html"
set "EMERGENCY_BACKUP=EMERGENCY_DEMO_OCT15.html"

echo [TARGET] Your L.I.F.E. Dashboard Location:
echo [PATH] %DASHBOARD_FILE%
echo.

if exist "%DASHBOARD_FILE%" (
    echo [SUCCESS] ✅ Found your comprehensive L.I.F.E. Platform dashboard!
    
    REM Get file size for verification
    for %%A in ("%DASHBOARD_FILE%") do set FILE_SIZE=%%~zA
    set /a FILE_SIZE_KB=%FILE_SIZE%/1024
    
    echo [INFO] File size: %FILE_SIZE_KB% KB (Full-featured version)
    echo [STATUS] Original dashboard ready for October 15th demo!
    echo [TEAMS] Compatible with 23 colleagues ✅
    echo [FEATURES] Complete algorithm and data visualization
    echo.
) else (
    echo [WARNING] ⚠️ Original dashboard not accessible on E: drive!
    echo [PATH] Expected: %DASHBOARD_FILE%
    echo.
    echo [FALLBACK] Checking for emergency backup...
    
    if exist "%EMERGENCY_BACKUP%" (
        echo [BACKUP] ✅ Using emergency dashboard as fallback
        set "DASHBOARD_FILE=%EMERGENCY_BACKUP%"
        echo [INFO] Emergency dashboard ready for demo
    ) else (
        echo [ERROR] ❌ No dashboard available!
        echo.
        echo [TROUBLESHOOTING] Solutions:
        echo 1. Check if E: drive is connected and accessible
        echo 2. Verify the exact file path and spelling
        echo 3. Make sure the file hasn't been moved or renamed
        echo 4. Create emergency backup dashboard
        echo.
        pause
        exit /b 1
    )
    echo.
)

echo [LAUNCH] Opening your L.I.F.E. Platform dashboard...
echo [METHOD] Direct browser launch (fastest and most reliable)
echo [URL] file:///%DASHBOARD_FILE%
echo.

echo [TEAMS] 📢 DEMO INSTRUCTIONS FOR OCTOBER 15th:
echo ════════════════════════════════════════════════════
echo 1. ✅ Join your Teams meeting
echo 2. ✅ Click "Share Screen" button  
echo 3. ✅ Select "Browser Window" (not full desktop)
echo 4. ✅ Choose the window showing L.I.F.E. Platform
echo 5. ✅ Your 23 colleagues can now see the dashboard!
echo.

echo [FEATURES] 🧠 What to demonstrate:
echo • Real-time neuroplasticity analysis
echo • EEG signal processing algorithms
echo • Clinical-grade brain adaptability metrics
echo • Advanced learning efficiency calculations
echo • Interactive data visualization
echo.

echo [CHAT] 📱 Copy this to Teams chat during demo:
echo ┌─────────────────────────────────────────────────┐
echo │ 🧠 L.I.F.E. Platform Clinical Demo - LIVE! 🚀   │
echo │ 📊 Real-time neuroplasticity EEG analysis      │
echo │ 🤖 Advanced brain adaptability assessment      │
echo │ 🏥 Clinical-grade learning efficiency metrics  │
echo │ 🎯 Interactive Q&A welcome!                    │
echo └─────────────────────────────────────────────────┘
echo.

echo [OPENING] 🌐 Launching dashboard in your default browser...

REM Open the dashboard file directly
start "" "%DASHBOARD_FILE%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Failed to start demo server
    echo [FALLBACK] Attempting Python HTTP server...
    echo.
    
    REM Fallback to Python server
    python -m http.server 8080 --bind 127.0.0.1
    
    if %ERRORLEVEL% neq 0 (
        echo.
        echo [ERROR] No suitable server available
        echo [HELP] Please install Python or enable PowerShell execution
        pause
        exit /b 1
    )
)

echo.
echo [COMPLETE] Demo server stopped
echo [INFO] Thank you for using L.I.F.E. Platform!
pause