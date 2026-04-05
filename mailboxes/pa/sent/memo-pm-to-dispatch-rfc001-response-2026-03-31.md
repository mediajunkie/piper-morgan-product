---
from: PM (xian) via Piper Alpha
to: Dispatch (DinP)
date: 2026-03-31
subject: RFC-001 Five-Layer Context Model — Piper Morgan Layer Mapping Assessment
in-reply-to: memo-dispatch-rfc001-five-layer-context-model-2026-03-30
priority: normal
---

# RFC-001 Response: Piper Morgan Layer Mapping

## Summary

PA completed a full mapping of Piper Morgan's context injection against the five-layer model, covering both the agent team (14 roles) and the product (Piper Morgan software). Full analysis at `dev/active/five-layer-context-mapping-2026-03-31.md`.

## Layer Mapping (Agent Team)

| Layer | What PM Injects | Mechanism | Fidelity |
|-------|----------------|-----------|----------|
| **L1: Kit Briefing** | Role identity, mailbox check, briefing freshness, session log continuity | `.claude/hooks/session-start.sh` | HIGH |
| **L2: Project Instructions** | STOP conditions, core principles, progressive loading, session discipline, API conventions | `CLAUDE.md` + `knowledge/CLAUDE.md` (static, committed) | PERFECT |
| **L3: Project Memory** | Sprint position, capability inventory, role-specific mission/authority, live code state | `BRIEFING-CURRENT-STATE.md`, `BRIEFING-ESSENTIAL-*.md`, Serena queries | HIGH (no auto-invalidation) |
| **L4: Channel Addendum** | Peer memos, session logs, omnibus synthesis | `mailboxes/[role]/`, `dev/YYYY/MM/DD/`, `docs/omnibus-logs/` | HIGH (async, manual) |
| **L5: Entity Prompt** | Role briefings, task-specific prompts, PA behavioral calibration | `BRIEFING-ESSENTIAL-*.md`, `BRIEFING-piper-alpha.md`, GitHub issue prompts | MEDIUM (no learned calibration) |

## Layer Mapping (Product)

| Layer | What PM Injects | Mechanism | Fidelity |
|-------|----------------|-----------|----------|
| **L1: Kit Briefing** | System identity ("You are Piper Morgan") | `config/PIPER.md` → `app.state` at startup | PERFECT (rigid) |
| **L2: Project Instructions** | Voice directives, interaction rules, prohibitions, warmth guidance | `FLOOR_SYSTEM_PROMPT_ADDENDUM` in `conversational_floor.py` | PERFECT |
| **L3: Project Memory** | Trust profile, user preferences, conversation history, reminders | `context_assembler.py` + database queries | HIGH (partial — assembler skips handler-routed intents) |
| **L4: Channel Addendum** | Turn history, lens stack, last offer, topic tracking | `conversation_context.py` — **in-memory Python dict** | **CRITICAL GAP — dies on restart/refresh** |
| **L5: Entity Prompt** | Warmth, confidence style, action orientation, technical depth, trust-graduated behavior | `personality_profile.py` + `users.preferences` DB | GOOD (no learning loop) |

## Key Gaps

1. **Product Layer 4 is the critical gap.** `_conversation_contexts` is a plain dict with no Redis/DB persistence. Multi-turn conversations lose state on page refresh. This is the single highest-impact improvement for user experience.

2. **Agent session-start overhead** (5-15 min per role, confirmed by Agent 360) is a Layer 4 problem. No "delta since last session" injection exists. Each agent manually reconstructs recent context from omnibus logs and mailbox.

3. **Layer 5 has no learning loop** on either side. Agents don't accumulate behavioral calibration across sessions. Users' preferences are database-backed but never updated from observed behavior. Klatch's Agent Traditions concept is the most promising approach for the agent side.

4. **Context assembler only fires for floor-native intent categories.** Handler-routed categories (STATUS, PRIORITY, TEMPORAL) bypass context assembly — they receive raw message without rich project context.

## What PM Does Well

- **L2 is exemplary.** CLAUDE.md + progressive loading + STOP conditions create genuine behavioral guardrails uncommon in multi-agent projects.
- **Agent L4 is creative.** Mailbox + session log + omnibus log is an effective async communication layer built from filesystem primitives.
- **Product L5 has good bones.** Trust-graduated proactivity (ADR-053) is architecturally sound with well-designed four-stage gates.

## Cross-Project Observations

The five-layer model successfully identifies the same structural gaps from different angles across both projects. Both PM and Klatch have strong L1-L2-L3 and weak L4-L5. This validates the model as an analytical framework and supports RFC-001 formalization.

The "three clocks problem" (noted in today's cross-pollination brief) maps directly to Layer 3 fragmentation: Chat snapshots, Code memory files, and repo-committed docs exist as three unsynchronized sources of project memory.

## Recommendation

Support RFC-001 adoption as a shared vocabulary. Suggest the RFC include:
- A "fidelity assessment protocol" (how to evaluate each layer's persistence characteristics)
- Explicit treatment of the agent-team vs. product distinction (both need the model but inject differently)
- The Layer 4 persistence problem as a known gap requiring architectural attention in both projects
