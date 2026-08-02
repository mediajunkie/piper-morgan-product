#!/bin/bash
# MCP Development Environment Setup Script
# Prepares environment for PM-033a MCP Consumer Core implementation

echo "🚀 MCP Monday Infrastructure Setup"
echo "=================================="
echo "Setting up development environment for aggressive MCP sprint"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

# Check Python version
echo "📋 Checking Python environment..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "   Python version: $PYTHON_VERSION"
    print_status 0 "Python installed"
else
    print_status 1 "Python not found"
    exit 1
fi

# Check virtual environment
echo ""
echo "📋 Checking virtual environment..."
if [ -d "venv" ]; then
    print_status 0 "Virtual environment exists"
    source venv/bin/activate
    print_status 0 "Virtual environment activated"
else
    print_status 1 "Virtual environment not found"
    echo "   Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    print_status 0 "Virtual environment created and activated"
fi

# Install/upgrade MCP dependencies
echo ""
echo "📦 Installing MCP dependencies..."

# Check if mcp package needs installation
pip show mcp > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "   Installing mcp package..."
    pip install mcp==1.0.0
    print_status $? "MCP package installed"
else
    print_status 0 "MCP package already installed"
fi

# Install additional protocol dependencies
echo "   Installing protocol dependencies..."
pip install -q pydantic httpx websockets asyncio

# Create MCP development structure
echo ""
echo "🏗️ Creating MCP development structure..."

# Create consumer core directory
if [ ! -d "services/mcp/consumer" ]; then
    mkdir -p services/mcp/consumer
    print_status 0 "Created services/mcp/consumer/"

    # Create initial files
    touch services/mcp/consumer/__init__.py
    touch services/mcp/consumer/protocol_client.py
    touch services/mcp/consumer/tool_federation.py
    touch services/mcp/consumer/resource_discovery.py
    touch services/mcp/consumer/auth_integration.py
    print_status 0 "Created consumer core files"
else
    print_status 0 "Consumer directory already exists"
fi

# Create test structure
if [ ! -d "tests/integration/mcp" ]; then
    mkdir -p tests/integration/mcp
    touch tests/integration/mcp/__init__.py
    touch tests/integration/mcp/test_mcp_consumer_reality.py
    print_status 0 "Created MCP test structure"
else
    print_status 0 "MCP test structure exists"
fi

# Set up configuration
echo ""
echo "⚙️ Setting up MCP configuration..."

# Copy MCP environment template if .env doesn't have MCP settings
if [ -f ".env" ]; then
    grep -q "MCP_CLIENT_ENABLED" .env
    if [ $? -ne 0 ]; then
        echo "" >> .env
        echo "# MCP Configuration (added by setup script)" >> .env
        cat .env.mcp.example >> .env
        print_status 0 "Added MCP configuration to .env"
    else
        print_status 0 "MCP configuration already in .env"
    fi
else
    cp .env.example .env
    cat .env.mcp.example >> .env
    print_status 0 "Created .env with MCP configuration"
fi

# Create JWT keys directory if needed
echo ""
echo "🔐 Setting up JWT keys directory..."
if [ ! -d "keys" ]; then
    mkdir -p keys
    print_status 0 "Created keys/ directory for JWT"
    echo "   ⚠️  Remember to generate JWT keys for production"
else
    print_status 0 "Keys directory exists"
fi

# Check Docker services
echo ""
echo "🐳 Checking Docker services..."
if command_exists docker; then
    docker ps | grep -q piper-postgres
    if [ $? -eq 0 ]; then
        print_status 0 "PostgreSQL running"
    else
        print_status 1 "PostgreSQL not running - run 'docker-compose up -d'"
    fi

    docker ps | grep -q piper-redis
    if [ $? -eq 0 ]; then
        print_status 0 "Redis running"
    else
        print_status 1 "Redis not running - run 'docker-compose up -d'"
    fi
else
    print_status 1 "Docker not installed"
fi

# Create MCP development launcher
echo ""
echo "🚀 Creating MCP development launcher..."
cat > scripts/run_mcp_dev.sh << 'EOF'
#!/bin/bash
# MCP Development Server Launcher

echo "🚀 Starting MCP Consumer Development Server"
source venv/bin/activate
export MCP_DEV_MODE=true
export MCP_CLIENT_ENABLED=true
export MCP_DEV_VERBOSE_LOGGING=true
export PYTHONPATH=.

echo "Starting with MCP consumer mode enabled..."
python main.py
EOF

chmod +x scripts/run_mcp_dev.sh
print_status 0 "Created scripts/run_mcp_dev.sh"

# Summary
echo ""
echo "=================================="
echo "📊 MCP Development Setup Summary"
echo "=================================="
echo ""
echo "✅ Environment ready for PM-033a implementation"
echo ""
echo "📁 Structure created:"
echo "   - services/mcp/consumer/ (protocol client)"
echo "   - tests/integration/mcp/ (reality testing)"
echo "   - .env.mcp.example (configuration template)"
echo "   - scripts/run_mcp_dev.sh (dev launcher)"
echo ""
echo "🔄 Next steps:"
echo "   1. Start services: docker-compose up -d"
echo "   2. Activate venv: source venv/bin/activate"
echo "   3. Run dev server: ./scripts/run_mcp_dev.sh"
echo "   4. Begin PM-033a implementation"
echo ""
echo "📚 Documentation:"
echo "   - Architecture: docs/internal/architecture/current/adrs/adr-070-mcp-consumer-connector-architecture.md"
echo "   - ADR-012: docs/internal/architecture/current/adrs/adr-012-protocol-ready-jwt-authentication.md"
echo ""
echo "🎯 Ready for aggressive Monday MCP sprint!"
