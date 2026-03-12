#!/bin/bash
set -e

APP_DIR=/home/pi/edge-traffic

mkdir -p "$APP_DIR"
rsync -av --delete ./ "$APP_DIR"/

cd "$APP_DIR"

python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pkill -f "python.*src/app.py" || true
nohup .venv/bin/python src/app.py > app.log 2>&1 &
