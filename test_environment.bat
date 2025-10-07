@echo off
REM L.I.F.E. Platform Environment Validation
REM Run this batch file to test the development environment
REM Copyright 2025 - Sergio Paya Borrull

echo ================================================================================
echo L.I.F.E. Platform - Development Environment Test
echo October 7th Launch Readiness Validation
echo ================================================================================
echo.

echo [1/4] Testing Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found or not working
    goto :error
)
echo ✅ Python installation verified
echo.

echo [2/4] Testing core dependencies...
python -c "import numpy, pandas, scipy, sklearn, tensorflow, torch; print('✅ Core ML/AI libraries working')"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Core dependencies failed
    goto :error
)
echo.

echo [3/4] Testing Azure integration...
python -c "import azure.identity, azure.storage.blob, azure.functions; print('✅ Azure SDK integration working')"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Azure integration failed
    goto :error
)
echo.

echo [4/4] Running full L.I.F.E. Platform validation...
python validate_environment.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: L.I.F.E. Platform validation failed
    goto :error
)
echo.

echo ================================================================================
echo 🎉 SUCCESS: L.I.F.E. Platform Development Environment Ready!
echo 🚀 October 7th Launch: All systems operational
echo ================================================================================
echo.
echo Next steps:
echo - Run L.I.F.E. components: python autonomous_optimizer.py
echo - Run tests: python -m pytest -v --tb=short
echo - Deploy to Azure: azd up
echo.
pause
goto :end

:error
echo.
echo ================================================================================
echo ❌ ERROR: Development environment issues detected
echo ================================================================================
echo.
echo Troubleshooting:
echo 1. Check Python installation: python --version
echo 2. Reinstall dependencies: pip install -r requirements.txt
echo 3. Review DEVELOPMENT_ENVIRONMENT_RESOLUTION_GUIDE.md
echo.
pause

:end