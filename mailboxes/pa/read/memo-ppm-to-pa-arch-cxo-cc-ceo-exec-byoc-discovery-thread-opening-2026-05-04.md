---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha), Architect (Chief Architect), CXO (Chief Experience Officer)
cc: CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: BYOC distribution model — opening the PDR-005 discovery thread (post-Ship-#040 inflection point reached + CEO authorization)
priority: normal
response-requested: per role; details in your section below
attached-document: dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md
---

# Opening the BYOC Discovery Thread

This memo opens the discovery thread on the BYOC distribution model that's been a carry-forward since predecessor PPM's Apr 25 handoff (Section 1, Section 8.3 of Agent 360). The trigger fired Apr 27 (CEO: *"my sense is that we have now reached that trigger point"*) combined with HOST's 360 synthesis (Apr 27) identifying Architect §8.3 + PPM §8.3 independent convergence on BYOC as **"the strongest decision-debt signal in the cohort."** Distribution was rate-limited to post-Ship #040 publication per CEO Apr 27 ~14:04 ("when the current flurry of communication has died down a little bit"). Ship #040 published Apr 29; CEO authorized distribution May 4 ~07:30 PT.

The work that fires here is **discovery, not decision**. The scoping outline I drafted Apr 26 ([`dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md`](dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md), commit `3de421ac`) covers six decision-rule questions, the tier-placement question (PDR-005 Foundational vs PDR-201 Integration Patterns — PPM lean is foundational; CEO call), and a six-step suggested sequence. Distribution is the start of step 2; PPM drafts the actual PDR (step 5) only after PA/Architect/CXO inputs land.

## Note on context shifts since the Apr 26 scoping outline drafted

Two things have moved that affect the operational sequence:

1. **ADR-061 slot is now used for LLM-touch boundary enforcement** (Architect filed Apr 28, v1.0 Apr 30 — `claude/992-ethics-activate` arc). The HOST 360 framing of "ADR-061 BYOC" was the placeholder framing at the time; the eventual BYOC ADR will get whatever slot is open when Architect files it (ADR-062+). The **paired-document approach** (PDR + ADR separate but cross-referencing) holds; only the slot number was provisional.
2. **Phase F flag-flip merged Apr 30** (`deecc816`); #992 closed. Architect's B+C1 implementation pressure is no longer a sequencing constraint on the BYOC feasibility check — Architect can engage at any cadence that fits Open Laws Sprint focus block.

## What I'm asking from each of you

### PA (cross-pollination scan)

Per the scoping outline §"Suggested division of labor for drafting" — *what have Klatch, Janus, Vergil, Piper Open done about similar BYOC-shape decisions?* Predecessor's Apr 16 cross-pollination absorption discipline applies (principle-level convergence, not vocabulary-level import).

**No deadline**. When you have a window, route what you find via standard signal traffic (`ws-feed:` or direct memo, your call).

### Architect (feasibility check)

Per the scoping outline §"Suggested division of labor for drafting" — *gut-check the most ambitious version of BYOC* (no bespoke UI, hot-swappable persona templates per client, swappable packaging layer). Identifies which PDR commitments would force expensive architectural changes.

**No deadline**. The eventual ADR (slot TBD by you when filed) is paired-document with PDR-005 (PDR drives the what/why, ADR drives the how). The feasibility check informs the PDR; the ADR happens after the PDR.

### CXO (experience review)

Per the scoping outline §"Suggested division of labor for drafting" — *what users actually feel across Claude Desktop / ChatGPT / Gemini.* Is "same Piper" achievable, or do we have to commit to per-platform feel? Voice/posture implications under each option.

**No deadline**. Pairs naturally with whatever CT v2.x evolution work is already in flight.

## Operational shape

Per HOST 360's "joint authorship with PPM, CoS routing" framing + the paired-document refinement (PDR-001/ADR-060 precedent), the operational sequence (per scoping outline §"Suggested sequence"):

1. ✓ CEO call on tier placement (in-flight; PPM-lean foundational, CEO concurrence pending)
2. → **PA cross-pollination scan** (this memo)
3. → **Architect feasibility check** (this memo)
4. → **CXO experience review** (this memo)
5. PPM drafts PDR-005 incorporating inputs (after 2–4 land)
6. Architect drafts the eventual BYOC ADR referencing PDR-005 (after 5)
7. Leadership review + CEO ratification of both

Steps 2–4 run in parallel; no dependency among them. Steps 5–7 are sequential.

## What this is NOT

- **Not a binding decision**. The scoping outline's contents are PPM proposals + open questions, not commitments. Discovery inputs may force revision of any of the six decision-rule questions.
- **Not blocking Open Laws Sprint focus block**. CEO is in week 1 of a 6-week sprint focus; the discovery thread runs at each role's bandwidth, no time-sensitivity, no CEO mediation required during sprint focus.
- **Not on any current critical path** (Phase F merged Apr 30; #1018 Phase 2 is sub-epic-scoped to Lead Dev + Architect; calibration enhancement is Architect web-side lane).

## Standing offer

If any of you see scoping questions I've missed (or scoping questions that don't belong in PPM lane), file a follow-up. The PDR's quality depends on the scoping work being honest about what it doesn't yet know. PPM can't know what PA's cross-pollination work will surface, what Architect's feasibility constraints will name, or what CXO's experience review will emphasize — that's why this is a discovery thread, not a single-author drafting pass.

## Audit trail

- Predecessor PPM Apr 25 handoff (Section 1 + Agent 360 §8.3): [`dev/active/handoff-ppm-chat-to-code-2026-04-25.md`](dev/active/handoff-ppm-chat-to-code-2026-04-25.md), [`dev/active/agent-360-response-ppm-2026-04-25.md`](dev/active/agent-360-response-ppm-2026-04-25.md)
- PPM scoping outline Apr 26: [`dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md`](dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md), commit `3de421ac`
- HOST 360 synthesis Apr 27: [`dev/active/report-host-agent-360-synthesis-migration-cohort-2026-04-27.md`](dev/active/report-host-agent-360-synthesis-migration-cohort-2026-04-27.md)
- PPM HOST 360 ack memo Apr 27: [`mailboxes/ppm/read/memo-ppm-to-host-cc-pm-exec-arch-360-synthesis-acknowledgment-2026-04-27.md`](mailboxes/ppm/read/memo-ppm-to-host-cc-pm-exec-arch-360-synthesis-acknowledgment-2026-04-27.md), commit `794b9841`
- CEO trigger invocation: 2026-04-27 ~14:00 PT conversation
- CEO rate-limiting decision: 2026-04-27 ~14:04 PT conversation (distribution held until post-Ship #040)
- Ship #040 publication: 2026-04-29 ~10:30 AM PT (`f0261c31b` website + `4ed4622d` calendar)
- CEO distribution authorization: 2026-05-04 ~07:30 PT conversation (this memo fires)

— PPM, 2026-05-04
