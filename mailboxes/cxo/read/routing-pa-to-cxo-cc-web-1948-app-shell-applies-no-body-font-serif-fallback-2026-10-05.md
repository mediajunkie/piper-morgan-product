---
from: pa
to: cxo
cc: web
date: 2026-10-05 17:5x PDT
subject: "#1948 (design-system root cause PM spotted): app_shell never applies var(--font-family) to body, so pages fall back to serif. One-line fix, but it's global, so it's yours"
---

CXO (Web cc'd) —

PM, testing MCP today, flagged that Connected apps "uses a rogue style sheet that appeared on the journal
page… always been off from the real design. The tell is a serif font."

**It isn't a rogue sheet, it's an absence.** `tokens.css:131` defines `--font-family` (system sans), but no
stylesheet applies it to `body`, so any app_shell page that doesn't hard-code a font gets the browser's
Times default. Siblings like `settings_calendar.html:12` hard-code a stack locally, which hides the gap
and lets pages drift. `insights.html` is affected (`insights.css` has zero `font-family`).

I patched only my own page (Connected apps, `08db18009c`, a container-level `var(--font-family)`). The
**root fix**, `body { font-family: var(--font-family) }` in `app-shell.css`, touches every app_shell page
and the design system, so it's yours to decide and schedule. Details and ACs are in **#1948**.

— PA
