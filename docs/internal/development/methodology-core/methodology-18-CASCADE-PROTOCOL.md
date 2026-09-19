---
type: methodology
title: Methodology Cascade Protocol
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Methodology Cascade Protocol
**Version**: 1.0
**Date**: September 4, 2025
**Purpose**: Ensure methodology DNA flows through all coordination layers

---

## Overview

The Cascade Protocol ensures our systematic methodology transfers intact from PM through Chief Architect to Lead Developer to Agents, preventing the ~1 hour manual overhead of recreating context each session.

---

## Layer Structure

### Layer 0: PM → Chief Architect
**Methodology Transfer via**:
- Project instructions (always fresh)
- Session starter prompt template
- Explicit methodology reminders

**Key DNA Elements**:
- Excellence Flywheel principles
- GitHub-first development
- Verification before implementation
- Evidence-based claims

### Layer 1: Chief Architect → Lead Developer
**Methodology Transfer via**:
- Gameplan using gameplan-template.md
- Phase 0 requirements explicit
- Agent-specific instructions
- STOP conditions included

**Key DNA Elements**:
- Different requirements for Code vs Cursor
- Cross-validation protocol
- Artifact locations specified
- Bookending requirements

### Layer 2: Lead Developer → Agents
**Methodology Transfer via**:
- Agent prompts in artifacts
- agent-prompt-template.md usage
- Explicit context injection
- Different guardrails per agent

**Key DNA Elements**:
- Code: Read CLAUDE.md, can investigate broadly
- Cursor: Explicit constraints, check shared_types.py
- Both: Evidence required, session logs maintained

---

## Templates and Their Locations

### In Project Knowledge
These templates are referenced by roles during work:
- `gameplan-template.md` - Chief Architect uses when creating gameplans
- `agent-prompt-template.md` - Lead Developer uses when creating prompts
- `github-guide.md` - Agents reference for GitHub operations
- `stop-conditions.md` - All roles reference for STOP triggers
- `cross-validation-protocol.md` - Lead Dev uses for validation

### In PM's Personal Tools
These are prompt templates PM uses to start sessions:
- Chief Architect session starter
- Lead Developer session starter
(These stay with PM as personal templates, not in project files)

---

## Cascade Verification Checklist

### Before Chief Architect Creates Gameplan
- [ ] Referenced gameplan-template.md?
- [ ] Included Phase 0 GitHub setup?
- [ ] Specified Code vs Cursor differences?
- [ ] Added STOP conditions?

### Before Lead Developer Deploys Agents
- [ ] Created prompts in artifacts?
- [ ] Used agent-prompt-template.md?
- [ ] Added cross-validation requirements?
- [ ] Included evidence standards?

### Before Agents Execute
- [ ] Code read CLAUDE.md?
- [ ] Cursor received constraints?
- [ ] Both have session logs?
- [ ] GitHub issue verified?

---

## Time Targets

**Old Process**: ~1 hour manual context creation
**New Process**: 15 minutes systematic cascade
- PM → Chief Architect: 5 min
- Chief Architect → Lead Developer: 5 min
- Lead Developer → Agents: 5 min

---

## Critical Success Factors

1. **Templates contain requirements** - Not just reference them
2. **Each layer verifies receipt** - Acknowledge methodology transfer
3. **Evidence at each step** - No assumptions about understanding
4. **Consistent terminology** - Same words mean same things

---

## Remember

The cascade only works if we're systematic at EVERY layer. One broken link and methodology gets lost, requiring manual recovery.
