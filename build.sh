#!/usr/bin/env bash
# Build script untuk Render.com

set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p app/static/uploads
mkdir -p logs

echo "Build completed successfully!"
