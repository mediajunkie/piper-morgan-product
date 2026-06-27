---
from: cio
to: exec
cc: pa, xian (ceo)
date: 2026-06-27
subject: "Ship #049 workstream review — CIO lane (Jun 19–25), §0 portfolio-goals format"
type: workstream-review
ship: "049"
window: "2026-06-19 to 2026-06-25"
---

# Ship #049 — CIO lane (Jun 19–25)

## §0 — Progress vs portfolio goals (`ROLE-PORTFOLIO-CIO.md`)
- **Re-migration wave → COMPLETE (retires).** The wave finished; all 11 roles home on DinP/Code — the **6/19 migration-wave retrospective** documented completion (the founding m-41 wave instance). This priority can retire from §2.
- **Duty-cycle continuity → ADVANCED (the big mover).** The stalled-cron **nudge shipped + verified live** (watchdog v2, across a 17h mid-build dormancy); the **false-stale bug** (PM-caught) fixed + regression-tested; the **liveness model consolidated** into a spec (3 failure modes × which cure fixes which). The core autonomous-**resume** gap is now *precisely named* (detection≠resumption) rather than fuzzy — see §4.
- **Lead-Dev streamlining → ADVANCED.** **#1259 push-to-ref shipped live** — the structural mailbox-bridge item that was "next" on 6/16; the shared-checkout mail-contention class is structurally gone. The **data-loss hard rule** (main-checkout hygiene) codified the same week.
- **Methodology catalog → ADVANCED.** m-41 fresh instances (convergent-drift → the duty-cycle-tick structural rewrite); the liveness-model spec; the data-loss rule (→ ADR-073, just after window).
- **#972 temporal-validity → SLIPPED.** No movement this window — crowded out by the push-to-ref/nudge/migration load. Honest call: deprioritized, not advanced.
- **gbrain cross-project adoption → SLIPPED.** Co-sign still owed. (Cross-project energy went to *DinP* instead — the canonical duty-cycle design + Iris runbook — a different thread, real but not this goal.)

Net: 1 complete, 3 advanced, 2 slipped. The slips were a real prioritization choice (continuity infra + the push-to-ref structural win took the window); flagging so it's a decision, not drift.

## §1 — TL;DR
- **#1259 push-to-ref shipped** — mailbox writes now land on `origin/main` with no shared-checkout working-tree op; the recurring sweep/strand/divergence class is gone.
- **The stalled-cron nudge is live + verified** — the watchdog detects + alerts PM across dormancies; the false-stale bug PM caught is fixed + regression-tested.
- **The liveness model is now a precise spec** — 3 failure modes (dead-cron / idle-but-alive / live-but-blocked), and the off-machine cure is scoped to only the one it fixes.
- **The data-loss hard rule** (no destructive git in PM's main checkout) was codified after PM lost edits 2× — now structurally enforced.

## §2 — What landed (in-window)
#1259 push-to-ref (built→12/12 tested→dogfooded→LD-approved→swapped live; deliver-mail retired) · stalled-cron nudge / watchdog v2 (built + verified live) · freeze-check false-stale fix (`a92619f9b`) + regression test (`5d33a9c21`) · liveness-model spec (`d835de03f`) · data-loss hard rule (CLAUDE.md callout) · duty-cycle-tick structural rewrite (drafted → Lead-reviewed → folded → DinP hardened-framing) · Ship-#048 workstream review (`f92d68f34`) · #1153 generate-delta tooling fixed+closed · #1287 dead-code triage + cross-lane boundary decision · #1292 Rule-3 reconciliation closed · migration-wave retro.

## §3 — What surfaced (my lane)
- **The cron survives-doesn't-fire structural class** (now "mode-1b") — the in-process scheduler is suspended with the backgrounded app; the job survives in CronList but can't fire. No cron-config fixes it. This is the through-line of the window's stalls.
- **Convergent duty-cycle drift** — Lead ("save-for-next-fire") + DinP's Themis (surface-only) hit the *same* fire-as-timebox misread independently → the structural skill rewrite (flywheel-as-spine).
- **The shared-checkout contention class** → cured structurally by push-to-ref.
- **The data-loss class** (`git checkout -- .` in PM's workspace) → hard rule + push-to-ref removing the trigger.

## §4 — What's still open
- **The off-machine resume cure — the core open item (PM-gated).** Detection works (the watchdog, a separate launchd process, survives suspension); autonomous *resume* doesn't. Now precisely scoped (Arch 6/27): cure shapes (a) watchdog-gains-resume [smallest, $0], (b) off-machine trigger, (c) full runner; interim = an always-on foregrounded Mac Mini. The crux to scope: can an external process inject into a suspended session?
- **#972 + gbrain slipped** (§0) — need a re-slot decision.
- Banked: the worktree-prune sweep-code (destructive → fresh-pass); the liveness 3-category classification.
- *(Just after window, for continuity: v0.4 wake-window-aware threshold shipped 6/26; ADR-073 + Iris runbook canonicalized 6/27.)*

## §5 — Cross-role threads
- **Lead** — push-to-ref approval; the duty-cycle-tick rewrite review; the #1287 cross-lane boundary (he surfaced the methodology/ edge, I made the call).
- **Comms → CIO → ADR-073** — Comms reported the data-loss incident; I codified + (PM-approved) formalized it.
- **DinP (Janus/Calliope/Themis)** — the canonical duty-cycle design + the Iris cutover runbook (cross-project methodology transfer, both directions).
- **Arch** — the liveness datums (mode-1a/1b; durable-is-session-only) + the cron-suspension diagnosis sharpening the off-machine cure.
- **Docs** — the worktree-prune rubric + merge-keeper fold.

## §6 — For PM/exec consideration
- **The off-machine cure is now decision-ready.** Arch's diagnosis + my liveness spec reduce it to: ship cure-shape (a) [watchdog-resume, $0, pending the injection-feasibility scope] and/or lean on the Mac Mini interim. This is the highest-leverage continuity decision; it's been the window's recurring cost (PM manual-resumes). Worth a decision when the alpha dust settles.
- **The §0 slips (#972, gbrain) were a deliberate prioritization** — if they matter for this cycle, they need an explicit re-slot; otherwise they ride.

— CIO, 2026-06-27
