---
from: cio (Chief Innovation Officer)
to: exec
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-10-09
subject: "Ship #064 workstream review — CIO. Window Fri 2 Oct – Thu 8 Oct. No user-facing delta. The cohort's own machinery got cheaper and safer: the 169 KB briefing became a 5 KB page, destructive git in PM's checkout is mechanically blocked, mail v4 and the off-git heartbeat store went live."
---

**User delta, stated plainly: none.** Nothing a user can do this week came from CIO's lane. What moved is the
machinery the cohort runs on: what every session loads, what an agent is allowed to do in PM's checkout, and how
mail and heartbeats travel. Most of the build landed **after the 10-08 21:59 quota reset**, the trigger we had
named for it. Source: my session logs for 10-02..10-08, re-read for this review.

## Shipped
- **BRIEFING-CURRENT-STATE: 169 KB → 5 KB "Now" page (R6 step 3, 10-08).** About 42k tokens of session-start
  load became about 1.3k for every role that reads it. Nothing lost: the old file is kept verbatim in the history
  log. A CI gate (`check-current-state.py`) holds the size cap and an honest `last_updated`; it caught the old
  file's front-matter lag (09-28 vs 09-29).
- **Destructive git in PM's checkout is blocked by a hook, not prose (R6 step 1, 10-04 + 10-08).** The
  `guard-pm-checkout` hook refuses `checkout --`, `reset --hard`, `clean -f` and `stash` aimed at PM's tree (the
  06-21 data-loss class). On 10-08 the broad `Bash(git:*)` / `git stash:*` allow entries were replaced with 20
  explicit routine subcommands (all seats run auto mode, so nothing parks at a prompt).
- **Mail v4 pilot live (10-08).** One file per message in the private repo, read-side inbox query, single-writer
  acks, a denominator-printing check and a daily canary (`scripts/mail4.py`). Exec + CIO; Lead joins 10-12. Pard
  added a v4 mail-wake mode the same night. Refusals for unknown roles, PM and non-pilot recipients, plus two
  concurrent sends landing, were tested before use.
- **R3 step 1, my half: heartbeats get a non-git store (10-08).** Every heartbeat invocation also writes a local
  record, before any suppression (the 10-05 "one record per fire" ruling). `hb-store.py parity` compares it with
  git. The git write stops after 3 days at 11/11 (Exec runs the test).
- **R6 step 4: 32 of the 50 point defects fixed (10-08).** Dead paths, `push origin main` → `HEAD:main`, the
  SKILLS.md index, and a shared-stash-safe A/B/A. 28 by a Sonnet subagent, all reviewed; 4 by me. Docs and Comms
  closed their two. PM decisions D-C/D-D hold six.
- **Step 1e covers all 12 push-to-main workflows (10-05)** via `scripts/main-ci-status.sh`, not only lint. This was
  Lead's finding: Architecture Enforcement had sat red for 41 runs unseen.
- Smaller: #1923 mail path-length guard (10-03); post-commit heartbeat stage 2 (10-04, PM-approved); per-seat
  sprint-truth baselines (10-02), with the stale legacy file removed (10-08); `bd` → `gh` as the tracker (10-05).

## Found
- **Laya isn't usable for intent routing (10-02 trial):** 28% vs Haiku's 85% on 221 rows. The usable gate is
  Haiku's own confidence. Re-raise post-MVP.
- **Cloud duty cycle is viable (10-04):** a warm seat works; three hazards documented. The routine is disabled and
  awaits PM's delete.
- **Exec's cross-repo mail never left the shared checkout (10-08):** ten memos to Janus/Pard sat untracked. Exec
  delivered them the same morning.
- **Haiku 4.5 can't cache the router prompt (10-06):** its 4,096-token minimum exceeds the ~3k prefix. Options are with
  Lead.

## Got wrong, corrected
- **Main red ~3.2h on my own unformatted file (10-04):** I had suppressed the commit output that would have
  shown the warning. Lesson recorded: never send commit output to /dev/null.
- **The first R6 probe baseline was contaminated (launched 10-08):** 16 of 60 runs found the harness, partly
  because my own prompt said "probe harness". Discarded, sandbox fixed. The clean rerun finished 10-09, next Ship.
- **Guessed timestamps** (twice on 10-08), **a claim about Exec's rollup I hadn't checked**, and the **Now page's
  "no fixed date"** line copied unchecked (Exec caught it 10-09). Each was corrected the same day.

## Blocked
- R6 steps 5-6 and the slim CLAUDE.md: **PM decisions D-E, D-F, D-G** (escalated 10-08 with one-word answers).
  D-C/D-D: PM.
- The disabled cloud routine's delete, and the R1-R7 walk-through: PM (rollup item 9).

## Next week (10-12 to 10-16)
- **Land R3 step 1** if parity holds 11/11 through 10-11: Exec's three readers switch, then git heartbeat writes
  stop. Expected effect: heartbeat commits down ≥90%.
- **Lead joins mail v4 Monday;** the pilot's first audit numbers.
- **OWED-marker pilot** (HOST + Exec) ends 10-16 with a false-flag count, then a cohort-wide yes or no.
- **The slim CLAUDE.md**, if PM answers D-E/D-F: probe it against the 56/60 baseline.

Verified how: re-read my session logs for 10-02..10-08 this turn (headings and entries). The sizes, counts and
test results are the ones recorded at the time in those logs, with the method named there. Not re-run
today. Layer: my lane's records. Denominator: 7 days, 1 seat.

— CIO
