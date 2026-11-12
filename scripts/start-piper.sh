#!/bin/bash

# Piper Morgan One-Click Startup Script
# Version: 1.1.0 (Cross-platform)
# Purpose: Launch Piper Morgan with health checks
# Supports: macOS, Linux, Windows (Git Bash/WSL)

set -e  # Exit on any error

# Source OS detection library
# Resolve symlinks to find actual script location
SCRIPT_PATH="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
    SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
    [[ $SCRIPT_PATH != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
# shellcheck source=lib/os-detect.sh
source "$SCRIPT_DIR/lib/os-detect.sh"

# Configuration - use environment variables with sensible defaults
export ENVIRONMENT="${ENVIRONMENT:-development}"
export BACKEND_PORT="${BACKEND_PORT:-8001}"
export WEB_PORT="${WEB_PORT:-8081}"
# xian, 2026-11-12: "default them to the database store." Credentials come from the
# encrypted database store, never the login keychain, unless PIPER_CREDENTIAL_STORE=keychain
# is set on purpose (xian's own permission; a seat never sets it). Both processes this
# script starts inherit it.
export PIPER_CREDENTIAL_STORE="${PIPER_CREDENTIAL_STORE:-db}"

echo "🚀 Starting Piper Morgan..."
echo "🔧 Environment: $ENVIRONMENT"
echo "🔧 Backend Port: $BACKEND_PORT"
echo "🌐 Web Port: $WEB_PORT"
echo "🔐 Credential store: $PIPER_CREDENTIAL_STORE"
echo "================================"

# Check if Docker Desktop is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker Desktop is not running"
    echo "Please start Docker Desktop and try again"
    echo "You can find Docker Desktop in your Applications folder"
    exit 1
fi

echo "✅ Docker Desktop is running"

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "web/app.py" ]; then
    echo "❌ Not in Piper Morgan directory"
    echo "Please navigate to your piper-morgan directory and try again"
    exit 1
fi

echo "✅ Piper Morgan directory confirmed"

# Activate virtual environment (cross-platform)
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    if activate_venv "venv"; then
        echo "✅ Virtual environment activated"
    else
        echo "❌ Failed to activate virtual environment"
        exit 1
    fi
else
    echo "❌ Virtual environment not found"
    if is_windows; then
        echo "Please run: python -m venv venv && .\\venv\\Scripts\\activate"
    else
        echo "Please run: python -m venv venv && source venv/bin/activate"
    fi
    exit 1
fi

# Check Python dependencies
echo "🔍 Checking Python dependencies..."
if ! python -c "import services" > /dev/null 2>&1; then
    echo "❌ Python dependencies not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Python dependencies verified"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start backend services
echo "🚀 Starting backend services..."
echo "Starting main.py in background..."
nohup python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check backend health
if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "Check logs/backend.log for details"
    exit 1
fi

# Start frontend
echo "🌐 Starting frontend..."
echo "Starting web frontend with uvicorn..."
# Export environment variables to ensure they're passed to subprocess
export GITHUB_TOKEN="$GITHUB_TOKEN"
nohup bash -c "export GITHUB_TOKEN='$GITHUB_TOKEN' && export ENVIRONMENT='$ENVIRONMENT' && export WEB_PORT='$WEB_PORT' && export BACKEND_PORT='$BACKEND_PORT' && cd web && python -m uvicorn app:app --host 0.0.0.0 --port \$WEB_PORT" > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 3

# Check frontend health
if curl -s http://localhost:$WEB_PORT/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    echo "Check logs/frontend.log for details"
    exit 1
fi

# Create PID file for management
echo "$BACKEND_PID" > .piper-backend.pid
echo "$FRONTEND_PID" > .piper-frontend.pid

echo "🎉 Piper Morgan is ready!"
echo "================================"

# Branch management reminder
echo ""
echo "🌿 Branch Management Reminder:"
echo "================================"
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "📍 Current Branch: $CURRENT_BRANCH"
    if [ "$CURRENT_BRANCH" = "main" ]; then
        echo "⚠️  Working on main branch - consider feature branch for development"
        echo "📚 See: docs/development/BRANCH-MANAGEMENT.md"
    elif [[ "$CURRENT_BRANCH" == feature/* ]]; then
        echo "✅ Good! Working on feature branch"
    elif [[ "$CURRENT_BRANCH" == dev/* ]]; then
        echo "🔬 Development branch - experiments and research"
    fi
    echo "📋 Quick guidance: ./scripts/branch-guidance.sh"
fi
echo "🌐 Frontend: http://localhost:$WEB_PORT/"
echo "🔧 Backend: http://localhost:$BACKEND_PORT/"
echo "📊 Health: http://localhost:$WEB_PORT/health"
echo ""
echo "💡 Tip: Bookmark http://localhost:$WEB_PORT/ for quick access"
echo "🔄 To stop: ./stop-piper.sh"
echo ""
echo "🚀 Ready for your 6:00 AM PT standup!"

# Open browser (cross-platform)
if ! open_browser "http://localhost:$WEB_PORT/"; then
    : # Browser opening failed, but script already notified user
fi

# Show Windows warning if on Windows
warn_windows_limitations
