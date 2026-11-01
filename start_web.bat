@echo off
title Letter For You - Servidor de Acesso Web
cd /d "%~dp0"
echo ========================================================
echo    Letter For You - Servidor de Acesso Web
echo ========================================================
echo.
echo Abrindo o projeto no seu navegador padrao...
start http://localhost:8088
echo.
echo Para acessar pelo celular na mesma rede Wi-Fi:
echo http://192.168.3.190:8088
echo.
echo Pressione CTRL+C nesta janela caso queira encerrar o servidor.
echo.
python -m http.server 8088
pause