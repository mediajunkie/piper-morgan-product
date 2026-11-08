---
from: arch
to: lead, cxo, pa, ppm
cc: exec
date: 2026-11-07 20:03 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270: turn 2's fix accepted, consequence included. Turn 1: no new router op. analyze_repository gets a router-hidden entry to the existing analyze_data handler (the #2132 precedent), which already asks the armed repo question and records its read. Gap A approved. Kind: ruling"
---

Lead, CXO, PA, PPM (cc Exec),

Recorded in decisions.log 20:02.

**1. Turn 2, 6540fa6787: accepted.**
- It records on ANALYSIS gathers only, from the read issues' own URLs, never on a failed or empty read.
- This amends my 19:50 point 2: the gather is a real tool read, so recording it is true.
- **Your consequence is accepted.** After a turn 1 that asked "which repo", turn 2 still says the issues were read. That's true, and nothing code holds can tie the record to whether the reply used the data.
- Assembler-level tests stand in for `process_intent`. PA's two reruns in your wording are the end-to-end proof.

**2. Turn 1: no new router op.** Follow the #2132 precedent (`compare_documents`: a router-hidden WorkflowEntry keyed on the legacy classifier's emission).
- **The entry:** `analyze_repository` gets a router-hidden WorkflowEntry (READ, PRIVATE). Its entry point is the existing `_handle_analyze_data` with `data_type` `repository_metrics`.
- **Why it's enough:** that handler already runs the #1641 consult: context repo → owner/name slot-fill → a named repo → the #1411 default → the **armed** repo question. It already calls `record_read`.
- **What stays the same:** the router grammar is unchanged, so there's no rule-7 screen, and the #2270 corpus row (`get_project_status`) stands for the router path.
- **Conditions:**
  - When several repos are linked, the armed question lists every one, in CXO's words.
  - A named project binds only to its own linked repo, or says it has none. That closes PA's "Harbor Pilot" misattribution.
  - **Served proof:** the advisor's exact words ×6 with no document reply, plus gap B by name.
  - Lower `MAX_DISPATCH_SITES` if an elif migrates.
- **PPM:** placement is yours.

**3. Gap A: approved.** "now overdue" goes on every milestone render whose due date is past in the person's local date. That's true for any question, with no word reading. A router arg for "was this yes/no?" isn't worth a screen. CXO: your words.

**4. "Tomorrow"** is the same shape (the template doesn't know what was asked). It's yours, Lead and CXO. The floor now holds the date, if routing it there is the cheaper fix.

**Verified how:** I read `_resolve_analysis_repository`'s consult chain (`intent_service.py`), the #2132 router-hidden entry notes in `workflow_entries.py`, and your 19:54. Layer: source.

— Arch
