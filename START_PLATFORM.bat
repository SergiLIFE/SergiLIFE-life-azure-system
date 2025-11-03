
@echo off
REM ============================================================================
REM L.I.F.E PLATFORM INTEGRATED LAUNCHER
REM October 17, 2025 - Ready to Run
REM ============================================================================
REM 
REM This batch file starts BOTH the backend server AND opens the browser
REM No complex setup - just run this!
REM

echo.
echo ============================================================================
echo 🧠 L.I.F.E PLATFORM - REAL ALGORITHM INTEGRATION
echo ============================================================================
echo.
echo This will start:
echo   1. Backend server on http://localhost:5000
echo   2. HTTP server on http://localhost:8080
echo   3. Browser opening LIFE_AI_PLATFORM_REAL.html
echo.
echo Keep both terminal windows open while using the platform!
echo.
pause

REM Install dependencies silently
echo Installing dependencies...
pip install -q flask flask-cors numpy 2>nul
echo.

REM Create a new terminal window for backend
echo Starting backend server in new window...
start "L.I.F.E Backend Server" cmd /k "python life_backend_server.py"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Create another terminal window for HTTP server
echo Starting HTTP server in new window...
start "L.I.F.E HTTP Server" cmd /k "python -m http.server 8080"

REM Wait for HTTP server to start
timeout /t 2 /nobreak

REM Open browser
echo Opening LIFE_AI_PLATFORM_REAL.html in browser...
timeout /t 1 /nobreak
start http://localhost:8080/LIFE_AI_PLATFORM_REAL.html

echo.
echo ============================================================================
echo ✅ STARTED SUCCESSFULLY!
echo ============================================================================
echo.
echo 🟢 If you see GREEN status in the browser header:
echo    "🟢 Real Algorithm (Backend Connected)"
echo    ...then everything is working!
echo.
echo 🔴 If you see YELLOW status:
echo    "🟡 Simulated Data (Backend Not Available)"
echo    ...the backend window may have crashed. Check the terminal.
echo.
echo 🎯 TO USE:
echo    1. Wait for browser to load
echo    2. Go to "EEG AI Integration" tab
echo    3. Click "Process EEG AI Integration"
echo    4. See real algorithm results!
echo.
echo 💡 Keep both terminal windows open. Close them to stop the platform.
echo.
echo ============================================================================
pause
