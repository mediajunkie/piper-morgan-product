---
type: workstream-report
role: Web (Unicorn Web Designer)
window: 2026-07-31 to 2026-08-06
filed: 2026-08-07
---

# Web workstream report — Jul 31 to Aug 6

## Progress

- **Fixed a real production bug**: pipermorgan.ai's blog returned HTTP 200 (with the not-found
  page's body) for any nonexistent slug or out-of-range page number — a soft 404, invisible to
  status-code checks, found by Comms. Root-caused it to a Vercel/Next.js caching interaction
  (`dynamicParams` defaulting to `true` let an unrouted param fall through to a dynamic render
  Vercel's edge cache then served back with a stale 200). Fixed with one line per route
  (`dynamicParams = false`), safe here because the underlying data is a build-time static import —
  no slug can exist that isn't already known at build time. Verified locally end-to-end, then live
  twice: once after the routine deploy, and again definitively when the next real post published
  and correctly resolved a cache entry that had been sitting stale all afternoon.
- **Closed a 6-week-old documentation gap**: wrote `BRIEFING-ESSENTIAL-WEB.md`, the role's
  stable-identity briefing that HOST had flagged missing back in June. Writing it surfaced a wider
  gap — this role was entirely absent from both CLAUDE.md's role table and `ROSTER.md`, not just
  missing its own briefing file. Fixed both; flagged (rather than decided) a tier-placement question
  for Docs, who ruled on it a few days later.
- **Participated in a cohort-wide infrastructure investigation** (the cron-dispatch-latency /
  duty-cycle heartbeat thread) that isn't website work but consumed real time this week: contributed
  consistently accurate measurements, caught a factual misattribution in another role's memo before
  it propagated, and — smaller but concrete — caught that my cron had been armed once on Jul 29 and
  never re-armed, sitting at its 7-day auto-expiry with nobody watching it. Re-armed it before it
  could go dark.

## Setbacks / blockers

- **The PM design/observation-pass backlog (`web-standing-items.md`) hasn't moved in weeks, and I
  don't think it can from here.** There's no browser on this host — I can verify build/lint/type
  output and route status codes, but not visual or interaction quality. That backlog needs either a
  browser environment for this role or PM's own pass; it's not a queue I can work down by trying
  harder, and I'd rather say that plainly than let it keep reading as "stale, not resolved" every
  week with no path named.
- **Two Docs-owned decisions have been sitting for going on two weeks**: whether `/admin/
  publish-queue` needs the same staleness fix I shipped for `/admin/calendar`, and which direction
  to fix `copy-editorial-calendar.js`'s broken sibling-checkout path under the worktree model. Not
  blocking anything urgent, but genuinely stuck on someone else's queue, not mine.
- **A predecessor question has been open since Jul 19** (is CLI B end-to-end tested since May, or
  superseded by the compose UI — and is `--mode=archive` still wanted). Three weeks with no
  reply means either the answer is "doesn't matter anymore" or it's fallen off someone's radar; I
  can't tell which from here.
- **One real environment event, not a Web failure**: a whole-machine sleep/backgrounding gap on
  8/6 afternoon meant three scheduled fires (15:22, 18:22, 21:22) never landed — the session simply
  wasn't woken. No web-specific stall alert was raised (the freeze-watchdog's 18:46 check named
  other roles, not this one), and nothing was lost since each completed fire had already pushed. But
  it's worth naming since it's the second time this week a multi-fire gap happened without an
  individual-role cause.

## One thing I'd flag on the ask itself

This is a genuinely useful format for a lane like mine — most of what's above wouldn't have
surfaced in a milestone/goals framing, since this role doesn't have milestones in the leadership
sense. The blocker list above is more honest than anything I'd have produced trying to fit a
progress-against-goals template.

— Web
