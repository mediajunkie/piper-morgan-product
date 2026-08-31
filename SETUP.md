# Piper Morgan Developer Setup Guide

Complete step-by-step guide to set up the Piper Morgan development environment.

> **Not a developer?** If you're an alpha tester who just wants to try Piper Morgan, see [ALPHA_QUICKSTART.md](docs/ALPHA_QUICKSTART.md) instead. This guide is for contributors who want to modify the codebase.

> ⚠️ **Overlap note, added 2026-08-31 (#1708)**: `CONTRIBUTING.md` §"1b. Running the Full App
> Locally" now also covers this setup, with steps that are probe-measured against a real fresh
> clone rather than assumed. This doc's factual errors found by that same probe (wrong config
> file, wrong psql command, wrong server entry point) are corrected below, but the two docs
> substantially overlap now and a consolidation decision is still open — see #1708. If they ever
> disagree, trust `CONTRIBUTING.md`'s §1b as the more recently verified source.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or 3.12 only** (pinned dependencies have no 3.13/3.14 builds — probe-measured,
  2026-08-31, see `CONTRIBUTING.md` §1b)
  - Check: `python --version`
  - Install: https://www.python.org/downloads/

- **Git**
  - Check: `git --version`
  - Install: https://git-scm.com/downloads

- **Docker & Docker Compose** (optional, for local database)
  - Check: `docker --version`
  - Install: https://www.docker.com/products/docker-desktop

- **PostgreSQL** (local install) OR Docker
  - If local: PostgreSQL 12+
  - If Docker: Included in docker-compose setup

- **VSCode** (recommended editor)
  - Download: https://code.visualstudio.com/

## Step 1: Clone the Repository

```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

## Step 2: Open in VSCode

```bash
code .
```

This will automatically:
- Detect the Python environment
- Suggest installing recommended extensions (see `.vscode/extensions.json`)
- Load workspace settings (see `.vscode/settings.json`)

## Step 3: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat
```

**Verify**: `which python` (or `where python` on Windows) should show path in `venv/`

## Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Verify
python --version  # Should be 3.11 or 3.12 (see Prerequisites)
pip list | grep pytest  # Should see pytest
```

## Step 5: Set Up Environment Variables

```bash
cp .env.example .env
```

> ⚠️ **Corrected 2026-08-31** — this step previously said `cp config/PIPER.example.md config/PIPER.md`.
> `config/PIPER.example.md` doesn't exist and never has (verified against the current tree); the
> generic config template is `config/PIPER.defaults.md`, and it's read automatically — you don't
> copy it. The actual per-developer file to create is `.env` from `.env.example`.

Key settings to configure in `.env`:
- `PIPER_PORT`: Default 8001 (non-default only if you need to run multiple instances)
- An Anthropic or OpenAI API key (the `/setup` wizard also collects this on first run — see Step 8)

*(Unverified this pass — not part of Lead's 2026-08-31 probe, may need its own check:
`SLACK_BOT_TOKEN` / `NOTION_TOKEN` for optional integrations.)*

## Step 6: Set Up Database

### Option A: Local PostgreSQL

```bash
# Create database
createdb piper_morgan

# Run migrations
source venv/bin/activate
alembic upgrade head
```

### Option B: Docker PostgreSQL

```bash
# Start database container
docker compose up -d
```
> ⚠️ **Added 2026-08-31** (probe-measured, see `CONTRIBUTING.md` §1b): the compose project/container
> names are fixed, not per-checkout. A second checkout on this machine will silently commandeer the
> first one's containers rather than erroring — don't run two Piper checkouts against Docker on one
> machine without changing the project name.
```bash
# Run migrations
source venv/bin/activate
alembic upgrade head
```

**Verify**:
```bash
# Option A (local Postgres): your own local defaults — typically your OS user, port 5432.
psql piper_morgan

# Option B (Docker): corrected 2026-08-31 — this used to say the same bare command as Option A,
# which doesn't match the container's actual config (host port 5433, user "piper").
psql -h localhost -p 5433 -U piper piper_morgan
```

## Step 7: Run Tests

```bash
# Verify setup by running tests
source venv/bin/activate

