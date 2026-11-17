@echo off
setlocal
set "ROOT=%~dp0"
set "POWERSHELL_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"

echo Checking for stale services on ports 3000 and 5000...
"%POWERSHELL_EXE%" -NoProfile -Command "$ErrorActionPreference='Stop'; foreach ($port in 3000,5000) { $pids = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; foreach ($procId in $pids) { Write-Host \"Stopping stale process on port $port (PID $procId)\"; Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue } }"

echo Starting ML Service...
start "ML Service" "%POWERSHELL_EXE%" -NoExit -Command "Set-Location '%ROOT%ml-service'; $py = if (Test-Path 'venv\Scripts\python.exe') { '.\venv\Scripts\python.exe' } else { 'python' }; & $py -m uvicorn app:app --host 0.0.0.0 --port 5000"

echo Waiting for ML service health check...
"%POWERSHELL_EXE%" -NoProfile -Command "$tries = 0; while ($tries -lt 60) { try { Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:5000/health' -TimeoutSec 2 | Out-Null; exit 0 } catch { Start-Sleep -Milliseconds 500; $tries++ } }; exit 1" >nul 2>&1
if errorlevel 1 (
  echo Failed to start ML service on port 5000.
  exit /b 1
)

echo ML service is ready.

echo Starting Backend Service (which also serves the frontend)...
start "Backend Service" "%POWERSHELL_EXE%" -NoExit -Command "Set-Location '%ROOT%backend'; node server.js"

echo Waiting for backend health check...
"%POWERSHELL_EXE%" -NoProfile -Command "$tries = 0; while ($tries -lt 60) { try { Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:3000' -TimeoutSec 2 | Out-Null; exit 0 } catch { Start-Sleep -Milliseconds 500; $tries++ } }; exit 1" >nul 2>&1
if errorlevel 1 (
  echo Failed to start backend on port 3000.
  exit /b 1
)

echo Application is live at http://localhost:3000
echo ML Service running at http://127.0.0.1:5000
