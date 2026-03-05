@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo  EZI Returns - Local Launcher
echo  ==============================
echo.

if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python.exe -m venv venv
    if errorlevel 1 (
        echo.
        echo  ERROR: Could not create virtual environment.
        echo  Make sure Python is installed. Download from https://python.org
        pause & exit /b 1
    )
    echo [2/3] Installing packages (first time only, takes ~30s)...
    venv\Scripts\pip install -r requirements-local.txt -q
    if errorlevel 1 (
        echo  ERROR: Package install failed. Check your internet connection.
        pause & exit /b 1
    )
) else (
    echo [INFO] Virtual environment ready.
)

echo [3/3] Initialising local database...
venv\Scripts\python init_local_db.py

echo.
echo  ================================================
echo   Open your browser at: http://localhost:5000
echo   Press Ctrl+C to stop the server.
echo  ================================================
echo.

venv\Scripts\python local_app.py
pause
