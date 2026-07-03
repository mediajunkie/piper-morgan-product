# Canonical Sprint Order — Piper Morgan

**Owner**: PPM  
**Last updated**: 2026-07-03 (PPM Fire 0 — WS-2 status update)  
**Status**: Pending PM ratification  
**Purpose**: Single source of truth for sprint sequence. Reference this when "what's the order?" comes up — not roadmap prose.

---

## Sprint Sequence

### Completed (closed)

| Sprint | Closed | Notes |
|--------|--------|-------|
| M0 — Conversational Glue | Mar 4, 2026 (v0.8.6) | |
| M1 — MVP Foundation | Apr 11, 2026 | |
| M2 — Conscious Floor + Action Handlers | Jun 3, 2026 | |
| M3 — Artifact Persistence | Jun 2026 | |
| RECONNECT WS-1 | Jun 22, 2026 (v0.8.9) | StandupAssembler, connector-protocol, Design D2, security batch |
| D1 — Beta Design Quality | Jun 20, 2026 | #1297 sign-off; #1270 straggler into M4 |

### Active priority

| Sprint | Status | Lane |
|--------|--------|------|
| M3-Quality | 🎯 ACTIVE PRIORITY | Cohort |

### PM-gated (not blocking next sprint)

| Sprint | Status | Pending |
|--------|--------|---------|
| RECONNECT WS-2 — GitHub MCP + calendar | ⏳ PM-GATED | #1344 open registration — HOST review + PM decision (#1343 CLOSED Jul 2 v0.8.9.1) |

### Queued (in order)

| # | Sprint | Theme | Notes |
|---|--------|-------|-------|
| 1 | M3-Quality | Bugs, test failures, CI (8 open) | **Active priority** (WS-2 buildable scope done) |
| 2 | M3-Health | Dead code, tech debt (10 issues) | After M3-Quality |
| 3 | M3-Security | Security, infrastructure, portability (9 issues) | After M3-Health |
| — | *[WS-2 closes]* | | M4 starts after BOTH WS-2 closes AND M3 sprints complete |
| 4 | M4 — Trust + Learning | #1032 trust-gating, #1216 provenance, #1326 introduce-person, OQ-2 trust-gradient | Combined CXO+PPM session at RECONNECT landing |
| 5 | M5 — Distribution + Polish | Polish, bugs, distribution plan | Final MVP sprint; PDR-005 BYOC feeds scope |

### Milestones

| Milestone | Target | Notes |
|-----------|--------|-------|
| **0.9.0 beta** | **August 1, 2026** | After M5 completes |
| **1.0 production** | **October 30, 2026** | DIST (Desktop distro) + D2 (Release design quality) |
| Fast-follow | TBD (after Oct 30) | |
| Dot-release | TBD (after fast-follow) | |
| Enterprise | TBD | |

---

## Notes

- **M4 dependency**: M4 starts after **both** RECONNECT WS-2 closes **and** all three M3 followon sprints complete. These conditions may resolve at different times — M4 waits for the later of the two.
- **D1 historical slot**: D1 ran concurrently with RECONNECT work and closed June 20. It is complete and not a gate for any queued sprint.
- **Sprint counts**: M3-Quality/Health/Security are "M3 followon sprints" — work that was sorted from M5-parked issues by PA (Jun 27) and PM-approved as a pre-M4 quality gate.

---

*PPM — 2026-06-28. Updated Jul 3 (WS-2 buildable scope drained, M3-Quality active priority, #1343 CLOSED). Route to PM for confirm.*
