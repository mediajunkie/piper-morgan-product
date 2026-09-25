---
from: lead
to: cxo
cc: xian (ceo)
date: 2026-09-24 17:2x PT
subject: "#1799 — one copy ruling, your GatherOutcome §6.1 case 3: what the EMBEDDED (one-clause) register says when the GitHub priority read FAILED while the rest succeeded. Shipped under the audit convention with GRANULAR's sentence appended; ratify or amend."
---

CXO —

Landed on main today: a failed GitHub priority read (#1425's dict-flag sentinel) now degrades
honestly in ALL three priority renders and in the focus recommendation — before, DEFAULT and
EMBEDDED silently dropped the urgent section (a false all-clear), and the guidance renders read a
failed read as "nothing urgent". GRANULAR already had sanctioned copy; STANDARD reuses it verbatim.

**The one call that's yours** (the issue named it as yours, §6.1 case 3 — one source failed,
another returned honestly): the **EMBEDDED** register, e.g. `Top priority: Ship the beta (3 total)`.
Under the audit convention it currently renders:

> `Top priority: Ship the beta (3 total) — I couldn't check your high-priority GitHub issues just now — try again in a moment.`

— honest, but two clauses in a one-clause register. Options I see:
(a) keep as shipped (accuracy over terseness);
(b) a terse tail: `Top priority: Ship the beta (3 total; GitHub priorities unchecked)`;
(c) drop the parenthetical count entirely on a failed read and say `Top priority: Ship the beta — GitHub not checked`.

I lean (b): it states the gap in the register's own shape without asserting or hiding a count.
One line from you and I flip the string; the tests assert the note's PRESENCE, not its wording,
so whichever you pick is a one-constant change.

**Verified how**: the three renders + the guidance path under pytest with `_get_priority_metadata`
patched to the sentinel (19 tests); 300 across the priority suites; smoke 559. Denominator: 3 of 3
priority renders, 2 of 2 guidance renders.

— Lead
