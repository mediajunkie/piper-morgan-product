# Development Environment Setup

## Python 3.11 Installation

### Using pyenv (Recommended)

```bash
# Install pyenv (if not already installed)
# macOS
brew install pyenv

# Install Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9

# Verify installation
python --version  # Should show Python 3.11.9
```

### Using asdf

```bash
# Install asdf (if not already installed)
# macOS
brew install asdf

# Install Python 3.11
asdf install python 3.11.9
asdf local python 3.11.9

# Verify installation
python --version  # Should show Python 3.11.9
```

### Direct Installation

#### macOS

```bash
brew install python@3.11
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

#### Windows

Download Python 3.11 from [python.org](https://www.python.org/downloads/)

## Virtual Environment Setup

```bash
# Create virtual environment with Python 3.11
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Verify Python version in venv
python --version  # Should show Python 3.11.x
```

## Dependency Installation

```bash
# Install development dependencies
pip install -r requirements.txt

# Verify key packages
python -c "import fastapi, sqlalchemy, pytest, asyncio"
python -c "asyncio.timeout(1.0); print('✅ asyncio.timeout available')"
```

## Docker Setup

```bash
# Build Docker containers with Python 3.11
docker-compose build

# Start services
docker-compose up -d

# Verify container Python version
docker-compose exec app python --version  # Should show Python 3.11.x
```

## Common Issues and Solutions

### Python Version Mismatch

**Problem**: `AttributeError: module 'asyncio' has no attribute 'timeout'`

**Solution**: Ensure Python 3.11+ is active. Check with `python --version`

```bash
# Check current Python version
python --version

# If < 3.11, activate correct version
pyenv local 3.11.9  # or asdf local python 3.11.9
source venv/bin/activate  # reactivate virtual environment

# Verify fix
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Fixed')"
```

### Docker Issues

**Problem**: Container uses wrong Python version

**Solution**: Rebuild containers with Python 3.11 base

```bash
# Rebuild with no cache
docker-compose build --no-cache

# Verify container Python version
docker-compose exec app python --version  # Should show 3.11.x
```

### CI/CD Failures

**Problem**: GitHub Actions fails with Python version errors

**Solution**: Workflows now specify Python 3.11 - should auto-resolve

```bash
# Check workflow configuration
cat .github/workflows/test.yml | grep "python-version"

# Should show: python-version: '3.11'
```

### Virtual Environment Issues

**Problem**: Virtual environment created with wrong Python version

**Solution**: Delete and recreate with correct Python version

```bash
# Remove old virtual environment
rm -rf venv

# Create new with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Verify version
python --version  # Should show 3.11.x
```

### Dependency Installation Issues

**Problem**: Package installation fails with version conflicts

**Solution**: Ensure clean environment and correct Python version

```bash
# Deactivate and reactivate virtual environment
deactivate
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Environment Validation

### Quick Validation Script

```bash
#!/bin/bash
echo "=== Python Environment Validation ==="

# Check Python version
echo "Python version: $(python --version)"

# Check asyncio.timeout availability
python -c "import asyncio; asyncio.timeout(1.0); print('✅ asyncio.timeout available')"

# Check key dependencies
python -c "import fastapi, sqlalchemy, pytest; print('✅ Key dependencies available')"

# Check virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected"
fi

echo "=== Validation Complete ==="
```

### Docker Validation

```bash
#!/bin/bash
echo "=== Docker Environment Validation ==="

# Check container Python version
echo "Container Python version:"
docker-compose exec app python --version

# Check container dependencies
echo "Container dependencies:"
docker-compose exec app python -c "import fastapi, sqlalchemy; print('✅ Container dependencies OK')"

echo "=== Docker Validation Complete ==="
```

## IDE Configuration

### VS Code

1. **Select Python Interpreter**:

   - `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - "Python: Select Interpreter"
   - Choose Python 3.11 from virtual environment

2. **Install Python Extension**:

   - Install "Python" extension by Microsoft
   - Install "Pylance" for enhanced type checking

3. **Configure Settings**:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.linting.enabled": true,
     "python.formatting.provider": "black"
   }
   ```

### PyCharm

1. **Configure Project Interpreter**:

   - File → Settings → Project → Python Interpreter
   - Add interpreter → Existing environment
   - Select `./venv/bin/python`

2. **Configure Code Style**:
   - File → Settings → Editor → Code Style → Python
   - Set line length to 100 (matches project black config)

## Pre-commit Setup

```bash
# Install pre-commit hooks (pre-commit and pre-push)
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push

# Run pre-commit on all files
pre-commit run --all-files
```

**Note**: The `--hook-type pre-push` installs the release notes enforcement hook, which ensures release notes exist in `docs/releases/` when pushing version changes to production.

## Testing Setup

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/services/ -v  # Service tests
pytest tests/integration/ -v  # Integration tests

# Run with Python 3.11 specific checks
python -W error::DeprecationWarning -m pytest tests/
```

## Next Steps

After completing setup:

1. **Verify Environment**: Run validation scripts above
2. **Run Tests**: Ensure all tests pass with Python 3.11
3. **Start Development**: Begin working on features
4. **Check Documentation**: Review [Contributing Guidelines](../../../CONTRIBUTING.md)

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review the PM-055 Implementation Package *(dead link removed 2026-09-02 — no file at this or
   any other path in the repo; likely never committed or lost in an early reorg)*
3. Check [GitHub Issues](https://github.com/yourusername/piper-morgan-platform/issues)
4. Contact the development team
