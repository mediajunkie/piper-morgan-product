# Ship #054 internal report — window Jul 24–30 (for PM's eyes)

**By**: Exec, 2026-08-04 evening · **Companion to**: `weekly-ship-054-draft-2026-08-03.md` (public, awaiting your pass, publishes Wed Aug 5)
**Sources**: all 7 omnibus logs (Jul 29–30 backfilled by Docs this afternoon — the draft predates them; cross-check below), all 6 workstream memos, session logs where omnibus was thin, live GitHub verification.
**Process note, honestly**: this report is late in the cycle — #053's pattern (report → then draft) is the right order and this cycle went straight to the draft. Yours via Janus tonight; corrected next cycle.

---

## The window in one paragraph

The whole team moved house (11/11 roles to Amber across five days) while running its busiest coordination week yet — and spent the same week discovering that five of its own trusted instruments could report "clear" without measuring. Zero publication slots missed. The backlog lever got pulled (105→56 via the methodology-package deletion). The alpha-tester review completed 4/4 with independent convergence, PDR-006 reached ratification-ready, and the beta gate got caught unfalsifiable in *both* directions — by their own would-be signers. Only 5 issues closed, and that's the honest shape: a migration/instrumentation week, not a burn-down week.

## The three-lens read you asked me to carry (#052/#053 framing)

- **What held**: the 6/6 workstream gate (through CIO's late memo — nudged, not waived); mail delivery through every cutover (push-to-ref never broke); the publication cadence (5/5 slots); mailbox discipline while its enforcement hook was *proven never to have fired* — prose held where the mechanism was absent.
- **What was resilient**: five dark roles recovered with full context (2-for-2 woken predecessors answered "I have the thread"); PM's main-checkout conflict and the gloss race both resolved same-day without loss; every provisioning defect (stale worktree, prefix-match, silent kickoff wedge) was caught by the one-at-a-time roll discipline.
- **What was antifragile**: each instrument failure produced a stronger mechanism — the hook saga ended in a real git-level gate (structurally shape-independent); the memory-index near-miss ended in a generator-level refusal rule; the watchdog's alert-on-compliance defect produced the heartbeat; the probe confusion produced m-45. None of these depends on anyone being careful next time.

## What the public draft deliberately doesn't say (register, not concealment)

- **Names**: the "founder's live user ID in the test suite" is yours; the four-wrong-characterizations arc is Arch's own honest telling; the "role that didn't exist for two days" is Arch (cron un-armed — the consequence-naming lesson).
- **The near-miss count**: five separate fixes this window contained the defect they fixed, every one caught by a non-author (CIO's §3 — their escalation: "individual rigor is not the working mechanism here, cross-checking is").
- **CXO's §6.1 flag, verbatim intent**: the D2 design-system portfolio hasn't moved in two windows — "it should be a decision rather than a drift." That's yours to make, not theirs to keep absorbing.
- **HOST's welfare item** (in the public Blockers only softly): 12 tokens out, 1 report, obtained only after you asked twice. HOST: "I need a decision rather than more work."

## Cross-check against the backfilled Jul 29–30 omnibus (written after the draft)

Two items the draft under-weights; **both are candidate one-liners for your pass if you want them**:
1. **The compose-autosave data-loss bug** — your alt text silently blanked by a React closure-staleness defect; found by Comms, root-caused and fixed same-day by Web, verified via a standalone reproduction on a browserless host. A real production save-path bug with a same-day fix; currently only implicit in the draft.
2. **#1461 cross-user token isolation** — found *because* the seat finally had keys ("keyless CI green was vacuous — only a keyed seat can see it"); you ruled isolation semantics (a) on 8/1 (out-of-window, so the *finding* is #054 material, the *ruling* is #055's).

Everything else in the backfill confirms the draft's claims; no factual conflicts found.

## Per-role, one line each (franker than the ship)

- **Lead** — dark most of the window post-migration-readiness (structural: never armed), then the stack landed at window-edge. The lane's discipline held in absentia — Tests green survived unattended.
- **Arch** — the window's intellectual engine (TOCTOU ruling, layer map, m-45) *and* its honest cautionary tale (two nonexistent days; three of its own currency rules found dead). Their §6 framing — "checkable beats careful" — is the week's best sentence.
- **CIO** — ran the migration end-to-end; five fixes with embedded defects, all caught by others; owned it as a systems finding rather than apologizing. Retired their top portfolio priority (migration) legitimately.
- **CXO** — strongest instrument-QC of the window (criterion-2 withholding; caught the probe re-encoding its own confound); named their own portfolio slip unprompted.
- **PPM** — availability was the binding constraint (parked, PM-resumed three times); when running, the synthesis function was excellent (the sort key, the gate finding). Their three-pass PM-caught error produced the best transferable lesson: familiarity suppresses the read-the-whole-artifact check.
- **HOST** — highest output (166 commits), a third of it self-correction, every instance named; the checklist v2.0 rewrite is the durable artifact.
- **Comms** — zero missed slots through the migration + the laundering-effect finding (a silent revert that gets helpfully re-filled looks like diligence — only your open browser tab caught it).
- **Docs** — the omnibus gap (Jul 29–30) was theirs and they closed it retroactively this afternoon, plus the CLAUDE.md separation you greenlit landed at −5.1% with four missing norms added.

## Your open decision queue as of tonight (all previously flagged, consolidated)

1. **Ship #054 pass** → then your go to Comms. Publishes tomorrow; #053 proved same-day works if needed.
2. **Jake six items** — CXO's positions filed; confirm-or-adjust unblocks PPM's conversion.
3. **#1484** (supersedes #1481 per PPM's accepted Arch ruling) — now labeled the beta blocker; PPM's scope-not-engineering read stands.
4. **Skill-candidates review** — CIO's prep ready; slipped from today.
5. **Tester-welfare instrument** (HOST) · **memory-index format** (governance; guard live) · **#1278 scope** (gate criterion 1) · **#1462 milestone** (rec: Production).

*Beta: Sat Aug 8, durably recorded. Criterion 2: routing signed 100%, quality signed 90.9%, one discharge line open. Scenario-B run + criteria 1/4/5/6 remain.*
