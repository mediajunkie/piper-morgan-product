# Sprint History Recovery Plan — Piper Morgan

**Owner**: PPM
**Status**: ACTIVE — designed 2026-07-05, execution in progress
**Purpose**: Full recovery of the project's historical issue→sprint assignments, after two GitHub Projects v2 field wipes (~2026-06-25, cause unclear; 2026-07-05, a full-replace field mutation — see CLAUDE.md CRITICAL warning), and a durable, wipe-proof canonical record going forward.

---

## Why this is hard, stated plainly

The GitHub Projects v2 "Sprint" field has no history of its own — confirmed empirically today across five independent checks (REST issue timeline, Enterprise/Org audit log, GraphQL schema introspection, webhook delivery logs, full git-history search). It only ever exposes current state. Once wiped, the true prior values are gone; anything we produce now is a *reconstruction*, not a *recovery* in the literal sense. The honest goal is: get as close to the true historical assignment as the evidence allows, be explicit about confidence everywhere, and never silently guess.

## What "sprint" actually means here, and why one method isn't enough

Two different kinds of sprints behave differently, and conflating them was my error until this session corrected it:

- **Narrow, workstream-style sprints** (Alpha-series A1–A31, D1, RECONNECT-WS-numbered work, the MUX V/X/L/I/P series): the sprint *is* the execution window. An issue's close date reliably falls inside its sprint's dates because the work happened then.
- **Broad, theme-bucket sprints** (M0–M5, RECONNECT as a whole): these function more as standing categories than tight execution windows. An issue can be deliberately assigned to one theme (e.g. M5) and then get formally closed much later, incidentally, during a different bucket's busy window (e.g. M2) — closing during M2 does not mean it was M2 work. Verified concretely today: #921/#932/#933/#935/#936 all closed during the M2 window but an explicit, dated April 8 planning document assigned them to M5 *before* they even closed.

This means the recovery method has to vary by sprint type, and every finding needs its method tagged so confidence is legible, not implicit.

## Recovery tiers, highest confidence first

**Tier 0 — Already known good (done).** 265 issues restored today from first-hand knowledge + the June 27 CSV's HIGH/MEDIUM rows, independently verified. Today's snapshot script (`scripts/snapshot-project-board.sh`) now protects this going forward.

**Tier 1 — Explicit dated planning-document assignments.** The highest-value source: documents where a PM or agent made a deliberate, dated, written assignment decision (not an inference). Known documents so far: `sprint-reassignment-plan-2026-04-08.md`, `m2-surface-review-decisions-2026-05-03.md`, `m2-unmapped-families-triage-verdicts-2026-05-05.md`, `pa-m2-convergence-memo-2026-05-23.md`, PA's June 28 execution log (225 assignments run) and the PPM June 28 findings memo. **Action**: systematically extract every assignment from every such document project-wide, not just the ones surfaced so far — this is likely the largest lever available, and it's the one immune to the broad-vs-narrow sprint problem, since it's direct evidence of intent rather than inference from timing.

**Tier 2 — closedAt-vs-calendar match, narrow sprints only.** 243 candidates found today: single clean match, and the sprint is a narrow/workstream type where close-timing is trustworthy. High confidence.

**Tier 3 — Text-mining, HIGH confidence, no conflict.** 24 candidates from today's session-log archaeology: explicit, unambiguous statements, independently verified against source files.

**Tier 4 — closedAt-vs-calendar match, broad-bucket sprints, corroborated by Tier 1.** The 273 broad-bucket matches from today, kept only where a Tier 1 document agrees or where no Tier 1 evidence contradicts them. Where Tier 1 and the date-coincidence disagree, Tier 1 wins.

**Tier 5 — Ambiguous overlaps requiring disambiguation.** 273 issues where multiple sprint windows overlap their close date. Many are likely resolvable mechanically via title-prefix matching (an issue titled `RECONNECT-WS...` closing during a RECONNECT/D1 overlap is clearly RECONNECT) — attempt this first; what's left needs domain judgment.

**Tier 6 — Domain-authority consultation.** Where the project's own real cohort agents have standing authority PA's June 27 memo already named: CXO on the D1/D2 boundary, Lead Dev on the RECONNECT cluster (deferred — Lead Dev is busy per PM's direction; Architect as secondary read given their ADR-071/073 involvement), PA on what happened to the "31 M5-Other" list and any memory of the June 28–July 4 window.

**Tier 7 — Open issues (162).** closedAt doesn't apply — they haven't closed. These need "what's the currently-intended sprint" logic, not historical reconstruction. Lower priority; not lost history, just未-assigned current work.

**Tier 8 — PM-dependent resolution.** What's left after Tiers 1–7: the inchworm map (PM is repasting this), the 18 CSV rows already flagged needing an explicit PM call, and whatever remains genuinely ambiguous after every automated and cohort-consulted method is exhausted. This is the honest floor — some fraction of ~1,164 issues' history may simply not be recoverable, and I will say so explicitly rather than paper over it with a guess.

## Durable output

A new git-tracked canonical file — issue# | sprint | confidence | tier/method | evidence citation | date — becomes the source of truth going forward, cross-linked from `beta-blockers.md`/`sprint-order.md`. The GitHub Sprint field is repopulated from it, but the field is no longer the *only* record — every entry in the file has its own git history, isn't subject to a single mutation wiping it, and gets refreshed by the snapshot script on a regular cadence.

## What I'm asking the cohort for (via mailbox, this session)

- **CXO**: domain call on D1/D2-boundary ambiguous issues (Tier 5/6)
- **Architect**: secondary read on RECONNECT-cluster ambiguous issues, given Lead Dev is unavailable
- **PA**: what happened to the "31 M5-Other" issue list mentioned in the June 27/28 exchange, and any memory of sprint-assignment work between June 28 and July 4

## Honest scope estimate (running total, will update as tiers execute)

To be filled in as each tier completes — see session log / next PM update for current numbers.
