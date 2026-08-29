# Knowledge Base Staging Area

**Purpose**: Files that exist in claude.ai web project knowledge but have no other home in the repository
**Last Updated**: February 18, 2026

---

## Overview

This directory contains files that are added to the claude.ai project knowledge base but **do not belong elsewhere in the repository**.

**Key principle**: If a file has a natural home in the repository (e.g., briefings belong in `docs/briefing/`, patterns belong in `docs/internal/architecture/patterns/`), it should live there — NOT here. When adding such files to web project knowledge, add them directly from their canonical location.

---

## What Belongs Here

Files in this directory should be:
- **Web project knowledge only**: Content created specifically for the claude.ai knowledge base
- **No other home**: Doesn't fit naturally elsewhere in the repo structure
- **Reference material**: Templates, guides, glossaries used by web project agents

**Examples of files that belong here**:
- `gameplan-template.md` — Template for agent gameplans (no natural home in docs/)
- `agent-prompt-template.md` — Template for agent prompts
- `piper-morgan-glossary-v1.1.md` — Project glossary for agents
- `serena-briefing-queries.md` — Symbolic query reference
- `CLAUDE.md` — Agent entry point for web project

---

## What Does NOT Belong Here

**BRIEFING-* files**: These now live in `docs/briefing/` (their natural home as documentation)
- When updating web project knowledge, add briefings directly from `docs/briefing/`
- No symlinks, no copies — just one canonical location

**Other repository content**: Patterns, ADRs, guides, etc. should live in their proper locations and be added to web knowledge from there.

---

## Workflow

### For Developers/Agents

1. **Update briefings** in `docs/briefing/` (not here)
2. **Update templates** here if they're web-project-only files
3. **Don't create BRIEFING-* files here** — they belong in docs/briefing/

### For PM (Web Knowledge Updates)

When updating claude.ai project knowledge:

1. **Briefings**: Add directly from `docs/briefing/BRIEFING-*.md`
2. **Templates/glossaries**: Add from `knowledge/` (this directory)
3. **Other docs**: Add from their canonical location in the repo

---

## Current Files

| File | Purpose |
|------|---------|
| `agent-prompt-template.md` | Template for agent task prompts |
| `gameplan-template.md` | Template for issue gameplans |
| `piper-morgan-glossary-v1.1.md` | Project terminology glossary |
| `serena-briefing-queries.md` | Symbolic query reference |
| `CLAUDE.md` | Web project agent entry point |
| `claude-desktop-briefing-guide.md` | Guide for briefing web agents |
| `session-log-instructions.md` | How to maintain session logs |
| `team-structure.md` | Agent team structure |
| `work-streams-definition.md` | Workstream definitions |
| `github-guide.md` | GitHub workflow guide |
| `tdd-pragmatic-approach.md` | Testing philosophy |
| Various other templates and guides | See directory listing |

---

## Related Documentation

- **docs/briefing/** — All BRIEFING-* files (canonical location)
- **docs/NAVIGATION.md** — Complete documentation navigation
- **.github/workflows/weekly-docs-audit.yml** — Automated weekly checks

---

## Cleanup History

**February 18, 2026**: Removed all BRIEFING-* files from knowledge/. These now live only in `docs/briefing/`. Removed symlinks in both directions. Single canonical location = zero drift.

---

*Last updated: February 18, 2026*
