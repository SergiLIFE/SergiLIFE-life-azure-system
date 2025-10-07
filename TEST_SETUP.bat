@echo off
echo ======================================================================
echo Testing Batch File Execution
echo ======================================================================
echo.
echo Current directory: %CD%
echo.
echo Batch file location: %~dp0
echo.
echo Checking for files:
echo.

cd /d "%~dp0"

echo Looking for Azurecycle.png...
if exist "Azurecycle.png" (
    echo ✅ Found Azurecycle.png
) else (
    echo ❌ NOT FOUND: Azurecycle.png
    echo.
    echo Please place Azurecycle.png in this folder:
    echo %CD%
)

echo.
echo Checking Python...
if exist ".venv\Scripts\python.exe" (
    echo ✅ Found Python: .venv\Scripts\python.exe
) else (
    echo ❌ NOT FOUND: .venv\Scripts\python.exe
)

echo.
echo Checking Pillow...
".venv\Scripts\python.exe" -c "import PIL; print('✅ Pillow is installed')" 2>nul || echo ❌ Pillow not installed

echo.
echo ======================================================================
echo.
pause
