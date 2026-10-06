---
name: discovered-work-capture
description: Capture discovered work as tracking issues immediately. Use when you notice test failures, bugs, missing features, or technical debt during development. Prevents invisible work and ensures PM can prioritize appropriately.
scope: cross-role
version: 1.1
created: 2026-01-26
---

# discovered-work-capture

> **Tracker: GitHub issues** (`gh issue create`). This skill used to say `bd create`, but the beads CLI isn't installed on Amber; every seat already files via `gh` (CIO ruling 2026-10-05, from Docs's finding). Note that all seats share one GitHub author, so `--author @me` doesn't isolate your own filings; search by title prefix instead.

**Purpose**: Ensure all discovered work is captured as tracking issues immediately, preventing invisible work and enabling proper prioritization.

---

## Core Principle

**"Not my problem" is NEVER valid reasoning.**

When you discover an issue during development, you don't decide whether it matters—you file it, and PM decides priority. Untracked work is invisible work. Invisible work accumulates into technical debt, surprise failures, and broken user experiences.

---

## Trigger Conditions (When to Use)

**You MUST use this skill when you encounter:**

1. **Test failures not caused by your current changes**
   - You're working on feature X, but test Y fails
   - The failure predates your work
   - File it: `gh issue create --title "TEST-FAILURE: [describe]" --body "<what, where, evidence>"`

2. **Bugs noticed during development**
   - You observe incorrect behavior while testing your work
   - It's not directly related to your current task
   - File it: `gh issue create --title "BUG: [describe]" --body "<what, where, evidence>"`

3. **Missing features that should exist**
   - You expected capability X but it's not implemented
   - You had to work around a gap
   - File it: `gh issue create --title "MISSING: [describe]" --body "<what, where, evidence>"`

4. **Technical debt observations**
   - Code that should be refactored
   - Patterns that don't match conventions
   - Performance concerns
   - File it: `gh issue create --title "TECH-DEBT: [describe]" --body "<what, where, evidence>"`

5. **Documentation gaps**
   - Missing or outdated docs that caused confusion
   - File it: `gh issue create --title "DOCS: [describe]" --body "<what, where, evidence>"`

---

## Workflow

### Step 1: Notice the Issue

During your work, you observe something that isn't right but isn't your current task.

**Wrong response**: "That's not related to my work, I'll ignore it."
**Correct response**: "I need to file this before continuing."

### Step 2: Create the Issue Immediately

```bash
# Use bd (beads CLI) to create the issue
gh issue create --title "CATEGORY: Brief description of the issue" --body "<what, where, evidence>"

# Example:
gh issue create --title "TEST-FAILURE: test_user_preferences fails with KeyError on empty config" --body "<what, where, evidence>"
```

### Step 3: Add Context

The issue should include:
- What you observed
- Where you observed it (file, line, test name)
- How you encountered it (what were you doing?)
- Any error messages or output

### Step 4: Link if Relevant

```bash
# If discovered while working on another issue:
bd dep add <new-issue> <parent-issue> --type discovered-from
```

### Step 5: Continue Your Work

After filing, return to your assigned task. PM will triage and prioritize the new issue.

### Step 6: Session Wrap-up

Before ending your session, your log MUST include:

```markdown
### Discovered Issues Filed
- #XXX: TEST-FAILURE: [description]
- #YYY: BUG: [description]
- (or "None" if no discoveries)
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correction |
|--------------|----------------|------------|
| "I'll file it later" | Later never comes; context is lost | File NOW, takes 30 seconds |
| "It's not blocking me" | Blocking YOU isn't the criteria | PM decides priority |
| "Someone else will notice" | They might not; you noticed NOW | You file it NOW |
| "It's too small to track" | Small issues compound | File it; PM can close as won't-fix |
| "I'll just fix it quickly" | Scope creep; unplanned work | File first, then ask PM if you should fix |
| "Not my area" | Ownership doesn't matter for filing | File it; correct owner will be assigned |

---

## Why This Matters

### The Invisible Work Problem

Work that isn't tracked:
- Doesn't get prioritized
- Doesn't get resources
- Doesn't get credit when fixed
- Compounds until it causes an outage or user complaint

### The Discovery Advantage

You noticed something *because* you were in the code. That context is valuable:
- You know what you were doing when you found it
- You can describe the symptoms accurately
- You have the error messages fresh

If you don't file it now, that context evaporates.

### The Priority Fallacy

"I shouldn't file this because it's not important" is a priority decision. **You don't make priority decisions.** PM does. Your job is to surface the work. PM decides when (or if) it gets done.

---

## Session Wrap-up Checklist

Before marking your session complete:

- [ ] Review work done for any discovered issues
- [ ] All discoveries filed with `gh issue create`
- [ ] Session log includes "Discovered Issues Filed" section
- [ ] If no discoveries: explicitly state "None" (proves you checked)

---

## Quick Reference

```bash
# Create discovered issue
gh issue create --title "CATEGORY: Description" --body "<what, where, evidence>"

# Categories
TEST-FAILURE:  # Test that fails unexpectedly
BUG:           # Incorrect behavior observed
MISSING:       # Expected capability not present
TECH-DEBT:     # Code that needs improvement
DOCS:          # Documentation gap or error

# Link to parent work
bd dep add <new> <parent> --type discovered-from

# List your filed issues
gh issue list --search "in:title CATEGORY:" --state open
```

---

*Skill created: January 26, 2026*
*Per CIO approval of Simple Trigger Architecture*
