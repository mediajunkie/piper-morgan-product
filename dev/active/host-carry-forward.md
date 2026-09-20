---
last_updated: 2026-09-19
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-09-19 22:0x PDT (STOP fire, day 57 on Amber — frontmatter above is the checkable claim; this prose line is not checkable and must not be trusted over it). · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Standing checks — proven under repeated real use

✅ **Cron-count fix**: `grep -c "^## Fire"` vs. comma count before writing STOP. **Known exception found 08-12**: if a multi-fire backlog gets absorbed into one catch-up START (date rolled while away, several prompts arrived stacked in one turn), the heading count will read LOW relative to the comma count even on a genuinely-last fire — because 2+ cron slots collapsed into 1 heading. When that happens, trust the **date-based rule** (next scheduled fire's calendar date ≠ today → STOP), not the heading count, and say so explicitly in the STOP entry rather than silently overriding the count check.
✅ **Step 1c headroom**: reads the guard-convention count from `check-derived-drift.sh`'s own output. **CIO's hybrid-packing landed 08-16** (`rc=0`, MEMORY.md now 91 lines / 180 entries, packed several terse-slug entries per line) — headroom jumped from 12 to ~109. Was 188/12 pre-landing.
✅ **Step 2c (cohort-freeze)**: reads `origin/main` directly (CIO's fix), prints `ref=`/`tip=`. Held clean (`rc=0`, non-alarming) across a genuinely low-activity post-reboot morning on 08-11 and every fire since — the non-discriminating case is working as designed, not silently passing.
✅ **Step 5b self-verification (v1.34/v1.35, since 09-12)**: `scripts/duty-cycle-freeze-check.sh` (full output, not just an own-name grep) after every heartbeat — no alert line = the step ran and produced a measured absence, not an unmeasured one (the `rows=N` denominator check landed in v1.35 same day CXO found the gap). Run clean every fire since.
✅ **Armed ≠ firing, checked and already conforms (09-13)**: cohort-wide finding (Exec/Lead, from Lead's 12-dark-hour auth-outage gap) that `CronList` returning a job proves a schedule is *armed*, never that fires are *landing*. Grepped HOST's own session-log wording across four days — never claims schedule-liveness from `CronList` alone, always runs `duty-cycle-freeze-check.sh` separately as the actual liveness measurement. No change needed; noting the pairing is deliberate, not incidental.
✅ **Compound git-add-bypass bug, checked and already conforms (09-13)**: `git add X && git commit` in one Bash call bypasses PreToolUse hook detection (the hook reads an empty index before `add` runs) — found on `pre-commit-broad-staging-warn.sh`, same mechanism as July's `check-branch.sh` finding. HOST's own commits have used a separate call for stage vs. commit all session; verified from direct review of this session's own tool-call sequence, not assumed from habit.
✅ **Holding a ratified bar against a recommendation to lower it — proven under real stakes (09-14)**: when Arch (the bar's own author) recommended lifting the #1810 invite hold on evidence one layer short of PM's ratified "observed, not merged" condition, held the line rather than defer — verified the gap directly, stated the position to PM, and offered a concrete cheap unblock instead of an indefinite block. Six hours later the actual observation existed and Arch credited the line-holding directly: "the person who sets a bar is the worst-placed person to decide it can be skipped this once." The mechanism that made this possible: independently verifying claims (a grep, a `git merge-base`, a `gh issue view`) rather than accepting a colleague's summary, even a trusted one, on a decision with real consequences for a real person.
✅ **Re-held on the SAME tester within nine hours of clearing, and cleared again the same day (09-15)**: when a fresh discovery (#1814) re-opened the exact risk HOST's own added condition had created, re-held the invite as the first action of the fire, before any other work; cleared again four hours later on genuinely-driven evidence (a real 401, not a pin), independently verified via `gh issue view` and a direct code read of the adjacent #1816 finding rather than assuming it either blocked or didn't. Two full hold/clear cycles in 24 hours on one real person, every step independently checked.
✅ **Heartbeat push-race, diagnosed not retried blind (09-15)**: `scripts/duty-cycle-heartbeat.sh` failed loud ("Investigate now") on a normal non-fast-forward race; confirmed the loud-failure design was intentional (grepped source) rather than assume a bug, then merge+retried — landed clean. Arch independently reported the same transient firing on their own seat minutes later, cross-validating it as a shared push-race artifact rather than a HOST-specific fault.
✅ **The 09-16/17 standdown saga, fully resolved and archival.** A ~39-hour gap with no scheduling turn during a cohort-wide PM-directed standdown (real, independently confirmed by Web's parallel gap) — HOST initially mis-stated one supporting detail (claimed the registry row was "never parked"; it genuinely was, and HOST's own catch-up STOP correctly cleared it per documented v1.17 behavior). Corrected in both places the wrong claim had landed (carry-forward + registry row text) after verifying Exec's per-commit trace directly. **Two durable lessons carried forward**: (1) a session-scoped cron surviving a directive doesn't prove the directive was followed — only a turn to read the mail does; (2) a `git log -p` skim is not a per-commit trace — when a claim is about what changed between two specific points, `git show` those two commits directly rather than infer from a scroll.
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

Current job **`e018f052`** (chain … `db3710ca → bc447bf5 → e018f052`), expression **`37 6,9,12,15,18,21 * * *`** — re-armed at 09-18 STOP via delete-then-create, `CronList`-verified exactly one job before and after. Full Amber-reboot parking/re-arm history (08-11) preserved in `docs/handoff-host-2026-08-11.md`. Re-arm weekly minimum; silent 7-day expiry (~09-25); delete-then-create-then-verify. **Never write your cadence from memory.**

## Open threads, as of 09-18 STOP

- 🛑 **Janne Lammi's invite — PM-DECIDED HOLD, still in force, 09-20 ~15:4x PT state (compressed
  from the 09-19/20 chain — full history in the roster, main checkout, and
  `dev/2026/09/19/...`/`dev/2026/09/20/...` session logs if the chain itself ever matters).**
  Current position: alpha (`alpha.pipermorgan.ai`, the DO droplet) is now upgraded to `v0.8.12.0`
  (Lead, 09-20 morning, verified live — blue-green, backup, rollback path, genuinely solid work),
  closing the stale-billing-semantics risk that drove the original hold. **But the hold does NOT
  lift on deploy-health alone** — HOST's own established bar for THIS invite (09-14, 09-15,
  reapplied 09-20) requires an actually-driven BYOC flow (signed-in user, own stored key, real
  network call, a real 401 proving selection-and-transmission), never just a deploy check, and that
  layer has never run against alpha specifically. **In flight now**: Lead mints a throwaway
  test-burn invite token and drives the full real path (register → store key → substantive turn) —
  stronger evidence than the 09-14/15 method since it also exercises the registration gate. HOST
  verifies independently once Lead reports, same discipline as both prior lifts. **Separately**:
  PM asked to run one read-only DB check themselves (the #1599 admin-grant gap on their own alpha
  account) — HOST declined to run it (would cross HOST's own "never touches the DB" line), Lead
  can't either (would see identity data), so it's PM's alone. **Scope stays wider than just this
  invite**: PM's separately tasked Arch with a full deployment-pipeline design (stated top
  priority, driven by cost — the droplet was superseded by July's Fly cutover and PM's been paying
  for a dead box ~2 months) and Pard with the immediate archaeology/unblock thread. HOST watches
  both, drives neither. **What would actually move this forward next**: Lead's token-drive report
  landing in HOST's inbox — that's the next real decision point, not a status check.
- ✅ **Amber-restart handoff doc filed** (`docs/handoff-host-2026-09-18.md`, 09-18) — gate-blocking cohort requirement, met same-day. Archival unless the restart itself surfaces something HOST needs to act on.
- ✅ **Sprint closeout for Sep 11–17 filed** (09-18, to Exec cc PM). Archival.
- ✅ **Registry-parking asymmetry corrected cohort-wide** (09-18): only the owning session may un-park its own row; anyone may park any row. Archival, but worth remembering if a similar central-action temptation arises.
- ✅ **Fourth STALE-belt cause proposed and agreed** ("session alive/armed, no scheduling turn") — CIO will fold into `duty-cycle-freeze-check.sh`'s header on next real touch, not urgent. Archival on HOST's side.
- **Classifier bucket-split (the `auth` error bucket, `_classify_llm_error`) — ruled and copy drafted as of 09-15, status still unknown.** Not HOST's to build; check for movement.
- **`#1731`** — CIO's instance retracted; **PPM's separate instance remains open.** Watching only.
- **PM's backlog/epic reforms** — outside HOST's lane, tracked for context only.
- **Role Health Check** — ✅ #1714 closed 08-31. Next due ~09-28.
- **Agent 360 v0.4** — ✅ Fully closed. Only cohort-share remains, pending PM's framing sign-off.
- **ESSENCE.md v0.1 trust-lens** — ✅ Given 08-29. **Watch for**: Lead's watched round adding the inversion-path test.
- **BRIEFING-CURRENT-STATE.md flagged STALE** by SessionStart hook — unchanged status, still not HOST's lane to refresh unprompted.
- **Weekly reflection section (Exec's proposal, CIO-ratified 09-18)** — a ~150-word subjective reflection now rides the sprint-closeout template. HOST's next closeout should include it.
