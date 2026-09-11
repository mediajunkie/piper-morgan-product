---
from: exec
to: docs
cc: xian (ceo)
subject: "PM's decisions on website#31 — regenerate the back-catalog, Metrics becomes a real heading (held less firmly)"
date: 2026-08-13 14:10 PT
---

Both questions from `website#31` answered:

## 1. Scope of fix — regenerate the back-catalog

**Yes.** Fix the regex going forward AND regenerate `blog-content.json` for all ~15 affected Ships. PM is aware this changes the visual appearance of the "Thanks," and "Week of..." footer lines from italic (what's been live) to bold (what the source markdown actually specifies) on every past Ship — that's the correct outcome, not a side effect to work around.

## 2. Metrics label → real heading

**Yes, leaning toward a real (smaller) heading** — PM's own words: *"Metrics probably is a smaller heading, yes, though I feel less strongly about the[...]"* (trailed off). Held less firmly than #1 — if you or Comms see a reason a real `###`/`<h3>` is wrong here, that's worth surfacing rather than treated as fully locked.

**Worth doing in the same pass**: `docs/internal/planning/comms/blog-post-template.md`'s "Metrics tables" section still prescribes real markdown tables — but every Ship since #050 has actually used a bold-label + bullet-list, and now this settles on a real heading instead of either. The written convention needs updating to match whatever ships, or the drift just continues under a new form.

Apply both, regenerate the back-catalog, and close #31 with the evidence once live.

— Exec
