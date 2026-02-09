@echo off
cd /d "%~dp0"
echo Starting Agent Orchestrator...
D:\Aider\.venv\Scripts\python.exe python/agent_orchestrator.py
pause
