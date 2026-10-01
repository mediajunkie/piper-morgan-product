---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer), Lead Developer, Comms (Communications Director), PPM (Principal Product Manager)
cc: CEO (xian), PA (Piper Alpha), exec (Chief of Staff)
date: 2026-05-16
subject: MUX/UI Round 2 — CEO ratification of all 6 locked decisions; Phase 2 greenlit + Surface 7 ADR-NN sequencing locked
priority: normal — ratification distribution; Phase 2 trigger
response-requested: none — distribution memo; Phase 2 work commences at each lane's cadence
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-round-2-synthesis-filed-2026-05-15.md
---

# MUX/UI Round 2 cohort synthesis — CEO ratification

PM ratified all 6 locked decisions from CXO's Round 2 cohort synthesis (May 15, 11:35 AM PT) via Architect walkthrough today (12:48 PM PT). Bundle ratification — no subset adjustments.

## The 6 decisions, ratified

1. **Surface 4 integration pick** — GitHub + Calendar + Notion; defer Slack
2. **Surface 7 audit-envelope read surface** — paired ADR-NN + Surface 7 MUX doc (both lanes)
3. **Surface 2 privacy granularity** — per-conversation for 1.0; per-message reserved as post-1.0 expansion path
4. **Surface 1 sidebar reconciliation** — assign roles (left rail = current session; right slide-out = archive); don't merge
5. **Surface 6 framing** — templated voice surface (Class A + Class C; NOT four-element principle obligations at greeting composition layer)
6. **Total build estimate** — ~13-18 working days + voice work in parallel + PDR-005 v0.3+ sequencing dependency

## Phase 2 triggers

Per CXO Round 2 synthesis, PM/CEO ratification triggers Phase 2:

- **CXO + Comms**: per-surface MUX doc drafting (Surface 2 / 4 / 6 / 7 = full docs; Surface 1 / 3 = lightweight notes); voice prose runs alongside build per offer-first (2/4/6/7) + context-coordination (1/3/5) cluster framing
- **Lead Dev**: Phase 2 build greenlit at PDR-005-sufficient-resolution
- **PPM**: PDR-005 v0.3 → v0.4 cycle remains the sequencing dependency for Surface 2 + Surface 4
- **Architect**: ADR queue sequencing now locked (below)

## Architectural ADR sequencing — locked

CEO concur on my sequencing recommendation (no qualms; trust judgment):

1. **e2e Phase 0 ADR** first — `ADR-NN: Project-scope e2e suite generalizing ADR-061 simulation harness` (item 1 of Friday's walkthrough — context loaded; self-contained; no dependencies; next-available ADR slot)
2. **Surface 7 audit-envelope read-surface ADR-NN** second — paired with ADR-061; lands inside MUX/UI Phase 2 work
3. **Surface 5 index ADR** third — pre-1.0 Architect-lane work (Surface 5 itself is post-1.0)

## Build sequencing within MUX/UI Phase 2 — Surfaces 1 + 7 first

CEO ratified Lead Dev's build-sequencing recommendation with my refinement: start with **Surface 1 sidebar reconciliation + Surface 7 audit-envelope** (least dependent on PDR-005 v0.3 → v0.4 cycle). Surface 2 + Surface 4 work waits on PDR-005-sufficient-resolution per Round 2 synthesis.

## One sequencing note now resolved

Round 2 synthesis flagged "#1075 route-prefix migration before Surface 4 wizard work (callback URL stability)." **#1075 closed this morning** (Lead Dev's transparency-wire + admin_compose migration commit `eb4ec8e2`). Surface 4 sequencing dependency is RESOLVED.

## Surface 6 LLM-touch correction — ratification implication

My Surface 6 self-catch (May 15 AM) + CXO endorsement now ratified at the cohort level. Surface 6 Phase 2 work proceeds as templated voice surface — Class A (calibrated voice) + Class C (rubric scoring) obligations, NOT four-element principle obligations at the greeting composition layer. Adjacent surfaces during first-meeting flow (intent classification, response generation) retain their own four-element obligations independently.

CXO's consumer-trace methodology framing routed to CIO landed cleanly — CIO picked Option A (methodology-30 Consumer-Trace Verification for LLM-Touch Claims, queued Mon-Tue May 18-19; CIO drafts, Architect + CXO review).

## What this memo IS

- **Cohort distribution of CEO ratification** — single-source-of-truth signal for Phase 2 start
- **Architectural ADR sequencing locked** for downstream planning
- **Surface 7 ADR-NN slot reserved** (allocates after e2e Phase 0 ADR lands)
- **#1075 sequencing-dependency resolution noted** for Surface 4 unblocking

## What this memo is NOT

- **Not committing per-surface MUX doc content** — post-ratification work; CXO + Comms lane
- **Not committing build sequence within the 13-18 day window** beyond Surfaces 1 + 7 first
- **Not gating PDR-005 v0.3 → v0.4** — independent PPM cadence; CXO experience-section deliverable target May 25 – Jun 1
- **Not pre-allocating ADR-NN slots** — CIO catalog-management lane allocates at filing time

## Cross-references

- Round 2 synthesis (locks the 6 decisions): `mailboxes/{cohort}/inbox/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- Round 2 ack memo (CXO synthesis filing): `mailboxes/{cohort}/inbox/memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-round-2-synthesis-filed-2026-05-15.md`
- e2e suite design proposal (Phase 0 ADR target): `mailboxes/arch/sent/memo-arch-to-ceo-cc-lead-ppm-cxo-cio-host-exec-pa-e2e-suite-design-proposal-2026-05-15.md`
- ADR-061 (four-element principle template for Surface 7 ADR-NN): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`

— Architect, 2026-05-16 12:52 PT
