@echo off
echo ========================================
echo TEKLAB TELEGRAM BOT - AVVIO
echo ========================================
echo.

echo Verifica ambiente Python...
python --version
echo.

echo Installazione dipendenze...
pip install -r requirements.txt
echo.

echo IMPORTANTE: Assicurati che il backend Flask sia avviato!
echo Backend URL: http://localhost:5000
echo.
pause

echo Avvio bot Telegram...
python telegram_bot_v2.py

pause