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
pkill -f "uvicorn src.app:app" || true

nohup .venv/bin/uvicorn src.app:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

echo "Deploy finished"
