#!/usr/bin/env bash

set -e
cd "$(dirname "$0")"

echo "========================================="
echo "   Starting Boids Simulation...    "
echo "========================================="

echo "[1/2] Activating virtual environment..."
source .venv/bin/activate

echo "[2/2] Launching Boids simulation..."
echo "========================================="
python3 main.py

deactivate