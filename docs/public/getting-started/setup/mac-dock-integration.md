# Mac Dock Integration for One-Click Startup

> **Rewritten 2026-09-02 (Docs, #1611)**: this doc previously had two problems, either one enough
> to block using it as-is. First, it was framed entirely around PM's own personal "6:00 AM PT
> standup" routine — not something an alpha tester or contributor has. Second, its startup script
> launched what it described as two separate processes (`main.py` on port 8001 and a second
> `web/app.py`/`uvicorn` process on port 8081) — a nearly-year-old architecture. **Confirmed
> directly**: `main.py` runs `web.app:app` internally via uvicorn on a single port; there is no
> separate frontend process, and CLAUDE.md's own quick reference agrees (`python main.py # Start
> server (port 8001)`, "Entry point: `main.py` (not `web/app.py`)"). Rewritten below against the
> real single-process architecture, with generic "one-click startup" framing instead of PM's own
> routine.

## Overview

This guide adds Piper Morgan to your Mac dock for one-click startup — launch the server with a
single click instead of typing a command every time.

## 🎯 Benefits

- **One-Click Startup**: Launch Piper Morgan with a single dock click
- **Zero Configuration**: No manual setup required after initial configuration
- **Professional Appearance**: Clean dock icon representing Piper Morgan
- **Health Check Integration**: Automatic service validation on startup

## 📋 Prerequisites

### System Requirements

- **macOS**: 10.15 (Catalina) or later
- **Docker Desktop**: Must be running before startup (for PostgreSQL/Redis)
- **Git**: For repository access and updates
- **Terminal**: Built-in macOS Terminal app

### Piper Morgan Setup

- Repository cloned to local machine
- Python virtual environment configured
- PostgreSQL and Redis accessible (via Docker Compose — see `SETUP.md`)

## 🚀 Setup Instructions

### Step 1: Create Startup Script

```bash
# Navigate to your Piper Morgan directory
cd /path/to/piper-morgan

# Create the startup script
cat > start-piper.sh << 'EOF'
#!/bin/bash

# Piper Morgan One-Click Startup Script
# Purpose: Launch Piper Morgan with health checks

set -e  # Exit on any error

echo "🚀 Starting Piper Morgan..."
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
if [ ! -f "main.py" ]; then
    echo "❌ Not in Piper Morgan directory"
    echo "Please navigate to your piper-morgan directory and try again"
    exit 1
fi

echo "✅ Piper Morgan directory confirmed"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    echo "Please run: python -m venv venv && source venv/bin/activate"
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

# Start the server (main.py runs the app internally — one process, port 8001)
echo "🚀 Starting Piper Morgan server..."
nohup python main.py > logs/piper.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for the server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Check server health
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Server is healthy"
else
    echo "❌ Server health check failed"
    echo "Check logs/piper.log for details"
    exit 1
fi

# Create PID file for management
echo "$SERVER_PID" > .piper.pid

echo "🎉 Piper Morgan is ready!"
echo "================================"
echo "🌐 Open: http://localhost:8001/"
echo "📊 Health: http://localhost:8001/health"
echo ""
echo "🔄 To stop: ./stop-piper.sh"

# Open browser
open http://localhost:8001/
EOF

# Make the script executable
chmod +x start-piper.sh
```

### Step 2: Create Stop Script

```bash
# Create the stop script
cat > stop-piper.sh << 'EOF'
#!/bin/bash

# Piper Morgan Stop Script
# Purpose: Clean shutdown of the Piper Morgan server

echo "🛑 Stopping Piper Morgan..."
echo "================================"

if [ -f ".piper.pid" ]; then
    SERVER_PID=$(cat .piper.pid)
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo "🛑 Stopping server (PID: $SERVER_PID)..."
        kill $SERVER_PID
        echo "✅ Server stopped"
    else
        echo "ℹ️  Server already stopped"
    fi
    rm -f .piper.pid
else
    echo "ℹ️  No PID file found"
fi

# Clean up any remaining process
pkill -f "python main.py" 2>/dev/null || true

echo "✅ Piper Morgan stopped successfully"
echo "================================"
EOF

# Make the stop script executable
chmod +x stop-piper.sh
```

### Step 3: Create Logs Directory

```bash
mkdir -p logs
echo "✅ Logs directory created"
```

### Step 4: Add to Mac Dock

#### Option A: Drag and Drop (Recommended)

1. **Open Finder** and navigate to your Piper Morgan directory
2. **Drag the `start-piper.sh` file** to your Mac dock
3. **Right-click the dock icon** and select "Options" → "Keep in Dock"
4. **Customize the icon** (optional — see Customization section below)

#### Option B: Create Application Bundle

For a more professional appearance, create an application bundle:

```bash
mkdir -p "Piper Morgan.app/Contents/MacOS"
mkdir -p "Piper Morgan.app/Contents/Resources"

cp start-piper.sh "Piper Morgan.app/Contents/MacOS/Piper Morgan"
chmod +x "Piper Morgan.app/Contents/MacOS/Piper Morgan"

cat > "Piper Morgan.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Piper Morgan</string>
    <key>CFBundleIdentifier</key>
    <string>com.piper-morgan.startup</string>
    <key>CFBundleName</key>
    <string>Piper Morgan</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
EOF

echo "✅ Application bundle created"
```

### Step 5: Test the Integration

```bash
./start-piper.sh
curl http://localhost:8001/health
./stop-piper.sh
```

## 🎨 Customization

### Custom Dock Icon

1. Create or download a 512x512 PNG icon
2. Convert to ICNS format using Icon Composer or online tools
3. Replace the icon in your application bundle:

```bash
cp your-icon.icns "Piper Morgan.app/Contents/Resources/AppIcon.icns"
# Add to Info.plist:
# <key>CFBundleIconFile</key>
# <string>AppIcon.icns</string>
```

## 🔧 Troubleshooting

### Docker Desktop Not Running

```bash
open -a Docker
```

### Port Already in Use

```bash
./stop-piper.sh
# Or find and kill the process directly
lsof -ti:8001 | xargs kill -9
```

### Virtual Environment Issues

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Denied

```bash
chmod +x start-piper.sh
chmod +x stop-piper.sh
```

### Log Analysis

```bash
tail -f logs/piper.log
```

### Health Check Commands

```bash
curl http://localhost:8001/health
ps aux | grep "main.py"
lsof -i :8001
```

## 📱 Daily Usage

### Starting

1. Click the Piper Morgan dock icon
2. Wait for startup completion (usually 15-30 seconds)
3. Your browser opens automatically to http://localhost:8001/

### Stopping

1. Run `./stop-piper.sh`
2. Verify the process stopped (`ps aux | grep "main.py"` shows nothing)

### Quick Restart

```bash
./stop-piper.sh && sleep 2 && ./start-piper.sh
```

## 🔄 Maintenance

### Regular Updates

```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
./stop-piper.sh
./start-piper.sh
```

### Log Rotation

```bash
find logs/ -name "*.log" -mtime +7 -delete
```

## 🔗 Related Documentation

- **[Troubleshooting Guide](../../../installation/troubleshooting.md)** — Common issues and solutions
- **[Architecture Overview](../../README.md#architecture-overview)** — System design and components

## 📞 Support

- **Repository**: [piper-morgan-product](https://github.com/mediajunkie/piper-morgan-product)
- **Issue Template**: Use "Bug Report" for technical issues
- **Main Site**: [pmorgan.tech](https://pmorgan.tech)

---

**Last Updated**: September 2, 2026 (Docs, #1611) — rewritten against the current single-process
architecture; PM's personal-routine framing replaced with generic one-click-startup language.
