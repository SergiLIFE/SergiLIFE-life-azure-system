@echo off
echo ========================================
echo 🧠 L.I.F.E PLATFORM - SIMPLE SERVER START
echo ========================================
echo.

echo Installing Flask if needed...
python -m pip install flask

echo.
echo Starting L.I.F.E Platform Simple Server...
echo.
echo The server will start on: http://127.0.0.1:5000
echo Available endpoints:
echo   • http://127.0.0.1:5000/
echo   • http://127.0.0.1:5000/api/health
echo   • http://127.0.0.1:5000/api/health_simple
echo.
echo Press Ctrl+C to stop the server when done testing
echo.

python simple_life_server.py

pause