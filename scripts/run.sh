#!/bin/bash
set -e
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python server/main.py &
SERVER_PID=$!
sleep 2
python app/main.py
kill $SERVER_PID
