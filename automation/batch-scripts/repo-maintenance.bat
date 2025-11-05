@echo off
REM Repository Maintenance Script (Windows)
REM Implements the guidelines from REPOSITORY_GUIDELINES.md

echo ==========================================
echo REPOSITORY MAINTENANCE SCRIPT
echo ==========================================
echo.

REM Check for problematic file patterns
echo 1. CHECKING FOR PROBLEMATIC FILE PATTERNS...
echo ------------------------------------------
echo Files with problematic prefixes:
dir /b *EMERGENCY* *QUICK* *IMMEDIATE* *COMPREHENSIVE* *FINAL* 2>nul | findstr /v "ERROR" | head -10
echo.

REM Check repository health
echo 2. REPOSITORY HEALTH CHECK...
echo ------------------------------------------
echo Repository information:
if exist ".git" (
    echo ✅ Git repository detected
    git status --porcelain | wc -l > temp_count.txt
    set /p uncommitted=<temp_count.txt
    del temp_count.txt
    echo Uncommitted changes: %uncommitted%
) else (
    echo ❌ No git repository found
)
echo.
echo File count by type:
for /f %%i in ('dir /s /b *.md 2^>nul ^| find /c /v ""') do echo   Markdown files: %%i
for /f %%i in ('dir /s /b *.py 2^>nul ^| find /c /v ""') do echo   Python files: %%i
for /f %%i in ('dir /s /b *.bat 2^>nul ^| find /c /v ""') do echo   Batch files: %%i
for /f %%i in ('dir /s /b *.html 2^>nul ^| find /c /v ""') do echo   HTML files: %%i
echo.

REM Check for large files
echo 3. LARGE FILE ANALYSIS...
echo ------------------------------------------
echo Largest files in repository:
dir /s /-c /o-s | findstr /v "Directory" | head -5
echo.

REM Cleanup recommendations
echo 4. CLEANUP RECOMMENDATIONS...
echo ------------------------------------------
echo Suggested actions:
if exist ".cleanup" (
    echo ✅ Cleanup system already in place
) else (
    echo ❗ Consider setting up .cleanup directory structure
)

if exist ".gitignore" (
    echo ✅ .gitignore file exists
) else (
    echo ❗ Create .gitignore to prevent future issues
)

echo.
echo ==========================================
echo MAINTENANCE SCRIPT COMPLETE
echo Run this script weekly as per guidelines
echo ==========================================
pause