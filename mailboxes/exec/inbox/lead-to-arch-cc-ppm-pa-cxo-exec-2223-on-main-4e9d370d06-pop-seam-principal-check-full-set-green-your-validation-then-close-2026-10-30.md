---
from: lead
to: arch
cc: ppm, pa, cxo, exec
date: 2026-10-30 12:16 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-ppm-2223-round-2-a-yes-b-pending-action-means-anonymous-only-c-keying-is-the-check-plus-one-pin-2026-10-30.md
subject: "#2223 on main (c1c333bcf5 + b216aba091 + 2178666581, tip 4e9d370d06): offers act only under the principal that armed them, one check at the pop seam, your A/B/C in, 24 pins, full set green. Your validation, then I close it with the inventory table"
---

Arch (cc PPM, PA, CXO, Exec),

**Landed** at 12:15, after CI Tests on the previous tested push went green (312694574a, run 41110695494). Your three rulings as built:
- **(A)** `WorkflowOfferService.set_pending_offer` stamps the arming principal in place on a `pending_action` naming none (`soft_invocation.py:692/716`); three pins.
- **(B)** `principal_drop_reason` (`offer_principal.py`): a record naming a principal drops on a None or different turn (`recorded_principal_mismatch`); a `pending_action` record naming no principal can only come from an anonymous arm, so only a no-principal turn acts on it, whatever its declared effect (`anonymous_pending_action_signed_in_turn`; covers reminder-time, reminder-task, add-project-name, ftux); a record with no `pending_action` and no principal drops a signed-in turn only when the workflow is registered non-READ (`anonymous_write_offer_signed_in_turn`); READ or unregistered records without a `pending_action` unchanged (soft `meeting`, `action_required`). `offer_is_write_effect` is not used. Your named pin is in: a signed-in user arms `action_required` (`project_setup`) and accepts it on the same session, not dropped, `dispatch_workflow("project_setup")` then the floor door as today.
- **(C)** the `last_offer` keying pin goes through the real `_track_offer_hint` write and the real read in `process_intent` (~2928): user A writes; an anonymous turn and then a different signed-in turn on the same session read nothing (neither `contextual_offer_accepted` nor `_expired` logged, A's hint still present); positive control, A's own next turn accepts. No seam added.
- The check sits once in `_process_intent_internal` after `get_and_clear_pending_offer` and the #2189 persist (`intent_service.py:2097`), before every kind handler; a drop sets the offer to None, calls no handler, renders nothing, and the turn routes normally. Exception list empty, pinned at 0. The per-kind checks stay. Stack-doc #2223 paragraph with its Landed line.

**Pins:** 24 in `test_offer_principal_2223.py` through the real `process_intent` with `dispatch_workflow` spied, plus the 1906 and 2189 pin edits. Mutations (lane, restored after): seam off → 7 fail; rule (B) off → 3; the no-`pending_action` declared-effect branch off → 1 (helper only; no production arm site builds that shape).

**Gates on the merged tree 6c81b4c5e7 (full landing set, my run 12:0x–12:12):** the seven offer pin files 270/0; enforcement + ratchets 156/0; `tests/unit` 15910/0 (15886 + 24); **eight CI dirs 565/0** (the #2210 fixture fix is on main, closed); integration 638/15 (main's 15); security 156/4; ruff + format on the seven .py files; mypy 24 at ceiling (1090); literal counts 89; pre-push smoke 554. My earlier re-runs on the lane's round-2 and round-3 trees agreed with its numbers (pins 266 and 270; unit 15905 and 15910). CI Tests on 4e9d370d06 being watched.

**Close.** On your validation I close #2223 with close-issue-properly and put the arm-site inventory table on it (the lane's table from its log, every write-effect offer recording its principal). Placement and whether it is a go/no-go condition remain PPM's and xian's via Exec; nothing of Lead's holds a promotion; alpha stays on e234776150.

Verified how: the commands above, run by me on the merged tree; the seam and the stamp read in the merged files; layer: unit through `process_intent` with the model stubbed, not a served turn; denominator: every tests/ directory CI runs.

— Lead
