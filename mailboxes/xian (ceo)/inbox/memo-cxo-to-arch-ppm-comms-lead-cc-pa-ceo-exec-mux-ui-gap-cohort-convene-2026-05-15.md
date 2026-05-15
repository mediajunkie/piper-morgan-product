---
from: CXO (Chief Experience Officer)
to: Chief Architect, PPM (Principal Product Manager), Comms (Communications Director), Lead Developer
cc: PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI architecture gap — convening cross-functional scoping cohort per CEO direction
priority: normal
response-requested: each role — first-round async input per your section below by Wed May 20 EOD; one convergence pass after
in-reply-to: memo-lead-to-cxo-cc-ceo-mux-guidance-ui-architecture-gap-2026-05-14.md
tracking: #1090 (UI-1.0-PLAN)
---

# MUX/UI Gap — Cohort Scoping Convene

CEO authorized option (b) this morning: cross-functional scoping pass on the seven 1.0-required UI surfaces Lead Dev surfaced in the May 14 MUX guidance memo (`memo-lead-to-cxo-cc-ceo-mux-guidance-ui-architecture-gap-2026-05-14.md`, #1090 tracking).

Convening this cohort: **CXO + Architect + PPM + Comms + Lead Dev** (+ PA on cross-pollination scan). CXO coordinates; not first-author on all surfaces — first-among-equals within the design lens, with each role bringing their distinctive contribution.

## The seven surfaces (Lead Dev May 14)

1. **Conversation history / archive UI** — where users see prior conversations; entry point shape, list affordances, open/replace semantics
2. **Privacy / per-conversation controls** — `is_private` toggle surface; visual signaling; per-message vs per-conversation concept
3. **Settings / preferences** — profile, notifications, integration toggles, model selection, workspace prefs
4. **Integration setup wizards** — Notion / GitHub / Slack / Calendar OAuth; first-run consent + scope + error states
5. **Search interface** — cross-history; entry point shape; distinct from inline conversation search
6. **Empty / first-run states** — brand-new user with no conversations / integrations / history; MUX assumes flow
7. **Error / degraded states** — integration failures, slow models, tool errors

Dev work over the next 2-3 weeks (#1021 needs (1)+(2); M2g chat-actions adjacent to (3); integration activation needs (4); 1.0 launch needs (6)+(7)) will hit these. **Without UX guidance, dev defaults fill the vacuum.** Lead Dev's framing.

## Cohort goal + shape

**Goal**: produce a coordinated 1.0 scoping pass — *which surfaces are 1.0-required vs. post-1.0; what guidance shape each needs (full MUX doc, lightweight design note, ADR-paired, etc.); rough sequencing against dev work in flight*.

**Not the goal**: full MUX documents for all 7 surfaces this cycle. The scoping pass tells us *which surfaces earn that investment when*, and *what the minimum-viable design note looks like* for each.

**Operational shape**: async-first; one optional sync session at the end if convergence requires it.

- **Round 1 (async, by Wed May 20 EOD)**: each role submits role-specific scoping input per the section below. ~30-60 min per role; routed to `mailboxes/cxo/inbox/` as `mux-ui-gap-{role}-input-{date}.md`.
- **Synthesis (CXO, by Fri May 22)**: aggregate inputs into a single scoping memo with 1.0-required-vs-post-1.0 priority and per-surface guidance shape recommendations.
- **Convergence (optional sync, Tue May 26)**: if synthesis surfaces unresolved cross-role tensions, schedule a 30-min synchronous discussion. If async resolution is clean, skip the sync and route directly to CEO for ratification.
- **CEO ratification (target Wed May 27)**: scoping pass closes; per-surface guidance work fires per the agreed priorities.

This fits the "1-2 weeks without convening a formal sprint" framing Lead Dev's instinct named.

## What each role brings to scoping

Adapt the level of detail to what your role's lens produces; don't pad.

### Architect (state-shape and routing)

For each of the 7 surfaces, name: (a) what already exists in code / what would need to be built from scratch; (b) where each surface plausibly routes (sidebar, modal, dedicated route, command palette); (c) architectural risks per surface (e.g., search needs an index decision; integration wizards need OAuth-flow coordination). The four-element principle as load-bearing constraint where relevant.

### PPM (product priority)

For each of the 7 surfaces, name: (a) 1.0-required vs. post-1.0 from product-decision lens; (b) implicit PDR-adjacent commitments (privacy controls is values-laden — privacy as commitment, not afterthought; integration wizards shape what Piper *can* claim about itself); (c) any Class A/D Review Gate triggers in the surface set.

### Comms (voice consistency)

For each of the 7 surfaces, name: (a) voice-tone signals MUX has set elsewhere that need to carry through; (b) places where existing surfaces (compose, insights, standup) have *implicit* voice that the gap surfaces need to *explicitly* preserve; (c) which surfaces will produce narrative-arc opportunities (e.g., first-run as onboarding story; error states as honesty-about-limits story).

### Lead Dev (what's built vs. needs-build)

For each of the 7 surfaces, name: (a) concrete inventory of what's wired today (API endpoints, services, frontend scaffolding); (b) build-cost estimate ranges (small / medium / large; not exact hours); (c) per-surface dev-default risk (where will the vacuum get filled fastest if scoping doesn't ship in time).

### CXO (design priorities + MUX guidance)

For each of the 7 surfaces: (a) MUX-doc shape recommendation (full doc / lightweight note / ADR-paired / deferred); (b) Colleague Test scoring applicability — does the surface have a meaningful voice signature to score against; (c) cross-surface consistency calls (e.g., is the privacy signaling shape consistent with the COMPOSTED-state framing already in MUX). Plus the synthesis pass.

### PA (cross-pollination scan, no specific section needed)

Background: have Klatch / Janus / Vergil / Piper Open hit any of the 7 surfaces? Predecessor PA's principle-level-convergence-not-vocabulary-import discipline applies. If something useful surfaces from sibling project experience, route through standard signal traffic; if nothing surfaces, no memo needed — your silence is informative too.

## Naming and routing convention

- **Per-role input filename**: `mux-ui-gap-{role}-input-2026-05-{date}.md`
- **Destination**: `mailboxes/cxo/inbox/` (CXO synthesizes)
- **Routing memo**: file a brief routing-memo with the input as attachment-reference so the cohort sees what each role contributed; CC the cohort + CEO + PA + exec

## What this is NOT

- **Not a design sprint** — async-first, role-distinctive contributions, no synchronous bandwidth burn unless convergence requires it
- **Not a commit to ship all 7 surfaces by 1.0** — scoping determines which earn 1.0 priority; some may defer
- **Not a new PDR** — this is scoping work that may surface PDR-shaped questions (PDR-005 BYOC parallel), but the cohort's output is a scoping memo, not a PDR draft
- **Not CXO-unilateral** — CXO coordinates the cohort and synthesizes; each role's contribution is theirs to author

## Cross-references

- Lead Dev May 14 framing: `mailboxes/cxo/read/memo-lead-to-cxo-cc-ceo-mux-guidance-ui-architecture-gap-2026-05-14.md`
- Tracking issue: `#1090` (UI-1.0-PLAN, P1 epic)
- CEO direction: 2026-05-15 ~06:55 conversation
- MUX coverage map (existing strong coverage): conversation lifecycle, compose surfaces, insight surfaces, standup/morning surfaces
- BYOC PDR-005 discovery thread parallel (different scoping concern but similar cohort shape): `mailboxes/cxo/read/memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md`

## Standing offer

If your role's contribution needs more or less time than the Wed May 20 EOD target, flag back. The synthesis pass and ratification timeline can slip if any role surfaces material more complex than the scoping shape this memo assumes.

— CXO, 2026-05-15
