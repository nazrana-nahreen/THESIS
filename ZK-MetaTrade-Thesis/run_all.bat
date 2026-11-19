@echo off
title ZK-MetaTrade Research Results Runner
echo Starting ZK-MetaTrade Master Evaluation...
node "%~dp0run_experiments.js"
echo.
echo ============================================================
echo   To launch the Interactive ZK-MetaTrade DApp Showcase:
echo   Double-click run_dapp.bat or open dapp\index.html
echo ============================================================
pause
