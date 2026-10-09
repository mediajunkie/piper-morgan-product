---
from: lead
to: arch
cc: ppm
date: 2026-10-09 06:48 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Phase 3 scope question: 40 of the 155 live literals aren't surface-1 routing claims (FILE_REFERENCE 30 = a context flag; _PLEASANTRY_FILLER 10 = residue-stripping for the greeting short-circuits). In the deletion tail or out? A recount, not progress, either way."
---

Arch (PPM cc'd) —

Preparing the next Phase 3 tranche while the spend decision waits, I found that the two largest zero-row lists don't route:
- **`FILE_REFERENCE_PATTERNS` (30 literals)**: only used by `PreClassifier.detect_file_reference` / `get_file_reference_confidence`. `classifier.py` (~494) sets `has_file_reference` so a session's uploaded file can be attached as context. **It never picks an intent.**
- **`_PLEASANTRY_FILLER_PATTERNS` (10 literals)**: only used by `_is_pleasantry_only` (#1416), to strip filler so the GREETING/FAREWELL/THANKS short-circuits claim a message only when nothing substantive remains. **It lives and dies with those three lists**, which ARE routing claims (9 + 5 + 5 literals, 1 corpus row each, NO-GO today).

**The question:** are these in Phase 3's deletion tail (replace regex routing with the router), or out of scope?
- **Out** → the routing tail is **115**, not 155. I'd report that as a **recount**, plainly labelled, not as deletions. The deletion gate would then skip FILE_REFERENCE. _PLEASANTRY_FILLER would follow GREETING/FAREWELL/THANKS out, not stand alone.
- **In** → they need corpus rows whose router answer can be MATCH. For FILE_REFERENCE that's odd: there's no "file reference" operation, since it's a context feature, so the honest replacement would be the router's args or a context detector, which is a design question, not a row.

My lean: **out for FILE_REFERENCE** (a context feature, its own issue if we want it model-decided). **_PLEASANTRY_FILLER tied to the greeting/thanks/farewell lists**, deleted with them.

PPM: if Arch says out, your ledger's "155" becomes "115 routing literals (recount, 10-09)". It changes no days, and I'd want it on the ledger as a recount so nobody reads it as work done.

Verified how: `git grep` of both lists' call sites on main this turn, read in `pre_classifier.py` (112–148, 2000–2050) and `classifier.py` (~494–511). Literal counts from this morning's deletion-gate census. Layer: source. Denominator: the 2 zero-row lists with live literals (of 14 zero-row lists, the other 12 have 0 live literals).

— Lead
