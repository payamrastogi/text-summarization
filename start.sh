#!/bin/bash

mkdir log
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python summarize_app.py &
echo $! >> summarize_app.pid