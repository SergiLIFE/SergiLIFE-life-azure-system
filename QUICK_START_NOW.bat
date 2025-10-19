@echo off
REM 🚀 QUICK START - L.I.F.E Platform (October 18, 2025)
REM This script starts BOTH servers and opens the browser

setlocal enabledelayedexpansion

cd /d "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  🚀 L.I.F.E PLATFORM - QUICK START                     ║
echo ║  Starting Backend + HTTP Server + Browser              ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Install dependencies silently
echo [1/4] Installing dependencies...
pip install flask flask-cors numpy -q >nul 2>&1

echo [2/4] Starting Backend Server on :5000...
start "🧠 L.I.F.E Backend Server" cmd /k "python life_backend_server.py"

REM Wait for backend to start
timeout /t 3 /nobreak

echo [3/4] Starting HTTP Server on :8080...
start "🌐 HTTP Server :8080" cmd /k "python -m http.server 8080"

REM Wait for HTTP to start
timeout /t 2 /nobreak

echo [4/4] Opening browser...
start "" http://localhost:8080/LIFE_AI_PLATFORM_REAL.html

echo.
echo ✅ Both servers started!
echo.
echo 📍 Browser: http://localhost:8080/LIFE_AI_PLATFORM_REAL.html
echo 🧠 Backend: http://localhost:5000
echo.
echo ⏳ Waiting for page to load (5 seconds)...
timeout /t 5 /nobreak

echo.
echo 🎯 NEXT STEPS:
echo   1. Close any "ML Model Creation Wizard" popup
echo   2. Click "EEG AI Integration" tab
echo   3. Click "Process EEG AI Integration" button
echo   4. Wait 2-5 seconds for REAL algorithm results
echo.
echo ✨ If you see "REAL_ALGORITHM" → SUCCESS! ✨
echo.

pause
