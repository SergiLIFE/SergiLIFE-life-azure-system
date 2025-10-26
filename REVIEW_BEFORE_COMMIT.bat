@echo off
echo ========================================
echo REVIEW STAGED CHANGES BEFORE COMMIT
echo ========================================

echo Step 1: Count staged files...
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set staged_count=%%i
echo "Staged files: %staged_count%"

echo.
echo Step 2: File types breakdown...
echo "Python files:"
git diff --cached --name-only | findstr "\.py$" | find /c /v ""

echo "HTML/CSS/JS files:"
git diff --cached --name-only | findstr "\.html$\|\.css$\|\.js$" | find /c /v ""

echo "Batch/Config files:"
git diff --cached --name-only | findstr "\.bat$\|\.json$\|\.yml$\|\.yaml$\|\.md$" | find /c /v ""

echo "Other files:"
git diff --cached --name-only | findstr /v "\.py$\|\.html$\|\.css$\|\.js$\|\.bat$\|\.json$\|\.yml$\|\.yaml$\|\.md$" | find /c /v ""

echo.
echo Step 3: Sample of files (first 30):
git diff --cached --name-only | more +0

echo.
echo Step 4: Check for potentially problematic files...
echo "Large files (potential issues):"
git diff --cached --name-only | findstr "\.exe$\|\.dll$\|\.zip$\|\.rar$\|\.iso$"

echo "Sensitive files (check content):"
git diff --cached --name-only | findstr "password\|secret\|key\|token\|credential"

echo "Temp/cache files:"
git diff --cached --name-only | findstr "temp\|tmp\|cache\|\.log$\|\.bak$"

echo.
echo ========================================
echo "Review complete. Ready to commit safely?"
echo "1. Remove problematic files with: git reset HEAD filename"
echo "2. Commit good files with: git commit -m 'message'"
echo ========================================
pause