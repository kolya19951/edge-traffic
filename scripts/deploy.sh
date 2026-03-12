#!/bin/bash
set -e

APP_DIR="$HOME/edge-traffic"

echo "Starting deploy..."

cd "$APP_DIR"

echo "Updating repo..."
git pull origin main

echo "Creating virtualenv..."
python3 -m venv .venv || true

source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Restarting app..."

pkill -f "python src/app.py" || true

nohup .venv/bin/python src/app.py > app.log 2>&1 &

echo "Deploy finished"
