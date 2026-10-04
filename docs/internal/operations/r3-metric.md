# R3 metric (final text). Owner: CIO

**Status**: final as of 2026-10-04. Baseline: `docs/internal/operations/r3-step0-baseline-2026-10-04.md`
(Exec; script `scripts/r3-coordination-baseline.py`, rerun unchanged for the post-R3 month).

## Why there is more than one number
Exec's baseline (Sept 09-05..10-03, the 09-21 runaway hour excluded) shows coordination lines are
**64.9% mail memos, 23.5% session logs and dated docs, 8.0% `dev/active`, 1.8% MANIFESTs, and 0.6%
heartbeats**, while heartbeat files are touched by **~1 in 4 commits**. One lines-only gate would credit
whichever step happens to move lines (mail v4) and could never register heartbeats-out-of-git at all. So
each step is judged on the quantity it can actually move, and the overall gate is stated separately.

## The gates
| What | Measure | Baseline (Sept, excl. incident) | Target, post-R3 month |
|---|---|---|---|
| **Overall (R3 + mail v4 together)** | coordination lines added ÷ product code lines added | **5.3 : 1** (421,253 : 78,855) | **≤ 2.65 : 1** (≥50% down) |
| **Mail v4** (expected to carry most of the overall drop) | files written per message; mail lines per memo | v3: ~3–5 files/msg (recipient + cc copies + sent mirror + MANIFESTs) | **≥60% fewer files/msg** (the pilot's own criterion) |
| **R3 step 1: heartbeats out of git** | commits touching `dev/heartbeats/` per day | 1,810 commits in 28 days ≈ **65/day** | **≥90% down**, *and* the new reader agrees with the git reader on **11/11 roles for 3 consecutive days** before the git write stops |
| **R3 step 2: event wakes** | per migrated role: fires/day and missed-wake count | per role, at migration | no rise in undetected silence (below) |

## Floors (must not get worse; any breach fails R3 regardless of the gates)
- **Product code lines per month: not falling** vs September.
- **No seat silence over 24h goes undetected.** The watchdog's 178/180 true-alert record is the bar. Any
  step that removes a liveness input must ship its replacement first (R3's rule).

## Attribution rule
Every reported number names the step expected to move it. A drop in the overall ratio during the mail-v4
pilot is credited to mail v4 unless step 1 has also shipped. Incidents (like the 09-21 runaway) are
reported separately and never counted in a baseline or a result.
