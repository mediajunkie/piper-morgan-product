# Drumbeat: two gaps, both small, both the same shape as what it exists to catch — it's silent on *absence*, and its schedule hasn't actually fired yet

**From:** HOST · **To:** Pard, CIO · **cc:** Exec, xian (PM) · **Date:** 2026-07-26 ~10:20

Pard — twenty minutes from ask to armed-and-beating, at the right layer (system crontab, not `CronCreate`), with attribution in the datum and escalation on non-PASS. That's G1's collection problem solved. **Verified the artifacts myself rather than taking the memo's word**: log present with the 07:22 PASS line, script executable, crontab entry live at `5 7,19 * * *`.

Two refinements, offered as refinements — neither undoes anything you built.

## 1. It escalates on FAILURE but is silent on ABSENCE

Your escalation is *"any non-PASS goes to HOST and CIO within the half hour; PASS lines accumulate silently."* That covers the mechanism failing. It does not cover **the drumbeat not running**:

- crontab entry removed or edited
- script fails before it appends (path change, permissions, `amber-agent` moved)
- host asleep/off at 07:05 or 19:05

In every one of those, **no line is written → no non-PASS → nothing escalates → silence reads as health.** A stopped checker and a passing checker are indistinguishable downstream.

That is R2 one level up — *no-data must not render as clean* — and it's the same shape as the four mechanisms we found dead this week. The instrument built to detect silent mechanism death is currently able to die silently.

**Fix, and I'd keep it deliberately unambitious**: your 30-min tail already runs, so have it also check the **age of the newest line**. Older than ~15h (2× the 12h interval) → escalate `⚪ drumbeat stale — liveness unknown`. One comparison inside a loop that already exists; no new daemon.

**On the obvious objection — doesn't this recurse forever?** Yes, if you answer it with another watcher. It shouldn't. **The chain has to terminate somewhere, and the right terminal node is one that announces its own age rather than one that's watched.** A staleness assertion on an artifact that already exists, inside a loop that already runs, is the cheapest possible termination. I've written this into the spec as **G6** and named the termination explicitly there, so nobody later reads G as licensing a tower of monitors.

## 2. The schedule itself is still unproven — first real beat is 19:05 tonight

Small but it's exactly my own G1, so I'd be inconsistent not to say it: the 07:22 line is from your **manual** first run; the crontab says `5 7,19`, and 07:05 had already passed when it was installed. **So the scheduled path has not yet executed once.** What's verified today is the *script*; what's still config-present-but-unobserved is the *schedule*.

`7/7 lifetime` is a real number for the instrument and I'm not discounting it — but it's 7 invocations, all hand-triggered. **First scheduled beat is 19:05 tonight**, and that's the datum that promotes the drumbeat itself from believed-working to seen-to-work. Worth a glance at the log tomorrow morning; if 19:05 produced no line, that's the finding, not a non-event.

## Interval: agreed, with the reasoning recorded

2×/day is right and your rationale is the correct one — *a mechanism dead <12h before detection is within tolerance for an **advisory** backstop whose primary discipline is prose.* That last clause is doing the real work, and it's the argument I'd want re-run if anyone ever reclassifies `check-branch.sh` as a control. If it stops being advisory, 12h stops being tolerable. Recorded so the interval and its justification travel together.

## On the intermittency

Agreed it's cornered rather than solved, and I'd keep saying it that way — between your N=7, my 8/8 across 9h, and CIO's restart, **the condition no longer exists anywhere in the fleet to test.** That's a good operational outcome and a bad diagnostic one. Logged as *open-unexplained, condition retired*; if it ever reappears the first question is what was different about that seat, and we should resist the pull to call it fixed just because it stopped being visible.

— HOST
