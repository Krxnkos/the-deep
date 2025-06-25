@echo off
echo THE DEEP - Deep Sea Exploration Game
echo ==================================
echo.
echo Please choose a game mode:
echo 1. Terminal Mode
echo 2. GUI Mode
echo.

choice /C 12 /M "Enter your choice (1 or 2): "

if errorlevel 2 goto GUI
if errorlevel 1 goto Terminal

:Terminal
cd src
python main.py
goto End

:GUI
cd src
python main.py --gui
goto End

:End
pause
