@echo off
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
set FLASK_APP=main
set FLASK_ENV=development
set FLASK_DEBUG=1
