# Audit-cascade — ISSUE gate: Radar entity-source issues (2026-06-14)

**Phase**: Issue (the front-bookend gate of the excellence flywheel)
**Template (checklist)**: `.github/ISSUE_TEMPLATE/feature.md`
**Artifacts audited**: 4 drafted issues for the full-four-type Radar (PM directive 2026-06-14: "no partial ship… ship it all")
- `radar-entity-sources-umbrella-issue.md` → created **#1237**
- `radar-document-source-issue.md` → created **#1238**
- `radar-workitem-source-issue.md` → created **#1239**
- `radar-people-source-issue.md` → created **#1240**
- (Conversation = done under **#1236**, the proven pattern)

**Method**: drafted the 4 issues → **fresh-eyes audit** (Explore subagent) of each against every `feature.md` requirement → fixed ALL ⚠️/❌ → re-verified → created on the board. (Per the skill's asymmetry insight: LLMs audit templates better than they follow them while creating; a fresh agent has the least creation-attachment.)

---

## Gaps found (fresh-eyes audit) and fixed

| Gap | Files affected | Fix applied |
|---|---|---|
| **Example User Experience** (Goal) — missing | all 4 | Added a before/after block to each |
| **Success Metrics** (Quantitative + Qualitative) — missing | all 4 | Added honest, modest metrics (coverage, 0 seed-as-observed, latency budget, "answerable at a glance") |
| **STOP Conditions** — only a custom one, missing the standard set | all 4 | Added the standard escalation checklist + kept the domain-specific STOP |
| **Related Documentation** (dedicated section) — missing | Document/WorkItem/People | Added (Architecture / Methodology / Strategic) |
| **Notes for Implementation** — missing | Document/WorkItem/People | Added |
| **Testing Strategy** (named scenarios) — implicit only | umbrella | Added explicit Unit/Integration/Manual |
| Evidence Section / Completion Checklist | all 4 | Present as template-sanctioned "filled during implementation" scaffolds |

**Result**: all 4 issues now conform to `feature.md`. No `N/A` was self-granted (skill rule); every required section is substantive or a template-sanctioned during-implementation scaffold.

---

## ⚠️ The dimension the INITIAL audit missed (PM-requested capture)

PM, on seeing the four-type Radar reduced in practice to conversations-only: *"how do we overlook this i wonder."* Honest post-mortem of the **initial #1236 audit-cascade** (issue gate + gameplan self-audit, Fire 24):

**What the initial audit checked**: template **conformance** — every `feature.md` section present, the gameplan to v9.4, Phase-0.5/0.6 contract+data-flow verification. #1236 passed: it *had* a Dependencies section ("#706 entity catalog — PPM-owned, not yet built") and a "Not In Scope" deferral ("richer types later, non-blocking").

**What it MISSED — dependency completeness / referent verification**:
1. **The deferred dependency cited a dead referent.** #1236 pointed the other 3 types at **#706** — which is **CLOSED** and was a *design discovery* epic, not the backend implementation. The audit checked "is there a dependency line?" (yes) but not "is the referent real, open, and sufficient?" (no).
2. **The Phase-0.5/0.6 integration verification was scoped to what was being built (the conversation path), not to the full capability the issue claimed (four types).** So "verify the backend contract" passed for Conversation while 3 of 4 backends were absent/hard — invisible to a conformance audit.
3. **The deferred scope had no durable tracked home.** "Slot in later" had nowhere to live, so the surface workstream (Lead) and the entity-model workstream (PPM/CXO) drifted with nothing tying them. (This umbrella #1237 is the fix.)

**Root**: conformance ≠ soundness. The audit-cascade audits *artifact-vs-template structure*; it had no step that *traces each claimed capability/entity to a concrete, existing, verified backend referent*. This is the **investigate-before-extending** discipline (which we apply rigorously to code) **not applied to product scope**. It also tripped the "minimal deliverable needs a durably-tracked fleshing-out plan" lesson.

**Proposed fix to the audit-cascade skill (flag → CIO / skill owner)**:
> Add a **Referent-Verification / Dependency-Completeness check** to every Issue and Gameplan audit:
> - For each capability, entity type, or data source the artifact *claims*, trace it to a **concrete, existing, verified** backend (file:line / service+method) — or to an **OPEN, tracked** dependency issue. A deferred dependency that cites a **closed** or **absent** referent fails the gate.
> - For UI/surface work, the Phase-0.5/0.6 contract verification must cover the **full stated capability**, not just the slice being built first.
> - Any "slot in later / non-blocking" deferral must name its **durable tracked home** (an open issue), per the minimal-deliverable lesson.

This is a *substantive* audit-cascade improvement (the kind PM's "noting that initial audit missed this dimension" asks us to institutionalize), not just a one-off fix.

---

## Next cascade gates (per-source, when unblocked)
Issue gate ✅ (this doc). The **Gameplan → Prompts → Execute** gates run **per child** as each is picked up:
- **#1238 Document** — unblocked → gameplan+audit next (the tonight-startable candidate; Phase-0 contract read first).
- **#1239 WorkItem** — gated on #1233 identity.
- **#1240 People** — gated on the PPM People entity-model.

---
_Audit run: 2026-06-14 (Lead Dev). Issues created per PM "write issues" authorization. Board Sprint placement pending PM._
