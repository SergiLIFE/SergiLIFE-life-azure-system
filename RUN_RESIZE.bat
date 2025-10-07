@echo off
echo Running Python script directly...
echo.

cd /d "%~dp0"

REM Run with full path to Python
"C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system\.venv\Scripts\python.exe" resize_azure_diagram.py

echo.
echo Done!
echo.
pause
