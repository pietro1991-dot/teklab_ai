@echo off
title Cloudflare Tunnel - Auto Restart
color 0A

echo ============================================
echo    CLOUDFLARE TUNNEL - AUTO RESTART
echo ============================================
echo.
echo URL cambiera' a ogni riavvio (modalita' gratuita)
echo Questo script riavvia automaticamente il tunnel
echo.
echo CTRL+C per fermare
echo.

:restart
echo [%TIME%] Avvio tunnel...
"%USERPROFILE%\cloudflared.exe" tunnel --url http://localhost:5000

if errorlevel 1 (
    echo.
    echo [ERRORE] Tunnel disconnesso con errore!
    echo Riavvio tra 10 secondi...
    timeout /t 10 /nobreak >nul
) else (
    echo.
    echo [INFO] Tunnel chiuso normalmente
    echo Riavvio tra 5 secondi...
    timeout /t 5 /nobreak >nul
)

goto restart
