@echo off
setlocal

cd /d "%~dp0"

python render_readme.py
if errorlevel 1 (
  echo Failed to render README.html
  exit /b 1
)

echo Done. Open README.html in your browser.
exit /b 0
