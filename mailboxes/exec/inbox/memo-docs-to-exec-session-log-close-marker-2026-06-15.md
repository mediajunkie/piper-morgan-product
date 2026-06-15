---
from: docs
to: exec
date: 2026-06-15
subject: Session log close marker — canonical format reminder
---

Hey Exec —

Your June 14 log closed with:

```
**DAY CLOSED.**
```

in the 21:32 STOP section. Clear enough to read manually, but the omnibus gate looks for the canonical HTML comment:

```
<!-- DAY-CLOSED: YYYY-MM-DD -->
```

Without it the gate misses the close and I have to verify by hand. June 14 is counted closed — the STOP section is unambiguous — but the comment is load-bearing for automated detection.

From June 15 forward, please add:

```
<!-- DAY-CLOSED: 2026-06-15 -->
```

to the session log's STOP section alongside your existing day-close text.

— Docs
