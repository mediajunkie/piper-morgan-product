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
Model choice is a **token-efficiency lever** (PM-ULTRA-HIGH). Use the **cheapest model adequate** for a role's *core daily work*; reserve Opus for genuinely reasoning-dense work. **Escape valve**: a role bursts up a tier (Sonnet→Opus, directly or via subagent) for an occasional hard task — so a cheaper default is low-risk. Three tiers: **Opus** (deep reasoning), **Sonnet** (drafting / synthesis / cadence — handles long-form writing + summarization very well), **Haiku** (mail-triage / inbox-empty heartbeats). **Versions track the current release** — as of 2026-06-13: **Opus 4.8, Sonnet 4.8, Haiku 4.5** (HOST migrated 6/13 on Sonnet 4.8). This map fixes the **tier** per role; any "4.6" in the table below = the then-current Sonnet, now 4.8. (Versioning-as-staleness is exactly what #972 temporal-validity addresses.)

## The map

| Role | Model | Rationale |
|---|---|---|
| **Architect** | **Opus 4.8** | Deep architectural reasoning, ADRs, mechanism design |
| **CIO** | **Opus 4.8** | Methodology corpus, catalog work, multi-file synthesis, verify-first discipline |
| **Exec** | **Opus 4.8** | Workstream synthesis, attention rollups, cross-cutting reasoning |
| **Lead Dev** | **Opus 4.8** — *PM override 6/13* (map's original was Sonnet-default/Opus-burst) | **PM 6/13: keep on Opus** given the architecturally-complex work LD orchestrates. The map's Sonnet-default (routine PR/hooks/debugging fits Sonnet) is on hold; **reconsider over time** as LD's load shifts. |
| **CXO** | **Sonnet 4.6** | UX writing + design lens; Sonnet handles long-form writing very well |
| **PPM** | **Sonnet 4.6** | Roadmap drafting, structured synthesis |
| **Comms** | **Sonnet 4.6** | Drafting + voice work is squarely Sonnet's sweet spot |
| **Docs** | **Sonnet 4.6** | Omnibus, audits, doc-sync — all summarization-shaped |
| **HOST** | **Sonnet 4.6** | Trust/welfare lens, relationship reasoning |
| **PA** | **Sonnet 4.6** — *PM 6/13: not Haiku* | **PM 6/13: keep on Sonnet.** Beyond PM-assistant, PA is being promoted to a **"product associate"** role (PMing the skunkworks for PM) — that substantive product work wants Sonnet, not Haiku. |
| **Web** | **Sonnet 4.6** | Frontend work, two-repo composition; burst to Opus for complex builds |
| **Comms / PA mail-only fires** | **Haiku 4.5** | Mail triage + inbox-empty heartbeats don't need Opus or Sonnet |

## Current-state reconciliation (updated 2026-06-13)
Migrated: PA (Sonnet ✓), Exec (Opus ✓), CIO (Opus ✓), Lead Dev (Opus ✓ — see below).
- **LD — RESOLVED 6/13 (PM): keep on Opus.** The map's original was Sonnet-default; PM overrode to keep LD on Opus given the architecturally-complex work it orchestrates. Noted as an override (not a map change); **reconsider over time.**
- **PA — confirmed Sonnet** (PM 6/13: not Haiku; product-associate elevation).
- **Queued roles migrate per the map**: **Architect → Opus**; **HOST, CXO, PPM, Comms, Docs, Web → Sonnet**. **HOST migrating now → Sonnet ✓** (PM 6/13).
- No open conflicts remain.

## Maintenance
- When a role migrates, set its model per this map; record any PM override here with its reason.
- Mail-only fires (lightest heartbeats) → Haiku.
- Re-tier signal: a role bursting up a tier *too frequently* → revisit its tier (its core work is heavier than assumed).
- Bump `last_verified` whenever this map is re-confirmed current.
