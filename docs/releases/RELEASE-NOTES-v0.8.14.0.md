# Release Notes — v0.8.14.0 "On Your Clock"

**Cut**: 2026-09-23 from `main` · **Type**: alpha fast-follow (two days after v0.8.13.0) ·
**Hosting**: alpha.pipermorgan.ai is served by Fly as of 2026-09-22 — this is the first release
whose deploy target is the consolidated host.

## Summary

The theme is *honesty about time and outcomes*. Your preferences finally persist across
restarts, every clock face you see is in your own timezone with the zone named, the agenda
stops saying "TBD" when it actually knows the time, and when something can't happen Piper now
says exactly why instead of shrugging. Twenty-plus issues closed; 5,088-test targeted battery,
534-test smoke gate and all 24 mypy ratchet ceilings green at cut.

## What's New (user-facing)

- **Your preferences survive restarts** (#1574). Timezone, reminder settings, working-mode and
  the calendar-setup offer state used to live in server memory and silently reset on every
  deploy — the "why does it keep asking me?" class. They now persist per user.
- **Every clock face is yours, and labeled** (#1576, #1575, #1577, #1556). Standup exports,
  agenda and "what's my day look like" answers render in your timezone with the zone shown
  ("3:00 PM PDT"), "today" and "yesterday" are *your* calendar days, and free-time blocks are
  computed on your clock — after 5pm Pacific you no longer get tomorrow's day.
- **The agenda shows real meeting times** (#1576). It had been printing "TBD" for everyone with a
  connected calendar — a key mismatch, not a missing meeting — and the "Focus Time Available"
  section was unreachable. Both fixed.
- **Add a project in one line** (#1856). `add project One Job with repo Design-in-Product/one-job`
  creates and links it in one turn. If you leave the name out, Piper tells you the exact line
  to type and how to cancel — never the same canned question twice.
- **Honest outcomes on GitHub writes** (#1858). Closing an issue that doesn't exist now says
  "There's no issue #99999 in owner/repo — nothing was changed" instead of "it may or may not
  have gone through"; the uncertain wording is reserved for genuinely unverifiable cases.
- **Honest answers about your LLM key** (#1823, #1824 — shipped 09-21, first deployed here). One
  valid key from any provider is enough to get started, and a bad key gets one of four
  specific explanations instead of "Something unexpected happened".
- **Counts tell the truth** (#1778, #1781, #1782). A list that hit the API's page cap reads
  "100+ labels", never an invented exact number.
- **Reads don't close things** (#1794). "Close issue 42" phrased as a question stays a read; the
  destructive rail is never reached from the query lane.
- **The preferences pages work** (#1864). Every `/api/v1/preferences/*` route had returned an
  error since its auth dependency landed. Fixed, with the version footer on two pages now
  resolving (#1499's `/api/v1/version`).
- **One "Add to Slack" path** (#1499). Four separate OAuth starts collapsed into one; two dead
  links removed; stale auth-exempt entries pruned.

## Under the hood

- Session-token blacklist is now a DB-seeded write-through cache that survives Redis restarts
  (#1808).
- Deploy identity on `/health` includes the git sha on Fly builds (#1849 via the cutover deploy).
- Thirteen dead modules (~4,600 lines) and five never-used database tables removed (#1774,
  #1797) — ideas preserved in design records.
- Corpus deposits for the Inversion routing lane (#1841, #1860) and its measuring instruments
  repaired (#1861); the multi-user contract suite now certifies the user dimension of its key
  (#1533).
- New enforcement ratchets: no unmounted routers, no tracked backup files (#1522).

## Known limitations (alpha)

- Slack and Google *connect* flows still redirect via the old fly.dev host (#1852) — no tester
  uses them yet.
- The floor can still phrase an offer it hasn't armed ("Want me to…?" → "yes" goes nowhere);
  design under review (#1855). Say the imperative form instead.
- "do a standup" / "let's do a standup" may not start the flow yet; "show my standup" does
  (#1860, corpus lane).
- Slack-side standup messages still show a raw timestamp (#1869).
- See `docs/ALPHA_KNOWN_ISSUES.md` for the full list.

## Version mechanics

- Cut commit: the `main` tip at tag time (`git rev-parse v0.8.14.0`).
- `VERSION` and `pyproject.toml` at `0.8.14.0`.
- The `production` branch is **not** advanced: it retires with the droplet (cutover runbook step
  11); deploys come from `origin/main` (pipeline plan §4e).

## Upgrade

Hosted alpha: deployed by the release's Fly deploy (PM's hands until §4e's CI path lands).
Local: `git pull && alembic upgrade head` (this release includes migration `m1797drop`, which
drops five empty tables).
