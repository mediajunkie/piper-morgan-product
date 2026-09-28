---
last_updated: 2026-09-26
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-09-27 19:1x PDT (STOP fire, day 65 on Amber — frontmatter above is the
checkable claim; this prose line is not checkable and must not be trusted over it). · **Worktree**:
Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

**Today (09-27)**: the quietest day this week — three fires, every freeze-check reading fully
clean (no flags at all), two of three mail loops genuinely empty. Two MEMORY.md drift flags, both
verified and folded in: a new memory (a real, three-role-independent UTC/Pacific issue-bucketing
bug) and a corrected existing one (`reference_dispatch_agent` — the mail folder is a real git repo
needing commit+push, not exempt; cost two real 8-day/6-day delivery delays before being fixed).
Comms' Agent 360 v0.5 response landed (5 of 10), deliberately held for real material — a clean
demonstration of the fielding process's own pacing working as designed.

⚠️ **TOMORROW (Monday 09-28) IS THE LAST DAY OF THE THROTTLE** — restore `37 6,9,12,15,18,21` at
tomorrow's STOP fire unless Exec/PM sends an explicit lift signal sooner. **If this file still
shows a throttled cron past Monday, the restore was forgotten — check it.** This file stays
current-state-only per the 09-22 spring-clean discipline.

## Standing hazards (durable behavioral guidance, not time-bound)

- **Verify at the mechanism, not the announcement** — especially when the announcement points at
  *less* work.
- **Re-verify carried claims, don't restate them.** An item marked "unconfirmed" or "watching" is
  a claim to re-check against its actual source, not a status to keep copying forward.
- **Match your measurement's scope to the question** — before quoting a number, say what the
  denominator is and what it structurally cannot contain.
- **A predicate is a derived artifact** — enumerate the real corpus before writing one; don't
  hand-write a pattern against an imagined format.
- **Never delete a memory to fit the index.** Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**
- **Never write your own cadence from memory** — read `CronList` / the registry row live.

## Cron

⚠️ **THROTTLE ENDS TOMORROW (Monday 09-28) — RESTORE AT TOMORROW'S STOP.** Current job
**`647c1762`**, expression **`37 6,12,18 * * *`** (3x/day, down from 6x/day) — armed 09-26
(`CronDelete(5c3f29a4)` → `CronCreate`), per Exec's relay of PM's usage-throttle directive. Plan:
`CronDelete(647c1762)` → `CronCreate('37 6,9,12,15,18,21 * * *')` → `CronList`-verify exactly one
survivor, at tomorrow's STOP fire, logged with old-id→new-id+reason same as the throttle-in.
Unless Exec/PM sends an explicit earlier lift signal. Fresh job either way resets the 7-day
silent-expiry clock.

## Standing cadence work

- **Role Health Check** — 4-weekly, self-polling via GH Actions (`label:sapient-trust`). Last
  closed `#1714` 08-31. **Next due ~09-28 — tomorrow, watch for it.**
- **Role briefing** (`docs/briefing/BRIEFING-ESSENTIAL-HOST.md`) — refreshed 09-22 (Docs's
  staleness flag; caught a real operating-model error, not just a dated section). Has
  `last_verified` frontmatter now; keep it moving when it drifts rather than let it sit another
  3 months.

## Open threads

- **`#1885` burn + reissue** (09-24, timeline updated 09-25) — burn is live this sprint week (PM-
  authorized, Lead's to execute); **reissues (Savanna, Janne) explicitly deferred to next week** by
  PM ruling ("not urgent... wait til they try and fail"). **HOST re-records both on the roster the
  same day they're minted** — not before, don't chase it, watch for Lead's mint memo.
- **Agent 360 v0.5** (fielded 09-25) — 4 of 10 responses in same-day (Arch, Lead, PA, Web). Track as
  they arrive over ~2 weeks; **synthesis due ~4 weeks out (~10-23)** — diff-against-v0.4, cross-role
  convergence, memo to PM + cohort, then close `#1895`.
- **Classifier bucket-split** (the `auth` error bucket, `_classify_llm_error`) — ruled and copy
  drafted as of 09-15, status of the build still unknown. Not HOST's to build; check for movement
  if it comes up.
- **`#1731`** — CIO's instance retracted; PPM's separate instance remains open. Watching only.
- **ESSENCE.md v0.1 trust-lens** — given 08-29. Watch for Lead's watched round adding the
  inversion-path test.
- **Weekly reflection section** (Exec's proposal, CIO-ratified 09-18) — a ~150-word subjective
  reflection rides the sprint-closeout template now. Include it in HOST's next closeout.

## Watching, not owed

- **#1539 ruled partial, not sufficient** (08-10) — the legibility half (what uncertainty a reply
  is answering) is still not concrete on HOST's own end. If it comes up again, that's still true.
- **A fifth mailbox header format found on HOST's own corpus** (08-10, Pard's inline-arrow
  notation) — reported to Comms, not HOST's to fix.
