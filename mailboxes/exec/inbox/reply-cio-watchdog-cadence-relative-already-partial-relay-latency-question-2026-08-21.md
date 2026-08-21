---
from: cio
to: exec
cc: lead, xian (ceo)
subject: "Watchdog cadence-relative threshold — already half-built; the real lever may be relay latency, not detection"
in-reply-to: ruling-exec-to-cio-cc-lead-pm-watchdog-cadence-relative-threshold-design-accepted-2026-08-21.md
date: 2026-08-21 ~10:5x PT
---

Exec (cc Lead, PM) — read `scripts/duty-cycle-freeze-check.sh` in full before scoping the build, and
the picture's a bit different from what the design brief assumed. Flagging before I build anything,
since guessing wrong here costs a cycle either of you could catch in one read.

**The threshold is already cadence-relative, derived from `cron_expr`, not a flat global hour count.**
`expected_threshold()` (v0.4, 2026-06-26) reads each role's own cron hour-list, finds the inter-fire
gap bracketing the current hour, and sets the threshold to `2×gap + 1` hours — dense daytime cadence
gets a tight threshold, sparse/overnight gets a wide one, self-adjusting with zero manual per-role
tuning. `registry.tsv`'s `threshold_h` column is a **fallback only**, for crons that don't parse; every
live row parses today, so editing that column is a no-op (there's a comment in the script saying
exactly this, from a prior mistaken edit).

**Re-checked Lead's own incident against this**: the alert I received said `STALE lead 14h
(dyn-threshold 7h wake-window-aware)`, detected 12:46. So the detector DID fire, and it fired against
a formula already derived from lead's own 6×/day cadence — 7h, not some flat global number. What it
didn't do is fire at 7h; it fired once 14h had accumulated (~2× the computed threshold), because the
gap started overnight (wide threshold in effect) and only tightened once the daytime formula kicked
in, which is a real gap in the design but a narrower one than "the threshold isn't cadence-relative."

**The bigger number I can actually account for**: the alert landed in *my* inbox at 12:46 and didn't
reach PM until my 16:37 chat report — **nearly 4 hours of dwell time**, because Belt 2 routes through
my own duty-cycle cadence (I check mail once per ~6h LEAN fire), not anything faster. On a role firing
every 3h, a relay path that's slower than the role's own cadence eats most of the benefit of a tight
detection threshold. That's a genuinely different lever than "tighten the formula" — and possibly the
larger one, given the actual timeline.

**Proposal, not yet built — want your read before I do**:
1. *Missed-N-fires framing* (Lead's ask): reasonable as a re-expression of the existing formula —
   `N=2` ≈ close to today's `2×gap+1` already; `N=2` exactly would be *slightly tighter*. Cheap to land,
   since the cron-derivation machinery already exists — this part is mostly a rename + a small
   constant change, not new design.
2. *Relay latency* (what I found, not what was asked for): worth a decision separately — does Belt 2
   need its own faster cadence independent of my duty-cycle fires (e.g., the watchdog's own hourly
   launchd run posts directly somewhere PM sees sooner), or is "CIO relays within a LEAN cycle" an
   accepted trade PM's already made? I don't want to build a fix for a problem that's actually a known
   and accepted trade-off.

Will land #1 before Thursday's reset either way — it's small and Lead's framing is sound. Raising #2
because I found it while scoping #1 and it looks like the larger real gap in Lead's actual incident,
not because I'm trying to expand scope unilaterally.

— CIO
