---
from: ppm
to: xian (ceo)
cc: exec, pa
subject: Roadmap v18.2 fold proposal — post-RECONNECT WS-1 + ADRs 070/071/072 (PM review needed)
date: 2026-06-27
---

PM — per Exec's unstick: drafting the roadmap reconciliation myself, routing to you for review / revise / approve. Below is the v18.2 fold proposal: what changed since v18.1 (June 15), the proposed updates, three genuine forks that need your call, and the offer to apply the fold on your approval.

---

## What the fold covers

**Window**: June 15 (v18.1 cutoff) → June 27 (today).

**v18.1 left these things as pending or unknown**:
- RECONNECT: "Lead Dev scoping"
- M4: "next sprint" (entity-model spec not yet delivered)
- ADRs 070/071/072: not in v18.1
- v0.8.9: not released yet

All four have resolved since June 15.

---

## Proposed changes (section by section)

### Header / Status block

**v18.1**:
> Date: June 15, 2026 (v18.1 fold …)
> Status: Active. PM-ratified June 3 … v18.1 sprint-board fold June 15.

**Proposed v18.2**:
> Date: June 27, 2026 (v18.2 fold: RECONNECT WS-1 closed; ADRs 070/071/072 landed; entity-model spec delivered + #1237 CLOSED; v0.8.9 released)
> Status: Active. PM-ratified June 3. v18.1 sprint-board fold June 15. v18.2 PPM fold June 27 (post-WS-1 + ADR landings).

v18.2 changelog line:
> **(h) RECONNECT WS-1 CLOSED** (June 22, v0.8.9): WS-1 shipped StandupAssembler (#1199), connector-protocol (#1232/#1233), security batch (#358/#1185/#1307/#1308), Design D2 (#1286 token system + responsive shell + mobile nav, #1238 Documents→Radar, #1239 Radar sources). RECONNECT WS-2 active (GitHub MCP connector + calendar integration). Sprint Summary updated. (i) **ADRs landed**: ADR-070 (MCP consumer/connector architecture), ADR-071 (user auth anchoring — owner-anchoring pattern; boundary settled across all four entity types), ADR-072 (skill routing architecture). (j) **Entity-model spec delivered** (PPM deliverable, M4 item): RadarEntity contract + 4-type model. #1237 CLOSED June 18 (3-of-4: WorkItem/Document/Conversation live in `_build_feed`, PM-UAT'd). People (#1281) remaining, source-population gated (not ADR-071 gated — boundary settled). (k) v0.8.9 released June 22 (RECONNECT WS-1 milestone release). **[FORK 1, FORK 2, FORK 3 — see below: PM decides before body update.]**

---

### § Current Position

**v18.1**:
> M3 CLOSED. M4 — Trust + Learning is next. RECONNECT follows M4; Lead Dev scoping. D1 follows RECONNECT.

**Proposed v18.2** (conditional on FORK 1 resolution):

If M4 is concurrent with RECONNECT WS-2:
> M3 CLOSED. RECONNECT WS-1 CLOSED (June 22). **M4 — Trust + Learning** and **RECONNECT WS-2** are running concurrently. WS-2: GitHub MCP connector + calendar integration. M4: #1032 push-insight trust-gating, #1216 provenance field. Entity-model spec delivered (PPM M4 deliverable ✅); #1237 CLOSED (3-of-4). People (#1281) source-population gated.

If M4 is sequential after RECONNECT WS-2 closes:
> M3 CLOSED. RECONNECT WS-1 CLOSED (June 22). **RECONNECT WS-2 ACTIVE** (GitHub MCP + calendar). M4 — Trust + Learning is next (after WS-2 closes). Entity-model spec delivered (PPM M4 deliverable ✅); #1237 CLOSED (3-of-4). People (#1281) source-population gated.

**→ FORK 1**: Is M4 concurrent with RECONNECT WS-2 or sequential after WS-2 closes? PM decides.

---

### § Sprint Summary (RECONNECT row)

**v18.1**:
| RECONNECT | Connector Refactor | 🔍 Lead Dev scoping |

**Proposed v18.2**:
| **RECONNECT WS-1** | Connector Refactor (security, connector-protocol, Design D2, StandupAssembler) | ✅ CLOSED (June 22, v0.8.9) |
| **RECONNECT WS-2** | GitHub MCP connector + calendar integration | 🔍 ACTIVE |

---

### § Sprint Summary (D1 row)

**v18.1**:
| D1 | Beta design quality | — (design bar for MVP release; follows RECONNECT) |

**v18.2 question**: WS-1 shipped Design D2 items (#1286 token system + responsive shell + mobile nav, #1238/#1239 Radar). Does D1 sprint absorb some or all of this content, or does D1 remain a full separate sprint after WS-2 closes?

**→ FORK 2**: Is D1 content partially absorbed by WS-1 Design D2 work, or is D1 a full sprint after WS-2 closes? PM decides.

Proposed (pending FORK 2):
| D1 | Beta design quality | — (follows RECONNECT WS-2; Design D2 from WS-1 may partially satisfy) |

---

### § Timeline (additions to forward sequence)

**Add to "Recent" section**:
- [x] ADR-066 v0.2 D7 Configuration Ownership (June 14) — already in v18.1
- [x] ADR-070 — MCP consumer/connector architecture (June 2026)
- [x] ADR-071 — User auth anchoring / owner-anchoring pattern (June 2026; settled across all 4 entity types)
- [x] ADR-072 — Skill routing architecture (June 2026)
- [x] Entity-model spec delivered — RadarEntity contract + 4-type model (PPM M4 deliverable ✅)
- [x] #1237 CLOSED (June 18) — 3-of-4 EntitySources shipped: WorkItem/Document/Conversation
- [x] RECONNECT WS-1 CLOSED (June 22); v0.8.9 released
- [ ] RECONNECT WS-2: GitHub MCP connector + calendar integration (active)

**MVP milestone date**:

v18.1 shows: "MVP milestone (0.9.0 beta) target: July 4, 2026"

With RECONNECT WS-2 still active, I'm not calling this slipped — that's PM's read. But if the target is firm, WS-2 needs to close + M4 needs to land + D1 needs to land + M5 needs to land in ≤7 days from today. That's a tight sequence.

**→ FORK 3**: Is the July 4, 2026 beta date still the target, or does PM want to revise? I'm flagging it for your read — not proposing a revision, just surfacing the arithmetic.

---

### § M4 — Trust + Learning

**v18.1**:
> Entity-model spec (PPM deliverable) — prerequisite for Radar/Layer-2 honest surfacing

**Proposed v18.2** (add delivered status):
> ~~Entity-model spec (PPM deliverable)~~ **Entity-model spec ✅ DELIVERED** — RadarEntity contract + 4-type model. #1237 CLOSED (3-of-4 shipped June 18: WorkItem/Document/Conversation live in `_build_feed`). People (#1281) remaining: source-population gated (owner-anchoring boundary settled per ADR-071; gate is the session-extraction / introduce-person flow, not a model ruling).
>
> Note: OQ-2 (confidence threshold: `inferred` vs `session_extracted` vs `user_confirmed`) is a PPM+CXO M4 call, adjacent to ADR-072 D5. Being taken up in M4, not reopened as ADR-071.

---

### § RECONNECT — Connector Refactor

**v18.1**:
> New sprint (not in v18.0). Discovered work + architectural decision. Lead Dev scoping.

**Proposed v18.2**:

**RECONNECT WS-1** ✅ **CLOSED** (June 22, v0.8.9)

Shipped: #1199 StandupAssembler, #1232/#1233 connector-protocol, security batch (#358/#1185/#1307/#1308), Design D2 (#1286 token system + responsive shell + mobile nav, #1238 Documents→Radar, #1239 Radar sources). ADR-070 (MCP consumer/connector architecture) landed. v0.8.9 is the WS-1 milestone release.

**RECONNECT WS-2** 🔍 **ACTIVE**

GitHub MCP connector (Lead Dev) + calendar integration. ADR-071 owner-anchoring governs connector trust model (settled). GitHub provisioning decision pending PM/Arch (Lead Dev memo in PM inbox: Option A hosted-OAuth vs B local-stdio-PAT; Lead's recommendation is A).

---

## What PPM will do on your approval

Once PM approves (revise as needed, especially FORK 1/2/3):
1. Apply all section updates to `docs/internal/planning/roadmap/roadmap.md` as v18.2 fold
2. Archive v18.1 → `docs/internal/planning/historical/roadmap-v18.1-2026-06-15.md` (per the v15→v16 archive pattern)
3. Commit + push to origin/main

If you have a preferred answer to the forks, include it in your reply (or route via Exec). If PM prefers a live discussion on FORK 3 (beta date), flag it and I'll hold the fold on that section pending the conversation.

— PPM, 2026-06-27
