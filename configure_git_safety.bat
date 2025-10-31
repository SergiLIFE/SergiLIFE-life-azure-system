@echo off
REM ========================================
REM Git Configuration for Corruption Prevention
REM Sets up protective git settings
REM ========================================

echo Configuring Git for maximum safety and corruption prevention...

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

REM Core safety settings
echo Setting core safety configurations...
git config core.preloadindex true
git config core.fscache true
git config core.autocrlf true
git config core.safecrlf true

REM Enable fsck on receive and fetch
echo Enabling automatic integrity checks...
git config transfer.fsckobjects true
git config fetch.fsckobjects true
git config receive.fsckobjects true

REM Set up automatic garbage collection
echo Configuring garbage collection...
git config gc.auto 256
git config gc.autopacklimit 50
git config gc.autodetach true

REM Configure pack settings for stability
echo Setting pack configurations...
git config pack.packsizelimit 2g
git config pack.windowmemory 256m

REM Set up ref storage for reliability
echo Configuring ref storage...
git config core.logallrefupdates true

REM Configure merge and rebase safety
echo Setting merge/rebase safety...
git config merge.ff false
git config pull.rebase false
git config rebase.autostash false

REM Set up automatic backup of important refs
echo Configuring ref backup...
git config alias.backup-refs "!git for-each-ref --format='%(refname) %(objectname)' > .git/refs-backup-$(date +%%Y%%m%%d-%%H%%M%%S).txt"

REM Create useful aliases for maintenance
echo Creating maintenance aliases...
git config alias.health-check "!git fsck --full --strict && git gc --prune=now"
git config alias.safe-push "!git fsck --full && git push"
git config alias.verify-bundle "bundle verify"

REM Configure automatic maintenance
echo Setting up automatic maintenance...
git maintenance register 2>nul || echo "Maintenance registration requires Git 2.30+"

echo.
echo ===== Git Safety Configuration Complete =====
echo.
echo Safety features enabled:
echo ✅ Automatic integrity checks on fetch/receive
echo ✅ Enhanced garbage collection settings
echo ✅ Core safety and CRLF handling
echo ✅ Ref logging and backup aliases
echo ✅ Maintenance aliases created
echo.
echo New commands available:
echo   git health-check    - Full repository health verification
echo   git safe-push      - Verify integrity before push
echo   git backup-refs    - Backup all refs with timestamps
echo.
pause