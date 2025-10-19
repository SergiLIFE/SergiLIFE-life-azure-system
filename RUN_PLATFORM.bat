@echo off
REM ============================================================================
REM L.I.F.E PLATFORM STARTER - WORKING VERSION
REM October 17, 2025
REM ============================================================================

setlocal enabledelayedexpansion

cls
echo.
echo ============================================================================
echo 🧠 L.I.F.E PLATFORM STARTER
echo ============================================================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Current directory: %cd%
echo.

REM Step 1: Install dependencies
echo Step 1: Installing Python dependencies...
echo Command: pip install -q flask flask-cors numpy
pip install -q flask flask-cors numpy
if errorlevel 1 (
    echo ⚠️  Warning: Some packages may not have installed. Continuing anyway...
)
echo ✅ Dependencies checked
echo.

REM Step 2: Check if backend file exists
if not exist "life_backend_server.py" (
    echo ❌ ERROR: life_backend_server.py not found in %cd%
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)
echo ✅ Found life_backend_server.py
echo.

REM Step 3: Start backend in background
echo Step 2: Starting L.I.F.E Backend Server on http://localhost:5000...
echo.
start "L.I.F.E Backend - Close this window to stop" cmd /k ^
    "cd /d "%SCRIPT_DIR%" && echo Starting backend... && python life_backend_server.py"

REM Wait for backend to fully start
echo ⏳ Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak
echo.

REM Step 4: Start HTTP server
echo Step 3: Starting HTTP Server on http://localhost:8080...
echo Command: python -m http.server 8080
echo.
start "L.I.F.E HTTP Server - Close this window to stop" cmd /k ^
    "cd /d "%SCRIPT_DIR%" && echo Starting HTTP server on port 8080... && python -m http.server 8080"

REM Wait for HTTP server to start
echo ⏳ Waiting for HTTP server to start (3 seconds)...
timeout /t 3 /nobreak
echo.

REM Step 5: Open browser
echo Step 4: Opening browser...
echo URL: http://localhost:8080/LIFE_AI_PLATFORM_REAL.html
echo.
timeout /t 1 /nobreak
start http://localhost:8080/LIFE_AI_PLATFORM_REAL.html

REM Final instructions
echo.
echo ============================================================================
echo ✅ PLATFORM STARTED!
echo ============================================================================
echo.
echo 👀 Check the browser for:
echo    1. Status indicator in header (top right)
echo    2. Should show: 🟢 Real Algorithm (Backend Connected)
echo    3. If YELLOW 🟡: Backend is loading, wait a few seconds
echo    4. If YELLOW stays: Click "EEG AI Integration" tab anyway
echo.
echo 🎯 To test:
echo    1. Click: "EEG AI Integration" tab
echo    2. Click: "Process EEG AI Integration" button
echo    3. Wait 2-5 seconds for results
echo    4. See real algorithm output!
echo.
echo 🚀 Two terminal windows opened:
echo    - "L.I.F.E Backend" - Backend server (do NOT close)
echo    - "L.I.F.E HTTP Server" - File server (do NOT close)
echo.
echo ⏹️  To stop everything: Close both terminal windows
echo.
echo ============================================================================
echo.

REM Keep this window open
echo Press any key to close this window...
echo (But keep the two server windows open!)
echo.
pause
