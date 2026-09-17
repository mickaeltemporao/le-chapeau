#!/bin/bash
set -e

# Le Chapeau: Turnkey Deployment Assistant for Researchers
# Works on macOS and Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "  🎓 Bienvenue sur Le Chapeau - Assistant de Déploiement   "
echo "=========================================================="
echo ""

# Ensure data and config directories exist
mkdir -p data/logs data/exports config

# Ensure sample user file exists if users.txt is missing
if [ ! -f "data/users.txt" ]; then
    if [ -f "data/users.example.txt" ]; then
        echo "ℹ️  Aucun fichier data/users.txt trouvé. Copie de data/users.example.txt..."
        cp data/users.example.txt data/users.txt
    fi
fi

# Ensure salt exists for anonymization
if [ ! -f "config/salt.txt" ]; then
    if [ -f "config/salt.example.txt" ]; then
        cp config/salt.example.txt config/salt.txt
    fi
fi

# Increase file descriptor limits for high concurrency
if [ "$(uname)" = "Darwin" ] || [ "$(uname)" = "Linux" ]; then
    ulimit -n 20000 2>/dev/null || true
fi

# Function to get Local Network IP
get_local_ip() {
    if command -v ipconfig &>/dev/null; then
        ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || hostname -I | awk '{print $1}'
    elif command -v hostname &>/dev/null; then
        hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1"
    else
        echo "127.0.0.1"
    fi
}

LOCAL_IP=$(get_local_ip)

# Check deployment options
HAS_DOCKER=false
if command -v docker &>/dev/null && docker compose version &>/dev/null; then
    HAS_DOCKER=true
fi

echo "Options de déploiement :"
echo "1) Lancement standard avec 'uv' (Recommandé - simple et direct)"
if [ "$HAS_DOCKER" = true ]; then
    echo "2) Lancement avec Docker Compose (Isolé en conteneur)"
fi
echo ""

read -p "Votre choix [1] : " CHOICE
CHOICE=${CHOICE:-1}

if [ "$CHOICE" = "2" ] && [ "$HAS_DOCKER" = true ]; then
    echo ""
    echo "🐳 Démarrage du conteneur Docker..."
    docker compose up -d --build
    echo ""
    echo "=========================================================="
    echo "  🎉 Le Chapeau est EN LIGNE (Docker) !"
    echo "  Lien d'accès étudiant :"
    echo "    ➡️  http://$LOCAL_IP:8501"
    echo "    ➡️  http://localhost:8501"
    echo ""
    echo "  Pour arrêter le conteneur : docker compose down"
    echo "=========================================================="
    exit 0
fi

# Native execution with uv
if ! command -v uv &>/dev/null; then
    echo ""
    echo "⚠️  L'outil 'uv' n'est pas encore installé sur cette machine."
    echo "Installation automatique de 'uv' en cours..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo ""
echo "📦 Synchronisation des dépendances Python..."
uv sync

echo ""
echo "=========================================================="
echo "  🎉 Le Chapeau démarre !"
echo "  Lien d'accès à partager aux étudiants :"
echo "    ➡️  http://$LOCAL_IP:8501"
echo "    ➡️  http://localhost:8501"
echo ""
echo "  (Appuyez sur Ctrl+C dans ce terminal pour arrêter l'application)"
echo "=========================================================="
echo ""

uv run streamlit run src/chapeau/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
