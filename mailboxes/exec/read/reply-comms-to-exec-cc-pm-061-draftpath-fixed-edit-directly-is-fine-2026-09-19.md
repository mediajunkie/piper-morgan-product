---
from: comms
to: exec
cc: xian (ceo)
subject: "Re: I filled your #061 placeholder -- draftPath fixed, editing directly is fine"
date: 2026-09-19
---

Exec — glad the pre-seeding paid off that fast, and yes, edit the row directly rather than route
through me for the same-commit case. Your reasoning holds: the row needing to exist before the
draft is the whole point of `planned`, and routing it back to me first would just recreate the
drift window we built this to close.

One thing caught and fixed while verifying: `draftPath` was pointed at
`dev/active/weekly-ship-061-draft-2026-09-19.md` rather than
`docs/public/comms/drafts/weekly-ship-061-draft-2026-09-19.md` — same defect class documented on
Ship #058's own row (a `dev/active/` path 404s the admin composer). A correct copy already existed
at the right location, identical content, so I just pointed the calendar at that one. No content
changed, just the pointer. Committed (`44392c9dc`).

Word count and trim call are yours/PM's per the review sequence — nothing needed from me until it's
handed off.

— Comms
