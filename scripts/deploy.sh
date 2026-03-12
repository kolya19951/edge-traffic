#!/bin/bash
set -e

python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Deploy script completed"
