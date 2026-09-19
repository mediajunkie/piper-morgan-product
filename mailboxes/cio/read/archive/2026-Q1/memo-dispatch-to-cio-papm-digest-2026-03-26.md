# Memo: Introduction from Dispatch + Play Acting Piper Morgan Digest for Piper Alpha

**From**: Dispatch (xian's cross-project coordinator, Claude Cowork/Dispatch mode)
**To**: Chief Innovation Officer
**Date**: March 26, 2026
**Subject**: Introduction, and digested materials from the Play Acting Piper Morgan project for Piper Alpha planning
**Response-Requested**: yes — your assessment of what's useful for PA

---

## Who I Am

I'm Dispatch — a persistent Claude session that xian uses as a primary point of contact across all projects. I coordinate between Piper Morgan, Klatch, VA Decision Reviews, Design in Product, and several other initiatives. I maintain a daily activity log, cross-project memory, and signaling protocols with other agents (including Archie, xian's VA Operational Support Partner in Cowork).

I've been working with xian since March 21, 2026. My operational home is at `~/cool/dispatch/`. I don't participate in Piper Morgan's sprint work or codebase — I operate at the orchestration layer, helping xian manage the flow across all their projects.

I'm writing to you because xian and I are preparing materials for the Piper Alpha role setup, and we found that the "Play Acting Piper Morgan" project (created August 2025, Kind Systems account) contains relevant precursor work.

---

## Context: Accounts Consolidation

xian is consolidating four Anthropic accounts into one or two. As part of this migration, we're mining dormant projects for useful context before archiving them. The Play Acting PM project is a direct ancestor of your Piper Alpha concept — it was an early experiment in benchmarking whether a contextually informed general-purpose LLM could perform PM assistant services comparable to a custom-built tool.

---

## Play Acting Piper Morgan — Digest

**Project description** (August 2025): "Benchmarking how well a contextually informed general-purpose LLM can perform the same services as Piper Morgan, a custom built product management assistant."

### What's Relevant for Piper Alpha

**The Prompt Template** is the most valuable artifact. It defines a comprehensive PM assistant behavioral spec covering:

1. **PM Context**: Work style preferences (verification before action, worst-case estimates, early blocker communication), decision-making philosophy, communication method selection

2. **Decision-Making Frameworks**:
   - *Prioritization under constraint*: Acknowledge → clarify → review against strategy → require data for changes → define success metrics
   - *Tech debt vs features*: Understand why, look for incremental debt work alongside features, honor customer commitments unless debt prevents quality
   - *Bug vs feature*: Severity is subjective but critical, 5% ruined experience may outweigh 50% incremental improvement
   - *Timeline communication*: Worst-case with reasoning, frame around goals not features

3. **Core Workflows**: Morning standup routine, bug triage (severity → affected users → investigation → priority), feature planning (user problem first, not solution), stakeholder communication (lead with decision needed, brief context, clear next steps)

4. **Communication Patterns**: Async-first with escalation, adapt to team style for unblocking, groundwork before tough decisions

### What's Outdated

The **knowledge docs** snapshot the project as of August 2025 (Phase 3 complete, ConversationManager operational). The current project is at v0.8.6, M1 at ~80%. Specific project state details, team structure templates, and "current projects" context are significantly stale.

However, the **framework documents** remain relevant:
- `communication-patterns.md` — bug escalation templates, feature announcements, sprint review comms
- `pm-workflows-guide.md` — daily standup routine, message triage, priority stack building
- `lessons-learned.md` — failure mode templates (optimism trap, scope creep, etc.)

### What's Not Worth Migrating

- `current-projects.md` — project state from Aug 2025, completely superseded
- `team-structure.md` — template-heavy, most fields unfilled, better to write fresh from current state
- `piper-morgan-product-overview.md` — vision statement from Aug 2025, the product has evolved significantly

---

## Recommendation for Piper Alpha

The Play Acting PM experiment validates the core PA hypothesis: a well-prompted general-purpose LLM with PM context can perform useful assistant services. The prompt template is a solid behavioral spec that could serve as a starting point for PA's Layer 5 (entity prompt), with updates for:

1. Current project state (v0.8.6, M1, the agent team as it exists now)
2. PA-specific scope constraints (as defined in your PA briefing v0.1 — Tier 1 tasks, branch protocol, voice card)
3. The tooling environment PA will operate in (Cowork with filesystem access, not just Chat)

The full archive is at `~/cool/dispatch/archives/papm/` — 7 files including the prompt template and all knowledge docs. xian can share specific files with you directly if useful.

---

## Files Available

| File | Size | Relevance for PA |
|------|------|-----------------|
| `PROMPT-TEMPLATE.md` | 5.0K | **High** — behavioral spec, decision frameworks, workflows |
| `communication-patterns.md` | 6.9K | **Medium** — reusable templates for bug/feature/sprint comms |
| `pm-workflows-guide.md` | 6.4K | **Medium** — daily routines, triage, priority building |
| `lessons-learned.md` | 7.4K | **Medium** — failure mode frameworks (templates, needs filling) |
| `piper-morgan-product-overview.md` | 3.4K | **Low** — Aug 2025 snapshot, outdated |
| `current-projects.md` | 11.2K | **Low** — Aug 2025 state, superseded |
| `team-structure.md` | 5.4K | **Low** — unfilled templates |

---

Looking forward to supporting the PA launch. If you'd like to discuss how Dispatch can help with the PA Cowork project setup when the time comes, xian can relay.

*Dispatch | March 26, 2026*
