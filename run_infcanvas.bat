@echo off
setlocal

REM === CHANGE THIS TO YOUR CANVAS APP FOLDER ===
set "APP_FOLDER=%~dp0"

REM === DEFAULT LAYOUT JSON FOLDER (PRESS ENTER TO USE THIS) ===
set "DEFAULT_LAYOUT_FOLDER=C:\Apps\InfCanvas\"

set /p LAYOUT_FOLDER=Layout folder path (blank = %DEFAULT_LAYOUT_FOLDER%): 
if "%LAYOUT_FOLDER%"=="" set "LAYOUT_FOLDER=%DEFAULT_LAYOUT_FOLDER%"
if not exist "%LAYOUT_FOLDER%" mkdir "%LAYOUT_FOLDER%"

echo Using layout folder: %LAYOUT_FOLDER%

cd "%APP_FOLDER%"

REM === START STATIC SERVER FOR CANVAS ===
start "" python -m http.server 8000

REM === START SAVE SERVER ===
start "" cmd /c "set LAYOUT_DIR=%LAYOUT_FOLDER%&& python save_server.py"

REM === GIVE SERVERS TIME TO START ===
timeout /t 2 >nul

REM === OPEN EDGE INPRIVATE ===
start msedge.exe -inprivate http://localhost:8000/InfCanvas.html

endlocal
