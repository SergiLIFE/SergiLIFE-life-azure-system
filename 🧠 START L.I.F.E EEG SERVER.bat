@echo off
title L.I.F.E AI EEG Processing Server
cls

echo.
echo ================================================================
echo  🧠 L.I.F.E AI EEG PROCESSING SERVER
echo ================================================================
echo  Strategic Partnership Ready - October 15, 2025
echo  Real Flask Backend for EEG File Processing
echo ================================================================
echo.

echo 🚀 Starting L.I.F.E AI EEG Processing Server...
echo.

REM Check if the server file exists
if not exist "life_eeg_server.py" (
    echo ❌ ERROR: life_eeg_server.py not found!
    echo Please ensure you're running this from the correct directory.
    pause
    exit /b 1
)

echo ✅ Server file located: life_eeg_server.py
echo ✅ Flask backend with L.I.F.E AI algorithms ready
echo.

echo 📡 Server Features:
echo    • Real EEG file upload processing
echo    • L.I.F.E neuroplasticity analysis
echo    • Brainwave pattern recognition
echo    • AI-powered insights and recommendations
echo    • Support for EDF, CSV, BDF, TXT, DAT formats
echo.

echo 🌐 Starting Flask server on http://localhost:5000...
echo    API Endpoints:
echo    • POST /api/upload-eeg - Upload EEG files
echo    • POST /api/process-eeg - Process with L.I.F.E algorithms
echo    • GET /api/status - Server status
echo.

echo 💡 TIP: Keep this server running while using the L.I.F.E AI Platform
echo      for full server-backend EEG processing capabilities!
echo.

REM Start the Flask server
python life_eeg_server.py

echo.
echo Server stopped. Press any key to exit...
pause >nul