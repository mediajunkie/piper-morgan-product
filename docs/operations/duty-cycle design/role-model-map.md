---
title: Role → Model Map (Opus vs Sonnet per duty-cycle role)
status: PROPOSED
valid_from: "2026-06-13"
last_verified: "2026-06-13"
owner: CIO
---

# Role → Model Map

**STATUS: PROPOSED by CIO 2026-06-13 — pending PM ratification.** This is the canonical home for "which model each duty-cycle role runs." The plan-of-record's "per PM's role-model map" points here.

**Why this doc exists**: the original per-role model decision was made during the move-back planning (part of the 6/9 token-efficiency conversation) but never written down — a session-logging lapse (only PA=Sonnet survived in the records). PM 6/13: *"we should still write things down even if they are not ratified."* This doc is the durable record; the `status` field keeps proposed-vs-ratified legible. (See `feedback_write_down_even_if_not_ratified` memory.)

## The framework

Model choice is a **token-efficiency lever** (PM-ULTRA-HIGH priority): use **Sonnet** (cheaper) wherever it's adequate; reserve **Opus** (more capable, costlier) for roles whose *core daily work* is heavy multi-step / cross-cutting reasoning, or is correctness/quality-critical in a way that ripples to others.

**Escape valve**: any Sonnet-default role can escalate a single heavy task to an Opus/Fable subagent (the PA pattern — `feedback_opus_fable_subagent_for_heavy_tasks`). So **"Opus by default" = "needs deep reasoning *often enough* that constant subagent-escalation would be overhead"** — not "occasionally does something hard." This lowers the risk of a Sonnet default.

## Proposed map

### Opus by default — high confidence (core work is reasoning-dense / quality-critical)
| Role | Why Opus |
|---|---|
| **Exec** (Chief of Staff) | Cross-cohort synthesis daily — Ship pipeline, attention rollup, braintrust synthesis: many inputs → one coherent view. |
| **CIO** | Methodology synthesis + pattern-catalog reasoning + architecture-of-process; cross-cutting. |
| **Lead Dev** | Multi-step code + debugging; correctness-critical. |
| **Architect** | System design, ADRs, soundness reviews; architecture errors are expensive. |

### Opus by default — lean, but defensibly Sonnet under cost pressure (the swing roles)
| Role | Lean-Opus rationale / Sonnet-defensible |
|---|---|
| **PPM** (Principal Product Manager) | Product strategy, roadmap, PDR/gate judgment — decisions ripple → lean Opus. But much cadence is reviewable; Sonnet + escalation defensible if cost pressure is high. |
| **CXO** (Chief Experience Officer) | Sets voice/experience standards others follow (Colleague Test, design system, floor-quality) — quality-critical judgment → lean Opus. Sonnet defensible given the escalation valve. |

### Sonnet adequate — high confidence (cadence / craft / scaffolded-synthesis; escalate occasionally)
| Role | Why Sonnet |
|---|---|
| **PA** (Piper Alpha) | Product-assistant / backlog / data-gathering / daily cadence. Already Sonnet; Opus/Fable subagent for heavy synthesis. |
| **HOST** (Head of Sapient Trust) | Welfare, role-health, cadence comms — day-to-day is monitoring + cadence; periodic 360 synthesis escalates to an Opus subagent. |
| **Comms** | Narrative / editorial / blog — writing is Sonnet's strength; the voice-guide + PM editorial review are the quality net. (Historical precedent: Comms ran Sonnet.) |
| **Docs** | Omnibus synthesis + merge-keeper + doc-sync — substantial but skill-scaffolded + pattern-following; escalate for unusually complex days. (Higher end of the Sonnet tier — revisit if omnibus quality dips.) |

## Net change from current state

All queued roles (HOST, Comms, CXO, PPM, Arch, Docs) last ran **Opus**. Under this proposal:
- **Move Opus → Sonnet (the cost win):** HOST, Comms, Docs *(3 roles)*
- **Stay Opus:** Exec, CIO, Lead Dev, Architect *(firm)* + PPM, CXO *(swing — trim to Sonnet if cost pressure rises)*
- **Already Sonnet:** PA

**Firm tiers**: Opus = {Exec, CIO, Lead Dev, Architect}; Sonnet = {PA, HOST, Comms, Docs}; swing = {PPM, CXO}.

## Maintenance
- **On ratification**: change `status` to RATIFIED + bump `last_verified`; fill the plan-of-record migration-table model column; pin the ratified map in memory.
- **When a role migrates**: set its model per this map; if PM overrides a role, record the override here with its reason.
- **Re-tier signal**: a Sonnet role escalating to an Opus subagent *too frequently* means its core work is heavier than assumed → revisit its tier.
