@echo off
cd /d "%~dp0"
REM Start Aider with local Mistral model
echo Starting Aider with Ollama/Mistral...
echo Ensure Ollama is running!

REM Set environment variables if needed
set OLLAMA_API_BASE=http://localhost:11434

REM Run Aider from the virtual environment
D:\Aider\.venv\Scripts\aider --model ollama/mistral --no-auto-commits --no-git --no-show-model-warnings

pause
