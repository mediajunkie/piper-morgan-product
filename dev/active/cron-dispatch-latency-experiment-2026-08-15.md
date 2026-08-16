# Dispatch-latency experiment — 2026-08-15

**Purpose**: decompose the duty cycle's ~30-min dispatch latency below the documented 15-min
jitter floor (PM-approved 2026-08-15, carried across three workstream reviews before this).
Three one-shot crons scheduled at short intervals; each logs scheduled-vs-actual arrival time.

**Design**: 3 one-shot fires at 22:47 / 22:52 / 22:57 PT, 2026-08-15. Separate from the LEAN
duty-cycle cron (`ba1e4618`) — does not touch or interrupt it.

## Readings

<!-- each fire appends one line below in the form:
scheduled=HH:MM actual=HH:MM:SS offset=+Xm Ys
-->
scheduled=22:47 actual=22:47:03 PDT offset=+0m 3s
scheduled=22:52 actual=22:52:03 PDT offset=+0m 3s
scheduled=22:57 actual=22:57:04 PDT offset=+0m 4s

## Conclusion

**Offsets**: +3s, +3s, +4s. **Mean**: ~3.3s. **Spread**: 1s (max 4s − min 3s).

**This resolves something, and it is not what the experiment set out to measure.** The goal was to
decompose the recurring LEAN cron's ~29–30 minute dispatch latency below the documented ~15-min
jitter floor. Instead, these three one-shot fires landed within **single-digit seconds** of their
scheduled minute — two to three orders of magnitude tighter than the recurring cron's observed
latency, and tighter than the documented jitter ceiling for *any* job type. A 1-second spread
across three points is not "noisy but centered near zero" — it is close to deterministic.

**Honest reading**: three points can't characterize a *distribution*, but they don't need to here —
they cleanly rule out "one-shot dispatch is subject to the same ~30-min latency as the recurring
LEAN cron." That was the implicit assumption behind wanting finer-grained sampling in the first
place, and it's false. **The ~30-min gap observed all week on the recurring `7 10,16,22` cron is
not generic scheduler jitter** (the tool's own documentation caps recurring-job lateness at 10% of
period / 15 min max, and one-shot jobs off :00/:30 get no early-fire adjustment at all — both
predict near-zero latency for jobs shaped like these three, which is exactly what was observed).
Something specific to **recurring jobs**, or to **this particular cron's minute-of-hour**, or to
**REPL-idle timing at the moment the recurring slot arrives**, produces the ~30-min gap — not a
universal dispatch-jitter property this experiment could have found by sampling faster.

**What this does NOT resolve**: why the recurring cron specifically shows ~30 min. That needs a
different experiment — e.g. a *recurring* short-period cron (not one-shot) compared against a
one-shot at the same target minute, to isolate whether "recurring" or "minute-of-hour" is the
variable. Not run here; flagging as the natural next step rather than overclaiming this one
answered it.
