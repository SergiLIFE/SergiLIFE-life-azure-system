@echo off
echo ========================================
echo L.I.F.E PLATFORM - LOCAL DEVELOPMENT
echo ========================================
echo.

echo Installing Flask for local development...
pip install -r requirements_local.txt

echo.
echo Starting L.I.F.E Platform Local Server...
echo.
echo 🧠 L.I.F.E Platform will be available at:
echo    http://localhost:5000
echo.
echo 📋 Available endpoints:
echo    • http://localhost:5000/api/health
echo    • http://localhost:5000/api/health_simple  
echo    • http://localhost:5000/api/eeg_processor
echo    • http://localhost:5000/api/platform_info
echo.
echo ⏳ Azure Functions deployment pending authorization...
echo.

python local_life_server.py

pause