@echo off
REM INSTANT L.I.F.E. DEMO LAUNCHER - October 15, 2025
REM Works with your E: drive dashboard file

title L.I.F.E. Demo - INSTANT LAUNCH
color 0B

echo.
echo ============================================
echo   🧠 L.I.F.E. PLATFORM - INSTANT DEMO 🚀
echo   October 15, 2025 - Teams Ready!
echo ============================================
echo.

REM Your specific dashboard path from the file URL you showed
set E_DRIVE_DASHBOARD=E:\THE L.I.F.E Theory Algorithm\L.I.F.E Theory Evolution\L.I.F.E. Platform - Core Algorithm Dashboard.html

echo [CHECK] Looking for your L.I.F.E. dashboard...

if exist "%E_DRIVE_DASHBOARD%" (
    echo [SUCCESS] ✅ Found your dashboard on E: drive!
    echo [FILE] L.I.F.E. Platform - Core Algorithm Dashboard.html
    echo.
    echo [LAUNCH] Opening in your default browser...
    echo [TEAMS] Ready for screen sharing with 23 colleagues!
    echo.
    echo 🌐 Dashboard URL: file:///%E_DRIVE_DASHBOARD%
    echo 📅 Demo Date: October 15, 2025 (2 days to go!)
    echo 👥 Teams Compatible: YES ✅
    echo.
    
    REM Open the file directly in browser
    start "" "%E_DRIVE_DASHBOARD%"
    
    echo [OPENED] Dashboard launched in browser!
    echo.
    echo 📢 TEAMS DEMO INSTRUCTIONS:
    echo 1. Join your Teams meeting
    echo 2. Click "Share Screen"  
    echo 3. Select the browser window with L.I.F.E. dashboard
    echo 4. Your 23 colleagues can now see the demo!
    echo.
    echo 💡 DEMO TIPS:
    echo - Test AI assistant responses
    echo - Show PhysioNet data integration
    echo - Demonstrate export features
    echo - Highlight clinical-grade metrics
    echo.
    pause
) else (
    echo [ERROR] ❌ Dashboard not found at expected location
    echo [PATH] Expected: %E_DRIVE_DASHBOARD%
    echo.
    echo 💡 SOLUTIONS:
    echo 1. Check if E: drive is accessible
    echo 2. Verify the file path is correct
    echo 3. Try the Python launcher: python launch_life_demo.py
    echo 4. Move dashboard to current directory
    echo.
    
    echo [SEARCH] Looking for HTML files in current directory...
    dir *.html /b 2>nul
    if errorlevel 1 (
        echo No HTML files found in current directory.
    )
    echo.
    pause
)

echo.
echo 🎉 L.I.F.E. Platform Demo Ready!
echo Thank you for choosing L.I.F.E. for your presentation!
pause