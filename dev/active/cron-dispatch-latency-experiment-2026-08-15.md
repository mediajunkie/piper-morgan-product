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

## Cross-project corroboration — 2026-08-18 (Themis, Design in Product)

This finding traveled via the curation-offload trial (CIO ↔ Janus) and met a second, independent
dataset: Themis (DinP) reported their own duty cycle (schedule `3 8,14,20 * * *`, ~20 fires since
08-11) has shown the **identical ~30-minute signature** — consistent arrivals at :33–34 against a
:03 scheduled minute. Full memo:
`~/Development/designinproduct/docs/mail/memo-themis-to-janus-cc-cio-dispatch-latency-corroboration-2026-08-18.md`.

**Two details that narrow the three-way open question** ("recurring-specific, target-minute-
specific, or session-state-specific"):

1. **The signature survived a job replacement.** Themis's cron was recreated from scratch twice
   (a post-reboot re-arm, and again when the 7-day auto-expiry deleted the original — the final
   dispatch of the *old* job still arrived at 14:33 before the new one took over). Different job
   instances, same ~30-min gap. **Weakens "that particular cron's own state" as the explanation.**
2. **The sessions differ structurally.** DinP's cycle and Piper Morgan's run in different sessions,
   different repos, different activity patterns — yet the gap matches, including on Themis's own
   weekend fires (08-15/16) with no interactive activity at all. **Weakens session-state as the
   *sole* driver**, though the platform's fire-only-while-idle rule means busy-session deferral
   could still contribute in principle; Themis's own quiet-weekend data argues against it being
   necessary, not that it's impossible.

**Updated read, still honest about what's unresolved**: two independent projects, different repos,
different schedules, same ~30-minute signature — the evidence now points at **recurring-job
dispatch itself** as the locus, more strongly than a single dataset could support. **Still doesn't
settle it**: the isolating test (a recurring short-period cron vs. a one-shot at the same target
minute) hasn't been run on either side. What changed is confidence in *where* to point that test,
not whether it's still needed.
