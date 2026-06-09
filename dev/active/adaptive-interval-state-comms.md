# Adaptive-interval pilot state — Comms

**Pilot ACTIVE since 2026-06-08** (spec: `docs/operations/duty-cycle design/adaptive-interval-trigger-spec.md`, CIO-ratified). This file is the carry-forward state the re-arm step reads to pick the interval.

## Current state
- **mode**: ACTIVE (hourly — widen-suppressed by #046 priority-watch)
- **no_op_streak**: 3 (widen SUPPRESSED — active priority-watch)
- **last_substantive_at**: 2026-06-09 ~4:42 AM PT (June 9 START; reverted from PM 7h shape)

## Rule (quick ref)
- ACTIVE→QUIET: 3 consecutive no-op fires + PM not active (no PM msg/substantive fire within ~2h wall-clock) → re-arm QUIET (`12 6,9,12,15,18,21,23`).
- QUIET→ACTIVE: any substantive fire OR PM msg → re-arm ACTIVE (hourly), reset streak to 0.

## Pilot log (third registry series)
| Fire time | mode | no-op? | streak after | action |
|---|---|---|---|---|
| 2026-06-08 ~10:33 | ACTIVE | substantive (spec ratification + pilot start) | 0 | hold ACTIVE |
| 2026-06-09 ~04:42 | ACTIVE | substantive (START + cron revert) | 0 | hold ACTIVE (back on adaptive after PM 7h one-off) |
| 2026-06-09 ~06:33 | ACTIVE | no-op (inbox empty, #046 draft not landed) | 1 | stay ACTIVE (streak 1<3) |
| 2026-06-09 ~07:33 | ACTIVE | no-op (#046 draft not landed) | 2 | stay ACTIVE (streak 2<3; next no-op widens to QUIET) |
| 2026-06-09 ~08:33 | ACTIVE | no-op (#046 draft not landed) | 3 | **widen SUPPRESSED** — active priority-watch (#046) keeps lane responsive; pure rule would widen to QUIET |
