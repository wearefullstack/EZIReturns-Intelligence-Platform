@echo off
cd /d "%~dp0"

echo.
echo  EZI Returns Intelligence Platform - Local Launcher
echo  ====================================================
echo.

:: Check if venv exists, create if not
if exist "venv\Scripts\python.exe" goto :venv_ready

echo  [1/3] Creating virtual environment...
python.exe -m venv venv
if errorlevel 1 goto :err_python

echo  [2/3] Installing packages (first time only, ~30 seconds)...
venv\Scripts\pip install -r requirements-local.txt -q
if errorlevel 1 goto :err_pip

:venv_ready
echo  [ OK ] Virtual environment ready.

:: Initialise database
echo  [3/3] Initialising local database...
venv\Scripts\python.exe init_local_db.py

echo.
echo  ================================================
echo    Open your browser at: http://localhost:5000
echo    Press Ctrl+C to stop the server.
echo  ================================================
echo.

venv\Scripts\python.exe local_app.py
goto :end

:err_python
echo.
echo  ERROR: Python not found. Download from https://python.org
echo.
pause
exit /b 1

:err_pip
echo.
echo  ERROR: Package install failed. Check your internet connection.
echo.
pause
exit /b 1

:end
echo.
echo  Server stopped.
pause
