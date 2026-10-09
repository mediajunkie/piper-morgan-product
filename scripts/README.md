# Piper Morgan Scripts

**Purpose**: Automated maintenance and workflow scripts
**Last Updated**: October 17, 2025

---

## Available Scripts

### 📝 update-briefing.sh

> **Obsolete since 2026-10-08**: BRIEFING-CURRENT-STATE.md is now a short "Now" page with no STATUS BANNER (R6 step 3). Use the `update-current-state` skill and `scripts/check-current-state.py` instead.

**Purpose**: Automatically update BRIEFING-CURRENT-STATE.md position and timestamp

**Usage**:
```bash
# Interactive mode (recommended for first time)
./scripts/update-briefing.sh

# Auto mode (use suggested position)
./scripts/update-briefing.sh --auto

# Specify exact position
./scripts/update-briefing.sh --position 2.3.5

# Show help
./scripts/update-briefing.sh --help
```

**What it does**:
1. Reads current position from BRIEFING-CURRENT-STATE.md
2. Suggests next position (auto-increments patch version)
3. Derives sprint from position (2.3.4 = A3, 2.3.5 = A4, etc.)
4. Generates current timestamp
5. Updates STATUS BANNER section
6. Creates backup before changes
7. Shows diff for verification
8. Verifies symlink propagation to knowledge/

**When to use**:
- End of each coding session
- When sprint position changes
- After completing major milestones
- Weekly if briefing feels stale

**Safety features**:
- Creates backup before changes
- Shows diff before committing
- Easy revert: `cp docs/briefing/BRIEFING-CURRENT-STATE.md.backup docs/briefing/BRIEFING-CURRENT-STATE.md`
- Works with symlinks (updates propagate to knowledge/)

**Position-to-Sprint mapping**:
```
2.3.1 = A1 (Critical Infrastructure)
2.3.2 = CRAFT (Superepic)
2.3.3 = A2 (Notion & Errors)
2.3.4 = A3 (Ethics & Knowledge)
2.3.5 = A4 (Standup Epic)
2.3.6 = A5 (Learning System)
2.3.7 = A6 (Polish & Onboarding)
2.3.8 = A7 (Testing & Buffer)
```

**Example session**:
```bash
$ ./scripts/update-briefing.sh

================================
  Briefing Update Tool
================================

Current position: 2.3.4 (Sprint A3)
Current timestamp: October 17, 2025, 11:09 AM PT

What is the new position?
  [Enter] = 2.3.5 (suggested)
  Or type a custom position (e.g., 2.3.5)
> [ENTER]

✓ New position: 2.3.5 (Sprint A4)
✓ New timestamp: October 17, 2025, 11:50 AM PT

✓ Created backup: docs/briefing/BRIEFING-CURRENT-STATE.md.backup
✓ Updated BRIEFING-CURRENT-STATE.md

Changes made:
---
< **Current Position**: 2.3.4 (Complete the Build of CORE - Sprint A3 Active)
< **Last Updated**: October 17, 2025, 11:09 AM PT
---
> **Current Position**: 2.3.5 (Complete the Build of CORE - Sprint A4 Active)
> **Last Updated**: October 17, 2025, 11:50 AM PT
---

✓ Symlink verified - changes propagate to knowledge/

Update complete!

Next steps:
  1. Review changes above
  2. If correct, commit: git add docs/briefing/BRIEFING-CURRENT-STATE.md
  3. Or revert: cp docs/briefing/BRIEFING-CURRENT-STATE.md.backup docs/briefing/BRIEFING-CURRENT-STATE.md
  4. Clean up backup: rm docs/briefing/BRIEFING-CURRENT-STATE.md.backup
```

---

### 🔧 fix-newlines.sh

**Purpose**: Fix end-of-file newlines to prevent pre-commit hook failures

**Usage**:
```bash
./scripts/fix-newlines.sh
```

**When to use**: Before every git commit (see CLAUDE.md for details)

---

### 🎯 new-pattern.sh

**Purpose**: Create new architecture pattern with proper numbering

**Usage**:
```bash
./scripts/new-pattern.sh
```

---

### 📋 new-adr.sh

**Purpose**: Create new Architecture Decision Record with proper numbering

**Usage**:
```bash
./scripts/new-adr.sh
```

---

### ✅ phase-z-validation.sh

**Purpose**: Comprehensive end-to-end validation for Phase Z completion

**Usage**:
```bash
./scripts/phase-z-validation.sh
```

---

## Adding New Scripts

**Guidelines**:
1. Use `.sh` extension for shell scripts
2. Start with shebang: `#!/bin/bash`
3. Add `set -e` for error handling
4. Include usage/help output
5. Document in this README
6. Make executable: `chmod +x scripts/your-script.sh`
7. Test thoroughly before committing

**Script template**:
```bash
#!/bin/bash
# scripts/your-script.sh
# Brief description

set -e  # Exit on error

# Your code here
```

---

## Maintenance

- Scripts tested on macOS (Darwin)
- May need adjustment for Linux (especially `sed -i` syntax)
- Keep this README updated when adding/modifying scripts
- Test scripts in dev environment before production use

---

**See also**:
- `knowledge/README.md` - Workflow documentation
- `CLAUDE.md` - Agent instructions
- `.github/workflows/` - Automated CI/CD scripts
