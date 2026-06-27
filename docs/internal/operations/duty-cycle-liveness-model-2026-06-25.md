# Duty-cycle liveness model — three failure modes, and which cure fixes which

**Author**: CIO · **Date**: 2026-06-25 · **Status**: design consolidation (spec for a banked build) · **Lane**: CIO duty-cycle infrastructure

Consolidates three converging signals from 2026-06-25 so they don't blur into one undifferentiated "stall pile" (Exec's phrase). The build this specs is **quality-banked for a fresh focused pass** — it's error-sensitive watchdog infra, and the data-point senders explicitly flagged "no build tonight."

## The core insight (Exec, 2026-06-25): "stale" conflates THREE failure modes

The freeze-watcher emits one signal — *no new commits / session-log stale past threshold*. But that single signal has (at least) three distinct causes, which look **identical from the outside**:

| # | Failure mode | What's actually happening | Does the off-machine firing cure fix it? |
|---|---|---|---|
| 1 | **Dead / backgrounded cron** | Session can't fire — cron suppressed while app backgrounded (survives in CronList, never fires) | **YES** — an external trigger (launchd / GH Actions / Calendar / Slack) wakes it |
| 2 | **Idle-but-alive** | Session is fine, just between fires / legitimately idle | No — it's a **false positive**; fix = better threshold/detection (v0.4) |
| 3 | **Live-but-blocked-on-approval** | Session *can* fire but is parked on a modal tool/file-change approval prompt despite permissive env | **NO** — an external trigger lands *behind the same modal*; fix is **upstream** (stop generating the prompt) |

Evidence: CXO blocked twice on 6/25 (mode 3, PM-cleared both); Exec false-flagged (mode 2); Arch flagged (mode 1, see below). Three different causes, one alert.

**Design consequence**: the watchdog must stop treating "stale" as monolithic. It can't perfectly disambiguate from outside, but it can hedge — e.g. distinguish "cron absent from CronList" (→ mode 1) from "cron present but no fire" (→ mode 1 or 3) from "within wake-window, recent-ish" (→ likely mode 2). And the **cure for each is different** — critically, the off-machine firing cure (the PM-gated decision) **only addresses mode 1**. Mode 3 in particular is a *permissions* problem, not a *firing* problem.

## The second gap (Arch, 2026-06-25): detection ≠ resumption

Arch's cron stalled the **entire daytime window** 6/25 (none of 09:27/12:27/15:27/18:27 fired; app backgrounded; `GAP-SINCE-LAST-FIRE: 13.5h`). The 6/21 nudge belt **detected** it (Exec's 17:20 rollup flagged "Arch + CXO stalled," cohort-visible by mid-afternoon) — but **nothing autonomously resumed Arch**; PM manually resumed at 20:21.

So the loop is **detection→alert→[GAP]→manual-resume**. The nudge closes detection→alert. It does **not** close alert→resume. On the daytime side, "PM still had to manually resume after 13.5h" is the verdict: **the autonomous resume loop is not closed.** (Whether it *can* be closed on-machine is the open question — a backgrounded session can't self-resume; resumption may inherently require either an off-machine trigger [mode 1] or a human. That's the same wall, restated.)

## The off-machine firing cure — option-space (only fixes mode 1)
From #1191 (cloud-surface survey) + prior: the cloud Code surface has **no `CronCreate`**, so off-machine firing needs an external trigger. Candidates: **launchd (on-mac)**, **GitHub Actions cron**, **Google Calendar recurring event**, **Slack scheduled message**, **~$70/mo Routines**. PM's call on cost. Reframe after Exec's insight: this cure is **narrower than "fix the stalls"** — it fixes mode 1 only. Modes 2 (threshold) and 3 (permissions) need separate fixes.

## The banked build (fresh-pass trigger)
1. **v0.4 wake-window-aware threshold** — tight daytime / wide overnight (cio's flat 8h is too coarse; PM beat it at 5.4h). Reduces mode-2 false positives + tightens daytime mode-1 detection.
2. **Three-category hedged classification** in the watchdog output (CronList-presence + wake-window + gap-size heuristics) so the alert says *which* mode is suspected, not just "stale."
3. **Mode-3 upstream diagnostic** (with CXO + Exec): why is a permissive session hitting approval prompts? Identify the operation class that escapes permission mode → stop generating the prompt (cleaner than detecting the block).
4. **The resume-loop question**: can alert→resume be closed autonomously, or does it inherently need off-machine (mode 1) / human? This is the crux of the PM off-machine decision.

## Inputs
- Exec memo `live-but-blocked-failure-mode` 2026-06-25 (the 3-category insight + mode-3 root-cause Q)
- Arch memo `cron-fullday-stall-datum` 2026-06-25 (detection≠resumption; 13.5h daytime stall)
- #1191 cloud-surface survey (no `CronCreate` in cloud → external-trigger option-space)
- Prior: freeze-watcher v2 (`ba4496d66`), false-stale fix + regression test (`a92619f9b` / `5d33a9c21`)

## Update 2026-06-27 — Arch datums (mode-1 splits; `durable:true` is session-only here)

Two datums from Arch's 6/25→6/27 stalls (corroborated by CIO's own 6/26 mode-1b stall):

**Mode 1 has two distinct flavors — split them:**
- **1a — cron object dies (Gap-C)**: `CronList` goes **empty**. **Re-arm fixes it.** (Seen 6/26 overnight on some roles; 6/27 re-arms from nothing.)
- **1b — cron survives but doesn't fire (backgrounded)**: `CronList` still shows the job, no fire while the app's backgrounded. **Re-arm does NOT fix it** — the schedule is intact, the runtime can't act. (Seen Arch 6/25 full daytime; CIO 6/26 overnight — `b1bb59a6` still listed at the 6/27 resume.)

They look identical externally ("stale"), opposite local fixes (re-arm vs. nothing-local). The off-machine trigger fixes **both** — because it's external to the dying/blocked session. Triage hint for the watchdog: `CronList`-empty ⇒ 1a; `CronList`-present-but-silent ⇒ 1b.

**`durable:true` does not persist in this environment (the load-bearing datum for the off-machine decision):** `CronCreate durable:true` still reports the job as *"session-only (not written to disk, dies when Claude exits)."* So **the durable flag isn't writing to `.claude/scheduled_tasks.json` here** → **every session restart (busy-signal, compaction, crash) kills the cron**, and re-arming only buys until the next restart. Arch took ~5 restarts in 4 days — the structural reason the daytime stalls recur on him. **This is the strongest evidence yet that the waker must live *outside* the session**: an in-session cron — durable or not — cannot survive the very event (restart) that backgrounds it.

**⚠️ Implication for the Iris cutover runbook (`docs/operations/duty-cycle/` in DinP):** the runbook's **F2 fix relies on `durable:true` persisting across restarts.** If Klatch behaves like this environment (durable reports session-only), F2 is NOT actually fixed by the flag — Iris's standing heartbeat would die on every restart, and the runbook's caveat (off-machine wake = Phase 4) becomes load-bearing, not optional. **Action: have Calliope verify what `durable:true` reports on Klatch** (`CronList` after creating it — does it say "session-only" or "written to disk"?). Flagged to Calliope via the reconcile thread.
