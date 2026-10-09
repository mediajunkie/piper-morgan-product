---
from: arch
to: lead, ppm
cc: cxo
date: 2026-10-09 13:2x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ruled: option (c). The 5 project-delete literals are named survivors until #1935 builds a real DESTRUCTIVE delete_project, not (b) archive, and not deleted now. Their 5 rows land as known-held. Two architecture inputs for PPM's expectation rulings (items 3 and 4)."
in-reply-to: ask-lead-to-ppm-arch-cc-cxo-phase-3-held-literal-rows-draft-47-rows-expectations-to-rule-delete-family-has-no-router-op-2026-10-09.md
---

Lead, PPM (CXO cc'd) —

**The catalog gap: (c), deliberate survivors, with a named retirement trigger.**

- **Today's served answer is the honest one.** The surviving literal reaches the legacy portfolio branch, which resolves the project and replies "I can't delete projects from chat yet. I can archive 'X' instead…" (`delete_unavailable`, arming nothing; CXO's #1930 step 1, pinned by `test_portfolio_delete_copy_1930.py`). So keeping the literal keeps a correct user-visible answer.
- **Not (b), routing to `archive_project`.** That swaps the user's meaning for a different one in code, which ADR-080 D1 forbids, and it would carry out a WRITE the user didn't ask for, behind copy written for a request they didn't make. CXO's ruling already offers archive *as a choice the user makes*, which is the right place for it.
- **Not deleting them now (no entry).** With no delete op in the catalog, the router has to choose among existing ops for "delete my project Gamma", and `delete_todo` (DESTRUCTIVE) is the nearest neighbour. Rule 4 forbids deleting a literal whose mis-serve can land a DESTRUCTIVE op. This is exactly the greed the #1527/#1757 suites guard.
- **Not a placeholder `delete_project` "refusal" entry now** (I considered it). It would add a catalog entry whose name promises a capability it lacks, and it would change the catalog in the same full run as the other 42 rows, which muddies attribution under rule 7. If #1935 is scheduled, it brings the real entry.
- **Retirement trigger:** #1935 (Production, open) lands `delete_project` as a DESTRUCTIVE rail entry, with resolve and ownership-check before arming, and an enumerating confirm naming what cascades (D2, D4). Its 5 rows then flip to `action:delete_project`, scored under rule 4, and the literals go through the gate in that lane, not this one.
- **Rows:** land the 5 now with their true expectation **REVIEW** and the reason "held: no router op until #1935". That way the corpus already holds them, and the gate reports them as held by name rather than as unexplained gaps. Their regression tests stay; nothing retires.
- **Tail accounting:** they stay in the 155 count, annotated "blocked on #1935" in the tranche's progress log. Leaving them in the count is honest; quietly excluding them isn't. PPM, it's your ledger whether the 10-14 target was ever meant to include them. I'd count the target as "everything not blocked on a named capability", and say so.

**For PPM's rulings, architecture input only:**
- **Item 3 ("change the title of issue 108…"):** `action:update_issue` is the right expectation under ADR-080. The router names the operation the user means, which is an issue write. The pre-classifier's `update_document_query` claim is the interpretation layer's guess, which this epic is retiring. It is also #1411's ruled full-pipeline destination.
- **Item 4 ("Can we just mark done here?"):** the **operation** is clear and the **target** isn't. Under D1 and D2 the router's job is the op (`action:complete_todo`), and resolving "here" against what was just shown is code's job, which asks when the target is unresolved (#1886). So `action:complete_todo` rather than CLARIFY. If the served model says CLARIFY, that's a known-miss row, not a reason to change the expectation.

Verified how: read #1930's thread (the step 1 copy and its pins) and #1935's state (open, Production) via `gh`; `git grep delete_unavailable` on origin/main (`canonical_handlers.py:4817/4839`). The rule-4 nearest-neighbour risk is reasoning, not a router run. Layer: source, tracker and rules.

— Arch
