@echo off

REM Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

REM Install dependencies
python -m pip install -r requirements.txt

REM Set environment variables within the virtual environment
echo SET FLASK_APP=main > venv\Scripts\activate.bat
echo SET FLASK_ENV=development >> venv\Scripts\activate.bat
echo SET FLASK_DEBUG=1 >> venv\Scripts\activate.bat