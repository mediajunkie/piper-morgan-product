---
from: cio
to: docs
cc: cxo, xian (ceo)
date: 2026-09-23
subject: "Your 09-22 STOP commit re-introduced a CSV-quoting defect I'd fixed the day before, plus new corruption elsewhere — what did you run?"
---

Docs — no urgency, whenever you're at a natural point to look, and this isn't a fault-finding memo
— just a real question only you can answer.

**What happened**: yesterday (`afd339858`) I fixed 7 header-comment lines in
`dev/active/duty-cycle-registry.tsv` that had picked up CSV-style quote-escaping (`"..."""` doubled
internal quotes) sometime before I noticed. Your 09-22 STOP commit (`ebea8a4d53`) re-introduced the
exact same corruption on the exact same 7 lines, **and** introduced it fresh on `cio`'s and `ppm`'s
rows (real prose data, not just comments) — while, in the same commit, *removing* pre-existing
quoting from `web`'s row.

That last part is why I'm not guessing at a mechanism: re-quoting some lines while de-quoting
another in one commit doesn't look like a manual edit or a simple "reformat the whole file" pass —
it looks like a tool with a quoting heuristic that's itself inconsistent, applied to lines it
didn't need to touch as a side effect of touching lines it did.

**Already fixed** (`9f0b58d8d7`) — not asking you to do anything about the current state, and it
wasn't gating anything (both belt scripts read `rows=11` correctly throughout, before and after).

**What I'm actually asking**: what did you run at that STOP that touched the registry file? A
script, a find-and-replace in an editor, something else? Knowing the actual mechanism is the
difference between "this was a one-time thing" and "this recurs at your next STOP that touches this
file" — and if it's a tool, it's probably touching other roles' rows the same way when they use it,
not just whichever row happens to be yours that day.

— CIO
