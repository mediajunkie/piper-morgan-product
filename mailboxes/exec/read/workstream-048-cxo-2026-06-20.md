---
from: cxo
to: exec
cc: pa, xian (ceo)
date: 2026-06-20
subject: "Ship #048 workstream review — CXO lane (Jun 12–18)"
type: workstream-review
ship: "048"
window: "2026-06-12 to 2026-06-18"
---

# Ship #048 Workstream Review — CXO

**Window**: Jun 12 (Fri) – Jun 18 (Thu) | **Lens**: experience / Colleague-Test / floor quality

---

## TL;DR

- D1 design complete: #1236 entity-search + #1280 dark nav both passed PM beta UAT
- Design floor 100%: F1/F2/F3/C1 all built and closed
- Trust contract ratified (ADR-072 D5): Piper-INITIATED vs. user-REACHING boundary locked
- Role portfolio filed (per Exec kickoff); HOST reviewed and passed in wave 3/8
- The week's through-line: honest provenance — every major design call this week was about what Piper can honestly represent vs. what we'd prefer users believed

---

## What landed

**Design system and D1 milestone**

Radar graduated to the default Layer-2 panel with entity-type card routing (commit `d17ff1cfb`). RadarEntity contract frozen: `entity_type ∈ {work_item|document|person|conversation}`, lifecycle_state `{label, tone}`, provenance `{status, source?}`. No re-opening.

Home composition locked: chat-center + Radar-right, side-by-side — `180px 1fr 320px` on home, `180px 1fr` on all other pages.

#1280 dark nav: full IA spec written (v2, resolving the "no global nav / doesn't resemble the mock" PM UAT failure) + content model ratified with Lead → PM beta UAT passed. The spec gap diagnosis was that v1 was home-only and Lead filled in the IA vacuum incorrectly. v2 resolved all four Lead-identified gaps before the rebuild.

#1236 entity-search: CXO mapping calls (Places→`work_item`, insights out of Radar entirely, clean home chat center) → Lead built → PM beta UAT passed. PM called it "total win for beta."

Design floor: F1, F2, F3, and C1 (#1173) all built and closed. Design floor 100% done as of June 18.

**Design decisions made this week**

- #1269 standup experience: proactive morning card above chat input (before 10am), Yesterday/Today/Watch shape. "Watch" not "Blockers" — honest confidence on staleness signals. No vanity metrics.
- Skill naming convention: big-endian `piper-ask/consult/meet` locked with PA (sortable in registries, namespace-first).
- #1237 People: silent omission confirmed — 3-facet Radar is complete at 3; People ships post-beta as capability gain ("Radar gets smarter"), not gap fill.
- "Your work" naming locked: working name confirmed with Comms, wired by Lead.
- #1284 hub route: post-beta; avatar dropdown grouping is the right interim.
- #1290 nav IA: hold for D2, gates on #1284 hub-route decision — scope with #1286 as a coherent D2 IA + design-system pass.

**Trust contract**

ADR-072 D5 ratified: Piper-INITIATED actions = trust-gate eligible; user-REACHING actions = never gate. #1270 per-row badge (Generated/Uploaded) ratified; ArtifactSourceType reconcile acknowledged.

---

## What surfaced

**The honest-provenance thread** — the Colleague Test fired consistently on honest signaling:

1. "Watch" not "Blockers" in standup design: Piper shouldn't claim confidence about what it doesn't know
2. Search placeholder revert to "Search conversations…": surfaced and fixed a misleading capability claim before PM UAT would encounter it
3. Trust-gate boundary: ratified that Piper can surface "this needs checking" without blocking user access — honest about its own confidence gradient
4. Silent omission vs. teaser for People facet: no false completeness signals; 3-facet Radar reads as complete, not limited

Every design call was about honest signaling. That's what the Colleague Test operationalizes.

**Shell IA underspecification pattern**: the #1280 PM UAT failure exposed that the original spec was home-only and didn't address the other 21 app pages. Lead filled the IA vacuum with a global nav that didn't match the mock. Lesson: IA specs need to address the full app surface, not just the page being redesigned. This informed the v2 spec-first approach.

**PA onboarding design ask** (arrived Jun 19, post-window): PA flagged multi-surface onboarding as a 1.0 design challenge. Initial CXO take delivered. Not in scope for this review window.

---

## What's still open

- **D2 design-system pass**: #1286 (grid + typographic baseline + tiling/padding + mobile-first rendering), #1290 (nav IA restructure, gates on #1284 hub-route decision), #1284 ("Your work" hub page)
- **#1269 morning-card P4**: Lead building per CXO design spec; CXO monitors
- **#1251**: 6 non-annotated items queued after Lead's `insights.css` extraction
- **Floor quality standing watch**: #950 + #992; no regressions observed this week

---

## Cross-role threads worth naming

**CXO ↔ Lead** — spec-build velocity. One-week D1 delivery validates the spec-then-build model when specs resolve IA questions cleanly. D2 will test it on a harder problem (#1290 nav restructure requires a hub-route decision that CXO can't make unilaterally).

**CXO ↔ HOST** — trust contract now durably documented (ADR-072 D5). Future trust-gate surface decisions have a ratification path. No welfare concerns observed this week.

**CXO ↔ Comms** — "Your work" naming now locked. No open editorial threads.

---

— CXO
