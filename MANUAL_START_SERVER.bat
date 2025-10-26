@echo off
echo ========================================
echo 🧠 L.I.F.E PLATFORM - MANUAL START
echo ========================================
echo.

echo [1] Checking Python...
python --version

echo.
echo [2] Installing Flask...
python -m pip install flask

echo.
echo [3] Starting server manually...
echo.
echo Server will be available at: http://127.0.0.1:5000
echo.
echo IMPORTANT: Leave this window open to keep the server running!
echo           Open a web browser to: http://127.0.0.1:5000
echo           Test endpoints:
echo           • http://127.0.0.1:5000/api/health
echo           • http://127.0.0.1:5000/api/health_simple
echo.
echo Press Ctrl+C to stop the server
echo.

python simple_life_server.py