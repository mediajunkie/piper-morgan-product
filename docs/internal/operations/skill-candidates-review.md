# Skill candidates review — standing PM+Exec surface

**STATUS: RATIFIED — monthly cadence** (PM, 2026-07-08 11:49: *"yes monthly seems right."*) Candidate dispositions below remain first-pass leans pending the first actual review. **CIO + HOST looped in per PM's direction** (same message): CIO for the skill discussion itself (methodology-catalog lane), both CIO and HOST for aligning this cadence with the existing staggered audits (weekly/monthly audit template split, Docs's weekly audit, quarterly sweeps) so this doesn't become a fourth unaligned rhythm.

**PM's framing observation worth keeping visible** (2026-07-08): *"one trend I've noticed in the past few months is emergent self-improvement and self-healing behaviors. Some from the model upgrades perhaps but others from our own harness."* This review is the deliberate channel for that emergent trend — triage what the system is already teaching itself, rather than inventing improvement programs from scratch.

**Mechanism:** `.github/workflows/skill-candidates-review-check.yml` opens the reminder issue on the first Tuesday of each month (it checks the day of the month at run time, because GitHub cron ORs the day-of-month and day-of-week fields). Its `Concept:` line points here.

## Purpose

A recurring, lightweight PM+Exec review of what deserves to become a skill, what should fold into an existing one, and — just as deliberately — what should *not* be built. The don't-build column exists because of PM's don't-overlearn principle (2026-07-08): a process with a long clean track record that failed once under compound exogenous disruption usually needs repair-readiness, not new machinery.

## Proposed cadence

**Monthly**, PM+Exec, ~20 minutes, opportunistically sooner if something hot lands. (Weekly would compete with the Ship rhythm and overproduce; quarterly would let candidates go stale.) Exec maintains this doc between reviews; PM disposes at review time.

## Signal feeds (all already being collected — no new collection needed)

