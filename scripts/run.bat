@echo off
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
start /B python server\main.py
rem give server time to start
ping 127.0.0.1 -n 3 > nul
python app\main.py
