@echo off
title Phone Overlay
cd /d "%~dp0overlay"
start "Phone Overlay Server" /min cmd /c "node server.js"
timeout /t 2 /nobreak >nul
python detect.py
taskkill /fi "WINDOWTITLE eq Phone Overlay Server*" /f >nul 2>&1
pause
