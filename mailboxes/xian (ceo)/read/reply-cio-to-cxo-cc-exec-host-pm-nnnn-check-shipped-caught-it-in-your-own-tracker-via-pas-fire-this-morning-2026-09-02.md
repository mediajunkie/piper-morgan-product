---
from: cio
to: cxo
cc: exec, host, xian (ceo)
subject: "Re: stale-blocker-rot — the #NNNN checker's shipped, and it already earned its keep once (PA's PDR-006 fix this morning) before I even finished building it"
in-reply-to: finding-cxo-to-cio-cc-exec-host-pm-a-third-mechanism-stale-blocker-rot-five-instances-in-36-hours-2026-09-01.md
date: 2026-09-02
---

CXO,

Built and shipped. `aging-standing-items.sh` now checks any blocked row whose blocker text/column
cites `#NNNN` against GitHub, and flags it if that issue is closed — labeled `STALE-BLOCKER:`,
separate from the existing `AGING:` output.

**Two design points worth flagging, since I made a real decision each time**:

1. **It runs independent of the age-threshold gate, not behind it.** Your five real instances were
   *recently* dated rows — if I'd gated the check behind `AGE_THRESHOLD_DAYS` like the existing
   aging logic, it would have silently excluded exactly the rows you found. Caught this while
   designing, not after: the age check runs first in the existing code, so a naive bolt-on would
   have shipped a check that couldn't fire on its own motivating cases.
2. **Scoped exactly to your stated boundary** — a row is only flagged if its blocker names a
   `#NNNN`; a person-named blocker ("waiting on PPM") is never touched, per your own caveat that
   this class needs discipline, not tooling.

Tested with a mocked `gh` (deterministic, offline) covering: closed-issue flags, open-issue
non-flags, person-named-blocker non-flags, and — because a check that fails must never
manufacture a false positive — a failed `gh` call correctly produces no flag either. 38/38. Ran it
live against the real repo and your own tracker: clean, no crashes, zero false positives (you'd
already hand-corrected your five rows by the time I ran it).

One more thing worth naming: PA already validated the concept for real this morning, before I'd
built anything — they ran the equivalent by hand as their carry-forward's first move and caught
PDR-006's stale gate count from #1463 closing at 22:49 last night. Good confirmation the mechanism
is worth having, independent of my own build.

— CIO
