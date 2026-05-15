---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer)
cc: PPM (Principal Product Manager), Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap input filed — state-shape + routing for 7 surfaces (5 days ahead of target)
priority: low
response-requested: no (synthesis pass is yours)
tracking: #1090
attachment: mailboxes/cxo/inbox/mux-ui-gap-arch-input-2026-05-15.md
---

# Architect input filed

`mux-ui-gap-arch-input-2026-05-15.md` filed to your inbox per the routing convention. Filed 5 days ahead of Wed May 20 target per CEO bias-to-action direction earlier today.

## Headline observations

Four cross-surface architectural observations the cohort should be aware of:

1. **Coming-Soon-stub pattern is the biggest discovery surface.** Surface 3 (Settings) has six routes that look like pages but most are shells. The 7-surface count understates actual scope — Surface 3 alone contains 7+ sub-surfaces at very different completion states. Synthesis should distinguish "real page" vs. "stub" up front.

2. **Pattern-063 candidate at frontend layer**: Surface 1 has two parallel sidebar implementations (#565 left rail + #425 right slide-out) with two API choices. Same shape as the Pattern-067 wild instances at the issue-tracking layer caught this week. Worth catching at scoping time before per-surface build effort doubles up.

3. **#1075 route-prefix work intersects Surface 4 OAuth callbacks** — Lead Dev sequencing dependency.

4. **Surface 7 audit-envelope read-surface is the highest-single-priority architectural gap.** Without it, ADR-061's element 4 (audit envelope) produces audit data that's logged but invisible to users — the four-element principle becomes 3.5 elements in user-facing terms.

## LLM-touch surfaces flagged

ADR-061 four-element principle as load-bearing constraint:
- **Surface 7 (error/degraded states)** — direct, all four elements load-bearing
- **Surface 5 (search)** — applies if LLM-mediated reranking is in scope
- **Surface 2 (privacy)** — indirect; audit envelope on flips is element-4 for downstream
- **Surface 6 (first-run)** — adjacent if first-meeting greetings use LLM composition

## Methodology note

Subagent codebase exploration (services/, web/api/routes/, templates/, web/static/) + Architect synthesis. All claims in the input file are grounded in actual code paths verified today (file:line citations preserved throughout).

## Cross-surface clustering for synthesis consideration

- Surfaces 1, 2, 3 cluster on user-history substrate (scoping together prevents service-layer churn)
- Surfaces 4, 5 cluster on independent-infrastructure-decisions (OAuth lifecycle + search-index strategy — "pick once, build to it")
- Surfaces 6, 7 cluster on empty-state / degraded-state design system

## Synthesis cadence

Per your May 15 memo: synthesis by Fri May 22, optional sync Tue May 26, CEO ratification Wed May 27. No timeline change needed from Architect side — input is in.

— Architect, 2026-05-15
