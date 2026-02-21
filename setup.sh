#!/bin/bash
# ─────────────────────────────────────────────
#  ChurnGuard — Project Setup & Launch Script
# ─────────────────────────────────────────────

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}✅ $1${NC}"; }
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

echo ""
echo -e "${BLUE}🎮 ChurnGuard — Player Churn Prediction System${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 1. Check prerequisites ───
info "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install it first."
    exit 1
fi

log "Python $(python3 --version | cut -d' ' -f2), Node $(node --version), npm $(npm --version)"

# ─── 2. Python virtual environment ───
info "Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    log "Virtual environment created"
else
    log "Virtual environment already exists"
fi

source venv/bin/activate

# ─── 3. Install Python dependencies ───
info "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r backend/requirements.txt
log "Python packages installed"

# ─── 4. Train the ML model (if not already trained) ───
if [ ! -f "backend/models/churn_model.pkl" ]; then
    info "Training ML model (first time)..."
    python -m backend.ml.train
    log "Model trained and saved"
else
    log "Model already trained — skipping"
fi

# ─── 5. Install frontend dependencies ───
info "Installing frontend dependencies..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install --silent 2>/dev/null || npm install --ignore-scripts --silent
    log "Frontend packages installed"
else
    log "Frontend packages already installed"
fi

cd ..

# ─── 6. Start both servers ───
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Starting servers..."
echo ""

# Start FastAPI backend
source venv/bin/activate
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Next.js frontend
cd frontend
node node_modules/next/dist/bin/next dev --port 3000 &
FRONTEND_PID=$!
cd ..

# Wait for servers to start
sleep 3

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Both servers are running!"
echo ""
echo -e "  🔵 Frontend  → ${BLUE}http://localhost:3000${NC}"
echo -e "  🟢 Backend   → ${GREEN}http://localhost:8000${NC}"
echo -e "  📄 API Docs  → ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  Press ${YELLOW}Ctrl+C${NC} to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cleanup on exit
cleanup() {
    echo ""
    info "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    log "Servers stopped. Goodbye!"
}

trap cleanup EXIT INT TERM

# Keep script alive
wait
