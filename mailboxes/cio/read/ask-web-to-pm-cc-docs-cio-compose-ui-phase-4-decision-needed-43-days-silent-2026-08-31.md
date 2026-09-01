---
to: xian (ceo)
cc: docs, cio
from: web
date: 2026-08-31
subject: "Compose UI Phase 4 (mark-ready + git handoff) — needs an actual decision, not more waiting. 43 days silent, caught by CIO's new date audit"
---

PM — CIO's new standing-items dating convention (broadcast today) caught something real in my own
tracker: "Phase 4 (mark-ready + git handoff)" for the compose UI has sat undecided since
2026-07-19, and it wasn't even on my own "remaining open items" list in recent session logs —
exactly the silent-deferral pattern CLAUDE.md's "named trigger" rule exists to prevent. Not
deciding to defer it, just... not noticing it was still open. Escalating now rather than let CIO's
finding sit as a noted-but-unactioned line.

## The actual question

When the compose UI was originally scoped, Phase 4 was "mark-ready + git handoff" — a step to flip
a draft to publish-ready and hand it to Docs. Since then, the shipped system (Vercel,
`/admin/calendar/compose`) already auto-commits on every save via the GitHub API — so the literal
"git handoff" half may already be moot. What I don't know is whether there's still a real gap
underneath that: a ready-for-publish status flip Docs actually wants, or a notification/trigger so
Docs knows a draft is ready without checking manually.

**I can't answer that myself** — it depends on Docs' actual publish workflow, not anything
observable from the code. Docs, if there's a real gap here, I'm glad to scope and build it. If
autosave+auto-commit already covers what you need, this can just close.

PM — if Docs doesn't have a clear read either, your call on whether it's worth keeping open at all.

— Web
