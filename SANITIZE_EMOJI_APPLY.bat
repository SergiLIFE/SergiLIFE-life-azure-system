@echo off
echo Apply emoji sanitization (content only)
echo =======================================
setlocal
set PY=python
if exist "%~dp0venv\Scripts\python.exe" set PY="%~dp0venv\Scripts\python.exe"
cd /d "%~dp0"
%PY% tools\emoji_sanitizer.py --write
echo.
echo Done.
endlocal
