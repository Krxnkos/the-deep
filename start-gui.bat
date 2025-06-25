@echo off
echo Starting THE DEEP in GUI mode...
echo.

cd src
python -c "import sys, os; sys.path.insert(0, os.path.dirname(os.getcwd())); sys.path.insert(0, os.getcwd()); from main import main; import sys; sys.argv.append('--gui'); main()"

if %errorlevel% neq 0 (
    echo.
    echo An error occurred while starting the game in GUI mode.
    echo Please check the logs for details.
)

pause
