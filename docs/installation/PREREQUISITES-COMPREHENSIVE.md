# Piper Morgan: Comprehensive Prerequisites & System Requirements

This is the **single source of truth** for what's needed to build and run Piper Morgan from scratch.

---

## 🖥️ System Requirements

### Minimum

- **OS**: macOS 10.14+, Windows 10+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB (8GB recommended)
- **Disk**: 2GB free (for Docker images + virtual environment)
- **Network**: Stable internet (for downloading Python, Docker, dependencies)

### Supported Platforms

- macOS (Intel & Apple Silicon)
- Windows 10/11 (with WSL 2)
- Linux (Ubuntu, Debian)

---

## 🔧 Pre-Installation Software

### 1. Python 3.12 (REQUIRED)

**Why**: Piper Morgan requires Python 3.12.x specifically

- Python 3.13+ lack pre-built wheels for scipy, onnxruntime, pillow
- Python 3.11 works but 3.12 is recommended
- Python 3.9/3.10 are too old

**Status Check**:

```bash
python3.12 --version  # Should show: Python 3.12.x
```

**Install**: See `step-by-step-installation.md` Check 1

---

### 2. Git (REQUIRED)

**Why**: Clone the repository from GitHub

**Status Check**:

```bash
git --version  # Should show: git version 2.x.x
```

**Install**: See `step-by-step-installation.md` Check 2

---

### 3. Docker Desktop (REQUIRED)

**Why**: Runs PostgreSQL, Redis, ChromaDB, Temporal, and Traefik

> **⏱️ First time installing Docker?** Docker Desktop will guide you through account creation, terms acceptance, and initial setup (~5-10 minutes). You can use your Google account for quick signup.

**Status Check**:

```bash
docker --version   # Should show: Docker version 20.x+
```

**Mac**: Must be running (click Docker icon to launch, wait for whale icon to be solid, not grayed)
**Windows**: Must be running + WSL 2 enabled

**Install**: See `step-by-step-installation.md` Check 4

---

## 📦 Environment Variables (Optional for Local Dev)

These are automatically managed by the wizard, but listed for reference:

### API Keys

Enter your provider key at a hidden prompt. See the [self-host guide](./self-host-guide.md), step 5. Do not put a key in an `export` line or a shell profile.

### Optional: Integration Credentials

Notion and Slack are not offered in this beta, self-hosted installs included, so there is nothing to set up for them. GitHub and Google Calendar connect from Settings → Integrations in the browser after Piper is running.

---

## 🐳 Docker Services & Ports

When you run `docker-compose up -d postgres`, these services start:

| Service    | Port       | Purpose         | Required |
| ---------- | ---------- | --------------- | -------- |
| PostgreSQL | 5433       | Main database   | ✅ Yes   |
| Redis      | 6379       | Cache/queue     | ✅ Yes   |
| ChromaDB   | 8000       | Vector database | ✅ Yes   |
| Temporal   | 7233, 8088 | Workflow engine | ✅ Yes   |
| Traefik    | 80, 8090   | API gateway     | ✅ Yes   |

**Health Check**:

```bash
docker ps  # Shows all running containers
```

**Port Availability**: If any ports are in use, you'll see Docker startup errors. Free up ports or stop conflicting services.

---

## 📁 Directory Structure

After cloning, you'll have:

```
piper-morgan-product/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker service definitions
├── config/
│   ├── PIPER.user.md.example  # Preferences template (NOT API keys!)
│   └── PIPER.user.md          # (Created by you) User preferences
├── scripts/
│   ├── setup_wizard.py        # Interactive setup
│   ├── status_checker.py      # Health check
│   └── preferences_questionnaire.py  # Personality settings
├── services/                  # Core application code
├── web/                       # FastAPI web application
├── tests/                     # Test suite
└── venv/                      # (Created by wizard) Python environment
```

---

## 📋 Configuration Files

### 1. `PIPER.user.md` (User Preferences, NOT Secrets)

