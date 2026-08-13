# Version Bump & venv Fix — a Resolved Incident, Kept for Reference

**What this is**: a record of two specific bugs the Piper Morgan team hit and fixed in November 2025 — a missed version bump and a `venv/` directory that had been accidentally tracked in git. Both are resolved; this page is kept because the root causes (a deploy commit that named a version without updating the version files; a `.gitignore` entry added after files were already tracked) are common enough mistakes that seeing the actual fix may save you time if you hit either one yourself.

**Created**: 2025-11-24
**Purpose**: Fix two issues discovered during test laptop setup

---

## Issue 1: Version Bump Never Happened

The "Deploy v0.8.1" commit (8ce65661) only had "0.8.1" in the commit message - the actual version files were never updated.

### Steps to Fix (on dev laptop)

```bash
# 1. Make sure you're on main branch and up to date
git checkout main
git pull origin main

# 2. Update VERSION file
echo "0.8.1" > VERSION

# 3. Update pyproject.toml - change line 7 from:
#    version = "0.8.0-alpha"
#    to:
#    version = "0.8.1"

# 4. Update docs/versioning.md - change line 3 from:
#    ## Current Version: 0.8.0-alpha
#    to:
#    ## Current Version: 0.8.1
#
#    Also update the version history table at the bottom

# 5. Commit the version bump
git add VERSION pyproject.toml docs/versioning.md
git commit -m "chore: Bump version to 0.8.1

Updates VERSION file, pyproject.toml, and versioning.md to reflect
the actual deployed version. This was missed during the 0.8.1 deployment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 6. Create git tag
git tag -a v0.8.1 -m "Version 0.8.1 - Alpha testing release (Nov 21-23 features)"

# 7. Push changes and tag
git push origin main
git push origin v0.8.1

# 8. Merge to production branch
git checkout production
git merge main
git push origin production
```

---

## Issue 2: venv Tracked in Git (Causing Corruption)

The venv directory is being tracked in git despite being in .gitignore. This causes corruption when cloning/pulling on different machines (hardcoded paths).

### Root Cause
`.gitignore` only prevents NEW files from being tracked. Files already tracked before the gitignore entry was added remain tracked.

### Steps to Fix (on dev laptop)

```bash
# 1. Make sure you're on main branch
git checkout main

# 2. Remove venv from git tracking (keeps local files)
git rm -r --cached venv/

# 3. Verify .gitignore has venv entry (it should)
grep "venv" .gitignore
# Should show: venv/

# 4. Commit the removal
git add .gitignore
git commit -m "chore: Remove venv from git tracking

The venv directory was being tracked despite .gitignore entry.
This caused corruption when pulling on different machines due to
hardcoded Python interpreter paths in venv/bin/*.

.gitignore only prevents NEW files from being tracked - files
already tracked before the gitignore entry need explicit removal.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 5. Push to main
git push origin main

# 6. Merge to production
git checkout production
git merge main
git push origin production
```

---

## Verification

After completing both fixes:

```bash
# Verify version files
cat VERSION                           # Should show: 0.8.1
grep version pyproject.toml | head -1 # Should show: version = "0.8.1"

# Verify venv not tracked
git ls-files | grep venv              # Should return nothing

# Verify tag exists
git tag -l | grep v0.8.1              # Should show: v0.8.1
```

---

## Prevention (Future)

1. **Version bumps**: Add to deployment checklist - update VERSION, pyproject.toml, docs/versioning.md, create tag
2. **venv tracking**: Already prevented by .gitignore now that existing tracked files are removed
3. **Consider**: Add pre-commit hook to validate version consistency across files

---

## Related Files

- `VERSION` - Single source of truth for version
- `pyproject.toml` - Python package version
- `docs/versioning.md` - Version strategy documentation
- `.gitignore` - Should have `venv/` entry
