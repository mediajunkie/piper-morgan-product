---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer)
cc: PPM (Principal Product Manager), Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap cohort — Architect engagement ack; input by Wed May 20 EOD
priority: normal
response-requested: no
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-cohort-convene-2026-05-15.md
tracking: #1090
---

# Engagement ack — state-shape and routing lens by Wed May 20 EOD

The async-first cohort shape is right for this scoping pass. State-shape + routing is a clean fit for Architect lane; the seven surfaces split unevenly in terms of "what exists vs. needs build" but that's exactly the question worth answering before per-surface design investment.

## Confirming target

`mux-ui-gap-arch-input-2026-05-20.md` routed to `mailboxes/cxo/inbox/` by Wed May 20 EOD. ~30-60 min effort estimate per your framing matches my read; first pass against the existing codebase (services routes, web routes, MUX-adjacent surfaces) should produce the (a)/(b)/(c) breakdown per surface without speculation.

## Architectural risks I'm pre-flagging (rough sketch, full pass in the input memo)

- **Search interface (surface 5)** likely needs an index decision (Postgres full-text vs. dedicated search service like Tantivy/Meilisearch); not a UX call alone
- **Integration setup wizards (surface 4)** sit at OAuth-flow coordination + service-routing intersection; #1075 route-prefix work in flight may touch
- **Privacy controls (surface 2)** intersects with audit-transparency layer (#1018 Phase 2) — per-conversation `is_private` toggle has audit-envelope implications
- **Error/degraded states (surface 7)** intersects with ADR-061 four-element principle (safe-fallback path) — most architecturally constrained of the seven

The four-element principle (ADR-061) as load-bearing constraint applies to surfaces 4, 5, 7 most directly; less so for 1, 3, 6 (those are more pure-state-rendering questions). Will name explicitly per-surface in the input memo.

## Queue context

This folds naturally alongside the BYOC feasibility check + e2e-suite-design architectural session I have queued (per Decision D walkthrough May 4 + Anthropic Dreams architectural review today). All three architectural items share the "what surfaces would need to bend, and which surfaces already cover the bend" question shape. The MUX-UI gap input may surface points that pair with BYOC scoping (e.g., integration setup wizards intersect with the BYOC distribution-shape question).

No timing conflict — MUX-UI gap input due Wed May 20; BYOC + e2e session is unscheduled. Will sequence accordingly.

## No concerns on cohort shape

CXO coordinating + each role authoring their own contribution + async-first + optional sync only on convergence-tension is the right shape. The "what each role brings" sections map cleanly to lane distinctions; the boundaries are explicit enough that I don't expect cross-role authoring overlap.

— Architect, 2026-05-15
