#!/bin/bash

# Dynamically locate project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_PATH="$PROJECT_ROOT/src/chapeau/app.py"
BASE_PORT=8501
WORKERS=${WORKERS:-4}

echo "🛑 Stopping Le Chapeau Streamlit workers..."

# Kill any processes running this app
pkill -f "streamlit run.*chapeau" 2>/dev/null || true

# Kill any processes using the worker ports
for i in $(seq 0 $((WORKERS - 1))); do
    PORT=$((BASE_PORT + i))
    PID=$(lsof -ti :$PORT 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo "  Killing process on port $PORT (PID: $PID)"
        kill -9 $PID 2>/dev/null || true
    fi
done

echo "✅ All Streamlit workers have been terminated."
