# Piper Morgan Alpha Testing Guide

**Version**: 0.8.9.1
**Last Updated**: July 2, 2026
**For**: Alpha Testers

---

## Returning Tester? Start Here

If you already have Piper set up and running, skip straight to what matters:
- **[What's New in 0.8.9](#whats-new-in-089)** - Connector infra, field encryption, mobile nav, Radar rename
- **[What to Test in 0.8.9](#what-to-test-in-089)** - Priority testing areas for this release
- **[Troubleshooting](#chapter-3-troubleshooting)** - If something isn't working

---

## Quick Navigation

This guide has three main sections:

| Section | Description | Start Here If... |
|---------|-------------|------------------|
| **[Chapter 1: Setup](#chapter-1-setup)** | Prerequisites, installation, configuration | You're setting up for the first time |
| **[Chapter 2: Testing](#chapter-2-testing)** | Test scenarios, features to explore | You already have an account and want to start testing |
| **[Chapter 3: Troubleshooting](#chapter-3-troubleshooting)** | Common issues and solutions | Something isn't working |

**First-time setup?** Start with [Chapter 1](#chapter-1-setup). **Already have an account?** Jump to [Chapter 2: Testing](#chapter-2-testing).

---

# Chapter 1: Setup

## Before You Begin - Prerequisites Checklist

**Required Software:**

- [ ] Git installed and configured
- [ ] Python 3.11 or higher
- [ ] Docker installed and running
- [ ] A code editor (VS Code recommended)
- [ ] Terminal/command line access

**Required Accounts & Keys:**

- [ ] **GitHub account with SSH key configured** (required BEFORE cloning)

  - **Why needed**: You must authenticate to GitHub to clone the repository
  - **If you already have SSH keys**: Test with `ssh -T git@github.com`
    - ✅ Success: "Hi username! You've successfully authenticated..."
    - ❌ Failure: See setup guide below
  - **If you need to set up SSH keys**: Follow GitHub's official guides:
    - 📖 [Generating SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
    - 📖 [Adding SSH Key to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
  - **Note**: This MUST be done before Step 1 (cloning repository)

- [ ] At least one LLM API key:
  - OpenAI API key (GPT-4 access preferred), OR
  - Anthropic API key (Claude access)
- [ ] Budget $5-20 for LLM API testing costs

**Optional but Recommended:**

- [ ] Notion API key (for document management features)
- [ ] Slack workspace (for notification features)
- [ ] GitHub personal access token (for issue creation features)

**Time Commitment:**

- [ ] 45-60 minutes for guided setup and initial exploration (includes Docker installation if needed)
- [ ] 15-30 minutes weekly for feedback during alpha period

---

## Important Disclaimers - Please Read

**⚠️ ALPHA SOFTWARE WARNING ⚠️**

This is pre-release alpha software (version 0.8.9). By proceeding, you acknowledge:

1. **Expected Issues**: Bugs, crashes, and incomplete features are normal
2. **Data Loss Risk**: Your data may be lost at any time without warning
3. **No Production Use**: Do NOT use for mission-critical or time-sensitive work
4. **Employer Systems**: Do NOT install on employer hardware without written permission
5. **API Charges**: You are responsible for all LLM API costs incurred
6. **Security**: Not security audited - use test data only, no sensitive information
7. **No Warranty**: Software provided "as-is" without any warranty whatsoever
8. **No Support SLA**: Best-effort support only, no guaranteed response times

See `ALPHA_AGREEMENT_v2.md` for complete legal terms.

---

## What's New in 0.8.9

v0.8.9 closes three fronts: connector infrastructure (RECONNECT WS-1), field-level security, and Design D2 (token system + mobile nav + Radar rename).

- **Connector config (RECONNECT WS-1)**: Connector configuration now lives in the database, not an ephemeral JSON file. Repo config and integration state survive restarts. When GitHub isn't configured, Piper says so honestly.
- **Real standup pipeline**: The hollow `MorningStandupWorkflow` is retired; `StandupAssembler` is the live pipeline. Ask Piper for your standup in chat.
- **Field encryption**: User secrets (API keys) are now encrypted at rest using AES-256-GCM with HKDF per-field key derivation.
- **Per-user LLM key routing**: Your BYOC key is now routed per-request. The BYOC credential flow (from D1) is end-to-end complete.
- **Auth hardening**: `admin_compose` route removed; auth-exempt-list lint-enforced.
- **Design D2 — token system + mobile nav**: Design token system applied to the app shell; responsive shell; mobile nav (hamburger → drawer); Documents → Radar rename throughout.
- **Dockerfile → bookworm**: Debian 12 base image for chromadb SQLite ≥3.35 support.

**Database Migration Required**: Run `alembic upgrade head` (includes secret-column encryption migration).

See [Release Notes v0.8.9](releases/RELEASE-NOTES-v0.8.9.md) for full details.

<details>
<summary><strong>Previous release (0.8.8 — D1/RECONNECT)</strong></summary>

Conscious Floor, BYOC credential layer, Radar as default workspace, navigation IA (History→Radar, Collections→Lists), full-height home chat, compose autosave, source-provenance badges on files. 252/252 canonical regression clean.

</details>

<details>
<summary><strong>Previous release (0.8.5.3)</strong></summary>

**Windows Compatibility & Setup UX** - 14 issues from Ted Nadeau's Windows testing: uvloop fix, missing migrations, CRLF handling, installation validator, actionable errors.

</details>

<details>
<summary><strong>Previous release (0.8.5)</strong></summary>

**MUX-IMPLEMENT Complete** - The Modeled User Experience super epic:
- WCAG 2.1 AA Accessibility (11 colors fixed, all ratios ≥4.5:1)
- Lifecycle State Persistence with visual indicators
- New Views: Work Items and Project Detail
- ProcessRegistry for guided processes (ADR-049)

</details>

<details>
<summary><strong>Previous release history (0.8.3 - 0.8.4.3)</strong></summary>

**0.8.4.3**: Fresh install fixes, migration validation at startup, GUI wizard routing.

**0.8.4.2**: Calendar bug fixes (TEMPORAL handler), markdown rendering, sidebar ordering.

**0.8.4.1**: Chat auto-load on refresh, `/standup` routing fix, RequestContext model (ADR-051).

**0.8.4**: Integration Settings (OAuth for Slack/Calendar, PAT for GitHub, API key for Notion), Portfolio Onboarding, logout fix.

**0.8.3.2**: Interactive Standup Assistant (conversational standup creation, preference learning, iterative refinement).

**0.8.3**: Integration Health Dashboard, OAuth Connection Management, Notion in Setup Wizard.

</details>

---

## Windows Alpha Tester Setup

**Best Option: Use the Automated Setup Script**

We've created a Windows batch file that automates the entire setup process:

```cmd
REM Fast clone (~91MB instead of ~800MB) - recommended for alpha testers
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
```

The script will:
- Check for Python 3.11/3.12 and Docker
- Create a virtual environment
- Install all dependencies
- Generate a secure JWT key
- Start Docker containers
- Launch the setup wizard at http://localhost:8001/setup

### Alternative: WSL2 (Windows Subsystem for Linux)

If you prefer a Linux-like environment on Windows, WSL2 provides a smooth setup experience:

```powershell
# 1. Run as Administrator
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# 2. Inside Ubuntu terminal
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv git

# 3. Clone and setup (uses bash script - faster)
# --depth 1 gives you a fast ~91MB download (vs ~800MB full history)
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
./scripts/alpha-setup.sh
```

### Manual Setup (If You Prefer Full Control)

If you prefer not to use automated scripts, follow the guided setup below. On Windows, use:
- PowerShell or Command Prompt
- `venv\Scripts\Activate.ps1` to activate (Windows-style path)
- See [Windows Setup Guide](installation/windows-setup-guide.md) for troubleshooting

### Known Windows Issues for Alpha Testers

1. **Clone failures**: Ensure you have long path support enabled:
   ```powershell
   # Run as Administrator
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
     -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

2. **Python not found**:
   - Reinstall from https://www.python.org/downloads
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart Command Prompt/PowerShell after installing

3. **Path errors in commands**: Use backslashes (Windows-native) or quotes with forward slashes:
   ```powershell
   python main.py setup              # Works on all platforms
   python -c "import sys; print(sys.version)"  # Also works
   ```

4. **Docker Desktop not running**: The setup script will fail if Docker Desktop isn't running
   - Start Docker Desktop before running the setup script
   - Wait for it to fully initialize (check system tray)

---

## Guided Setup Instructions

### Step 1: Clone the Repository

```bash
# --depth 1 gives you a fast ~91MB download (vs ~800MB full history)
# You get all the code, just not the git history (which you don't need for testing)
git clone --depth 1 -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

**Note**: On Windows, use the WSL2 terminal or PowerShell with proper path handling

### Step 2: Create Virtual Environment

```bash
python3.12 -m venv venv
# Requires Python 3.11 or 3.12 - verify with: python --version
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start Server for First-Time Setup

Setup uses a visual web interface by default.

```bash
python main.py
# → Opens http://localhost:8001/setup (GUI setup wizard)
```

The GUI setup wizard will automatically open in your browser and guide you through:

- ✅ System health checks (Docker, Python, Port, Database)
- ✅ API key configuration (OpenAI, Anthropic, Gemini)
- ✅ User account creation (username, email, password)
- ✅ Setup verification and confirmation

**See the Setup Wizard Walkthrough section below** for detailed screenshots and step-by-step guidance.

#### Alternative: Command-Line Setup

If you prefer the original command-line interface:

```bash
python main.py setup
```

This will run the CLI setup wizard with prompts in your terminal. Both methods configure the same settings - use whichever you're comfortable with.

### Step 5: Configure Your Preferences

After setup, personalize your experience:

```bash
python main.py preferences
```

This 2-minute questionnaire configures:

- **Communication Style**: concise, balanced, detailed
- **Work Style**: structured, flexible, exploratory
- **Decision Making**: data-driven, intuitive, collaborative
- **Learning Style**: examples, explanations, exploration
- **Feedback Level**: minimal, moderate, detailed

### Step 6: Verify Installation

```bash
python main.py status
```

You should see:

```
==================================================
Piper Morgan System Status
==================================================

Database:
  ✓ PostgreSQL connected
     Users: 1, Size: 15.2 MB

API Keys:
User: [your-username]
  ✓ openai: Valid
  ✓ anthropic: Valid (or ○ Not configured)

Performance:
  ✓ Database response: 12ms

Recommendations:
  ✓ All systems operational!
```

### Step 7: First Run

```bash
python main.py
```

The server will start and automatically open http://localhost:8001 in your browser.

**Login with your credentials:**

- Username: [from setup wizard]
- Password: [from setup wizard]

After login, you'll see the Piper Morgan chat interface.

---

## Setup Wizard Walkthrough
The GUI setup wizard provides a visual, step-by-step interface for configuration. Here's what to expect at each stage:

### Step 1: Welcome Screen

![Setup Wizard - Welcome](assets/images/alpha-onboarding/setup-wizard-welcome.png)

The welcome screen introduces the setup process and explains what will be configured. Click "Get Started" to begin.

### Step 2: System Health Check

![Setup Wizard - Health Check](assets/images/alpha-onboarding/setup-wizard-health-check.png)

Automatic validation of your system:
- ✓ Docker installed and running
- ✓ Python version correct (3.11 or 3.12)
- ✓ Port 8001 available
- ✓ Database accessible

If any checks fail, the wizard provides specific guidance on how to fix them.

### Step 3: API Key Configuration

![Setup Wizard - API Keys](assets/images/alpha-onboarding/setup-wizard-api-keys.png)

Configure your LLM API keys through a web form interface. This is **much easier** than the command-line method - you can see what you're typing, correct mistakes easily, and get immediate validation feedback.

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google Gemini

You can configure one, two, or all three providers. At least one is required.

### Step 4: User Account Creation

![Setup Wizard - User Creation](assets/images/alpha-onboarding/setup-wizard-user-creation.png)

Create your admin account:
- Username (alphanumeric, unique)
- Email address (valid format required)
- Secure password (min 8 chars, bcrypt-hashed)
- Password confirmation with validation

The form provides real-time feedback on password strength and format requirements.

### Step 5: Setup Complete

![Setup Wizard - Success](assets/images/alpha-onboarding/setup-wizard-success.png)

Setup confirmation screen with:
- Summary of what was configured
- Next steps and quick links
- "Start Using Piper" button to proceed to login

Click the button to go to the login page and start using Piper Morgan.

---

# Chapter 2: Testing

This chapter covers what to test and how. If you're already set up, **start here**.

## What to Test in 0.8.9

Connector persistence, standup quality, and the security migration are the focus. **Does config survive restarts? Does Piper say "not connected" when it should? Does the standup pipeline return real data?**

### Priority Testing Areas

1. **Connector config persistence** - Configure a GitHub repo, restart the server — does it remember the config?
2. **Honest no-repo UX** - Remove or skip GitHub config — does Piper tell you it's not connected rather than guessing or failing silently?
3. **Standup via chat** - Ask "what's my standup?" in the chat — does `StandupAssembler` return a real, assembled response (not a generic template)?
4. **BYOC key routing** - Enter your API key in Settings, make a few requests — confirm your key is being used (check your provider's usage dashboard)
5. **Mobile nav** - Open Piper on a phone or narrow browser window — does the hamburger → drawer nav work correctly?
6. **Radar rename** - Is "Radar" (not "Documents") the label throughout the nav, page headers, and breadcrumbs?
7. **Existing features still working** - Conscious Floor, files experience, Slack inbound, BYOC key persistence

### Basic Functionality Tests

Start with these simple tests to verify everything works:

1. **Basic Chat**: "Hello, what can you help me with?"
2. **Task Creation**: "Add a todo: Review Q3 metrics"
3. **Information Query**: "What tasks do I have?"
4. **File Upload**: Upload a PDF or DOCX file (max 10MB) and ask for analysis
5. **Document Summary**: "Summarize the document I just uploaded"
6. **Preference Check**: "How do you prefer to communicate?" (should reflect your settings)
7. **Multi-User Test**: If testing with others, verify you can't see their data

---

## Exploring Piper's Features

### Lists, Todos, and Projects Management

**Basic CRUD Operations** (test these first):

1. **Create a List**
   - Navigate to http://localhost:8001/lists
   - Click "Create New List" button
   - Enter name: "Alpha Testing Tasks"
   - Enter description: "Testing the Lists feature"
   - Verify list appears in the list view

2. **Edit and Delete**
   - Open the list you created
   - Edit the name or description
   - Try deleting a list (should show confirmation)

3. **Repeat for Todos and Projects**
   - Navigate to /todos and /projects
   - Same CRUD operations available
   - Test that all three resource types work consistently

### File Management

**Basic File Operations** (test these first):

1. **Upload a File**
   - Navigate to http://localhost:8001/files
   - Click "Upload File" or drag-and-drop a file
   - Supported formats: PDF, DOCX, TXT, MD, JSON (max 10MB)
   - Verify file appears in file list with correct metadata

2. **Download a File**
   - Click "Download" button on uploaded file
   - Verify file downloads correctly

3. **Delete a File**
   - Click "Delete" button on a file
   - Verify file is removed from list

4. **Test File Privacy**
   - Files are owner-based (private to you)
   - Other users should NOT see your files

### Interactive Standup Assistant (New in 0.8.3.2)

1. **Start a Standup Conversation**
   - In the chat, say "let's write a standup" or "/standup"
   - Piper should respond with initial guidance
   - Verify conversation flow starts properly

2. **Test Preference Gathering**
   - Tell Piper your preferences: "I prefer bullet points" or "keep it concise"
   - Verify Piper acknowledges and remembers your preference
   - Generate content should reflect your stated style

3. **Test Iterative Refinement**
   - Ask Piper to make changes: "add more detail about the bug fix" or "make it shorter"
   - Verify Piper updates the standup accordingly
   - Previous versions should be saved for comparison

4. **Complete the Standup**
   - Say "looks good, let's use this" or "finalize"
   - Verify standup is marked complete
   - Check that performance is fast (sub-500ms responses)

5. **Edge Cases to Test**
   - Abandon a standup mid-conversation (say "nevermind" or navigate away)
   - Start multiple standups in one session
   - Long conversations (10+ turns) - verify memory isn't growing unbounded

### Quick Standup Generation (Legacy)

1. **Generate a Standup**
   - Navigate to http://localhost:8001/standup
   - Click "Generate Standup" button
   - Wait 2-3 seconds for AI generation
   - Verify standup report appears with meaningful content
   - Note: First standup may be generic if no prior activity

2. **Test with Activity**
   - Create some lists, todos, upload files
   - Generate standup again
   - Verify it reflects your recent activity

### Authentication & Logout

1. **Test Logout**
   - Click user menu (top right corner of page)
   - Click "Logout" button
   - Verify you're redirected to login page
   - Verify session is cleared (can't access /lists without login)

2. **Test Login After Logout**
   - Enter your credentials on login page
   - Verify you can log back in
   - Verify your data is still there (lists, files, etc.)

### Navigation & Polish

1. **Test Breadcrumbs**
   - Navigate to /lists, /todos, /projects, /files, /standup
   - Verify each page shows breadcrumb: Home › [Page Name]
   - Click "Home" in breadcrumb, verify navigation works

2. **Test Page Consistency**
   - Check that Settings pages are on unified grid
   - Verify no "My Lists" prefix (should just be "Lists")
   - Check that Integrations page shows placeholder (not 404)
   - Check Privacy & Data settings has informative content

---

## Advanced Testing (Multi-User Sharing)

> **Note**: These features require multiple user accounts and are considered advanced. Focus on basic CRUD operations first.

### Sharing Lists, Todos, and Projects

1. **Share a List**
   - Open a list you created
   - Click "Share" button
   - Enter another user's email (if multi-user testing)
   - Select role: Editor
   - Verify sharing modal shows success

2. **Test Permission Badges**
   - Notice "Owner" badge on your list
   - If shared with another user, verify their role badge shows

### Permission System

1. **Conversational Permission Commands**
   Try these in the chat interface:
   - "share my Alpha Testing Tasks list with [email] as editor"
   - "who can access my Alpha Testing Tasks?"
   - "show me shared lists"
   - "give [email] viewer access to my project plan"

2. **Role-Based Access Testing** (requires 2 users)
   - Create a list as User A
   - Share with User B as "Viewer"
   - Log in as User B
   - Verify: Can view list but NOT edit/delete
   - Share same list with User C as "Editor"
   - Log in as User C
   - Verify: CAN edit and update list

---

# Chapter 3: Troubleshooting

## Troubleshooting

### Setup Wizard Issues

**GUI setup wizard not loading?**

- Make sure you ran `python main.py` (not `python main.py setup`)
- Check that http://localhost:8001/setup opens in your browser
- If browser didn't auto-open, manually navigate to http://localhost:8001/setup
- Alternative: Use CLI setup with `python main.py setup`

**"Docker not installed" or "Docker not running"**

The setup wizard (GUI or CLI) will guide you through Docker installation with platform-specific instructions. If you encounter issues:

- Make sure Docker Desktop is running (look for whale icon in system tray/menu bar)
- Restart Docker Desktop if it seems stuck
- On macOS: Check Applications folder for Docker Desktop
- On Windows: Check if Docker Desktop service is running
- Test manually with: `docker --version`

**"Python 3.11+ not found"**

- Install Python 3.11 or 3.12: https://www.python.org/downloads/
- Test with: `python --version`

**"Port 8001 not available"**

- Another service is using port 8001
- Find what's using it: `lsof -i :8001`
- Stop other Piper Morgan instances or change port

**"Database not accessible"**

- Ensure database is running: `docker compose up -d db`
- Wait 10 seconds for database to start
- Check Docker containers: `docker ps`

### Runtime Issues

**"No LLM provider configured"**

- Re-run GUI setup wizard: Navigate to http://localhost:8001/setup
- Or use CLI setup: `python main.py setup`
- Verify API keys are valid in your provider dashboard (OpenAI, Anthropic, Google)
- Check status: `python main.py status`

**High API costs**

- Piper uses GPT-4/Claude by default for best results
- Monitor usage in your provider's dashboard
- Configure preferences for more concise responses

**Preference changes not taking effect**

- Re-run: `python main.py preferences`
- Restart Piper Morgan after preference changes
- Check status shows your username correctly

**Login issues**

- Forgot password? Run `python main.py setup` to create a new account
- Can't access http://localhost:8001? Try http://127.0.0.1:8001
- Check server is running: Look for "Server ready" message
- Browser didn't open? Manually navigate to http://localhost:8001

**File upload issues**

- Supported formats: PDF, DOCX, TXT, MD, JSON
- Max file size: 10MB
- Check file isn't corrupted or password-protected
- Verify you're logged in (file upload requires authentication)

### Feature-Specific Troubleshooting

**Can't create lists/todos/projects?**
- Make sure you're on the `production` branch: `git status`
- Update to latest: `git pull origin production`
- Refresh browser page
- Check browser console for errors (F12)
- Verify you're logged in (authentication required for CRUD operations)

**Files page not loading or shows errors?**
- Update to latest: `git pull origin production`
- Restart server: `python main.py`
- Clear browser cache if needed
- Check file size limit: 10MB maximum
- Verify supported formats: PDF, DOCX, TXT, MD, JSON

**Interactive Standup issues?**
- Conversation should respond in <500ms (P95 target)
- If conversation seems stuck, try "start over" or navigate away
- Each turn should build on previous context
- Preferences should be remembered within the conversation

**Quick Standup generation hangs or fails?**
- Should complete in 2-3 seconds
- If hanging, check API key configuration: `python main.py status`
- Verify you have activity data (lists, todos, files created)
- Try refreshing the page and generating again

**Logout not working?**
- Logout is in the user menu (top right corner)
- Click user menu → "Logout"
- Verify redirect to login page after logout
- If session persists, clear browser cookies

**Permission sharing not working?**
- Requires multi-user setup (2+ user accounts)
- Make sure other user exists in database
- Try conversational command: "share my [resource] with [email] as editor"
- Verify resource ownership (you must own the resource to share it)
- Check that SEC-RBAC is active: `python main.py status`

---

## Providing Feedback

We need your feedback to improve! Please report:

### What to Report

- Bugs and crashes (with error messages)
- Setup wizard issues or confusing steps
- Preference system problems
- Missing features you expected
- Performance issues
- Successful workflows that delighted you

### How to Report

1. **GitHub Issues**: Preferred for bugs (if comfortable with GitHub)
2. **Email**: christian@[domain] for private feedback
3. **Weekly Check-in**: Optional 15-minute calls available

### Helpful Feedback Format

```
SETUP METHOD: [wizard/manual]
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
SYSTEM STATUS: [output of `python main.py status`]
SEVERITY: [blocker/major/minor]
```

---

## Privacy & Data Collection

- We collect anonymous usage analytics to improve the product
- Error logs may be transmitted (no personal data included)
- Your LLM API keys are stored securely in system keychain, never transmitted
- Preference data is stored locally in your database
- You can opt out of analytics in settings
- Setup wizard completion statistics help us improve onboarding
- SEC-RBAC Phase 1 ensures owner-based access control
- Shared resources require explicit permission grants
- Your files, lists, todos, and projects are private by default
- **Note**: Data is not yet fully encrypted at rest (see `ALPHA_KNOWN_ISSUES.md` for details)

---

## Advanced: Manual Setup (If Wizard Fails)

If the setup wizard fails, you can fall back to manual configuration:

1. **Environment Variables**: Copy `.env.example` to `.env` and edit
2. **Database**: Run `docker compose up -d db`
3. **API Keys**: Manually add to `.env` file
4. **Database Migration**: Run database setup scripts

See original testing guide for detailed manual steps.

---

## Advanced: Browsing the Database Directly

For debugging and development, you can browse the PostgreSQL database directly:

### Connection Details

| Setting | Value |
|---------|-------|
| Host | `localhost` (or `127.0.0.1` on Windows) |
| Port | `5433` (note: not default 5432) |
| Database | `piper_morgan` |
| Username | `piper` (from docker-compose.yml) |
| Password | `dev_changeme_in_production` (from docker-compose.yml) |

### GUI Tools (Optional)

**pgAdmin** (recommended for beginners):
1. Download from https://www.pgadmin.org/
2. Add Server → Enter connection details above
3. Browse tables under Databases → piper_morgan → Schemas → public → Tables

**DBeaver** (full-featured alternative):
1. Download from https://dbeaver.io/
2. New Connection → PostgreSQL → Enter connection details
3. Browse schema visually

### Command Line Access

```bash
# Connect via Docker container
docker exec -it piper-postgres psql -U piper -d piper_morgan

# List tables
\dt

# Query example
SELECT * FROM users;

# Exit
\q
```

---

## Questions?

Remember: This is alpha software (version 0.8.9). The GUI setup wizard handles most complexity, but you're still testing early-stage software. Expect bugs and incomplete features.

If guided setup seems overwhelming, a hosted version is planned for later in 2026.

Thank you for being an early adopter and helping us improve! 🚀

---

## See Also

- `VERSION_NUMBERING.md` - Understanding Piper Morgan's version scheme
- `ALPHA_AGREEMENT_v2.md` - Legal terms and conditions
- `ALPHA_KNOWN_ISSUES.md` - Current bugs and limitations
- `ALPHA_QUICKSTART.md` - Quick 2-5 minute setup guide

---

_Last updated: June 22, 2026_
_Software version: 0.8.9_
