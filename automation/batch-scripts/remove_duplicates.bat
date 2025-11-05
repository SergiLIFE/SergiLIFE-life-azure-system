@echo off
REM Step 6: Remove duplicate files (keep one version)
REM Windows batch equivalent of bash duplicate removal script

setlocal enabledelayedexpansion

echo [%date% %time%] Starting Step 6: Duplicate file removal >> .cleanup\logs\deleted-files.log

set DUPLICATE_COUNT=0
set PROCESSED_COUNT=0

echo Processing CORRECTED and FIXED files for duplicates...

REM Create a temporary file list
dir /b /s *CORRECTED* *FIXED* > temp_file_list.txt 2>nul

REM Process each file
for /f "delims=" %%f in (temp_file_list.txt) do (
    if exist "%%f" (
        set /a PROCESSED_COUNT+=1
        echo Processing: %%f
        
        REM Check if this is a duplicate based on filename patterns
        echo %%f | findstr /i "CORRECTED.*CORRECTED\|FIXED.*FIXED\|_FIXED_CORRECTED\|_CORRECTED_FIXED" >nul
        if not errorlevel 1 (
            REM This appears to be a duplicate
            move "%%f" ".cleanup\quarantine\duplicates\" >nul 2>>.cleanup\logs\deleted-files.log
            if not errorlevel 1 (
                echo [%date% %time%] REMOVED DUPLICATE: %%f >> .cleanup\logs\deleted-files.log
                echo Removed duplicate: %%f
                set /a DUPLICATE_COUNT+=1
            ) else (
                echo [%date% %time%] ERROR moving duplicate: %%f >> .cleanup\logs\deleted-files.log
            )
        )
    )
)

REM Clean up temp file
del temp_file_list.txt 2>nul

echo [%date% %time%] Step 6 Complete: Processed %PROCESSED_COUNT% files, removed %DUPLICATE_COUNT% duplicates >> .cleanup\logs\deleted-files.log
echo Step 6 complete: Processed %PROCESSED_COUNT% files, removed %DUPLICATE_COUNT% duplicates

endlocal