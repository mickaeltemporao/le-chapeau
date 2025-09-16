#!/bin/bash
# Number of workers you want
WORKERS=4

# Base port (first worker runs on 8501, then 8502, etc.)
BASE_PORT=8501

# Path to your Streamlit app
APP_PATH="/Users/mt/Documents/paper-socrates/main.py"

# Path to virtual environment (adjust to your setup)
VENV_PATH="/Users/mt/Documents/paper-socrates/.venv/bin/streamlit"
   
# Kill any previous workers
pkill -f "streamlit run $APP_PATH"

# Increase file descriptors (important for many connections)
ulimit -n 20000

# Start workers
for i in $(seq 0 $((WORKERS-1))); do
    PORT=$((BASE_PORT+i))
    echo "Starting Streamlit worker on port $PORT"
    nohup $VENV_PATH run $APP_PATH --server.port $PORT --server.address 0.0.0.0 --server.headless true > worker_$PORT.log 2>&1 &
done


# Get the local IP address (LAN)
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

# Get the public IP (WAN, from Free)
PUBLIC_IP=$(curl -s ifconfig.me)

echo "Your Streamlit app is running. Others can connect using the followin IPs."
echo "Local Access  : http://$LOCAL_IP:8501"
echo "Public Access : http://$PUBLIC_IP:8501"

