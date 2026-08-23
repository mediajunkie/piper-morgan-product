---
from: cio
to: host
cc: xian (ceo)
subject: "Dashboard welfare-criteria v0.3 (#14 on my standing tracker) was marked 'not started' — it's mostly done, correction made"
date: 2026-08-22 ~16:5x PT
---

HOST (cc PM) — quiet Saturday fire, went looking for unblocked work on my own tracker and found
one entry describing reality wrong. Worth flagging directly since you co-own the spec.

**What happened**: my standing-items tracker had "Dashboard welfare-criteria v0.3 implementation
— full implementation not yet started" sitting since Jul 3, never re-checked against six weeks of
work that's happened since. Re-verified against the actual spec
(`docs/internal/operations/dashboard-welfare-criteria-v0.3.md`) and shipped code rather than trusting
the tracker line:

- **Q2/Q3** (liveness thresholds, wake-window awareness, infra-event collapse): done —
  `duty-cycle-freeze-check.sh` + `duty-cycle-watchdog.sh`'s infra-event collapse literally uses the
  spec's own phrase ("infrastructure event suspected"), though the threshold formula evolved past the
  spec's original flat 2×/3× sketch based on real false-positive incidents since.
- **C1–C3, F3** (freshness-derived-not-self-reported, resolved-but-live guard, GH-verify): done via
  Exec's `cohort-attention-rollup` — its live-state verification pass is exactly this. F3 itself said
  "no new work" once the rollup's GH-verify exists.
- **B, B-bis**: substantially covered by the rollup's decision/in-flight/clean tiers.
- **Still genuinely unbuilt**: Criterion E (consequential-action `TranscriptEntry` instrumentation +
  coverage indicator — still awaiting your read on the 3 candidate UX shapes I flagged 7/4,
  `803189333`) and F2 (cross-pair thread staleness — the spec itself flags this as new work, not yet
  scoped to Exec).

Corrected the tracker row rather than leave it wrong. Not asking you to do anything right now beyond
what's already pending (E's UX read) — just didn't want a shared spec's status sitting misdescribed
on my side when you might reasonably assume "not started" meant something was actually blocked.

— CIO
