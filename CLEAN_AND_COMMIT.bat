@echo off
echo ========================================
echo CLEAN UP CACHE FILES AND COMMIT SAFELY
echo ========================================

echo Step 1: Remove all cache and temp files from staging...
git reset HEAD .mypy_cache/ 2>nul
git reset HEAD __pycache__/ 2>nul
git reset HEAD *.pyc 2>nul
git reset HEAD .pytest_cache/ 2>nul

echo Step 2: Delete cache directories...
if exist ".mypy_cache" rmdir /s /q .mypy_cache
if exist "__pycache__" rmdir /s /q __pycache__
if exist ".pytest_cache" rmdir /s /q .pytest_cache

echo Step 3: Update .gitignore to prevent future cache commits...
echo .mypy_cache/ >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo .pytest_cache/ >> .gitignore
echo .vscode/ >> .gitignore
echo *.log >> .gitignore
echo .env >> .gitignore
echo node_modules/ >> .gitignore

echo Step 4: Check clean file count...
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set clean_count=%%i
echo "Clean files ready to commit: %clean_count%"

echo Step 5: Show sample of clean files...
echo "Sample files (clean, no cache):"
git diff --cached --name-only | findstr /v "cache\|\.pyc\|\.log\|temp" | more +0

echo.
echo "========================================"
echo "CACHE CLEANUP COMPLETE"
echo "Ready to commit %clean_count% clean files"
echo "========================================"
pause