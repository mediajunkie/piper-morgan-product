# Exec carry-forward

**STATE: LIVE.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, expires ~09-27, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound.

**Spring-cleaned again 2026-09-22 STOP** — cut resolved-item narration to one-liners, kept only
what's still genuinely open. Full arcs for anything below live in dated session logs, not here.

## Open, real work owed

1. **Belt classification, due Sat 09-27** — CIO's half is a real first pass, not just a plan:
   `scripts/belt-mechanical-reasoning-proxy.py` built and tested, caught and fixed a genuine 20x
   confound (967 fire-zero-incident heartbeat commits inflating CIO's own mechanical count) before
   reporting a number. Current table (incident window excluded): arch 0.63, cio 0.72, comms 0.75,
   cxo 0.60, docs 0.92, exec 0.80, host 0.78, lead 0.82, pa 0.79, ppm 0.55, web 0.66 (substantive
   ratio). **Confirms the atypical-week caveat hard**: 43% of all commits in the 4-day window came
   from one incident. Open question CIO raised: widen the window past this week, or keep it and lean
   on the caveat — my call to make when I do my own half. **My half (session-log reading) not
   started yet.**
2. ✅ **mcp.pipermorgan.ai assignment — RULED 09-23.** PM approved PA's recommendation directly
   (reuse this week's PM+Pard scoped-grant pattern). `decisions.log` entry written. Closed.
3. **Duty-cycle standard cascade — still waiting on PM's word.** All three declarations in.
   Full context PM asked for, since the rollup card was too thin to decide from: session-scoped
   crons (`CronCreate`) are documented as ephemeral by design — die with the session, auto-expire
   at 7 days — which is the root cause behind a whole week of things I've personally had to manage
   by hand (offset drift, 7-day rotations, the Gap-C compaction-kills-cron incident). The proposal
   replaces that with OS-level LaunchAgents that fire independent of any session's lifetime — a
   stronger "not-failing" guarantee instead of "detect-and-heal." Concrete cost: ~2h Pard's time,
   all 11 seats, reversible per seat with one command, doesn't change *when* anything fires or touch
   the worktree/push-to-main/mail layer. CIO (who owns the mechanism being replaced) recommends it;
   Klatch already adopted independently. If it lands: retire my own manual cron-rotation ritual from
   `duty-cycle-tick`'s text same day — don't let the old prose become its own accretion.
4. ✅ **STALE, corrected 09-23 — this was never mine.** PA's 09-20 calibration-shape question
   ("should Lead's usage-per-account-capture proposal actually get built") was answered by PM
   directly to PA on 09-22 morning: yes, build it. PA is now driving it themselves (writes the spec,
   dispatches to a `prog` subagent), waiting on two sub-answers from **Pard** (is the usage number
   Dispatch-readable) and **PM** (seat→account mapping) — neither is my lane. Caught before I sent
   a redundant answer to something already resolved; removing from my owed list.
5. **Ship #061** — publishes TODAY (Wed 09-23) per Comms' approval.
6. **Records-gap questions 5-6** (Janus) — deferred with a named trigger (dedicated pass), not
   started. Q1-4 already answered by Docs and relayed.
7. **#1744 (ruleset) — real finding, relayed to Arch/Lead/Pard 09-23.** PM created the new ruleset
   directly (Repository Admin bypass, exact-match on `refs/heads/main` only — verified via API, does
   NOT cover `main-old` despite how the UI copy read to PM). **`main-old` genuinely has 503 commits
   not in `main`** — checked directly, not assumed; PM's uncertain memory that it might carry
   unmerged content was correct. Recommended: safe to delete the classic protection rule on `main`
   now; do NOT touch `main-old` until someone reviews those 503 commits. Not mine to execute — Arch/
   Lead/Pard's, PM believes Lead owns #1744.
8. **PM stays ahead on publishing** — tomorrow's post queued, Saturday's being illustrated now.
   No action needed, noted for continuity.

## Context-floor plan — still the standing top priority, real progress this week

Four items, wide movement across 5+ roles (Docs, CIO, Lead, PPM, Web all shipped or correctly
declined work). **Only genuinely open piece**: CIO's own BRIEFING-CURRENT-STATE.md entry and Docs'
two are still unreviewed; Web's tick-skill pilot (Phase B) continues watching, clean through day 1;
Lead opting into the registry-trim tool at tonight's STOP. **Scheduled-clear cadence with Pard is
STILL UNCONFIRMED** — separate from the (fixed) hook-recursion incident, don't let today's other
progress read as covering it. Full detail: `docs/internal/operations/context-floor-reduction-
plan-2026-09-21.md` + this week's session logs.

## Standing PM-gated, unchanged

- **The ruleset decision** (parks Arch/CXO) — blocked since 09-16, two enforcement surfaces exist,
  question is which should own it. `decisions.log` 09-16.
- **Vercel storage** — raised to PM 09-22, I can't check it myself (no CLI/token/dashboard).

## Resolved this week, no longer tracked in detail (see session logs for the full arc)

- ✅ Model-tier question (Sonnet is the intent, RULED 09-21).
- ✅ Runaway hook incident (both root causes fixed, tested; re-arm is Pard's call, not blocking).
- ✅ Hosting migration — **COMPLETE**. alpha.pipermorgan.ai on Fly, zero data drift, path A revoked.
  Post-cutover deploy path ruled Lead's (§4e, pipeline plan v0.3). #1850/#1852 filed, non-urgent.
- ✅ **Usage crisis — CLOSED 09-23 ~11:5x.** Wall hit, PM applied the one-time reset, full week's
  credit restored. Fleet closure notice sent. Don't-self-throttle + context-floor-top-priority both
  stand as before — neither was contingent on this. ⚠️ **Observed at the same moment: this seat's
  model changed Sonnet 5 → Fable 5, unannounced** — flagged to PM as observed-not-chosen per this
  week's tier-change discipline; awaiting PM's word on whether it was intentional.

## This seat's standing errors (deduplicated, keep watching)

- **Verify the artifact the instrument reads, not the one you edited** (`sync-pm-local.sh`).
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **Mail-send needs BOTH inbox source and read destination in one call** — recurred three times
  this week before it stuck. Verify with `git ls-tree origin/main`, not a clean exit code.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`, written via manual `git -C` there, verified via `git log origin/main -1` in *that* repo.
  Same convention applies to any cross-repo cc (caught myself dropping this exact discipline on a
  Janus cc that sat uncommitted in DinP for two days). Adopt `reply-to:` frontmatter on anything
  leaving this repo. ⚠️ **PM told PA directly (09-23) to write to Pard's real inbox themselves
  rather than route through Exec-as-relay** — a live exception to the documented default. Worth
  watching whether this becomes the general rule or stays PA-specific; not mine to decide, just
  tracking that it happened.
- **Don't write a decision brief on another role's surface without them reading it first.**
- **A park without a computed deadline is not falsifiable.**
- **Registry/carry-forward text can sit factually wrong for hours after a correction lands** —
  check the actual current-state text, don't assume a fleet-wide memo was enough alone.
- **zsh does not word-split `$VAR`** — build path lists as arrays.
- **`closedAt` is UTC** — compute in Pacific and say which timezone.

## Also live, lower priority

- **Weekly reflection proposal** with CIO — must ride an artifact with a live reader.
- **Memory export cadence** — open question with CIO: event or schedule.
