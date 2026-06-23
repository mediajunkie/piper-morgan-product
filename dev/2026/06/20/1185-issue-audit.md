# Audit: #1185 (BYO-KEY-MULTI-TENANT) against feature.md issue template

**Date**: 2026-06-20 · **Auditor**: Lead Dev · **Cascade gate 1 (Issue)**
**Scope**: WHOLE (PM 2026-06-20 — per-user identity + LLM-key wiring, one coherent effort)

| Template Requirement | Status | Notes / Action |
|---|---|---|
| Priority / Labels / Milestone / Epic / Related | ⚠️ | Sprint=RECONNECT (board) only. Add Priority (P1 — beta-gating), Related (#1300/#358/#1162). |
| Problem Statement — Current State | ✅ | "The gap": `user_api_keys` exists; LLM client uses instance key. Strong. |
| Problem Statement — Impact | ⚠️ | Impact lives inside the PM-decision line (shared-key limit = everyone's ceiling). Pull into an explicit Impact block. |
| Problem Statement — Strategic Context | ✅ | PM 2026-06-09 decision (live evidence: shared-key 429 blocked testers). |
| Goal — Primary Objective | ❌ | Add one-sentence success statement. |
| Goal — Example UX | ❌ | Add before/after. |
| Goal — Not In Scope | ❌ | Add (account/registration #441; OAuth; admin key-rotation UI; non-Anthropic per-user keys). |
| What Already Exists (✅/❌) | ✅ | The gap section. Now verified: `user_api_keys` covers `anthropic` → no schema change. |
| Requirements / Phases | ⚠️ | "Work" lists 4 items; phasing + tasks/deliverables → gameplan (gate 2). OK for the issue once AC added. |
| Acceptance Criteria | ❌ | **Key gap.** Add Functionality / Testing / Quality. |
| Completion Matrix | ⏸️ | Deferred to gameplan (gate 2) **by design** — the issue states WHAT, gameplan states HOW. Not marked N/A. |
| Testing Strategy | ⚠️ | Add the shape: unit (resolution), integration (per-request by user_id), wiring (clients.py→user_api_keys, no mock). |
| Success Metrics | ⚠️ | Make explicit (no tester blocked by a shared-key 429; per-user attribution). |
| STOP Conditions | ⏸️ | Template defaults apply; gameplan carries specifics. Not marked N/A. |
| Effort Estimate | ❌ | Add (Large — 4 parts; Part 2 per-user auth = largest unknown). |
| Dependencies | ⚠️ | Add #1300 (the `/connect` capture step), #358 (encrypt-at-rest). |
| Related Documentation | ✅ | PA scoping docs present. |
| Open Qs | ⚠️ | Q1 (does `user_api_keys` cover Anthropic?) — **RESOLVED: yes** (verified). Q2 (auth mechanism: token vs account/login) — open design decision → gameplan/PM. |

## Action taken (before gate 2)
Updated #1185 body to add: Priority/Related; explicit Impact; Goal (objective + UX + Not-In-Scope); Acceptance Criteria; Testing Strategy shape; Success Metrics; Effort; Dependencies (#1300, #358); resolved Open-Q-1; flagged Open-Q-2 as the gameplan's key design decision.
**Deferred to gate-2 gameplan by design (not N/A):** Completion Matrix, detailed phase tasks/deliverables, STOP-condition specifics.

**Verdict**: gaps fixed → proceed to gate 2 (gameplan).
