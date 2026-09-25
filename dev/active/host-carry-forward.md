---
last_updated: 2026-09-24
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-09-24 22:1x PDT (STOP fire, day 62 on Amber — frontmatter above is the checkable
claim; this prose line is not checkable and must not be trusted over it). · **Worktree**: Model A,
`~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

**Today (09-24)**: two threads. `#1875`/`#1859` (alpha wizard blocker → fully fixed same-day,
verified through the render layer, `#1859`'s residual flash traced to a bad n=1 measurement and
self-corrected by CXO) is fully closed, nothing carries forward. **`#1885` is not closed** — a real
credential-leak incident (three live unused invite tokens in full form in tracked files, two via
HOST's own session logs) found the scrub done and `#1845` ratified as a durable cohort rule
(CLAUDE.md + decisions.log), but the burn-on-prod + two reissues (Savanna, Janne) are explicitly
queued by PM (low blast radius, not urgent) — **owed by HOST**: re-record both tokens on
`dev/alpha/alpha-tester-roster.md` once Lead mints them post-burn. See today's session log
(`dev/2026/09/24/...host-code-log.md`) for full detail, including the second lint review (one real
gap found: lowercase invite tokens slip the Crockford regex, reported to Lead). This file stays
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

Current job **`5c3f29a4`**, expression **`37 6,9,12,15,18,21 * * *`** — armed since the 09-22 STOP
re-arm (delete-then-create from `63870a85`), unchanged through 09-23's and 09-24's twelve fires,
`CronList`-verified exactly one every fire both days. Session-only; silent 7-day expiry (~09-29,
**within a week now** — re-arm proactively rather than wait for absence).

## Standing cadence work

- **Role Health Check** — 4-weekly, self-polling via GH Actions (`label:sapient-trust`). Last
  closed `#1714` 08-31. **Next due ~09-28 — 4 days out, watch for it.**
- **Role briefing** (`docs/briefing/BRIEFING-ESSENTIAL-HOST.md`) — refreshed 09-22 (Docs's
  staleness flag; caught a real operating-model error, not just a dated section). Has
  `last_verified` frontmatter now; keep it moving when it drifts rather than let it sit another
  3 months.

## Open threads

- **`#1885` burn + reissue** (new, 09-24) — three unused invite tokens queued for prod burn (PM's
  hand, not urgent per PM's own risk read) + two reissues (Savanna, Janne). **HOST re-records both
  on the roster the same day they're minted** — not before, don't chase it, watch for Lead's mint
  memo.
- **`#1845` lint gap** (new, 09-24) — reported a lowercase-invite-token detection gap to Lead with
  the specific fix; Lead's call whether/when to land it. Watching, not owed.
- **Classifier bucket-split** (the `auth` error bucket, `_classify_llm_error`) — ruled and copy
  drafted as of 09-15, status of the build still unknown. Not HOST's to build; check for movement
  if it comes up.
- **`#1731`** — CIO's instance retracted; PPM's separate instance remains open. Watching only.
- **Agent 360 v0.4** — fully closed; only the cohort-share remains, pending PM's framing sign-off.
- **ESSENCE.md v0.1 trust-lens** — given 08-29. Watch for Lead's watched round adding the
  inversion-path test.
- **Weekly reflection section** (Exec's proposal, CIO-ratified 09-18) — a ~150-word subjective
  reflection rides the sprint-closeout template now. Include it in HOST's next closeout.

## Watching, not owed

- **#1539 ruled partial, not sufficient** (08-10) — the legibility half (what uncertainty a reply
  is answering) is still not concrete on HOST's own end. If it comes up again, that's still true.
- **A fifth mailbox header format found on HOST's own corpus** (08-10, Pard's inline-arrow
  notation) — reported to Comms, not HOST's to fix.
