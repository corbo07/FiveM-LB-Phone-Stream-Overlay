@echo off
title Phone Snapshot
cd /d "%~dp0"
python detect.py --snap
pause
