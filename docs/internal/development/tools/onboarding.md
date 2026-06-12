# Developer Onboarding Checklist

## Prerequisites

- [ ] **Python 3.11+** installed and active
  - [ ] Verify with `python --version` (should show 3.11.x)
  - [ ] Verify asyncio.timeout availability: `python -c "import asyncio; asyncio.timeout(1.0)"`
- [ ] **Git** configured with your credentials
- [ ] **Docker** installed and running
- [ ] **IDE/Editor** configured for Python 3.11
  - [ ] VS Code with Python extension
  - [ ] Or PyCharm with Python 3.11 interpreter
- [ ] **GitHub access** to repository

## Environment Setup

- [ ] **Repository cloned**
  ```bash
  git clone https://github.com/yourusername/piper-morgan-platform.git
  cd piper-morgan-platform
  ```
- [ ] **Python 3.11 verified**
  ```bash
  python --version  # Should show Python 3.11.x
  cat .python-version  # Should show 3.11
  ```
- [ ] **Virtual environment created** with Python 3.11
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  # OR venv\Scripts\activate  # Windows
  ```
- [ ] **Dependencies installed** successfully
  ```bash
  pip install -r requirements.txt
  ```
- [ ] **AsyncIO.timeout functionality verified**
  ```bash
  python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 ready')"
  ```

## Development Workflow

- [ ] **Tests pass locally**
  ```bash
  pytest tests/ -v
  ```
- [ ] **Docker containers build** successfully
  ```bash
  docker-compose build
  docker-compose up -d
  ```
- [ ] **Pre-commit hooks installed** and working
  ```bash
  pip install pre-commit
  pre-commit install
  pre-commit install --hook-type pre-push
  pre-commit run --all-files
  ```
  Note: `--hook-type pre-push` installs the release notes enforcement hook for production pushes.
- [ ] **IDE recognizes Python 3.11** type hints
  - [ ] VS Code: Python interpreter set to venv/bin/python
  - [ ] PyCharm: Project interpreter set to Python 3.11

## Validation

- [ ] **Can run application locally**
  ```bash
  python main.py
  # Should start without Python version errors
  ```
- [ ] **Can build and run Docker containers**
  ```bash
  docker-compose exec app python --version  # Should show 3.11.x
  ```
- [ ] **Tests pass in local environment**
  ```bash
  python -m pytest tests/ --tb=short
  ```
- [ ] **AsyncIO features work correctly**
  ```bash
  python -c "
  import asyncio
  async def test_timeout():
      async with asyncio.timeout(1.0):
          await asyncio.sleep(0.1)
  asyncio.run(test_timeout())
  print('✅ AsyncIO.timeout works correctly')
  "
  ```

## Code Quality Tools

- [ ] **Black formatting** works
  ```bash
  black --check .
  ```
- [ ] **isort import sorting** works
  ```bash
  isort --check-only .
  ```
- [ ] **Flake8 linting** passes
  ```bash
  flake8 . --count --exit-zero --max-line-length=100
  ```

## CI/CD Integration

- [ ] **GitHub Actions workflows** are configured
  - [ ] Test workflow uses Python 3.11
  - [ ] Lint workflow uses Python 3.11
  - [ ] Docker workflow validates Python 3.11
- [ ] **Can push changes** to trigger CI
  ```bash
  git add .
  git commit -m "Initial setup"
  git push origin main
  ```

## Documentation Review

- [ ] **README.md** reviewed and understood
- [ ] **Development setup guide** followed
- [ ] **Contributing guidelines** reviewed
- [ ] **Architecture documentation** familiarized
- [ ] **API documentation** reviewed

## Next Steps

- [ ] **Review contributing guidelines** in CONTRIBUTING.md
- [ ] **Set up development branch** for first feature
  ```bash
  git checkout -b feature/your-first-feature
  ```
- [ ] **Complete first development task**
  - [ ] Create a simple test
  - [ ] Make a small code change
  - [ ] Verify tests still pass
  - [ ] Submit a pull request

## Windows Developer Setup

**For Windows developers, we recommend WSL2 for the best experience.**

### Quick Start (Windows with WSL2)

WSL2 provides a native Linux environment on Windows, making development seamless:

```powershell
# 1. Run as Administrator
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# 2. Inside Ubuntu terminal
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3.11-pip git

