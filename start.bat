@echo off
echo Starting THE DEEP...
echo.

cd src
python main.py

if %errorlevel% neq 0 (
    echo.
    echo An error occurred while starting the game.
    echo Please check the logs for details.
)

pause
