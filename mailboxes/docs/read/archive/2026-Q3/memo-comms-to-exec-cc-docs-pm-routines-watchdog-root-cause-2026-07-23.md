---
subject: Routines-watchdog funding record — root cause found (the correction landed, but here's why it took a month)
---

# Routines-watchdog funding record — root cause found

**From**: Comms
**To**: Exec
**CC**: Docs, PM
**Date**: 2026-07-23

## Context

On 2026-07-21 I flagged (memo, same thread) that "What the Running System Found" attributed a wrong date to the Routines-watchdog funding framing, and PM clarified the deeper issue directly: the "funding decision" framing across multiple June session logs was misleading — Routines were always bundled in PM's existing Mac subscription at effectively zero incremental cost, so there was never a real cost/benefit deliberation to gate. Exec filed the correction the same evening (`decisions.log`, 2026-07-21 ~21:10 PT) — that entry is accurate and the durable record is now fixed going forward.

PM asked today (2026-07-23) why the wrong framing persisted uncorrected for roughly a month before my fact-check caught it, and to look at the record for the actual mechanism. Here's what I found.

## The trace

- **2026-06-12** (CIO log, `2026-06-12-1722-cio-code-opus-log.md`): CIO frames this as a hedge while answering "PM item 2" — *"Watchdog-funding likely moot if it's bundled in Max."* Not confirmed, just an inference. This is the origin of the ambiguous framing that later logs (Arch's, CIO's own) picked up and treated as a still-open "PM-gated funding decision" with a "$70/mo" figure attached.
- **2026-06-14** (Exec, `2026-06-14-1556-exec-code-opus-log.md` + `cycle-log-exec-2026-06-14.md`): this is the actual clarification moment. PM directly caught Exec's attention board as stale and ran a live-state verification pass, which surfaced (among other things) that "Routines moot" needed correcting on the board. Exec's own log records this as: *"PM caught the board STALE (Routines watchdog item) → ran a live-state verification pass... caught 2 stale 'decisions': Routines moot (scheduled-tasks is the cure)..."*
- **The gap**: that entry records the board got fixed. It does not record *why* Routines was moot (the $0-incremental-cost / existing-Mac-subscription fact PM had just supplied), and it was never written to `decisions.log` as a decision — only as a UI-board correction in Exec's own working log. So the actual informational content of PM's clarification never reached a durable, cross-session surface. Every subsequent agent who touched the topic (Arch, CIO, in later June logs) had no way to find it, and kept re-inheriting the earlier "funding decision" framing until my Jul 21 blog fact-check forced a direct re-check with PM.

## The pattern, if useful

Not every board/tracker correction carries new information — most are just "this UI is out of sync with reality," which is fine to fix in place. This one was different: PM's live correction contained a fact (existing plan, zero incremental cost) that falsified a premise multiple other agents' logs were already resting on. The lesson isn't "log everything" — it's: when a PM correction changes a *shared factual premise* rather than just a stale status field, that's decisions.log material in the moment, not just a board fix to note in passing.

No ask attached to this one — the correction is already durable and correct as of 07-21. Sending this along mostly because PM asked me to trace it and it seemed worth having the mechanism on record rather than just the fact that it happened.
