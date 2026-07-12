# PPM Standing Items — Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-12 (~3:25 PM PT)
**Purpose**: duty-cycle carry-forward; rewritten each fire to reflect current queue

---

## Current lane: sprint-history recovery (started 2026-07-05)

Full detail and decision record: `docs/internal/planning/sprint-recovery-decisions-log.md` (append-only — do not start a new file) and `docs/internal/planning/sprint-history-recovery-plan.md` (method).

| Item | Status | Gate |
|---|---|---|
| **HIGH-confidence tier (433+ issues)** | ✅ Complete (2026-07-06) | — |
| **MEDIUM-confidence tier (93 issues)** | ✅ Complete (2026-07-06) | — |
| **LOW-confidence tier (218 issues)** | ✅ Complete (2026-07-10 evening) | — |
| **S2→A12 bulk-move (19 issues)** | Recommended, evidence documented | **PM go-ahead needed** (overwrites existing values, not blank fills) |
| **Group 3: 19 true-zero-evidence issues** | Not yet built | Build artifact whenever PM wants — last open piece of the 7/5 recovery |

## Beta-gate (#1386) / Fly cutover (#1278)

| Item | Status | Gate |
|---|---|---|
| **#1386 Scenario A/C** | Co-signed, C executed and PASSED 3/3 on live beta (7/12) | Scenario A rides PM's cutover smoke |
| **#1386 Scenario B** | Blocked by #1394 (real cross-turn continuity gap, identical alpha+beta — not a migration regression) | **PPM recommendation sent to CXO 7/12** for joint sign-off: re-scope B for this gate pass, commit #1394 before invite wave 2 |
| **#1278 Fly cutover** | PPM recommended gating against the Fly artifact (7/10), Lead endorsed (7/12); PM appears to be executing DNS cutover now | Watch for completion + criterion-2 Run 15 results |

---

## Prior lane (pre-7/5 crisis) — STATUS UNVERIFIED, do not treat as current

Everything below is carried over unmodified from the 2026-06-18 rewrite. 24 days and a full sprint-field-wipe recovery + beta-gate cycle have passed since; nothing here has been re-checked. Revalidate before acting on any of it.

### Entity-model lane (PPM was designated owner, 6/15)

Canonical spec: `docs/internal/product/pdr/ppm-spec-radar-layer2-entity-model-2026-06-15.md`

| Item | Status (as of 6/18) | Gate |
|---|---|---|
| #1237 4-type Radar (3-of-4 for M5) | Awaiting Lead build | ADR-071 anchoring path |
| #1240 PeopleEntitySource | Deferred post-beta | #1281 filed under Dot Releases |
| #1269 standup skill | Model + experience design delivered | PM milestone call needed before Lead builds |
| #1270 ArtifactSourceType reconcile | Mapping table delivered to Lead | Lead to build |
| Trust-model sweep | Delivered, CXO-ratified | Lead implementing |
| People UI treatment | CXO decided: silent omission | Recorded on #1237 + #1281 |

### Blocked / waiting-on-external (as of 6/18)

| Item | Blocked on |
|---|---|
| #683 | Lead Dev operational-check recipe |
| #967 | No trigger yet |
| #1185 M5 | Not in sprint yet |
| #5 Multi-Agent | Lane unclear |
| PDR-005 | Docs swap |
| ADR-071 anchoring | Lead's lane |

### Roadmap v18.1/v19 fold
Owed since 6/15, never actioned — likely superseded by the beta-blockers/Fly work since; revalidate before resuming.

### Ship #048
No Comms kickoff memo as of 6/18 — status unknown.

### Done as of 6/18 (for context only)
People entity-model, trust-model sweep, #1270 reconcile table, #1269 data model, #1240 deferral decision, CXO empty-door question, all 4 entity-model types, ADR-066 m-38 check, history-sidebar-is-radar resolution.

---

*Duty-cycle: drain in priority order until blocked or empty. Rewrite this file each fire.*
