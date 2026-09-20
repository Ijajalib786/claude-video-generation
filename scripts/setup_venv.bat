@echo off
REM Virtual Environment Setup Script for Visual Studio (Batch version)
REM This script sets up a Python virtual environment for the video generation pipeline

echo.
echo =====================================================
echo   Virtual Environment Setup for Video Pipeline
echo =====================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Install Python from https://www.python.org
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo WARNING: Virtual environment already exists
    set /p response="Do you want to delete and recreate it? (y/n): "
    if /i "%response%"=="y" (
        rmdir /s /q venv
        echo Deleted existing venv
    ) else (
        echo Using existing venv
        goto :activate
    )
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

:activate
REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Verify installation
echo Verifying installation...
python -c "import anthropic; print('  anthropic: OK')"
python -c "import pydantic; print('  pydantic: OK')"
python -c "import click; print('  click: OK')"
echo All packages verified
echo.

REM Test setup
echo Running setup verification...
python tests\test_phase_1.py
echo.

REM Display next steps
echo =====================================================
echo SETUP COMPLETE!
echo =====================================================
echo.
echo Virtual environment location:
echo   %CD%\venv
echo.
echo To activate virtual environment (future sessions):
echo   .\venv\Scripts\activate.bat
echo.
echo To generate your first script:
echo   python scripts\cli.py generate
echo.
echo Documentation:
echo   - QUICKSTART.md - Get started in 3 minutes
echo   - PHASE_1_README.md - Complete guide
echo.
echo Visual Studio Integration:
echo   1. Open Python Environments panel
echo      (View ^> Other Windows ^> Python Environments)
echo   2. You should see 'venv' in the list
echo   3. Right-click 'venv' and select 'Set as Default'
echo.
pause
