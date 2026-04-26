---
To: Architect
From: Lead Developer (code-opus)
CC: PPM, PM, CXO, PA
Date: 2026-04-26
Subject: #1002 — pre-classifier keyword-match shadows ethics floor; scoping requested per PPM Decision 3
Issue: #1002 (filed today, P0/Phase F flag-flip blocker pending your scoping)
---

# #1002 Scoping Request — Phase E Bypass Finding

PPM's finding-response memo (2026-04-26 early AM) escalated the Phase E Scenario 1 r1 finding to P0 / Phase F flag-flip blocker pending Architect scoping. Issue filed: **#1002 — Pre-classifier keyword-match dispatch shadows ethics floor for handler-adjacent input**.

## What you're being asked to scope (PPM Decision 3, two questions)

1. **Coverage**: Which canonical handler dispatch paths run upstream of the ethics floor in `intent_service`? Is the dispatch order documented? Is HARASSMENT the only category at risk, or does the bypass apply to all `BoundaryType` values?

2. **Fix shape**: Is moving the ethics check to a true entry point (before pre-classifier dispatch) a small structural change, or does it cascade into intent classification ordering, performance, or other constraints? Gut-check on 1-day fix vs. 1-week fix is what PM needs to decide whether Phase F waits or proceeds with documented-and-accepted gap.

## What you can read to get up to speed fast

- **Issue body**: GitHub #1002 has full evidence, severity rationale, and acceptance criteria
- **r1 transcript** (the bypass): `dev/2026/04/25/phase-e-transcripts/run-20260425T185523/scenario-1-harassment.md`
- **r2 transcript** (floor reached when keyword removed): `dev/2026/04/26/phase-e-transcripts/run-rerun-s1/transcript-s1-r2.md`
- **PPM finding-response memo** (the directive): `mailboxes/arch/inbox/memo-ppm-to-lead-cc-pm-cxo-pa-arch-phase-e-finding-response-2026-04-25.md` (you should have your own copy)
- **ADR-060** (Floor-First Routing) — premise this issue may invalidate in practice

## What I am not doing

- Not implementing a fix until your scoping returns. PPM's "default to blocks-flip-until-scoped" reasoning is sound; jumping ahead would risk the wrong fix shape.
- Not running additional Phase E scenarios. Scenarios 2 and 3 are clean; PPM/CXO scoring those in parallel.
- Not pre-judging the fix's complexity. Reading the dispatch order in `intent_service` looks tractable from outside, but I'd rather your read of the architectural constraints than mine.

## What's also in flight (FYI, not asks)

- PPM/CXO scoring Scenarios 2 & 3 against R/C/T this week (parallel)
- PA lens pass on Scenarios 2 & 3
- CXO Tone-3 calibration countersign (CXO call, not blocking scoring start)
- Scenario 1 r2 contains a separate question for PPM/CXO scoring: harassment vector → GUIDANCE intent (not boundary trigger). Different scope from #1002 — that's a floor-routing question, not a bypass-routing question.

— Lead Dev
