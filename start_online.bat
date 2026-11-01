@echo off
title Letter For You - Link Online na Internet
cd /d "%~dp0"
echo ========================================================
echo    Letter For You - Gerando Link Publico Online
echo ========================================================
echo.
echo IP de confirmacao caso solicitado no primeiro acesso:
curl -s https://api.ipify.org
echo.
echo.
echo Iniciando tunel localtunnel na porta 8088...
npx --yes localtunnel --port 8088
pause