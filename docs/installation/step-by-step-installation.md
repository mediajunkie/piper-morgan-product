# 🚀 Piper Morgan: Complete Installation Guide

**For**: First-time users, fresh laptops, zero assumptions
**Time**: ~20-30 minutes from complete nothing to running Piper Morgan
**Difficulty**: Beginner-friendly (we explain everything)

---

## ⚠️ Prerequisites: Do You Have What You Need?

**Before starting, verify you have everything:**

→ **[Read: Comprehensive Prerequisites Guide](./PREREQUISITES-COMPREHENSIVE.md)**

This covers:

- ✅ System requirements (OS, RAM, disk)
- ✅ Python 3.12 installation & verification
- ✅ Git installation & verification
- ✅ Docker Desktop installation & verification
- ✅ How to check everything with verification commands

**Skip ahead only if you already verified all four items above.**

---

## 🎯 Installation: Let's Get Piper Morgan Running

### Step 1: Open Terminal/Command Prompt

**Mac**:

1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter
4. You'll see a window with a command prompt

**Windows**:

1. Press `Windows + R`
2. Type "cmd"
3. Press Enter
4. You'll see a black window with a command prompt

**Keep this window open** for all remaining steps. Don't close it!

---

### Step 2: Create a Folder for Piper Morgan

We'll create a dedicated folder to keep everything organized.

**Type this command** (press Enter after each line):

```bash
cd ~
mkdir piper-morgan-workspace
cd piper-morgan-workspace
```

**What these do**:

- `cd ~` takes you to your home folder (fastest way)
- `mkdir piper-morgan-workspace` creates a new folder
- `cd piper-morgan-workspace` moves you into that folder

**Verify it worked**: Type `pwd` and press Enter. You should see a path ending in `piper-morgan-workspace`.

---

### Step 3: Download Piper Morgan

**Type this command** (press Enter after each line):

```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
```

**What these do**:

- `git clone ...` downloads the Piper Morgan code into a new `piper-morgan-product` folder
- `cd piper-morgan-product` moves you into that folder

**Verify it worked**: Type `pwd` and press Enter. You should see a path ending in `piper-morgan-product`.

---

## 🚀 Start Docker (Required Before Wizard)

Piper Morgan's database runs in Docker. First, **make sure Docker Desktop is running**:

**Mac**:

1. Press `Cmd + Space`
2. Type "Docker"
3. Press Enter (launches Docker Desktop)
4. **Wait 30 seconds** for the whale icon to appear in the menu bar (top-right)
5. Make sure the whale icon is **solid/filled** (not grayed out)

**Windows**:

1. Click the Windows Start menu
2. Search for "Docker Desktop"
3. Click "Docker Desktop" to launch it
4. **Wait 30 seconds** for Docker to start
5. Look for the whale icon in the system tray (bottom-right)

**Once Docker is running**, open a **new terminal tab** and start the database:

**Mac/Linux**:

```bash
docker-compose up -d postgres
```

**Windows** (PowerShell):

```bash
docker-compose up -d postgres
```

Press Enter.

**What you'll see**:

```
Creating network "piper-morgan-product_default" with the default driver
Creating piper-morgan-product_db_1 ...
Creating piper-morgan-product_db_1 ... done
```

✅ **If you see "done"**: Database is starting! Give it 10 seconds to fully initialize.

**Keep this terminal tab open** (Docker will keep running).

Go back to your **original terminal tab** (the one in the piper-morgan-product folder) and proceed below.

---

## 🎯 Recommended: Use the Setup Wizard (Automated)

Instead of doing the manual steps below, you can use the automated setup wizard:

```bash
python3.12 main.py setup
```

This single command will:

1. ✅ Check for Python 3.12
2. ✅ Create your virtual environment
3. ✅ Install all dependencies
4. ✅ Generate SSH key (if needed)
5. ✅ Guide you through GitHub setup
6. ✅ System checks (Docker, port, database)
7. ✅ Create your user account
8. ✅ Collect and validate API keys

**Time**: ~5-10 minutes total (including waiting for dependencies to install)

If you prefer to do it manually, continue below. Otherwise, you're done! 🎉

---

## Manual Setup (Optional Alternative)

If you prefer to understand each step, follow the steps below. Both approaches work!

⚠️ **Note**: these steps currently stop after installing dependencies (Step 8) and don't yet cover verifying the install or starting the server — if you're following the manual path, use the [Quick Reference](./quick-reference.md)'s steps 6 onward (verify installation, then `python main.py`) to finish.

### Step 5: Create a Python Virtual Environment

This is **critical**. A virtual environment isolates Piper Morgan's Python packages from the rest of your system.

⚠️ **IMPORTANT: First, clean up any old virtual environment**

If you see a `venv` folder from a previous attempt, delete it:

```bash
rm -rf venv
```

Press Enter.

**Now create the virtual environment using Python 3.12 explicitly:**

**Mac**:

```bash
python3.12 -m venv venv
```

**Windows**:

```bash
python -m venv venv
```

Press Enter.

**What this does**: Creates a special folder called `venv` that contains everything Piper Morgan needs, using Python 3.12.

**What you'll see**: Nothing much. The command runs silently. Wait for the command prompt to return.

**This takes ~30-60 seconds.** Don't interrupt!

**Verify it worked**: Type `ls -la` and press Enter. You should see a folder named `venv` in the list.

**Troubleshoot**: If you see an error like `python3.12: command not found`:

- On Mac: You need to install Python 3.12.10. Go back to Check 1 and follow the Python installation steps.
- On Windows: The installer should have added Python to PATH. Close your command prompt completely, open a NEW one, and try again.

---

### Step 6: Activate the Virtual Environment (CRITICAL STEP)

This step changes your terminal to use the Piper Morgan Python environment. **You must do this step or nothing will work.**

**Mac/Linux - Type this command**:

```bash
source venv/bin/activate
```

**Windows - Type this command**:

```bash
venv\Scripts\activate
```

Press Enter.

**What you'll see**: Your command prompt changes. Look at the beginning of the line—it should now say `(venv)` before your username.

**Before**: `username@computer piper-morgan $`
**After**: `(venv) username@computer piper-morgan $`

❌ **If you don't see `(venv)`**: The activation didn't work. Try the command again.

✅ **If you see `(venv)`**: Perfect! You're now using the virtual environment.

⚠️ **Important**: Every time you close your terminal and open a new one, you'll need to repeat this step (Step 6) to use Piper Morgan again!

---

### Step 7: Update pip (Python's Package Installer)

pip is the software that installs Python packages. Let's make sure it's up to date.

**Type this command**:

```bash
pip install --upgrade pip
```

Press Enter.

**What you'll see**: Text showing pip being downloaded. This takes ~30 seconds. Wait for the prompt to return.

**Verify it worked**: Type `pip --version` and press Enter. You should see a version number.

---

### Step 8: Install All Python Dependencies (THE KEY STEP)

This command installs all the Python packages Piper Morgan needs.

**Type this command**:

```bash
pip install -r requirements.txt
```
