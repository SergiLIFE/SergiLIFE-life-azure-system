@echo off
REM DOUBLE-CLICK THIS FILE - No Terminal Needed!
REM Generates logo and screenshot for Azure Marketplace

echo.
echo ============================================================
echo DOUBLE-CLICK SOLUTION - No Terminal Required!
echo ============================================================
echo.
echo Generating your marketplace visuals...
echo.

python generate_visuals_standalone.py

echo.
echo Done! Check the marketplace_assets folder.
echo.
pause
