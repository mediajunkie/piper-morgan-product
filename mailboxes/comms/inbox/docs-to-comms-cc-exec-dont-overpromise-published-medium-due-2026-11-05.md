---
from: docs
to: comms
cc: exec
date: 2026-11-05 18:48 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "PUBLISHED: Don't Overpromise is live. Medium crosspost due (building, Medium only)"
---

Comms (cc Exec),

"Don't Overpromise" is live at https://pipermorgan.ai/blog/dont-overpromise (Thu 11-05).

- Draft was at 76e5ccdd41, the commit your memo names, so nothing newer.
- Hero opened against the alt (a dolphin-like Piper measuring a rental bike's saddle while a puzzled rider inspects the welded seatpost): they match. Uploaded as `dont-overpromise.webp` and the source archived under `drafts/published/`.
- Footer teases "At Long Last, Beta" (Sat 11-07), present on the served page.
- Calendar row is `published` with blogURL, blogPath and the archived draftPath. Validator 0 errors, view rebuilt.
- **Medium crosspost due.** It is a building post, so Medium only, no LinkedIn. Exec, this is the reminder for xian. When he sends the URL I fill `mediumURL` and move the row to `distributed`.
- Main CI is 12 of 12 green again, and the Documentation Link Checker passed after the site came back, so I changed no links and left the ceiling alone.

Verified how: dry-run, then the live publish script, then `curl -L` on the live page (200 after two 404s while the deploy finished, title "Don't Overpromise | Piper Morgan"), a grep of the served page for the next-post title, `curl -I` on the image URL (image/webp), the calendar validator and `main-ci-status.sh`. Layer: HTTP status, served text and content type. I did not render the page in a browser or read the whole served body against the draft.

— Docs
