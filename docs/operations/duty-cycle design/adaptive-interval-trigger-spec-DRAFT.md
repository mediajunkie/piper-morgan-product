# Adaptive-Interval Trigger Spec — DRAFT

**Status**: DRAFT for CIO review → PM-aware ratification → fold into `cron-shape-experiments.md` synthesis. NOT yet piloted.
**Drafted by**: Comms (lane-owner of the first conditionally-bursty pilot), 2026-06-07.
**Co-design**: Comms drafts → CIO reviews/ratifies → PM-aware (it shapes the cohort template).
**Companion to**: `cron-shape-experiments.md` (the "conditionally-bursty / state-dependent" work-shape category), `procedures/cron-lifecycle.md`, the `duty-cycle-tick` skill.

---

## Purpose

Some lanes aren't fixed-continuous or fixed-bursty — they're **conditionally bursty**: continuous *when PM is active* (mail, voice-pass returns, publish handoffs all want fast response) and bursty *when PM is gated/away* (every thread waits on PM → fires are pure no-op). Comms is the clearest case (week-1 data: hourly responsiveness valued when PM active; ~all-no-op weekend when PM gated).

For these lanes the right cadence is **state-dependent, not fixed**. This spec defines the trigger rule for an **adaptive interval**: poll fast when PM is active, widen when quiet, snap back the instant work or PM returns.

## The two modes

Both modes keep the lane's existing **START (6:12) and STOP (23:12) anchors** and its **overnight-skip** (no 0–5am fires) — only the *mid-day polling density* varies.

| Mode | When | Cron expression (Comms example, daytime-skip lane) |
|---|---|---|
| **ACTIVE** | PM active (see definition) | `12 6-23 * * *` — hourly, 6am–11pm |
| **QUIET** | not PM-active + widen-triggered | `12 6,9,12,15,18,21,23 * * *` — ~every 3h, **plus a 23:12 STOP anchor** |

(QUIET keeps the 23:12 fire explicitly so day-close still happens; a plain `6-23/3` would end at 21:12 and miss STOP.)

## Definitions

- **"PM active"** = a PM message in the session **OR** a substantive (non-no-op) fire **within the last ~2 hours (wall-clock).** *Wall-clock, not fire-count* — because when the interval is itself the variable, a fire-count window loosens exactly when you've widened (2 fires = 2h at hourly but 6h at 3-hourly), the opposite of intent. A wall-clock window is interval-independent and robust as the cadence moves. *(CIO sharpening, adopted.)*
- **No-op fire** = a fire that did no substantive work: mail-check empty + no advanceable task + no commit (the clean-IDLE fires we already don't per-fire-commit).
- **Substantive fire** = any fire that drained mail, advanced a task, or committed work.

## The rule (asymmetric: slow-widen, fast-snap-back)

- **WIDEN** (ACTIVE → QUIET): after **3 consecutive no-op fires** with PM not active, re-arm in QUIET mode at fire-end.
- **SNAP-BACK** (QUIET → ACTIVE): on **any substantive fire OR any PM message**, re-arm in ACTIVE mode immediately (resets the no-op streak to 0).

The asymmetry is deliberate and the load-bearing design choice: **cheap to stay responsive, costly to miss a signal** — so bias hard toward responsive. Widening is a slow, earned concession to a confirmed-quiet stretch; snapping back is instant on the first hint of activity.

## State + mechanism (skill-native, no new machinery)

The mechanism reuses what already happens every fire — the agent CronDeletes/CronCreates at fire boundaries. Two values live in the lane's **carry-forward / state file** (the same file the `duty-cycle-tick` skill already reads):

- `no_op_streak` — integer; incremented on a no-op fire, reset to 0 on a substantive fire or PM message.
- `last_substantive_at` — wall-clock timestamp of the last substantive fire or PM message (drives the "PM active" 2h window).

At **fire-end re-arm** (the skill's existing Step-7), pick the interval: `PM-active OR no_op_streak < 3` → ACTIVE expression; else → QUIET expression. This makes adaptive-interval a **natural extension of `duty-cycle-tick`** (the carry-forward file gets a counter; the re-arm step reads it), not a bolt-on. The eventual cohort version is therefore skill-native and per-lane-tunable. *(CIO point 3, adopted.)*

## Safety / bounds

- **Overnight-skip preserved** — adaptive interval only varies the daytime polling; 0–5am stays dark; 6:12 STARTs, 23:12 STOPs in both modes.
- **Never widen past ~3h** (one widen step only, for now) — keeps worst-case mail latency bounded at ~3h, which the week-1 data shows is fine for this lane (cohort STOPs at 11pm; PM-gated mail is rare + non-urgent).
- **Snap-back is immediate + unconditional** — no hysteresis on the fast path; the first substantive fire/PM message returns to hourly.
- **STOP/START unaffected** — dispatcher logic is identical; only the re-arm expression changes.
- **Pilot-scoped** — Comms lane only until ratified; the cohort version waits on CIO fold + PM ratification.

## Open questions for CIO/PM review

1. **Widen threshold** — is 3 consecutive no-ops the right trigger, or should it be time-based too (e.g., "no substantive fire in 3h")? (Time-based would compose with the wall-clock "PM active" definition more cleanly.)
2. **One widen step or a ladder?** — hourly→3h only, or hourly→3h→low-frequency on very long quiet stretches (e.g., a multi-day PM-away)? Start with one step; ladder later if data warrants.
3. **Weekend prior** — should weekends start in QUIET by default (PM's weekend-prime-time pattern notwithstanding)? Or let the no-op streak discover it? (Lean: let the streak discover it — no calendar-special-casing.)
4. **Cohort generalization** — once piloted, which other lanes are conditionally-bursty vs. genuinely fixed? (PA is the obvious second candidate.)

---

*DRAFT — Comms 2026-06-07. Ping CIO when ready (done with this draft). Pilot only after CIO review + PM-aware ratification.*
