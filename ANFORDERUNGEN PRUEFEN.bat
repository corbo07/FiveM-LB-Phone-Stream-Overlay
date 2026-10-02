@echo off
title Anforderungen pruefen
cd /d "%~dp0"
set NEUSTART=0

echo === Node.js ===
node -v >nul 2>&1
if errorlevel 1 (
    echo Node.js fehlt, wird installiert...
    winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    set NEUSTART=1
) else (
    for /f %%v in ('node -v') do echo Node.js gefunden: %%v
)

echo.
echo === Python ===
python -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo Python fehlt, wird installiert...
    winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    set NEUSTART=1
) else (
    for /f "tokens=*" %%v in ('python --version') do echo Python gefunden: %%v
)

echo.
if "%NEUSTART%"=="1" (
    echo Es wurde etwas neu installiert. Bitte dieses Fenster schliessen und
    echo diese Datei noch einmal starten, damit die Python-Pakete installiert werden.
    echo.
    pause
    exit /b
)

echo === Python-Pakete ===
python -m pip install --quiet opencv-python mss numpy
if errorlevel 1 (
    echo Fehler beim Installieren der Python-Pakete.
) else (
    echo opencv-python, mss und numpy sind installiert.
)

echo.
echo Alles bereit. Jetzt "OVERLAY STARTEN.bat" ausfuehren.
echo.
pause
