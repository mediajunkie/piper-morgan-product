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

### The precise root cause + the cure shapes (Arch diagnosis, 2026-06-27)

**Root cause, named precisely**: the CronCreate scheduler is **in-process**; macOS suspends the Claude process when the app is backgrounded (App Nap / background-suspension), which **freezes the scheduler's timer**. The job object survives (still in CronList — mode-1b), but nothing fires until the app is foregrounded. **No cron-config change, re-arm, or `durable` flag can fix this** — they don't un-suspend the process. (This is *why* durable-reports-session-only matters: the cron shares the fate of the process it's trying to wake.)

**The proof-of-concept is already running**: the **launchd watchdog is a *separate* process**, so it survives the suspension that freezes the in-app cron — which is exactly why it can still detect staleness. That confirms the trigger CAN live off-process; it's the existence proof for the cure.

**Cure shapes (increasing robustness), CIO lane:**
- **(a) Watchdog gains a RESUME capability** (not just nudge) — the existing launchd watchdog injects the duty-cycle prompt into the session, not only notifies PM. **Smallest change; closes the alert→resume gap directly; $0 (extends what's already running).** Open technical question: *can an external process inject a prompt into a backgrounded/suspended GUI-app session, and via what mechanism?* — that feasibility question is the crux of (a) and the first thing to scope.
- **(b) Move the trigger off-machine** — a launchd/cron job fires the tick from outside the Claude process (suspension irrelevant).
- **(c) Full off-machine runner** (cloud cron / always-on host).

**Interim (PM lever)**: an always-on foregrounded machine (the incoming **Mac Mini**) ≈ eliminates mode-1b (the process never backgrounds). Foregrounding the window helps until then; the watchdog nudge remains the safety net.

**CIO next step**: scope (a) — the watchdog-resume injection mechanism — as the smallest cure that closes alert→resume. If injection-into-suspended-session isn't feasible, (b)/(c) become necessary. This is the concrete shape of the PM off-machine decision.

### Update 2026-06-27 (later) — (a) BUILT; its scope; CXO datums; the scheduled-tasks candidate

**Cure (a) is built + deployed** (watchdog Belt 0, `dafc4904f`). Arch's decomposition (15:30) confirmed the design: "inject into a suspended session" is a category error (a suspended process can't receive input) — (a) decomposes to **(1) foreground/un-suspend the app** [launchd can: `open -b`] **+ (2) let the now-un-frozen in-process cron fire** [no injection needed; the existing cron is the resume]. Belt 0 is exactly step 1 via `open -b com.anthropic.claude-code` (osascript-activate hangs from-within + is TCC-blocked; `open -b` is Launch-Services, clean). The remaining test = "does foregrounding un-freeze the scheduler + fire promptly (next-tick vs dropped)?" — self-validates on the first real stall.

**⚠️ Belt 0's SCOPE — it fixes Mode 1b ONLY** (CXO datum, 2026-06-27). CXO hits **Mode 1a** (session *death*: `CronList` empty, two days running) — the cron OBJECT is gone, so **foregrounding can't resume a cron that no longer exists**, and the **carry-forward/session-local state is lost too** (1b keeps it). So:
- **Mode 1b** (cron survives, backgrounded): Belt 0 (foreground) resumes it. ✓
- **Mode 1a** (cron object dead / session ended): needs a **re-arm**, which is a *session action* the launchd watchdog can't do → needs either the nudge→human, or an off-machine trigger that re-creates the session. Belt 0 does NOT cover 1a.
This is the cleanest argument yet that **the cohort has both modes and (a)/Belt-0 is a partial cure** — the off-machine trigger (b/c) remains the only thing that covers Mode 1a.

**Mode-2/3 root-cause lead (CXO, actionable)**: `~/.claude/settings.json` has `autoMode.allow` entries written as **English prose, not `"Bash(git *)"` tool-pattern format** (+ `skipAutoPermissionPrompt: true`). The format mismatch may be why permitted operations still hit the approval modal (mode-2/3, live-but-blocked). Strong lead for the mode-3 upstream fix (CXO+Exec lane): correct the allowlist format → stop generating the prompt. (Settings.json is PM/env config — flag, don't unilaterally edit.)

**The `mcp__scheduled-tasks__*` mechanism (CXO surfaced it; verify-first found it's ALREADY-REJECTED, not a fresh candidate)**: tasks stored in `~/.claude/scheduled-tasks/{id}/SKILL.md`, cron or one-shot, each run **fresh + self-contained**, **app-tied** (not off-machine: "runs while this app is open; on next launch if closed"). Its catch-up-on-relaunch beats CronCreate's drop-missed-tick — BUT **`list_scheduled_tasks` shows I already tried it and PM rejected it**: `cio-duty-cycle` (same cron `7 3,10,13,16,19,22`) was **SUSPENDED 2026-06-14** — *"spawns concurrent fresh sessions (persona fork), not a wake of the live session; PM-flagged design divergence; do not re-enable without a wake-this-session redesign."* (Also piloted 6/13 as `cio-gapc-pilot-probe`.) **That persona-fork problem is exactly why the whole duty cycle uses CronCreate (wake-this-session) instead.** So scheduled-tasks is NOT a drop-in better scheduler — the catch-up benefit doesn't outweigh spawning a *second* concurrent CIO.
  - **NUANCE worth keeping for the off-machine decision (PM-input, not a unilateral re-adopt)**: in the *stalled* case specifically — the live session is frozen/suspended, so there's nothing for a spawned run to fork-conflict *with* — a one-shot `scheduled-task` that fires a resume IS already how Iris was resumed (`iris-duty-cycle-resume-2026-06-22`). So scheduled-tasks could be a **stall-recovery trigger** (spawn-a-run-when-frozen) even though it's wrong as the *steady-state* scheduler. That re-opens the 6/14-rejected design, so it's a PM call, not mine. **[Refined 6/28 — see [the off-machine scope](off-machine-resume-cure-scope-2026-06-28.md): scheduled-tasks fires only catch-up-on-app-relaunch (app-dependent), so it's a *partial* recovery option, not a true off-machine wake. The spawn-fresh lead is B1 (launchd → headless `claude -p`), which doesn't depend on the app at all.]**

### Update 2026-06-27 — the "fossil cron" robustness investigation (PM-prompted)

PM noticed HOST's cron "looks different (tells its identity each time)" + "feels durable, firing regularly," and asked why a fossil cron is so robust — "the old reptiles have tricks the new mammals forgot." Investigation:

- **It is NOT a more-durable cron by design.** HOST stalled June 26 with the whole cohort (its log: *"June 26 — no logged fires — cron stalled"*), re-armed `8ab6a203` 6/26-eve, and has been clean since — same shape as cio's `b1bb59a6`. The whole cohort stalled 6/26 and re-armed 6/26-eve→6/27.
- **Activity correlates with fragility (a real lever).** Commit counts 6/26–27: **host 10** · ppm 12 · cxo 21 · cio 48 · arch 52 · exec 61. The fragile failures hit the *busy* roles mid-work: arch's session died to "a busy signal mid-START" **even though its cron survived in CronList** (mode-1b cron-alive but session-dead). Low-activity HOST spends little time mid-work → small window to be caught when a busy-signal/compaction lands → survives. (Imperfect: cio is high-activity + alive — because PM kept re-engaging/foregrounding it. So *foregrounding* is the primary driver; activity-exposure is secondary.)
- **STRONGEST genuine-trick hypothesis — UNCONFIRMED, needs HOST's live CronList**: if `8ab6a203` is the **old hourly `2,4-23` expr** (~20 fires/day) vs the new 6×/day, that IS real robustness — 3× more fire-attempts → far higher chance one lands foregrounded. The mammals cut to 6×/day almost certainly for **token economy** (fewer LLM calls), **trading firing-frequency (robustness) for cost** — a tradeoff likely made without pricing the robustness loss. HOST's fire-log looks ~3-hourly (suggests 6×/day, not hourly), so probably not — but only its CronList expr settles it.
- **Implication for "update HOST"**: do NOT blindly modernize HOST to the 6×/day thin prompt — IF its cadence is the trick, that would *remove* the robustness. Confirm its expr first; if hourly-is-the-trick, the lesson flows backward (raise the others' firing-frequency, balanced vs token cost), not overwrite HOST. Either way the general cure (off-machine re-create for session-death; foregrounding via Mac Mini) subsumes both the activity-exposure and the cadence effects.
- **Likely root of the "different-looking prompt"**: the canonical-cron-prompt-template-**v0.7 doc is stale** (Model A / bridge / old `2,4-23` expr) — now banner-flagged. A role armed from it pre-migration would carry the heavier, identity-inline, possibly-hourly fossil prompt. (Full template rewrite = CIO follow-up.)

### Update 2026-06-28 — cure-(a)/Belt 0 FIRST-REAL-STALL VALIDATION: **FAILED** (the decisive result)

Belt 0's first real exercise (Sun 6/28 morning) **disproves cure-(a) for the cohort's multi-window setup.** The watchdog FOREGROUND-fired **4×** (06:50/07:50/08:51/09:51) while exec/arch/cxo/ppm were stale — and **the roles did NOT resume from it**: arch climbed 8h→12h and is still down (no 6/28 log); cxo only resumed at **10:17** (26+ min after the last foreground = PM's morning engagement, not Belt 0). So `open -b` *executed* but did not deliver autonomous resume.

**Diagnosis** — `open -b com.anthropic.claude-code` foregrounds the **app** (one window), but the cohort runs **each role in its own Claude Code window/session**, and macOS/Chromium throttles **background windows even while the app is frontmost** (per-renderer background throttling). So app-level foreground can't un-throttle arch's/cxo's specific background windows. (Compounding: any role at Mode 1a — dead session — can't be foregrounded back at all; Belt 0 was scoped to exclude 1a anyway.) Either way, **app-level foreground is too coarse to target a specific stalled role-window.** There's no easy fix: per-window raise needs AppleScript (hangs/TCC-blocked) or per-role distinct app instances (not the setup).

**What DID work**: detection + the **nudge backstop** (06:50 nudge exec/arch, 07:50 cxo/ppm) + dedup/cooldown (no spam). So the watchdog's detect→alert is solid; only the (a) auto-resume failed.

**Conclusion — the (a)-vs-(b)/(c) branch point is now resolved: (a) does NOT close the autonomous-resume loop → the off-machine trigger (b/c) is the necessary path.** This is the validation working as designed (self-test caught the failure before we relied on it). Honest miss: I built + recommended (a) believing the foreground would resume the cron; the first real stall shows it doesn't for multi-window.

**Next steps — both DONE 2026-06-28 (PM-approved):**
1. **Belt 0 DISABLED** (default `WATCHDOG_AUTO_FOREGROUND=0`, watchdog v2.2, deployed; tests 10/10). Nudge backstop unchanged.
2. **(b) SCOPED** → see **[off-machine-resume-cure-scope-2026-06-28.md](off-machine-resume-cure-scope-2026-06-28.md)**. **Correction to my earlier lead**: the cure must be **SPAWN-FRESH, not wake-existing** (wake-existing is what Belt-0 did → failed at window granularity). The concrete lead is **B1 — launchd watchdog → headless `claude -p` spawn**, NOT "the Iris / one-shot-`scheduled-task` shape" I cited this morning: Iris's mechanisms (durable cron / `fireAt`) are all *in-app*, so they share the **same backgrounding-suppression limit**; `mcp__scheduled-tasks__*` only fires **catch-up-on-app-relaunch** (app-dependent, not a true off-machine wake). The durable fix is **B2 — the always-on Mac Mini** (subsumes B1). **Decision pending PM**: Mac-Mini timing (build-B1-vs-wait) + approve the cheap §5 validation spike. Persona-fork remains moot for a dead/stalled role.