# Unit tests only
pytest tests/unit/ -v

# All tests
pytest tests/ -v

# Current file (in VSCode)
# Use Debug: "Python: Pytest (Current File)"
```

**Expected**: Tests should pass (or show known failures documented in issues)

## Step 8: Start Development Server

### Option A: Command Line

```bash
source venv/bin/activate
python main.py
```
> ⚠️ **Corrected 2026-08-31** — this used to say `python -m uvicorn web.app:app --reload --port
> 8001`. `main.py`'s own docstring states it directly: *"This is the proper way to start Piper
> Morgan."* Set `PIPER_PORT` in `.env` if you need a non-default port.

### Option B: VSCode Debugger

1. Open `.vscode/launch.json`
2. Select "Python: FastAPI (Piper Morgan)" from Run menu
3. Press F5 or click "Run"

**Verify**: Visit http://localhost:8001

## Step 9: VSCode Setup (Recommended)

### Install Extensions

VSCode will suggest recommended extensions automatically. Or install manually:

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Black Formatter** (ms-python.black-formatter)
- **GitLens** (eamodio.gitlens)
- **YAML** (redhat.vscode-yaml)
- **TOML** (tamasfe.even-better-toml)

### Configure Debug Launcher

The `.vscode/launch.json` includes pre-configured debug configurations:

- **Python: FastAPI** - Start dev server with debugger
- **Python: Pytest (Current File)** - Debug current test
- **Python: Pytest (All Unit Tests)** - Run all unit tests

### Use Tasks for Common Operations

Open Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`):

- `Tasks: Run Task` → "Start Piper Server"
- `Tasks: Run Task` → "Run Unit Tests"
- `Tasks: Run Task` → "Format Code (Black)"
- `Tasks: Run Task` → "Lint Code (Flake8)"

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version

# If wrong version, use explicit python3.11 (if installed)
python3.11 -m venv venv
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
# Local install: psql piper_morgan (your own defaults)
# Docker: psql -h localhost -p 5433 -U piper piper_morgan (see Step 6, Option B)

# If using Docker:
docker compose ps  # Check if container is running
docker compose logs db  # Check logs
```

### VSCode Not Recognizing Python

1. Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: "Python: Select Interpreter"
3. Choose the one in `./venv/bin/python`

### Migrations Failing

```bash
# Check current migration status
alembic current

# Rollback to specific version if needed
alembic downgrade <revision>

# Re-apply migrations
alembic upgrade head
```

## Quick Reference

> ⚠️ **Reminder**: Activate your virtual environment each time you open a new terminal!

| Task | Command | VSCode Alternative |
|------|---------|-------------------|
| Activate venv (Mac/Linux) | `source venv/bin/activate` | Auto on open |
| Activate venv (Windows) | `.\venv\Scripts\Activate.ps1` | Auto on open |
| Install deps | `pip install -r requirements.txt` | Task: "Install Dependencies" |
| Run tests | `pytest tests/unit/ -v` | Debug: "Pytest (Current File)" |
| Start server | `python main.py` | Debug: "FastAPI" |
| Format code | `black .` | Task: "Format Code (Black)" |
| Run linter | `flake8 .` | Task: "Lint Code (Flake8)" |
| Database setup | `alembic upgrade head` | Task: "Database: Setup" |

## Next Steps

1. ✅ Environment set up
2. ✅ Dependencies installed
3. ✅ Database configured
4. ✅ Tests passing

**Ready to contribute!**

- Check `docs/NAVIGATION.md` for project documentation
- See `docs/internal/architecture/adrs/` for architectural decisions
- Review open issues in GitHub for tasks to work on

## Support

- **Issues**: Check GitHub issues for known problems
- **Documentation**: See `docs/` directory
- **Architecture**: See `docs/internal/architecture/current/`
- **Patterns**: See `docs/internal/architecture/patterns/`

## References

- **Project Structure**: `docs/briefing/PROJECT.md`
- **Contributing Guide**: Check repository for CONTRIBUTING.md
- **Development Methodology**: `docs/internal/development/methodology-core/`
- **Architecture Decisions**: `docs/internal/architecture/adrs/`
