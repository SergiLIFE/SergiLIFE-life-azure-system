@echo off
echo ======================================================================
echo L.I.F.E Platform Screenshot Generator
echo Creating 1280x720 screenshot for Azure Marketplace
echo ======================================================================
echo.

cd /d "%~dp0"

".venv\Scripts\python.exe" create_screenshot_simple.py

echo.
echo ======================================================================
echo DONE! Check for LIFE_Platform_Screenshot_1280x720.png
echo ======================================================================
echo.
pause
