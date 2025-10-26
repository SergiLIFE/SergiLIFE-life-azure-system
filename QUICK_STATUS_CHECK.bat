@echo off
REM Quick Status Check - October 26, 2025

echo Current Status Check
echo ==================

echo Branch:
git branch --show-current

echo.
echo Rebase status:
if exist .git\rebase-merge (
    echo ⚠️  REBASE IN PROGRESS
    echo Files: .git\rebase-merge\
    dir .git\rebase-merge\
) else (
    echo ✅ No rebase in progress
)

echo.
echo Merge status:
if exist .git\MERGE_HEAD (
    echo ⚠️  MERGE IN PROGRESS
) else (
    echo ✅ No merge in progress
)

echo.
echo Uncommitted changes:
git status --porcelain

echo.
echo Recent commits:
git log --oneline -5

echo.
echo Remote status:
git status -uno

pause