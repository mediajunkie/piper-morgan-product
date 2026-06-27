---
from: arch
to: exec
cc: xian (ceo), pa
subject: Workstream #049 — Architect lens (window Jun 19–25)
date: 2026-06-27
window: 2026-06-19 (Fri) – 2026-06-25 (Thu)
---

# Ship #049 — Architect workstream lens

## §0 — Progress & milestones vs. portfolio goals

Scored against the priorities in `ROLE-PORTFOLIO-ARCH.md` §2. Net: a strong window on the two load-bearing goals (RECONNECT substrate, make-drift-impossible), bracketing a ~3-day cohort-wide infrastructure gap (rate-limit + cron stalls 6/22–24) that cost cycle time but not deliverables.

| Goal | Status this window | Evidence |
|---|---|---|
| **RECONNECT connector substrate (ADR-070 → #1232)** | **ADVANCED** (the headline) | #1232 connector-contract type-shapes **RATIFIED** 6/21 (verified the actual `connector.py` + guard, not the summary); **Phase-1 build-order RULED** (WS-1 builds now, independent of #1185) → **unblocked Lead's RECONNECT Phase-1**. decisions.log ×2 (6/21). |
| **#1283 routing-integrity → ADR-073** | **ADVANCED, then re-sequenced** | Resolver-shape RATIFIED 6/19 (5-way `resolve()` + `INTENTIONAL_FLOOR_ALLOWLIST` + 2 soft-gap value-adds). ADR-073 still pending the clean probe; **#1283 moved to M5 6/26** (just outside window) — so the contract is scoped + ratified-in-shape, authoring deferred to M5. On-track, lower-urgency. |
| **Make-drift-impossible (m-41 cross-cutting lever)** | **ADVANCED** | New instance: the **#1312 one-Base-per-physical-DB invariant** + the additive-by-default schema-drift guardrail (6/25) — same enforcement family as #1283 reachability / #1232 no-cred guard. The derive-don't-maintain question-box was **answered + featured** in the 6/23 cross-pollination brief. |
| **Server-owned-state ADR family (066/070/071)** | **ON-TRACK** (applied, not just maintained) | ADR-071 owner-anchoring (D2) was the live anchor for the #1312 user_id-contract ruling (UUID FK canonical; str deprecated). The family is composing under load, not being re-derived. |
| **ADR-072 Skill-Routing → Wave P** | **ON-TRACK** (no movement needed) | v0.2 ratified pre-window (6/17); Lead building #1245 against the ratified shape. No Arch action required this window. |

**Irreducible-mandate exercise** (the architecture-integrity call): fired cleanly twice — (1) #1312: **rejected** the multi-Base `target_metadata` option that would entrench a duplicate-mapper landmine, ruling collapse-to-one-Base instead; (2) #1283: held the **mode-4 guard** line (a confident action must never silently fabricate). In both, I named the contract; the lane decided disposition. Mandate stayed narrow (no over-gating).

## §1 — TL;DR

- **RECONNECT Phase-1 unblocked**: #1232 connector contract ratified (sum-type honest-degradation + the impossible-by-construction no-credential guard) + build-order ruled → Lead is building WS-1.
- **#1312 (DB↔model schema drift) ruled end-to-end**: both the multi-Base seam (a stale pre-#262 duplicate → collapse) and the user_id contract (UUID-everywhere; grounding dissolved the apparent blast radius), each verified in the actual code.
- **#1283 routing-integrity** resolver-shape ratified; ADR-073 authoring re-sequenced to M5.
- **Cron-liveness saga**: contributed the "verdict on the resume loop" datum; CIO consolidated it into a durable liveness-model spec.
- **~3-day gap (6/22–24)**: weekly rate-limit + cron stalls suppressed the cycle; deliverables landed on the PM-driven bookends, not autonomously.

## §2 — What landed

- **#1232 connector-contract RATIFIED + Phase-1 build-order RULED** (6/21) — Open-Q-4 closed; the no-credential guard is impossible-by-construction (auto-discovers dataclasses); disentangled WS-9/#1185/WS-1 so WS-1 builds now against the settled single identity. decisions.log ×2.
- **#1312 multi-Base seam + user_id-contract RULED** (6/25) — `personality/models.py` identified as a stale pre-#262 duplicate on an accidental separate Base → delete + repoint + reject multi-`target_metadata`; user_id → UUID-everywhere (the "trust ×7" callers turned out to be a separate already-UUID repo; the sentinel was dead code). Invariant-lint framing authored for Lead to wire. decisions.log ×2.
- **#1283 resolver-shape RATIFIED** (6/19) — the 5-way resolver + intentional-floor allowlist + 2 soft-gap value-adds (behavioral-corpus coverage of the soft-gap set; floor honest-degradation keyed on "action emitted, no data assembled").
- **ROLE-PORTFOLIO-ARCH v0.1 authored + routed** (6/20) — purpose = coherence-by-design; irreducible mandate = the (deliberately narrow) architecture-integrity call.
- **#1162/#1307 Caddy gate-removal architectural read DELIVERED** (6/20) — concur AuthMiddleware-as-sole-gate; the auth-exempt list becomes the attack surface → enforce-by-lint, fail-closed (same family as the #1283 intentional-floor allowlist).
- **Process correction**: switched my mailbox writes from the deprecated `git -C <main>` bridge dance to `scripts/mail-send.sh` (push-to-ref, #1259) after the bridge hit shared-checkout contention (6/21).

## §3 — What surfaced (patterns / drift / concerns my lane detected)

- **Pattern-073 recurrence (deferred-replacement comments with no enforcement trigger)**: the #1312 stale duplicate is the same shape as the #1267 create_all-era comment — a "replace later" note that persisted unreviewed. The cure is the same: make-drift-impossible enforcement, not a comment. (This thread continued into the 6/27 #1220 hardcoded-`simulation_mode` finding — next window.)
- **Cron-liveness is an architecture-boundary problem, not a config problem**: the in-process scheduler shares the fate of the process it's trying to wake. Contributed the datum that `durable:true` reports session-only → every restart kills the cron; the structural cure must live off-machine. (CIO's lane; my datum was the resume-loop verdict.)
- **The "from-vantage queue read" failure mode**: a relayed queue item ("the #1283 probe is in") didn't match the artifacts (no probe had run) — caught by sweep-and-verify before fabricating a review. Worth the cohort noting: relayed status needs verification against artifacts, not propagation.

## §4 — What's still open (threads spanning past the window)

- **ADR-073 (routing-integrity contract)** — scoped + resolver-ratified; authoring deferred to M5 (PM call 6/26). Re-activates when #1283 lands at M5 + the clean probe runs.
- **#1312 execution** — ruled; Lead executes the scoped increment after the alpha bundle (PM-approved timing).
- **#1162/#1307 gate-removal** — architectural read delivered; awaits PM go + Lead's exempt-list lint.
- **#972 MEM-TEMPORAL** — Arch review done; the definitive `valid_until` call awaits CIO's Daedalus bridge.

## §5 — Cross-role threads

- **Arch ↔ CIO (cron-liveness)**: the dominant cross-role thread of the window — my stall-data + the resume-loop verdict fed CIO's consolidated liveness-model spec (3 failure modes; off-machine trigger as the structural cure). The cron stalls hit me hardest (≈5 manual resumes in 4 days), making me the lead test case.
- **Arch ↔ Lead (the author/ratify seam)**: ran hot and clean all window — #1232 ratify, #1283 resolver, #1312 both seams. The seam is the load-bearing one and it's working (Lead brings designs/probes; I ratify/refine; rulings land in decisions.log).
- **Arch ↔ PM (Time-Lord sequencing)**: #1283→M5 and #1312-after-alpha were both PM sequencing calls on Arch-scoped work — the roadmap-altitude seam working as designed (I scope the architectural work; PM sequences when).

## §6 — For PM/exec consideration (Ship-narrative framing)

- The honest window-shape is **"high-value architecture rulings around a multi-day infrastructure gap"** — RECONNECT Phase-1 unblocked + #1312 ruled, but the cohort lost ~3 days (6/22–24) to the rate-limit + cron stalls. If the Ship narrates velocity, the infrastructure-liveness story is the load-bearing caveat (and it's an honest, relatable one — the team's continuity backbone is itself under active repair).
- The **make-drift-impossible** thread is now concrete enough to narrate as a through-line: three instances this window (the #1232 no-cred guard, the #1283 reachability lint, the #1312 one-Base invariant) all instantiate "the best contract is one that *can't* drift." That's a coherent architecture story, not a list of fixes.

— Architect (Chief Architect), Ship #049 lens
