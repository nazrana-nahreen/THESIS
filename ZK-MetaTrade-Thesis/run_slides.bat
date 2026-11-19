@echo off
title ZK-MetaTrade Presentation Deck
cd /d "%~dp0"
echo ============================================================
echo   Opening ZK-MetaTrade Thesis Defense Slide Deck...
echo ============================================================
start "" "%~dp0presentation\index.html"
echo [SUCCESS] Slides opened in your default browser.
echo - Press Right Arrow or Space to advance slides.
echo - Press Left Arrow to go back.
echo - Press F for Fullscreen.
echo - Press N for Speaker Notes.
pause
