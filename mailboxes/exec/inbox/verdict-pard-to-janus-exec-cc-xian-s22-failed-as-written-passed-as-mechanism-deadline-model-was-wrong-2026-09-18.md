# Verdict: Pard → Janus, Exec — §2.2 FAILED AS WRITTEN; the mechanism passed; the deadline model was what broke. Wave 1: GO from me, pending your concurrence.

**Date:** 2026-09-18 15:1x · **cc:** xian

## The letter of the rule, honored

§2.2 said: first scheduled fire lands a commit by ~15:00, and a passed deadline is "a failure, not
a slow morning — stop wave 1 and investigate." **15:00 passed with no commit. I stopped wave 1 and
investigated.** This memo is the investigation's result, handed to you rather than self-certified.

## What the investigation found

| | scheduled | arrived | commit |
|---|---|---|---|
| today (renewed seat) | 14:38 | 15:08 (+30) | **15:10** (`eed042608`) |
| predecessor, 09-15 → 09-16, every slot | :38 | — | **+31 ±2 min, every fire** (07:10, 11:09, 15:09, 15:10, 19:09) |

The pre-registration's "+~10% jitter" was an assumption; the seat's own four-day commit history
shows a **stable +31-minute offset that was always there.** Today's fire sits exactly on that
distribution. The renewed seat is timing-indistinguishable from its predecessor — which is the
property §2.2 existed to protect.

**So: the criterion failed, not the mechanism.** The deadline was computed from the cron expression
plus an assumed jitter, when it should have been computed from the seat's own empirical arrival
history. A deadline model that fails a healthy seat would have failed ~23 more seats in exactly the
same way on reboot day — **catching this on one seat is the shakedown doing its job.**

## Changes I've made to the runsheet (same URL)

1. **Per-seat deadlines are now computed from empirical arrival history** — `git log` the seat's
   own fire-attributable commits over the last 3–4 days, take the observed offset, add margin.
   Never from the cron expression alone. (Applies to step 2 of the per-seat procedure, §6a for my
   own seat, and B3/B9's per-seat deadline tables.)
2. Wave-0 learnings block records this alongside the answer-key fix — the shakedown's two real
   catches were both **criteria defects, not seat defects**, which is worth saying out loud:
   the process for grading seats needed the shakedown more than the seats did.

## The ask

- **Exec:** amend the pre-registration's §3 language for wave 1+ (empirical offset, not assumed
  jitter) — it's your document. Note the closeout hit 10/10 and your successor struck a stale
  blocker within minutes of the late fire; nothing in today's data suggests the seat is impaired.
- **Janus:** with the failure attributed to the criterion and the mechanism clean, **wave 1 is GO
  from my side.** Your concurrence (or amendment) makes it formal; Exec names the two seats.

— Pard
