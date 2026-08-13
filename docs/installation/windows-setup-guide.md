# 🪟 Windows Development Setup Guide

**For**: Windows developers setting up Piper Morgan for local development
**Updated**: November 21, 2025
**Status**: Complete setup and troubleshooting guide

---

## Quick Start (WSL2 Recommended)

If you're on Windows 10/11 and unfamiliar with any of this, **use WSL2**:

```powershell
# 1. Run as Administrator
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# 2. From Ubuntu terminal inside WSL
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3.11-pip git

# 3. Clone and setup
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/  # Verify setup works
```

**That's it!** WSL2 gives you Linux for development while staying on Windows.

---

## Option 1: WSL2 (Recommended for Windows Developers)

### Why WSL2?

- ✅ Native Linux bash scripts (no translation layer)
- ✅ Faster file operations than Hyper-V VMs
- ✅ Python 3.11 works perfectly
- ✅ Git operations are native
- ✅ Can use Windows tools (VS Code, Git GUI) editing WSL files
- ✅ All pre-commit hooks work without modification

### Installation

#### Step 1: Enable WSL2

```powershell
# Run PowerShell as Administrator, then:
wsl --install
wsl --set-default-version 2

# Restart your computer when prompted
```

#### Step 2: Install Ubuntu

```powershell
wsl --install -d Ubuntu-22.04

# First launch will take a few minutes
# Creates Linux user account when done
```

#### Step 3: Update Ubuntu

```bash
# Inside Ubuntu terminal (you should see ubuntu prompt)
sudo apt update
sudo apt upgrade -y
```

#### Step 4: Install Python 3.11

```bash
sudo apt install python3.11 python3.11-venv python3.11-pip git
```

#### Step 5: Clone Repository

```bash
# In Ubuntu terminal
cd ~
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

#### Step 6: Set Up Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # You should see (venv) in prompt

# Verify Python 3.11
python --version  # Should show Python 3.11.x
```

#### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 8: Verify Setup

```bash
# Run basic tests
pytest tests/unit/ -v

# Should show passing tests ✅
```

### Accessing WSL Files from Windows

**From File Explorer:**
```
\\wsl$\Ubuntu-22.04\home\<your-username>\piper-morgan-product
```

**From VS Code:**
```powershell
# In terminal (PowerShell or CMD)
code \\wsl$\Ubuntu-22.04\home\<username>\piper-morgan-product

# Or install "Remote - WSL" extension and click "Open Folder in WSL"
```

**From Command Line (Windows PowerShell):**
```powershell
# Run WSL command from Windows PowerShell
wsl -d Ubuntu-22.04 pwd  # See current directory
wsl -d Ubuntu-22.04 python --version  # Run Python from WSL
```

### Daily Development Workflow (WSL2)

```powershell
# 1. Open Ubuntu terminal (Start Menu → Ubuntu)
# OR open Terminal and select Ubuntu profile

# 2. Navigate to project
cd ~/piper-morgan-product
source venv/bin/activate

# 3. Make changes (from Windows editor or WSL terminal)
# Everything works as documented in CONTRIBUTING.md

# 4. Commit changes
git add .
git commit -m "Your message"
git push origin your-branch
```

---

## Option 2: Native Windows Setup (Advanced)

If you prefer **not** to use WSL2:

### Prerequisites Check

- **Windows 10/11** (Build 19041 or later)
- **Administrator access** for installs
- **Disk space**: ~5GB for Python + dependencies

### Installation

#### Step 1: Install Python 3.11

**Option A: Windows Package Manager (Easiest)**
```powershell
# Run as Administrator
winget install Python.Python.3.11
```

**Option B: Direct Download**
1. Go to https://www.python.org/downloads/
2. Download "Windows installer (64-bit)"
3. Run installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"

#### Step 2: Verify Installation

```powershell
python --version  # Should show Python 3.11.x
```

If not found, restart PowerShell/CMD and try again.

#### Step 3: Install Git

Download from https://git-scm.com/download/win and run installer. Use all default options.

#### Step 4: Clone Repository

```powershell
# Choose location for your code
cd C:\Users\YourUsername\code

git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

#### Step 5: Create Virtual Environment

```powershell
# In the piper-morgan-product directory
python -m venv venv
.\venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try Activate.ps1 again
```

#### Step 6: Install Dependencies

```powershell
pip install -r requirements.txt

# Wait 3-5 minutes for installation to complete
```

#### Step 7: Verify Setup

```powershell
python --version  # Should show Python 3.11.x

# Run basic tests
pytest tests\unit\ -v
```

### Daily Development Workflow (Native Windows)

```powershell
# 1. Open PowerShell
# 2. Navigate to project
cd C:\Users\YourUsername\code\piper-morgan-product

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1  # PowerShell
# OR
venv\Scripts\activate.bat    # CMD (old Command Prompt)

