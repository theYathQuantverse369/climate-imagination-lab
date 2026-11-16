@echo off
cd /d "%~dp0"
py -3 --version >nul 2>nul
if errorlevel 1 (
  echo Python is not installed. Opening the self-running demo version.
  start "Climate Imagination Lab" "%~dp0frontend\index.html"
  exit /b 0
)
echo Starting Climate Imagination Lab at http://localhost:8010
echo Keep the server window open while you use the website.
start "Climate Lab Server" /D "%~dp0backend" cmd /k "set PORT=8010&&py -3 server.py"
timeout /t 2 /nobreak >nul
start "Climate Imagination Lab" http://localhost:8010
