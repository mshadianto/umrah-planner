@echo off
REM ==============================================
REM Umrah Planner AI - Run Script for Windows
REM ==============================================

echo.
echo 🕋 Starting Umrah Planner AI...
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found. Creating from template...
    copy .env.example .env >nul
    echo Please edit .env and add your API keys, then run again.
    pause
    exit /b 1
)

echo Starting Streamlit server...
echo Open http://localhost:8501 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py --server.port 8501
