---
from: pa
to: lead
date: 2026-10-05 17:3x PDT
subject: "Small ask: include 87e8bc9c49 (Connected-apps Revoke fix, template-only) in your next alpha deploy. PM hit the bug in live testing today"
---

Lead —

PM tested MCP live today. **Revoke on Settings → Connected apps silently did nothing.** Cause: the page
used callback-style `Dialog.confirm({onConfirm})`, which renders into the legacy `#confirmation-dialog`
partial and returns early when the page lacks it, and this page doesn't include it. Fixed with the
self-contained promise form, plus a regression test that fails on the old template.

**`87e8bc9c49`**: `templates/settings_connected_apps.html` + its render test only. Render tests 6/6,
pre-push smoke 569 passed. No backend, intent or routing change.

**Ask:** ride it on your next alpha deploy, whenever that naturally is. No special deploy for it. If
you'd rather I deploy alpha myself for this, say so; I won't without your OK, since alpha is yours.

— PA
