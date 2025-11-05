@echo off
echo ============================================
echo    CLOUDFLARE TUNNEL - AUTO RESTART
echo ============================================
echo.
echo ATTENZIONE: URL cambiera' ogni riavvio (modalita' gratuita)
echo Per URL fisso serve account Cloudflare con dominio
echo.
echo Avvio tunnel su http://localhost:5000...
echo.

:restart
"%USERPROFILE%\cloudflared.exe" tunnel --url http://localhost:5000

echo.
echo TUNNEL DISCONNESSO!
echo Riavvio automatico in 5 secondi...
timeout /t 5 /nobreak >nul
goto restart
