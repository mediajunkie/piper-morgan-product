---
from: comms
to: docs
cc: xian (ceo)
subject: "PUBLISH-READY — The Bug That Was Misdiagnosed Twice"
date: 2026-09-15 (Tuesday ~16:0x PT)
---

Today's beat (originally scheduled 9/15). Had a real thread along the way — PM was rewriting the
piece directly, hit a merge conflict against fixes I'd landed plus a compose-UI regression Web was
independently fixing at the same time. Full trail is in the calendar row's notes and today's
session log if useful context; summarizing the state here.

Reviewed in two passes:
- **Content pass** (post-merge-resolution): full `template-audit` (narrative theme, all 16
  checks). Fixed 3 real issues on close read — a lost blank line after the dateline, and two
  typos in PM's rewrite ("turned out to be have a different cause," "recommends copy"/"derivs the
  URL"). Verified the piece's central factual claims directly against the original Aug 19-20
  session logs rather than trust them, since accuracy is literally the story's subject: "81 of 81
  published posts," "0 of 81 frontmatter values matched," and "only two had ever visibly broken"
  (exactly Ship #054 and #056) all confirmed exact.
- **Final pass** (art landed): diffed the current version directly against the last commit I'd
  fully audited rather than re-read blind — confirmed the *only* change is the frontmatter, zero
  drift in body prose. Re-ran the full checklist end to end: image file verified present and valid
  (1672×941 PNG), YAML frontmatter syntactically sound, footer tease correct against the calendar
  ("The Week the Checks Started Checking Themselves"), 0 semicolons, no banned terms, no
  AI-writing tics, no placeholder brackets. 610 words.

Calendar row updated: status `drafted` -> `ready-for-docs`, notes carry the full trail. Draft:
`docs/public/comms/drafts/the-bug-that-was-misdiagnosed-twice.md`.

Ready for your proofread + publish.

— Comms
