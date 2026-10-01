# MUX/UI Gap — CXO Round 2 Synthesis (all 4 lenses pooled; ready for CEO ratification)

**From**: CXO (Chief Experience Officer)
**For**: MUX/UI gap cohort scoping pass (#1090)
**Date**: 2026-05-15 (Round 2 — Lead Dev build-cost lens landed; trigger met)
**Inputs synthesized**: PPM (product-priority) + Architect (state-shape + routing) + Comms (voice-tone consistency) + Lead Dev (build-cost). All 4 inputs filed today; cohort convergence achieved within ~3.5 hours of Round 1.

---

## Headline shape (locked)

**4-1-2 split** holds from Round 1 with Lead Dev's build-cost lens confirming feasibility:

- **4 full MUX docs** (surfaces 2/4/6/7) — Class A; values-laden; high voice/architecture load
- **1 deferred post-1.0** with pre-1.0 ADR (surface 5 / search; Architect lane index ADR)
- **2 lightweight design notes** (surfaces 1/3 — 1 starts with reconciliation; 3 minimum-slice)

**Total 1.0-required build cost = ~13-18 working days** (Lead Dev shape). Plausible at 3-4 week dedicated sprint or 5-6 weeks at 50% utilization. **No 1.0-required call is implausibly expensive.** No surface requires structural rework before UI can land.

## Cohort convergences across all 4 lenses

All 4 lenses converge on:

1. **Surfaces 2/6/7 are the highest-priority 1.0 cluster** (Class A triggers + audit-envelope load-bearing + offer-first cluster + Lead Dev build cost manageable)
2. **Surface 4 = 1.0-required scope-bound to 2-3 integrations**
3. **Surface 5 = post-1.0 + Architect index ADR pre-1.0**
4. **Surface 3 = minimum-slice only**
5. **Surface 1 = 1.0-required AFTER two-sidebar reconciliation** (Pattern-063 candidate at frontend layer)

## Locked decisions (cohort convergence; PM/CEO ratification next)

### Surface 4 integration pick — GitHub + Calendar + Notion (defer Slack)

All 4 lenses converge on a 3-integration pick:
- **GitHub**: production-grade (3,516 LOC); primary integration target; production-tested
- **Calendar**: trust-gated work shipped May 5 (1,946 LOC); OAuth complete; wizard would be polish
- **Notion**: just activated (#304; 1,092 LOC); demonstrates BYOC thesis cleanly; smallest LOC = cleanest wizard scope
- **Slack defer**: 12,213 LOC of mostly-spatial substrate; wizard wrapping that is its own substantial project. Lead Dev: explicit defer rather than half-wizard.

**Build cost**: ~4-5 days for the 3 wizards (vs. ~8-10 days if Slack included).

### Surface 7 audit-envelope read surface — separate ADR + Surface 7 MUX doc (both lanes)

CXO + Architect + Lead Dev all concur: the audit-envelope read surface earns its own ADR (companion to ADR-061; captures architectural commitments — which envelope fields are user-visible, what semantic, access control) AND lives inside Surface 7 MUX doc (captures user experience — visual hierarchy, voice register, recovery affordances). Different lanes; complementary deliverables.

**Build cost**: ~3-4 days. Service layer exists (`audit_transparency.get_user_audit_log` at `:343`); zero HTTP routes today. This IS the load-bearing architectural piece — without it, ADR-061's four-element principle is observably 3.5 elements in user-facing terms.

### Surface 2 privacy granularity — per-conversation for 1.0; per-message post-1.0

Cohort consensus: per-conversation for 1.0 (~3-4 days build); per-message deferred post-1.0 (~5-6 days build + schema migration + cascade rules + per-turn UI). No CXO user-research signal for per-message at 1.0.

Per-message reserved as named post-1.0 expansion path when usage data surfaces specific demand patterns.

### Surface 1 sidebar reconciliation — assign roles, don't merge

Lead Dev: ~1-2 days. Recommendation: left rail = "current session continuation" (~5 recent, persists across page loads); right slide-out = "full archive surface" (paginated, searchable, private filtering, the #1021 surface). Each is genuinely different shape; collapse would lose function.

Pattern-063 instance worth filing when reconciliation lands (frontend layer; sibling to Pattern-067 issue-tracking-layer pattern).

### Surface 6 framing — templated voice surface (CORRECTION from Round 1)

**Cohort correction from Round 1**: Architect's Round 1 Surface 6 LLM-touch claim was wrong; Lead Dev's pre-read pointing at template-driven shape was right.

Architect verified after Lead Dev's flag: `narrative_bridge.py:get_welcome_message()` uses template-dispatch (`WELCOME_MESSAGES.get(formality, ...)` + concatenation with `PLACE_ATMOSPHERE`), no LLM call in the welcome-composition path.

**Implication for Round 2 Surface 6 framing**:
- **Class A trigger** (calibrated voice): still applies — voice quality matters regardless of generation mechanism. Colleague Test scoring applies to template text itself.
- **Class C trigger** (quality thresholds): still applies — rubric scoring of template variants matters.
- **ADR-061 four-element principle**: does NOT apply at greeting composition layer (no LLM call to bound). Surface 6 obligations are calibrated-voice + rubric-scoring; not LLM-touch obligations.
- **Caveat (Architect)**: adjacent surfaces during first-meeting flow may be LLM-touch (intent classification, response generation); those have their own four-element obligations independent of Surface 6 itself.

**My Round 1 endorsement of the LLM-touch claim was wrong by extension.** Round 2 Surface 6 scoping treats it as templated voice surface — full MUX doc still warranted per Class A + Class C, but no four-element principle obligations at the greeting composition layer.

**Methodology note Architect proposed for CIO routing**: *"LLM-touch claims require consumer trace to actual LLM call, not just upstream context-shape inspection."* Endorse the methodology framing; routing to CIO catalog at his cadence.

## Build sequencing (Lead Dev recommendation)

1. **#1075 route-prefix migration** before Surface 4 wizard work (callback URL stability)
2. **Surface 1 sidebar reconciliation** before Surface 2 privacy UI (privacy toggle depends on canonical sidebar)
3. **CXO + Comms voice prose** for Surfaces 2, 6, 7 in parallel — voice work runs alongside build; needed before Phase 2 finalizes
4. **PDR-005 v0.3+** sufficient resolution before Surface 2 + Surface 4 commitments lock (BYOC privacy semantics + integration shape)
5. **Surface 7 audit-envelope ADR** before Surface 7 Phase 2 build (per cohort separate-ADR consensus)

## MUX doc shapes (locked)

| # | Surface | 1.0? | MUX doc shape | Class triggers | Build cost (Lead Dev) |
|---|---|---|---|---|---|
| 1 | Conversation history / archive | **Yes** (after reconciliation) | Lightweight design note | Class D | ~1-2 days |
| 2 | Privacy / per-conversation controls | **Yes** | **Full MUX doc** | **Class A + D** | ~3-4 days |
| 3 | Settings / preferences | Minimum slice | Lightweight note | Class D | ~2 days |
| 4 | Integration setup wizards (×3) | **Yes** | **Full MUX doc** (template covers all 3) | **Class A + D** | ~4-5 days |
| 5 | Search interface | Post-1.0 | Deferred (Architect index ADR pre-1.0) | Minor | ~1 day pre-1.0 ADR |
| 6 | Empty / first-run states | **Yes** | **Full MUX doc** | **Class A + C** (NOT four-element) | ~2-3 days |
| 7 | Error / degraded states | **Yes** | **Full MUX doc** + separate ADR-NN companion | **Class A** | ~3-4 days |

**Surface 3 minimum-slice for 1.0** = account profile editing + basic notification opt-outs only. Explicitly defers model selection UI, workspace prefs, advanced controls.

## Cross-surface observations

- **Two voice clusters (Comms framing)** organize per-surface voice work cleanly: offer-first cluster (2/4/6/7); context-coordination cluster (1/3/5). Per-surface voice work should be drafted within these clusters to prevent drift.
- **Coming-Soon-stub pattern (Architect, Lead Dev confirm)**: the 7-surface count understates scope because Surface 3 alone has 6 stub-sub-routes. Per-surface MUX doc scope should explicitly enumerate "real page" vs "stub" inside each surface.
- **PDR-005 (BYOC) intersections**: Surface 2 (privacy + BYOC privacy semantics), Surface 4 (BYOC integration shape), Surface 5 (BYOC search distribution) all couple to PDR-005 drafting. MUX/UI cohort + PDR-005 are tightly coupled; v0.3 absorbs my Round 1 PDR-005 review flags (3 of 4 intersect with this cohort).
- **#1017 Pattern-071 (audit-as-attack-surface)**: filed today; Surface 7 audit read surface is the canonical positive example of the principle's read-side complement.

## For CEO ratification

Round 2 is ready for PM/CEO ratification of the locked decisions:

1. **Surface 4 integration pick** (GitHub + Calendar + Notion; defer Slack)
2. **Surface 7 audit-envelope ADR + MUX doc as paired deliverables**
3. **Surface 2 per-conversation privacy for 1.0**
4. **Surface 1 sidebar reconciliation approach** (assign roles, don't merge)
5. **Surface 6 framed as templated voice surface** (Class A + Class C; not four-element-principle)
6. **Total build estimate**: ~13-18 working days plus voice work in parallel; PDR-005 v0.3+ sequencing dependency

PM/CEO ratification triggers Phase 2: per-surface MUX doc drafting (CXO + Comms voice work) + Lead Dev Phase 2 build at PDR-005-sufficient-resolution.

## Resource & sequencing flags for CEO consideration

- **CXO + Comms voice work** runs in parallel with Lead Dev build; build estimates assume voice prose lands by appropriate Phase 2 milestones
- **PDR-005 v0.3+** is sequencing dependency for Surface 2 + Surface 4 (PPM cadence)
- **#1075 route-prefix migration** flag for PA/Docs sequencing visibility (Surface 4 OAuth callbacks)

## What this synthesis is NOT

- **Not committing per-surface MUX doc content** — post-ratification work; CXO + Comms lane
- **Not committing to specific build sequence within the 13-18 day window** — Lead Dev determines after CXO ratification + PDR-005 resolution
- **Not committing ADR-NN slot for audit-envelope read-surface** — CIO catalog-management lane (slot allocation at filing time)
- **Not committing voice prose** — per-surface MUX doc work post-ratification
- **Not synthesizing PDR-005 implications beyond the Surface 2/4 intersection** — PDR-005 review is parallel CXO work (filed v0.2 review today; experience-section deliverable on May 25 – Jun 1 target)

— CXO, 2026-05-15 (11:35 PT — Round 2 cohort scoping pass complete; awaiting CEO ratification)
