@echo off
setlocal

echo Stopping InfCanvas Python servers...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$targets = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and ($_.CommandLine -match 'save_server.py' -or $_.CommandLine -match ' -m http\.server 8000') }; if (-not $targets) { Write-Host 'No matching InfCanvas Python server processes found.'; exit 0 }; $targets | ForEach-Object { Write-Host ('Stopping PID ' + $_.ProcessId + ': ' + $_.CommandLine); Stop-Process -Id $_.ProcessId -Force }"

endlocal