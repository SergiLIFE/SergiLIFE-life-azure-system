@echo off
REM ================================================================
REM L.I.F.E. PLATFORM - MICROSOFT CLOUD BACKUP SCRIPT
REM Backs up to both GitHub and OneDrive
REM ================================================================

echo.
echo ========================================================
echo   L.I.F.E. PLATFORM MICROSOFT CLOUD BACKUP
echo ========================================================
echo.

cd /d C:\Users\SergiPaya\SergiLIFE-life-azure-system

REM Step 1: Commit to Git
echo [1/4] Committing changes to Git...
git add -A
git commit -m "Auto-backup: %DATE% %TIME%"

REM Step 2: Push to GitHub (Microsoft)
echo.
echo [2/4] Pushing to GitHub (Microsoft Cloud)...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo ✓ Successfully backed up to GitHub
) else (
    echo ✗ GitHub push failed - please check connection
)

REM Step 3: Copy to OneDrive (if available)
echo.
echo [3/4] Checking OneDrive backup location...
if exist "%UserProfile%\OneDrive" (
    echo ✓ OneDrive detected
    set ONEDRIVE_BACKUP=%UserProfile%\OneDrive\LIFE-Platform-Backup
    
    if not exist "!ONEDRIVE_BACKUP!" mkdir "!ONEDRIVE_BACKUP!"
    
    echo Copying critical files to OneDrive...
    xcopy /Y /Q algorithms\python-core\experimentP2L_REPAIRED.py "!ONEDRIVE_BACKUP!\"
    xcopy /Y /Q documentation\LIFE_14_EQUATION_SYSTEM_COMPLETE.md "!ONEDRIVE_BACKUP!\"
    xcopy /Y /Q EMERGENCY_BACKUP_STRATEGY.md "!ONEDRIVE_BACKUP!\"
    
    echo ✓ Critical files backed up to OneDrive
) else (
    echo ⚠ OneDrive not detected - skipping
)

REM Step 4: Create recovery point
echo.
echo [4/4] Creating recovery point...
git tag backup-%DATE:~-4%-%DATE:~-7,2%-%DATE:~-10,2%-%TIME:~0,2%%TIME:~3,2%
git push origin --tags

echo.
echo ========================================================
echo   BACKUP COMPLETE
echo ========================================================
echo.
echo Your work is now protected in:
echo   ✓ GitHub Repository (Microsoft Cloud)
echo   ✓ Git Tags (Recovery Points)
if exist "%UserProfile%\OneDrive" (
    echo   ✓ OneDrive (Microsoft Cloud)
)
echo.
echo Latest commit: 
git log -1 --oneline
echo.
echo Press any key to exit...
pause >nul
