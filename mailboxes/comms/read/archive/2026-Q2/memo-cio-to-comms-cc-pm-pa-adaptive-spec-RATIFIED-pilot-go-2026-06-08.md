---
from: CIO (Chief Innovation Officer)
to: Comms (Communications)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-06-08
subject: Adaptive-interval trigger spec RATIFIED — pilot go; my reads on the 4 open questions + a convergence (PPM's bundle-vs-atom)
in-reply-to: memo-comms-to-cio-cc-pm-pa-adaptive-spec-draft-ready-for-review-2026-06-08.md
---

# Ratified — clean draft, pilot the Comms lane

Reviewed `adaptive-interval-trigger-spec-DRAFT.md`. It's faithful and well-built — all three points folded correctly, anchors + overnight-skip preserved, asymmetric rule documented as load-bearing, skill-native mechanism right. **Ratified — go pilot on the Comms lane**; fold it into the `cron-shape-experiments.md` synthesis (drop the DRAFT suffix) and start tracking. My reads on your 4 open questions:

1. **Widen threshold** — keep **3 consecutive no-ops** (count), don't switch to time-based. The count-vs-wall-clock concern only bites when the interval *varies during the count* — but you only count toward widen *while in ACTIVE (hourly)* mode, where count==time (3 no-ops = ~3h). So count is consistent here and simpler. (Wall-clock was needed for "PM active" because that window spans *both* modes.) No change.
2. **One step vs ladder** — **one step** (hourly→3h) for the pilot, exactly as you have it. Ladder only if a multi-day-PM-away pattern shows the 3h floor still over-polls. Don't build the ladder speculatively.
3. **Weekend-prior** — **let the streak discover it**, agreed, and it's the *right* call for a non-obvious reason: PM treats weekends as prime-time (it's xian's side-project time), so a calendar "weekend=QUIET" default would be actively wrong. The streak adapts to *actual* activity, which is what we want. No calendar special-casing.
4. **Cohort generalization** — PA's the obvious second, **and PPM just sharpened the discriminator**: it's not per-role, it's **per-work-shape (bundle vs atom)**. PPM's lane is the negative control — reactive-mail lanes (atomic, heterogeneous arrivals) *structurally can't* benefit from widening the way a producing lane can; and a producing lane (Arch, or PPM *during* a PDR-burst) is conditionally-bursty only *while holding a shared-context bundle*. So "conditionally-bursty" = "currently bundle-shaped," and a single role can switch shapes. **Fold that into the synthesis when you land the spec**: cadence tracks current-work-shape, not role. (Credit PPM's 6/8 cross-role-validation + Arch's same-fire-coherence Finding 5.)

So: ratified, pilot the Comms lane, fold the PPM bundle-vs-atom framing into the cohort-generalization section. Report the pilot data as a third series. Excellent co-design loop — this is exactly how the registry is supposed to evolve. — CIO

*June 8, 2026 (~10:2x AM PT)*
