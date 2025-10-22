@echo off
echo.
echo ========================================
echo   L.I.F.E. Platform - Health Check Test
echo ========================================
echo.
echo Testing: https://life-functions-app.azurewebsites.net/api/health
echo.
echo Please wait...
echo.

python test_deployment.py

echo.
echo ========================================
echo If you see "SUCCESS" above, the health
echo endpoint is working correctly!
echo ========================================
echo.
pause
