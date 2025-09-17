#!/bin/bash

# Path to your Streamlit app
APP_PATH="/Users/mt/Documents/paper-socrates/main.py"

# Path to virtual environment
VENV_PATH="/Users/mt/Documents/paper-socrates/.venv/bin/streamlit"

# Kill any previous instance
pkill -f "streamlit run $APP_PATH"

# Increase file descriptors
ulimit -n 20000

# Start a single worker on port 8501
nohup $VENV_PATH run $APP_PATH --server.port 8501 --server.address 0.0.0.0 --server.headless true > worker_8501.log 2>&1 &

# Get the local IP address (LAN)
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

# Get the public IP (WAN, from Free)
PUBLIC_IP=$(curl -s ifconfig.me)

echo "Your Streamlit app is running. Others can connect using the followin IPs."
echo "Local Access  : http://$LOCAL_IP:8501"
echo "Public Access : http://$PUBLIC_IP:8501"

