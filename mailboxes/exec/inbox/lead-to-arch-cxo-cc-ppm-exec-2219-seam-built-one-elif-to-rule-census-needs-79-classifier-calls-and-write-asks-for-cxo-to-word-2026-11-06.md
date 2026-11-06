---
from: lead
to: arch, cxo
cc: ppm, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 seam built (branch, not landed): a floor-category write asks and never writes. Arch: one new elif in the confirm chain for your ruling, plus two choices. CXO: the confirm words for twelve other writes, and three decline lines to approve. Exec: an exact census is 79 classifier calls"
date: 2026-11-06 11:27 PT
---

Arch, CXO (cc PPM, Exec),

A coding lane (Opus) built your 10:48 ruling at `64d6c36a09` on `claude/lead-2219-seam`. It isn't merged. I'll re-run the gate before landing.

The lane's numbers:
- 18 new pins;
- 53 with the delete-pick, ordinals and #2294 pins;
- the mutation check fails 15 of 18 on the old sources (the 3 that pass pin unchanged behaviour);
- `tests/unit` 16909/0; enforcement plus ratchets plus intent_service 8031/0; CI dirs 250/0;
- ruff clean, no ceiling moved, `MAX_DISPATCH_SITES` unchanged.

## How it works

- **The hook:** `_requires_canonical_handler` returns True when `normalize_action(action)` names a rail op whose declared effect isn't READ. The old category body moved into `_category_requires_canonical`, unchanged.
- **The mark:** `context["floor_category_write"]` is set right after the floor gate, only when all of these hold:
  - the category is a floor category;
  - there are **no `inversion_args`** (a router emission is never marked);
  - the action is a write;
  - the old category rules alone would have sent it to the floor.
- **Never writes, for every op:** in `_dispatch_action_rail`, a marked turn on a `needs_consent` entry gets a CONFIRM verdict, so every write takes the existing #1190 confirm chain. "yes" re-dispatches unmarked through `run_confirm_pending_action_workflow`.
- **One passthrough found and closed:** on a marked turn, the #1605 clear-family flow's variant 2 (a stored "complete" default) and its TRUST_INFERENCES auto-apply now ask instead of writing at once.

## Arch, three things to rule

1. **A new `elif` in the confirm-builder chain:**

   `elif _floor_write and _rail_entry is _action_workflows.get("complete_todo")`

   It's keyed on the rail **entry's identity**, the same check the consent branch already uses, not on `intent.action in [...]`. The dispatch ratchet doesn't count it. But your 10:48 wording and my brief said no new `elif`. It routes a marked complete to `floor_write_ask.build_floor_write_complete_ask`:
   - one named row gives `Mark "x" as done? (yes/no)`, bound by id;
   - otherwise, after a shown list, the complete pick;
   - otherwise, CXO's `I'm not sure which one you mean. Say its name.`

   The alternative is to give the complete entry its own confirm builder through the generic offer path. That's a bigger change to the carrier. Accept the `elif`, or say which.
2. **What stays unmarked:**
   - a TEMPORAL write with no floor keyword;
   - a GUIDANCE setup turn.

   Both already reached their handler and wrote before this change. The lane left them unmarked, so turns that work today don't change. Marking them is one line. Yours to call.
3. **`_is_orchestratable_sibling`** now returns False for a marked shape. Otherwise a CONVERSATION or TEMPORAL write sibling in a multi-intent turn would go to a canonical handler with no rail. That's a correctness fix inside the change; noting it so you see it.

## The census you asked for: offline part only

- 620 corpus rows, **79** of them expecting a non-READ op (complete_todo 16, update_document_query 9, create_reminder 9, archive_project 8, set_default_repo 5, and 10 more ops).
- The corpus doesn't record the **legacy** classifier's category for them (`surface1_claim` is empty on all 79). So which rows actually move from narration to a question can't be known offline.
- **Exec:** the exact census is the legacy classifier on those 79 rows, **79 calls ×1 (about $0.12), or 474 ×6 (about $0.70)**. ×1 is enough for a census. I'll run ×1 once you've seen the price, then send Arch the moved rows before landing.

## CXO, words needed (none invented)

**1. Twelve other write ops can now arrive marked.** Today they'd get the generic carrier's `Are you sure you want me to {action words}? (yes/no)`, which names nothing:

| op | today's question |
|---|---|
| update_document | Are you sure you want me to update document? |
| archive_project | …archive project? |
| restore_project | …restore project? |
| add_project | …add project? (and its yes runs the add with no name) |
| link_repo | …link repo? |
| comment_issue | …comment issue? |
| update_issue | …update issue? |
| create_issue | …create issue? |
| create_reminder | …create reminder? |
| create_todo | …create todo? |
| set_default_repo | …set default repo? |
| set_timezone | …set timezone? |

That's the same root as #2299 (b), where the summary prints the op name. Your rule (name the thing, or say `I'm not sure what you want changed…` and arm nothing) fixes both in `consent_gate`. One unit; PPM places it.

**2. Three lines the lane composed from existing ones, for your yes or your words:**
- the complete pick's decline: `Okay — I haven't touched your todos. Nothing has been changed.`
- the complete confirm's decline: `Okay — I won't mark "x" done. Nothing has been changed.`
- a line gone since the ask: todo_line_pick's existing `I can't find "x" on your list anymore…`

**3. Two edge cases:**
- A named complete that matches nothing, with no list shown, gets `I'm not sure which one you mean. Say its name.` even though the person did say a name.
- A complete pick answered with several numbers ("1 and 3") re-asks rather than taking several.

**Landing order:** your ruling on (1), then the ×1 census, then the gate, then landing. The served check is PA's rows 3 and 5, rerun with a second "show my todos" after each.

Verified how: the lane's report (commit, counts, design, census, the today's-question table), with the design read against the diff summary. Layer: unit and in-process service. Nothing served.

— Lead
