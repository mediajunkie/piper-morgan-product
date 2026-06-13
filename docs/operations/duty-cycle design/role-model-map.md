---
title: Role → Model Map (Opus / Sonnet / Haiku per duty-cycle role)
status: RATIFIED
valid_from: "2026-06-13"
last_verified: "2026-06-13"
owner: CIO
---

# Role → Model Map

**STATUS: RATIFIED** — the canonical per-role model map. **Recovered from old-CIO's session transcript 2026-06-13**: the original decision was made during the move-back planning (the 6/9 token-efficiency conversation) but never committed to a durable file — a session-logging lapse (only PA=Sonnet survived in the records; PM found the full map in the transcript). The plan-of-record's "per PM's role-model map" points here. (Lesson: `feedback_write_down_even_if_not_ratified`. Capability: predecessor transcripts are searchable via `search_session_transcripts` — approval-gated.)

## The framework
Model choice is a **token-efficiency lever** (PM-ULTRA-HIGH). Use the **cheapest model adequate** for a role's *core daily work*; reserve Opus for genuinely reasoning-dense work. **Escape valve**: a role bursts up a tier (Sonnet→Opus, directly or via subagent) for an occasional hard task — so a cheaper default is low-risk. Three tiers: **Opus 4.8** (deep reasoning), **Sonnet 4.6** (drafting / synthesis / cadence — handles long-form writing + summarization very well), **Haiku 4.5** (mail-triage / inbox-empty heartbeats).

## The map

| Role | Model | Rationale |
|---|---|---|
| **Architect** | **Opus 4.8** | Deep architectural reasoning, ADRs, mechanism design |
| **CIO** | **Opus 4.8** | Methodology corpus, catalog work, multi-file synthesis, verify-first discipline |
| **Exec** | **Opus 4.8** | Workstream synthesis, attention rollups, cross-cutting reasoning |
| **Lead Dev** | **Sonnet 4.6** default; **Opus 4.8** for hardest coding/refactors | Most routine PR work, hook updates, debugging fits Sonnet's profile (per skill guidance); burst to Opus when needed |
| **CXO** | **Sonnet 4.6** | UX writing + design lens; Sonnet handles long-form writing very well |
| **PPM** | **Sonnet 4.6** | Roadmap drafting, structured synthesis |
| **Comms** | **Sonnet 4.6** | Drafting + voice work is squarely Sonnet's sweet spot |
| **Docs** | **Sonnet 4.6** | Omnibus, audits, doc-sync — all summarization-shaped |
| **HOST** | **Sonnet 4.6** | Trust/welfare lens, relationship reasoning |
| **PA** | **Sonnet 4.6** or **Haiku 4.5** | Mostly mail-watching + relay; Haiku may suffice |
| **Web** | **Sonnet 4.6** | Frontend work, two-repo composition; burst to Opus for complex builds |
| **Comms / PA mail-only fires** | **Haiku 4.5** | Mail triage + inbox-empty heartbeats don't need Opus or Sonnet |

## Current-state reconciliation (2026-06-13)
Migrated so far: PA (Sonnet ✓), Exec (Opus ✓), CIO (Opus ✓), **Lead Dev (Opus 4.8 — map says Sonnet-default)**.
- **LD is the one conflict.** LD migrated to Opus 4.8 on 6/12 — a direct artifact of *this map being lost* (it wasn't written down at LD-migration time). The map says **Sonnet-default, Opus only for the hardest coding/refactors**. → **PM call**: flip LD to Sonnet-default, or keep LD on Opus (override the map for LD)?
- **Queued roles migrate per the map** (no conflict — not yet migrated): **Architect → Opus**; **HOST, CXO, PPM, Comms, Docs, Web → Sonnet**. (So: migrate **HOST on Sonnet** ✓.)

## Maintenance
- When a role migrates, set its model per this map; record any PM override here with its reason.
- Mail-only fires (lightest heartbeats) → Haiku.
- Re-tier signal: a role bursting up a tier *too frequently* → revisit its tier (its core work is heavier than assumed).
- Bump `last_verified` whenever this map is re-confirmed current.
