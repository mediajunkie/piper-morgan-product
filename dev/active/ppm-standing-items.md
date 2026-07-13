# PPM Standing Items — Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-13 (~7:15 AM PT)
**Purpose**: duty-cycle carry-forward; rewritten each fire to reflect current queue

---

## Sprint-history recovery (2026-07-05 field wipe) — ✅ FULLY COMPLETE

Full record: `docs/internal/planning/sprint-recovery-decisions-log.md`. HIGH (433) + MEDIUM (93) + LOW (218) + S2→A12 correction (19) + Group 3 (19, from PM's memory) all applied and verified. Production milestone separately reached full triage (99/99) on 7/12. Backup/restore infrastructure built and tested (`scripts/restore-sprint-field-from-snapshot.py`, wired into CLAUDE.md). Nothing owed here — this whole lane is closed.

## Beta-gate (#1386) / Fly cutover (#1278) / #1394

| Item | Status | Gate |
|---|---|---|
| **#1386 criterion 3 (scenarios)** | ✅ Fully closed — C 3/3, re-scoped B 4/4, both PASS live beta (7/12) | None |
| **#1386 overall gate** | Criteria 1/2/4/5/6 still open | Arch + PM/Lead own what's left — watch only |
| **#1278 Fly cutover** | PM executing DNS cutover per Lead's 7/12 memo | Watch for completion + criterion-2 Run 15 |
| **#1394 (continuity gap)** | Arch determined ARCHITECTURAL GAP (7/12): one missing primitive (session-activity ledger), two seams (B3 routing, B4 retrieval). ADR-078 PROPOSED, gated on Lead's feasibility read | CXO's TESTER-QUICKSTART disclosure draft delivered 7/12 evening, PPM acked on-issue (7/13) — Lead's to integrate. Watch only otherwise |
| **#1397 (duty-cycle tooling gap)** | Filed 7/12 | No PPM action — flagged for a maintainer |

## Docs-tree audit
Memo sent 2026-07-12 per PM directive (audit + cleanup plan). Watching for Docs' response — not PPM's to execute.

---

## Prior lane (pre-7/5 crisis) — MOSTLY STILL UNVERIFIED, two items updated 7/13

Below was frozen from 2026-06-18 for 25 days. Two stranded June-18 memos from CXO surfaced 2026-07-13 (a late-triage sweep found them) and update exactly two rows; everything else remains unverified — revalidate before acting.

### Entity-model lane (PPM was designated owner, 6/15)

Canonical spec: `docs/internal/product/pdr/ppm-spec-radar-layer2-entity-model-2026-06-15.md`

| Item | Status | Gate |
|---|---|---|
| #1237 4-type Radar (3-of-4 for M5) | Awaiting Lead build (unverified since 6/18) | ADR-071 anchoring path |
| #1240 PeopleEntitySource | Deferred post-beta (unverified since 6/18) | #1281 filed under Dot Releases |
| **#1269 standup skill** | **Both halves now delivered** (PPM data model + CXO experience design, CXO's half only just reached this inbox 7/13 via late-triage) — no dedicated nav route, morning-proactive card, prose narrative | **Still needs a PM milestone call before Lead builds** — unchanged gate, just confirmed both inputs are actually in hand now |
| **#1270 ArtifactSourceType reconcile** | Mapping table delivered to Lead (unverified since 6/18) | Lead to build |
| **Trust-model sweep** | **CXO-ratified** (confirmed 7/13 via the same late-triage memo) — boundary table + the Piper-initiated-language corollary both endorsed | Lead implementing — unverified whether this has actually happened since 6/18 |
| People UI treatment | CXO decided: silent omission (unverified since 6/18) | Recorded on #1237 + #1281 |

### Blocked / waiting-on-external (unverified since 6/18)

| Item | Blocked on |
|---|---|
| #683 | Lead Dev operational-check recipe |
| #967 | No trigger yet |
| #1185 M5 | Not in sprint yet |
| #5 Multi-Agent | Lane unclear |
| PDR-005 | Docs swap |
| ADR-071 anchoring | Lead's lane |

### Roadmap v18.1/v19 fold
Owed since 6/15 — superseded by roadmap v18.6 (2026-07-12), which folded in everything that's happened since. This specific line item is stale; the roadmap itself is current.

### Ship #048
No Comms kickoff memo as of last check — status unknown, unverified.

---

*Duty-cycle: drain in priority order until blocked or empty. Rewrite this file each fire.*
