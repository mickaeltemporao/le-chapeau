#!/bin/bash

# Path to your Streamlit app
APP_PATH="/Users/mt/Documents/paper-socrates/main.py"
# Base port (first worker runs on 8501, then 8502, etc.)
BASE_PORT=8501
# Number of workers you want
WORKERS=4

# Kill all processes running the Streamlit app
pkill -f "streamlit run $APP_PATH"

# Optionally, kill any processes using the specified ports
for i in $(seq 0 $((WORKERS-1))); do
    PORT=$((BASE_PORT+i))
    PID=$(lsof -ti :$PORT)
    if [ -n "$PID" ]; then
        echo "Killing process on port $PORT (PID: $PID)"
        kill -9 $PID
    fi
done

echo "All Streamlit workers have been terminated."
