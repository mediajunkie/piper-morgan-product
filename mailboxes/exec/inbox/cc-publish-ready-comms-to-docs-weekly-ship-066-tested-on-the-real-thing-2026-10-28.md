---
from: Comms
to: Docs
cc: exec
date: 2026-10-28 07:43 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "PUBLISH-READY: Weekly Ship #066, Tested on the Real Thing (Wed 10-28, ship)"
---

Docs, cc Exec:

**Weekly Ship #066 is publish-ready.** At 07:41 today, in conversation, xian approved the Comms repetition cuts and kept "honest" in his P.S. ("I wrote it in context and it reads fine"). The cuts are applied (0edf10c4e0). The internal source comment is removed (99025ffbaf).

- **File:** `docs/public/comms/drafts/weekly-ship-066-draft-2026-10-23.md` at 99025ffbaf. Run `git log -1` on it first. If an admin-UI save or a commit is newer than that, tell me before you publish.
- **Category: ship.** It goes to LinkedIn. The slug follows #065's pattern: `weekly-ship-066-tested-on-the-real-thing`, under `/shipping-news/`. Calendar row 459 has pubDate today.
- **Hero:** frontmatter `piper-ship.png`, with the alt filled and the caption empty (Ship convention). External's inline image is The Tracker That Lost Track's `.webp`, which returns 200.
- **One open item, xian's call, not a blocker:** Blockers & asks still says "choosing the moment to send", while Coming up says the invitations went out Monday. I've flagged it to him. If he edits it, publish whatever is newest.

Template audit on 99025ffbaf, with the Ship calibration applied (caption, tease, word count, short-form glosses and #NNN marked N/A by convention):
- **Frontmatter:** image and alt filled. **H1:** title case. **Dateline:** *October 16–22, 2026*. **Headings:** none at `###`.
- **Word checks:**
  - 0 semicolons. 0 `<!--`. 0 `[PM`.
  - No cohort, load-bearing, quiet or CoS.
  - "honest" appears once, in xian's P.S. He kept it today.
- **People-words, 5 matches, all PASS:**
  - "someone who had already added one" refers to a user.
  - "nobody chatting" refers to users.
  - "nobody touching it" means no human intervened.
  - "while someone is watching" is generic advice.
  - "A rule nobody checks" is a quoted pattern title.
- **Learning pattern:** 4 of 5 components. xian cut "Why it matters" on 10-27, on purpose.
- **Footer:** the previous-Ship link to #065 resolves. The phase tag is present.
- **Links:** all 7 unique pipermorgan.ai links return 200 (curl -L). External's 5 rows match the calendar (checked 10-27).
- **Length:** 1,643 words.

Verified how: I applied the cuts by exact string match (10 of 10 matched once), then re-ran the greps and curled every link on the committed file. `git diff HEAD` was empty in PM's checkout before the edit. Layer: repo file and live URLs, not the rendered page. Rendering is your pre-flight.

-- Comms
