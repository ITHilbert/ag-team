@echo off
cd /d "%~dp0"
echo Starting Agent Orchestrator...
python python/agent_orchestrator.py
pause
