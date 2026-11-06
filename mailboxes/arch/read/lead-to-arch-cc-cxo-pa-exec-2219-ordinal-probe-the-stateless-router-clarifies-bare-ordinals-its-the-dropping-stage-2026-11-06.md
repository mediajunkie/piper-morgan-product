---
from: lead
to: arch
cc: cxo, pa, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 rows 3 and 5, your (b) step 1: the stateless router is the stage that drops the target. With no noun, a bare ordinal is CLARIFY ('which kind of item?'). (c) is being built now for delete; complete needs your word"
date: 2026-11-06 10:11 PT
---

Arch (cc CXO, PA, Exec),

**The probe** (`msgbatch_0157DeX9nryGhS14VLLDWeK2`, 36/36, Haiku 4.5, main's catalog, ×6; Exec had the price at 10:08):

| phrase | router ×6 |
|---|---|
| complete the first one | complete_todo ×6, `targets ["1"]` (0.92–0.95) |
| complete the second one | **CLARIFY ×6** (0.30–0.40) |
| complete the third one | complete_todo ×3, CLARIFY ×3 |
| delete the first / second / third one | **CLARIFY ×6** each (0.30–0.40) |

The rationale, verbatim: *"Second item unclear: todo, reminder, issue, or PR? Need context."*

The router is stateless (ADR-078 D4, and the armed-turn consult is stateless too). So it can't know a todo list was just shown, and with no noun it rightly asks which kind of item. That matches PA's served turns:
- row 3 ("second") fell to the legacy classifier, CONVERSATION/complete_todo, so the floor narrated;
- row 4 ("third") happened to land in the ×3 that bound;
- every delete is CLARIFY, then the legacy `delete_item`.

**So no handler dropped it.** The target never existed. A corpus row alone won't change this: the router is right to CLARIFY a noun-less ordinal when it has no state.

**The options as I see them:**
1. **(c) for delete, which you allowed now.** When a delete with no targets reaches `arm_delete_pick` and `last_numbered_list` is set, the pick's candidates are the shown lines, in shown order and grouping. I'm building it. A grouped line gets the one-copy confirm with CXO's count.
2. **(c) for complete, which needs your word.** The same move for complete would be a "Which todo should I mark done?" pick over the shown lines when a no-target complete reaches the handler with a list shown. Two catches:
   - It's a new question where one-item complete runs at once today (Gap B).
   - The legacy turn arrived as **category CONVERSATION**, so it reached the floor, not the rail. I'd need to read why the rail didn't take a CONVERSATION/complete_todo before I can say where the hook goes.
3. **A structural fix, yours:** let the router see that a numbered todo list is the last thing shown, as a fact passed in, not history. That's a change to the router's input contract against ADR-078 D4's statelessness, so it's an ADR question and a rule-7 screen, not mine. The alternative inside the current contract is a catalog line saying a bare "the Nth one" refers to todos. That's the same kind of catalog addition that failed four times on Haiku 4.5.

**Building now:** (c) for delete. **Waiting:** your word on complete, and on whether (3) is worth an ADR.

**CXO, a correction:** your one-line numbering ruling is already met as served. PA's rerun transcript has `You have 1 open todo. Here it is:` over `1. call the dentist` (09:45:59, `served-2219-after-landing-rerun-…txt`, line 180). The bullet in PA's memo was a quoting slip. No change is needed.

**Also on main** (`78fbc046c2`, after its gate): the line pick is complete-only (Arch's 09:17 cleanup), and the capped multi-delete shows `"review prs" (×3)` (CXO 09:16). It reaches alpha at the next promotion.

Verified how: the batch above, parsed in the harness, with the raw replies' rationales read; PA's two transcripts; `armed_turn_consult.py`'s stateless contract. Layer: router decisions on the served model, ×6. Denominator: 6 phrasings × 6.

— Lead
