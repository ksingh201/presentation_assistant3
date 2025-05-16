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

echo "--- AWS Credentials Setup for Script ---"
# Fetch credentials and region using aws configure get and export them
# This makes them available to the Python script's EnvironmentCredentialsResolver
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
export AWS_DEFAULT_REGION=$(aws configure get region)

# Check if they were set (optional debug)
# echo "AWS_ACCESS_KEY_ID is: $AWS_ACCESS_KEY_ID"
# echo "AWS_SECRET_ACCESS_KEY is: $AWS_SECRET_ACCESS_KEY"
# echo "AWS_DEFAULT_REGION is: $AWS_DEFAULT_REGION"
echo "-------------------------------------"

echo "Running Python script..."
python3 modified_nova_sonic_simple.py

echo "Deactivating virtual environment..."
deactivate 