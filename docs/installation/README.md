# Installation Guides

**New to Piper Morgan?** Start here. Choose your path:

---

## 🚀 Quick Start (Recommended)

If you just want to **get it running**:

1. Read: **[Prerequisites Comprehensive](./PREREQUISITES-COMPREHENSIVE.md)** (2 min)
   - Verify you have Python 3.12, Git, Docker installed
   - Check supported OS & minimum specs

2. Follow: **[Step-by-Step Installation](./step-by-step-installation.md)** (20-30 min)
   - Clone repo
   - Launch Docker Desktop
   - Run setup wizard
   - Done!

---

## 📚 Reference Guides

These are for **specific questions**, not required reading:

- **[Key Setup Guide](./key-setup.md)** - How to manage API keys securely (keychain vs env vars)
- **[Quick Reference](./quick-reference.md)** - Cheat sheet for common commands
- **[Troubleshooting](./troubleshooting.md)** - Common errors & fixes

---

## ✅ Check Your Setup

Before starting, verify:

```bash
python3.12 --version      # Python 3.12.x
git --version             # git 2.x+
docker --version          # Docker 20.x+
```

If any are missing, see **Prerequisites** above.

---

## 🎯 Flow Diagram

```
START
  ↓
Read: PREREQUISITES-COMPREHENSIVE (verify you have everything)
  ↓
Follow: step-by-step-installation (clone + wizard + done)
  ↓
Running! Open http://localhost:8001
  ↓
(Optional) Read key-setup.md or troubleshooting.md if you hit issues
```

---

## 🆘 Stuck?

1. Check **[Troubleshooting](./troubleshooting.md)** for your error
2. If not listed, continue with setup anyway—many errors are non-blocking
3. The wizard will tell you what's actually wrong

---

**Last Updated**: October 29, 2025
**Status**: Ready for alpha testing *(directionally still true — alpha is ongoing per
`docs/README.md` — but this page's own content wasn't re-verified today; flagged 2026-08-11
during #1583/#1585 rather than silently re-dating without a real review)*
