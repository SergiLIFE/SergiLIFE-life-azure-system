@echo off
echo L.I.F.E Repo Emoji Sanitizer
echo ============================
echo.
setlocal
set PY=python

if exist "%~dp0venv\Scripts\python.exe" (
  set PY="%~dp0venv\Scripts\python.exe"
)

cd /d "%~dp0"

%PY% tools\emoji_sanitizer.py --dry-run
echo.
echo Review the dry-run summary above.
echo.
choice /M "Apply changes now (write)?"
if errorlevel 2 goto :eof

%PY% tools\emoji_sanitizer.py --write
echo.
echo Done.
endlocal
