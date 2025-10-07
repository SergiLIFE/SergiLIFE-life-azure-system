@echo off
echo ======================================================================
echo L.I.F.E Platform - Architecture Diagram Converter
echo Converting your Azure diagram to 1280x720 for Partner Center
echo ======================================================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. Save your "Azurecycle.png" diagram to this folder:
echo    %~dp0
echo.
echo 2. Then run this batch file again
echo.
echo ======================================================================
echo.

cd /d "%~dp0"

REM Check if file exists
if not exist "Azurecycle.png" (
    echo ❌ Azurecycle.png not found in current folder
    echo.
    echo Please copy the file here and try again.
    echo.
    pause
    exit /b 1
)

echo ✅ Found Azurecycle.png
echo.
echo Converting to 1280x720...
echo.

".venv\Scripts\python.exe" resize_azure_diagram.py

echo.
echo ======================================================================
if exist "LIFE_Platform_Architecture_Screenshot_1280x720.png" (
    echo ✅ SUCCESS! Screenshot created!
    echo.
    echo File: LIFE_Platform_Architecture_Screenshot_1280x720.png
    echo Size: 1280x720 pixels
    echo.
    echo 🎯 Ready to upload to Partner Center!
) else (
    echo ❌ Something went wrong. Check for errors above.
)
echo ======================================================================
echo.
pause
