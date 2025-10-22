@echo off
echo ========================================
echo 🧠 L.I.F.E PLATFORM - LOCAL DASHBOARD
echo ========================================
echo.

echo 🚀 Opening L.I.F.E Platform endpoints in browser...
echo.

echo Opening main platform...
start http://localhost:5000

timeout /t 2 /nobreak >nul

echo Opening health endpoints...
start http://localhost:5000/api/health
start http://localhost:5000/api/health_simple

timeout /t 2 /nobreak >nul

echo Opening EEG processor...
start http://localhost:5000/api/eeg_processor

timeout /t 2 /nobreak >nul

echo Opening platform info...
start http://localhost:5000/api/platform_info

echo.
echo ✅ L.I.F.E Platform dashboard opened!
echo.
echo 🎯 All endpoints now accessible locally:
echo    • Main Platform: http://localhost:5000
echo    • Health Check: http://localhost:5000/api/health  
echo    • Simple Health: http://localhost:5000/api/health_simple
echo    • EEG Processor: http://localhost:5000/api/eeg_processor
echo    • Platform Info: http://localhost:5000/api/platform_info
echo.
echo 📝 Note: Local development mode active
echo    Azure Functions deployment pending authorization
echo.
pause