@echo off
REM Step 7: Clean Git history (optional but recommended)
REM Only execute after backup confirmed!
REM This removes all Copilot-generated files from entire git history

echo ===================================
echo STEP 7: GIT HISTORY CLEANUP
echo ===================================
echo WARNING: This will modify git history!
echo Ensure backup is confirmed before proceeding!
echo.

REM Step 1: Create list of files to remove
echo Step 1: Creating list of problematic commits...
git log --all --full-history --oneline | findstr /i "copilot emergency quick comprehensive" > files-to-remove.txt

echo Commits found with problematic patterns:
type files-to-remove.txt

REM Step 2: Use git filter-branch to remove from history (DESTRUCTIVE - use backup first!)
echo.
echo Step 2: Git history cleanup options available:
echo.
echo OPTION A - git filter-branch (traditional method):
echo # git filter-branch --tree-filter "rm -f [filename]" -- --all
echo.
echo OPTION B - git-filter-repo (safer, modern approach):
echo # First install: pip install git-filter-repo
echo # git filter-repo --invert-paths --paths "[filename]" --force
echo.
echo Files identified for removal from history:
echo - All COPILOT-generated files
echo - All EMERGENCY deployment files  
echo - All QUICK fix files
echo - All COMPREHENSIVE analysis files
echo.
echo WARNING: Only proceed after confirming backup exists!
echo To execute cleanup, manually run one of the options above.
pause