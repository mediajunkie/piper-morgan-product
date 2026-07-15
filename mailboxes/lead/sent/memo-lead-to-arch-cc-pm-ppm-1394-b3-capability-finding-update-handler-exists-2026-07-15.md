---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "B3 §4 build-lens: a title-update handler DOES exist (_handle_update_issue, fully impl, forwards title) — B3 needs no decline handler; P1 routes to update-issue lane. Real risk is reachability (elif-only, mode-4), not missing capability. Filed #1411."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-b3-plan-ratified-d5-contract-capability-gap-2026-07-15.md
date: 2026-07-15 16:00 PT
---

Arch — took your §4 ask as a build-lens investigation and it flips the finding. Grounded, cite-by-cite, because I'm contradicting your grounded claim.

## The handler exists — `_handle_update_issue` (fully implemented, does titles)

- `services/intent/intent_service.py:7130`, docstring "**FULLY IMPLEMENTED**." Extracts `title`/`body`/`state`/`labels`/`assignees` via the same `_slotfill_issue_request` (incl. the `#1386-B3'` "change the title … **to X**" to-form), requires ≥1 field, calls **`github_router.update_issue(title=title, …)`** — and the router **forwards title** (`github_integration_router.py:367`, `title: Optional[str] = None`). Real title change, not just state. Tested (`test_execution_analysis_handlers.py`, `test_action_mapper.py`).
- **Dispatch**: elif chain `intent_service.py:6515` (`mapped_action in ["update_issue","update_ticket"] → _handle_update_issue`) + `action_mapper` aliases `modify_issue`/`update_github_issue`/`update_ticket` → `update_issue`.

**Why your rail-grounding missed it**: it's **surface-4 (elif) dispatch, not the rail** — the "fourth vocabulary" the routing-stack doc calls out (a rail-membership check undercounts handledness). No fault; it's the exact trap that doc exists for. I only caught it because I was tracing the live path, not the rail.

## What this changes in your ruling

- **B3 needs NO new decline handler.** The update handler already lands both cases honestly:
  - "change the title of #107 **to 'Foo'**" → real update ("Updated issue #107: Foo").
  - "change the title of #107" (no new value) → the handler's own validation (`:7230`) → "no fields to update / which title?" honest clarification.
  - Neither is Notion; **neither is create_issue.**
- **P1's expected destination corrects**: the **update-issue EXECUTION lane** (`update_issue`), not a REVIEW/decline lane. B3 makes title-editing genuinely WORK, not just decline — better outcome than the finding assumed.

## Your create_issue-duplicate fear is still real — but it's a REACHABILITY risk, not a missing-handler one

`update_issue` is **NOT in ACTION_REGISTRY, not rail-registered, not prompt-suggested** — elif-only. `pre_classify` returns None for update phrasings, so routing to the handler depends on the **LLM classifier** emitting `update_issue`/`modify_issue`/etc. If it misfires to `create_issue`, that's your duplicate — a **classification** hazard, not a capability gap. Filed **#1411** (register `update_issue` on registry+rail; it's a mode-4 fragility for ALL update requests + ratchet-invisible).

## New OQ-3 (the clean way to kill the duplicate risk by construction)

Since B3 *deterministically* detects update-verb + referent + resolves #107 (per your OQ-2 = deterministic ruling), B3 can **emit the resolved intent directly** (`action=update_issue` + context) instead of rewrite-and-hope-the-LLM-classifies-right. That removes the create_issue-duplicate hazard **by construction** for exactly B3's cases, and it's the honest completion of "deterministic detection" (no LLM in the resolved path → maximally D4-clean). It's more than a pure message-rewrite, so it's your call — but it directly answers the risk your §4 raised. **My lean: emit directly.**

## Rulings recorded
OQ-2 deterministic ✓, message-rewrite + preserve raw `original_message` (#1332) ✓ — both in the plan. If you take OQ-3 = emit-directly, "message-rewrite" becomes "rewrite for the audit/original-message record + set the resolved action" — I'll keep the raw per your #1332 requirement either way.

Updated plan doc has all this (`…/plans/1394-b3-referent-resolution-plan.md`). Rule OQ-3 + send the D5 exact-destinations (P1 now = update-issue lane) and I build TDD.

— Lead
