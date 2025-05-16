#!/bin/bash
# Script to set up venv, install requirements, and run modified_nova_sonic_simple.py
cd "$(dirname "$0")"

VENV_DIR=".venv-nova-sample"

echo "Checking for existing virtual environment..."
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment: $VENV_DIR"
    rm -rf "$VENV_DIR"
fi

echo "Creating new virtual environment: $VENV_DIR"
python3 -m venv "$VENV_DIR"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment."
    exit 1
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: Virtual environment could not be activated."
    exit 1
fi
echo "Virtual environment activated: $VIRTUAL_ENV"

echo "Installing dependencies from requirements.txt..."
# Use python3 -m pip to ensure we're using the venv's pip
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies."
    exit 1
fi

echo "Running Python script..."
python3 modified_nova_sonic_simple.py

echo "Deactivating virtual environment..."
deactivate 