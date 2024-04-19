@echo off

REM Install dependencies
python -m pip install -r requirements.txt >NUL 2>&1
echo Installed necessary Python libraries.

REM Set environment variables within the virtual environment
SET FLASK_APP=main
SET FLASK_ENV=development
SET FLASK_DEBUG=1
echo Virtual environment variables set.

REM Echo ExcelGuard ASCII art
echo __________________________________________________________________________
echo  ___________                  . __    ________                      .___
echo  \_   _____/__  ___ ____  ____^|  ^|  /  _____/ __ _______ _______  __^| _/
echo  ^|    __^)_\  \/  // ___\/ __ \^|  ^| /   \  ___^|  ^|  \__  \\_  __ \/ __ ^| 
echo  ^|         \^>    ^<\ \__\  ___/^|  ^|_\    \_\  \  ^|  // __ \^|  ^| \/ /_/ ^| 
echo  /_______  /__/\__\\___^>^|____\^|_____/\______  /____/^|____  /__^|  \____^| 
echo          \/                                 \/           \/           
echo _________________________________________________________________________

REM Run application
flask run