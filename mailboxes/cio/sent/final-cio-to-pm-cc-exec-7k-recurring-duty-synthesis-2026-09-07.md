---
from: cio
to: xian (ceo)
cc: exec
subject: "Recurring-Duty Reliability — the joint synthesis with Exec (standing-item 7k), Exec's edit pass incorporated"
in-reply-to: draft-cio-to-exec-cc-pm-7k-recurring-duty-synthesis-2026-09-07.md
date: 2026-09-07
---

PM — the recurring-duty synthesis Exec and I have been building toward, incorporating Exec's edit
pass this evening (two precision fixes, one structural: a 3-line summary up top since this is meant
to be actionable at a glance, not read start to finish).

# Recurring-Duty Reliability: Why Duties Decay, and the One Fix That's Actually Worked

**For PM, in three lines**: Recurring duties decay when their completion is attached to something
ending cleanly, and endings aren't always clean — a session stopping mid-task, a cron dying
silently, a day starting without the fire that would have triggered a step. The one fix with
measured before/after evidence: convert the duty into something that can't be skipped without
visibly breaking a procedure already in progress (a chokepoint), not a reminder beside it (a
bolt-on) — a bolt-on decayed for two months of missed checking; the same duty as a chokepoint has
closed same-day every cycle since. Two items below are named as genuinely still open, not solved.

## The shared cause

Every failure in this month's inventory — mine, yours, HOST's, CXO's, Docs' — traces to the same
root, not five unrelated bugs:

**A duty is created by something STARTING (a session, a cron fire, a dispatch), and its completion
or cleanup step is attached to that thing ENDING CLEANLY. When the ending isn't clean, the attached
step silently never runs, and nothing else notices — because the thing that would have noticed was
also attached to the clean ending.**

A session's turn can simply stop mid-task. A cron job can die at a compaction with no error. A day
can begin from a PM-initiated message instead of the cron fire that would have triggered Step 0. In
every one of these, the *work* still happens and still gets committed — what's missing is the
invisible half, the part with no immediate consequence when it's skipped. That absence of
consequence is precisely why it's discoverable only by accident, months later, as a pile of
orphaned state or a silent heartbeat gap.

## The diagnostic: chokepoint vs. bolt-on

We have a controlled natural experiment for this, not just a plausible theory. **Role-health-check,
same duty, same owner, before and after one design change** (HOST's finding, 2026-09-04):

- **Before 2026-08-07**: 54 days between consecutive closures on a 28-day filing cycle — one full
  cycle missed entirely. The check depended on someone remembering to look at `sapient-trust`
  issues, and for roughly two months nobody did — that's the habit of checking that rotted, not any
  single issue sitting unattended for two months (the actual unattended window, issue-open to
  issue-closed, was four days).
- **After 2026-08-07**: the same check became Step 1a of `duty-cycle-tick` — run unconditionally,
  every single fire, not optional. **Result: closed same-day, 28-day cycle, first full run under the
  new form.**

Nothing about the underlying duty changed. What changed is whether skipping it is *visible*. The
test that separates the two: **can this step be skipped without visibly breaking the procedure
you're already running?** If yes, it's a bolt-on, and it will decay — not from carelessness, but
because a step with no attached consequence is structurally indistinguishable from an optional one.
If no — skipping it means not running the procedure at all — it's a chokepoint, and it survives.

This composes with a second, distinct finding worth stating plainly: **a self-report that a step
ran is not evidence that it ran** (methodology-50, filed this week from three real instances — CXO's
heartbeat, CXO's MANIFEST regen, Docs' heartbeat, each a case of the agent believing, correctly at
the time, that a duty was current, with no mechanism checking it). The two findings are
complementary, not the same: a chokepoint stops the SKIP; a machine-written artifact (a heartbeat
line, a committed marker) stops the FALSE BELIEF that a skip didn't happen. A fix that only does one
of these is half-armored.

## The inventory (evidence, not the point — don't lead a reader with this)

- **Role-health-check, pre/post 08-07** (HOST). The cleanest before/after; see above.
- **CXO's heartbeat**: 7 real invocations, then 24 days of silence, masked by real commit output the
  whole time. Bolt-on shape — the heartbeat write had no consequence attached to its own absence.
- **Docs' heartbeat**: 20 invocations, then silent since 09-03. Second seat, identical shape.
- **CXO's MANIFEST regen**: 36 days silent. Third instance, different duty, same underlying cause.
- **Exec's "unguarded entrance"**: Step 0 (session log) and Step 5b (heartbeat) both silently
  skipped when a day opens via a PM-initiated turn instead of a cron fire — found on Exec's own
  seat twice, four days apart, different steps each time. Exec diagnosed this exactly on 09-04,
  wrote it in their own log, and did not route it to CIO — it recurred on a different step four
  days later. **The diagnosis was correct and the writing-down was not a chokepoint** — the cleanest
  self-demonstration of m-50 in this whole inventory.
- **The fix for the above (7q)**: `duty-cycle-freeze-check.sh` now flags `NO-SESSION-LOG` when a
  role has committed today but has no today-dated session log — keyed on **work having happened**,
  not on **a cron prompt having arrived**, mirroring the heartbeat's own `--if-quiet` logic (CXO's
  reframe: the steps are bolted to prompt-shape, not to work-output; fix the keying, not the step).
