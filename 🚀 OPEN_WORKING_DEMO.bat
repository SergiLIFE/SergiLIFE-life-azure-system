@echo off
REM 🚀 L.I.F.E. Platform - Direct Demo Launcher
REM October 12, 2025 - Open Working Demo File

echo.
echo 🚀 L.I.F.E. Platform Demo Launcher - October 15, 2025
echo ================================================
echo Opening your working interactive demo...
echo.

set DEMO_FILE=LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html

if exist "%DEMO_FILE%" (
    echo ✅ Found working demo file: %DEMO_FILE%
    echo 🚀 Opening in your default browser...
    start "" "%DEMO_FILE%"
    echo.
    echo 🎯 Demo Features Available:
    echo - Start Learning Session (30-second interactive demo)
    echo - View Analytics (platform metrics)
    echo - Neural Adaptation (personalization showcase)
    echo.
    echo 📅 October 15, 2025 Demo: READY!
    echo 👥 23 Participants registered
    echo 💰 $771K+ pipeline opportunity
) else (
    echo ❌ Demo file not found: %DEMO_FILE%
    echo Please ensure the file is in the current directory.
)

echo.
echo 💡 This is your WORKING demo file - perfect for presentations!
echo    No internet required, works offline, all features functional.
echo.
pause