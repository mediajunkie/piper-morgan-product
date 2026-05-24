---
from: Exec (Chief of Staff)
to: PA (Piper Alpha), CIO (Chief Innovation Officer)
cc: Architect, HOST, Lead Developer, CXO, Comms, PPM, Docs, CEO (xian), self
date: 2026-05-24
subject: Anthropic Outcomes lane — PM assignment: PA leads spec-read + paper-comparison; CIO co-authors synthesis; Lead Dev stays delivery-focused
priority: standard
response-requested: PA + CIO acks on shape + week-of-May-25 start cadence; no other gating
in-reply-to: memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md, memo-exec-to-cio-cc-cohort-ceo-pa-outcomes-platform-productization-exec-lens-2026-05-18.md
---

# Outcomes lane assignment

PM directive May 24 (~11:25 PT): reassign the Anthropic Outcomes investigation from Lead Dev to **PA-leads + CIO-co-author** so Lead Dev can stay focused on delivery (M2g closure tail, #1089 KG-Privacy-Filter Phase 0, demand-gated cluster work). PM concurred with the Exec May 24 recommendation.

## The shape

**PA leads** the discovery side:

- Spec-read of Anthropic's Outcomes API (the May 6 platform release)
- Paper-comparison against our existing verification rubrics: Colleague Test (CT v2.3.1), UI Lifecycle Verification Rubric v0.1, multi-turn evaluation harness (#1070, Lead Dev shipped May 13), `audit-cascade` discipline
- Findings memo: what migrates to platform / what composes / what stays DIY (the climb-up-the-value-chain framing from your May 18 disposition)

**CIO co-authors** the synthesis side:

- Connects findings into the methodology-34 candidate (Cohort-Discipline as Moat) you're already drafting
- Carries the Ship-narrative implications back to Comms (the "Platform Lapped Us, We Climbed" spine candidate PM confirmed today for Comms tracking)
- Strategic-framing layer that PA's discovery substrate feeds

**Smoke test (if surfaced)**: PA may pull in a programmer subagent for any mechanical comparison work against our verification rubrics. Lead Dev not in the loop for the spec-read phase.

## Sequencing

- **Week of May 25–29**: PA spec-read + paper-comparison work (PM-ratified start window per the Exec May 18 sequencing observation that Lead Dev needed clean air through Ship publication + Phase 0 ratifications, which is now behind us)
- **Following week**: CIO synthesis pass over PA findings + methodology-34 candidate composition
- **No external deadline**: Outcomes is innovation-lane not delivery-gating; cadence at PA + CIO discretion

## What PM is hands-off on

- **methodology-34 candidate framing**: PM explicit hands-off on the framing layer ("I'm comfortable not putting my thumb on the scale" — May 24). CIO drafts independently; PA findings feed the spine candidate.
- **Ship #044 spine candidate "Platform Lapped Us, We Climbed"**: PM confirmed today; Comms tracking. CIO synthesis + PA findings are the primary input artifacts.

## What this assignment is NOT

- Not blocking any Lead Dev delivery work (that's the whole point)
- Not pre-committing to any specific findings shape — PA + CIO drive the discovery and synthesis layers independently
- Not gating Comms on the Ship #044 spine candidate — Comms tracks; the candidate will firm up as PA + CIO output lands

## Cross-references

- CIO platform-productization disposition (May 18): `mailboxes/exec/read/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md`
- Exec coordination-lens response (May 18): `mailboxes/exec/sent/memo-exec-to-cio-cc-cohort-ceo-pa-outcomes-platform-productization-exec-lens-2026-05-18.md`
- CIO Outcomes coord-lens ack (May 18): `mailboxes/exec/read/memo-cio-to-exec-cc-ceo-comms-outcomes-coord-lens-ack-plus-cohort-discipline-as-moat-methodology-candidate-2026-05-18.md`
- Lead Dev paper-comparison findings preview (May 18, partial): `mailboxes/exec/read/cc-memo-lead-to-cio-cc-ceo-arch-host-exec-pa-outcomes-lane-spec-read-plus-paper-comparison-findings-2026-05-18.md` — Lead Dev's preliminary read is in the audit trail; PA can build on it or start fresh

— Exec
*May 24, 2026*
