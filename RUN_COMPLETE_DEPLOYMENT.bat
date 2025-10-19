@echo off
echo ============================================================
echo  L.I.F.E PLATFORM - COMPLETE DEPLOYMENT WORKFLOW
echo ============================================================
echo.
echo This will:
echo   1. Configure Function App settings
echo   2. Validate all Azure resources  
echo   3. Prepare for code deployment
echo.
echo ============================================================
echo.

python COMPLETE_DEPLOYMENT_WORKFLOW.py

echo.
echo ============================================================
echo Workflow completed. Check logs folder for details.
echo ============================================================
pause
