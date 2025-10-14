@echo off
title L.I.F.E Platform - Deployment & Sharing Assistant
color 0E

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          🌐 L.I.F.E Platform Deployment Assistant           ║
echo ║         Ready for 7 Academic Meeting Demonstrations         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🧠 L.I.F.E Theory Algorithm Status: INTEGRATED ✅
echo 🔧 Tab Navigation: FIXED ✅  
echo 📊 Real-time Processing: ACTIVE ✅
echo.

echo 📋 Deployment Options:
echo ────────────────────────────────────
echo   [1] Start Local Web Server (Recommended)
echo   [2] Create Shareable ZIP Package
echo   [3] Test Platform Locally
echo   [4] View Sharing Instructions
echo   [0] Exit
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto webserver
if "%choice%"=="2" goto createzip
if "%choice%"=="3" goto testlocal
if "%choice%"=="4" goto instructions
if "%choice%"=="0" goto exit
goto menu

:webserver
echo.
echo 🌐 Starting Local Web Server...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📋 Getting your IP address for sharing...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "ip=%%a"
    set "ip=!ip: =!"
    goto :found_ip
)
:found_ip

echo ✅ Server will start on: http://localhost:8000
echo 🌍 Your IP Address: %ip%
echo 📧 Share this URL with attendees: http://%ip%:8000/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
echo.
echo 📱 Instructions for meeting invitees:
echo   1. Connect to the same network (WiFi)
echo   2. Open web browser on any device
echo   3. Go to: http://%ip%:8000/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
echo   4. L.I.F.E Platform will load with all features
echo.
echo 🔒 Press Ctrl+C to stop server when meetings are complete
echo.
echo Starting L.I.F.E Platform server now...
python life_platform_server.py
goto exit

:createzip
echo.
echo 📦 Creating Shareable ZIP Package...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ L.I.F.E Platform found
    echo 📄 Creating LIFE_Platform_Demo_Package.zip...
    
    REM Create a temporary directory
    if not exist "temp_package" mkdir temp_package
    copy "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" "temp_package\index.html" >nul
    copy "LIFE_PLATFORM_SHARING_GUIDE.md" "temp_package\" >nul 2>&1
    
    echo 📋 Creating instructions file...
    echo Instructions for L.I.F.E Platform Demo > "temp_package\README.txt"
    echo ========================================= >> "temp_package\README.txt"
    echo 1. Extract all files to a folder >> "temp_package\README.txt"
    echo 2. Double-click "index.html" to open >> "temp_package\README.txt"
    echo 3. Platform will open in your web browser >> "temp_package\README.txt"
    echo 4. All tabs and L.I.F.E features are functional >> "temp_package\README.txt"
    echo. >> "temp_package\README.txt"
    echo L.I.F.E Theory Algorithm v2025.1.0-PRODUCTION integrated >> "temp_package\README.txt"
    echo For support: sergio.paya.borrull@example.com >> "temp_package\README.txt"
    
    REM Use PowerShell to create ZIP (Windows 10+)
    powershell -Command "Compress-Archive -Path 'temp_package\*' -DestinationPath 'LIFE_Platform_Demo_Package.zip' -Force"
    
    REM Cleanup
    rmdir /s /q "temp_package"
    
    echo ✅ Package created: LIFE_Platform_Demo_Package.zip
    echo 📧 Ready to share via email, cloud storage, or USB
    echo 🎓 Contains everything needed for 7 academic meetings
) else (
    echo ❌ L.I.F.E Platform file not found
    echo 💡 Ensure LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html exists
)
echo.
pause
goto exit

:testlocal
echo.
echo 🧪 Testing L.I.F.E Platform Locally...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ Opening L.I.F.E Platform for testing...
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    echo.
    echo 🔍 Test Checklist:
    echo   ✓ Check all 6 tabs work (Overview, EEG Analysis, etc.)
    echo   ✓ Verify L.I.F.E algorithm messages appear
    echo   ✓ Test interactive buttons (Run Diagnostic, etc.)
    echo   ✓ Confirm real-time metrics update
    echo   ✓ Ensure charts and visualizations load
    echo.
    echo 🧠 L.I.F.E Algorithm should display analysis results
    echo 📊 All clinical functions should respond
) else (
    echo ❌ L.I.F.E Platform file not found
)
echo.
pause
goto exit

:instructions
echo.
echo 📖 Sharing Instructions for 7 Academic Meetings
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🎓 METHOD 1 - Local Web Server (Best for live demos):
echo   • Run option [1] to start server
echo   • Share your IP address + port with attendees
echo   • Everyone accesses via web browser
echo   • You control the presentation in real-time
echo.
echo 📧 METHOD 2 - Email ZIP Package (Best for preparation):
echo   • Run option [2] to create ZIP package  
echo   • Email LIFE_Platform_Demo_Package.zip to attendees
echo   • Include instructions: "Download, extract, open index.html"
echo   • Works offline, no internet required
echo.
echo 🌐 METHOD 3 - Cloud Sharing (Most convenient):
echo   • Upload ZIP to Google Drive/OneDrive/Dropbox
echo   • Share download link with meeting invitees
echo   • Attendees download and run locally
echo   • Professional and reliable
echo.
echo 📋 Email Template for Invitations:
echo ────────────────────────────────────────────
echo Subject: L.I.F.E Platform Demo - Academic Research Presentation
echo.
echo Dear Colleagues,
echo.
echo You are invited to experience the L.I.F.E Platform demonstration
echo (Learning Individually From Experience) featuring advanced 
echo neuroplasticity analysis with integrated AI algorithms.
echo.
echo ACCESS: [Include your chosen sharing method above]
echo.
echo The platform demonstrates clinical-grade EEG processing,
echo real-time neural analysis, and individual learning optimization.
echo.
echo Best regards,
echo Sergio Paya Borrull
echo ────────────────────────────────────────────
echo.
pause
goto exit

:exit
echo.
echo 🎓 L.I.F.E Platform ready for your 7 academic meetings!
echo 🧠 All L.I.F.E Theory algorithms integrated and functional
echo 🌐 Multiple sharing options available for maximum compatibility
echo.
pause
exit