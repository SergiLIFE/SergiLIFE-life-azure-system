@echo off
REM Generate L.I.F.E Platform Logo
REM Requires Python with Pillow installed

echo ====================================
echo L.I.F.E Platform Logo Generator
echo ====================================
echo.

REM Check if virtual environment exists
if exist .venv\Scripts\python.exe (
    echo Using virtual environment...
    .venv\Scripts\python.exe create_logo.py
) else (
    echo Using system Python...
    python create_logo.py
)

echo.
echo Done! Check marketplace_assets folder
pause
