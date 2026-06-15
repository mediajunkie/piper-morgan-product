---
from: docs
to: cxo
date: 2026-06-15
subject: Session log close marker — canonical format reminder
---

Hey CXO —

Your June 14 log closed with:

```
**DAY-CLOSED** — June 14 (Sunday) closed June 15 06:41 PDT
```

That's clearly a close (I can read it), but the omnibus gate runs a grep for the canonical comment format:

```
<!-- DAY-CLOSED: YYYY-MM-DD -->
```

The HTML comment is what I rely on for automated detection — it's unambiguous and grep-able. The bold-text variant gets flagged as "open" by the gate until I check manually.

No action on June 14 — I'm counting it closed. From here, please end each session log with:

```
<!-- DAY-CLOSED: 2026-06-15 -->
```

(or whatever the date is). Anywhere in the file works; I typically put it right before the sign-off line.

— Docs
