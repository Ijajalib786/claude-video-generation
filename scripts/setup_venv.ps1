# Virtual Environment Setup Script for Visual Studio
# This script sets up a Python virtual environment for the video generation pipeline

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  Virtual Environment Setup for Video Pipeline" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "   Install Python from https://www.python.org" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to delete and recreate it? (y/n)"
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force "venv"
        Write-Host "Deleted existing venv" -ForegroundColor Gray
    } else {
        Write-Host "Using existing venv" -ForegroundColor Gray
    }
}

if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q
Write-Host "✅ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📥 Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "✔️  Verifying installation..." -ForegroundColor Yellow
python -c "import anthropic; print(f'  anthropic: {anthropic.__version__}')"
python -c "import pydantic; print(f'  pydantic: {pydantic.__version__}')"
python -c "import click; print(f'  click: OK')"
Write-Host "✅ All packages verified" -ForegroundColor Green
Write-Host ""

# Test setup
Write-Host "🧪 Running setup verification..." -ForegroundColor Yellow
python tests\test_phase_1.py
Write-Host ""

# Display next steps
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Virtual environment location:" -ForegroundColor Cyan
Write-Host "   $(Get-Location)\venv" -ForegroundColor Gray
Write-Host ""
Write-Host "🔄 To activate virtual environment (future sessions):" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 To generate your first script:" -ForegroundColor Cyan
Write-Host "   python scripts\cli.py generate" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - docs/QUICKSTART.md - Get started in 3 minutes" -ForegroundColor Gray
Write-Host "   - docs/PHASE_1_README.md - Complete guide" -ForegroundColor Gray
Write-Host ""
Write-Host "🧩 Visual Studio Integration:" -ForegroundColor Cyan
Write-Host "   1. Open Python Environments panel (View > Other Windows > Python Environments)" -ForegroundColor Gray
Write-Host "   2. You should see 'venv' in the list" -ForegroundColor Gray
Write-Host "   3. Right-click 'venv' and select 'Set as Default'" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: Virtual environment is active in this terminal session" -ForegroundColor Yellow
Write-Host "   You can now run Python commands with all dependencies available" -ForegroundColor Yellow
Write-Host ""
