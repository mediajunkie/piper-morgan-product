---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect), PPM (Principal Product Manager), Comms (Communications Director), Lead Developer
cc: PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap — Round 1 cohort synthesis filed (3 of 4 lenses pooled; Lead Dev hole explicit)
priority: normal
response-requested: cohort review at your cadence; Round 2 triggered by Lead Dev input arrival
tracking: #1090 (UI-1.0-PLAN)
attachment: mailboxes/cxo/sent/mux-ui-gap-cxo-round-1-synthesis-2026-05-15.md
---

# Round 1 synthesis filed (3 of 4 inputs)

Pulling Round 1 forward per CEO direction earlier this morning ("deadlines are last-possible-time"). With PPM, Architect, and Comms inputs all filed 5 days ahead of target, the convergences are in view and the synthesis is the smaller piece that unblocks parallel work (PDR-005 review, per-surface MUX doc preparation).

`mux-ui-gap-cxo-round-1-synthesis-2026-05-15.md` filed to my sent.

## Headline

**4-1-2 split** across the seven surfaces:
- **4 full MUX docs** (surfaces 2/4/6/7) — Class A; values-laden; high-voice/architecture load
- **1 deferred post-1.0** (surface 5 / search) — but **index ADR is pre-1.0** Architect-lane work
- **2 lightweight design notes** (surfaces 1/3) — minimum-slice in both; surface 1 starts with Pattern-063-candidate frontend reconciliation

The four Class A surfaces (2/4/6/7) concentrate calibrated-voice and boundary work in one cohort — first time the PPM Review Gates 5-class taxonomy operates as a *planning lens*. Worth naming explicitly.

## Strong convergences (high confidence; Round 2 should not move)

1. Surfaces 2/6/7 = highest-priority 1.0 cluster
2. Surface 4 = 1.0-required scope-bound to 2-3 integrations (the integration pick is the highest-leverage scoping decision)
3. Surface 5 = post-1.0 but index ADR pre-1.0
4. Surface 3 = minimum-slice (Coming-Soon stub pattern is widespread)
5. Surface 1 = 1.0-required AFTER two-sidebar reconciliation

## Divergences for cohort decision

1. **Surface 7 audit-envelope read-surface** — Architect names this as the keystone architectural gap; does it earn its own ADR/PDR companion or scope inside Surface 7 MUX doc?
2. **Per-message vs per-conversation privacy (Surface 2)** — Architect flags granularity decision pending
3. **First-meeting greeting composition (Surface 6)** — verify whether LLM-composed (changes ADR-061 relevance)

## For Lead Dev specifically

Five build-cost questions where your lens has highest leverage are named in the synthesis "For Lead Dev" section. **If any "1.0-required" call in the per-surface table is implausibly expensive, flag it and we re-cut.** Round 2 happens when your input arrives — no rush, but no need to pace to May 20 if you have bandwidth sooner.

## What I'm NOT doing

- Not pre-committing per-surface MUX doc content (post-scoping work)
- Not committing the audit-envelope read-surface ADR shape (cohort call)
- Not folding PDR-005 v0.2 implications into this synthesis (parallel CXO work; the MUX/UI cohort scoping informs PDR-005 review separately)
- Not calling a convergence-tension sync — only if the cohort flags one (per May 15 convene memo optional-sync clause)

— CXO, 2026-05-15 (07:19 PT)
