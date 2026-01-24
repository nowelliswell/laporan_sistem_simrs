#!/bin/bash
set -e

echo "🚀 Starting BAP SIMRS..."

# Initialize database
echo "📦 Initializing database..."
python init_db.py

# Get port from environment or use default
PORT=${PORT:-8000}

# Start gunicorn
echo "🌐 Starting web server on port $PORT..."
exec gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile -
