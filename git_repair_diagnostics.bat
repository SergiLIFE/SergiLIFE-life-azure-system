@echo off
cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo ===== GIT REPAIR DIAGNOSTICS ===== > diagnostics_output.txt
echo Date: %date% %time% >> diagnostics_output.txt
echo. >> diagnostics_output.txt

echo ----- GIT FSCK FULL ----- >> diagnostics_output.txt
git --no-pager fsck --full >> diagnostics_output.txt 2>&1
echo FSCK Exit Code: %ERRORLEVEL% >> diagnostics_output.txt
echo. >> diagnostics_output.txt

echo ----- GIT STATUS ----- >> diagnostics_output.txt
git status >> diagnostics_output.txt 2>&1
echo STATUS Exit Code: %ERRORLEVEL% >> diagnostics_output.txt
echo. >> diagnostics_output.txt

echo ----- GIT REMOTES ----- >> diagnostics_output.txt
git remote -v >> diagnostics_output.txt 2>&1
echo REMOTES Exit Code: %ERRORLEVEL% >> diagnostics_output.txt
echo. >> diagnostics_output.txt

echo ----- GIT BRANCH INFO ----- >> diagnostics_output.txt
git branch --show-current >> diagnostics_output.txt 2>&1
git branch -a >> diagnostics_output.txt 2>&1
echo BRANCH Exit Code: %ERRORLEVEL% >> diagnostics_output.txt
echo. >> diagnostics_output.txt

echo ----- REFS DIRECTORY LISTING ----- >> diagnostics_output.txt
dir .git\refs /s /-C >> diagnostics_output.txt 2>&1
echo. >> diagnostics_output.txt

echo ===== DIAGNOSTICS COMPLETE ===== >> diagnostics_output.txt
echo Diagnostics saved to diagnostics_output.txt