# 4. Make changes
# (All commands work same as Linux, just use \ instead of /)

# 5. Commit changes
git add .
git commit -m "Your message"
git push origin your-branch
```

---

## Common Windows Issues and Fixes

### Issue: "python command not found"

**Why**: Python not in Windows PATH

**Fix**:
1. Uninstall Python (Settings → Apps)
2. Reinstall from https://www.python.org/downloads/
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart PowerShell
5. Verify: `python --version`

### Issue: Virtual environment activation fails

**Error**:
```
.ps1 cannot be loaded because running scripts is disabled
```

**Fix**:
```powershell
# Run once as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate normally
.\venv\Scripts\Activate.ps1
```

### Issue: "No module named 'structlog'" or other import errors

**Why**: Dependencies not installed

**Fix**:
```powershell
# Make sure venv is activated (you see (venv) in prompt)
pip install -r requirements.txt

# Wait for completion, then retry
```

### Issue: Git clone fails with "filename too long"

**Why**: Windows has 260-character path limit

**Fix**:
```powershell
# Enable long paths (run as Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Then clone again.

### Issue: Pre-commit hook blocks commit with filename error

**Error**:
```
❌ Pre-commit hook: Windows-illegal characters found in filenames
Windows filenames cannot contain: : < > " | ? *
```

**Why**: You're committing a file with illegal Windows characters (colons, quotes, etc.)

**Fix**:
- Rename the file to use dashes or underscores instead
- Example: "file (10:30 AM).txt" → "file-1030-AM.txt"
- Then retry the commit

**To bypass** (not recommended):
```powershell
git commit --no-verify
```

### Issue: Tests fail with "No such file or directory"

**Why**: Path separator issues (should use `\` on Windows in commands)

**Fix**:
```powershell
# Wrong (forward slash)
pytest tests/unit/test_file.py

# Right (backslash)
pytest tests\unit\test_file.py

# Or use forward slashes with quotes
pytest "tests/unit/test_file.py"
```

### Issue: Terminal doesn't recognize bash commands

**Why**: You're in CMD or old PowerShell without Git Bash

**Fix**:
- Use PowerShell 7+ (modern Windows)
- OR install Git Bash and use that terminal
- OR use WSL2 (recommended)

### Issue: Cannot edit .env file from Windows editor

**Why**: File might be locked or have wrong permissions

**Fix**:
```powershell
# Check if it exists
Test-Path .env

# If it exists and you can't edit, remove and recreate
Remove-Item .env
New-Item .env

# Add your config to .env file
```

---

## Troubleshooting: Repository Cloning Issues

### Issue: Clone hangs or fails on Windows

**Why**: Long filenames or illegal characters in repository

**Fix Option 1: Shallow Clone**
```powershell
git clone --depth 1 https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
git fetch --unshallow  # Get full history after
```

**Fix Option 2: No Checkout First**
```powershell
git clone --no-checkout https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
git checkout main
```

**Fix Option 3: Use WSL2** (Recommended)
```powershell
# Just use WSL2 - it handles this automatically
wsl --install
# Then follow WSL2 setup above
```

---

## Verification Checklist

Before considering your setup complete:

- [ ] Python 3.11 installed: `python --version` shows 3.11.x
- [ ] Virtual environment activated: Prompt shows `(venv)`
- [ ] Dependencies installed: `pip list | grep -i structlog` shows a result
- [ ] Basic test passes: `pytest tests/unit/ -v` shows ✅ passing
- [ ] Git working: `git status` shows clean repository
- [ ] Pre-commit hooks installed: `pre-commit run --all-files` completes

---

## When to Use What

| Situation | Recommendation |
|-----------|-----------------|
| New to Windows development | WSL2 |
| Need to use Windows GUI tools | WSL2 + VS Code Remote |
| Prefer pure Windows solution | Native Windows + PowerShell 7 |
| Have performance concerns | WSL2 (actually faster) |
| Just getting started | **WSL2** (seriously, it's best) |

---

## Getting Help

If you're stuck:

1. **Check this guide** for your specific error
2. **Check CONTRIBUTING.md** Windows Development section
3. **Check GitHub Issues** - many Windows issues have solutions
4. **If you don't find an existing issue, [file a new one](https://github.com/mediajunkie/piper-morgan-product/issues/new)** - include error message and steps taken

---

## Related Documentation

- [CONTRIBUTING.md - Windows Development Section](../CONTRIBUTING.md#windows-development)
- [Installation Troubleshooting](./troubleshooting.md)
- [Development Setup Guide](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/development/tools/setup.md)
- [Getting Started](./step-by-step-installation.md)

---

**Last Updated**: November 21, 2025
**Tested On**: Windows 10/11, Python 3.11, WSL2 (Ubuntu 22.04), Git 2.42+
