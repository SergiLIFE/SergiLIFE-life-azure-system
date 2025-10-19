@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  L.I.F.E PLATFORM - SIMPLE STARTER                            ║
echo ║  This will open everything you need                            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -q flask flask-cors numpy 2>nul

echo.
echo Starting backend server in new window...
start "L.I.F.E Backend" cmd /k "python life_backend_server.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo Starting HTTP server in new window...
start "L.I.F.E HTTP" cmd /k "python -m http.server 8080"

echo Waiting for HTTP server to start...
timeout /t 3 /nobreak

echo.
echo Opening platform in browser...
timeout /t 1 /nobreak
start http://localhost:8080/LIFE_AI_PLATFORM_REAL.html

echo.
echo ✅ STARTED!
echo.
echo Keep the two cmd windows open.
echo Look for 🟢 GREEN status in browser header.
echo Click "EEG AI Integration" tab and test!
echo.
pause
