---
from: xian (ceo)
to: docs
subject: "LinkedIn cover-image upload automation is dead — manual upload is now the documented default"
date: 2026-08-13 PT
---

Relayed from a Cowork session (no filesystem access to this repo), so this is arriving via a
general-purpose Claude Code agent rather than a cohort seat.

**Scope: LinkedIn cross-posts only. Medium is unaffected** — nothing in the Medium path changed.

## What's broken

Two independent image paths into LinkedIn are both dead:

1. **`file_upload` MCP tool — broken at the session level.** Every call fails with the same error:
   *"file_upload can't accept pre-read files in this session; it only takes paths of files in folders
   the user has connected to the session."* Confirmed twice on **2026-08-12** — once with no folder
   connected, once **after** connecting a folder. **Identical error both times**, so this is not a
   connected-folder configuration issue and connecting a folder does not fix it. The failure is
   independent of the input path.

2. **Clipboard paste into LinkedIn's drop zones — confirmed dead end.** This covers both the
   cover-image drop zone and the in-body image drop zone, and it fails for **both** scripted
   automation **and** a real manual Cmd+V by me at the keyboard. I verified a real image was on the
   OS clipboard and the paste still didn't take.

## Current standing workaround

**Manual upload through LinkedIn's real "Upload from computer" OS file picker.** The `cross-post`
skill (which lives in my saved skills, not in this repo) has already been corrected to document this
as the **default** path going forward — not as a fallback after automation fails.

## Why you're getting this

So nobody on the team drafting or publishing content that lands on LinkedIn burns time re-attempting
automation that's already been ruled out, or diagnoses this as a bug on their end. It isn't — it's
the current reality of the tooling. If you're handing a post off for LinkedIn, assume the image goes
up by hand.

Worth propagating to Comms and anyone else in the publishing path; I sent this to Docs only, so
route as you see fit.

— xian
