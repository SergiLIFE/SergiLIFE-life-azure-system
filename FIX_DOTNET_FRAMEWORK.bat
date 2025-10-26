@echo off
REM 🔧 .NET Framework Repair Script for Bitdefender VPN
REM October 26, 2025 - Fixes Microsoft .NET Framework corruption

echo ========================================
echo .NET Framework Repair Utility
echo ========================================

echo Step 1: Checking .NET Framework versions...
dir /b "%windir%\Microsoft.NET\Framework\v*"

echo.
echo Step 2: Stopping Bitdefender services...
net stop "Bitdefender VPN Service" /y 2>nul
net stop "Bitdefender Agent WatchDog Service" /y 2>nul

echo.
echo Step 3: Clearing .NET temporary files...
del /s /f /q "%WINDIR%\Microsoft.NET\Framework64\v*\Temporary ASP.NET Files\*.*" 2>nul
del /s /f /q "%WINDIR%\Microsoft.NET\Framework\v*\Temporary ASP.NET Files\*.*" 2>nul
echo Temporary files cleared.

echo.
echo Step 4: Running System File Checker...
sfc /scannow

echo.
echo Step 5: Repairing Windows Image...
dism /online /cleanup-image /restorehealth

echo.
echo Step 6: Clearing Windows Update cache...
net stop wuauserv
del /f /s /q %windir%\SoftwareDistribution\*.*
net start wuauserv

echo.
echo Step 7: Restarting Bitdefender services...
net start "Bitdefender Agent WatchDog Service"
net start "Bitdefender VPN Service"

echo.
echo ========================================
echo .NET Framework repair completed!
echo Please restart your computer to complete the repair.
echo ========================================
pause