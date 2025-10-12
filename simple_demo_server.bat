@echo off
REM L.I.F.E. Platform - Simple GDPR-Compliant Demo Server
REM October 15, 2025 University Demo - 23 Colleagues
REM No data collection, no cookies, academic use only

echo =============================================
echo L.I.F.E. PLATFORM - UNIVERSITY DEMO SERVER
echo GDPR-Compliant Academic Demonstration
echo =============================================
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set "ip=%%i"
    goto :found
)
:found
set ip=%ip: =%

echo 🎓 Starting L.I.F.E. Dashboard Server...
echo 📧 Share this link with your colleagues:
echo.
echo    🔗 http://%ip%:8000/LIFE_CORE_ALGORITHM_DASHBOARD.html
echo.
echo 🔒 GDPR COMPLIANCE:
echo    ✅ NO personal data collection
echo    ✅ NO cookies or tracking  
echo    ✅ NO analytics systems
echo    ✅ Academic use only
echo.
echo 📱 Press Ctrl+C to stop server
echo =============================================
echo.

REM Start simple Python HTTP server
python -m http.server 8000

echo.
echo 🛑 Server stopped
pause