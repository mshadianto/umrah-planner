@echo off
REM ==============================================
REM Umrah Planner AI - Setup Script for Windows CMD
REM ==============================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║          🕋 Umrah Planner AI - Setup Script               ║
echo ║      RAG Agentic AI untuk Simulasi Biaya Umrah            ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies (this may take a few minutes)...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Setup environment file
echo [5/5] Setting up environment...
if not exist ".env" (
    copy .env.example .env >nul
    echo Created .env file
    echo IMPORTANT: Edit .env and add your API key!
) else (
    echo .env file already exists
)
echo.

REM Create directories
if not exist "data\chroma_db" mkdir data\chroma_db
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              Setup Complete!                              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Edit .env file and add your API key
echo   2. Get free Groq API key at: https://console.groq.com/
echo   3. Run: run.bat
echo.
pause
