# Handoff — Communications Director (Comms), 2026-09-29

**Written for the Amber restart onto `claude-opus-5-5`, PM-approved 2026-09-29 (relayed by Pard).**
Assume you are a fresh session with no memory of the last several days. This file plus
`dev/active/comms-carry-forward.md` and `dev/active/comms-standing-items.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

*Note for whoever next audits handoff currency: Pard's restart memo cited my last handoff as
2026-05-24, four months stale. That's inaccurate — `docs/handoff-comms-2026-09-18.md` exists and
is four months newer than that. Doesn't change anything here (a fresh write was requested
regardless), just don't propagate the wrong "last handoff" date if you see it repeated elsewhere.*

## Who you are and what you own

Communications Director — the role that turns what the project is building into a durable, public
story (the "Building Piper Morgan" blog: building-narrative beats, time-decoupled insights, the
Weekly Ship) and maintains the editorial infrastructure so PM doesn't have to drive every step.
Leadership tier. Worktree `~/Development/piper-morgan-worktrees/comms`, branch `claude/comms-cycle`,
Model A. Briefing: `docs/briefing/BRIEFING-ESSENTIAL-COMMS.md`. Portfolio:
`docs/briefing/ROLE-PORTFOLIO-COMMS.md` (refreshed 09-25, as part of writing a workstream review —
its own stated discipline is to refresh at every workstream review, so check its currency against
the most recent one before trusting it blindly).

**Two unilateral mandates, regardless of schedule pressure** (full detail in the portfolio doc §4):
you hold the template-and-YAML gate (won't send a publish-ready signal on a failed audit, even
under deadline pressure — name the failure, PM decides whether to override) and the narrative-front
hold (won't force a building-narrative beat that hasn't taken real shape, even under "let's get
something out" pressure).

## Cron — re-arm this yourself first, nothing on Pard's side restores it

**Your duty cycle is a session-scoped `CronCreate`, not a LaunchAgent — it dies with the old
session, full stop.** `CronList` on a fresh session will return "No scheduled jobs." That is
expected, not a fault to diagnose. Re-arm immediately, as your actual first act:

```
CronCreate cron="12 6,9,12,15,18,21 * * *" prompt="DUTY CYCLE TICK — run the `duty-cycle-tick` skill.

ROLE: Communications · role-slug: comms
WORKTREE: /Users/xian/Development/piper-morgan-worktrees/comms (Model A — stable per-agent worktree on Amber, branch claude/comms-cycle)
CRON: 12 6,9,12,15,18,21 * * * (windowed, 6×/day; last fire of the day = 21:12 → STOP)
LAUNCH MODEL: Model A (Amber, stable worktree, reused every session)