**Created by**: Wizard or manually (`cp config/PIPER.user.md.example config/PIPER.user.md`)
**Contains**: Working hours, timezone, project preferences, personality settings
**Does NOT contain**: API keys (those go in OS keychain)
**Location**: `config/PIPER.user.md`

### 2. `.env` (Optional, for advanced users)

**Contains**: Environment variable overrides
**Note**: Most users don't need this; wizard handles it

### 3. `docker-compose.yml` (Service Definitions)

**Contains**: PostgreSQL, Redis, ChromaDB, Temporal configuration
**Note**: Do not modify unless you know what you're doing

---

## 🔑 API Keys & Security

### Supported LLM Providers

| Provider      | Required? | Format       | How to Get                                 |
| ------------- | --------- | ------------ | ------------------------------------------ |
| OpenAI        | ✅ Yes    | `sk-...`     | https://platform.openai.com/api-keys       |
| Anthropic     | Optional  | `sk-ant-...` | https://console.anthropic.com/account/keys |
| Google Gemini | Optional  | API key      | https://aistudio.google.com/app/apikey     |
| Perplexity    | Optional  | API key      | https://www.perplexity.ai/settings/api     |

### Storage Location

- **Primary**: OS Keychain (secure, recommended)
  - macOS: Keychain Access
  - Windows: Credential Manager
  - Linux: Secret Service
- **Fallback**: Environment variables (for servers)
- **Never**: PIPER.user.md config file

---

## 💾 Database & Volumes

### PostgreSQL Database

- **Container**: `piper-postgres`
- **User**: `piper`
- **Database**: `piper_morgan`
- **Port**: 5433 (internal 5432)
- **Volume**: `piper_postgres_data_v1` (persistent)

### Data Directories

```
data/
├── redis/          # Redis persistence
└── chromadb/       # Vector database storage
```

---

## 🧪 Verification Commands

Run these to verify everything is set up:

```bash
# Check all prerequisites
python3.12 --version        # Should show: Python 3.12.x
git --version              # Should show: git version 2.x+
docker --version           # Should show: Docker version 20.x+
docker ps                  # Should show running containers

# Check Piper Morgan setup
cd piper-morgan-product
source venv/bin/activate   # Activate virtual environment
python -c "import structlog; print('✅ Dependencies installed')"
```

---

## 🚀 Quick Start

Once all prerequisites are met:

```bash
# 1. Start Docker database
docker-compose up -d postgres

# 2. Run wizard (handles everything else)
python3.12 main.py setup

# 3. Start Piper Morgan
python3.12 main.py
```

---

## 🆘 Common Issues & Fixes

| Issue                             | Cause                             | Fix                                                      |
| --------------------------------- | --------------------------------- | -------------------------------------------------------- |
| `Cannot connect to Docker daemon` | Docker Desktop not running        | Launch Docker Desktop, wait for whale icon               |
| `no such service: db`             | Wrong docker-compose service name | Use: `docker-compose up -d postgres`                     |
| `ModuleNotFoundError: structlog`  | Dependencies not installed        | Run: `pip install -r requirements.txt`                   |
| `Python 3.12 not found`           | Wrong Python version              | Install Python 3.12.10 from python.org                   |
| `Address already in use`          | Port 8001 occupied                | Kill other process: `lsof -i :8001`                      |
| `Database accessible error`       | PostgreSQL not running            | Run: `docker-compose up -d postgres` (separate terminal) |

---

## 📚 Next Steps

1. **Read**: `step-by-step-installation.md` (user-friendly walkthrough)
2. **Run**: `python3.12 main.py setup` (interactive wizard)
3. **Configure**: Answer wizard prompts for user creation & API keys
4. **Start**: `python3.12 main.py` to launch the application

---

**Last Updated**: October 29, 2025
**Version**: 1.0 - Comprehensive prerequisite guide
**Status**: Ready for alpha testing
