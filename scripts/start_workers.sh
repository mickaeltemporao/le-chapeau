#!/bin/bash
set -e

# Dynamically locate project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_PATH="$PROJECT_ROOT/src/chapeau/app.py"
BASE_PORT=8501
WORKERS=${WORKERS:-4}

echo "🎓 Starting Le Chapeau multi-worker cluster ($WORKERS workers)..."

# Ensure directories exist
mkdir -p data/logs

# Terminate any existing instances
"$PROJECT_ROOT/scripts/stop_workers.sh" || true

# Increase file descriptors
if [ "$(uname)" = "Darwin" ] || [ "$(uname)" = "Linux" ]; then
    ulimit -n 20000 2>/dev/null || true
fi

# Launch each worker process
for i in $(seq 0 $((WORKERS - 1))); do
    PORT=$((BASE_PORT + i))
    LOG_FILE="$PROJECT_ROOT/data/logs/worker_${PORT}.log"
    echo "  -> Spawning worker on port $PORT (log: data/logs/worker_${PORT}.log)"

    nohup uv run streamlit run "$APP_PATH" \
        --server.port "$PORT" \
        --server.address 0.0.0.0 \
        --server.headless true \
        --server.enableCORS false \
        --server.enableXsrfProtection false \
        --browser.gatherUsageStats false \
        > "$LOG_FILE" 2>&1 &
done

LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")

echo ""
echo "=========================================================="
echo "  ✅ All $WORKERS Streamlit workers have been started."
echo "  With Nginx reverse proxy enabled (port 80):"
echo "    http://$LOCAL_IP"
echo ""
echo "  Direct worker access (e.g. Worker 1):"
echo "    http://$LOCAL_IP:$BASE_PORT"
echo ""
echo "  To stop all workers: ./scripts/stop_workers.sh"
echo "=========================================================="
