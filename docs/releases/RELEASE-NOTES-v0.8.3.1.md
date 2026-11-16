# Release Notes: v0.8.3.1

**Release Date**: January 7, 2026
**Release Type**: Patch Release (Sprint B1 FTUX improvements)

---

## Overview

This patch release delivers the Sprint B1 P0 "First Time User Experience" (FTUX) improvements, focusing on making Piper's first impression warmer and more oriented.

---

## What's New

### FTUX-PIPER-INTRO (#547)
**Piper greeting panel in setup wizard**

New users now see a friendly greeting from Piper Morgan at the start of the setup wizard:

> "Hi, I'm Piper Morgan, your PM assistant! You can call me Piper."
>
> "I'm here to help you with product management work—tracking tasks, managing GitHub issues, prepping for standups, and staying on top of your calendar."

- Friendly introduction sets expectations
- Dismissible panel (doesn't block setup)
- Accessible with ARIA role and keyboard support

### FTUX-EMPTY-STATES (#548)
**Voice-guided empty state copy**

Empty states across all primary views now use Piper's voice instead of generic system messages:

| View | Before | After |
|------|--------|-------|
| Todos | "No todos yet. Create your first todo." | "No todos yet. Say 'add a todo: [task]' to create one, or I can suggest some based on your open GitHub issues." |
| Projects | "No projects found." | "No projects set up yet. Projects help me understand your work context. Say 'create a project called...' to get started." |
| Files | "No files uploaded." | "No documents in your knowledge base yet. You can upload files, connect Notion, or just paste content into our chat—I'll remember it for later." |
| Lists | "No lists yet." | "No lists yet. Say 'create a list called...' to get started. Lists help you group and organize related items." |

### FTUX-POST-SETUP (#549)
**Post-setup orientation modal**

After completing setup, users now see a brief orientation modal:

> "You're all set! Here are some things we can do together..."

- Shows integration-aware suggestions (GitHub, Calendar, Todos)
- Only appears once (persisted dismissal)
- Dismissible with button or Escape key

---

## Bug Fixes

- **#549 UUID fix**: Fixed orientation modal not appearing due to UUID type mismatch in SQL parameter binding
- **#548 CSS fix**: Fixed Files empty state not spanning full grid width

---

## Technical Details

### Commits Included
```
88a8faab fix(#549): Convert UUID to string for SQL parameter binding
ebbc93d9 fix(ui): Files empty state spans full grid width
7c1b3168 fix(test): Use naive datetime in orientation integration tests
b82b674a feat(ftux): Add post-setup orientation modal (#549)
e993005f feat(ftux): Replace empty state copy with voice guide templates (#548)
ab6716e1 feat(ftux): Add Piper greeting panel to setup wizard (#547)
c801450f docs: Add Lists View section to empty state voice guide
```

### Database Migration
- Migration `336bd317e5cc`: Adds `orientation_seen` column to users table

### New Endpoints
- `POST /api/v1/orientation/dismiss` - Marks orientation as seen for user

### Test Coverage
- 15 new tests across FTUX features
- 1198 unit tests passing

---

## Upgrade Notes

**From v0.8.3:**
1. Run database migration: `alembic upgrade head`
2. Restart application

No breaking changes. Existing users will see the orientation modal on first login after upgrade.

---

## Known Issues

See [ALPHA_KNOWN_ISSUES.md](../BETA_KNOWN_ISSUES.md) for current known issues.

**New follow-up issue:**
- #550: Add "Ask Piper" button to empty states (bridges users to chat when on pages without chat input)

---

## Contributors

- PM: xian
- Lead Developer: Claude Code (Opus)
- Subagents: Task agents for #547, #548, #549 implementation

---

*Release managed by Lead Developer session 2026-01-07*
