@echo off
echo =============================================
echo L.I.F.E. PLATFORM - UNIVERSITY DEMO SERVER
echo GDPR-Compliant Academic Demonstration
echo October 15, 2025 - 23 University Colleagues  
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if dashboard file exists
if not exist "LIFE_CORE_ALGORITHM_DASHBOARD.html" (
    echo ❌ Dashboard file not found in current directory
    echo Please ensure LIFE_CORE_ALGORITHM_DASHBOARD.html is present
    pause
    exit /b 1
)

echo ✅ Starting GDPR-compliant dashboard server...
echo 📧 Share the provided links with your colleagues
echo 🔒 No personal data collection - Academic use only
echo.

python dashboard_server.py

echo.
echo 🛑 Server stopped
pause