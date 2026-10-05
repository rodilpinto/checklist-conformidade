@echo off
rem Sobe o app. Chamado pela tarefa agendada (servidor\instalar_tarefa.ps1).
rem Argumento opcional: porta (padrao 8401). Saida do app em logs\app.log.
setlocal
cd /d "%~dp0.."
set PORTA=%1
if "%PORTA%"=="" set PORTA=8401
if not exist logs mkdir logs
set PYTHONIOENCODING=utf-8
echo [%date% %time%] iniciando na porta %PORTA% >> logs\app.log
".venv\Scripts\python.exe" -m streamlit run app.py --server.port %PORTA% --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false >> logs\app.log 2>&1
