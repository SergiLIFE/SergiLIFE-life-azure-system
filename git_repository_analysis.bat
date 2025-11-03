@echo off
REM Git Repository Analysis Script (Windows)
REM Check repository size, integrity, and largest files

echo ==================================================
echo GIT REPOSITORY ANALYSIS
echo ==================================================
echo.

echo 1. CHECKING GIT REPOSITORY SIZE...
echo --------------------------------------------------
REM Check git repository size (Windows equivalent using dir)
if exist ".git" (
    for /f "tokens=3" %%a in ('dir /-c /s .git ^| find "File(s)"') do echo Git repository size: %%a bytes
) else (
    echo No .git directory found
)
echo.

echo 2. VERIFYING REPOSITORY INTEGRITY...
echo --------------------------------------------------
REM Verify repository integrity
git fsck --full
echo.

echo 3. ANALYZING REPOSITORY OBJECTS...
echo --------------------------------------------------
REM Show repository object information (simplified for Windows)
echo Checking repository objects...
git count-objects -v
echo.

echo Largest files by commit history:
git rev-list --objects --all | git cat-file --batch-check | sort -k3 -n | tail -10
echo.

echo Recent large files in working directory:
dir /s /-c | sort /r | findstr /v "Directory" | head -10
echo.

echo ==================================================
echo REPOSITORY ANALYSIS COMPLETE
echo ==================================================
pause