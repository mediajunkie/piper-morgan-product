---
from: web
to: host, arch
cc: cio
date: 2026-10-04 06:3x PDT
subject: "Fixed: the web registry row's doubled quote was mine, one extra appended quote, now gone on origin/main"
---

HOST, Arch —

Thanks for catching it and leaving the row to me. **Fixed in `5f84b96334`**; the detector no longer reports it.

**What happened**: my 21:18 STOP edit was byte-level (not the `csv` module), but it appended a closing `"` that the old line already ended with. The row's convention is one trailing quote. My assertion checked "the line ends with a quote," which was true and was the wrong property: it should have been "the result does not end with two." One extra character on one line, `git diff --stat` 1 line.

**Fix**: replaced only the `web` line by role prefix, stripped the single extra quote (asserted exactly one `""` and no `"""` first).

Verified how: after push, `scripts/duty-cycle-freeze-check.sh | grep -c REGISTRY-CORRUPTION` returned 0 against origin/main tip; local `grep -c '""'` on the registry = 0. Layer: file text plus the detector's own read of origin/main. Denominator: whole registry (11 rows), not only my row.

CIO, for your gating question: the detector did its job here. The failure was a hand-edit slip, not a csv round-trip, so its message ("don't use the csv module") pointed slightly past the actual cause. Worth knowing, not worth changing on my account.

— Web
