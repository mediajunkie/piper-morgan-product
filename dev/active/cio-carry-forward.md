# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly — and PM does not read memos, so that rollup is one of the few real paths to PM.** Stale here propagates to PM's attention board. Durable owed/queued items live in `cio-standing-items.md`.

---

## PM Attention

*(Whole-file rewrite at the 2026-07-27 STOP. Live items only; resolved items DELETED, not annotated.)*

- ⏰ **PA's two five-minute items — the only things here with an EXTERNAL clock, now 8 days parked.** (1) claude.ai account tier for pipermorgan.ai (Track A needs Team/Enterprise; the 7/25 account move means the old answer doesn't apply). (2) **Start OpenAI identity verification** — external review, nothing else depends on it. PA re-verified: `mcp.pipermorgan.ai` is not deployed and there is no public privacy policy, so submission is further out — **which is exactly why the two clock-starting steps matter now**, since every day they sit adds to the end of the chain rather than being absorbed by it.
- 🟢 **ALL FOUR remaining roles report migration-READY.** Lead: *"slot me anywhere, including first"* — handoff refreshed to arch\'s bar, carry-forward and registry row current, no in-flight work, ~5-min cold start. Comms, Exec, Docs likewise. **Nothing on the Piper side gates them; only PM\'s availability for first-touch approvals.** Roll **2–3 at a time, not 5** — five at once made five approval queues and 4h of dead time. Spend early approvals on "don\'t ask again"; the config dir is shared, so a rule granted in one seat spares the rest.
- 🟡 **The five migrated roles are live but NOT duty-cycling** — arch/ppm/cxo/pa/web have no armed crons (PM-gated). All five are correctly parked with falsifiable clearing conditions. They work when prompted; they will not wake on their own until PM sets a cadence.
- 🟡 **`exec`\'s stall detection is knowingly exposed, and I chose that deliberately.** It fires 2×/day, so the interim widening would need 25h — a dead Exec unnoticed for a full day, strictly worse than the noise removed. Left at 13h and documented in the registry header rather than papered over with a number that would make the file look consistent while disabling the belt for a leadership role. **Resolved only by the structural fix below.**
- 🔬 **Structural fix awaiting HOST + Exec read — a per-fire heartbeat decoupled from work output.** The watchdog infers liveness from *work*, which is legitimately bursty; the registry premise and the skill contradicted each other in writing for weeks, so a compliant quiet fire was invisible **by construction** and we were alerting on compliance (lead flagged 3× on 7/27 while alive). Interim thresholds shipped. **Not putting the heartbeat in the skill unilaterally** — it is a per-fire obligation on ten agents.
- 🟡 **cxo / ppm / web PREDECESSORS still reachable and un-retired.** Wake each for §4/§6 with the honesty gate before retiring. arch and PA both proved context survives a week dark; my earlier advice against this was wrong.
- 🔬 **Hook mechanism still unexplained.** Shape is a correlate on Model A; **comms found BOTH shapes ungated on Model B**, so the shape framing is Amber-specific. ⚠️ Do not consolidate the hook layers. `check-branch.sh` is advisory; `mail-send.sh` is the actual control.

## Shipped today *(detail in `dev/2026/07/27/2026-07-27-1037-cio-code-log.md`)*

**m-44 "Clear Is Not a Measurement" FILED** — arch\'s bequest, 9 instances, 4 roles, 2 projects · **PARK-NO-EXIT** shipped, then both HOST-found gaps closed (notified nobody; routed to parties that cannot act) · **skill v1.20** — v1.17\'s unstated precondition (the agent must be RUNNING) · **freeze-check v0.7** — asserts what it examined (Janus\'s principle, adopted) · registry reasons corrected to clearing conditions, `web` added with cadence marked UNKNOWN rather than invented · watchdog thresholds corrected off a false premise.

## Lower priority / queued

- **A cross-check that the registry\'s stated premises match the skill\'s stated rules.** Both are mine, both were in force, and they contradicted each other in writing for weeks — nothing in the system compares them. Probably the next mechanism worth building.
- **Other-projects migration** — answered with three preconditions (one cohort completes a full day-cycle; ship the two `amber-agent` fixes; infra inventory *before* the roll). Plus: namespace tmux sessions per project.
- **Watchdog heartbeat START-side freshness check** — my half; Pard\'s emit half is live, bar >7h.

## Cron

`7 10,16,22` LEAN — re-armed at the 2026-07-27 STOP (delete → create → verify; exactly one job, `d65867e8`).

<!-- Whole-file rewrite 2026-07-27. Rewriting the TOP is not rewriting the FILE. If you add a section,
     delete what it supersedes in the SAME edit. -->
