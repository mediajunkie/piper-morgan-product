# 🔧 Piper Morgan Installation Troubleshooting Guide

**For**: When something goes wrong during installation
**Updated**: October 27, 2025
**Status**: Common issues with solutions

---

## Issue #1: "No module named 'structlog'"

### Error Message You See

```
Failed to initialize LLM service: No module named 'structlog'
ModuleNotFoundError: No module named 'structlog'
```

### What This Means

Python is looking for a package called `structlog`, but it's not installed.

### Most Common Cause

❌ **You skipped Step 8**: Did not run `pip install -r requirements.txt`

### How to Fix It

**Step 1**: Make sure you're in the virtual environment (you should see `(venv)` in your prompt)

**Step 2**: Run this command to install all dependencies:

```bash
pip install -r requirements.txt
```

**Step 3**: Wait 3-5 minutes for it to finish

**Step 4**: Verify it worked:

```bash
pip list | grep structlog
```

You should see `structlog 23.2.0` or similar.

**Step 5**: Try starting Piper Morgan again:

```bash
python main.py
```

✅ Should work now!

---

## Issue #2: "command not found: python3"

### Error Message You See

```
command not found: python3
```

### What This Means

Your computer doesn't recognize the `python3` command.

### Possible Causes

1. Python is not installed
2. Python is installed but not in the system path
3. You're using the wrong command name

### How to Fix It

**First, check if Python is installed at all**:

**Mac/Linux**:

```bash
which python
```

or

```bash
which python3
```

**Windows**:

```bash
where python
```

