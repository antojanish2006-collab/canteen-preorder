@echo off
python --version
python -m pip --version
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python seed.py
python app.py
