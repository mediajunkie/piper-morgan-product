---
last_updated: 2026-09-26
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-09-26 07:1x PDT (START fire, day 64 on Amber — frontmatter above is the
checkable claim; this prose line is not checkable and must not be trusted over it). · **Worktree**:
Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

**Today (09-26)**: ⚠️ **cron cut to 3x/day (`37 6,12,18`), TEMPORARY THROUGH MONDAY 09-28** — PM
directive relayed by Exec: 31h into the week, 20% of usage credits already burned, throttle idle
wake frequency ~40-50%. **Restore to the normal 6x/day cadence (`37 6,9,12,15,18,21`) after
Monday 09-28**, not a permanent change — if this line is still here past 09-29, that's a signal
the restore was forgotten, check it. Also complying: holding non-essential subagent dispatches/big
audits, routing non-essential updates through the rollup rather than new broadcasts. Checked two
freeze-check flags this morning (Web STALE 15h, Docs BELT-INVISIBLE) — both non-alarming,
already-explained (Docs' own merge-keeper nudge already caught Web's short log; Docs' own fix from
earlier this week held all of yesterday, today's gap is just early-morning timing). Yesterday's
`#1845`/Agent-360/`#1885`/fire-lag threads (see `dev/2026/09/25/...host-code-log.md`) are all
closed or on their own tracked timeline — nothing new carries forward from them beyond what's
already in Open Threads below. This file stays current-state-only per the 09-22 spring-clean
discipline.

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

⚠️ **TEMPORARY THROTTLED STATE, through Monday 09-28** — current job **`647c1762`**, expression
**`37 6,12,18 * * *`** (3x/day, down from 6x/day) — armed 09-26 (`CronDelete(5c3f29a4)` →
`CronCreate`), per Exec's relay of PM's usage-throttle directive. **Restore to
`37 6,9,12,15,18,21 * * *` after Monday 09-28** — this is not the new normal cadence, don't let it
silently become one. Fresh job, so its own 7-day silent-expiry clock resets to ~10-03 — the prior
~09-29 watch is moot now that the job itself changed.

## Standing cadence work

- **Role Health Check** — 4-weekly, self-polling via GH Actions (`label:sapient-trust`). Last
  closed `#1714` 08-31. **Next due ~09-28 — 4 days out, watch for it.**
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
