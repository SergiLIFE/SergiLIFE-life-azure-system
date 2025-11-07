@echo off
echo ========================================
echo   L.I.F.E. Platform - Complete Setup
echo   Copyright 2025 - Sergio Paya Borrull
echo ========================================
echo.

echo Step 1: Checking available drives...
wmic logicaldisk get caption,size,freespace /format:table

echo.
echo Step 2: Creating F: drive development structure...
if not exist "F:\" (
    echo ERROR: F: drive not found!
    echo Available alternatives:
    echo - Use current directory: %CD%
    echo - Use D: drive if available
    echo - Use external drive
    pause
    exit /b 1
)

mkdir "F:\LIFE-Platform-Development" 2>nul
mkdir "F:\LIFE-Platform-Development\Source-Code" 2>nul
mkdir "F:\LIFE-Platform-Development\Tools" 2>nul
mkdir "F:\LIFE-Platform-Development\Azure-Deployments" 2>nul
mkdir "F:\LIFE-Platform-Development\Documentation" 2>nul
mkdir "F:\LIFE-Platform-Development\OneDrive-Sync" 2>nul

echo Directory structure created successfully!

echo.
echo Step 3: Downloading Bicep CLI...
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/Azure/bicep/releases/latest/download/bicep-win-x64.exe' -OutFile 'F:\LIFE-Platform-Development\Tools\bicep.exe' -UseBasicParsing; Write-Host 'Bicep downloaded successfully!' } catch { Write-Host 'Download failed - please download manually from: https://github.com/Azure/bicep/releases/latest/download/bicep-win-x64.exe' }"

echo.
echo Step 4: Copying L.I.F.E. project files...
xcopy "%~dp0*" "F:\LIFE-Platform-Development\Source-Code\" /E /H /C /I /Y

echo.
echo Step 5: Verifying setup...
dir "F:\LIFE-Platform-Development" /B
echo.
dir "F:\LIFE-Platform-Development\Source-Code" /B | findstr /I "algorithm\|azure\|life"

echo.
echo Step 6: Testing Bicep installation...
"F:\LIFE-Platform-Development\Tools\bicep.exe" --version 2>nul
if %errorlevel% neq 0 (
    echo Bicep installation needs verification
) else (
    echo Bicep is ready!
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Your L.I.F.E. Platform is now ready at:
echo F:\LIFE-Platform-Development\
echo.
echo Next steps:
echo 1. Navigate to: F:\LIFE-Platform-Development\Source-Code
echo 2. Install Python dependencies: pip install -r requirements.txt
echo 3. Run validation: python ULTIMATE_FULL_CYCLE_ECOSYSTEM_TEST.py
echo 4. Setup OneDrive sync for automatic backup
echo.
echo Complete documentation: F:\LIFE-Platform-Development\L.I.F.E-COMPLETE-SETUP-GUIDE.md
echo.
pause