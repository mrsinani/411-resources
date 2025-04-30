#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Determine the script directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install or upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create a lock file
echo "Generating requirements.lock..."
pip freeze > requirements.lock

echo "Setup complete. To activate the virtual environment, run:"
echo "source .venv/bin/activate" 