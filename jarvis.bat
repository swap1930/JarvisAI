@echo off
:start
python 'your_file_name.py'  %user_command%
set /p user_command="Enter your command: "
pause
goto start