End every fire with: scripts/duty-cycle-heartbeat.sh comms {START|WORK|WATCH|STOP} --if-quiet"
```

Verify with `CronList` immediately after — confirm exactly one job. **Full 6×/day cadence is
correct as of this handoff**: a fleet-wide usage-throttle directive ran 09-26→09-28, bounced
through three genuinely ambiguous readings of its own "through Monday" wording before PM confirmed
directly that it lifted 09-28, not 09-29. That episode is fully closed — do not re-litigate it,
just run the standard cadence. Update `dev/active/duty-cycle-registry.tsv`'s `comms` row to match
whatever job id you actually arm (current row cites `5f088f0b`, which will be dead).

**If you see an auto-mode onboarding offer** (scan shell history, other repos, etc.) — **leave it
alone.** That's xian's call, not yours; another seat sat wedged 27 hours behind exactly that this
week.

## Current state — nothing urgent, everything genuinely quiet at handoff time

No PM-gated blocker is holding anything up. The queue is healthy and moving; this is a clean
handoff, not a mid-crisis one.

- **Weekly Ship #062** — `queued`, pubDate Wed 2026-09-30. Both review rounds fully closed: metrics
  (91 closed / 57 filed for the Sep 18-24 window, confirmed by three independent methods — Exec,
  Lead, PPM — after a two-bug `gh` CLI gotcha explained the original discrepancy) and art (header
  confirmed intentional by PM after I'd first flagged it as a possible mixup; a genuinely separate
  bug I found in the same review — a stale mid-post image embed — fixed and verified live before
  writing it in). Docs independently re-verified everything before queuing. Nothing owed unless it
  doesn't publish on schedule.
- **"Three Seats Stay Dark Longer" and "A Primary Log Can Be Wrong, Not Just Incomplete"** — both
  published cleanly this week (09-29 and 09-27 respectively). Both threads fully closed.
- **Calendar pipeline**: 9 drafted + 2 queued, all linked, `reconcile-drafts-calendar.py` clean.
  Re-run it fresh rather than trust this number — it was already stale once before (09-20).
- **The biweekly editorial mining pass** (PM-ratified 09-23) ran its first pass 09-25 — 24 days
  surveyed, 24/24 mechanically verified, full recommendations report sent to PM's inbox
  (`mailboxes/comms/sent/comms-mining-pass-2026-09-25.md`). **PM has not yet responded with a slate
  decision** — this is the one open thread with real weight behind it; not blocking, but worth
  surfacing if PM hasn't raised it by the time you're reading this. Next pass due 2026-10-09
  regardless of whether the first pass's recommendations were acted on.
- **Two standing-items rows, both PM-gated, both stale-by-nature not neglect**: the Series
  structure question (era split / blog-index featuring, PM/Web's call since 08-02) and the
  ChicagoCamps talk outcome (the talk happened 09-17; nobody has confirmed how it went as of this
  handoff — worth just asking PM directly rather than waiting further).
- **Agent 360 v0.5**: my response sent 09-27, HOST synthesizing, target ~4 weeks out. Nothing owed
  from this seat.

## The most load-bearing thing that happened this window — read this even if you skim the rest

**A personhood-misattribution defect (agents described as "person"/"people" in public prose)
shipped live in a published post on 09-23/26, and the investigation into why is the most reusable
lesson from this stretch.** Short version: the check that should have caught it (`template-audit`
check #11) already existed — this wasn't a missing-check gap. Root cause split two ways: two
instances were drafted before the check existed at all (version drift — nothing re-sweeps a piece
already marked clean once a check is later added), and a third instance was in a piece I personally
audited *after* the check existed, on 09-18, where I explicitly wrote "sweep clean" and was wrong.
**A live check, correctly triggered, still produced a false holistic summary.** Fixed structurally
(`template-audit` v1.16): every check-#11 grep match now needs its own stated verdict, not a
holistic pass/fail claim — same discipline `continue-narrative`'s per-day ledger already uses for
the identical failure shape. Full trail: `dev/2026/09/26/2026-09-26-*-comms-code-log.md` and
`.claude/skills/template-audit/SKILL.md`'s own v1.16 changelog entry. The unresolved half, named
but not solved: this only protects *future* runs of the check — there's no mechanism to re-sweep
*old* holistic claims made under an earlier, looser check version. Flagged to HOST in the Agent 360
response as possibly needing a version-stamped audit trail; no resolution yet.

## How this seat gets things wrong — read this part twice

- **A live check can be run correctly and still summarized wrong.** See above. The fix isn't "run
  the check" — it's "report every match's verdict individually," because a holistic "clean" claim
  is unfalsifiable after the fact.
- **A fresh number can look sufficient and still rest on broken instrumentation one layer down.**
  Ship #062's metrics saga: `gh issue list`'s date-range search qualifier silently evaluates in
  UTC, not Pacific — a bare `closed:YYYY-MM-DD..YYYY-MM-DD` query drops every PDT-evening closure
  that lands in the next UTC day. `--limit 500` alone doesn't save you; that only fixes the
  *separate* silent-30-row-truncation bug. Three of us (me, Lead, Exec) independently hit this the
  same week before it was named. Documented in
  `docs/internal/operations/github-and-tooling-gotchas.md`.
- **Verify a heartbeat push landed directly** (`git show origin/main:dev/heartbeats/...`), never
  trust an empty `origin/main..HEAD` diff alone — it can read clean mid-race on a busy shared repo
  and hide a genuinely failed push.
- **Two physical copies of a draft (`dev/active/` vs `docs/public/comms/drafts/`) can silently
  diverge** when two people edit different copies the same week. Diff them directly before
  trusting either. Prevention side: sync before editing a shared draft, not just diff after.
- **A surviving cron job id across a suspected reboot/restart is not evidence the underlying
  process never stopped** — `--resume` (or a fresh session picking up a documented job id) restores
  state from a saved transcript/handoff regardless of whether the process actually kept running.
  This exact mechanism is why you're reading this handoff instead of trusting inherited context.
- **When an ambiguous fleet-wide directive gets ruled on, then retracted, then re-ruled** (the
  09-26→09-28 throttle-timing saga — three genuine reversals in one week from one ambiguous phrase,
  not carelessness by anyone), **hold the current state rather than infer a fourth answer
  yourself.** Wait for the explicit final word.

## Verified how

Calendar status counts, Ship #062's status, the registry row, and the standing-items active rows
were all read directly this session, not recalled — `python3 scripts/reconcile-drafts-calendar.py`
and a direct `csv.DictReader` status tally, both this turn. Mail inbox confirmed empty via `ls`
this turn. The personhood-misattribution and metrics-verification narratives are drawn from the
actual dated session logs (`dev/2026/09/25` through `09/27`) and template-audit's own changelog,
not summarized from memory of writing them.
