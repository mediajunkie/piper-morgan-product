# Piper Morgan Alpha - Quick Start

**Version**: 0.8.9.1
**Branch**: `production` (stable alpha releases)
**For**: Experienced developers who want to dive in fast

> 📍 **Branch Info**: This quickstart uses the `production` branch, which receives stable alpha releases. The `main` branch is for active development and may have bugs.

⚠️ **If you hit issues, see `ALPHA_TESTING_GUIDE.md` for comprehensive troubleshooting.**

---

## Time & Storage Requirements

| Step | First Run | Subsequent Runs |
|------|-----------|-----------------|
| Clone repository | 1-2 min (~91MB with --depth 1) | N/A |
| Install Python packages | 5-10 min (~216 packages, ~1GB) | 1-2 min |
| Docker image download | 10-30 min (~4GB, depends on connection) | Skipped if cached |
| Database migrations | 1-2 min | 30 sec |
| Setup wizard | 2-5 min | N/A |
| **Total (first time)** | **20-50 minutes** | **5-10 min** |

**Storage Requirements**:
- Docker images: ~4GB
- Python packages: ~1GB
- Database: ~100MB (grows with usage)
- **Total**: ~6GB free disk space recommended

---

## What's New in 0.8.9

This release closes three fronts: connector infrastructure (RECONNECT WS-1), field-level security, and the Design D2 token system and mobile nav.

**Connector infrastructure (RECONNECT WS-1)** — Connector config now lives in the database, not a JSON file or in-memory store. Repo config and integration state survive restarts. When GitHub isn't connected, Piper says so honestly rather than guessing or failing silently.

**Real standup pipeline** — The hollow standup workflow is retired. `StandupAssembler` is the real thing: it pulls from live connector data, Radar sources, and your context. Ask Piper for your standup in chat; the `/api/v1/standup/today` endpoint is the canonical path.

**Field encryption** — User secrets are now encrypted at rest using AES-256-GCM with HKDF per-field key derivation. Your API keys in the database are encrypted, not plaintext. This is the first-generation implementation of the security architecture.

**Per-user LLM key routing** — Your BYOC API key (brought via Settings in D1) is now routed per-request. Each inference call uses your key when present, falling back to the server key. The BYOC credential flow is end-to-end complete.

**Auth hardening** — The `admin_compose` route is removed. The auth exemption list is now lint-enforced: any new exemption requires an explicit rationale, or CI fails.

**Design D2 — token system + mobile nav** — The design token system is fully applied to the app shell. The responsive shell adapts across viewport widths. Mobile nav is implemented (hamburger → drawer), not just tolerated.

**Documents → Radar** — The "Documents" nav label is renamed to "Radar" throughout. Standup content and work items are now first-class Radar data sources.

**Dockerfile → bookworm** — The production Dockerfile upgrades to Debian 12 (bookworm) to satisfy chromadb's SQLite ≥3.35 requirement.

**Database Migration Required**: Run `alembic upgrade head` after updating (includes secret-column encryption migration).

See [Release Notes v0.8.9](releases/RELEASE-NOTES-v0.8.9.md) for full details.

---

## Choose Your Path

| I want to... | Use this guide | Time |
|--------------|----------------|------|
| **Try Piper Morgan** (alpha testing) | This guide (ALPHA_QUICKSTART.md) | 20-50 min |
| **Develop/contribute code** | [SETUP.md](../SETUP.md) | 30-60 min |

> 🔮 **Future**: A hosted version and Docker Hub images are planned for 2026, which will enable a true "5-minute setup" for users who just want to run Piper. For now, all paths require the developer setup.

---

## Prerequisites

- Python 3.11 or 3.12, Docker, Git installed and working
- OpenAI or Anthropic API key ready
- Terminal comfort (for initial clone and install)

---

## Automated Setup (Recommended for Alpha Testers)

**For macOS/Linux/WSL2:**
```bash
# Fast clone (~91MB instead of ~800MB) - recommended for alpha testers
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/alpha-setup.sh
# Script will:
# → Check requirements (Python 3.11/3.12, Docker, Git)
# → Create virtual environment
# → Install dependencies
# → Generate JWT secret automatically
# → Start Docker containers
# → Launch the setup wizard at http://localhost:8001/setup
```

