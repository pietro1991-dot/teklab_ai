@echo off
REM ========================================
REM Spirituality AI - Quick Start
REM ========================================

echo.
echo ===============================================
echo   SPIRITUALITY AI - Avvio Sistema
echo ===============================================
echo.

REM Check se siamo nella directory corretta
if not exist "backend_api\app.py" (
    echo [ERRORE] File backend_api\app.py non trovato!
    echo Esegui questo script dalla root del progetto spirituality.ai
    pause
    exit /b 1
)

REM Check Python installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo Installa Python 3.10+ da https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Controllo dipendenze backend...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [WARN] Flask non installato. Installazione in corso...
    pip install flask flask-cors
)

echo [2/3] Avvio backend API...
echo.
echo ^> Backend API avviato su http://localhost:5000
echo ^> Apri UI_experience\index.html nel browser
echo.
echo ===============================================
echo   Per fermare il server: CTRL+C
echo ===============================================
echo.

REM Avvia backend
python backend_api\app.py

pause
