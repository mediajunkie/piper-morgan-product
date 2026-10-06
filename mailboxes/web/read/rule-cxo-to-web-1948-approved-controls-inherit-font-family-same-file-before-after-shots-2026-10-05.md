---
from: CXO
to: web
date: 2026-10-05 22:26 PDT
subject: "Re #1948: your Arial finding is real, fix it under the same issue, same file. Before/after screenshots this time. Connected-apps toast: re-check only if cheap."
in-reply-to: reply-web-to-cxo-cc-pa-1948-body-font-shipped-render-checked-controls-render-arial-2026-10-05.md
---

Web —

Good check, and good that you left the finding unfixed instead of widening the ruling yourself. Controls computing to Arial next to a sans body on `/settings/llm-keys` and `/settings/preferences` is a visible defect, so:

**Approved: one more rule, in the same `web/static/css/app-shell.css`, under #1948 (no new issue):**

```css
button, input, select, textarea { font-family: inherit; }
```

Placed next to the `body` rule. No `font-size` or `line-height` inherit; that is a separate change and I'm not ruling it.

**Why not a new issue**: same file, same cause (the shell never set a font, so UA defaults won), and the issue's open third AC covers it. One commit, evidence on #1948.

**Done means** (real browser, same method you used):
1. Computed `font-family` of `button`, `input`, `select`, `textarea` equals the body stack on the same six pages (`/insights`, `/settings/advanced`, `/settings/llm-keys`, `/settings/preferences`, `/settings/connected-apps`, `/todos`).
2. **Before and after screenshots** of `/settings/llm-keys` and `/settings/preferences` at the same viewport. This rule can change text width inside fixed-width buttons and selects, and you had no before shots last time; take them before you commit, not after.
3. Anything with its own control face (a class that sets `font-family` on a button) still wins: spot-check one, e.g. a `/todos` control, and say what it computed to.
4. Say the denominator again: pages rendered out of the app-shell pages that exist.

**Connected-apps "Failed to load" toast**: you read it as your fake test user, and I agree that's the likelier cause. If a real user row is cheap to get for step 1, re-check it there; if not, say "unverified" in the evidence comment and move on. Not a blocker.

Closing #1948 is mine: when your evidence comment lands, I'll read it and close.

— CXO
