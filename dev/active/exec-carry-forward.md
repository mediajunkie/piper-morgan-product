# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-11 ~23:20 PT at day-close.**

## Cron
Job `83258e51`, **`38 6,10,14,18,22`** — 5 fires/day, never >4h apart in the 06:00–22:00 window
(PM-proposed 09-11, adopted same morning; was `32 8,20`). Armed 09-11 06:55, expires ~09-18 →
**rotate ~09-16.** Registry row updated.

## ⭐ Where the weekly cycle stands
**Ship #060 window Fri 09-04 → Thu 09-10.** Omnibus 7/7 · kickoff sent 07:00 · **10/10 reports in**
· **internal report DELIVERED to PM** (`dev/active/ship-060-internal-report-for-pm-2026-09-11.html`).
**Next per PM's ten-step cycle: PM discussion → then the public Ship draft.** The draft has NOT
started; Step 2c is satisfied but the discussion hasn't happened.

**The theme, if the draft keeps it**: nearly every role's most substantive contribution this week
was catching their OWN error. Ten instances, one per role, mine included.

## Blocked on PM
1. **Bot onto protected main** — Arch's re-test: PR rule gone, **a SECOND masked blocker surfaced**
   (required status check; a direct push can't pre-satisfy a check that runs on pushes). Repo is
   **public with ZERO rulesets**, so the ruleset+bypass-actor path is free. Arch recommends it; I agree.
2. **#1617 retest** — ~90s, Lead's replay passes 3/3.
3. **Vercel** — 14.91 GB / 10 GB deployment storage; deleting old deployments is free and sufficient.
4. **Q5** — probably dissolved by PM's own work-queue ruling; worth confirming that reading.

## Awaiting others
CIO (archive `read/` proposal · cc-rule change · re-check-anomalies rule · #1746) · Arch/CIO
(scope-guard delivery, blocked on #1 above) · janus / pard / dispatch-dinp (orphan-mail triage +
their durable channel) · Lead (epic order continues).

## State
MVP **47 not done** (37 Sprint Backlog, 3 In Progress, 7 In Review); **1,134 done**; zero
unmilestoned. Window 09-04→09-10: 26 closed (18 MVP), 23 opened, net −3, 1,998 commits, 4 deploys.
**49 days to 30 Oct. 37 never started — the number that matters and it rose today.**

## Standing corrections on me
- ⚠️ **`closedAt` is UTC** — always compute closures in Pacific.
- ⚠️ **Re-check an anomalous reading once before reporting it** (PM's rule, from my own stale-belt
  error). Applied 3× since; it changed my reading twice.
- ⚠️ **Verify at the layer where the thing happens**, not where the schema says it should.
- ⚠️ **Ask once is not ask** — and **read-and-file is not act**: Pard told me on 09-08 that my mail
  wasn't reaching them and I kept routing there all week.
- ⚠️ **Check my own seat before reporting someone else's lapse.** 13/14 on DAY-CLOSED tonight —
  clean, but I checked rather than assumed.
