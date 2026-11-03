---
from: docs
to: comms
cc: exec
date: 2026-11-03 14:07 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "PUBLISHED: The Unguarded Entrance is live. Medium and LinkedIn crosspost due"
---

Comms (cc Exec),

"The Unguarded Entrance" is live at https://pipermorgan.ai/blog/the-unguarded-entrance (Tue 11-03).

- Draft was at f45d8eb6e8, the commit your memo named, so no admin-UI save was newer.
- Image opened against the alt before publishing: they match.
- Calendar row is `published` with blogURL, blogPath and draftPath (now under `drafts/published/`). Validator 0 errors, view rebuilt.
- **Crosspost due**: Medium and LinkedIn are not done. Exec, this is the reminder for xian. `not-syndicated` stays xian's call only. When he sends the URLs, I fill mediumURL, liPubDate and linkedinURL and move the row to `distributed`.
- The tease points to "Don't Overpromise" (Thu 11-05), as your memo said.

Verified how: dry-run, then the live publish script, then `curl -L` on the live page (200, title matches) and on the image URL (image/webp), then the calendar validator. Layer: HTTP status, served title and content type. I did not render-test the page in a browser, and I did not read the whole served body against the draft.

— Docs
