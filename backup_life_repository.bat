@echo off
REM ========================================
REM L.I.F.E. Repository Protection System
REM Automated Backup & Corruption Prevention
REM ========================================

set REPO_PATH=c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system
set DESKTOP_BACKUP=C:\Users\%USERNAME%\Desktop\LIFE_Repository_Backups
set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo ===== L.I.F.E. Repository Protection System =====
echo Starting backup process at %date% %time%

REM Create backup directory structure
echo Creating backup directories...
if not exist "%DESKTOP_BACKUP%" mkdir "%DESKTOP_BACKUP%"
if not exist "%DESKTOP_BACKUP%\daily" mkdir "%DESKTOP_BACKUP%\daily"
if not exist "%DESKTOP_BACKUP%\weekly" mkdir "%DESKTOP_BACKUP%\weekly"
if not exist "%DESKTOP_BACKUP%\git_bundles" mkdir "%DESKTOP_BACKUP%\git_bundles"
if not exist "%DESKTOP_BACKUP%\health_reports" mkdir "%DESKTOP_BACKUP%\health_reports"

cd /d "%REPO_PATH%"

REM Health check before backup
echo Running pre-backup health check...
git fsck --full > "%DESKTOP_BACKUP%\health_reports\health_%TIMESTAMP%.txt" 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: Repository health issues detected!
    echo Check %DESKTOP_BACKUP%\health_reports\health_%TIMESTAMP%.txt
)

REM Create git bundle (complete repository backup)
echo Creating git bundle backup...
git bundle create "%DESKTOP_BACKUP%\git_bundles\life_repo_%TIMESTAMP%.bundle" --all
if %ERRORLEVEL% eq 0 (
    echo ✅ Git bundle created successfully
) else (
    echo ❌ Git bundle creation failed
)

REM Create file system backup (excluding large/temp files)
echo Creating file system backup...
robocopy "%REPO_PATH%" "%DESKTOP_BACKUP%\daily\life_repo_%TIMESTAMP%" /MIR /XD ".git\objects\tmp" "__pycache__" ".mypy_cache" ".venv" "node_modules" /XF "*.tmp" "*.log" "thumbcache*" /R:3 /W:5 /NFL /NDL /NP

REM Keep only last 7 daily backups and 4 weekly backups
echo Cleaning old backups...
forfiles /p "%DESKTOP_BACKUP%\daily" /m life_repo_* /d -7 /c "cmd /c rmdir /s /q @path" 2>nul
forfiles /p "%DESKTOP_BACKUP%\git_bundles" /m *.bundle /d -28 /c "cmd /c del /q @path" 2>nul

REM Create backup summary
echo Creating backup summary...
echo Backup completed at %date% %time% > "%DESKTOP_BACKUP%\last_backup.txt"
echo Repository path: %REPO_PATH% >> "%DESKTOP_BACKUP%\last_backup.txt"
echo Bundle location: %DESKTOP_BACKUP%\git_bundles\life_repo_%TIMESTAMP%.bundle >> "%DESKTOP_BACKUP%\last_backup.txt"
echo Files location: %DESKTOP_BACKUP%\daily\life_repo_%TIMESTAMP% >> "%DESKTOP_BACKUP%\last_backup.txt"

echo.
echo ===== Backup Complete =====
echo Desktop backup location: %DESKTOP_BACKUP%
echo Latest bundle: life_repo_%TIMESTAMP%.bundle
echo.
echo To restore from bundle: git clone [bundle_path] [new_folder]
echo To verify backup: run verify_backups.bat