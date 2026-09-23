# Exec carry-forward

**STATE: LIVE.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, expires ~09-27, re-armed delete-then-create
at each STOP. ⚠️ **Offset is per-job and re-rolls on every create** — use the documented bound.

**Spring-cleaned again 2026-09-22 STOP** — cut resolved-item narration to one-liners, kept only
what's still genuinely open. Full arcs for anything below live in dated session logs, not here.

## Open, real work owed

1. **Belt classification, due Sat 09-27** — joint pass with CIO (mechanical-vs-reasoning per seat),
   feeding Lead's Opus 5.5 trial starting 09-28. CIO confirmed, will bring registry/heartbeat data;
   I bring session-log reading + correction/retraction proxy. **Not started.** Caveat both of us
   already flagged: this week is atypical (migration, incidents, usage crisis) — don't let it
   become the baseline silently.
2. **mcp.pipermorgan.ai assignment** — PA's proposal is in (reuse this week's exact PM+Pard scoped-
   grant pattern, not Arch supervising a fresh instance); I relayed to PM agreeing with PA's
   reasoning. **Waiting on PM's decision.**
3. **Duty-cycle standard cascade** — all three declarations in (Klatch adopt-with-exception, DinP
   adopted, my read = adopt, both my confirmations answered satisfactorily). **PM's word is the
   only thing left to close it.** If it lands: retire my own manual cron-rotation ritual from
   `duty-cycle-tick`'s text same day (CIO's offer, Pard confirmed) — don't let the old prose become
   its own accretion.
4. ✅ **STALE, corrected 09-23 — this was never mine.** PA's 09-20 calibration-shape question
   ("should Lead's usage-per-account-capture proposal actually get built") was answered by PM
   directly to PA on 09-22 morning: yes, build it. PA is now driving it themselves (writes the spec,
   dispatches to a `prog` subagent), waiting on two sub-answers from **Pard** (is the usage number
   Dispatch-readable) and **PM** (seat→account mapping) — neither is my lane. Caught before I sent
   a redundant answer to something already resolved; removing from my owed list.
5. **Ship #061** — publishes TODAY (Wed 09-23) per Comms' approval.
6. **Records-gap questions 5-6** (Janus) — deferred with a named trigger (dedicated pass), not
   started. Q1-4 already answered by Docs and relayed.

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
- ✅ Usage crisis — PM will use the one-time full-week reset once the wall hits (likely tomorrow AM).
  **Fleet-wide directive sent**: do not self-throttle or postpone work; context-floor plan stays top
  priority regardless. Separate fact from Janus: DinP/Klatch run on a different account
  (designinproduct.com) — no shared headroom with pipermorgan.ai either way.

## This seat's standing errors (deduplicated, keep watching)

- **Verify the artifact the instrument reads, not the one you edited** (`sync-pm-local.sh`).
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **Mail-send needs BOTH inbox source and read destination in one call** — recurred three times
  this week before it stuck. Verify with `git ls-tree origin/main`, not a clean exit code.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`, written via manual `git -C` there, verified via `git log origin/main -1` in *that* repo.
  Same convention applies to any cross-repo cc (caught myself dropping this exact discipline on a
  Janus cc that sat uncommitted in DinP for two days). Adopt `reply-to:` frontmatter on anything
  leaving this repo.
- **Don't write a decision brief on another role's surface without them reading it first.**
- **A park without a computed deadline is not falsifiable.**
- **Registry/carry-forward text can sit factually wrong for hours after a correction lands** —
  check the actual current-state text, don't assume a fleet-wide memo was enough alone.
- **zsh does not word-split `$VAR`** — build path lists as arrays.
- **`closedAt` is UTC** — compute in Pacific and say which timezone.

## Also live, lower priority

- **Weekly reflection proposal** with CIO — must ride an artifact with a live reader.
- **Memory export cadence** — open question with CIO: event or schedule.
