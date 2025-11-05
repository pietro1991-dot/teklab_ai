@echo off
echo ============================================
echo    TEKLAB CHATBOT - PRODUCTION MODE
echo ============================================
echo.

REM Avvia Flask backend in finestra separata
echo [1/3] Avvio Flask Backend...
start "Teklab Backend" cmd /k "cd /d %~dp0backend_api && python app.py"
timeout /t 3 /nobreak >nul

REM Avvia Cloudflare Tunnel in finestra separata
echo [2/3] Avvio Cloudflare Tunnel...
start "Cloudflare Tunnel" cmd /k "%USERPROFILE%\cloudflared.exe tunnel --url http://localhost:5000"
timeout /t 5 /nobreak >nul

echo.
echo ============================================
echo    SISTEMA AVVIATO!
echo ============================================
echo.
echo IMPORTANTE: Copia URL Cloudflare dalla finestra "Cloudflare Tunnel"
echo Esempio: https://teklab-abc-xyz.trycloudflare.com
echo.
echo Poi aggiorna UI_experience/config.js con questo URL
echo.
echo [3/3] Apro browser per testare...
timeout /t 3 /nobreak >nul
start "" "http://localhost:5000"

echo.
echo Premi un tasto per chiudere...
pause >nul
