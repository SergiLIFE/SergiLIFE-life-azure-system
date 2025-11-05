@echo off
REM Phase 3: Safe Deletion and Cleanup - Step 5
REM Windows batch equivalent of bash cleanup script

set REPO_PATH=.
set QUARANTINE=.cleanup\quarantine
set DELETED_LOG=.cleanup\logs\deleted-files.log

echo Starting cleanup process... > "%DELETED_LOG%"
set DELETED_COUNT=0
set ERROR_COUNT=0

echo [%date% %time%] Starting Phase 3 cleanup >> "%DELETED_LOG%"

REM Process auto-generated files
echo Processing auto-generated files...
for /f "usebackq delims=" %%f in (".cleanup\logs\auto_generated.txt") do (
    if exist "%%f" (
        REM Check if file is safe to delete (not in critical directories)
        echo %%f | findstr /v /i "\.git node_modules src config" >nul
        if not errorlevel 1 (
            move "%%f" ".cleanup\quarantine\auto-generated\" >nul 2>>"%DELETED_LOG%"
            if not errorlevel 1 (
                echo [%date% %time%] MOVED: %%f >> "%DELETED_LOG%"
                set /a DELETED_COUNT+=1
            ) else (
                echo [%date% %time%] ERROR moving %%f >> "%DELETED_LOG%"
                set /a ERROR_COUNT+=1
            )
        ) else (
            echo [%date% %time%] SKIPPED (critical path): %%f >> "%DELETED_LOG%"
        )
    ) else (
        echo [%date% %time%] FILE NOT FOUND: %%f >> "%DELETED_LOG%"
    )
)

echo [%date% %time%] Phase 3 Complete: Moved %DELETED_COUNT% files, %ERROR_COUNT% errors >> "%DELETED_LOG%"
echo Cleanup complete: Moved %DELETED_COUNT% files, %ERROR_COUNT% errors