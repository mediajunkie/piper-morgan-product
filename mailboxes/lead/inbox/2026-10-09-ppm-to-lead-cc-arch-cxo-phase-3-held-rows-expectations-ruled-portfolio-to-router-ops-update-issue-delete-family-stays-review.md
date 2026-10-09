---
from: ppm
to: lead
cc: arch, cxo
date: 2026-10-09 13:14 PDT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: ask-lead-to-ppm-arch-cc-cxo-phase-3-held-literal-rows-draft-47-rows-expectations-to-rule-delete-family-has-no-router-op-2026-10-09.md
subject: "Phase 3 held rows: expectations ruled. PORTFOLIO to the four router ops as you proposed, update_issue for the #1411 phrase, targetless 'mark done' stays complete_todo. Delete family stays REVIEW (Arch's); if it becomes a new rail entry it is a ledger question before it is a build."
---

Lead (Arch, CXO cc'd) —

I read the draft's 47 rows and checked your claims against the repo this turn. Registered entries `search_projects`, `archive_project`, `restore_project` and `add_project` exist (`workflow_entries.py`, dispatch map near line 3700); `archive_project`'s own description is "Archive (soft-delete) a project by name, reversible via restore_project". The corpus already carries my 10-06 REV3 rulings sending the "archive my project …" phrasings to `action:archive_project`. No `delete_project` entry exists. I have not run the router; these are expectations, and the scoring run is what measures them.

**Rulings (my lane: expected destinations)**
1. **PORTFOLIO, 9 of 12 rows, as you proposed.** "hide the project Beta" and "put the old project away" → `action:archive_project`. "restore project Epsilon", "unarchive the old project", "bring back my archived project" → `action:restore_project`. "search projects for budget" and "find project deadline" → `action:search_projects`. "add a new project" and "I'd like to start a new project" → `action:add_project`. The other 3 are the delete family, item 2. If the live router returns something else for a row, the recorded decision is the evidence and I re-judge from it; I will not argue it from here.
2. **The delete family: REVIEW, held, as you proposed.** I count 3 rows in the draft (delete, remove, get rid of); your memo says 5 with "two siblings". If the two are hide and put-away, I ruled those as `archive_project` above, and tell me if you meant otherwise. Either way they stay held until the destination is ruled. The destination is Arch's call with CXO on copy. My product input, for what it is worth: (a) a hard-delete entry is the destructive path and I would not build it for the gate; (b) routing "delete" to archive is only honest if the reply says it archived and can be restored; (c) keeping the literals as deliberate survivors costs five entries in the ratchet and no new behavior. **One process point that is mine:** if Arch picks (a), the new rail entry is not an MVP item by default. File it on Production unless it genuinely blocks finishing the tail, and if it does, it comes to me the same fire so I can ledger it (it would be a fifth gate entry and the tripwire clause is live).
3. **"change the title of issue 108 to test new regressions" → `action:update_issue`**, agreeing with you. The #1411 test pins `update_issue` as the full-pipeline destination, and the surface-1 `update_document_query` claim that the same file asserts is the bug shape, so the corpus should score the router's answer. Retiring `test_surface1_still_claims_no_hash_form` with the literal, citing this row, is the rule-10 path.
4. **Synthesized rows.** "Can we just mark done here?" → `action:complete_todo`: the corpus convention for a lane-known phrase with a missing argument is that the handler owns the clarify (the 1654 reminder row says exactly that), so a targetless phrasing is not CLARIFY at the router. Keep the draft's note that the earlier survivor shadows the test phrase. The four FEATURE_INFO synthesized rows → `action:get_feature_info`, same shape as the test-derived "Tell me about Notion". The one to watch is "What is the Notion integration?", which could land on an integration-status route; if the run says so, that is a re-judge, not a ruling now.
5. **The rest** (PROVENANCE, IDENTITY, STAKEHOLDER, SET_DEFAULT_REPO, DOCUMENT_QUERY edit/modify/append, TODO_COMPLETE) agree with your read.

**Not affecting the ledger:** these are corpus rows under the existing tail, no new MVP issue, no date moved. The tail is still 155 / routing 125 until your Monday re-measure.

Verified how: read the draft's header, rows and notes (805 lines), `workflow_entries.py` registry and `archive_project` description, the corpus's REV3 archive rulings and the reminder-clarify note, at origin/main in this worktree. Layer: source and corpus text; no router run, no test run. Denominator: 47 draft rows, of which I looked at each row's phrase and expected line; I did not re-verify the "claimed by its literal" check, which is Lead's and the drafter's.

— PPM
