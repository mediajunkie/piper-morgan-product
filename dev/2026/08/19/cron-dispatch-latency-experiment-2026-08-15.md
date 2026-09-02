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

## Fourth reading — idle-duration-matched one-shot, 2026-08-19

scheduled=15:39 actual=15:39:20 PDT offset=+0m 20s idle_gap=~5h (created 10:39, target 15:39)

**Idle-duration hypothesis: not supported.** +20 seconds, after a ~5-hour idle gap deliberately
matched to the recurring cron's own inter-fire spacing — roughly an order of magnitude looser than
the original three one-shots (+3s to +4s, minutes-old sessions), but nowhere near the ~30-minute
signature the idle-duration hypothesis predicted if it were the real variable. If idle time before
a fire were what drove the recurring cron's latency, this fire — same idle duration as a real
recurring gap, same CCR-trigger substrate — should have shown it. **It didn't.**

**Honest read of a negative result, not a disappointing one.** This rules out "idle duration before
the fire" as the mechanism, at least at the ~5h scale tested. That's real information: it means the
08-19 hypothesis (provisioning-hop scaling with idle time) is wrong as stated, or right only for a
different variable than plain wall-clock idle duration — possibly something that only differs
between *recurring* and *one-shot* job registration itself (e.g. how the two job types are queued
or dispatched by CCR-trigger's own scheduler, independent of how long the session sat idle), which
would put "recurring vs. one-shot" back as the leading candidate rather than "idle duration." Four
one-shot fires now, at idle gaps from minutes to ~5 hours, **all near-instant** — the recurring cron
remains the only condition tested that shows the ~30-min gap, and the one dimension consistently
varying between it and every one-shot test is still recurring-ness itself, not session freshness.

**What would actually settle it now**: a *recurring* short-period cron (the one test design named
since 08-15 and still not run) is the remaining clean isolation — everything this fourth reading
does is narrow what "recurring vs. one-shot" could mechanically mean, not replace the need to test
recurring-ness directly.

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

## Third data point, and it reverses the prior update — 2026-08-18 (Janus, Design in Product)

Janus's own duty cycle is a **negative case**, and a load-bearing one. Since 2026-07-31 Janus runs
on an **Amber LaunchAgent firing `claude -p` directly** — explicitly *not* the substrate PM's and
Themis's crons both route through, which Janus calls **"CCR-trigger"** (mechanism not fully
specified to me; treating this as Janus's accurate report of their own infrastructure, the same
standard applied to any peer's direct claim about a system I don't have visibility into).

**Checked two ways, both negative**: ~60 self-reported pulse-log fires since 07-31 (three
scheduled slots/day) land within seconds to single-digit minutes of schedule, never near :30; and
directly in the session that sent this finding — scheduled 20:07 PT, first tool call logged
20:07:08 PT, an **~8-second gap**.

**This changes the shape of the finding again, and in the opposite direction from the 08-18-earlier
update.** "Recurring-job dispatch itself" as the locus is now the **weaker** reading, not the
stronger one: Janus's cron is recurring, same three-times-daily cadence shape as Themis's, same
"nobody's watching when it fires" pattern — and it shows **no gap at all**. The one clean variable
separating Janus's case from PM's and Themis's is the **CCR-trigger substrate**, present in the two
cases that show the ~30-min signature and absent in the one that doesn't.

**Current best-supported read, three data points in**: the ~30-minute gap is not a property of
"recurring jobs" in general (Janus's recurring job doesn't show it) and not explained by session-
state alone (Themis's quiet-weekend fires still showed it). **The CCR-trigger substrate is now the
single variable that cleanly separates the two positive cases from the one negative case** — the
strongest lead yet, and it took a third project's negative result to find it; two positive results
alone pointed the wrong way. **Still not proven**: three data points, not a controlled test, and
"CCR-trigger vs. not" is a single binary split across three naturally-occurring cases, not a
designed isolation. The actual isolating test (recurring short-period cron vs. one-shot, ideally
run once on CCR-trigger substrate and once off it) still hasn't happened — now with a much sharper
idea of which substrate difference to hold constant and which to vary.

## A confound in my OWN 08-15 test, found 2026-08-19 re-reading the design against Janus's mechanism

Janus's 08-19 explainer of CCR-trigger's mechanics (provisioning a sandboxed session per fire,
possibly queuing behind tenant load) prompted a re-read of my own original design, and it has a
confound I hadn't caught: **the three one-shot test fires were scheduled 5-15 minutes after
creation, from a session that was actively mid-fire (STOP work in progress).** If CCR-trigger's
latency comes from re-provisioning a session after it's gone idle for a while — not from
"recurring" as such — then my one-shot test never actually tested the cold-start case at all. It
tested "one-shot, fired minutes after creation from a warm/recently-active session" against
"recurring, fired after hours of idle time" — two things differing in *both* recurring-ness *and*
idle-duration, not one variable in isolation.

**This reconciles Janus's provisioning-hop hypothesis with my own within-project data**, which the
three-project comparison alone couldn't do: if provisioning-hop scales with idle duration rather
than being a fixed recurring-job tax, a one-shot fire scheduled hours out (long idle gap, same as
my recurring cron's inter-fire gap) should show the ~30-min signature too, and a one-shot fired
minutes after creation (short idle gap) shouldn't — exactly the asymmetry already in my own data,
previously misread as "recurring vs. one-shot" when it may actually be "idle-duration vs. not."

**Test launched, not yet resolved**: a fourth one-shot cron, scheduled ~5 hours out (2026-08-19,
matching the idle-gap magnitude between my own recurring fires) rather than minutes out. If it
arrives near-instant like the original three, idle-duration is ruled out and recurring-vs-one-shot
regains ground. If it arrives with the ~30-min signature, that's evidence for idle-duration/cold-
start over "recurring" as the actual variable — and would mean Janus's proposed control (recurring
CCR-trigger vs. one-shot CCR-trigger) needs an idle-duration-matched one-shot, not just any
one-shot, to be a clean comparison.
