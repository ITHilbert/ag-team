@echo off
set "WINDOW_TITLE=%~1"
set "TARGET_SCRIPT=%~2"

echo [LAUNCHER] Opening window: "%WINDOW_TITLE%"
echo [LAUNCHER] Script: "%TARGET_SCRIPT%"

rem Use standard start command
start "%WINDOW_TITLE%" cmd /k "%TARGET_SCRIPT%"