**For Windows (Command Prompt or PowerShell):**
```cmd
REM Fast clone (~91MB instead of ~800MB) - recommended for alpha testers
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
REM Script will:
REM → Check requirements (Python 3.11/3.12, Docker, Git)
REM → Create virtual environment
REM → Install dependencies
REM → Generate JWT secret automatically
REM → Start Docker containers
REM → Launch the setup wizard at http://localhost:8001/setup
```

---

## Manual Setup (If You Prefer Full Control)

```bash
# 1. Clone and setup (~2-3 min)
# --depth 1 gives you a fast ~91MB download (vs ~800MB full history)
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.12 -m venv venv && source venv/bin/activate
# Requires Python 3.11 or 3.12 - verify with: python --version

# 2. Install dependencies (~5-10 min first time, 216 packages)
python -m pip install --upgrade pip
pip install -r requirements.txt
# ☕ This downloads ~1GB of packages - good time for a coffee break

# 3. Configure environment variables (~1 min)
cp .env.example .env
# Edit .env and set JWT_SECRET_KEY:
# Generate a secure key: openssl rand -hex 32
# Add to .env: JWT_SECRET_KEY=your-generated-key-here
# Note: .env is gitignored and survives git pull operations

# 4. Start Docker containers (~10-30 min first time)
docker compose up -d
# First run downloads ~4GB of images (PostgreSQL, Redis, etc.)
# ☕ Another good coffee break opportunity
# Subsequent runs: instant (images are cached)

# 5. Run database migrations (~1-2 min)
python -m alembic upgrade head
# This creates/updates all database tables

# 6. Start server for first-time setup
python main.py
# → Opens http://localhost:8001/setup (GUI setup wizard)

# 7. Complete setup wizard (~2-5 min)
# → Navigate through visual setup screens
# → Configure API keys, create user account
# → See "Setup Wizard Walkthrough" below for details

# 8. Configure preferences (optional, ~2 min)
python main.py preferences
# → Answer 5 questions about your work style
# → Or skip and configure later via Settings page

# 9. Validate installation (optional)
python scripts/validate_install.py
# → Checks all components are working
# → Shows clear pass/fail status
```

---

## Setup Wizard Walkthrough (New in 0.8.2)

The GUI setup wizard guides you through configuration with a visual interface:

### Step 1: Welcome Screen
The setup wizard welcome screen explains what will be configured and gives you a clear starting point.

<img src="./assets/images/alpha-onboarding/setup-wizard-welcome.png" alt="Setup wizard welcome screen" width="600">

### Step 2: System Health Check
Automatic validation of your system:
- ✓ Docker installed and running
- ✓ Python version correct
- ✓ Port 8001 available
- ✓ Database accessible

<img src="./assets/images/alpha-onboarding/setup-wizard-health-check.png" alt="Setup wizard health check" width="600">

### Step 3: API Key Configuration
Configure your LLM API keys through a form interface. Much easier than pasting in the terminal - you can see what you're typing, correct mistakes, and get immediate validation feedback.

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google Gemini

<img src="./assets/images/alpha-onboarding/setup-wizard-api-keys.png" alt="Setup wizard API key configuration" width="600">

### Step 4: User Account Creation
Create your admin account:
- Username and email
- Secure password (min 8 chars, bcrypt-hashed)
- Confirmation and validation

<img src="./assets/images/alpha-onboarding/setup-wizard-user-creation.png" alt="Setup wizard user account creation" width="600">

### Step 5: Setup Complete
Setup confirmation with next steps and quick links to start using Piper.

<img src="./assets/images/alpha-onboarding/setup-wizard-success.png" alt="Setup wizard success screen" width="600">

---

## Alternative: Command-Line Setup

If you prefer the original command-line setup wizard:

```bash
python main.py setup
# → Follow prompts for:
#    - Username and email
#    - Secure password (min 8 chars, bcrypt-hashed)
#    - API keys (OpenAI/Anthropic/Gemini)
```

Both methods configure the same settings. Use whichever you're comfortable with.

---

## First Commands to Try

### Via Chat Interface
```bash
# In Piper's chat interface:
"Hello, what can you help me with?"
"Add a todo: Test Piper Morgan"
"What tasks do I have?"
"Upload a document and summarize it"
```

### Via UI Features

After logging in to http://localhost:8001:

1. **Lists Management** → Click "Lists" → "Create New List"
   - Add list name and description
   - Try sharing with another user (if multi-user testing)