# 3. Clone and setup (same as Linux)
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Verify setup
pytest tests/ -v
```

**Why WSL2?**
- All bash scripts work natively
- No path separator issues (no `\` vs `/` confusion)
- Python behaves exactly like on Linux
- Actually faster than native Windows
- Seamless integration with Windows tools (VS Code, Git, etc.)

### Alternative: Native Windows Setup

If you prefer not to use WSL2:

1. **Install Python 3.11**: https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
2. **Follow steps in "Environment Setup"** above
3. **Use PowerShell** for all terminal commands
4. **Use backslashes** in file paths: `pytest tests\unit\test_file.py`

See [Windows Setup Guide](../../../installation/windows-setup-guide.md) for detailed setup instructions.

### Cross-Platform Notes

- **Virtual environment activation**:
  - Linux/macOS: `source venv/bin/activate`
  - Windows: `.\venv\Scripts\Activate.ps1`
- **File paths** (if using native Windows):
  - Use backslashes: `tests\unit\test_file.py`
  - Or quote with forward slashes: `"tests/unit/test_file.py"`
- **Pre-commit hooks** prevent commits with Windows-illegal characters (`: < > " | ? *`)

## Troubleshooting

### Common Issues

**Python Version Issues**:

```bash
# If you see: AttributeError: module 'asyncio' has no attribute 'timeout'
python --version  # Check if < 3.11
# Solution: Install and activate Python 3.11
```

**Docker Issues**:

```bash
# If containers fail to build
docker-compose build --no-cache
docker-compose exec app python --version  # Verify 3.11.x
```

**Test Failures**:

```bash
# If tests fail with version errors
python -W error::DeprecationWarning -m pytest tests/
# Check for Python 3.11 compatibility issues
```

**Windows-Specific Issues**:

If using **native Windows** (not WSL2):

1. **Virtual environment activation fails**:
   ```powershell
   # PowerShell execution policy error? Run as Administrator:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Pre-commit hook blocks commit** (illegal filename characters):
   ```powershell
   # Rename file to use dashes instead of colons/quotes
   # Example: "file (10:30).txt" → "file-1030.txt"
   git add .
   git commit -m "Rename file"
   ```

3. **Path errors in tests** (backslash vs forward slash):
   ```powershell
   # Use backslashes
   pytest tests\unit\test_file.py
   # Or quote with forward slashes
   pytest "tests/unit/test_file.py"
   ```

**Recommendation**: If Windows issues persist, **use WSL2** (see Windows Developer Setup above).

### Getting Help

1. **Check this onboarding guide** for common solutions
2. **Review troubleshooting guide** in docs/development/troubleshooting-guide.md
3. **Check PM-055 implementation package** for Python 3.11 details
4. **Ask the team** in GitHub Issues or team chat
5. **Review CI/CD logs** if GitHub Actions fail

## Success Criteria

You're successfully onboarded when:

- [ ] All tests pass with Python 3.11
- [ ] Docker containers build and run correctly
- [ ] You can make code changes and run tests
- [ ] CI/CD workflows pass on your changes
- [ ] You understand the Python 3.11 requirements
- [ ] You can contribute to the project effectively

## Welcome to the Team! 🎉

Once you've completed this checklist, you're ready to contribute to Piper Morgan Platform. The Python 3.11 migration (PM-055) ensures a modern, consistent development environment for all team members.

**Key Benefits of Python 3.11**:

- ✅ Enhanced async/await performance
- ✅ `asyncio.timeout()` functionality
- ✅ Better error messages and debugging
- ✅ Improved type checking support
- ✅ Consistent environment across all contexts
