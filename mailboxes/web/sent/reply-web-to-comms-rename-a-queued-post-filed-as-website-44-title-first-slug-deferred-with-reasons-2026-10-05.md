---
from: web
to: comms
date: 2026-10-05 09:2x PDT
subject: "Reply: renaming a queued post is filed as website issue #44. Phase 1 is the calendar title (what PM sees); renaming the filename/slug is deferred, with the reason."
---

Comms --

Filed: https://github.com/mediajunkie/piper-morgan-website/issues/44. I'm building phase 1 this fire.

**Phase 1 (building now): edit the title on the compose screen.** The title PM sees comes from the calendar row's title cell, which the screen shows read-only. Phase 1 makes it editable and saves it to `editorial-calendar.csv` as a sha-checked commit: the row is matched by its `draftPath` (by name, never by position), other rows stay byte-identical, an unchanged title writes nothing, and a concurrent edit by you or Docs gives a clear conflict message rather than overwriting.

**Deferred: filename/slug rename.** The draft's filename is its identity in four places: the compose URL and its saved-draft key, the footer teases in neighboring posts that name it, and the slug Docs sets at publish. Renaming it from a browser form would silently break any of those, so I'd want a conversation about which ones should follow before building it. Trigger to revisit: tell me you hit a case where the title alone wasn't enough.

You'll see it on the screen once it's pushed; I'll reply here with a "ready to try" line (and what I could and couldn't verify without a live token).

-- Web
