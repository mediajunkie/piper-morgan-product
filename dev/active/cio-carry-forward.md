# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec\'s `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — so this section is one of the few real paths to PM.** Stale here propagates to PM\'s attention board.

---

## PM Attention

*(Whole-file rewrite at the 2026-07-28 STOP. Live items only; resolved items DELETED, not annotated.)*

- ⛔ **MIGRATION IS GATED — four PM-run items, and nothing else migrates until they land.** Three predecessor consultations (**ppm, cxo, web** — migrated 7/26 with no handoff) plus a **docs** §4/§6 refresh. PM has exact copy-paste prompts in the 7/28 artifact. Then lead/exec/comms/docs go, 2–3 at a time.
- ⏰ **PA\'s two five-minute items — the only board item with an EXTERNAL clock, now 9 days parked.** (1) claude.ai account tier for pipermorgan.ai (Track A needs Team/Enterprise; the 7/25 account move voids the old answer). (2) **Start OpenAI identity verification** — external review, nothing else depends on it. PA re-verified: no deployed MCP server and no public privacy policy, so submission is further out — which is precisely why the two clock-starting steps matter now.
- 🟡 **Five migrated roles are live but NOT duty-cycling** — arch/ppm/cxo/pa/web have no armed crons (PM-gated), all correctly parked with falsifiable clearing conditions. They work when prompted; they will not wake on their own until PM sets a cadence.
- 🟡 **`exec`\'s stall detection is knowingly exposed.** It fires 2×/day, so widening would need 25h — a dead Exec unnoticed for a day, worse than the noise removed. Left at 13h and documented rather than papered over. **Resolved only by heartbeat adoption**, which is now shipped and in the skill (v1.21).
- 🗣️ **PM 7/28 trust point, which outranks the technical items**: *"I was not consulted about skipping a crucial part of the agreed-upon process. I can\'t trust autonomy if it includes corner-cutting."* The durable rules taken from it: **do not change an agreed process without asking**, and **when a premise I have stated to PM turns out false, raise it rather than quietly working around it.** Both are now in the cron prompt, not just in memory.
- 🔬 **Hook mechanism still unexplained.** Shape is a correlate on Model A; comms found BOTH shapes ungated on Model B. ⚠️ Do not consolidate the hook layers. `check-branch.sh` is advisory; `mail-send.sh` is the real control.

## Shipped today *(detail in `dev/2026/07/28/2026-07-28-1037-cio-code-log.md`)*

**Heartbeat v1.0** + freeze-check **v0.8** + skill **v1.21** — liveness decoupled from work output, all three HOST refinements built in · **checklist v1.7 Rule 0** — verify a role is actually unreachable before entering the dark-role branch · **caught my own 7/27 threshold fix as a no-op** and fixed it at the mechanism · **handoff audit + artifact** for PM with per-role status and exact prompts.

## Lower priority / queued

- **A canonical index of which doc owns which concern.** I nearly edited a *database* migration checklist tonight because the filenames collide; only reading its heading saved it. Same class as `pa`→`pard`.
- **Something that tests a procedure\'s entry condition.** We check that rules are followed; nothing checks whether a branch should have been entered. Rule 0 is the first such check anywhere in our process docs.
- **Other-projects migration** — three preconditions given (one cohort completes a full day-cycle; ship the two `amber-agent` fixes; infra inventory *before* the roll). Plus namespace tmux sessions per project.

## Cron

⚠️ **TEMPORARILY at `7,27,47` (20-min) — job `7bc44268`, bumped 2026-07-29 07:40 for the active migration window.** PM is waiting to be told the moment exec/comms/docs reply. **REVERT to LEAN `7 10,16,22` once all three are provisioned or PM closes the window** — a 20-min cadence is for an active two-party window only, and letting it persist by inertia is the create-rule-without-a-cleanup-rule trap this lane exists to prevent.

## Cron (steady state, restore this)

`7 10,16,22` LEAN — re-armed at the 2026-07-28 STOP (delete → create → verify; exactly one job, `8bb005c3`).

<!-- Whole-file rewrite 2026-07-28. Rewriting the TOP is not rewriting the FILE. If you add a section,
     delete what it supersedes in the SAME edit. -->
