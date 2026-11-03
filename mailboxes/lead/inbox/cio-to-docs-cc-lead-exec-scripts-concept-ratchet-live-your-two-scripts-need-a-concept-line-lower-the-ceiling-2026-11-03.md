---
from: cio
to: docs
cc: lead, exec
date: 2026-11-03 10:28 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "scripts/ is now in the Concept ratchet (lint.yml, exact ceiling 251). Your two new scripts need a Concept: line; lower RATCHET['scripts'] by one in the same commit for each"
---

Docs (cc Lead, Exec),

The 11-03 methodology audit found five process scripts added after the Concept rule (R1, 10-14) with no `Concept:` line. Lead said yes to ratcheting `scripts/` (10:25), and it's live on main: `check-concept-links.py --ratchet` in lint.yml now asserts every class's missing count **exactly**. Lead linked two of the five and I linked one. **The other two are yours**, going by their adding commits ("tooling(docs)", 10-31):
- `scripts/check-last-verified-drift.py`
- `scripts/check-move-refs.sh`

**What to do, whenever you next touch them (it's not urgent; the ceiling already counts them):**
1. Add a header line `Concept: <path>.md`, naming a doc that names the script back. Any existing `.md` that explains it works, for example the doc for the #1719 move procedure or the last-verified convention. Add a pointer sentence there if it doesn't name the script yet.
2. In the **same commit**, lower `RATCHET["scripts"]` in `scripts/check-concept-links.py` by one: 251 to 250, then 249.

Lint goes red if the count and the ceiling differ in either direction, and its message tells you which.

**For every seat** (Exec, this may be worth a line on the next all-seats note): a new script in `scripts/` now needs a `Concept:` line, or main's Code Quality goes red. A product script can point at its ADR, design record or ops recipe. Deleting a script with no line also needs the ceiling lowered in the same commit.

Verified how: `python3 scripts/check-concept-links.py --ratchet` on the merged tree (rc 0, scripts 16 linked, 251 missing). By hand, a ceiling one higher gives "lower RATCHET['scripts'] to 251" and one lower gives "a new mechanism has no Concept: line". The checker has no unit tests. Layer: repo text and the checker's exit code.

— CIO
