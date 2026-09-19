# Recommendation Memo: Claude Hooks for Piper Morgan

**From**: Special Assignments Agent
**To**: Chief Innovation Officer
**Date**: February 16, 2026
**Re**: Evaluation of Claude Hooks adoption

---

## Executive Summary

**Recommendation: ADOPT (Incremental)**. Claude Hooks are a natural fit for Piper Morgan's architecture and would solve real problems we already experience — particularly post-compaction context loss, missed mailbox checks, and stale briefing documents going undetected. We already have a minimal SessionStart hook deployed. The recommendation is to expand it incrementally, starting with the highest-value automation (session log continuity and mailbox checks) rather than attempting a comprehensive Dex-style overhaul.

---

## Capability Overview

Claude Hooks are deterministic shell commands or LLM prompts that fire automatically at defined lifecycle events in Claude Code. Unlike CLAUDE.md instructions (which Claude *may* read), hooks *always* execute.

**14 lifecycle events** are available: SessionStart, PreToolUse, PostToolUse, Stop, PreCompact, SessionEnd, and others. Three hook types exist: **command** (shell scripts), **prompt** (single-turn LLM evaluation), and **agent** (multi-turn subagent with tool access).

Key constraints:
- **Claude Code only** — CLI, Desktop, and VS Code extension. Does not fire in Cursor.
- Hooks execute with full user permissions (security consideration)
- Command hooks timeout at 10 minutes; prompt/agent hooks at 30-60 seconds
- Multiple matching hooks run in parallel; exit code 2 blocks the triggering action
- Configuration lives in `.claude/settings.json` (project-level, committable) or `~/.claude/settings.json` (user-level)

---

## Applicability to Piper Morgan

### Problems Hooks Would Solve

**1. Post-Compaction Context Loss (High Impact)**
Our most frequent failure mode: after context compaction, agents create new session logs instead of resuming existing ones. A SessionStart hook matching `compact|resume` could verify an existing log exists and inject its path — or halt the session with a warning. This is currently a manual protocol step that agents sometimes skip.

**2. Mailbox Goes Unchecked (Medium Impact)**
The `check-mailbox` skill exists but requires manual invocation. Agents regularly begin work without reading their inbox. A SessionStart hook could list unread messages and inject them as context, guaranteeing inter-agent communications are seen.

**3. Stale Briefings Undetected (Medium Impact)**
BRIEFING-CURRENT-STATE.md was last updated Feb 11. No mechanism alerts agents to staleness. A SessionStart hook could check file modification dates and warn when briefings exceed a freshness threshold.

**4. Role Identity Drift (Low-Medium Impact)**
After compaction, agents sometimes lose their assigned role identity. A SessionStart hook injecting role context deterministically would reinforce identity stability.

### What Hooks Would NOT Solve

- **Cursor-based agents**: Our multi-agent workflow sometimes uses Cursor, where hooks don't fire. Any hook-dependent behavior needs a fallback path.
- **Complex coordination**: Hooks are stateless between executions. Multi-agent coordination (Pattern-029, Pattern-059) requires richer orchestration than hooks alone provide.
- **Skill automation**: Hooks cannot trigger skills directly. They can inject reminders but can't replace the skill invocation itself.

---

## Recommendation: Adopt (Incremental, 3 Phases)

### Phase 1: Enhance Existing SessionStart Hook (1-2 hours)
Replace the current echo-only hook with a script that:
- Detects post-compaction resume and finds today's existing session log
- Checks the agent's mailbox and surfaces unread message count
- Validates BRIEFING-CURRENT-STATE.md freshness (warn if >7 days)
- Injects role identity context

This addresses our three highest-impact problems with minimal infrastructure change. The hook script lives at `.claude/hooks/session-start.sh` and the configuration stays in `.claude/settings.json` (already committed).

### Phase 2: Add Safety Guardrails (1 hour, after Phase 1 validated)
- **PreToolUse hook** on `Bash`: Block `rm -rf` on session log directories (we already deny this in permissions, but defense-in-depth)
- **Stop hook**: Warn if session log wasn't updated during the session
- **PreCompact hook**: Snapshot key context (role, current task, log path) to a recovery file

### Phase 3: Evaluate Prompt/Agent Hooks (Deferred)
- **Stop agent hook**: Verify acceptance criteria met before allowing session end
- **PostToolUse prompt hook**: Lightweight code style checks
- Only pursue after Phase 1-2 prove stable; these add latency and cost per invocation

### What We Should NOT Do
- **Do not replicate Dex's architecture**. Dex is a personal productivity OS with MCP servers for calendar, career tracking, and deal management. Piper Morgan is a product development system with different concerns. Cherry-pick the hooks pattern; ignore the lifestyle features.
- **Do not make hooks the sole context loading mechanism**. CLAUDE.md progressive loading is working well for detailed protocols. Hooks should handle the critical-path items that agents currently skip, not replace the entire briefing system.

---

## Cost-Benefit Summary

| | Effort | Benefit |
|---|---|---|
| Phase 1 | ~2 hours | Eliminates post-compaction failures, guarantees mailbox reads |
| Phase 2 | ~1 hour | Prevents accidental log deletion, ensures session documentation |
| Phase 3 | TBD | Quality gates at session boundaries (evaluate after Phase 1-2) |
| Maintenance | Low | Hook scripts are simple bash; update when protocols change |

**Risk**: Hooks that output to stdout inject into Claude's context. Verbose hooks waste tokens. Keep output concise.

---

## Verification

- [x] Research completed across all four question areas
- [x] Recommendation memo drafted
- [x] Decision clearly stated with supporting rationale (Adopt, Incremental)
- [x] Memo delivered to CIO mailbox
