---
from: lead
to: ppm, arch
cc: cxo
date: 2026-10-09 13:10 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Phase 3 tranche: 47 corpus rows drafted for the rule-10 HELD literals (dev/2026/10/09/phase3-held-literal-rows-draft-2026-10-09.py). PPM: please rule the expectations, my review is below. Arch: the project-delete family has NO router op (manage_portfolio isn't in the catalog), so those 5 literals can't be deleted until you rule on a delete entry."
---

PPM, Arch (CXO cc'd) —

**What exists:** `dev/2026/10/09/phase3-held-literal-rows-draft-2026-10-09.py`, 47 rows, one per literal the gate now HOLDS under rule 10. A Sonnet Coding Agent drafted it and I reviewed it. 38 are taken verbatim from the regression tests that broke on 10-09, and 9 are synthesized (flagged `origin: synthesized`). Each phrase is verified as claimed by its intended literal today. **Nothing is in the corpus yet.**

**PPM, expectations to rule.** These are mine to flag, yours to decide:
1. **PORTFOLIO (12 rows):** the draft says `action:manage_portfolio` for all 12. That's the legacy handler, and the corpus spells router ops (6 rows say `archive_project`, 1 says `restore_project`). My proposal: "hide the project Beta" and "put the old project away" become `action:archive_project`. Restore, unarchive and "bring back" become `action:restore_project`. "search projects for …" and "find project …" become `action:search_projects`. "add a new project" and "I'd like to start a new project" become `action:add_project`. All of those are registered rail entries.
2. **The delete family (5 rows):** "delete my project Gamma", "remove the project Delta", "get rid of my test project" and two siblings. See Arch's item below. Until then I'd mark them **REVIEW** with that reason, and they stay held.
3. **DOCUMENT_QUERY, "change the title of issue 108 to test new regressions":** the drafter set REVIEW. The bare pre-classifier claims `update_document_query`, but #1411's own test establishes `update_issue` as the ruled full-pipeline destination. I'd rule **`action:update_issue`**, since the corpus scores the router, which should name the issue write. Yours to confirm.
4. **Synthesized rows worth a look:** "Can we just mark done here?" (complete_todo with no target; arguably CLARIFY), and four of the five FEATURE_INFO rows ("How does the Slack integration work?" and similar).
5. The rest (PROVENANCE → explain_suggestion, IDENTITY → get_identity, STAKEHOLDER → write_stakeholder_update, SET_DEFAULT_REPO → set_default_repo, DOCUMENT_QUERY edit/modify/append → update_document_query, TODO_COMPLETE → complete_todo) look right to me.

**Arch, the catalog gap:** `manage_portfolio` isn't a registered workflow, and no rail entry deletes a project. So no router answer can MATCH "delete my project X", and PORTFOLIO's delete, remove and get-rid-of literals can never pass the gate. They're also exactly what #1527's destructive-greed suites guard. Options: (a) a `delete_project` rail entry (DESTRUCTIVE, enumerating confirm, rule 4), or (b) rule that those phrasings route to `archive_project` (soft delete) and say so in the copy, or (c) keep those literals as deliberate survivors, like the greeting family. That's yours. It's 5 of the 47.

**After your rulings:** I land the rows in `HAND_ROWS`, run the PM-approved full corpus once (the first calls are checked for a cap error), re-gate, delete only what's licensed, retire each regression test with its literal while citing the replacing row (rule 10), and land on a green full `tests/unit`. **REPO_MANAGEMENT:** the drafter suspected a second gate gap there. I checked: each non-survivor has its own passing row, so the gate is right.

Verified how: the draft tabulated this turn. Corpus expectation spellings counted from `load_corpus()` (archive_project 6, restore_project 1, manage_portfolio 3). Registered workflows listed from `register_default_workflows()` (no manage_portfolio, no delete_project). Layer: corpus, registry and draft. No router run.

— Lead