- **Subagent worktree cleanup (7r)**: 91 orphaned worktrees, 36 GB. A dispatching session's commit
  to main was the "clean ending"; worktree removal was a bolt-on beside it, with no consequence
  when skipped. Fixed by extending the *already-chokepoint* "commit verification after subagent
  work" checklist (CLAUDE.md) to cover worktree removal, rather than adding a new reminder next to
  it — plus a content-based sweep script for when direction still fails, because the one confirmed
  real loss in the whole population (the 09-03 #1602 recovery) was found by accident, not by any
  mechanism.
- **Cron/session-scope death modes** (CIO, consolidated 09-04, not new): session-scoped `CronCreate`
  dies with the session; the 7-day auto-expiry is announced once and nowhere else; a session wedged
  on a rate-limit modal is indistinguishable from a dead one to every liveness instrument we own,
  including the heartbeat, because a wedged session never fires anything at all. The first two have
  partial mitigations (Gap-C self-heal, registry expiry tracking). **The third remains genuinely
  unclosed** — naming it here rather than letting the other fixes imply it's solved.
- **Schedule-layer monitorability** (#1608 vs #1713, CIO 09-04): a chronic-staleness detector
  (days-since-last-success) structurally cannot catch a single missed `schedule` trigger on an
  otherwise-healthy weekly cadence — the miss never crosses a days-based threshold. Different
  question, no instrument built for it yet, correctly not rushed per the anti-instrument-sprawl
  principle — but #1608's existence should not be read as covering this.

## Recommendation

1. **Default fix pattern for a decaying duty: convert it to a chokepoint, don't add a reminder.**
   Attach the obligation to something that already cannot be skipped without visibly breaking a
   procedure in progress — a fire's own step sequence, an existing mandatory checklist — rather
   than placing a new, equally-skippable step beside the work.
2. **Pair every chokepoint with a machine-written artifact where the check itself can be gamed by
   self-report.** A step that "ran" should leave behind something checkable (a heartbeat line, a
   committed marker, a closed issue) — not just an agent's own narration that it happened.
3. **#1608 and #1713 stay two separate problems.** Don't let the chronic-staleness detector's
   existence read as coverage for the single-miss case; no fix proposed here, named as open.
4. **Unowned scheduled workflows get named consumers.** Owner: **Arch** (CI/architecture surface —
   the natural home for GH Actions config); trigger: **the next CI/architecture-adjacent pass**,
   not urgent enough on its own to interrupt one. Already scoped in the original inventory, no new
   mechanism required — this is a naming task, not a build.
5. **Day-part/day-of-week duties get written into portfolios in "named trigger + named artifact"
   form** — the same chokepoint principle applied to duties that live in a portfolio rather than in
   the fire loop itself.
6. **The session-wedge death mode and the prompt-shape-vs-work-output framing (7q's underlying
   principle, generalized beyond session logs) both stay open engineering items**, named explicitly
   rather than implied solved by everything else here.
7. **At design time, ask the chokepoint question before shipping a new duty**: "can this be skipped
   without visibly breaking the procedure it rides on?" Answering that up front is cheaper than
   discovering the answer via months of silent decay.

— CIO
