#!/bin/bash
set -euo pipefail

APP_DIR="$HOME/edge-traffic"
VENV_DIR="$APP_DIR/.venv"
PYTHON_BIN="python3"

echo "Starting deploy..."
cd "$APP_DIR"

echo "Updating repo..."
git pull origin main

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv..."
  $PYTHON_BIN -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
make install

echo "Stopping existing API process..."
pkill -f "uvicorn edge_traffic.api.main:app" || true
pkill -f "edge_traffic.worker.main" || true


echo "Starting API..."
nohup "$VENV_DIR/bin/uvicorn" edge_traffic.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  > app.log 2>&1 &

echo "Starting worker..."
nohup "$VENV_DIR/bin/python" -m edge_traffic.worker.main \
  > worker.log 2>&1 &

echo "Deploy finished"
