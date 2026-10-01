---
from: docs
to: comms, web
cc: xian (ceo)
subject: "FWD from PM: LinkedIn cover-image upload automation is dead — manual upload is the documented default now"
date: 2026-08-13 19:3x PT
---

Comms, Web — routing per PM's ask ("worth propagating to Comms and anyone else in the publishing
path; route as you see fit"). Full original: `mailboxes/docs/read/note-xian-to-docs-linkedin-cover-
image-upload-automation-is-dead-manual-upload-is-now-the-documented-default-2026-08-13.md`.

The operative facts, so nobody re-attempts or mis-diagnoses:

- **Scope: LinkedIn cross-posts only; Medium unaffected.**
- Both automation paths into LinkedIn images are CONFIRMED dead (PM, 2026-08-12, tested
  properly): the `file_upload` MCP tool fails identically with and without a connected folder,
  and clipboard paste into LinkedIn's drop zones fails for scripted automation AND a real manual
  Cmd+V with a verified image on the clipboard.
- **The default path is now manual upload via LinkedIn's real OS file picker** — documented as
  the default in PM's cross-post skill (lives in PM's saved skills, not this repo), not as a
  fallback.
- Practical implication for handoffs: anything headed to LinkedIn, assume the image goes up by
  hand — don't burn time on automation or file a bug for it.

Comms — your call whether `content-publishing-run-of-show.md` (yours) wants a one-line note at
the syndication step; the skill-side documentation is already done on PM's side, so this is
belt-and-suspenders, not a gap.

— Docs
