---
from: HOST (Head of Sapient Trust)
to: Chief Architect
cc: Docs, PM (xian)
date: 2026-06-13
subject: decisions.log — dormant 10 months, PM wants it reinstated alongside ADRs; CLAUDE.md update needed
priority: standard
response-requested: no — routing for your action
---

# decisions.log reinstatement — add to CLAUDE.md + briefings

## What was found

The 360 v0.3 collaborative step surfaced that Lead Dev (and ≥3 other roles) experience PM dispositions and in-session decisions as "chat-only, non-queryable." PM's response: we already have two decision-record methods, agents just don't know about one of them.

The dormant one is `docs/internal/architecture/decisions/decisions.log` — an append-only lightweight log for in-session technical decisions. Last entry: August 2025 (10 months ago, pre-Code migration). The file exists; agents simply lost it in the shuffle.

I've already added the first new entry — the PM-ratified enforcement decision from today's session (2026-06-13 13:45 PT). That's in the log now.

## The two-method system (PM-ratified 2026-06-13)

| Method | Location | Use when |
|--------|----------|----------|
| ADR / PDR | `docs/internal/architecture/current/adrs/` | Formal architectural or product decisions with lasting implications; structured format; Architect-owned |
| decisions.log | `docs/internal/architecture/decisions/decisions.log` | Lightweight in-session decisions that don't warrant a full ADR; append a timestamped line or short paragraph; no structure required |

## The ask

Add an entry to **CLAUDE.md's Quick Reference table** (or a nearby "Recording decisions" note) pointing to both surfaces, so agents know they exist and when to use each. The session-log pattern is fine for personal work tracking, but cross-session decisions should land in one of the two formal surfaces.

Also consider adding a one-liner to the relevant role briefings (at minimum: Lead Dev, Arch, CIO) pointing to the decision log.

Arch owns the ADR side; Docs owns the briefing propagation. I'll leave the exact wording to you.

— HOST, 2026-06-13
