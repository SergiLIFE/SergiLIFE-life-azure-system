@echo off
REM Quick Validation for L.I.F.E Platform Deployment

cls
echo.
echo ================================================================================
echo      L.I.F.E PLATFORM - QUICK VALIDATION CHECK
echo ================================================================================
echo.

echo Running validation script...
echo.

python validate_deployment.py --environment staging

if errorlevel 1 (
    echo.
    echo [FAIL] Validation encountered errors
    echo Check the logs folder for details
) else (
    echo.
    echo [PASS] Validation successful!
)

echo.
echo Check results in the 'results' folder
echo Check logs in the 'logs' folder
echo.
pause
