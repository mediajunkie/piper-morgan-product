#!/bin/bash

##############################################################################
# Alpha Tester One-Line Setup for Piper Morgan
#
# Usage:
#   bash <(curl -s https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/production/scripts/alpha-setup.sh)
#
# Or if you already have the repo:
#   ./scripts/alpha-setup.sh
#
# This script automates the setup process for alpha testers:
# 1. Clones the repository (if needed)
# 2. Creates Python virtual environment
# 3. Installs dependencies
# 4. Generates JWT secret key
# 5. Creates .env file
# 6. Starts Docker containers
# 7. Launches the GUI setup wizard
#
# Requirements:
#  - Git
#  - Python 3.11 or 3.12
#  - Docker
#  - Bash/Zsh shell
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check for required tools
check_requirements() {
    print_step "Checking requirements..."

    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "Python 3.11+ not found"
        echo "   Install from: https://www.python.org/downloads/"
        exit 1
    fi

    # Determine python command
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ ! "$PYTHON_VERSION" =~ ^3\.(11|12) ]]; then
        print_error "Python $PYTHON_VERSION found, but 3.11 or 3.12 required"
        exit 1
    fi
    print_success "Python $PYTHON_VERSION found"

    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git not found"
        echo "   Install from: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found"
        echo "   Install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    print_success "Docker found"
}

# Clone repository if needed
clone_repo_if_needed() {
    if [ ! -d ".git" ]; then
        print_step "Cloning Piper Morgan repository..."
        git clone -b production https://github.com/mediajunkie/piper-morgan-product.git piper-morgan-product
        cd piper-morgan-product
        print_success "Repository cloned"
    else
        print_success "Repository already cloned"
    fi
}

# Create Python virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        print_step "Creating Python virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi

    # Activate virtual environment
    print_step "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_deps() {
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi

    print_step "Installing Python dependencies..."
    pip install --quiet --upgrade pip setuptools
    pip install --quiet -r requirements.txt
    print_success "Dependencies installed"
}

# Generate JWT secret and create .env
setup_env() {
    if [ ! -f ".env" ]; then
        print_step "Setting up environment configuration..."

        # Copy .env.example if it exists
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success ".env created from template"
        else
            # Create minimal .env
            touch .env
            print_success ".env created"
        fi

        # Generate JWT secret if not already in .env
        if ! grep -q "JWT_SECRET_KEY" .env; then
            print_step "Generating secure JWT secret key..."
            JWT_SECRET=$(openssl rand -hex 32)
            echo "JWT_SECRET_KEY=$JWT_SECRET" >> .env
            print_success "JWT secret added to .env"
        fi
    else
        print_success ".env already exists"
    fi
}

# Start Docker containers
start_docker() {
    print_step "Starting Docker containers..."

    if ! docker ps > /dev/null 2>&1; then
        print_error "Docker daemon not running"
        echo "   Start Docker Desktop and try again"
        exit 1
    fi

    if [ -f "docker-compose.yml" ]; then
        # Issue #644: Check docker-compose exit code to catch startup failures
        # Issue 2386: start the three data services by name, never the whole file. A
        # second copy on this machine sets PIPER_STACK and its ports in .env first
        # (see the head of docker-compose.yml); compose reads them from there.
        if docker-compose up -d postgres redis chromadb; then
            print_success "Docker containers started"
            print_warning "Waiting 5 seconds for services to initialize..."
            sleep 5
        else
            print_error "Failed to start Docker containers"
            echo "   Common causes:"
            echo "   - Docker daemon connection issues (restart Docker Desktop)"
            echo "   - Port conflicts (check: docker-compose ps)"
            echo "   - Network issues (check: docker network ls)"
            echo ""
            echo "   To see detailed logs: docker-compose logs"
            exit 1
        fi
    else
        print_warning "docker-compose.yml not found, skipping Docker startup"
    fi
}

# Start the application
start_app() {
    print_step "Launching Piper Morgan GUI setup wizard..."
    echo ""
    echo "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo "${GREEN}  Piper Morgan is starting...${NC}"
    echo "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "The setup wizard will open in your browser automatically."
    echo "If it doesn't, visit: ${BLUE}http://localhost:8001/setup${NC}"
    echo ""
    print_step "Starting server (press Ctrl+C to stop)..."
    echo ""

    $PYTHON_CMD main.py
}

# Main flow
main() {
    echo ""
    echo "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo "${BLUE}║${NC}     Piper Morgan Alpha Tester Setup Script             ${BLUE}║${NC}"
    echo "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    check_requirements
    clone_repo_if_needed
    setup_venv
    install_deps
    setup_env
    start_docker
    start_app
}

# Run main function
main "$@"