2. **Todos Management** → Click "Todos" → "Create New Todo"
   - Full CRUD operations

3. **File Upload/Download** → Click "Files" → Upload a file
   - Supports: PDF, DOCX, TXT, MD, JSON (max 10MB)
   - Download and delete files

4. **Daily Standup** → Click "Standup" → "Generate Standup"
   - AI-powered standup generation (2-3 seconds)

5. **Logout** → Click user menu (top right) → "Logout"
   - Token revocation and logout working

6. **Permission Management** → Try conversational commands:
   - "share my project plan with alex@example.com as editor"
   - "who can access my shopping list?"

---

## Testing Focus for 0.8.9

**What's Stable** (light testing recommended):
- ✅ Setup wizard (GUI and CLI)
- ✅ Login/authentication
- ✅ Lists, Todos, Projects management
- ✅ Files upload/download/preview/tagging
- ✅ Integration Dashboard and OAuth connections
- ✅ Slack outbound, DMs, @-mentions
- ✅ Radar as default home workspace
- ✅ Conscious Floor (honest no-context responses)

**Where to Focus Testing** (these need your attention):
- 🔍 **Connector config persistence**: Configure a GitHub repo, restart the server — does it remember the config?
- 🔍 **Honest no-repo UX**: Remove or skip GitHub config — does Piper tell you it's not connected rather than guessing?
- 🔍 **Standup via chat**: Ask "what's my standup?" in the chat interface — does `StandupAssembler` return a real response?
- 🔍 **BYOC key routing**: Enter your API key in Settings, make a few requests — confirm your key is being used (check your provider's usage dashboard if unsure)
- 🔍 **Mobile nav**: Open Piper on a phone or narrow browser window — does the hamburger → drawer nav work?
- 🔍 **Radar rename**: Is "Radar" (not "Documents") the label throughout the nav and page headers?

---

## If Something Breaks

### Docker not running?

```bash
docker --version  # Should show version
docker ps         # Should show containers
# If not: Start Docker Desktop
```

### Port 8001 taken?

```bash
lsof -i :8001     # See what's using it
kill -9 [PID]     # Kill it
```

### Database/migration issues?

```bash
# If setup wizard fails with "column does not exist" error:
python -m alembic upgrade head

# If alembic command not found (not in venv):
source venv/bin/activate
alembic upgrade head

# Verify database is running:
docker ps | grep postgres
# Should show: piper-postgres running on port 5433

# Reset database completely (WARNING: deletes all data):
docker compose down -v
docker compose up -d
python -m alembic upgrade head
```

### API key issues?

```bash
# Web UI method (easier):
# Navigate to http://localhost:8001/setup
# Re-enter your API keys in the form

# Or command-line method:
python main.py setup  # Re-run setup wizard
python main.py status # Verify keys
```

### Login issues?

```bash
# Forgot password? Re-run setup to create new account
python main.py setup

# Can't access http://localhost:8001?
# Check server is running: python main.py
# Try: http://127.0.0.1:8001
```

### Windows: localhost doesn't work?

**Problem**: `http://localhost:8001` gives connection error, but `http://127.0.0.1:8001` works.

**Why**: Windows may resolve `localhost` to IPv6 (`::1`) while Piper binds to IPv4 (`127.0.0.1`).

**Solution**: Use `http://127.0.0.1:8001` instead of `localhost:8001` on Windows.

### Environment variables not loading after git pull?

```bash
# Your .env file is gitignored and NEVER deleted by git operations
# If you see JWT_SECRET_KEY warnings after pulling new code:

# 1. Verify .env exists:
ls -la .env

# 2. If missing, CREATE it (this is required for all setups):
cp .env.example .env

# Edit .env in your IDE or text editor and add:
# JWT_SECRET_KEY=<paste-generated-key-here>

# Generate the key:
openssl rand -hex 32

# 3. Restart server:
python main.py

# Note: .env survives git pull, checkout, merge - git never touches it
# If you never created .env, that's the issue - Step 2 above is mandatory
# The setup wizard stores API keys separately (in secure keyring)
```

### Commands not found after restarting terminal?

If `python main.py` gives errors like "No module named..." or commands aren't found:

```bash
# You need to reactivate your virtual environment!
# The venv deactivates when you close your terminal.

# Mac/Linux:
cd piper-morgan-product
source venv/bin/activate

# Windows PowerShell:
cd piper-morgan-product
.\venv\Scripts\Activate.ps1

# Windows Command Prompt:
cd piper-morgan-product
venv\Scripts\activate.bat

# Your prompt should now show (venv) - try your command again
python main.py
```

---

## Key Commands Reference

> ⚠️ **Important**: All commands must be run inside an activated virtual environment!
>
> **Activate venv each time you open a new terminal:**
> ```bash
> # Mac/Linux:
> source venv/bin/activate
>
> # Windows PowerShell:
> .\venv\Scripts\Activate.ps1
>
> # Windows Command Prompt:
> venv\Scripts\activate.bat
> ```
> Your prompt should show `(venv)` when activated.

```bash
python main.py              # Start server (opens browser automatically)
python main.py setup        # CLI setup wizard (alternative to GUI)
python main.py preferences  # Configure your preferences
python main.py status       # System health check
python main.py --verbose    # Show detailed logs
python main.py --no-browser # Don't auto-open browser
```

### UI Navigation (After Server Starts)

After `python main.py` starts the server at http://localhost:8001:

- **Setup** → http://localhost:8001/setup (first-time setup only)
- **Home** → http://localhost:8001/ (chat interface)
- **Lists** → http://localhost:8001/lists (manage lists)
- **Todos** → http://localhost:8001/todos (manage todos)
- **Projects** → http://localhost:8001/projects (manage projects)
- **Files** → http://localhost:8001/files (upload/download files)
- **Standup** → http://localhost:8001/standup (generate daily standup)
- **Settings** → http://localhost:8001/settings (preferences, integrations)
- **User Menu** (top right) → Logout, profile settings

---

## What's Working in 0.8.9

✅ **Conversational AI (M2 Conscious Floor)**:
   - LLM-grounded floor for unmatched queries — Piper's voice, not templates
   - Context assembly: blocked items, active sprint, recent activity, calendar
   - Antecedent resolution ("it" and "that" resolve correctly across turns)
   - Honest refusal when context is missing (no fabrication)

✅ **Connector Infrastructure (RECONNECT WS-1)**:
   - DB-backed connector config — survives restarts
   - Honest no-repo UX when GitHub isn't connected
   - `StandupAssembler` pipeline replacing the hollow workflow

✅ **Security (field encryption)**:
   - AES-256-GCM field encryption with HKDF per-field key derivation
   - `user_api_keys` secret column encrypted at rest
   - Per-user LLM key routing (BYOC end-to-end complete)
   - Auth-exempt-list lint enforcement

✅ **Files (M3)**:
   - Search by name and filter by type
   - In-browser file preview
   - Bulk download as zip (checkbox select)
   - Drag & drop upload (multi-file)
   - Freeform tags with search

✅ **Design (D2)**:
   - Token system fully applied to the app shell
   - Responsive shell (adapts across viewport widths)
   - Mobile nav (hamburger → drawer)
   - Documents → Radar rename throughout

✅ **Integrations**:
   - Slack: inbound via Socket Mode, outbound, DMs, @-mentions
   - GitHub: issue summarization from live data, repo resolution, lifecycle
   - Notion: real append_blocks, URL unfurling
   - Calendar source aggregator

✅ **BYOC & Settings**:
   - API keys stored in macOS keychain via Settings UI
   - Per-user LLM key routing per-request
   - Radar as default home workspace

✅ **Setup & Onboarding**:
   - GUI setup wizard with visual interface
   - System health checks
   - API key validation (OpenAI, Anthropic, Gemini, Notion)
   - User account creation and portfolio onboarding

✅ **Core Infrastructure**:
   - Multi-user support, JWT auth, bcrypt passwords
   - PostgreSQL via Docker (port 5433), Redis, ChromaDB (Debian 12/bookworm)
   - Privacy filter and output filtering
   - 252/252 canonical regression baseline (D1 gate; regression suite unchanged)

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for current limitations.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) (comprehensive setup)
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT_v2.md](ALPHA_AGREEMENT_v2.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.6 means)

---

## Remember

This is **alpha software** (0.8.9). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Does connector config persist across restarts? Does Piper say "not connected" honestly when GitHub isn't configured? Does the standup pipeline return real data? Is the Radar label consistent throughout?

---

**Happy testing!** 🚀

_Last Updated: July 2, 2026_
