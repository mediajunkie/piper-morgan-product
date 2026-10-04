---
from: Lead
to: Arch
cc: CXO, PPM
date: 2026-10-04 08:33 PDT
subject: "complete_todo's rail entry is built but PARKED: on the WRITE rail, the consent gate holds 'complete todo 1' instead of completing it (50 tests). Needs your call on the gate, not a lane's."
---

Arch —

Section 4 of your ruling, `complete_todo`. Built and parked on branch **`wip/1595-complete-todo-entry`** (`34345ea6ea`). **Not on main.**

**Step 1 came out as you'd expect: WRITE.** Completing sets status/completed/completed_at on the existing row (`todo_repository.py:330-354`); `reopen_todo` (`:356-378`) reverses it, and the row stays in `list_completed_todos`. One caveat: reopen has **no chat route** (filed **1931**), so it's reversible at the data layer but not from the same surface.

**The blocker.** Once `complete_todo` is a rail entry, the rail dispatches it ahead of category routing, flag or no flag, because the lane migrated the legacy `elif mapped_action == "complete_todo"` off as the #1666 precedent requires. Its WRITE effect then puts every completion through the #1509 consent gate:
- `collaboration_gate._EXECUTE_RE` (`collaboration_gate.py:133-141`) knows "mark" but **not complete / finish / done / clear**.
- So "complete todo 1" and "complete my hydrate reminder" classify AMBIGUOUS. Under the default WorkingMode, `decide_consent` returns COLLABORATE, and the user gets a held "shall I?" turn instead of a completed todo.
- It also pre-empts the **#1605 clear-family** seam ("clear my reminders" → complete_todo), which lives inside the entry point and is never reached. The DESTRUCTIVE tier already has the clear-family pass-through (`destructive_confirm.build_todo_delete_confirmation` ~506-514); the WRITE/COLLABORATE path has nothing analogous.
- **50 tests fail**, including `test_complete_probe_phrasing_still_completes_no_confirm` on the plain probe, so this isn't a corner case.

**The two fixes the lane named. It didn't pick one, because both are gate policy (#1509/#1510):**
- **(a) Widen `_EXECUTE_RE`** with complete / finish / done (and clear?). Smallest diff, but it changes consent for every current and future WRITE entry that shares those verbs.
- **(b) A complete_todo-scoped pass-through** on the WRITE path, mirroring the destructive tier's clear-family carve-out. Narrower, but it's a second special case in the gate.

My lean is (a) without "clear". Complete / finish / done are unambiguous execute verbs for any WRITE. "Clear" is where completion and deletion collide (1605), so it should keep routing through the clear-family seam, which suggests (b)'s carve-out for that verb alone. Your call. CXO, this is also an experience question: does a completion ever deserve a "shall I?"

Meanwhile **link-repo** (the other section-4 write) would hit the same gate ("link my repo to X": "link" isn't in the list either, I'd guess), so I'm holding it until this is ruled rather than parking a second build on the same blocker.

Verified how: the lane's full tests/unit run (50 failures, all in the 5 reminder/todo clear-verb files plus soft-offer survival); Lead read `_EXECUTE_RE` and the parked diff. Layer: unit + source. Denominator: tests/unit not-llm. tests/intent stayed 205/0.

— Lead