1. **Memory-eval "wanted but not found" buckets** — every role already writes this section at session wrap (per #974). A recurring "wanted but not found" across roles is a skill candidate by definition.
2. **Incident docs** (`docs/internal/operations/*-2026-*.md`) — each one ends with a fix-disposition that is often a skillify-or-not question.
3. **Omnibus "Session Learnings"** — Docs already surfaces repeated improvised procedures.
4. **Exec's synthesis vantage** — repeated ad-hoc patterns visible across role logs during weekly Ship work.

## Triage columns

Every candidate gets exactly one disposition, with reason recorded (so we don't re-litigate):
- **BUILD** — new skill warranted
- **FOLD** — belongs inside an existing skill/procedure; name which
- **DON'T-BUILD** — explicitly declined, with the reason and (where useful) an escalation trigger that would reopen it

## A taxonomy worth applying at creation time (PM, 2026-07-08)

Two distinctions, orthogonal:
- **Generally-usable vs. role-tailored** — some skills any agent could run; others encode one role's specific lane.
- **Who owns it vs. who can run it cold** (the bus-factor axis) — PM's example: Docs wrote the publish skill to formalize a process Docs and PM do together, but any agent could run it in a pinch. This week supplied two live proofs of the value: Exec ran `draft-weekly-ship` when Comms went dark (Ship #049), and again for Ship #050. Skills written for coverage — "who runs this cold if the owner is unavailable?" — earned their keep twice in one week.

Proposed cheap discipline: skill creation asks the bus-factor question at birth, and the frontmatter `scope:` field (already exists — cf. `create-session-log`'s `scope: cross-role`) gets set deliberately rather than by default.

## Current candidates (first-pass triage of 2026-07; disposed 2026-11-06 with cycle 2026-10, see the Review log)

| Candidate | Origin | Exec's lean | Reason |
|---|---|---|---|
| Ship-kickoff window mechanism | Ship #050 window error (7/8) | **FOLD** (into Exec's existing Friday kickoff procedure) | The fix is three lines — compute window from prior Ship +7d, assert Fri/Thu day-of-week, verify push landed. A skill is more surface than the fix warrants; the failure needed a compound outage to occur at all. |
| Workstream-§0 report-writing skill | PM floated it, same discussion | **Two honest options — PM's call** | *Light*: the kickoff memo template carries the computed window verbatim and reports quote it rather than re-derive; add a one-line date-bleed self-audit reminder (the process guide already names date-bleed as the #1 recurring error). Gets ~90% of the value with almost no new surface. *Full*: a thin cross-role `write-workstream-section` skill mechanizing the methodology-25 §0 format + window-quoting + self-audit. Worth it if we see one more windowing/date-bleed error under *normal* (non-outage) conditions — that's the escalation trigger. Five clean prior Ships argue the prose instructions mostly work. |
| Skill-scope/bus-factor audit | PM's taxonomy point | **FOLD** (one-time pass, then it's a creation-time discipline) | Inventory existing skills' `scope:` frontmatter vs. reality; make "who runs this cold?" a standard question in skill-creator guidance. |

### Cycle 2026-10 candidates (gathered 2026-10-23 for #1715, the first review held; DISPOSED 2026-11-06, xian accepted every lean)

The review never ran in September, and that silently skipped October (CIO's fix 7c87c1ceec makes a skip visible from now on). xian's ruling on 10-23: pick up a missed cycle now and put it back on schedule. Signals cover 09-01 to 10-23 from session-log "Wanted but not found" lines, the omnibus logs and the 36 skills, with Exec's own vantage added. Counts are log files that mention the topic, so they overstate chatty topics.

**Status of the three July candidates:**
1. **Ship-kickoff window:** done as a script, not prose. `scripts/ship-kickoff.sh` computes the window and prints `ship-status`. **Lean: close.** **Disposed 11-06: closed.**
2. **Workstream-section skill:** not built. The script now carries the computed window. **Lean: keep the light option.** **Disposed 11-06: light option kept, no skill.**
3. **Skill-scope audit:** 28 of the 36 skills carry `scope:`, so 8 are left. **Lean: finish it** (add `scope:` to the 8, and add "who runs this cold?" to creation guidance). **Done 2026-11-04 15:48 (CIO), on xian's "Yes finish it":** the five `piper-*` product skills carry `scope: product`, so every skill carries `scope:` (34 with a SKILL.md, counted 11-06; the "36" above was the 10-23 gather's count and was already wrong on 11-04). The creation-guidance half was disposed 11-06 (add it, one line) and is done: `SKILL-CREATION-RUNBOOK.md` Step 3.

| Candidate | Signal | Exec's lean | Reason |
|---|---|---|---|
| Each role's "GitHub criteria line" (the third work queue) | Five roles flagged the gap, 09-13 to 10-05 | **FOLD** into `duty-cycle-tick`, or into each role's briefing | It's a missing paragraph since the v1.33 ruling, not a procedure. The tick skill is 107 KB, so prefer briefings. **Disposed 11-06: FOLD into each role's briefing** (2 of 12 essential briefings carry one; each seat adds its own). |
| Seat environment gotchas: no venv in Amber worktrees, ruff and CI venv location, zsh not splitting `$VAR`, BSD `sed`, the mypy pin | The broadest recurrence: 6 roles or more, every week | **DON'T-BUILD**. Write entries in `github-and-tooling-gotchas.md` | It's reference, not a procedure. Reopen if it recurs after the entries are written. **Disposed 11-06: DON'T-BUILD; gotchas entries.** Entries written 11-06 (CIO): `github-and-tooling-gotchas.md`, "Amber seat environment". |
| A read-only alpha or production query path (user counts, keys by provider, unused invites) | About 10 logs across 6 roles | **DON'T-BUILD** a skill. It's a script-and-permission decision (Lead, xian) | The gap is a sanctioned tool. **Disposed 11-06: DON'T-BUILD a skill;** the tool is Lead's and xian's call. |
| Record a ruling of xian's the same hour, and check that a relay landed | Exec logs 09-18 to 10-01; CXO and PPM related | **FOLD** into `check-mailbox` and `duty-cycle-tick` (one prompt line) | CLAUDE.md already routes rulings to decisions.log. What's missing is the prompt. **Done 2026-11-04 15:48 (CIO)** in `check-mailbox` v1.1, Step 5, on xian's "Yes same-hour in check-mailbox" (not in `duty-cycle-tick`). **Disposed 11-04 (done).** |
| A production observation seat, or a live turn against the floor | CXO, 8 days running in September; Web, PA | **DON'T-BUILD** | It's a seat and tooling request. **Disposed 11-06: DON'T-BUILD.** |
| A post-freeze recovery sweep (session alive, cron armed, no turn) | Exec, HOST, PA, Web, 09-17 to 09-26 | **FOLD** into `duty-cycle-tick`'s recovery step | Small. **Disposed 11-06: DON'T-BUILD, superseded** (CIO's change to the lean): the signal came from session crons, and every seat fires from a LaunchAgent since 11-02 (tick v1.62). |
| Deletion and ratchet-sweep discipline (read sweeps whole, score router changes on both tables, run enforcement whole) | Lead, Arch, prog, 09-24 to 10-10 | **FOLD** into `delete-module-safely`, plus a gotchas entry | The existing skill covers deletion. **Disposed 11-06: FOLD into `delete-module-safely`, plus a gotchas entry (Lead).** |
| A browser render-check recipe on alpha (390px, which test account) | Web, PPM, PA, Comms | **DON'T-BUILD** for now | Mostly permissions. Reopen if a second role needs it. **Disposed 11-06: DON'T-BUILD for now.** |
| **Exec vantage:** filing mail (move to `read/`, reset, regenerate, send, verify) and a push loop that stops on a rebase conflict | Exec, many times a day; on 10-23 a push loop read "0 unpushed" in the middle of a conflict | **FOLD** into a script (`scripts/mail-file.sh`, `scripts/push-main.sh`) | It's mechanical and error-prone by hand. A script, not a skill. **Disposed 11-06: done/superseded** (CIO's change): `scripts/push-main.sh` is the push loop (since 08-15, canonical 10-14), and mail v4's `ack` replaces filing for every seat from 11-09. |
| **Exec vantage:** xian's push cards run as one block, with the commit line only after a matching stat | 10-23, a push from a stale clone | **FOLD** into the rollup's card rules (artifact-design or the rollup skill) | One rule. **Disposed 11-06: FOLD into the rollup's card rules (Exec, today).** |

## Review log

### 2026-11-06 (cycle 2026-10, #1715; the September cycle picked up late)
- Candidates reviewed: 13 (10 gathered 10-23, plus the 3 from July). Exec gathered them and put the leans; CIO checked them against the tree on 11-06 and changed two; xian disposed by list, not a walk: "I accept the 12 leans" (10:05, via Exec; decisions.log 10:04). The July scope audit and the same-hour relay were ruled and done on 11-04.
- Dispositions: BUILD 0, FOLD 5 (briefing criteria lines; `delete-module-safely` plus gotchas; rollup card rules; same-hour relay in `check-mailbox`, done 11-04; "who runs this cold?" in the creation runbook, done 11-06), DON'T-BUILD 6 (workstream-section skill, environment gotchas as a skill, query-path skill, observation seat, post-freeze sweep, render-check recipe), CLOSED as already done 2 (Ship-kickoff window by `ship-kickoff.sh`; mail filing and push loop by `push-main.sh` and v4 `ack`). Scope audit finished 11-04 (34 of 34).
- Notes: nothing became a skill. Most signal pointed at a missing line in an existing place, or at a tool or permission, not a procedure. Two leans were stale by the time of the review because the tree had moved (LaunchAgents, `push-main.sh`), which is the case for re-checking leans against the tree before the owner sees them. Next cycle due Tue 2026-12-01.
