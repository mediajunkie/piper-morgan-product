# Contributing Guidelines

## Development Requirements

### Python Version

- **Required**: Python **3.11 or 3.12 only** — not 3.13 or 3.14. Pinned dependencies have no
  builds for newer versions (verified via a fresh-clone probe, 2026-08-31; `requirements.txt`'s
  pip wall is the first failure a newcomer on a newer Python hits).
- **Recommended**: Python 3.12 (latest of the two supported versions)

All development must be compatible with Python 3.11. Key features we rely on:

- `asyncio.timeout()` (Python 3.11+ feature)
- Enhanced error messages
- Performance improvements

### Code Quality

- All code must pass with Python 3.11
- Use Python 3.11+ type hints where beneficial
- Async/await patterns must be Python 3.11 compatible

### Testing

```bash
# All tests must pass with Python 3.11
python --version  # Verify 3.11+
pytest tests/ -v

# Check for Python 3.11 compatibility
python -W error::DeprecationWarning -m pytest tests/
```

## Development Workflow

### 1. Environment Setup

```bash
# Ensure Python 3.11 is active
python --version  # Should show 3.11.x

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify Python 3.11 features
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 ready')"
```

### 1b. Running the Full App Locally

*Added 2026-08-31, moved from `docs/ALPHA_QUICKSTART.md` — testers now use the hosted app
([piper-morgan.fly.dev](https://piper-morgan.fly.dev)), so this is an engineer/contributor path,
not a tester one. Steps below are probe-measured (Lead, 2026-08-31 fresh-clone test), not
assumed — see #1708.*

⚠️ **Clone `main`, never `production`.** `production` is not a deploy source (CI builds on `main`)
and drifts stale with no warning — see `docs/internal/planning/release-model.md`.

```bash
# 1. Clone and set up Python (see 1. Environment Setup above for the venv steps)
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # ~5-10 min cold; requires Python 3.11 or 3.12 (see above)
cp .env.example .env

# 2. Start the local infrastructure — ONE stack per machine
docker compose up -d
# → PostgreSQL on host port 5433, Redis, ChromaDB.
# ⚠️ The compose project/container names are fixed, not per-checkout. A second checkout on the
#    same machine silently commandeers the first one's containers rather than erroring — don't
#    run two Piper checkouts against Docker on one machine without changing the project name.

# 3. Migrate and launch
alembic upgrade head
python main.py
# → Fresh-clone measured: healthy server in ~13s with ZERO API keys configured. It warns, then
#    302s you to /setup, where the wizard collects an Anthropic or OpenAI key. Without a key the
#    server runs but chat won't work — the wizard tells you this rather than failing silently.
```

**If startup hangs silently** at `"Validating LLM providers..."` on macOS: that's a Keychain ACL
dialog for your new Python binary, and it's invisible in a headless/background terminal. Click
**Always Allow** once (a GUI dialog is waiting behind your terminal), or set
`PIPER_CREDENTIAL_STORE=db` to skip Keychain entirely.

**Visit `/setup`** to configure API keys and create your account through the GUI wizard (health
checks, key entry, account creation, confirmation) — or run `python main.py setup` for the
equivalent CLI flow. Both configure the same settings.

### 2. Code Quality Checks

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 . --count --exit-zero --max-line-length=100

# Run pre-commit hooks
pre-commit run --all-files
```

### 3. Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/services/ -v  # Service tests
pytest tests/integration/ -v  # Integration tests

# Run with Python 3.11 specific checks
python -W error::DeprecationWarning -m pytest tests/
```

### 4. Known Test Failures Workflow

Piper Morgan uses a **known-failures tracking system** to allow pushes even when some tests are failing, as long as those failures are:
1. **Documented** with clear reason
2. **Tracked** in a bead (issue tracker)
3. **Time-boxed** with expiry date
4. **Categorized** (TDD spec, known bug, or deferred)

#### How It Works

The pre-push hook will:
1. Run the fast test suite (`./scripts/run_tests.sh fast`)
2. If tests fail, check against `.pytest-known-failures`
3. Allow push if all failures are known
4. Block push if new failures are detected
5. Warn about expired or resolved failures

#### Adding a Known Failure

If you need to push with a failing test that's tracked in a bead:

```bash
# Edit .pytest-known-failures file
nano .pytest-known-failures
```

Add an entry following this format:

```yaml
- test_path: "tests/unit/path/to/test_file.py::TestClass::test_method"
  reason: "Clear explanation of why this test is failing"
  bead: "piper-morgan-xyz"  # Must be a valid bead ID
  expires: "2025-12-20"      # Max 30 days from creation
  category: "tdd_spec"       # or "known_bug" or "deferred"
```

**Categories:**
- `tdd_spec`: Test-driven development spec (expected to fail until implementation)
- `known_bug`: Known bug tracked in bead, fix planned
- `deferred`: Work deferred to later sprint, tracked in bead

**Rules:**
- All entries MUST have bead references (for tracking)
- Expiry dates MUST be within 30 days
- Expired entries cause WARNING (not block) - update or remove them
- Resolved tests (now passing) should be removed from the file

#### Validating Known Failures Manually

```bash
# Test the known-failures validation
python scripts/filter_known_failures.py

# Should output:
# ✅ All failures are known - push allowed
# OR
# ❌ NEW FAILURES DETECTED (BLOCKING PUSH)
```

#### Common Scenarios

**Scenario 1: TDD Workflow**
```yaml
- test_path: "tests/unit/services/test_new_feature.py::TestNewFeature::test_method"
  reason: "TDD - NewFeature.method() not implemented yet"
  bead: "piper-morgan-abc"
  expires: "2025-12-15"
  category: "tdd_spec"
```

**Scenario 2: Known Bug**
```yaml
- test_path: "tests/unit/services/test_service.py::TestService::test_edge_case"
  reason: "Bug - service crashes on empty input, tracked for fix"
  bead: "piper-morgan-def"
  expires: "2025-12-10"
  category: "known_bug"
```

**Scenario 3: Deferred Work**
```yaml
- test_path: "tests/integration/test_complex_flow.py::test_end_to_end"
  reason: "Deferred - integration test needs mock data setup"
  bead: "piper-morgan-ghi"
  expires: "2025-12-20"
  category: "deferred"
```

#### Best Practices

✅ **DO:**
- Create a bead BEFORE adding to known-failures
- Use clear, descriptive reasons
- Set realistic expiry dates (max 30 days)
- Remove entries when tests are fixed
- Review warnings about expired entries

❌ **DON'T:**
- Add failures without bead tracking
- Use vague reasons like "broken" or "fails sometimes"
- Set distant expiry dates (>30 days)
- Leave resolved tests in the file
- Ignore expiry warnings

### 5. Docker Validation

```bash
# Build and test Docker containers
docker compose build
docker compose up -d

# Verify container Python version
docker compose exec app python --version  # Should show 3.11.x

# Run tests in container
docker compose exec app pytest tests/ -v
```

## Pull Request Requirements

### Before Submitting

- [ ] **Code runs successfully** with Python 3.11
- [ ] **All tests pass** with Python 3.11
- [ ] **No deprecation warnings** introduced
- [ ] **Docker builds work** with Python 3.11 base images
- [ ] **Documentation updated** if adding Python 3.11+ features
- [ ] **Code formatted** with Black and isort
- [ ] **Linting passes** with flake8
- [ ] **Interface + experience verification (#683 two-layer DoD)** — *for any change that adds/modifies a user-facing surface or a service interface*: **Layer A** — a methodology-30 Consumer-Trace shows the real behavior is reachable by an actual consumer (not just declared/scaffolded upstream); **Layer B** — the delivered experience passes the Colleague Test (or branched rubric) + conforms to its MUX-doc intent. Both hard-gate the surface's committed scope; out-of-scope misses file discovered-work. See `docs/internal/development/interface-verification-dod-layer-a.md` + `experience-verification-dod-layer-b.md`. *(Skip for purely internal changes with no user-facing surface / consumer-relationship.)*

### Pull Request Template

```markdown
## Description

Brief description of changes

## Python Version Compatibility

- [ ] Tested with Python 3.11+
- [ ] No Python version-specific issues introduced
- [ ] AsyncIO.timeout functionality preserved (if applicable)

## Testing

- [ ] All tests pass locally
- [ ] Docker containers build successfully
- [ ] CI/CD workflows pass

## Documentation

- [ ] README.md updated (if needed)
- [ ] Code comments added for complex logic
- [ ] API documentation updated (if applicable)

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] No console.log or debug statements left
- [ ] Error handling implemented appropriately
- [ ] Interface + experience verification (#683 two-layer DoD) — Layer A Consumer-Trace + Layer B experience pass, if this touches a user-facing surface or service interface
```

## Code Style Guidelines

### Python 3.11 Best Practices

```python
# Use asyncio.timeout() for async operations
import asyncio

async def example_function():
    async with asyncio.timeout(5.0):  # Python 3.11+ feature
        await some_async_operation()

# Use enhanced error messages
try:
    result = await operation()
except Exception as e:
    raise RuntimeError(f"Operation failed: {e}") from e

# Use type hints with Python 3.11 features
from typing import Annotated

def process_data(data: Annotated[dict, "User input data"]) -> dict:
    return {"processed": data}
```

### Async/Await Patterns

```python
# Prefer async context managers
async def resource_management():
    async with asyncio.timeout(10.0):
        async with aiofiles.open('file.txt') as f:
            content = await f.read()
    return content

# Use proper error handling
async def robust_operation():
    try:
        async with asyncio.timeout(5.0):
            result = await external_api_call()
        return result
    except asyncio.TimeoutError:
        logger.warning("Operation timed out")
        return None
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

## Windows Development

### Repository Cloning on Windows

Piper Morgan repositories use cross-platform filenames validated by both local pre-commit hooks and GitHub Actions CI/CD. **If you encounter clone failures on Windows**, this is likely due to illegal filename characters.

**Windows cannot use these characters in filenames**: `: < > " | ? *`

Our pre-commit hooks prevent these characters from being committed. If an older version somehow has them:

```powershell
# Clone with a different branch strategy
git clone --no-checkout https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
git checkout main  # or your target branch
```

### WSL2 Recommendation for Windows Developers

**Why WSL2?**
- Native Linux environment without VM overhead
- Direct filesystem access to Windows
- Full Python 3.11 support
- All bash scripts work without modification
- Git operations are faster

**Installation Steps:**

1. **Enable WSL2** (Windows 10/11):
   ```powershell
   # Run as Administrator
   wsl --install
   wsl --set-default-version 2
   ```

2. **Install Ubuntu**:
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

3. **From inside Ubuntu terminal**, set up development environment:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python 3.11
   sudo apt install python3.11 python3.11-venv python3.11-pip git

   # Clone repository (using WSL terminal)
   git clone https://github.com/mediajunkie/piper-morgan-product.git
   cd piper-morgan-product

   # Continue with normal setup (see Environment Setup section above)
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Access from Windows**:
   - WSL files are available at: `\\wsl$\Ubuntu-22.04\home\<username>\`
   - Edit files from Windows with WSL paths: `code \\wsl$\Ubuntu-22.04\home\username\piper-morgan-product`

### Native Windows Setup (PowerShell)

If you prefer native Windows development:

1. **Install Python 3.11**:
   ```powershell
   # Using Windows Package Manager (recommended)
   winget install Python.Python.3.11

   # Or download from https://www.python.org/downloads/
   # During installation, MUST check "Add Python to PATH"
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify Python 3.11**:
   ```powershell
   python --version  # Should show Python 3.11.x
   ```

### Pre-commit Hooks on Windows

The `check-windows-filenames` hook prevents commits with illegal Windows characters automatically:

```bash
# This will be blocked by pre-commit hook:
# "❌ Pre-commit hook: Windows-illegal characters found in filenames"
# Windows filenames cannot contain: : < > " | ? *
# Use dashes (-) or underscores (_) instead.

# To bypass (not recommended):
git commit --no-verify
```

### Common Windows Development Issues

**Problem**: "command not found" errors in bash scripts
**Solution**: Use WSL2 (recommended) or ensure PowerShell scripts use proper syntax

**Problem**: Virtual environment activation fails
**Solution**: Use correct activation script for Windows:
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

**Problem**: File paths with spaces causing errors
**Solution**: Wrap paths in quotes:
```powershell
python -m pytest "tests\my test\test_file.py"
```

**Problem**: `git clone` fails partway through with `Filename too long`
**Solution**: Some `mailboxes/` memo filenames are long by convention (they encode sender,
recipient, and subject inline) and can overflow Windows' 260-character `MAX_PATH` once the
clone-destination path is added. Enable long-path support (per-repo or globally):
```
git config --global core.longpaths true
```
If that isn't enough, Windows itself also needs long paths enabled at the OS level — see
`docs/internal/operations/github-and-tooling-gotchas.md` ("Windows: `git clone` fails with
'Filename too long'") for the registry setting and full detail. New `mailboxes/` filenames are
capped going forward (#1616); existing long ones are intentionally left as historical record.

### GitHub Actions: Windows Validation

GitHub Actions automatically validates repository compatibility on Windows via the `windows-clone-test` job. This ensures:

- ✅ Repository clones successfully on Windows
- ✅ No illegal filename characters present
- ✅ All files transfer without corruption

This validation runs on every push to main/develop branches.

## Common Issues and Solutions

### Python Version Issues

**Problem**: `AttributeError: module 'asyncio' has no attribute 'timeout'`
**Solution**: Ensure Python 3.11+ is active

```bash
python --version  # Check version
pyenv local 3.11.9  # Set correct version
source venv/bin/activate  # Reactivate environment
```

### Docker Issues

**Problem**: Container tests fail with version errors
**Solution**: Rebuild with Python 3.11 base

```bash
docker-compose build --no-cache
docker-compose exec app python --version  # Verify 3.11+
```

### CI/CD Failures

**Problem**: GitHub Actions fail with Python compatibility
**Solution**: Workflows updated to use Python 3.11 - clear cache and retry

### Running the app locally — port, database, and environment issues

*Moved from `docs/ALPHA_QUICKSTART.md`, 2026-08-31 (#1708).*

**Port 8001 already taken?**
```bash
lsof -i :8001 && kill -9 [PID]
```

**Database/migration errors** (e.g. "column does not exist"):
```bash
alembic upgrade head          # from an activated venv
docker ps | grep postgres     # confirm piper-postgres is running on 5433

# Full reset (WARNING: deletes all local data):
docker compose down -v && docker compose up -d && alembic upgrade head
```

**`localhost:8001` doesn't load on Windows, but `127.0.0.1:8001` does**: Windows can resolve
`localhost` to IPv6 (`::1`) while Piper binds IPv4 (`127.0.0.1`) — use the IP form.

**`.env` missing after a `git pull`?** It won't be — `.env` is gitignored and git never touches
it. If you never created one: `cp .env.example .env`, then set `JWT_SECRET_KEY` (generate with
`openssl rand -hex 32`).

**Commands not found in a new terminal?** Your venv deactivated when the terminal closed —
`source venv/bin/activate` (or the Windows equivalent above) and try again.

## Review Process

### Code Review Checklist

- [ ] **Python 3.11 compatibility** verified
- [ ] **Async patterns** follow best practices
- [ ] **Error handling** is appropriate
- [ ] **Tests** cover new functionality
- [ ] **Documentation** is clear and complete
- [ ] **Performance** considerations addressed
- [ ] **Security** implications considered

### Review Guidelines

- Be constructive and specific
- Focus on code quality and Python 3.11 compatibility
- Consider async/await patterns and error handling
- Verify that new code doesn't introduce version-specific issues

## Getting Help

### Resources

- [Development Setup Guide](docs/development/setup.md)
- [Onboarding Checklist](docs/development/onboarding.md)
- [PM-055 Implementation Package](docs/development/pm-055-step1-implementation-package.md)
- [Architecture Documentation](docs/architecture/)

### Support Channels

- GitHub Issues for bug reports
- Team chat for quick questions
- Code review comments for specific feedback

## Thank You! 🎉

Thank you for contributing to Piper Morgan Platform! Your contributions help make this project better for everyone. The Python 3.11 migration ensures a modern, consistent development experience.
