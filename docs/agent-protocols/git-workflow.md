---
type: protocol
title: Git Workflow Protocol
valid_from: "2026-01-24"
last_verified: "2026-06-19"
---

# Git Workflow Protocol

Feature branch discipline for Claude Code sessions.

---

## Critical Rule

**Never develop on `main`**. Every session has an assigned feature branch.

Branch format:
- Starts with `claude/`
- Ends with session ID
- Example: `claude/ux-quick-wins-015W99syFQ7b9HrV2WoB9S48`

---

## Session Start

```bash
# Look up assigned branch from session instructions
# (Listed in "Git Development Branch Requirements")

git fetch origin <your-assigned-branch>
git checkout <your-assigned-branch>

# Verify
git branch  # Should show: * claude/your-branch-[SESSION_ID]
            # NOT: * main
```

---

## Development Workflow

```bash
# 1. Make changes on feature branch (never main)

# 2. Before committing - ALWAYS run this first
./scripts/fix-newlines.sh

# 3. Commit
git add <specific-files>  # Prefer specific files over "git add ."
git commit -m "your message"

# 4. Push to YOUR branch only
git push -u origin <your-assigned-branch>
```

---

## Branch Checklist

Before EVERY commit:

- [ ] `git branch` shows your assigned branch (not main)
- [ ] Branch starts with `claude/`
- [ ] Branch ends with your session ID
- [ ] You ran `./scripts/fix-newlines.sh`

---

## If You Accidentally Worked on Main

```bash
# Don't panic
git checkout <your-assigned-branch>
git log main..HEAD  # See commits that shouldn't be there
# Ask PM how to recover
```

---

## Why This Matters

- 403 errors on push to main are **intentional**
- Feature branches prevent conflicts
- Session ID in branch proves authorization
- Work stays isolated until merged

---

## Server Restart (if stuck)

```bash
# Find what's on port 8001
lsof -i :8001

# Kill by PID (column 2 of lsof output)
kill <PID>

# Verify port is free
lsof -i :8001  # Should return nothing

# Start fresh
python main.py

# Verify
lsof -i :8001  # Should show new PID
```

Note: `pkill -f "python main.py"` may fail if process name differs. Use port-based detection.
