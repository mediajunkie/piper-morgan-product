# ⚡ Piper Morgan Installation - Quick Reference

**Keep this handy!** Print it or save it to your phone.

---

## 📋 Pre-Installation Checklist

- [ ] Python 3.11+ installed: `python3 --version`
- [ ] Git installed: `git --version`
- [ ] ~500MB disk space available
- [ ] Anthropic API key ready ([get one here](https://console.anthropic.com))

---

## 🚀 Installation (First Time Only)

```bash
# 1. Create workspace
cd ~
mkdir piper-morgan-workspace
cd piper-morgan-workspace

# 2. Download Piper Morgan
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate           # Mac/Linux
# OR
venv\Scripts\activate              # Windows

# 5. Install dependencies (CRITICAL STEP - DON'T SKIP!)
pip install --upgrade pip
pip install -r requirements.txt

# 6. Verify installation
pip list | grep structlog          # Should show: structlog 23.2.0

# 7. Create config
cp config/PIPER.example.md config/PIPER.user.md

# 8. Edit config (add your API key)
open config/PIPER.user.md          # Mac
# OR
notepad config/PIPER.user.md       # Windows
# Find: anthropic_api_key: "your-key-here"
# Replace with your actual key

# 9. Verify everything
python -c "from services.container.service_container import ServiceContainer; print('✅ Ready!')"

# 10. Start Piper Morgan!
python main.py
```

**⏱️ Total time**: 20-30 minutes (mostly waiting for downloads)

---

## ▶️ Starting Piper Morgan (Every Time)

```bash
# 1. Navigate to folder
cd ~/piper-morgan-workspace/piper-morgan-product

# 2. Activate virtual environment
source venv/bin/activate           # Mac/Linux
# OR
venv\Scripts\activate              # Windows

# 3. Start
python main.py
```

**Key**: You must see `(venv)` in your prompt before running `python main.py`

---

## 🆘 Common Issues (Quick Fixes)

| Problem                          | Solution                                                  |
| -------------------------------- | --------------------------------------------------------- |
| `ModuleNotFoundError: structlog` | Run `pip install -r requirements.txt`                     |
| No `(venv)` in prompt            | Run the activation command (see above)                    |
| `command not found: python3`     | Install Python 3.12 from [python.org](https://python.org) |
| `command not found: git`         | Install Git from [git-scm.com](https://git-scm.com)       |
| `Invalid API key`                | Update `config/PIPER.user.md` with correct key            |
| `Address already in use`         | Close other Piper Morgan window                           |

**More help?** See `docs/installation/troubleshooting.md`

---

## 📂 Key Files & Folders

```
~/piper-morgan-workspace/piper-morgan-product/
├── venv/                          # Virtual environment (created during install)
├── config/
│   └── PIPER.user.md             # Your configuration (created from example)
├── requirements.txt               # Dependencies list
├── main.py                        # Start Piper Morgan here
└── docs/installation/
    ├── step-by-step-installation.md  # Full instructions
    ├── troubleshooting.md             # Common problems & fixes
    └── quick-reference.md            # This file!
```

---

## ✅ Success Checklist

After installation, you should be able to:

- [ ] Run `python main.py` and see startup messages
- [ ] Piper Morgan responds to commands
- [ ] Web interface accessible at http://localhost:8001
- [ ] Next time: Navigate, activate venv, run main.py (3 commands)

---

## 🔑 Important Commands

| Command                           | What It Does               |
| --------------------------------- | -------------------------- |
| `python3 --version`               | Check Python version       |
| `git --version`                   | Check Git version          |
| `python3 -m venv venv`            | Create virtual environment |
| `source venv/bin/activate`        | Activate (Mac/Linux)       |
| `venv\Scripts\activate`           | Activate (Windows)         |
| `pip install -r requirements.txt` | Install all dependencies   |
| `pip list \| grep structlog`      | Verify structlog installed |
| `python main.py`                  | Start Piper Morgan         |
| `Ctrl+C`                          | Stop Piper Morgan          |

---

## 🌐 Important URLs

- **Python 3.12**: https://python.org/downloads
- **Git**: https://git-scm.com
- **Anthropic Console**: https://console.anthropic.com
- **Piper Morgan GitHub**: https://github.com/mediajunkie/piper-morgan-product

---

## 💡 Pro Tips

1. **Keep terminal open** - Don't close it while Piper Morgan is running
2. **Check (venv)** - Always look for `(venv)` before pip/python commands
3. **Wait for downloads** - `pip install -r requirements.txt` takes 3-5 min
4. **Save your API key** - Copy it somewhere safe
5. **Use copy-paste** - Commands are complex, copy-paste is your friend

---

## 🆘 When All Else Fails

1. Read the error message **completely** (not just the first line)
2. Search the error on Google (often has solutions)
3. Check `troubleshooting.md` for your specific error
4. Report with: error message + step you were on + OS version

---

**Last updated**: October 27, 2025
**For**: Piper Morgan v0.8.0-alpha
