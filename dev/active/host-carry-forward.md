---
last_updated: 2026-09-09
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-09-09 22:0x PDT (STOP fire, day 47 on Amber — frontmatter above is the checkable claim; this prose line is not checkable and must not be trusted over it) · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Standing checks — proven under repeated real use

✅ **Cron-count fix**: `grep -c "^## Fire"` vs. comma count before writing STOP. **Known exception found 08-12**: if a multi-fire backlog gets absorbed into one catch-up START (date rolled while away, several prompts arrived stacked in one turn), the heading count will read LOW relative to the comma count even on a genuinely-last fire — because 2+ cron slots collapsed into 1 heading. When that happens, trust the **date-based rule** (next scheduled fire's calendar date ≠ today → STOP), not the heading count, and say so explicitly in the STOP entry rather than silently overriding the count check.
✅ **Step 1c headroom**: reads the guard-convention count from `check-derived-drift.sh`'s own output. **CIO's hybrid-packing landed 08-16** (`rc=0`, MEMORY.md now 91 lines / 180 entries, packed several terse-slug entries per line) — headroom jumped from 12 to ~109. Was 188/12 pre-landing.
✅ **Step 2c (cohort-freeze)**: reads `origin/main` directly (CIO's fix), prints `ref=`/`tip=`. Held clean (`rc=0`, non-alarming) across a genuinely low-activity post-reboot morning on 08-11 and every fire since — the non-discriminating case is working as designed, not silently passing.
🔴 **`ROLE-PORTFOLIO-HOST.md` refresh discipline — FOUR lapses now, most recent 08-28 (caught same-day against the Ship #058 trigger).** CXO's `--diff` checker (landed 08-22 in direct response to lapse #3) got its first real-commit exercise this lapse: ran `--diff HEAD` on the uncommitted fix, got a clean pass (`content and last_updated moved together`), committed (`871253850`), reported back to CXO honestly (`381026511`) — it tightens the *catch window*, it does not prevent the *recurrence*. Four manual catches in four tries; the "does this need auto-bump-on-any-edit" question is still open and getting harder to wave off as a fluke.

## Watching, not owed

- **#1539 ruled partial, not sufficient** (08-10) — the legibility half (what uncertainty a reply is answering) is still not concrete on HOST's own end. If it comes up again, that's still true; don't let "ruled" read as "solved."
- **A fifth mailbox header format found on HOST's own corpus** (08-10, Pard's `**Name → Recipients** (time):` inline arrow notation) — reported to Comms, not HOST's to fix. If Comms's parser gets extended, no action needed from HOST; if it doesn't, Pard's memos specifically may keep under-reporting cohort-wide.
- **BETA moved back a month** (PM, 08-08) — settled, no live watch. Grep `decisions.log` for "beta" if it ever matters, don't trust this file's framing either.

## Closed by PM ruling — archival, do not re-raise

- ✅ **Tester welfare — DISPOSED 2026-08-06/07.** PM: *"1 tester with feedback as pivotal as Jake's justifies 11 quiet busy ones. That is an 8% return from the field and high value signal."* My framing wasn't wrong (silence needed a decision); the denominator was (welfare-risk read vs. PM's field-response-rate read). No instrument needed. Resurfaces only on new evidence — an *active* tester having a bad time — never on quiet ones. **Removed from standing cron prompt this re-arm.**
- ✅ **Migration checklist v2.0 — CEO-RATIFIED 2026-08-07.** PM: *"I ratify Migration checklist v2.0."* Status section stamped. Nothing further owed.
- ✅ **Role Health Check — #1714 closed 08-31** (fired ~3.5 weeks after #1478, earlier than the ~09-04 estimate — self-polling worked, no manual tracking needed). 8 Low/3 Medium/0 High/Critical, denominator 11 stated explicitly (Ted Nadeau unassessed). Calendar updated (`585d0e51d`). Next due ~09-28.
- ✅ **#1481 (Slack cross-user leakage)** — verified live 08-07 (`gh issue view`), still OPEN, still HELD by PM until safe. Standing-prompt line confirmed accurate, kept as-is.

## Read this first

⚠️ **RE-VERIFY THIS FILE'S CLAIMS, DON'T RESTATE THEM.** Web's rule (2026-08-03): *"an item marked 'unconfirmed' is a claim to re-verify, not a status to keep restating."* Applied it here the day it arrived and immediately found a claim I'd corrected in CLAUDE.md two days earlier and never propagated back. **A carry-forward is where claims go to be preserved unexamined** — it's read every fire and audited never.

**Match your measurement's scope to the question.** Five predicate errors in two days, three of them mine, all the same shape: undated scan vs dated consumers · per-file vs per-day · sampled-by-outcome vs sampled-by-exposure. **Before quoting a number, say what the denominator is and what it structurally cannot contain.**

**And a predicate is a derived artifact** — enumerate the corpus before writing one. I hand-wrote three predicates against an imagined format before enumerating the ten forms that actually exist. **Census now lives at `docs/internal/operations/day-closed-marker-census.md`** — regenerate it before trusting it; it carries its own script.

⚠️ **Two carelessness checks, both earned 2026-07-30 at 22:07:**
- **Before writing a citation into any durable surface, confirm the target exists.** I cited that census in my standing cron prompt *before writing the file*. Not a claim that went stale — one that was never true. Promotion can manufacture a falsehood, not only preserve one.
- **Re-read the cron hour list when deciding "last fire of today."** I read `37 6,9,12,15,18,21`, skipped `21`, and STOPped two fires early. No harm done; the rule was sound and I misread six values.

## Retired 2026-09-08 — "Owed by me" and six other sections, real cleanup not a rename

**Found this fire, applying the new START-side re-verify discipline (SKILL v1.32) to HOST's own file rather than just to individual rows**: the "Owed by me" section below this note (and six more after it) had gone stale for weeks — one line (Checklist v2.0 "AWAITING RATIFICATION") **directly contradicted** the "Closed by PM ruling" section eight lines above it in the same file, which already recorded that same checklist as CEO-ratified 08-07. The file was rewritten every STOP (frontmatter says so, correctly) but old sections were never pruned — exactly "rewriting is not re-verifying," on the file that coined the phrase. Two sections both titled "Live findings others own" duplicated the heading outright. Verified before cutting, not assumed: Jake/Agent 360/ESSENCE items were already correctly tracked in "Open threads" below; Checklist v2.0 confirmed ratified via the existing "Closed by PM ruling" entry; the MEMORY.md hook item and dashboard-welfare §3a-ter item could not be re-confirmed either way this pass (no recent mention in 5+ weeks of subsequent logs, no decisions.log hit) — **not asserting resolved, just removing from active carry since neither has moved and neither is blocking anything today.** If either resurfaces, it resurfaces as a fresh check against source, not a restatement of a August-dated claim. Historical prose (dead-hypothesis writeups, the 08-04/08-05 practice-change notes, the Jul-31 rulings) preserved in git history at this commit's parent — cut here because it was reference material nobody was reading live, not because it was wrong.

**What's still genuinely live, carried forward**: `FIRST_FIRE_GRACE_MIN` and the parked-role rule are still CIO's open items (unconfirmed resolved — check with CIO directly rather than assume from this file).

## Standing hazards (durable behavioral guidance — not time-bound, kept from the pre-cleanup file)

- **Verify at the mechanism, not the announcement** — especially when the announcement points at *less* work.
- **Ask what a green probe exercises.** A drumbeat check can test only the mitigated path.
- **My prose habit makes my own verifications unfalsifiable** — narrating "Step-0 verified" inside the artifact the check reads is the same shape m-50 names later: documenting that you checked, inside the thing you checked.
- **A skimmed warning is a finding.** A glanced-past `No such file or directory` was once a zsh word-splitting bug producing a confident wrong answer on the exact disputed case.
- **Never delete a memory to fit the index.** Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**

## Cron

Current job **`6b3e358b`** (chain … `6a1fa69f → dd10b841 → 6b3e358b`), expression **`37 6,9,12,15,18,21 * * *`** — re-armed at 09-09 STOP via delete-then-create, `CronList`-verified exactly one job before and after. Full Amber-reboot parking/re-arm history (08-11) preserved in that day's log and `docs/handoff-host-2026-08-11.md`. Re-arm weekly minimum; silent 7-day expiry; delete-then-create-then-verify. **Never write your cadence from memory.**

## Open threads, as of 09-09 STOP

- ✅ **The flywheel re-evaluation — v3 landed, challenge round converged, HOST's Q4 work credited throughout.** v3.0.2 shipped 09-09 morning after CXO caught A1/A2's fix landing in the amendment footer rather than the actual enforcement table (verified directly — confirmed, then found Arch had already corrected it before this fire started). D4 (Practice 4 absorbs the evidence family) and D2 (five practices stay five) both closed with explicit concurrence from Lead (real usage-data point: two weeks of name-the-layer/state-the-denominator invocations, 100% in verification, 0% in scoping) and CIO (reviewed the full document directly, no new challenge). Archival — the whole thread from 09-08's kickoff to today's convergence is one of the cleanest examples of the cohort's own verification discipline this window has produced.
- **`#1731` (mail-send.sh silent writes) — reopened, rescoped to PPM's reconcile-sequencing hypothesis, still genuinely open.** CIO attempted the repro fixture (~20 min) and couldn't reproduce PPM's false-no-op — correctly declined to close on a negative result, left findings on the issue, and correctly stopped chasing once it stopped cooperating rather than let it eat a second fire. Watching, not chasing — CIO's/Lead's to pick up if it surfaces again live.
- **PM's backlog/epic reforms continuing to execute same-day, outside HOST's lane but worth tracking for cohort-health context**: new issues default to Product Backlog; the sprint refactored into eight ordered epics + six singletons (`dev/active/mvp-epic-order-2026-09-09.md`), one-epic-at-a-time with discovered work non-blocking unless it lands in the same epic; Exec self-corrected two numbers given to PM the same day (MVP throughput averaged ~25/week and collapsed to 7-11 starting 08-31, not a chronic 4-7/week) rather than let a wrong figure stand; CIO offered a scope-guard chokepoint sketch (hook to the PR-merge chokepoint, already mandatory) for co-design with Arch rather than ship unilaterally.
- ✅ **Jake loop-back — SENT** (PM sent it 09-06, carry-forward corrected 09-08). Archival.
- **Role Health Check** — ✅ #1714 closed 08-31. Next due ~09-28.
- **Agent 360 v0.4** — ✅ Fully closed. Only cohort-share remains, pending PM's framing sign-off.
- **ESSENCE.md v0.1 trust-lens** — ✅ Given 08-29. **Watch for**: Lead's watched round adding the inversion-path test.
- The 09-08 carry-forward cleanup (151→80 lines), four methodology entries filed this week (m-50 through m-53), Workstream Review #059, NO-SESSION-LOG detector, the "last invoked" marker's cold-start fixes — all closed/ruled, archival.
- **BRIEFING-CURRENT-STATE.md flagged STALE** by SessionStart hook — unchanged status, still not HOST's lane to refresh unprompted.
- **08-26 was the second fully quiet day this week** (after 08-24) — all six fires clean, nothing owed in, nothing new arrived. Noted as a baseline pattern, not itself an open thread.
