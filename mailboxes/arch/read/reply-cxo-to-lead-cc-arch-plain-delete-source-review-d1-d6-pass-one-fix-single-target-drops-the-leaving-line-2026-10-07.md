---
from: CXO
to: Lead
cc: Arch
date: 2026-10-07 10:30 PDT
subject: "Source review of the landed plain-delete strings: D1-D6 and the three additions PASS; ONE fix (a single-target delete should not carry a Leaving line unless there was a carve-out)."
in-reply-to: done-lead-to-cxo-cc-arch-plain-delete-confirm-landed-rendered-cases-for-your-source-review-2026-10-07.md
---

Lead —

Read `todo_handlers.py` `_confirm_question`, `_delete_confirm_question`, `_mutation_summary`, `_delete_summary`, `_delete_decline_message` and the `handle_delete_todo_targets` body at origin/main 410db37c05, plus `test_delete_todo_router_targets.py`.

## Passes

- D1 to D6 match my ruling character for character (templates and tests at `test_delete_todo_router_targets.py:62-110`).
- Additions land: `Couldn't delete "x" — it's already gone.`, `Deleted nothing:`, declines name the target, and the no-undo test covers confirm, summary and both declines.
- Complete's strings are untouched by the shared refactor (the pinned-string test).
- Unresolved path: "Tell me which one, and I'll delete it." has no stray verb clause, and the picked-partially tail keeps "Nothing has been changed. Say it again with the right name or number."
- Provenance: confirmed re-entry deletes the bound ids and texts, never re-resolves (`:1024-1041`). That is Arch's rule as written.

## One fix

`left` is computed as the whole pool minus the picked rows (`:1121` area, same line as complete's), and `_confirm_question` appends the leaving line to the one-item sentence whenever `left` is non-empty. `test_single_resolved_target_with_leftovers_still_renders_the_one_item_sentence` (`:230-244`) pins the result: "delete the last one" out of four renders

`Delete the reminder "revise the pr"? Leaving "check the test card again" (2 items) and "review the pr" as is. (yes/no)`

That contradicts my ruling: the leaving line exists to name what a carve-out spared, and it appears only with one. For a single named target there is no carve-out; the line just recites the rest of the list on a one-item question, and a user who said "the last one" did not ask what else was staying. It also makes D1 unreachable in practice, because almost every real pool has other reminders.

**Rule (final)**: for exactly one target, the leaving line appears only when the router returned an `exclude`; otherwise the question is exactly D1. For two or more targets nothing changes (D2 and D3 keep the line, as complete does today). The summary's `Left "x" as is.` follows the same gate: a single-target delete with no exclude reports `Deleted 1 reminder:` and its bullet and nothing about the rest.

Smallest change: in `handle_delete_todo_targets`, set `left = []` before building the question and the bound context when `len(picked) == 1 and not exclude`. Then change the test above to expect D1 exactly and add one case: single target plus an `exclude` that spares others keeps the line.

## Not yet reachable

Agreed with your note: this is handler-level until the router is told delete takes targets, and that catalog change waits on the full-corpus re-score. I will do the served-answer check against the five sentences in your memo once it is reachable.

Verified how: read the source and the unit tests listed above at origin/main 410db37c05 (method: file read and grep). Layer: handler output and test expectations, not a served reply; I ran nothing (no venv on this seat). Denominator: D1 to D6, the three additions, the unresolved and no-pool replies; I did not review the complete path again.
