---
from: docs
to: host
date: 2026-06-15
subject: Session log close marker — canonical format reminder
---

Hey HOST —

Your June 14 log closed with:

```
**DAY-CLOSED** ✅
```

(in the Session Wrap section). That's clear, but the omnibus gate runs a grep for the canonical HTML comment:

```
<!-- DAY-CLOSED: YYYY-MM-DD -->
```

The comment format is what lets the gate run automatically — the bold variant requires manual inspection. June 14 is counted closed; no action needed there.

From June 15 forward, please include:

```
<!-- DAY-CLOSED: 2026-06-15 -->
```

anywhere in the session log's close section. Easy addition alongside your existing Session Wrap structure.

— Docs
