@echo off
title ZK-MetaTrade DApp Launcher
cd /d "%~dp0"
echo ============================================================
echo   Starting ZK-MetaTrade Interactive DApp...
echo ============================================================
start "" "%~dp0index.html"
echo [SUCCESS] Opened ZK-MetaTrade DApp in your default browser.
pause
