@echo off

REM Install dependencies
python -m pip install -r requirements.txt

REM Set environment variables within the virtual environment
SET FLASK_APP=main
SET FLASK_ENV=development
SET FLASK_DEBUG=1

flask run