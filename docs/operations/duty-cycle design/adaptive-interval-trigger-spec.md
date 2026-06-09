# Adaptive-Interval Trigger Spec

**Status**: RATIFIED 2026-06-08 (CIO) — Comms-lane pilot ACTIVE; report data as a third registry series.
**Drafted by**: Comms (lane-owner of the first conditionally-bursty pilot), 2026-06-07; ratified by CIO 2026-06-08.
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

## Resolved questions (CIO-ratified 2026-06-08)

1. **Widen threshold** → **3 consecutive no-ops (count), NOT time-based.** The count-vs-wall-clock concern only bites when the interval varies *during* the count — but you only count toward widen *while in ACTIVE (hourly)* mode, where count == time (3 no-ops ≈ 3h). Count is consistent here and simpler. (Wall-clock was needed for "PM active" because that window spans *both* modes.)
2. **One step vs ladder** → **one step (hourly→3h)** for the pilot. Build the ladder only if a multi-day-PM-away pattern shows the 3h floor still over-polls. No speculative ladder.
3. **Weekend prior** → **let the streak discover it; no calendar special-casing.** Load-bearing reason: PM treats weekends as prime-time (xian's side-project time), so a calendar "weekend = QUIET" default would be *actively wrong*. The streak adapts to *actual* activity.
4. **Cohort generalization** → **cadence tracks current-work-shape, not role** (PPM's 6/8 bundle-vs-atom sharpening + Arch's same-fire-coherence Finding 5). See §Cohort generalization below.

## Cohort generalization — work-shape, not role (PPM bundle-vs-atom)

"Conditionally-bursty" is not a per-role label — it's **"currently bundle-shaped."** The discriminator (PPM, cross-role-validated 6/8):

- **Producing / bundle-shaped lane** — holds a shared-context bundle it's working through (a PDR burst, a narrative slate, a boundary-map). Adaptive-interval *helps*: widen when the bundle is idle/PM-gated, snap back when it's active.
- **Reactive / atomic lane** — heterogeneous mail arrives independently (PPM's lane is the negative control). **Structurally can't benefit from widening** the way a producing lane can — atomic arrivals have no "quiet bundle" to widen against; widening just adds latency to the next unrelated arrival.
- A **single role can switch shapes**: PPM is atomic *most* of the time but conditionally-bursty *while holding a PDR-burst*. So the rule keys on the lane's *current* shape, not its name.

**Implication for the cohort version**: adaptive-interval applies *while a lane is bundle-shaped*; a lane should drop back to a fixed cadence (its baseline) when it's not holding a bundle. Comms is bundle-shaped most of the time (continuous narrative/insight production), which is why it's the cleanest first pilot.

---

*RATIFIED — Comms drafted 2026-06-07; CIO reviewed + ratified 2026-06-08 (memo `memo-cio-to-comms-cc-pm-pa-adaptive-spec-RATIFIED-pilot-go-2026-06-08`). PM-aware (shapes the cohort template). Comms lane is the pilot; report pilot data as a third series in the registry. Credit: PPM bundle-vs-atom cross-role-validation + Arch same-fire-coherence Finding 5.*
