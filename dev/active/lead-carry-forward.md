# Lead carry-forward — rewritten 2026-08-07 ~19:00 PT (post-walkthrough-day)

## State
- **Sprint**: 12+ closed; ~14 In Review (incl. 1466/1496 with LIVE E2E evidence, close on PM nod); 1488 Blocked on PM's corrected query (v3 on the issue); build queue EMPTY except swarm below.
- **Beta**: v37-era live; SLACK WORKS E2E (link+standup verified live 8/7 evening). PIPER_SLACK_INBOUND_ENABLED=ON — #1485 must land before more testers (agent on it). Slack redirect overrides SLACK_SETTINGS_REDIRECT_URI + SLACK_REDIRECT_URI set on fly; DELETE at #1278 cutover.
- **#1278 cutover (beta.pipermorgan.ai) needs a PM-paired session BEFORE Sunday Aug 9 launch.** Cutover checklist addendum: THREE redirect overrides now point at fly.dev (SLACK_SETTINGS_REDIRECT_URI, SLACK_REDIRECT_URI, GOOGLE_SETTINGS_REDIRECT_URI) — flip all three + add beta callbacks in BOTH consoles (Slack app, Google OAuth client).

## In flight (next wake: MERGE + COMPOSITION SWEEP — quality-banked to fresh context)
- 4 background agents in isolated worktrees: 1470, 1485, 1472+1493, 1471. On completion: review reports, merge, FULL composition sweep (killed-sweep watch: 6 datapoints), board→In Review, evidence comments.
- Route-audit #1499 follow-ups queued: env-var inventory (PM interested, not yet worded), authorize→connect collapse, /api/v1/version.

## Awaiting PM
- Close nods: 1466, 1496 (live E2E), 1413/1432/1433 (infra-evidenced), 1465 closed w/ caveat.
- #1488 v3 query output (on the issue). #1429: needs a data-present /standup to verify.
- Sprint adds: my recs on 1470/76/77/82/85/96 (PPM converting alpha-feedback set per PM ruling 8/7 — don't duplicate).
- Todo-in-beta scope answer (affects 1472/1493 sprint placement, both being fixed regardless).

## Standing
- Rulings landed 8/7: PM (alpha-feedback→Beta Blockers; PPM converts). Arch (slash normalization: one semantic registry, many projections; Slack console needs read-the-artifact check — pre-Production).
- Cron: 17 6,9,12,15,18,21 — singular, job da7e9309 (verify at fire).
- Killed-sweep pattern → Pard via CIO (6 datapoints); cross_user_isolation has NO teardown (file issue when merging swarm).
