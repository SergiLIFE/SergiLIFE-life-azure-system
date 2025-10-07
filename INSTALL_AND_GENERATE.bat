@echo off
REM Install Pillow and Generate Visuals - All in One!

echo.
echo ============================================================
echo STEP 1: Installing Pillow (Image Library)
echo ============================================================
echo.

pip install Pillow

if errorlevel 1 (
    echo.
    echo ❌ Installation failed. Trying with --user flag...
    pip install --user Pillow
)

echo.
echo ============================================================
echo STEP 2: Generating Visuals
echo ============================================================
echo.

python generate_visuals_standalone.py

echo.
echo ============================================================
echo ALL DONE!
echo ============================================================
echo.
pause
