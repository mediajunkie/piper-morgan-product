---
type: protocol
title: Agent Protocols
valid_from: "2026-01-24"
last_verified: "2026-06-19"
---

# Agent Protocols

Detailed protocols for Claude Code agents. These are loaded on-demand via progressive disclosure - referenced from CLAUDE.md but only read when needed.

## Available Protocols

| Protocol | When to Load |
|----------|--------------|
| [debugging-protocol.md](debugging-protocol.md) | When debugging any technical issue |
| [e2e-investigation-protocol.md](e2e-investigation-protocol.md) | When assigned Phase 2 bug investigation |
| [issue-closure-protocol.md](issue-closure-protocol.md) | When closing any GitHub issue |
| [git-workflow.md](git-workflow.md) | For git operations and branch management |
| [completion-discipline.md](completion-discipline.md) | Reference for Patterns 045, 046, 047 |

## Design Principle

These protocols were extracted from CLAUDE.md on 2026-01-22 to reduce instruction count and improve model performance. Research shows LLMs follow ~150-200 instructions reliably; keeping CLAUDE.md concise ensures critical rules get attention.

**Trade-off**: Protocols must be explicitly loaded when relevant. Monitor for adherence fall-off.

## Related Resources

- **Skills**: `.claude/skills/` - Formalized procedures with triggers
- **Briefings**: `docs/briefing/` - Context loading (PROJECT.md, BRIEFING-CURRENT-STATE.md)
- **Patterns**: `docs/internal/architecture/current/patterns/` - Architectural patterns
