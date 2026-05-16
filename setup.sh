#!/usr/bin/env bash

set -e
cd "$(dirname "$0")"

echo "========================================="
echo "   Starting Boids Simulation Setup...    "
echo "========================================="

echo "[1/3] Verifying Python3"
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in your PATH."
    exit 1
fi

echo "[2/3] Verifying virtual environment"
if [ ! -d "venv" ]; then
    echo "Virtual environment does not exist, creating now..."
    python3 -m venv venv
fi

echo "[3/3] Installing/updating dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
else
    echo "Error: requirements.txt not found."
    exit 1
fi
echo "              Setup Success!             "
echo "========================================="