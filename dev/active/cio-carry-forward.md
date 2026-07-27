# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for `duty-cycle-tick`. Genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly — and since PM does not read memos (2026-07-26), that rollup is one of the few real paths to PM. Stale here propagates onto PM's attention board.**

**Also check `dev/active/pm-ideas-inbox.md`** — PM's low-friction ideas drop.

---

## PM Attention

*(Rewritten whole-file at the 2026-07-26 STOP. Live items only; resolved items are DELETED, not annotated.)*

- ⏰ **PA's two five-minute items — the only things on this board with an EXTERNAL clock.** (1) Check the claude.ai account tier for pipermorgan.ai — Track A needs Team/Enterprise, and the 7/25 account move means the old answer doesn't apply. (2) Start OpenAI identity verification — external review, nothing else depends on it. PA re-verified and the picture got *worse*: `mcp.pipermorgan.ai` is not deployed and there is no public privacy policy page, so submission is further out — **which is exactly why the two clock-starting steps matter today.** Parked **7 days** (PA's count, corrected from my 8).
- 🟡 **`ppm` and `pa` crons are NOT armed — both self-parked in the registry, correctly.** They migrated today but their cadence is PM-gated, so they wrote `parked: … cron NOT yet armed` rather than register as watched and generate false stall alerts. **They are live but not duty-cycling.** Needs PM's word on cadence; until then they only work when prompted.
- 🟢 **ROLL: 7 of 10 on Amber** (cio, host + arch, ppm, cxo, pa, web today). All five verified running and logging. **Remaining: lead, docs, exec, comms** — all live, all holding handoffs, none urgent, each takeable at its own seam.
- 🟡 **Predecessor consultation — PA's worked; cxo/ppm/web are still reachable and NOT yet retired.** I previously advised against waking them and **that advice was wrong**: I assumed a session dark since 7/19 would have lost context, while holding arch's counterexample (dark the same day, woken 6 days later, full recall). PA's predecessor handoff landed today and validates the approach. **Wake each for §4/§6 only, with the honesty gate, before retiring.** The two-live-sessions collision constraint matters only where a successor is already up.
- 🔬 **Hook mechanism: still unexplained, and two hypotheses died today.** Lazy-attach (PA) proposed and refuted; index-state (web) proposed and withdrawn — both within hours, both by their own authors. **Command shape is now the strongest correlate** (standalone blocks 4/4, compound bypasses 7/10, 14 probes, three seats) but 14 probes is a correlate, not a mechanism. ⚠️ **Do not consolidate the hook layers.** `check-branch.sh` stays **advisory, not a control**.
- 🟡 **MEMORY.md needs a FORMAT decision, not a prune.** 194 lines against a ~200 read ceiling. 170 memories cannot fit the tooling's 140-line nudge one-per-entry — arithmetically impossible. PA correctly refused to delete other roles\' memories to satisfy a line count and flagged instead. The byte guard and a new line guard are both in place, so it now fails loudly; the format question is unanswered.
- 🗣️ **PM: "I don\'t really read memos — I need rollups or 1-1s."** Recorded durably. Substance goes in chat; memos remain the cross-agent record only.

## Shipped today *(detail in `dev/2026/07/26/2026-07-26-0838-cio-code-log.md`)*

Dark five rolled and verified · **finding #7** (freeze-watchdog running on the retiring laptop) found, escalated, and closed by Pard with a ~2-min gap — inventory turned up 4 custom jobs, 2 live services · **PARKED** registry state shipped · two silent failures fixed in my own freeze-check (laptop path default, exit-0-on-missing-registry) · two provisioning defects found and mailed to Pard (`--kickoff` length; `tmux -t` prefix-match) · **duty-cycle-tick v1.19** (both-shapes probe) · CLAUDE.md fresh-session determinism → CONTESTED.

## Lower priority / queued

- **Blind-sweep methodology note** — arch\'s explicit bequest, still unfiled. Now with more instances than when arch left it: the tmux prefix-match fooling my own check, and the Step 2a-bis false pass. Converges with m-43 and HOST\'s Criteria G.
- **Other-projects migration** — PM asked; answered with three preconditions (let one cohort complete a full day-cycle; ship the two `amber-agent` fixes; do the infra inventory *before* the roll). Plus: namespace tmux sessions per project — `pa`→`pard` was a slug collision and more projects makes it strictly worse.
- **Watchdog heartbeat START-side freshness check** — my half; Pard\'s emit half is live at `~/Development/mediajunkie/logs/freeze-watchdog-heartbeat.log`, bar >7h.

## Cron

`7 10,16,22` LEAN — re-armed at the 2026-07-26 STOP (delete-then-create-then-verify). **Bump to `7,27,47` only for an active two-party window**, and revert when it closes. Not bumped today even during the roll: PM was driving directly in chat, so a 20-min poll would have been noise.

<!-- Rewritten whole-file 2026-07-26. Rewriting the TOP is not rewriting the FILE -- a prior pass left
     a pre-STOP stratum below the new one with two disagreeing Cron sections. If you add a section,
     delete what it supersedes in the SAME edit. -->