**If it says "not found"**: Python is not installed. Go to [python.org/downloads](https://www.python.org/downloads) and install Python 3.12.

**If you see a path like `/usr/bin/python3`**: Python IS installed. Try these alternatives:

Option 1 - Try `python` instead of `python3`:

```bash
python --version
```

Option 2 - If that doesn't work, reinstall Python:

1. Go to [python.org/downloads](https://www.python.org/downloads)
2. Download Python 3.12
3. Run the installer
4. **IMPORTANT**: Check the box "Add Python to PATH"
5. Click "Install Now"
6. Close your terminal completely
7. Open a NEW terminal and try again

---

## Issue #3: "command not found: git"

### Error Message You See

```
command not found: git
```

### What This Means

Git is not installed on your computer.

### How to Fix It

**Mac**:

1. Open Terminal
2. Type: `xcode-select --install`
3. Click "Install" when prompted
4. Wait ~10 minutes
5. Close Terminal
6. Open NEW Terminal and try again

**Windows**:

1. Go to [git-scm.com](https://git-scm.com)
2. Click "Download for Windows"
3. Run the installer
4. Click "Next" through all screens
5. At the end, make sure "Launch Git Bash" is checked
6. Click "Finish"
7. Close your Command Prompt
8. Open NEW Command Prompt and try again

---

## Issue #4: Virtual Environment Not Activating

### What Happens

You run the activation command but don't see `(venv)` in your prompt.

### How to Fix It

**Check 1: Are you in the right folder?**

You should be in the `piper-morgan` folder. Type:

```bash
pwd
```

You should see something ending in `piper-morgan`.

If not, navigate there:

```bash
cd ~/piper-morgan-workspace/piper-morgan
```

**Check 2: Try the activation command again**

**Mac/Linux**:

```bash
source venv/bin/activate
```

**Windows**:

```bash
venv\Scripts\activate
```

**Check 3: If still not working, recreate the virtual environment**

```bash
rm -rf venv          # Remove the old one
python3 -m venv venv # Create a new one
source venv/bin/activate  # Activate (Mac/Linux)
# or
venv\Scripts\activate     # Activate (Windows)
```

---

## Issue #5: "Invalid API key"

### Error Message You See

```
Invalid API key
Authentication failed
```

### What This Means

Your Anthropic API key is wrong or missing.

### How to Fix It

**Step 1**: Get a new API key from Anthropic

1. Go to [platform.claude.com](https://platform.claude.com/dashboard)
2. Sign in (use Google account)
3. Click your profile (top-right)
4. Click "API Keys"
5. Click "Create Key"
6. Copy the new key

**Step 2**: Add it to your config file

**Mac**:

```bash
open config/PIPER.user.md
```

**Windows**:

```bash
notepad config/PIPER.user.md
```

**Step 3**: Find this line:

```
anthropic_api_key: "your-key-here"
```

**Step 4**: Replace it with:

```
anthropic_api_key: "sk-ant-xxx..."
```

(Use your actual key, keep the quotes)

**Step 5**: Save the file and close

**Step 6**: Start Piper Morgan again:

```bash
python main.py
```

---

## Issue #6: "Address already in use"

### Error Message You See

```
Address already in use: ('127.0.0.1', 8001)
```

### What This Means

Piper Morgan is already running in another terminal window.

### How to Fix It

**Option 1**: Close the other terminal

1. Look for another Terminal/Command Prompt window that has Piper Morgan running
2. Close that window
3. Try starting Piper Morgan again

**Option 2**: If you can't find the other window, wait 30 seconds and try again

**Option 3**: Restart your computer (nuclear option but always works)

---

## Issue #7: "Permission denied"

### Error Message You See

```
Permission denied
chmod: cannot access
```

### What This Means

Your computer won't let you run or modify a file.

### How to Fix It (Mac/Linux)

This usually happens on the venv activation. Try this:

```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## Issue #8: "pip: command not found"

### Error Message You See

```
command not found: pip
```

### What This Means

pip is not installed or not in your PATH.

### How to Fix It

**Check 1**: Are you in the virtual environment?

You should see `(venv)` in your prompt. If not:

**Mac/Linux**:

```bash
source venv/bin/activate
```

**Windows**:

```bash
venv\Scripts\activate
```

**Check 2**: If you still see "pip: command not found"

Try using Python to run pip:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Issue #9: "ImportError" or "ModuleNotFoundError" (Other Packages)

### Error Message You See

```
ModuleNotFoundError: No module named 'fastapi'
ImportError: No module named 'sqlalchemy'
```

### What This Means

Some Python package is missing.

### How to Fix It

99% of the time, this means you didn't run Step 8. Run it now:

```bash
pip install -r requirements.txt
```

Wait for it to complete, then try again:

```bash
python main.py
```

---

## Issue #10: Slow Download During "pip install -r requirements.txt"

### What Happens

The installation is taking forever (more than 10 minutes).

### Is This Normal?

It depends on your internet speed. 3-5 minutes is normal. If it's taking much longer:

**Option 1**: Be patient! It might just be slow internet.

**Option 2**: Check if your internet is working:

```bash
ping google.com
```

If it says "command not found" (Windows) or hangs, your internet might be down.

**Option 3**: Cancel and try again

Press `Ctrl+C` to stop, wait 10 seconds, then run again:

```bash
pip install -r requirements.txt
```

---

## Issue #11: Getting Errors with Red Text During Installation

### What Happens

You see lots of red error messages during `pip install -r requirements.txt`.

### Is This Normal?

**Usually yes!** Red text during pip install is often just warnings. Let it finish.

### When It's a Problem

Only if the process STOPS and returns to the prompt **without installing all packages**.

If that happens:

1. Scroll up to see the actual error (before the red warnings)
2. Copy the error message
3. Report it (it might be a network issue)

---

## Issue #12: Can't Remember Where I Put Piper Morgan

### How to Find It

**Mac/Linux**:

```bash
find ~ -name "piper-morgan" -type d
```

**Windows**:
Use File Explorer:

1. Click "This PC"
2. Use the search box in the top-right
3. Search for "piper-morgan"

Once you find it, remember the path for next time.

---

## Issue #13: "Python 3.9" But I Installed 3.12

### What Happens

You installed Python 3.12, but `python3 --version` still shows 3.9.

### What This Means

You probably have multiple Python versions installed. Your system is using an older one.

### How to Fix It

**Mac/Linux**:

Try using the full path to Python 3.12:

```bash
/usr/local/bin/python3.12 -m venv venv
```

Or find where Python 3.12 was installed:

```bash
which python3.12
```

**Windows**:

Use the Python launcher:

```bash
py -3.12 -m venv venv
```

---

## Issue #14: Getting Different Error Than Listed

### What to Do

1. **Read the error carefully** - it often tells you what's wrong
2. **Search the error online** - Google it (seriously, often helps!)
3. **Take a screenshot** of the full error
4. **Note**:
   - What step you were on
   - Your operating system (Mac, Windows, Linux)
   - Your Python version (`python3 --version`)
   - Your macOS/Windows version

---

## General Troubleshooting Steps

**When stuck, try these in order**:

1. **Read the error** - It's usually telling you what's wrong
2. **Try again** - Sometimes network glitches cause failures
3. **Check prerequisites** - Did you install Python and Git?
4. **Check virtual environment** - Do you see `(venv)` in your prompt?
5. **Try Step 8 again** - `pip install -r requirements.txt`
6. **Restart your terminal** - Close and open a new one
7. **Restart your computer** - If nothing else works
8. **Ask for help** - Copy the error message and report it

---

## Quick Checklist: Before You Start

- [ ] Python 3.11 or later? (`python3 --version`)
- [ ] Git installed? (`git --version`)
- [ ] Enough disk space? (500MB free)
- [ ] Terminal/Command Prompt open?
- [ ] Downloaded Piper Morgan? (`git clone ...`)
- [ ] Virtual environment created? (see `venv` folder)
- [ ] Virtual environment activated? (see `(venv)` in prompt)
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] API key configured? (in `config/PIPER.user.md`)

If all of these ✅, Piper Morgan should run!

---

## Still Stuck?

If none of these solutions work:

1. **Copy the ENTIRE error message** (including all red text)
2. **Note your system**: Mac/Windows, version number
3. **Note what step you were on**
4. **Report it** with these details

Good error reporting = faster help!

---

**Last updated**: October 27, 2025
**Status**: Ready to help new users!

---

## Issue #15: "scipy" Build Error (Preparing metadata failed)

**Error Message**:
```
ERROR: Unknown compiler(s): [['gfortran'], ['flang-new'], ['flang'], ...
```

Or:
```
× Preparing metadata (pyproject.toml) did not run successfully.
```

**Root Cause**:
- Your venv is using Python 3.13 (or newer) instead of 3.12
- scipy lacks pre-built wheels for Python 3.13+
- pip tries to build scipy from source, which requires a Fortran compiler (not installed)

**Why It Happens**:
- You ran `python3 -m venv venv` but your system `python3` is 3.13 or newer
- Or you deleted Python 3.13 but the old venv's shebang still points to it

**Solution**:

1. **Delete the old venv completely:**
   ```bash
   rm -rf venv
   ```

2. **On Mac, create venv with Python 3.12 explicitly:**
   ```bash
   python3.12 -m venv venv
   ```

3. **On Windows, use:**
   ```bash
   python -m venv venv
   ```
   (Python 3.12 should be in your PATH if you installed it correctly)

4. **Activate the new venv:**
   ```bash
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

5. **Verify Python version in venv:**
   ```bash
   python --version
   ```
   Should show `Python 3.12.x` (NOT 3.13+)

6. **Try pip install again:**
   ```bash
   pip install -r requirements.txt
   ```

**Prevention**:
- Always use `python3.12 -m venv venv` explicitly (not `python3`)
- When upgrading/reinstalling Python, always delete the old `venv` folder first
- Check your Python version before creating venv: `python3.12 --version`

**If You Still See 3.13 or 3.14**:
- Check your system: `which python3.12` should exist
- If missing, reinstall Python 3.12.10 from [python.org/downloads/release/python-31210/](https://www.python.org/downloads/release/python-31210/)
- Close your terminal completely and open a NEW one (PATH updates need a fresh terminal)
- Try Step 1 again

---

## Windows-Specific Issues

For comprehensive Windows setup and troubleshooting, see [Windows Setup Guide](./windows-setup-guide.md).

### Issue: Virtual Environment Activation Fails on Windows

**Error**:
```
.ps1 cannot be loaded because running scripts is disabled on this system
```

**Solution**:
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Answer "Y" when prompted
# Now try activation again:
.\venv\Scripts\Activate.ps1
```

### Issue: Pre-commit Hook Blocks Commit on Windows

**Error**:
```
❌ Pre-commit hook: Windows-illegal characters found in filenames
Windows filenames cannot contain: : < > " | ? *
```

**Why**: You're committing a file with illegal Windows characters.

**Solution**:
1. Rename the file to use dashes or underscores
2. Example: `file (10:30).txt` → `file-1030.txt`
3. Re-add and commit

**To bypass** (not recommended):
```powershell
git commit --no-verify
```

### Issue: Repository Clone Fails on Windows

**Error**:
```
error: unable to create file <path>: Filename too long
```

**Solution**:
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Then retry clone
```

### Issue: Path-Related Test Failures on Windows

**Error**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'tests/unit/...'
```

**Why**: Test paths use forward slashes (Linux style) but Windows uses backslashes.

**Solution**:
```powershell
# Use backslashes in pytest commands:
pytest tests\unit\test_file.py

# Or use quotes with forward slashes:
pytest "tests/unit/test_file.py"
```

### Issue: "python command not found" on Windows

**Why**: Python not in Windows PATH

**Solution**:
1. Uninstall Python from Settings → Apps
2. Download from https://www.python.org/downloads/
3. Run installer and **check "Add Python to PATH"**
4. Restart PowerShell/CMD
5. Verify: `python --version`

### Recommendation: Use WSL2

If you encounter Windows-specific issues, consider using **WSL2** (Windows Subsystem for Linux):

- No more path separator issues
- All bash scripts work natively
- Better Python compatibility
- Actually faster than native Windows

See [Windows Setup Guide - WSL2 Option](./windows-setup-guide.md#option-1-wsl2-recommended-for-windows-developers) for setup instructions.
