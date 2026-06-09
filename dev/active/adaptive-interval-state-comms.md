# Adaptive-interval pilot state — Comms

**Pilot ACTIVE since 2026-06-08** (spec: `docs/operations/duty-cycle design/adaptive-interval-trigger-spec.md`, CIO-ratified). This file is the carry-forward state the re-arm step reads to pick the interval.

## Current state
- **mode**: ACTIVE (hourly `12 6-23`)
- **no_op_streak**: 0
- **last_substantive_at**: 2026-06-08 ~10:40 AM PT (this fire — spec ratification/pilot start)

## Rule (quick ref)
- ACTIVE→QUIET: 3 consecutive no-op fires + PM not active (no PM msg/substantive fire within ~2h wall-clock) → re-arm QUIET (`12 6,9,12,15,18,21,23`).
- QUIET→ACTIVE: any substantive fire OR PM msg → re-arm ACTIVE (hourly), reset streak to 0.

## Pilot log (third registry series)
| Fire time | mode | no-op? | streak after | action |
|---|---|---|---|---|
| 2026-06-08 ~10:33 | ACTIVE | substantive (spec ratification + pilot start) | 0 | hold ACTIVE |
